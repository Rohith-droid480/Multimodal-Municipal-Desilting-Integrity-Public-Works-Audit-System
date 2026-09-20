"""MuniAudit-AI — Two-Tier Uncertainty-Aware Evidence Fusion Engine.

Combines Tier 1 deterministic civil engineering hard gates with Tier 2 Subjective
Logic consensus opinion fusion. Computes the Evidence Consistency Score (ECS),
Audit Review Priority Index (ARPI), Epistemic Confidence Tier, and Leave-One-Out
Modality Attribution Vector.

Adheres strictly to Locked Architecture v1.0 and Section 31-34 epistemic standards.
"""

from __future__ import annotations

import math
from datetime import UTC, datetime
from enum import Enum
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field

from app.domain.epistemic import AdministrativeState, EpistemicCategory
from app.domain.models import Dossier
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
    fuse_multi_opinions,
    vacuous_opinion,
)
from app.rules.base import RuleEvaluationResult
from app.rules.runner import evaluate_dossier_rules


class PriorityTier(str, Enum):
    """Audit review triage priority tiers."""

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class ConfidenceTier(str, Enum):
    """Epistemic confidence tiers based on uncertainty mass u."""

    VERY_HIGH = "VERY_HIGH"
    HIGH = "HIGH"
    MODERATE = "MODERATE"
    LOW = "LOW"
    INSUFFICIENT_DATA = "INSUFFICIENT_DATA"


class FusionResult(BaseModel):
    """Composite evidence fusion evaluation for an audit dossier."""

    dossier_id: UUID = Field(..., description="Target dossier identifier")
    epistemic_category: EpistemicCategory = Field(
        default=EpistemicCategory.INFERENCE,
        description="Strict epistemic classification: INFERENCE",
    )
    evidence_consistency_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Evidence Consistency Score (ECS) in [0.0, 1.0]",
    )
    audit_review_priority_index: float = Field(
        ...,
        ge=0.0,
        le=100.0,
        description="Continuous Audit Review Priority Index (ARPI) in [0.0, 100.0]",
    )
    priority_tier: PriorityTier = Field(..., description="Categorical triage tier")
    confidence_tier: ConfidenceTier = Field(..., description="Epistemic confidence tier")
    fused_opinion: SubjectiveOpinion = Field(..., description="Subjective Logic consensus opinion")
    modality_attributions: dict[str, float] = Field(
        default_factory=dict,
        description="Leave-one-out marginal inconsistency contributions",
    )
    missing_modalities: list[str] = Field(
        default_factory=list,
        description="List of telemetry channels lacking sufficient data",
    )
    hard_gate_violation: bool = Field(
        default=False,
        description="True if an incontrovertible metrological violation triggered a Tier 1 halt",
    )
    hard_gate_rule_id: str | None = Field(
        default=None,
        description="Rule ID responsible for triggering the Tier 1 hard gate",
    )
    rule_results: list[RuleEvaluationResult] = Field(
        default_factory=list,
        description="Deterministic rule evaluation records",
    )
    summary_justification: str = Field(..., description="Detailed audit narrative and rationale")
    evaluated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Timezone-aware UTC timestamp of evaluation",
    )


def determine_confidence_tier(uncertainty: float) -> ConfidenceTier:
    """Categorize the total uncertainty mass u into an operational confidence tier."""
    if uncertainty <= 0.15:
        return ConfidenceTier.VERY_HIGH
    if uncertainty <= 0.35:
        return ConfidenceTier.HIGH
    if uncertainty <= 0.60:
        return ConfidenceTier.MODERATE
    if uncertainty <= 0.85:
        return ConfidenceTier.LOW
    return ConfidenceTier.INSUFFICIENT_DATA


def determine_priority_tier(arpi: float, hard_gate: bool) -> PriorityTier:
    """Categorize continuous ARPI into a triage review tier."""
    if hard_gate or arpi >= 75.0:
        return PriorityTier.CRITICAL
    if arpi >= 50.0:
        return PriorityTier.HIGH
    if arpi >= 25.0:
        return PriorityTier.MEDIUM
    return PriorityTier.LOW


def _extract_modality_parameters(
    dossier: Dossier,
    rule_results: list[RuleEvaluationResult],
) -> dict[str, Any]:
    """Extract raw scalar signals from dossier evidence items and rule evaluation results."""
    params: dict[str, Any] = {
        "visual_similarity": None,
        "ocr_confidence": None,
        "apparent_speed_kmh": None,
        "apparent_density_t_m3": None,
        "has_temporal_inversion": False,
        "temporal_timestamps_count": 0,
    }

    # 1. Inspect evidence items
    for item in dossier.evidence_items:
        meta = getattr(item, "metadata", None) or getattr(item, "metadata_json", None) or {}
        if "visual_similarity" in meta and params["visual_similarity"] is None:
            params["visual_similarity"] = float(meta["visual_similarity"])
        if "ocr_confidence" in meta and params["ocr_confidence"] is None:
            params["ocr_confidence"] = float(meta["ocr_confidence"])
        if "mean_confidence" in meta and params["ocr_confidence"] is None:
            params["ocr_confidence"] = float(meta["mean_confidence"])

    # 2. Inspect rule results
    for res in rule_results:
        if res.rule_id == "R-002-GEOSPATIAL-SPEED" and res.observed_value is not None:
            try:
                val_str = str(res.observed_value).replace(" km/h", "").strip()
                params["apparent_speed_kmh"] = float(val_str)
            except ValueError:
                pass
        elif res.rule_id == "R-003-PHYSICAL-DENSITY" and res.observed_value is not None:
            try:
                val_str = str(res.observed_value).replace(" t/m³", "").replace(" t/m3", "").strip()
                params["apparent_density_t_m3"] = float(val_str)
            except ValueError:
                pass
        elif res.rule_id == "R-004-TEMPORAL-SEQUENCE":
            if res.status == AdministrativeState.INCONCLUSIVE_DATA:
                params["temporal_timestamps_count"] = 0
            elif res.status == AdministrativeState.SUBSTANTIVE_INCONSISTENCY:
                params["has_temporal_inversion"] = True
                params["temporal_timestamps_count"] = 5
            elif res.status == AdministrativeState.VERIFIED_COMPLIANT:
                params["has_temporal_inversion"] = False
                params["temporal_timestamps_count"] = 5

    return params


def compute_leave_one_out_attributions(
    modality_opinions: dict[str, SubjectiveOpinion],
    fused_opinion: SubjectiveOpinion,
) -> dict[str, float]:
    """Calculate the marginal inconsistency contribution of each active modality via leave-one-out."""
    if not modality_opinions or fused_opinion.belief <= 1e-6:
        return {k: 0.0 for k in modality_opinions}

    raw_contributions: dict[str, float] = {}
    for mod_name in modality_opinions:
        # Fuse all other modalities excluding mod_name
        other_opinions = [op for name, op in modality_opinions.items() if name != mod_name]
        fused_without = fuse_multi_opinions(other_opinions)
        # Marginal belief drop when removing mod_name
        marginal_delta = max(0.0, fused_opinion.belief - fused_without.belief)
        raw_contributions[mod_name] = marginal_delta

    total_delta = sum(raw_contributions.values())
    if total_delta > 1e-6:
        return {k: round(v / total_delta, 4) for k, v in raw_contributions.items()}

    # Equal allocation if negligible individual delta
    equal_share = round(1.0 / len(modality_opinions), 4)
    return {k: equal_share for k in modality_opinions}


def fuse_dossier_evidence(
    dossier: Dossier,
    rule_results: list[RuleEvaluationResult] | None = None,
    visual_similarity: float | None = None,
    ocr_confidence: float | None = None,
) -> FusionResult:
    """Execute two-tier evidence fusion on an audit dossier.

    Tier 1 (Deterministic Hard Gates):
        Inspects deterministic rule results for SUBSTANTIVE_INCONSISTENCY.
        If found, immediately halts to Tier 1 violation status (ARPI = 100.0, CRITICAL).

    Tier 2 (Soft Evidential Fusion):
        Transforms multimodal telemetry into Subjective Logic opinions.
        Fuses opinions via Jøsang consensus operator to obtain ECS and ARPI.
    """
    # 1. Run deterministic rules if not supplied
    if rule_results is None:
        rule_results = evaluate_dossier_rules(dossier)

    # 2. Tier 1: Check for Hard Gate Violations
    hard_gate_violation = False
    hard_gate_rule_id: str | None = None
    violation_justifications: list[str] = []

    for rule in rule_results:
        if rule.status == AdministrativeState.SUBSTANTIVE_INCONSISTENCY:
            hard_gate_violation = True
            if hard_gate_rule_id is None:
                hard_gate_rule_id = rule.rule_id
            violation_justifications.append(f"[{rule.rule_id}] {rule.justification}")

    # 3. Extract telemetry parameters
    extracted = _extract_modality_parameters(dossier, rule_results)
    sim = visual_similarity if visual_similarity is not None else extracted["visual_similarity"]
    ocr_conf = ocr_confidence if ocr_confidence is not None else extracted["ocr_confidence"]
    speed = extracted["apparent_speed_kmh"]
    density = extracted["apparent_density_t_m3"]
    has_inversion = extracted["has_temporal_inversion"]
    ts_count = extracted["temporal_timestamps_count"]

    # 4. Map signals to Subjective Opinions and track missing modalities
    modality_opinions: dict[str, SubjectiveOpinion] = {}
    missing_modalities: list[str] = []

    # Visual Modality
    if sim is None:
        missing_modalities.append("visual_similarity")
        op_visual = vacuous_opinion()
    else:
        op_visual = map_visual_similarity_to_opinion(sim)
    modality_opinions["visual"] = op_visual

    # OCR Modality
    if ocr_conf is None:
        missing_modalities.append("weighbridge_ocr")
        op_ocr = vacuous_opinion()
    else:
        op_ocr = map_ocr_extraction_to_opinion(ocr_conf)
    modality_opinions["ocr"] = op_ocr

    # Geospatial Modality
    if speed is None:
        missing_modalities.append("geospatial_telemetry")
        op_geo = vacuous_opinion()
    else:
        op_geo = map_geospatial_kinematics_to_opinion(speed)
    modality_opinions["geospatial"] = op_geo

    # Physical Density Modality
    if density is None:
        missing_modalities.append("physical_density")
        op_density = vacuous_opinion()
    else:
        op_density = map_silt_density_to_opinion(density)
    modality_opinions["density"] = op_density

    # Temporal Sequence Modality
    if ts_count < 2:
        missing_modalities.append("temporal_sequence")
        op_temp = vacuous_opinion()
    else:
        op_temp = map_temporal_sequence_to_opinion(has_inversion, ts_count)
    modality_opinions["temporal"] = op_temp

    # 5. Execute Subjective Logic Consensus Fusion
    all_opinions = list(modality_opinions.values())
    fused_op = fuse_multi_opinions(all_opinions)

    # If telemetry channels are missing, dilute fused certainty proportionately
    total_modalities = len(modality_opinions)
    available_count = total_modalities - len(missing_modalities)
    if total_modalities > 0 and available_count < total_modalities:
        ratio = available_count / total_modalities
        b_adj = fused_op.belief * ratio
        d_adj = fused_op.disbelief * ratio
        u_adj = 1.0 - b_adj - d_adj
        fused_op = create_opinion(b_adj, d_adj, u_adj, base_rate=fused_op.base_rate)

    # 6. Compute Evidence Consistency Score (ECS)
    # ECS = d + a * u in [0.0, 1.0]
    raw_ecs = fused_op.disbelief + (fused_op.base_rate * fused_op.uncertainty)
    ecs = max(0.0, min(1.0, round(raw_ecs, 4)))

    # 7. Compute Audit Review Priority Index (ARPI)
    if hard_gate_violation:
        # Tier 1 Hard Gate Override
        arpi = 100.0
        ecs = min(0.05, ecs)  # Hard bound ECS on metrological violation
        priority_tier = PriorityTier.CRITICAL
    else:
        # Tier 2 Soft Discrepancy Scoring
        # Base inconsistency: (1 - ECS) * 100
        inconsistency_factor = (1.0 - ecs) * 100.0

        # Financial exposure scaling: log10 of claimed amount
        amount = float(dossier.claimed_amount_inr)
        if amount > 0:
            scale = 1.0 + 0.05 * math.log10(max(1.0, amount))
        else:
            scale = 1.0

        raw_arpi = inconsistency_factor * scale
        arpi = max(0.0, min(100.0, round(raw_arpi, 2)))
        priority_tier = determine_priority_tier(arpi, hard_gate=False)

    # 8. Epistemic Confidence Tier
    confidence_tier = determine_confidence_tier(fused_op.uncertainty)

    # 9. Modality Attributions
    attributions = compute_leave_one_out_attributions(modality_opinions, fused_op)

    # 10. Summary Justification Narrative
    if hard_gate_violation:
        justification = (
            f"TIER 1 HARD GATE ACTIVATED: Incontrovertible metrological violation detected by rule "
            f"'{hard_gate_rule_id}'. Review priority set to CRITICAL (ARPI: 100.0). "
            f"Details: {'; '.join(violation_justifications)}"
        )
    elif confidence_tier == ConfidenceTier.INSUFFICIENT_DATA:
        justification = (
            f"TIER 2 SOFT FUSION: Substantial data missingness detected across modalities: "
            f"{', '.join(missing_modalities)}. Fused uncertainty is high (u={fused_op.uncertainty:.2f}). "
            f"Dossier evaluated non-punitively with ECS {ecs:.2f} and triage priority {priority_tier.value}."
        )
    else:
        justification = (
            f"TIER 2 SOFT FUSION: Evidence reconciliation completed with ECS {ecs:.2f} "
            f"(Confidence: {confidence_tier.value}, Uncertainty: {fused_op.uncertainty:.2f}). "
            f"Assigned triage review priority {priority_tier.value} (ARPI: {arpi:.2f})."
        )

    return FusionResult(
        dossier_id=dossier.dossier_id,
        epistemic_category=EpistemicCategory.INFERENCE,
        evidence_consistency_score=ecs,
        audit_review_priority_index=arpi,
        priority_tier=priority_tier,
        confidence_tier=confidence_tier,
        fused_opinion=fused_op,
        modality_attributions=attributions,
        missing_modalities=missing_modalities,
        hard_gate_violation=hard_gate_violation,
        hard_gate_rule_id=hard_gate_rule_id,
        rule_results=rule_results,
        summary_justification=justification,
    )
