"""Integration tests for Dossier lifecycle API endpoints."""

import io
from uuid import uuid4

from fastapi.testclient import TestClient


def test_dossier_lifecycle(test_client: TestClient):
    # 1. Create a dossier
    create_payload = {
        "tenant_id": "WARD-09-CENTRAL",
        "work_order_id": "WO-2026-BLR-089",
        "contractor_id": "CONT-SWD-4412",
        "drain_reach_id": "REACH-KORAMANGALA-VALLEY-03",
        "claimed_amount_inr": 485000.0,
    }
    create_res = test_client.post("/dossiers", json=create_payload)
    assert create_res.status_code == 201
    dossier = create_res.json()
    dossier_id = dossier["dossier_id"]
    assert dossier["status"] == "CREATED"
    assert dossier["work_order_id"] == "WO-2026-BLR-089"

    # 2. Upload an evidence file
    file_bytes = b"Pre-monsoon desilting site photograph mock raw bytes"
    files = {"file": ("site_photo_pre.jpg", io.BytesIO(file_bytes), "image/jpeg")}
    data = {
        "source_type": "SITE_PHOTO",
        "provenance_tag": "REAL_MUNICIPAL_DATA",
    }
    upload_res = test_client.post(f"/dossiers/{dossier_id}/files", files=files, data=data)
    assert upload_res.status_code == 201
    evidence = upload_res.json()
    assert evidence["source_type"] == "SITE_PHOTO"
    assert len(evidence["sha256_digest"]) == 64

    # 3. Retrieve dossier to verify evidence attachment
    get_res = test_client.get(f"/dossiers/{dossier_id}")
    assert get_res.status_code == 200
    updated_dossier = get_res.json()
    assert updated_dossier["status"] == "UPLOADING"
    assert len(updated_dossier["evidence_items"]) == 1

    # 4. Finalize dossier
    finalize_res = test_client.post(f"/dossiers/{dossier_id}/finalize")
    assert finalize_res.status_code == 200
    job = finalize_res.json()
    assert job["status"] == "QUEUED"
    assert job["dossier_id"] == dossier_id

    # 5. Retrieve findings
    findings_res = test_client.get(f"/dossiers/{dossier_id}/findings")
    assert findings_res.status_code == 200
    findings = findings_res.json()
    assert isinstance(findings, list)


def test_dossier_not_found(test_client: TestClient):
    random_id = uuid4()
    get_res = test_client.get(f"/dossiers/{random_id}")
    assert get_res.status_code == 404

    fin_res = test_client.post(f"/dossiers/{random_id}/finalize")
    assert fin_res.status_code == 404


def test_review_finding(test_client: TestClient):
    finding_id = uuid4()
    review_payload = {
        "reviewer_id": "CHIEF_AUDITOR_01",
        "auditor_determination": "VERIFIED_COMPLIANT",
        "comments": "Reviewed historical photos; site desilting depth matches measurement book.",
    }
    res = test_client.post(f"/findings/{finding_id}/review", json=review_payload)
    assert res.status_code == 200
    review = res.json()
    assert review["reviewer_id"] == "CHIEF_AUDITOR_01"
    assert review["auditor_determination"] == "VERIFIED_COMPLIANT"
