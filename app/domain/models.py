"""Canonical Domain Schemas & Invariant Contracts for MuniAudit-AI."""

from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator

from app.domain.epistemic import (
    AdministrativeState,
    DossierStatus,
    EpistemicCategory,
    EvidenceSourceType,
    FindingSeverity,
    ProvenanceTag,
)


def utc_now() -> datetime:
    """Returns a timezone-aware current UTC datetime."""
    return datetime.now(UTC)


class EvidenceItem(BaseModel):
    """An immutable, tamper-evident piece of submitted public-works evidence."""

    evidence_id: UUID = Field(default_factory=uuid4)
    dossier_id: UUID
    sha256_digest: str = Field(
        ..., description="Hex-encoded SHA-256 cryptographic digest of the raw artifact bytes"
    )
    storage_uri: str = Field(..., description="S3 or local filesystem storage path")
    source_type: EvidenceSourceType
    byte_size: int = Field(..., ge=0)
    content_type: str = Field(default="application/octet-stream")
    provenance_tag: ProvenanceTag = Field(default=ProvenanceTag.SYNTHETIC_DATA)
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=utc_now)

    @field_validator("sha256_digest")
    @classmethod
    def validate_sha256(cls, v: str) -> str:
        if len(v) != 64 or not all(c in "0123456789abcdefABCDEF" for c in v):
            raise ValueError("sha256_digest must be a 64-character hexadecimal string")
        return v.lower()


class Finding(BaseModel):
    """An explainable anomaly finding linking observed vs expected evidence."""

    finding_id: UUID = Field(default_factory=uuid4)
    dossier_id: UUID
    category: str = Field(
        ..., description="Subsystem category (e.g. VISUAL, WEIGHBRIDGE, GEOSPATIAL)"
    )
    epistemic_category: EpistemicCategory
    severity: FindingSeverity
    title: str
    description: str
    evidence_refs: list[str] = Field(
        default_factory=list, description="List of evidence SHA-256 digests supporting this finding"
    )
    observed_value: str | None = None
    expected_value: str | None = None
    rule_reference: str | None = None
    recommendation: str | None = None
    created_at: datetime = Field(default_factory=utc_now)


class AuditReview(BaseModel):
    """Human auditor review decision, ensuring the human remains in the loop."""

    review_id: UUID = Field(default_factory=uuid4)
    finding_id: UUID
    reviewer_id: str
    auditor_determination: AdministrativeState
    comments: str
    reviewed_at: datetime = Field(default_factory=utc_now)


class ProcessingJob(BaseModel):
    """Asynchronous reconciliation job tracking execution progress."""

    job_id: UUID = Field(default_factory=uuid4)
    dossier_id: UUID
    status: DossierStatus = Field(default=DossierStatus.QUEUED)
    progress_percent: int = Field(default=0, ge=0, le=100)
    error_details: str | None = None
    created_at: datetime = Field(default_factory=utc_now)
    completed_at: datetime | None = None


class Dossier(BaseModel):
    """Municipal contractor public-works billing dossier."""

    dossier_id: UUID = Field(default_factory=uuid4)
    tenant_id: str = Field(default="WARD-09-CENTRAL")
    work_order_id: str
    contractor_id: str
    drain_reach_id: str | None = None
    claimed_amount_inr: float = Field(default=0.0, ge=0.0)
    status: DossierStatus = Field(default=DossierStatus.CREATED)
    created_at: datetime = Field(default_factory=utc_now)
    finalized_at: datetime | None = None
    evidence_items: list[EvidenceItem] = Field(default_factory=list)
    findings: list[Finding] = Field(default_factory=list)
