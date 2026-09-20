"""Initial canonical schema for MuniAudit-AI

Revision ID: 001_initial_schema
Revises:
Create Date: 2026-09-20 13:25:00.000000

"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "001_initial_schema"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # 1. municipal_tenants
    op.create_table(
        "municipal_tenants",
        sa.Column("tenant_id", sa.String(length=64), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("state", sa.String(length=100), server_default="Karnataka", nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
    )

    # 2. contractors
    op.create_table(
        "contractors",
        sa.Column("contractor_id", sa.String(length=64), primary_key=True),
        sa.Column("company_name", sa.String(length=255), nullable=False),
        sa.Column("pan_number", sa.String(length=20), nullable=True),
        sa.Column("gstin", sa.String(length=20), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
    )

    # 3. contracts
    op.create_table(
        "contracts",
        sa.Column("contract_id", sa.String(length=64), primary_key=True),
        sa.Column("tenant_id", sa.String(length=64), sa.ForeignKey("municipal_tenants.tenant_id"), nullable=False),
        sa.Column("contractor_id", sa.String(length=64), sa.ForeignKey("contractors.contractor_id"), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("total_value_inr", sa.Float(), server_default="0.0", nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
    )

    # 4. work_orders
    op.create_table(
        "work_orders",
        sa.Column("work_order_id", sa.String(length=64), primary_key=True),
        sa.Column("contract_id", sa.String(length=64), sa.ForeignKey("contracts.contract_id"), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("sanctioned_amount_inr", sa.Float(), server_default="0.0", nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
    )

    # 5. drain_reaches
    op.create_table(
        "drain_reaches",
        sa.Column("drain_reach_id", sa.String(length=64), primary_key=True),
        sa.Column("tenant_id", sa.String(length=64), sa.ForeignKey("municipal_tenants.tenant_id"), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("start_point_lat", sa.Float(), nullable=False),
        sa.Column("start_point_lng", sa.Float(), nullable=False),
        sa.Column("end_point_lat", sa.Float(), nullable=False),
        sa.Column("end_point_lng", sa.Float(), nullable=False),
        sa.Column("length_meters", sa.Float(), server_default="0.0", nullable=False),
    )

    # 6. audit_dossiers
    op.create_table(
        "audit_dossiers",
        sa.Column("dossier_id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=64), sa.ForeignKey("municipal_tenants.tenant_id"), nullable=False),
        sa.Column("work_order_id", sa.String(length=64), sa.ForeignKey("work_orders.work_order_id"), nullable=False),
        sa.Column("contractor_id", sa.String(length=64), sa.ForeignKey("contractors.contractor_id"), nullable=False),
        sa.Column("drain_reach_id", sa.String(length=64), sa.ForeignKey("drain_reaches.drain_reach_id"), nullable=True),
        sa.Column("claimed_amount_inr", sa.Float(), server_default="0.0", nullable=False),
        sa.Column("status", sa.String(length=32), server_default="CREATED", nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("finalized_at", sa.DateTime(), nullable=True),
    )

    # 7. evidence_items
    op.create_table(
        "evidence_items",
        sa.Column("evidence_id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("dossier_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("audit_dossiers.dossier_id"), nullable=False),
        sa.Column("sha256_digest", sa.String(length=64), nullable=False, index=True),
        sa.Column("storage_uri", sa.String(length=512), nullable=False),
        sa.Column("source_type", sa.String(length=32), nullable=False),
        sa.Column("byte_size", sa.Integer(), nullable=False),
        sa.Column("content_type", sa.String(length=128), server_default="application/octet-stream", nullable=False),
        sa.Column("provenance_tag", sa.String(length=32), server_default="SYNTHETIC_DATA", nullable=False),
        sa.Column("metadata_json", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
    )

    # 8. audit_findings
    op.create_table(
        "audit_findings",
        sa.Column("finding_id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("dossier_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("audit_dossiers.dossier_id"), nullable=False),
        sa.Column("category", sa.String(length=64), nullable=False),
        sa.Column("epistemic_category", sa.String(length=32), nullable=False),
        sa.Column("severity", sa.String(length=32), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("evidence_refs", sa.JSON(), nullable=True),
        sa.Column("observed_value", sa.Text(), nullable=True),
        sa.Column("expected_value", sa.Text(), nullable=True),
        sa.Column("rule_reference", sa.String(length=128), nullable=True),
        sa.Column("recommendation", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
    )

    # 9. audit_reviews
    op.create_table(
        "audit_reviews",
        sa.Column("review_id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("finding_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("audit_findings.finding_id"), nullable=False),
        sa.Column("reviewer_id", sa.String(length=128), nullable=False),
        sa.Column("auditor_determination", sa.String(length=32), nullable=False),
        sa.Column("comments", sa.Text(), nullable=False),
        sa.Column("reviewed_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
    )

    # 10. audit_ledger
    op.create_table(
        "audit_ledger",
        sa.Column("entry_id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("dossier_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("audit_dossiers.dossier_id"), nullable=False),
        sa.Column("event_type", sa.String(length=64), nullable=False),
        sa.Column("actor_id", sa.String(length=128), nullable=False),
        sa.Column("payload_hash", sa.String(length=64), nullable=False),
        sa.Column("timestamp", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("audit_ledger")
    op.drop_table("audit_reviews")
    op.drop_table("audit_findings")
    op.drop_table("evidence_items")
    op.drop_table("audit_dossiers")
    op.drop_table("drain_reaches")
    op.drop_table("work_orders")
    op.drop_table("contracts")
    op.drop_table("contractors")
    op.drop_table("municipal_tenants")
