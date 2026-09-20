"""MuniAudit-AI — Evidential Opinion Mappers.

Maps heterogeneous multimodal signals (visual duplicate embeddings, OCR confidence,
geospatial kinematics, silt volumetric density, temporal sequence) into Subjective
Logic opinions (b, d, u, a).
Follows Locked Architecture v1.0 and Section 34 missing modality non-punitive semantics.
"""

from __future__ import annotations

from app.fusion.subjective_logic import (
    SubjectiveOpinion,
    create_opinion,
    vacuous_opinion,
)


def map_visual_similarity_to_opinion(
    similarity: float | None,
    confidence: float = 1.0,
    duplicate_threshold: float = 0.85,
) -> SubjectiveOpinion:
    """Map pairwise image cosine similarity into a subjective opinion on duplicate reuse.

    - Missing or unextracted image: vacuous opinion (u=1.0).
    - Similarity >= duplicate_threshold (0.85): soft anomaly indicating potential duplicate reuse.
    - Similarity < 0.70: distinct site photography corroborating genuine documentation.
    - Intermediate range: elevated epistemic uncertainty.
    """
    if similarity is None:
        return vacuous_opinion()

    sim = float(similarity)
    conf = max(0.1, min(1.0, float(confidence)))

    if sim >= duplicate_threshold:
        # High similarity indicates near-duplicate reuse
        excess = min(1.0, (sim - duplicate_threshold) / (1.0 - duplicate_threshold))
        belief = (0.50 + 0.40 * excess) * conf
        uncertainty = max(0.05, 1.0 - belief)
        disbelief = 0.0
        return create_opinion(belief, disbelief, uncertainty)

    if sim < 0.70:
        # Distinct images corroborate authentic site capture
        disbelief = 0.75 * conf
        belief = 0.0
        uncertainty = 1.0 - disbelief
        return create_opinion(belief, disbelief, uncertainty)

    # Indeterminate range [0.70, 0.85)
    normalized = (sim - 0.70) / (duplicate_threshold - 0.70)
    belief = 0.20 * normalized * conf
    disbelief = 0.30 * (1.0 - normalized) * conf
    uncertainty = 1.0 - belief - disbelief
    return create_opinion(belief, disbelief, uncertainty)


def map_ocr_extraction_to_opinion(
    mean_confidence: float | None,
    field_completeness: float = 1.0,
    has_arithmetic_mismatch: bool = False,
) -> SubjectiveOpinion:
    """Map weighbridge OCR extraction confidence and completeness into a subjective opinion.

    - Missing slip or failed OCR: vacuous opinion (u=1.0, non-punitive).
    - Arithmetic mismatch: elevated belief in inconsistency.
    - High confidence + complete fields: strong disbelief in inconsistency (corroborating compliance).
    - Low confidence or degraded scan: increases uncertainty u, never creates false belief in fraud.
    """
    if mean_confidence is None:
        return vacuous_opinion()

    if has_arithmetic_mismatch:
        return create_opinion(belief=0.85, disbelief=0.0, uncertainty=0.15)

    conf = max(0.0, min(1.0, float(mean_confidence)))
    comp = max(0.0, min(1.0, float(field_completeness)))

    # Coherence score scaled by extraction quality
    coherence = conf * comp

    if coherence >= 0.70:
        disbelief = 0.80 * coherence
        belief = 0.0
        uncertainty = 1.0 - disbelief
        return create_opinion(belief, disbelief, uncertainty)

    # Degraded scan: primarily epistemic uncertainty
    disbelief = 0.30 * coherence
    belief = 0.0
    uncertainty = 1.0 - disbelief
    return create_opinion(belief, disbelief, uncertainty)


def map_geospatial_kinematics_to_opinion(
    apparent_speed_kmh: float | None,
    speed_ceiling_kmh: float = 80.0,
) -> SubjectiveOpinion:
    """Map apparent haul transit velocity into a subjective opinion.

    - Missing GPS coordinates or duration: vacuous opinion (u=1.0).
    - Speed approaching urban ceiling [60, 80] km/h: moderate anomaly belief.
    - Speed < 60 km/h: normal municipal urban transit speed (corroborates compliance).
    """
    if apparent_speed_kmh is None:
        return vacuous_opinion()

    speed = float(apparent_speed_kmh)

    if speed > speed_ceiling_kmh:
        # Severe breach (catches cases passed to soft layer)
        return create_opinion(belief=0.90, disbelief=0.0, uncertainty=0.10)

    if speed >= 60.0:
        # Approaching traffic plausibility limit
        fraction = (speed - 60.0) / (speed_ceiling_kmh - 60.0)
        belief = 0.20 + 0.45 * fraction
        disbelief = 0.10 * (1.0 - fraction)
        uncertainty = 1.0 - belief - disbelief
        return create_opinion(belief, disbelief, uncertainty)

    # Plausible urban transit speed (< 60 km/h)
    disbelief = 0.80
    belief = 0.0
    uncertainty = 0.20
    return create_opinion(belief, disbelief, uncertainty)


def map_silt_density_to_opinion(
    apparent_density_t_m3: float | None,
    density_ceiling_t_m3: float = 1.90,
) -> SubjectiveOpinion:
    """Map apparent silt bulk density into a subjective opinion.

    - Missing net weight or tipper volume: vacuous opinion (u=1.0).
    - Density exceeding saturation limit: severe anomaly belief.
    - Density approaching limit [1.60, 1.90] t/m³: soft anomaly belief.
    - Normal wet silt [0.90, 1.60) t/m³: strong compliance disbelief.
    """
    if apparent_density_t_m3 is None:
        return vacuous_opinion()

    density = float(apparent_density_t_m3)

    if density > density_ceiling_t_m3:
        return create_opinion(belief=0.90, disbelief=0.0, uncertainty=0.10)

    if density >= 1.60:
        fraction = (density - 1.60) / (density_ceiling_t_m3 - 1.60)
        belief = 0.20 + 0.50 * fraction
        disbelief = 0.15 * (1.0 - fraction)
        uncertainty = 1.0 - belief - disbelief
        return create_opinion(belief, disbelief, uncertainty)

    if density >= 0.90:
        # Standard wet silt bulk density
        disbelief = 0.85
        belief = 0.0
        uncertainty = 0.15
        return create_opinion(belief, disbelief, uncertainty)

    # Exceptionally low density (< 0.90 t/m³) - potential dry debris or hollow load
    belief = 0.25
    disbelief = 0.35
    uncertainty = 0.40
    return create_opinion(belief, disbelief, uncertainty)


def map_temporal_sequence_to_opinion(
    has_inversion: bool,
    timestamps_count: int,
) -> SubjectiveOpinion:
    """Map chronological lifecycle ordering into a subjective opinion.

    - Insufficient timestamps (< 2): vacuous opinion (u=1.0).
    - Chronological inversion: strong belief in inconsistency.
    - Monotonic ordering: corroborates procedural compliance.
    """
    if timestamps_count < 2:
        return vacuous_opinion()

    if has_inversion:
        return create_opinion(belief=0.90, disbelief=0.0, uncertainty=0.10)

    # Monotonic progression verified
    return create_opinion(belief=0.0, disbelief=0.85, uncertainty=0.15)
