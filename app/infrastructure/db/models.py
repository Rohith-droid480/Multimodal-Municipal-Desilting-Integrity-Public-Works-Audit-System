"""SQLAlchemy 2.0 ORM Models for MuniAudit-AI Canonical Database Tables."""

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import (
    JSON,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy import (
    Enum as SAEnum,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from app.domain.epistemic import (
    AdministrativeState,
    DossierStatus,
    EpistemicCategory,
    EvidenceSourceType,
    FindingSeverity,
    ProvenanceTag,
)


class Base(DeclarativeBase):
    """Declarative Base for SQLAlchemy Models."""


class MunicipalTenant(Base):
    __tablename__ = "municipal_tenants"

    tenant_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    state: Mapped[str] = mapped_column(String(100), default="Karnataka")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    contracts: Mapped[list["Contract"]] = relationship(back_populates="tenant")


class Contractor(Base):
    __tablename__ = "contractors"

    contractor_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    company_name: Mapped[str] = mapped_column(String(255), nullable=False)
    pan_number: Mapped[str | None] = mapped_column(String(20), nullable=True)
    gstin: Mapped[str | None] = mapped_column(String(20), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Contract(Base):
    __tablename__ = "contracts"

    contract_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(
        ForeignKey("municipal_tenants.tenant_id"), nullable=False
    )
    contractor_id: Mapped[str] = mapped_column(
        ForeignKey("contractors.contractor_id"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    total_value_inr: Mapped[float] = mapped_column(Float, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    tenant: Mapped["MunicipalTenant"] = relationship(back_populates="contracts")
    work_orders: Mapped[list["WorkOrder"]] = relationship(back_populates="contract")


class WorkOrder(Base):
    __tablename__ = "work_orders"

    work_order_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    contract_id: Mapped[str] = mapped_column(ForeignKey("contracts.contract_id"), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    sanctioned_amount_inr: Mapped[float] = mapped_column(Float, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    contract: Mapped["Contract"] = relationship(back_populates="work_orders")
    dossiers: Mapped[list["AuditDossier"]] = relationship(back_populates="work_order")


class DrainReach(Base):
    __tablename__ = "drain_reaches"

    drain_reach_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(
        ForeignKey("municipal_tenants.tenant_id"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    start_point_lat: Mapped[float] = mapped_column(Float, nullable=False)
    start_point_lng: Mapped[float] = mapped_column(Float, nullable=False)
    end_point_lat: Mapped[float] = mapped_column(Float, nullable=False)
    end_point_lng: Mapped[float] = mapped_column(Float, nullable=False)
    length_meters: Mapped[float] = mapped_column(Float, default=0.0)


class AuditDossier(Base):
    __tablename__ = "audit_dossiers"

    dossier_id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    tenant_id: Mapped[str] = mapped_column(
        ForeignKey("municipal_tenants.tenant_id"), nullable=False
    )
    work_order_id: Mapped[str] = mapped_column(
        ForeignKey("work_orders.work_order_id"), nullable=False
    )
    contractor_id: Mapped[str] = mapped_column(
        ForeignKey("contractors.contractor_id"), nullable=False
    )
    drain_reach_id: Mapped[str | None] = mapped_column(
        ForeignKey("drain_reaches.drain_reach_id"), nullable=True
    )
    claimed_amount_inr: Mapped[float] = mapped_column(Float, default=0.0)
    status: Mapped[DossierStatus] = mapped_column(
        SAEnum(DossierStatus), default=DossierStatus.CREATED, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    finalized_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    work_order: Mapped["WorkOrder"] = relationship(back_populates="dossiers")
    evidence_items: Mapped[list["EvidenceItemRecord"]] = relationship(back_populates="dossier")
    findings: Mapped[list["AuditFinding"]] = relationship(back_populates="dossier")


class EvidenceItemRecord(Base):
    __tablename__ = "evidence_items"

    evidence_id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    dossier_id: Mapped[UUID] = mapped_column(
        ForeignKey("audit_dossiers.dossier_id"), nullable=False
    )
    sha256_digest: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    storage_uri: Mapped[str] = mapped_column(String(512), nullable=False)
    source_type: Mapped[EvidenceSourceType] = mapped_column(
        SAEnum(EvidenceSourceType), nullable=False
    )
    byte_size: Mapped[int] = mapped_column(Integer, nullable=False)
    content_type: Mapped[str] = mapped_column(String(128), default="application/octet-stream")
    provenance_tag: Mapped[ProvenanceTag] = mapped_column(
        SAEnum(ProvenanceTag), default=ProvenanceTag.SYNTHETIC_DATA, nullable=False
    )
    metadata_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    dossier: Mapped["AuditDossier"] = relationship(back_populates="evidence_items")


class AuditFinding(Base):
    __tablename__ = "audit_findings"

    finding_id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    dossier_id: Mapped[UUID] = mapped_column(
        ForeignKey("audit_dossiers.dossier_id"), nullable=False
    )
    category: Mapped[str] = mapped_column(String(64), nullable=False)
    epistemic_category: Mapped[EpistemicCategory] = mapped_column(
        SAEnum(EpistemicCategory), nullable=False
    )
    severity: Mapped[FindingSeverity] = mapped_column(SAEnum(FindingSeverity), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    evidence_refs: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    observed_value: Mapped[str | None] = mapped_column(Text, nullable=True)
    expected_value: Mapped[str | None] = mapped_column(Text, nullable=True)
    rule_reference: Mapped[str | None] = mapped_column(String(128), nullable=True)
    recommendation: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    dossier: Mapped["AuditDossier"] = relationship(back_populates="findings")
    reviews: Mapped[list["AuditReviewRecord"]] = relationship(back_populates="finding")


class AuditReviewRecord(Base):
    __tablename__ = "audit_reviews"

    review_id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    finding_id: Mapped[UUID] = mapped_column(
        ForeignKey("audit_findings.finding_id"), nullable=False
    )
    reviewer_id: Mapped[str] = mapped_column(String(128), nullable=False)
    auditor_determination: Mapped[AdministrativeState] = mapped_column(
        SAEnum(AdministrativeState), nullable=False
    )
    comments: Mapped[str] = mapped_column(Text, nullable=False)
    reviewed_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    finding: Mapped["AuditFinding"] = relationship(back_populates="reviews")


class AuditLedger(Base):
    """Tamper-evident append-only ledger of audit events."""

    __tablename__ = "audit_ledger"

    entry_id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    dossier_id: Mapped[UUID] = mapped_column(
        ForeignKey("audit_dossiers.dossier_id"), nullable=False
    )
    event_type: Mapped[str] = mapped_column(String(64), nullable=False)
    actor_id: Mapped[str] = mapped_column(String(128), nullable=False)
    payload_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
