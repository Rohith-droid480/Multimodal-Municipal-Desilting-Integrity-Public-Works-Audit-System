"""Tests for MuniAudit-AI Explainability and Reporting Subsystem.

Validates GAGAS finding memoranda, deterministic lexical filter, epistemic segregation,
executive triage causal attributions, visual inspection canvas overlays, and
deterministic JSON/Markdown dossier exporters.
"""

from __future__ import annotations

import json
from uuid import uuid4

import pytest

from app.domain.epistemic import AdministrativeState, FindingSeverity
from app.domain.models import Dossier
from app.explainability.exporter import export_dossier_json, export_dossier_markdown
from app.explainability.memo import (
    GAGASElements,
    build_finding_memorandum,
    sanitize_lexical_tokens,
)
from app.explainability.triage import format_executive_triage
from app.explainability.visual_inspection import (
    OCROverlayToken,
    build_visual_inspection_package,
)
from app.fusion.engine import fuse_dossier_evidence
from app.ingestion.benchmark_loader import BenchmarkDossierLoader, BenchmarkDossierType
from app.rules.base import RuleEvaluationResult
from app.storage.interface import LocalStorageAdapter

# ---------------------------------------------------------------------------
# 1. Deterministic Lexical Filter Tests
# ---------------------------------------------------------------------------


def test_lexical_filter_sanitizes_prohibited_terms() -> None:
    """Validate that legal conclusion terms are replaced with objective GAGAS variance phrasing."""
    dirty_text = "This is a fraudulent claim showing clear fraud and criminal intent by contractor."
    clean_text, passed = sanitize_lexical_tokens(dirty_text)

    assert passed is False
    assert "fraudulent" not in clean_text.lower()
    assert "fraud" not in clean_text.lower()
    assert "criminal intent" not in clean_text.lower()
    assert "unsubstantiated" in clean_text
    assert "material discrepancy" in clean_text
    assert "operational noncompliance" in clean_text


def test_lexical_filter_passes_compliant_text() -> None:
    """Validate that objective technical text passes through unchanged."""
    clean_input = "Mass balance variance of 240.0 kg exceeds scale calibration tolerance (20.0 kg)."
    output, passed = sanitize_lexical_tokens(clean_input)

    assert passed is True
    assert output == clean_input


# ---------------------------------------------------------------------------
# 2. Audit Finding Memorandum Tests
# ---------------------------------------------------------------------------


def test_build_finding_memorandum_epistemic_segregation() -> None:
    """Validate that finding memorandum strictly segregates the 5 epistemic tiers."""
    dossier_id = uuid4()
    sha256 = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"

    rule_res = RuleEvaluationResult(
        rule_id="R-001-MASS-BALANCE",
        rule_name="Weighbridge Mass Balance Verification",
        status=AdministrativeState.SUBSTANTIVE_INCONSISTENCY,
        observed_value="Gross=15000 kg, Tare=5000 kg, Net=12000 kg",
        expected_value="Net=10000 kg",
        discrepancy_delta=2000.0,
        tolerance=20.0,
        evidence_refs=[sha256],
        justification="Mass balance mismatch exceeds tolerance",
    )

    memo = build_finding_memorandum(
        dossier_id=dossier_id,
        title="Weighbridge Mass Balance Discrepancy",
        severity=FindingSeverity.HIGH,
        evidence_hashes=[sha256],
        rule_result=rule_res,
    )

    # Check GAGAS elements
    assert "Standard Specifications" in memo.gagas_elements.criteria
    assert "2000.0 kg" in memo.gagas_elements.effect
    assert "docket book" in memo.gagas_elements.recommendation

    # Check Epistemic tiers
    assert "FACT" in memo.epistemic_breakdown
    assert "MODEL_OUTPUT" in memo.epistemic_breakdown
    assert "RULE_RESULT" in memo.epistemic_breakdown
    assert "INFERENCE" in memo.epistemic_breakdown
    assert "RECOMMENDATION" in memo.epistemic_breakdown

    # Facts must contain the SHA-256 hash
    facts = memo.epistemic_breakdown["FACT"]
    assert any(sha256 in f for f in facts)

    # Rule result must contain delta
    rules = memo.epistemic_breakdown["RULE_RESULT"]
    assert any("2000.0" in r for r in rules)


def test_finding_memorandum_invalid_hash_validation() -> None:
    """Validate that invalid evidence SHA-256 hash raises ValueError."""
    with pytest.raises(ValueError, match="Invalid evidence SHA-256 digest"):
        build_finding_memorandum(
            dossier_id=uuid4(),
            title="Valid Title",
            severity=FindingSeverity.LOW,
            evidence_hashes=["not-a-valid-64-char-hex-hash"],
        )


def test_finding_memorandum_sanitizes_prohibited_title() -> None:
    """Validate that memorandum title with prohibited word is sanitized and flags guardrail."""
    memo = build_finding_memorandum(
        dossier_id=uuid4(),
        title="Detected contractor fraud in weighbridge slip",
        severity=FindingSeverity.CRITICAL,
        evidence_hashes=["e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"],
    )

    assert "fraud" not in memo.title.lower()
    assert "material discrepancy" in memo.title.lower()
    assert memo.lexical_guard_passed is False


# ---------------------------------------------------------------------------
# 3. Executive Triage & Attribution Formatter Tests
# ---------------------------------------------------------------------------


def test_format_executive_triage_clean_dossier(tmp_path: pytest.TempPathFactory) -> None:
    """Validate executive triage narrative on clean compliant benchmark dossier."""
    storage = LocalStorageAdapter(str(tmp_path))
    loader = BenchmarkDossierLoader(storage_adapter=storage)
    dossier = loader.build_benchmark_dossier(BenchmarkDossierType.CLEAN_COMPLIANT)

    fusion_res = fuse_dossier_evidence(dossier, visual_similarity=0.40, ocr_confidence=0.95)
    triage = format_executive_triage(dossier, fusion_res)

    assert triage.dossier_id == dossier.dossier_id
    assert triage.evidence_consistency_score >= 0.70
    assert triage.audit_review_priority_index < 50.0
    assert "Running Account Bill" in triage.operational_summary
    assert triage.hard_gate_notice is None
    assert len(triage.causal_attributions) > 0


def test_format_executive_triage_hard_gate_violation(tmp_path: pytest.TempPathFactory) -> None:
    """Validate executive triage hard gate warning on inconsistent benchmark dossier."""
    storage = LocalStorageAdapter(str(tmp_path))
    loader = BenchmarkDossierLoader(storage_adapter=storage)
    dossier = loader.build_benchmark_dossier(BenchmarkDossierType.SUBSTANTIVE_INCONSISTENCY)

    fusion_res = fuse_dossier_evidence(dossier)
    triage = format_executive_triage(dossier, fusion_res)

    assert triage.hard_gate_notice is not None
    assert "STATUTORY METROLOGICAL HALT" in triage.hard_gate_notice
    assert triage.audit_review_priority_index == 100.0


def test_format_executive_triage_non_punitive_gaps(tmp_path: pytest.TempPathFactory) -> None:
    """Validate that unobserved channels produce technical data gap explanations."""
    storage = LocalStorageAdapter(str(tmp_path))
    loader = BenchmarkDossierLoader(storage_adapter=storage)
    dossier = loader.build_benchmark_dossier(BenchmarkDossierType.INCONCLUSIVE_DATA)

    fusion_res = fuse_dossier_evidence(dossier)
    triage = format_executive_triage(dossier, fusion_res)

    assert len(triage.technical_data_gaps) > 0
    # Must emphasize technical gaps without claiming non-performance
    gap_texts = " ".join(triage.technical_data_gaps)
    assert "without implying" in gap_texts or "evaluated as INCONCLUSIVE_DATA" in gap_texts


# ---------------------------------------------------------------------------
# 4. Visual Inspection Package Tests
# ---------------------------------------------------------------------------


def test_visual_inspection_package_bounding_boxes(tmp_path: pytest.TempPathFactory) -> None:
    """Validate that visual inspection overlays contain normalized [0, 1] bounding boxes."""
    storage = LocalStorageAdapter(str(tmp_path))
    loader = BenchmarkDossierLoader(storage_adapter=storage)
    dossier = loader.build_benchmark_dossier(BenchmarkDossierType.CLEAN_COMPLIANT)

    pkg = build_visual_inspection_package(dossier)

    assert pkg.dossier_id == dossier.dossier_id
    assert len(pkg.ocr_overlays) > 0

    for overlay in pkg.ocr_overlays:
        for token in overlay.tokens:
            assert len(token.bounding_box) == 4
            ymin, xmin, ymax, xmax = token.bounding_box
            assert 0.0 <= ymin <= 1.0
            assert 0.0 <= xmin <= 1.0
            assert 0.0 <= ymax <= 1.0
            assert 0.0 <= xmax <= 1.0


def test_ocr_overlay_invalid_bounding_box_rejected() -> None:
    """Validate that non-normalized bounding box raises ValueError."""
    with pytest.raises(ValueError, match="Bounding box coordinates must be normalized"):
        OCROverlayToken(
            field_name="gross_weight",
            extracted_text="15000 kg",
            bounding_box=[0.1, 0.2, 1.5, 0.6],  # 1.5 > 1.0
            confidence=0.9,
        )


def test_visual_duplicate_comparison_pairing() -> None:
    """Validate candidate duplicate pairing structure."""
    dossier = Dossier(
        dossier_id=uuid4(),
        tenant_id="BBMP-SWD",
        work_order_id="WO-PAIR-01",
        contractor_id="CONT-PAIR-01",
        claimed_amount_inr=100000.0,
        evidence_items=[],
    )

    pair = {
        "claimed_evidence_id": uuid4(),
        "claimed_sha256": "a" * 64,
        "matched_evidence_id": uuid4(),
        "matched_sha256": "b" * 64,
        "similarity": 0.94,
        "chainage_station": "CH-1+200",
    }

    pkg = build_visual_inspection_package(dossier, duplicate_pairs=[pair])

    assert len(pkg.duplicate_comparisons) == 1
    comp = pkg.duplicate_comparisons[0]
    assert comp.similarity_score == 0.94
    assert comp.chainage_station == "CH-1+200"
    assert "Sc=0.940 >= 0.85" in comp.audit_note


# ---------------------------------------------------------------------------
# 5. Deterministic Dossier Exporter Tests
# ---------------------------------------------------------------------------


def test_export_dossier_json_and_markdown(tmp_path: pytest.TempPathFactory) -> None:
    """Validate JSON and Markdown export structures across clean benchmark dossier."""
    storage = LocalStorageAdapter(str(tmp_path))
    loader = BenchmarkDossierLoader(storage_adapter=storage)
    dossier = loader.build_benchmark_dossier(BenchmarkDossierType.CLEAN_COMPLIANT)

    fusion_res = fuse_dossier_evidence(dossier, visual_similarity=0.42, ocr_confidence=0.94)

    # Compile a memorandum
    memo = build_finding_memorandum(
        dossier_id=dossier.dossier_id,
        title="Weighbridge Scale Verification",
        severity=FindingSeverity.LOW,
        evidence_hashes=[dossier.evidence_items[0].sha256_digest],
        gagas_elements=GAGASElements(
            criteria="CPWD Weighbridge Calibration Standards.",
            condition="Gross and Tare arithmetically reconciled.",
            cause_hypothesis="Routine execution.",
            effect="Zero material delta.",
            recommendation="Retain in audit workpaper.",
        ),
    )

    # 1. Test JSON Export
    json_export = export_dossier_json(dossier, fusion_res, memoranda=[memo])
    assert json_export["schema_version"] == "1.0.0"
    assert json_export["dossier_id"] == str(dossier.dossier_id)
    assert "executive_triage" in json_export
    assert "evidence_fusion" in json_export
    assert "finding_memoranda" in json_export
    assert "evidence_chain_of_custody" in json_export

    # Validate JSON serializability
    serialized = json.dumps(json_export)
    assert len(serialized) > 100

    # 2. Test Markdown Export
    md_export = export_dossier_markdown(dossier, fusion_res, memoranda=[memo])
    assert "# MUNICIPAL PUBLIC WORKS AUDIT FINDING WORKPAPER" in md_export
    assert "## 1. Executive Triage Summary" in md_export
    assert "## 2. Forensic Finding Memoranda (GAGAS Yellow Book Format)" in md_export
    assert "## 3. Cryptographic Chain of Custody (Source Artifacts)" in md_export
    assert "## 4. Human Auditor Adjudication & Sign-Off" in md_export
    assert "Officer Signature:" in md_export
