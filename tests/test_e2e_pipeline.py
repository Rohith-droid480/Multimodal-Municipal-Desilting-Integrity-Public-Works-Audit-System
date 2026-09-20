"""End-to-End Integration and Multimodal Pipeline Orchestration Tests.

Validates full system integration for MuniAudit-AI Milestone 10:
- Full lifecycle compliant dossier verification and GAGAS workpaper export
- Hard-gate isolation of adversarial weighbridge arithmetic contradictions
- Pairwise visual duplicate detection and bounding box overlays
- Non-punitive safe failure on unobserved / degraded telemetry channels
- Idempotent execution and endpoint error handling
"""

import io
from uuid import uuid4

from fastapi.testclient import TestClient
from PIL import Image

from app.api.main import app
from app.domain.epistemic import (
    AdministrativeState,
    DossierStatus,
    EpistemicCategory,
    EvidenceSourceType,
    ProvenanceTag,
)
from app.fusion.engine import ConfidenceTier, PriorityTier
from app.ingestion.synthetic_generator import (
    WeighbridgeAnomalyType,
    generate_synthetic_receipt_data,
    render_thermal_receipt_image,
)

client = TestClient(app)


def _create_synthetic_image_bytes(color: tuple[int, int, int] = (100, 150, 200)) -> bytes:
    """Helper to generate valid PNG bytes for a synthetic site photograph."""
    img = Image.new("RGB", (256, 256), color=color)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def test_e2e_compliant_dossier_lifecycle():
    """Validates complete audit reconciliation lifecycle for a fully compliant contractor dossier."""
    # 1. Create Dossier
    create_resp = client.post(
        "/dossiers",
        json={
            "tenant_id": "MUNI-BLR-EAST",
            "work_order_id": "WO-2026-DESILT-088",
            "contractor_id": "CONTR-APEX-INFRA",
            "drain_reach_id": "REACH-KORAMANGALA-VALLEY-04",
            "claimed_amount_inr": 450000.0,
        },
    )
    assert create_resp.status_code == 201
    dossier_data = create_resp.json()
    dossier_id = dossier_data["dossier_id"]

    # 2. Upload Clean Synthetic Weighbridge Receipt
    receipt_data = generate_synthetic_receipt_data(
        anomaly_type=WeighbridgeAnomalyType.NONE,
        ticket_seed=5001,
    )
    receipt_png = render_thermal_receipt_image(receipt_data)
    upload_wb = client.post(
        f"/dossiers/{dossier_id}/files",
        files={"file": ("weighbridge_slip_5001.png", receipt_png, "image/png")},
        data={
            "source_type": EvidenceSourceType.WEIGHBRIDGE_RECEIPT.value,
            "provenance_tag": ProvenanceTag.SYNTHETIC_DATA.value,
        },
    )
    assert upload_wb.status_code == 201

    # 3. Upload Two Distinct Site Photos
    photo1_bytes = _create_synthetic_image_bytes(color=(80, 120, 160))
    photo2_bytes = _create_synthetic_image_bytes(color=(160, 90, 40))

    upload_p1 = client.post(
        f"/dossiers/{dossier_id}/files",
        files={"file": ("site_photo_chainage_010.png", photo1_bytes, "image/png")},
        data={
            "source_type": EvidenceSourceType.SITE_PHOTO.value,
            "provenance_tag": ProvenanceTag.SYNTHETIC_DATA.value,
        },
    )
    assert upload_p1.status_code == 201

    upload_p2 = client.post(
        f"/dossiers/{dossier_id}/files",
        files={"file": ("site_photo_chainage_020.png", photo2_bytes, "image/png")},
        data={
            "source_type": EvidenceSourceType.SITE_PHOTO.value,
            "provenance_tag": ProvenanceTag.SYNTHETIC_DATA.value,
        },
    )
    assert upload_p2.status_code == 201

    # 4. Upload Valid Trip Log / GPS Track
    trip_log_kml = """<?xml version="1.0" encoding="UTF-8"?>
    <kml xmlns="http://www.opengis.net/kml/2.2">
      <Document>
        <Placemark>
          <name>Koramangala Valley Drain Reach 04</name>
          <LineString>
            <coordinates>
              77.6200,12.9300,0 77.6250,12.9350,0 77.6300,12.9400,0
            </coordinates>
          </LineString>
        </Placemark>
      </Document>
    </kml>
    """.strip()
    upload_trip = client.post(
        f"/dossiers/{dossier_id}/files",
        files={"file": ("drain_reach_track.kml", trip_log_kml.encode("utf-8"), "application/vnd.google-earth.kml+xml")},
        data={
            "source_type": EvidenceSourceType.TRIP_LOG.value,
            "provenance_tag": ProvenanceTag.SYNTHETIC_DATA.value,
        },
    )
    assert upload_trip.status_code == 201

    # 5. Upload Contract Milestone Metadata (Statutory Chronology)
    import json
    from datetime import timedelta

    wb_time = receipt_data.out_timestamp
    contract_meta = {
        "contract_award_at": (wb_time - timedelta(days=60)).strftime("%Y-%m-%d %H:%M:%S"),
        "work_order_at": (wb_time - timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S"),
        "work_execution_at": (wb_time - timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S"),
        "invoice_submitted_at": (wb_time + timedelta(days=2)).strftime("%Y-%m-%d %H:%M:%S"),
    }
    upload_contract = client.post(
        f"/dossiers/{dossier_id}/files",
        files={"file": ("contract_metadata.json", json.dumps(contract_meta).encode("utf-8"), "application/json")},
        data={
            "source_type": EvidenceSourceType.CONTRACT_METADATA.value,
            "provenance_tag": ProvenanceTag.SYNTHETIC_DATA.value,
        },
    )
    assert upload_contract.status_code == 201

    # 6. Finalize Submission
    fin_resp = client.post(f"/dossiers/{dossier_id}/finalize")
    assert fin_resp.status_code == 200

    # 7. Execute End-to-End Multimodal Audit Pipeline
    audit_resp = client.post(f"/dossiers/{dossier_id}/audit")
    assert audit_resp.status_code == 200
    audit_data = audit_resp.json()

    assert audit_data["dossier_id"] == dossier_id
    assert audit_data["status"] == DossierStatus.COMPLETED.value
    assert audit_data["administrative_state"] == AdministrativeState.VERIFIED_COMPLIANT.value
    assert audit_data["hard_gate_triggered"] is False
    assert audit_data["evidence_consistency_score"] >= 0.70
    assert audit_data["audit_review_priority_index"] < 35.0
    assert audit_data["confidence_tier"] in (
        ConfidenceTier.HIGH.value,
        ConfidenceTier.VERY_HIGH.value,
        ConfidenceTier.MODERATE.value,
    )

    # 8. Verify Executive Triage Assessment Endpoint
    triage_resp = client.get(f"/dossiers/{dossier_id}/triage")
    assert triage_resp.status_code == 200
    triage_data = triage_resp.json()
    assert "reconcil" in triage_data["operational_summary"].lower() or "compliant" in triage_data["operational_summary"].lower()
    assert triage_data["hard_gate_notice"] is None

    # 9. Verify Visual Inspection Package Endpoint
    visual_resp = client.get(f"/dossiers/{dossier_id}/visual-package")
    assert visual_resp.status_code == 200
    visual_data = visual_resp.json()
    assert visual_data["dossier_id"] == dossier_id
    assert len(visual_data["ocr_overlays"]) >= 1
    # Distinct photos produce zero near-duplicate comparisons
    assert len(visual_data["duplicate_comparisons"]) == 0

    # 10. Verify Deterministic JSON Export
    json_export = client.get(f"/dossiers/{dossier_id}/export/json")
    assert json_export.status_code == 200
    export_bundle = json_export.json()
    assert export_bundle["schema_version"] == "1.0.0"
    assert export_bundle["dossier_id"] == dossier_id
    assert len(export_bundle["evidence_chain_of_custody"]) == 5
    assert export_bundle["evidence_fusion"]["evidence_consistency_score"] >= 0.70

    # 11. Verify Deterministic GAGAS Markdown Export
    md_export = client.get(f"/dossiers/{dossier_id}/export/markdown")
    assert md_export.status_code == 200
    assert "text/markdown" in md_export.headers["content-type"]
    md_text = md_export.text
    assert "MUNICIPAL PUBLIC WORKS AUDIT" in md_text
    assert "GAGAS" in md_text
    assert "Chain of Custody" in md_text
    assert "Sign-Off" in md_text


def test_e2e_adversarial_arithmetic_mismatch():
    """Validates that a weighbridge slip arithmetic mismatch immediately triggers Tier 1 Hard Gate."""
    # 1. Create Dossier
    create_resp = client.post(
        "/dossiers",
        json={
            "tenant_id": "MUNI-BLR-SOUTH",
            "work_order_id": "WO-2026-DESILT-099",
            "contractor_id": "CONTR-SUSPECT-EARTHWORKS",
            "claimed_amount_inr": 920000.0,
        },
    )
    dossier_id = create_resp.json()["dossier_id"]

    # 2. Upload Weighbridge Receipt with Gross-Tare-Net discrepancy
    inconsistent_receipt_text = (
        "MUNICIPAL CORPORATION WEIGHBRIDGE DOCKET\n"
        "TICKET NO: WB-2026-9999\n"
        "VEHICLE REG: KA-01-MJ-8822\n"
        "GROSS WEIGHT: 25,000 KG\n"
        "TARE WEIGHT:  10,000 KG\n"
        "NET WEIGHT:   22,000 KG\n"  # 25000 - 10000 = 15000 != 22000 (delta = 7000 kg)
        "IN TIME:  2026-09-20 10:00:00\n"
        "OUT TIME: 2026-09-20 10:25:00\n"
    )
    client.post(
        f"/dossiers/{dossier_id}/files",
        files={"file": ("weighbridge_corrupted.txt", inconsistent_receipt_text.encode("utf-8"), "text/plain")},
        data={
            "source_type": EvidenceSourceType.WEIGHBRIDGE_RECEIPT.value,
            "provenance_tag": ProvenanceTag.SYNTHETIC_DATA.value,
        },
    )

    # 3. Execute Audit Pipeline
    audit_resp = client.post(f"/dossiers/{dossier_id}/audit")
    assert audit_resp.status_code == 200
    data = audit_resp.json()

    assert data["administrative_state"] == AdministrativeState.SUBSTANTIVE_INCONSISTENCY.value
    assert data["hard_gate_triggered"] is True
    assert data["audit_review_priority_index"] == 100.0
    assert data["priority_tier"] == PriorityTier.CRITICAL.value
    assert data["findings_count"] >= 1

    # 4. Verify Findings Endpoint
    findings_resp = client.get(f"/dossiers/{dossier_id}/findings")
    assert findings_resp.status_code == 200
    findings = findings_resp.json()
    assert len(findings) >= 1
    mass_finding = next((f for f in findings if f["category"] == "MASS_BALANCE"), None)
    assert mass_finding is not None
    assert mass_finding["epistemic_category"] == EpistemicCategory.RULE_RESULT.value
    assert len(mass_finding["evidence_refs"][0]) == 64

    # 5. Verify Triage Notice
    triage_resp = client.get(f"/dossiers/{dossier_id}/triage")
    assert triage_resp.status_code == 200
    triage_data = triage_resp.json()
    assert triage_data["hard_gate_notice"] is not None
    assert "r-001-mass-balance" in triage_data["hard_gate_notice"].lower() or "halt" in triage_data["hard_gate_notice"].lower()

    # 6. Verify Formal Auditor Review Submission
    review_resp = client.post(
        f"/findings/{mass_finding['finding_id']}/review",
        json={
            "reviewer_id": "AUDITOR-OFFICER-77",
            "auditor_determination": AdministrativeState.SUBSTANTIVE_INCONSISTENCY.value,
            "comments": "Scale docket shows 7,000 kg arithmetic contradiction; summoning weighbridge stamped logs.",
        },
    )
    assert review_resp.status_code == 200
    assert review_resp.json()["auditor_determination"] == AdministrativeState.SUBSTANTIVE_INCONSISTENCY.value


def test_e2e_adversarial_photo_duplicate():
    """Validates that duplicate site photo submissions are detected and flagged with SSCD copy detection."""
    # 1. Create Dossier
    create_resp = client.post(
        "/dossiers",
        json={
            "tenant_id": "MUNI-BLR-NORTH",
            "work_order_id": "WO-2026-DESILT-105",
            "contractor_id": "CONTR-REUSED-PICTURES",
            "claimed_amount_inr": 280000.0,
        },
    )
    dossier_id = create_resp.json()["dossier_id"]

    # 2. Upload Two Identical Photographs
    identical_photo = _create_synthetic_image_bytes(color=(120, 200, 140))
    client.post(
        f"/dossiers/{dossier_id}/files",
        files={"file": ("photo_chainage_000.png", identical_photo, "image/png")},
        data={
            "source_type": EvidenceSourceType.SITE_PHOTO.value,
            "provenance_tag": ProvenanceTag.SYNTHETIC_DATA.value,
        },
    )
    client.post(
        f"/dossiers/{dossier_id}/files",
        files={"file": ("photo_chainage_050_duplicate.png", identical_photo, "image/png")},
        data={
            "source_type": EvidenceSourceType.SITE_PHOTO.value,
            "provenance_tag": ProvenanceTag.SYNTHETIC_DATA.value,
        },
    )

    # 3. Execute Audit Pipeline
    audit_resp = client.post(f"/dossiers/{dossier_id}/audit")
    assert audit_resp.status_code == 200
    data = audit_resp.json()

    # Visual duplicates are flagged as findings and surfaced in visual inspection package
    assert data["findings_count"] >= 1

    visual_resp = client.get(f"/dossiers/{dossier_id}/visual-package")
    assert visual_resp.status_code == 200
    visual_data = visual_resp.json()
    assert len(visual_data["duplicate_comparisons"]) == 1
    dup = visual_data["duplicate_comparisons"][0]
    assert dup["similarity_score"] >= 0.85
    assert len(dup["claimed_sha256"]) == 64
    assert len(dup["matched_sha256"]) == 64


def test_e2e_missing_data_safe_failure():
    """Validates non-punitive safe failure when telemetry channels are missing."""
    # 1. Create Dossier with only 1 unverified photo and no weighbridge/GPS records
    create_resp = client.post(
        "/dossiers",
        json={
            "tenant_id": "MUNI-BLR-WEST",
            "work_order_id": "WO-2026-DESILT-112",
            "contractor_id": "CONTR-INCOMPLETE-SUBMISSION",
            "claimed_amount_inr": 120000.0,
        },
    )
    dossier_id = create_resp.json()["dossier_id"]

    sample_photo = _create_synthetic_image_bytes(color=(150, 150, 150))
    client.post(
        f"/dossiers/{dossier_id}/files",
        files={"file": ("single_photo.png", sample_photo, "image/png")},
        data={
            "source_type": EvidenceSourceType.SITE_PHOTO.value,
            "provenance_tag": ProvenanceTag.SYNTHETIC_DATA.value,
        },
    )

    # 2. Execute Audit Pipeline
    audit_resp = client.post(f"/dossiers/{dossier_id}/audit")
    assert audit_resp.status_code == 200
    data = audit_resp.json()

    # Safe failure: missing channels lead to INCONCLUSIVE_DATA, NOT false accusation of fraud
    assert data["administrative_state"] == AdministrativeState.INCONCLUSIVE_DATA.value
    assert data["confidence_tier"] in (
        ConfidenceTier.LOW.value,
        ConfidenceTier.INSUFFICIENT_DATA.value,
    )
    assert data["hard_gate_triggered"] is False

    # 3. Verify Triage Explains Technical Data Gaps Non-Punitively
    triage_resp = client.get(f"/dossiers/{dossier_id}/triage")
    assert triage_resp.status_code == 200
    triage_data = triage_resp.json()
    assert len(triage_data["technical_data_gaps"]) >= 1
    assert any("gap" in gap.lower() or "missing" in gap.lower() or "unobserved" in gap.lower() for gap in triage_data["technical_data_gaps"])


def test_e2e_audit_idempotency():
    """Validates that re-auditing a dossier produces identical deterministic scores and results."""
    # 1. Create Dossier
    create_resp = client.post(
        "/dossiers",
        json={
            "tenant_id": "MUNI-BLR-CENTRAL",
            "work_order_id": "WO-2026-DESILT-IDEM",
            "contractor_id": "CONTR-IDEMPOTENT",
            "claimed_amount_inr": 100000.0,
        },
    )
    dossier_id = create_resp.json()["dossier_id"]

    # 2. Audit 1
    audit1 = client.post(f"/dossiers/{dossier_id}/audit").json()
    # 3. Audit 2
    audit2 = client.post(f"/dossiers/{dossier_id}/audit").json()

    assert audit1["evidence_consistency_score"] == audit2["evidence_consistency_score"]
    assert audit1["audit_review_priority_index"] == audit2["audit_review_priority_index"]
    assert audit1["administrative_state"] == audit2["administrative_state"]
    assert audit1["hard_gate_triggered"] == audit2["hard_gate_triggered"]


def test_e2e_error_handling_unregistered_dossier():
    """Validates 404/400 HTTP error guards for nonexistent or unaudited dossiers."""
    random_id = str(uuid4())

    # Nonexistent dossier
    resp = client.post(f"/dossiers/{random_id}/audit")
    assert resp.status_code == 404

    resp_triage = client.get(f"/dossiers/{random_id}/triage")
    assert resp_triage.status_code == 404

    # Unaudited dossier
    create_resp = client.post(
        "/dossiers",
        json={
            "tenant_id": "MUNI-TEST",
            "work_order_id": "WO-UNAUDITED",
            "contractor_id": "CONTR-TEST",
            "claimed_amount_inr": 50000.0,
        },
    )
    unaudited_id = create_resp.json()["dossier_id"]

    unaudited_triage = client.get(f"/dossiers/{unaudited_id}/triage")
    assert unaudited_triage.status_code == 400
    assert "not been audited yet" in unaudited_triage.json()["detail"].lower()

    unaudited_export = client.get(f"/dossiers/{unaudited_id}/export/json")
    assert unaudited_export.status_code == 400
