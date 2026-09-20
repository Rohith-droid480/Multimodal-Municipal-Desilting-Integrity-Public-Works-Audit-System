"""Tests for MuniAudit-AI Evidence Fusion Subsystem.

Validates Subjective Logic mathematical invariants, consensus operator, modality mappers,
Tier 1 hard gates, Tier 2 soft evidential fusion, missing modality semantics, and
Leave-One-Out (LOO) modality attributions.
"""

from __future__ import annotations

import math
from uuid import uuid4

import pytest

from app.domain.epistemic import AdministrativeState, EpistemicCategory
from app.domain.models import Dossier
from app.fusion.engine import (
    ConfidenceTier,
    PriorityTier,
    determine_confidence_tier,
    determine_priority_tier,
    fuse_dossier_evidence,
)
from app.fusion.mappers import (
    map_geospatial_kinematics_to_opinion,
    map_ocr_extraction_to_opinion,
    map_silt_density_to_opinion,
    map_temporal_sequence_to_opinion,
    map_visual_similarity_to_opinion,
)
from app.fusion.subjective_logic import (
    SubjectiveOpinion,
    create_opinion,
    dogmatic_opinion,
    fuse_opinions,
    vacuous_opinion,
)
from app.ingestion.benchmark_loader import BenchmarkDossierLoader, BenchmarkDossierType
from app.rules.base import RuleEvaluationResult
from app.storage.interface import LocalStorageAdapter

# ---------------------------------------------------------------------------
# 1. Subjective Logic Mathematical Invariant Tests
# ---------------------------------------------------------------------------


def test_subjective_opinion_sum_to_one() -> None:
    """Validate that valid SubjectiveOpinion components strictly sum to 1.0."""
    op = SubjectiveOpinion(belief=0.3, disbelief=0.5, uncertainty=0.2, base_rate=0.5)
    assert math.isclose(op.belief + op.disbelief + op.uncertainty, 1.0, abs_tol=1e-5)
    assert math.isclose(op.expected_value, 0.3 + 0.5 * 0.2, abs_tol=1e-5)


def test_subjective_opinion_normalization_failure() -> None:
    """Validate that unnormalized opinion raises ValueError."""
    with pytest.raises(ValueError, match="Subjective opinion components must sum to 1.0"):
        SubjectiveOpinion(belief=0.8, disbelief=0.8, uncertainty=0.5)


def test_create_opinion_safe_normalization() -> None:
    """Validate that create_opinion automatically normalizes unscaled inputs."""
    op = create_opinion(belief=2.0, disbelief=2.0, uncertainty=1.0)
    assert math.isclose(op.belief, 0.4, abs_tol=1e-4)
    assert math.isclose(op.disbelief, 0.4, abs_tol=1e-4)
    assert math.isclose(op.uncertainty, 0.2, abs_tol=1e-4)


def test_vacuous_opinion_neutral_identity() -> None:
    """Validate that vacuous opinion (u=1.0) is the neutral identity element under ⊕."""
    vacuous = vacuous_opinion()
    opinion_a = create_opinion(belief=0.6, disbelief=0.2, uncertainty=0.2)

    # ω_A ⊕ vacuous == ω_A
    fused = fuse_opinions(opinion_a, vacuous)
    assert math.isclose(fused.belief, opinion_a.belief, abs_tol=1e-4)
    assert math.isclose(fused.disbelief, opinion_a.disbelief, abs_tol=1e-4)
    assert math.isclose(fused.uncertainty, opinion_a.uncertainty, abs_tol=1e-4)


def test_consensus_operator_commutativity() -> None:
    """Validate that consensus fusion is commutative: ω_A ⊕ ω_B == ω_B ⊕ ω_A."""
    op_a = create_opinion(belief=0.4, disbelief=0.3, uncertainty=0.3)
    op_b = create_opinion(belief=0.1, disbelief=0.6, uncertainty=0.3)

    fused_ab = fuse_opinions(op_a, op_b)
    fused_ba = fuse_opinions(op_b, op_a)

    assert math.isclose(fused_ab.belief, fused_ba.belief, abs_tol=1e-4)
    assert math.isclose(fused_ab.disbelief, fused_ba.disbelief, abs_tol=1e-4)
    assert math.isclose(fused_ab.uncertainty, fused_ba.uncertainty, abs_tol=1e-4)


def test_consensus_operator_associativity() -> None:
    """Validate that consensus fusion is associative: (ω_A ⊕ ω_B) ⊕ ω_C == ω_A ⊕ (ω_B ⊕ ω_C)."""
    op_a = create_opinion(belief=0.5, disbelief=0.2, uncertainty=0.3)
    op_b = create_opinion(belief=0.2, disbelief=0.5, uncertainty=0.3)
    op_c = create_opinion(belief=0.1, disbelief=0.4, uncertainty=0.5)

    left = fuse_opinions(fuse_opinions(op_a, op_b), op_c)
    right = fuse_opinions(op_a, fuse_opinions(op_b, op_c))

    assert math.isclose(left.belief, right.belief, abs_tol=1e-3)
    assert math.isclose(left.disbelief, right.disbelief, abs_tol=1e-3)
    assert math.isclose(left.uncertainty, right.uncertainty, abs_tol=1e-3)


def test_dogmatic_opinions_boundary() -> None:
    """Validate that fusing two dogmatic opinions (u=0) avoids ZeroDivisionError."""
    op_a = dogmatic_opinion(belief=0.8)
    op_b = dogmatic_opinion(belief=0.4)

    fused = fuse_opinions(op_a, op_b)
    assert math.isclose(fused.uncertainty, 0.0, abs_tol=1e-4)
    assert math.isclose(fused.belief, 0.6, abs_tol=1e-4)


def test_zadeh_paradox_resilience() -> None:
    """Validate that conflicting opinions pool uncertainty instead of fabricating false certainty."""
    # Sensor 1: high belief in anomaly
    op_1 = create_opinion(belief=0.85, disbelief=0.05, uncertainty=0.10)
    # Sensor 2: high disbelief in anomaly (belief in compliance)
    op_2 = create_opinion(belief=0.05, disbelief=0.85, uncertainty=0.10)

    fused = fuse_opinions(op_1, op_2)
    # Both beliefs balance, and uncertainty remains well above zero
    assert math.isclose(fused.belief, fused.disbelief, abs_tol=1e-2)
    assert fused.uncertainty > 0.0


# ---------------------------------------------------------------------------
# 2. Modality Mapper Tests
# ---------------------------------------------------------------------------


def test_map_visual_similarity_near_duplicate() -> None:
    """Validate that visual similarity >= 0.85 yields high belief in anomaly."""
    op = map_visual_similarity_to_opinion(similarity=0.92, duplicate_threshold=0.85)
    assert op.belief >= 0.50
    assert op.disbelief == 0.0


def test_map_visual_similarity_distinct() -> None:
    """Validate that visual similarity < 0.70 yields high disbelief in anomaly (compliance)."""
    op = map_visual_similarity_to_opinion(similarity=0.45)
    assert op.disbelief >= 0.60
    assert op.belief == 0.0


def test_map_visual_similarity_missing_is_vacuous() -> None:
    """Validate that missing visual telemetry yields vacuous opinion."""
    op = map_visual_similarity_to_opinion(similarity=None)
    assert op.uncertainty == 1.0
    assert op.belief == 0.0
    assert op.disbelief == 0.0


def test_map_ocr_extraction_high_confidence() -> None:
    """Validate that clear weighbridge OCR yields high compliance disbelief."""
    op = map_ocr_extraction_to_opinion(mean_confidence=0.95, field_completeness=1.0)
    assert op.disbelief >= 0.70
    assert op.belief == 0.0


def test_map_ocr_extraction_degraded_increases_uncertainty() -> None:
    """Validate that degraded OCR yields high uncertainty rather than false accusation."""
    op = map_ocr_extraction_to_opinion(mean_confidence=0.20, field_completeness=0.5)
    assert op.uncertainty >= 0.80
    assert op.belief == 0.0


def test_map_geospatial_kinematics() -> None:
    """Validate apparent transit speed opinion mapping."""
    # Normal urban transit
    op_normal = map_geospatial_kinematics_to_opinion(apparent_speed_kmh=42.0)
    assert op_normal.disbelief >= 0.75
    assert op_normal.belief == 0.0

    # Approaching limit (75 km/h)
    op_elevated = map_geospatial_kinematics_to_opinion(apparent_speed_kmh=75.0)
    assert op_elevated.belief > 0.40

    # Missing
    op_none = map_geospatial_kinematics_to_opinion(apparent_speed_kmh=None)
    assert op_none.uncertainty == 1.0


def test_map_silt_density() -> None:
    """Validate silt bulk density opinion mapping."""
    # Standard wet silt
    op_std = map_silt_density_to_opinion(apparent_density_t_m3=1.35)
    assert op_std.disbelief >= 0.80

    # Approaching saturation limit
    op_high = map_silt_density_to_opinion(apparent_density_t_m3=1.80)
    assert op_high.belief > 0.40

    # Missing
    op_none = map_silt_density_to_opinion(apparent_density_t_m3=None)
    assert op_none.uncertainty == 1.0


def test_map_temporal_sequence() -> None:
    """Validate chronological sequence opinion mapping."""
    op_inversion = map_temporal_sequence_to_opinion(has_inversion=True, timestamps_count=5)
    assert op_inversion.belief >= 0.85

    op_ok = map_temporal_sequence_to_opinion(has_inversion=False, timestamps_count=5)
    assert op_ok.disbelief >= 0.80

    op_insufficient = map_temporal_sequence_to_opinion(has_inversion=False, timestamps_count=1)
    assert op_insufficient.uncertainty == 1.0


# ---------------------------------------------------------------------------
# 3. Triage Tier & Confidence Functions
# ---------------------------------------------------------------------------


def test_determine_confidence_tier() -> None:
    """Validate confidence tier thresholds."""
    assert determine_confidence_tier(0.10) == ConfidenceTier.VERY_HIGH
    assert determine_confidence_tier(0.25) == ConfidenceTier.HIGH
    assert determine_confidence_tier(0.50) == ConfidenceTier.MODERATE
    assert determine_confidence_tier(0.70) == ConfidenceTier.LOW
    assert determine_confidence_tier(0.90) == ConfidenceTier.INSUFFICIENT_DATA


def test_determine_priority_tier() -> None:
    """Validate priority tier categorization."""
    assert determine_priority_tier(15.0, hard_gate=False) == PriorityTier.LOW
    assert determine_priority_tier(35.0, hard_gate=False) == PriorityTier.MEDIUM
    assert determine_priority_tier(60.0, hard_gate=False) == PriorityTier.HIGH
    assert determine_priority_tier(80.0, hard_gate=False) == PriorityTier.CRITICAL
    assert determine_priority_tier(10.0, hard_gate=True) == PriorityTier.CRITICAL


# ---------------------------------------------------------------------------
# 4. End-to-End Two-Tier Evidence Fusion Tests
# ---------------------------------------------------------------------------


def test_tier_1_hard_gate_on_substantive_inconsistency() -> None:
    """Validate that Tier 1 hard gate halts immediately with CRITICAL priority and ARPI 100.0."""
    dossier = Dossier(
        dossier_id=uuid4(),
        tenant_id="BBMP-TEST",
        work_order_id="WO-HARDGATE-01",
        contractor_id="CONT-01",
        claimed_amount_inr=500000.0,
        evidence_items=[],
    )

    hard_rule = RuleEvaluationResult(
        rule_id="R-001-MASS-BALANCE",
        rule_name="Weighbridge Mass Balance Verification",
        status=AdministrativeState.SUBSTANTIVE_INCONSISTENCY,
        observed_value="Gross=10000 kg, Tare=4000 kg, Net=8000 kg",
        expected_value="Net=6000 kg",
        discrepancy_delta=2000.0,
        tolerance=20.0,
        justification="Mass balance arithmetic mismatch exceeds tolerance",
    )

    result = fuse_dossier_evidence(dossier, rule_results=[hard_rule])

    assert result.hard_gate_violation is True
    assert result.hard_gate_rule_id == "R-001-MASS-BALANCE"
    assert result.priority_tier == PriorityTier.CRITICAL
    assert result.audit_review_priority_index == 100.0
    assert result.evidence_consistency_score <= 0.10
    assert result.epistemic_category == EpistemicCategory.INFERENCE
    assert "TIER 1 HARD GATE ACTIVATED" in result.summary_justification


def test_tier_2_clean_benchmark_dossier(tmp_path: pytest.TempPathFactory) -> None:
    """Validate that clean benchmark dossier achieves high ECS, low ARPI, and LOW priority."""
    storage = LocalStorageAdapter(str(tmp_path))
    loader = BenchmarkDossierLoader(storage_adapter=storage)
    clean_dossier = loader.build_benchmark_dossier(BenchmarkDossierType.CLEAN_COMPLIANT)

    result = fuse_dossier_evidence(
        clean_dossier,
        visual_similarity=0.45,  # Distinct site photos
        ocr_confidence=0.92,
    )

    assert result.hard_gate_violation is False
    assert result.hard_gate_rule_id is None
    assert result.evidence_consistency_score >= 0.70
    assert result.priority_tier in (PriorityTier.LOW, PriorityTier.MEDIUM)
    assert result.audit_review_priority_index < 50.0
    assert result.confidence_tier in (
        ConfidenceTier.VERY_HIGH,
        ConfidenceTier.HIGH,
        ConfidenceTier.MODERATE,
    )
    assert result.epistemic_category == EpistemicCategory.INFERENCE


def test_tier_2_inconsistent_benchmark_dossier(tmp_path: pytest.TempPathFactory) -> None:
    """Validate that inconsistent benchmark dossier triggers hard gate on physical density."""
    storage = LocalStorageAdapter(str(tmp_path))
    loader = BenchmarkDossierLoader(storage_adapter=storage)
    inconsistent_dossier = loader.build_benchmark_dossier(
        BenchmarkDossierType.SUBSTANTIVE_INCONSISTENCY
    )

    result = fuse_dossier_evidence(inconsistent_dossier)

    # Inconsistent benchmark has impossible haul weight 46,500 kg in 10 m³ (density 4.65 t/m³ > 1.90)
    assert result.hard_gate_violation is True
    assert result.priority_tier == PriorityTier.CRITICAL
    assert result.audit_review_priority_index == 100.0


def test_tier_2_inconclusive_missing_modalities_safe_failure(
    tmp_path: pytest.TempPathFactory,
) -> None:
    """Validate that dossier with missing telemetry evaluates non-punitively with high uncertainty."""
    storage = LocalStorageAdapter(str(tmp_path))
    loader = BenchmarkDossierLoader(storage_adapter=storage)
    inconclusive_dossier = loader.build_benchmark_dossier(
        BenchmarkDossierType.INCONCLUSIVE_DATA
    )

    result = fuse_dossier_evidence(inconclusive_dossier)

    # Must NOT trigger hard gate violation or accusation of fraud
    assert result.hard_gate_violation is False
    assert len(result.missing_modalities) > 0
    assert result.confidence_tier in (
        ConfidenceTier.MODERATE,
        ConfidenceTier.LOW,
        ConfidenceTier.INSUFFICIENT_DATA,
    )
    assert "TIER 2 SOFT FUSION" in result.summary_justification


def test_leave_one_out_attribution_isolates_visual_duplicate() -> None:
    """Validate that LOO attribution correctly attributes inconsistency to visual duplication."""
    dossier = Dossier(
        dossier_id=uuid4(),
        tenant_id="BBMP-TEST",
        work_order_id="WO-LOO-01",
        contractor_id="CONT-01",
        claimed_amount_inr=200000.0,
        evidence_items=[],
    )

    # Pass normal compliant rule results
    compliant_rule = RuleEvaluationResult(
        rule_id="R-001-MASS-BALANCE",
        rule_name="Weighbridge Mass Balance Verification",
        status=AdministrativeState.VERIFIED_COMPLIANT,
        observed_value="Gross=15000 kg, Tare=5000 kg, Net=10000 kg",
        expected_value="Net=10000 kg",
        tolerance=20.0,
        justification="Compliant",
    )

    # Pass high visual similarity (potential near-duplicate photo reuse)
    result = fuse_dossier_evidence(
        dossier,
        rule_results=[compliant_rule],
        visual_similarity=0.96,  # Strong duplicate signal
        ocr_confidence=0.90,
    )

    assert result.hard_gate_violation is False
    # Visual modality should have the largest marginal attribution to inconsistency
    visual_attr = result.modality_attributions.get("visual", 0.0)
    assert visual_attr > 0.50
