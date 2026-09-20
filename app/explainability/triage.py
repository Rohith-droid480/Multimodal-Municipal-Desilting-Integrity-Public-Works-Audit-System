"""MuniAudit-AI — Executive Triage & Attribution Formatter.

Translates mathematical evidential fusion results, leave-one-out marginal attributions,
and uncertainty metrics into plain municipal civil engineering audit narratives
for vigilance officers.
Adheres strictly to Locked Architecture v1.0 and Section 33 triage semantics.
"""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.domain.models import Dossier
from app.fusion.engine import ConfidenceTier, FusionResult, PriorityTier


class ExecutiveTriageDossier(BaseModel):
    """Executive summary and operational causal attribution for an audit claim."""

    dossier_id: UUID = Field(..., description="Dossier identifier")
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
    priority_tier: PriorityTier = Field(..., description="Categorical review triage tier")
    confidence_tier: ConfidenceTier = Field(..., description="Epistemic confidence tier")
    operational_summary: str = Field(..., description="Civil engineering executive narrative")
    causal_attributions: list[str] = Field(
        default_factory=list,
        description="Plain-language causal explanations derived from LOO attributions",
    )
    technical_data_gaps: list[str] = Field(
        default_factory=list,
        description="Non-punitive explanations of unobserved or missing telemetry channels",
    )
    hard_gate_notice: str | None = Field(
        default=None,
        description="Formal notice if a Tier 1 metrological violation halted processing",
    )
    generated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


def format_executive_triage(
    dossier: Dossier,
    fusion_result: FusionResult,
) -> ExecutiveTriageDossier:
    """Translate mathematical fusion outputs and LOO attributions into an executive triage report."""
    dossier_id = dossier.dossier_id
    ecs = fusion_result.evidence_consistency_score
    arpi = fusion_result.audit_review_priority_index
    priority = fusion_result.priority_tier
    conf_tier = fusion_result.confidence_tier

    causal_attributions: list[str] = []
    technical_gaps: list[str] = []
    hard_gate_notice: str | None = None

    # 1. Tier 1 Hard Gate Notice
    if fusion_result.hard_gate_violation:
        hard_gate_notice = (
            f"STATUTORY METROLOGICAL HALT: Incontrovertible invariant failure detected under "
            f"Rule {fusion_result.hard_gate_rule_id}. Claim review priority locked to CRITICAL (ARPI: 100.0). "
            f"Automated payment processing suspended pending physical verification."
        )

    # 2. Causal attributions derived from LOO attributions & rule findings
    attrs = fusion_result.modality_attributions

    # Visual attribution
    visual_weight = attrs.get("visual", 0.0)
    if visual_weight > 0.20:
        causal_attributions.append(
            f"Visual Photographic Telemetry (Attribution: {visual_weight * 100:.1f}%): "
            f"Image feature descriptor similarity approaches or exceeds duplicate threshold (Sc >= 0.85). "
            f"Suggests potential re-use of site photography across distinct Measurement Book (MB) billing entries."
        )

    # OCR / Mass Balance attribution
    ocr_weight = attrs.get("ocr", 0.0)
    if ocr_weight > 0.20:
        causal_attributions.append(
            f"Weighbridge Docket OCR (Attribution: {ocr_weight * 100:.1f}%): "
            f"Arithmetic variance between Gross, Tare, and Net weights exceeds calibration tolerance (20.0 kg) "
            f"or exhibits character substitution noise along thermal print lines."
        )

    # Geospatial attribution
    geo_weight = attrs.get("geospatial", 0.0)
    if geo_weight > 0.20:
        causal_attributions.append(
            f"Geospatial Haul Kinematics (Attribution: {geo_weight * 100:.1f}%): "
            f"Calculated transit velocity between drain reach chainage stationing and disposal geofence "
            f"exceeds plausible urban municipal fleet operating speed ceiling (80.0 km/h)."
        )

    # Physical Density attribution
    density_weight = attrs.get("density", 0.0)
    if density_weight > 0.20:
        causal_attributions.append(
            f"Physical Material Bulk Density (Attribution: {density_weight * 100:.1f}%): "
            f"Calculated bulk density exceeds maximum saturated wet silt capacity (1.90 t/m³), "
            f"indicating declared net haul mass exceeds the physical volumetric envelope of the tipper bed."
        )

    # Temporal attribution
    temporal_weight = attrs.get("temporal", 0.0)
    if temporal_weight > 0.20:
        causal_attributions.append(
            f"Project Lifecycle Chronology (Attribution: {temporal_weight * 100:.1f}%): "
            f"Milestone event sequence exhibits chronological inversion between work execution, "
            f"weighbridge logging, and invoice submission dates."
        )

    # Fallback if compliant or low variance
    if not causal_attributions and not fusion_result.hard_gate_violation:
        causal_attributions.append(
            "Multi-modal cross-corroboration confirms physical coherence across weighbridge dockets, "
            "reach chainage stationing, volumetric bed capacities, and project lifecycle milestones."
        )

    # 3. Technical Data Gaps (Non-Punitive Explanations)
    for mod in fusion_result.missing_modalities:
        if mod == "visual_similarity":
            technical_gaps.append(
                "Site photography was unavailable or unindexed; visual deduplication analysis "
                "was bypassed without implying work non-execution."
            )
        elif mod == "weighbridge_ocr":
            technical_gaps.append(
                "Weighbridge thermal receipt was degraded, unreadable, or missing; extraction "
                "evaluated as INCONCLUSIVE_DATA rather than adverse noncompliance."
            )
        elif mod == "geospatial_telemetry":
            technical_gaps.append(
                "GPS trip coordinates or disposal geofence timestamps were not recorded; "
                "transit kinematics evaluated as neutral uncertainty without alleging route falsification."
            )
        elif mod == "physical_density":
            technical_gaps.append(
                "Tipper volumetric dimensions were unrecorded; bulk density check abstained safely."
            )
        elif mod == "temporal_sequence":
            technical_gaps.append(
                "Lifecycle milestone dates were incomplete; temporal sequence verification was inconclusive."
            )

    # 4. Construct Operational Summary Narrative
    claimed_inr = f"INR {dossier.claimed_amount_inr:,.2f}"
    if fusion_result.hard_gate_violation:
        summary = (
            f"Dossier {dossier_id} (Running Account Bill claim: {claimed_inr}) triggered a Tier 1 "
            f"statutory hard gate ({fusion_result.hard_gate_rule_id}). Overall Evidence Consistency Score "
            f"is suppressed to {ecs:.2f} with Review Priority CRITICAL (ARPI: {arpi:.1f}/100). "
            f"Vigilance inspection must verify scale load calibration and physical tipper tare before disbursement."
        )
    elif conf_tier == ConfidenceTier.INSUFFICIENT_DATA:
        summary = (
            f"Dossier {dossier_id} (Running Account Bill claim: {claimed_inr}) exhibits substantial technical data gaps "
            f"across {len(fusion_result.missing_modalities)} telemetry channel(s). Fused uncertainty is elevated (Confidence: {conf_tier.value}). "
            f"Under Section 34 non-punitive standards, unobserved channels dilute confidence to {conf_tier.value} "
            f"without imputing wrongdoing. Review Priority assigned as {priority.value} (ARPI: {arpi:.1f}/100)."
        )
    else:
        summary = (
            f"Dossier {dossier_id} (Running Account Bill claim: {claimed_inr}) completed multimodal evidential reconciliation "
            f"with Evidence Consistency Score of {ecs:.2f} (Confidence: {conf_tier.value}). Assigned Review Priority {priority.value} "
            f"(ARPI: {arpi:.1f}/100) reflecting operational corroboration across municipal chainage stationing, weighbridge slips, and material volume."
        )

    return ExecutiveTriageDossier(
        dossier_id=dossier_id,
        evidence_consistency_score=ecs,
        audit_review_priority_index=arpi,
        priority_tier=priority,
        confidence_tier=conf_tier,
        operational_summary=summary,
        causal_attributions=causal_attributions,
        technical_data_gaps=technical_gaps,
        hard_gate_notice=hard_gate_notice,
    )
