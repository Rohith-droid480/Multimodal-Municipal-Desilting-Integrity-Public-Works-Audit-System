"""MuniAudit-AI — Audit Finding Memorandum Compiler.

Constructs forensic finding memoranda adhering to GAGAS (Yellow Book) standards,
enforces the 5-tier epistemic hierarchy, pins cryptographic evidence SHA-256 digests,
and executes a deterministic lexical filter blocking legal conclusion terms.

Adheres strictly to Locked Architecture v1.0 and MuniAudit AI Explainability Architecture.
"""

from __future__ import annotations

import re
from datetime import UTC, datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator

from app.domain.epistemic import EpistemicCategory, FindingSeverity
from app.rules.base import RuleEvaluationResult

# Deterministic lexical filter mapping prohibited legal conclusion terms
# to standardized GAGAS Yellow Book objective noncompliance phrasing.
PROHIBITED_LEGAL_TERMS: dict[str, str] = {
    r"\bfraud\b": "material discrepancy",
    r"\bfraudulent\b": "unsubstantiated",
    r"\bembezzlement\b": "unauthorized disbursement variance",
    r"\blarceny\b": "unsupported asset clearance",
    r"\bcorrupt\b": "procedural exception",
    r"\bcorruption\b": "internal control failure",
    r"\bbribe\b": "irregular transaction",
    r"\bkickback\b": "unverified commission",
    r"\bcriminal intent\b": "operational noncompliance",
    r"\bguilt\b": "evidentiary inconsistency",
    r"\bguilty\b": "inconsistent",
    r"\bmens rea\b": "substantive variance",
}


def sanitize_lexical_tokens(text: str) -> tuple[str, bool]:
    """Inspect text against the deterministic lexical filter.

    Returns:
        tuple[str, bool]: (sanitized_text, lexical_guard_passed).
        If any prohibited token is found, it is replaced with objective GAGAS phrasing
        and lexical_guard_passed is marked False (indicating the filter had to intervene).
    """
    sanitized = text
    guard_passed = True

    for pattern, replacement in PROHIBITED_LEGAL_TERMS.items():
        if re.search(pattern, sanitized, flags=re.IGNORECASE):
            guard_passed = False
            sanitized = re.sub(pattern, replacement, sanitized, flags=re.IGNORECASE)

    return sanitized, guard_passed


class GAGASElements(BaseModel):
    """The five standard elements of an audit finding under Yellow Book (GAGAS) standards."""

    criteria: str = Field(..., description="The legal, engineering, or statutory benchmark")
    condition: str = Field(..., description="The empirical situation observed in submitted evidence")
    cause_hypothesis: str = Field(
        ...,
        description="Hypothesis for auditor examination (e.g. data-entry error vs equipment drift)",
    )
    effect: str = Field(..., description="Quantified physical or financial impact of the variance")
    recommendation: str = Field(..., description="Advisory action for human vigilance inquiry")


class AuditFindingMemorandum(BaseModel):
    """Forensically structured audit finding memorandum with cryptographic bindings."""

    memorandum_id: UUID = Field(default_factory=uuid4)
    dossier_id: UUID = Field(..., description="Associated dossier UUID")
    finding_id: UUID = Field(default_factory=uuid4)
    rule_id: str | None = Field(default=None, description="Triggering civil rule ID if applicable")
    title: str = Field(..., description="Standardized GAGAS variance title")
    severity: FindingSeverity = Field(..., description="Finding severity tier")
    epistemic_breakdown: dict[str, list[str]] = Field(
        ...,
        description="Strict segregation across FACT, MODEL_OUTPUT, RULE_RESULT, INFERENCE, RECOMMENDATION",
    )
    gagas_elements: GAGASElements = Field(..., description="Yellow Book finding elements")
    evidence_hashes: list[str] = Field(
        default_factory=list,
        description="Pinned 64-character SHA-256 cryptographic digests",
    )
    lexical_guard_passed: bool = Field(
        default=True,
        description="True if original narrative passed lexical filter without substitution",
    )
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    @field_validator("evidence_hashes")
    @classmethod
    def validate_hashes(cls, hashes: list[str]) -> list[str]:
        """Validate that all evidence references are 64-character hex strings."""
        for h in hashes:
            if len(h) != 64 or not all(c in "0123456789abcdefABCDEF" for c in h):
                msg = f"Invalid evidence SHA-256 digest: '{h}'"
                raise ValueError(msg)
        return [h.lower() for h in hashes]


def _build_rule_gagas_elements(rule: RuleEvaluationResult) -> GAGASElements:
    """Derive GAGAS 5-elements from a deterministic rule evaluation result."""
    rule_id = rule.rule_id
    if rule_id == "R-001-MASS-BALANCE":
        criteria = "Standard Specifications for Road & Bridge Works Section 110: Scale tolerance |Gross - Tare - Net| <= 20.0 kg."
        condition = f"Observed weighbridge payload: {rule.observed_value}."
        cause = "Algorithmic Cause Hypothesis: Calibration load-cell drift, unrecorded tipper residue, or clerical tare transcription error."
        effect = f"Mass balance variance of {rule.discrepancy_delta} kg."
        recommendation = "Inspect original physical weighbridge docket book and request load-cell annual stamping certificate."
    elif rule_id == "R-002-GEOSPATIAL-SPEED":
        criteria = "Municipal Urban Fleet Guidelines: Maximum commercial haul velocity ceiling <= 80.0 km/h (WGS-84 Geodesic)."
        condition = f"Calculated apparent transit speed: {rule.observed_value}."
        cause = "Algorithmic Cause Hypothesis: Clock unsynchronization between scale and GPS logger, or invalid station coordinate logging."
        effect = "Trip duration implies physically implausible haul velocity along municipal corridor."
        recommendation = "Reconstruct vehicle telematics timeline and cross-check driver log sheet with toll/junction CCTV timestamps."
    elif rule_id == "R-003-PHYSICAL-DENSITY":
        criteria = "Civil Engineering Bulk Material Tables: Wet saturated desilted sludge density ceiling <= 1.90 t/m³."
        condition = f"Calculated apparent material density: {rule.observed_value}."
        cause = "Algorithmic Cause Hypothesis: Over-reporting net tonnage, incorrect tipper bed volumetric dimension, or non-silt payload."
        effect = "Billed silt mass exceeds physical volumetric capacity of the transport vehicle."
        recommendation = "Conduct physical volumetric measurement of tipper truck bed and audit weighbridge scale load logs."
    elif rule_id == "R-004-TEMPORAL-SEQUENCE":
        criteria = "Municipal Public Works Accounting Manual: Monotonic project lifecycle chronology."
        condition = f"Observed project milestone sequence: {rule.observed_value}."
        cause = "Algorithmic Cause Hypothesis: Retroactive document entry, incorrect fiscal year timestamp logging, or backdated slip issuance."
        effect = "Milestone dates are chronologically inverted relative to statutory execution sequence."
        recommendation = "Audit physical dispatch register and verified municipal server issuance timestamps."
    else:
        criteria = "Municipal Public Works Execution Standards."
        condition = f"Observed condition: {rule.observed_value}."
        cause = "Algorithmic Cause Hypothesis: Data entry variance or physical execution discrepancy."
        effect = f"Variance from expected baseline: {rule.expected_value}."
        recommendation = "Conduct detailed document audit and physical site verification."

    return GAGASElements(
        criteria=criteria,
        condition=condition,
        cause_hypothesis=cause,
        effect=effect,
        recommendation=recommendation,
    )


def build_finding_memorandum(
    dossier_id: UUID,
    title: str,
    severity: FindingSeverity,
    evidence_hashes: list[str],
    rule_result: RuleEvaluationResult | None = None,
    gagas_elements: GAGASElements | None = None,
    custom_facts: list[str] | None = None,
    custom_model_outputs: list[str] | None = None,
    custom_rule_results: list[str] | None = None,
    custom_inferences: list[str] | None = None,
    custom_recommendations: list[str] | None = None,
) -> AuditFindingMemorandum:
    """Compile an AuditFindingMemorandum with strict epistemic segregation and lexical filtering."""
    # 1. Enforce deterministic lexical filter on title
    sanitized_title, guard_passed = sanitize_lexical_tokens(title)

    # 2. Derive GAGAS elements if not provided
    if gagas_elements is None:
        if rule_result is not None:
            gagas_elements = _build_rule_gagas_elements(rule_result)
        else:
            gagas_elements = GAGASElements(
                criteria="Municipal Public Works Contractual and Operational Specifications.",
                condition="Operational variance identified in evidentiary submission.",
                cause_hypothesis="Algorithmic Cause Hypothesis: Documentation deficiency or telemetry variance.",
                effect="Unverified billing item requires auditor reconciliation.",
                recommendation="Review supporting work measurement records and corroborative telemetry.",
            )

    # Sanitize GAGAS elements
    clean_crit, p1 = sanitize_lexical_tokens(gagas_elements.criteria)
    clean_cond, p2 = sanitize_lexical_tokens(gagas_elements.condition)
    clean_cause, p3 = sanitize_lexical_tokens(gagas_elements.cause_hypothesis)
    clean_eff, p4 = sanitize_lexical_tokens(gagas_elements.effect)
    clean_rec, p5 = sanitize_lexical_tokens(gagas_elements.recommendation)
    all_guard_passed = guard_passed and all([p1, p2, p3, p4, p5])

    clean_gagas = GAGASElements(
        criteria=clean_crit,
        condition=clean_cond,
        cause_hypothesis=clean_cause,
        effect=clean_eff,
        recommendation=clean_rec,
    )

    # 3. Assemble Epistemic Breakdown
    facts = custom_facts or []
    model_outputs = custom_model_outputs or []
    rule_results_list = custom_rule_results or []
    inferences = custom_inferences or []
    recs = custom_recommendations or [clean_rec]

    if rule_result is not None:
        rule_results_list.append(
            f"[{rule_result.rule_id}] Status: {rule_result.status.value}; "
            f"Observed: {rule_result.observed_value}; Expected: {rule_result.expected_value}; "
            f"Delta: {rule_result.discrepancy_delta} (Tolerance: {rule_result.tolerance})"
        )

    # Add cryptographic hash facts
    for h in evidence_hashes:
        facts.append(f"Cryptographically verified source artifact SHA-256 digest: {h}")

    epistemic_map: dict[str, list[str]] = {
        EpistemicCategory.FACT.value: facts,
        EpistemicCategory.MODEL_OUTPUT.value: model_outputs,
        EpistemicCategory.RULE_RESULT.value: rule_results_list,
        EpistemicCategory.INFERENCE.value: inferences,
        EpistemicCategory.RECOMMENDATION.value: recs,
    }

    return AuditFindingMemorandum(
        dossier_id=dossier_id,
        rule_id=rule_result.rule_id if rule_result else None,
        title=sanitized_title,
        severity=severity,
        epistemic_breakdown=epistemic_map,
        gagas_elements=clean_gagas,
        evidence_hashes=evidence_hashes,
        lexical_guard_passed=all_guard_passed,
    )
