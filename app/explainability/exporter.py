"""MuniAudit-AI — Deterministic Audit Dossier Exporter.

Serializes audit dossiers into standardized JSON and GAGAS Yellow Book compliant
Markdown workpapers suitable for offline regulatory filing and legal proceedings.
Adheres strictly to Locked Architecture v1.0 and Section 31-34 explainability standards.
"""

from __future__ import annotations

from typing import Any

from app.domain.models import Dossier
from app.explainability.memo import AuditFindingMemorandum
from app.explainability.triage import ExecutiveTriageDossier, format_executive_triage
from app.fusion.engine import FusionResult


def export_dossier_json(
    dossier: Dossier,
    fusion_result: FusionResult,
    memoranda: list[AuditFindingMemorandum],
    triage: ExecutiveTriageDossier | None = None,
) -> dict[str, Any]:
    """Serialize the entire audit dossier, evidential fusion result, and finding memoranda to JSON."""
    if triage is None:
        triage = format_executive_triage(dossier, fusion_result)

    evidence_items_serialized = [
        {
            "evidence_id": str(item.evidence_id),
            "sha256_digest": item.sha256_digest,
            "source_type": item.source_type.value,
            "byte_size": item.byte_size,
            "content_type": item.content_type,
            "provenance_tag": item.provenance_tag.value,
            "storage_uri": item.storage_uri,
            "created_at": item.created_at.isoformat(),
        }
        for item in dossier.evidence_items
    ]

    return {
        "schema_version": "1.0.0",
        "dossier_id": str(dossier.dossier_id),
        "tenant_id": dossier.tenant_id,
        "work_order_id": dossier.work_order_id,
        "contractor_id": dossier.contractor_id,
        "drain_reach_id": dossier.drain_reach_id,
        "claimed_amount_inr": dossier.claimed_amount_inr,
        "status": dossier.status.value,
        "created_at": dossier.created_at.isoformat(),
        "finalized_at": dossier.finalized_at.isoformat() if dossier.finalized_at else None,
        "executive_triage": triage.model_dump(mode="json"),
        "evidence_fusion": fusion_result.model_dump(mode="json"),
        "finding_memoranda": [memo.model_dump(mode="json") for memo in memoranda],
        "evidence_chain_of_custody": evidence_items_serialized,
    }


def export_dossier_markdown(
    dossier: Dossier,
    fusion_result: FusionResult,
    memoranda: list[AuditFindingMemorandum],
    triage: ExecutiveTriageDossier | None = None,
) -> str:
    """Generate an offline-filing ready Markdown audit workpaper."""
    if triage is None:
        triage = format_executive_triage(dossier, fusion_result)

    claimed_str = f"INR {dossier.claimed_amount_inr:,.2f}"

    lines: list[str] = [
        "# MUNICIPAL PUBLIC WORKS AUDIT FINDING WORKPAPER",
        "**System of Record:** MuniAudit-AI — Automated Forensic Decision-Support System  ",
        "**Audit Standard:** Generally Accepted Government Auditing Standards (GAGAS / Yellow Book)  ",
        f"**Jurisdiction Tenant:** `{dossier.tenant_id}`  ",
        f"**Work Order ID:** `{dossier.work_order_id}`  ",
        f"**Contractor ID:** `{dossier.contractor_id}`  ",
        f"**Drain Reach ID:** `{dossier.drain_reach_id or 'UNSPECIFIED'}`  ",
        f"**Claimed Amount:** `{claimed_str}`  ",
        f"**Audit Dossier UUID:** `{dossier.dossier_id}`  ",
        f"**Report Generated At:** `{triage.generated_at.strftime('%Y-%m-%d %H:%M:%S UTC')}`  ",
        "",
        "---",
        "",
        "## 1. Executive Triage Summary",
        "",
        "| Metric | Value | Reference Standard / Operational Meaning |",
        "|:---|:---:|:---|",
        f"| **Evidence Consistency Score (ECS)** | `{triage.evidence_consistency_score:.2f}` / 1.00 | Aggregate cross-sensor metrological and documentary coherence |",
        f"| **Audit Review Priority Index (ARPI)** | `{triage.audit_review_priority_index:.1f}` / 100.0 | Operational review triage priority ranking |",
        f"| **Review Priority Tier** | **`{triage.priority_tier.value}`** | Triage inspection queue classification (`LOW` / `MEDIUM` / `HIGH` / `CRITICAL`) |",
        f"| **Epistemic Confidence Tier** | `{triage.confidence_tier.value}` | Uncertainty mass $u$ based on observed telemetry channels |",
        f"| **Hard Gate Violation** | `{'YES' if fusion_result.hard_gate_violation else 'NO'}` | Incontrovertible statutory or metrological invariant failure |",
        "",
        "### Operational Narrative",
        f"> {triage.operational_summary}",
        "",
    ]

    if triage.hard_gate_notice:
        lines.extend([
            "> [!WARNING]",
            f"> **{triage.hard_gate_notice}**",
            "",
        ])

    # Causal attributions
    lines.extend([
        "### Operational Causal Attributions (Leave-One-Out Decomposition)",
        "",
    ])
    for attr in triage.causal_attributions:
        lines.append(f"- {attr}")
    lines.append("")

    # Technical data gaps
    if triage.technical_data_gaps:
        lines.extend([
            "### Unobserved Telemetry & Non-Punitive Technical Data Gaps",
            "",
        ])
        for gap in triage.technical_data_gaps:
            lines.append(f"- {gap}")
        lines.append("")

    # Section 2: Detailed Finding Memoranda
    lines.extend([
        "---",
        "",
        "## 2. Forensic Finding Memoranda (GAGAS Yellow Book Format)",
        "",
    ])

    if not memoranda:
        lines.extend([
            "*No substantive exceptions or metrological variances detected. Multi-modal telemetry conforms to statutory baselines.*",
            "",
        ])
    else:
        for idx, memo in enumerate(memoranda, start=1):
            rule_str = f" ({memo.rule_id})" if memo.rule_id else ""
            lines.extend([
                f"### Finding {idx}: {memo.title}{rule_str}",
                f"- **Severity:** `{memo.severity.value}`",
                f"- **Memorandum ID:** `{memo.memorandum_id}`",
                f"- **Lexical Guardrail Passed:** `{'YES' if memo.lexical_guard_passed else 'SANITIZED (Prohibited term substituted)'}`",
                "",
                "#### GAGAS Yellow Book 5-Element Structure:",
                f"1. **Criteria:** {memo.gagas_elements.criteria}",
                f"2. **Condition:** {memo.gagas_elements.condition}",
                f"3. **Cause (Algorithmic Hypothesis):** {memo.gagas_elements.cause_hypothesis}",
                f"4. **Effect:** {memo.gagas_elements.effect}",
                f"5. **Recommendation:** {memo.gagas_elements.recommendation}",
                "",
                "#### Epistemic Hierarchy Breakdown:",
            ])
            for tier, entries in memo.epistemic_breakdown.items():
                if entries:
                    lines.append(f"- **`{tier}`:**")
                    for entry in entries:
                        lines.append(f"  - {entry}")
            lines.append("")

    # Section 3: Evidence Chain of Custody
    lines.extend([
        "---",
        "",
        "## 3. Cryptographic Chain of Custody (Source Artifacts)",
        "",
        "| Evidence ID | Modality Source | Size (Bytes) | Cryptographic Digest (SHA-256) | Provenance |",
        "|:---|:---|:---:|:---|:---:|",
    ])

    for item in dossier.evidence_items:
        lines.append(
            f"| `{str(item.evidence_id)[:8]}...` | `{item.source_type.value}` | `{item.byte_size:,}` | `{item.sha256_digest}` | `{item.provenance_tag.value}` |"
        )
    lines.extend([
        "",
        "---",
        "",
        "## 4. Human Auditor Adjudication & Sign-Off",
        "",
        (
            "Under Yellow Book and GAGAS standards, automated findings are strictly advisory decision-support instruments. "
            "Final administrative or legal determination requires human vigilance officer inquiry."
        ),
        "",
        "- **Reviewing Officer Name:** ________________________________________",
        "- **Officer Designation / ID:** ________________________________________",
        "- **Formal Determination:** [  ] VERIFIED_COMPLIANT    [  ] SUBSTANTIVE_INCONSISTENCY    [  ] INCONCLUSIVE_DATA",
        "- **Auditor Findings & Disposition Comments:**",
        "  ____________________________________________________________________________________________________",
        "  ____________________________________________________________________________________________________",
        "- **Officer Signature:** ____________________________  **Date:** ________________________",
        "",
    ])

    return "\n".join(lines)
