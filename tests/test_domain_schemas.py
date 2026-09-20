"""Tests for canonical domain models and epistemic category validation."""

from uuid import uuid4

import pytest
from pydantic import ValidationError

from app.domain.epistemic import (
    AdministrativeState,
    EpistemicCategory,
    EvidenceSourceType,
    FindingSeverity,
    ProvenanceTag,
)
from app.domain.models import AuditReview, EvidenceItem, Finding


def test_evidence_item_valid():
    dossier_id = uuid4()
    item = EvidenceItem(
        dossier_id=dossier_id,
        sha256_digest="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        storage_uri="/data/test.jpg",
        source_type=EvidenceSourceType.SITE_PHOTO,
        byte_size=1024,
        provenance_tag=ProvenanceTag.REAL_MUNICIPAL_DATA,
    )
    assert item.dossier_id == dossier_id
    assert len(item.sha256_digest) == 64
    assert item.byte_size == 1024
    assert item.source_type == EvidenceSourceType.SITE_PHOTO


def test_evidence_item_invalid_sha256():
    dossier_id = uuid4()
    with pytest.raises(ValidationError):
        EvidenceItem(
            dossier_id=dossier_id,
            sha256_digest="not_a_valid_sha256",
            storage_uri="/data/test.jpg",
            source_type=EvidenceSourceType.SITE_PHOTO,
            byte_size=1024,
        )


def test_finding_epistemic_invariants():
    dossier_id = uuid4()
    finding = Finding(
        dossier_id=dossier_id,
        category="WEIGHBRIDGE",
        epistemic_category=EpistemicCategory.RULE_RESULT,
        severity=FindingSeverity.HIGH,
        title="Vehicle Net Mass Exceeds Bed Volume Limit",
        description="Claimed net weight of 18.5 tonnes exceeds maximum physical bulk volume.",
        observed_value="18.5 tonnes",
        expected_value="<= 15.2 tonnes",
        rule_reference="REQ-PHYS-002",
        recommendation="Conduct manual weighbridge audit with transport receipt cross-verification.",
    )
    assert finding.epistemic_category == EpistemicCategory.RULE_RESULT
    assert finding.severity == FindingSeverity.HIGH


def test_audit_review_human_determination():
    finding_id = uuid4()
    review = AuditReview(
        finding_id=finding_id,
        reviewer_id="AUDITOR_OFFICER_42",
        auditor_determination=AdministrativeState.SUBSTANTIVE_INCONSISTENCY,
        comments="Confirmed that the weighbridge slip net weight violates the vehicle specification.",
    )
    assert review.auditor_determination == AdministrativeState.SUBSTANTIVE_INCONSISTENCY
    assert review.reviewer_id == "AUDITOR_OFFICER_42"
