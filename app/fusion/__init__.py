"""MuniAudit-AI — Evidence Fusion Subsystem.

Exposes Subjective Logic consensus operators, evidential opinion mappers,
two-tier evidence fusion engine, ECS, and ARPI models.
"""

from app.fusion.engine import (
    ConfidenceTier,
    FusionResult,
    PriorityTier,
    fuse_dossier_evidence,
)
from app.fusion.mappers import (
    map_geospatial_kinematics_to_opinion,
    map_ocr_extraction_to_opinion,
    map_silt_density_to_opinion,
    map_temporal_sequence_to_opinion,
    map_visual_similarity_to_opinion,
)
from app.fusion.subjective_logic import (
    SubjectiveOpinion,
    create_opinion,
    dogmatic_opinion,
    fuse_multi_opinions,
    fuse_opinions,
    vacuous_opinion,
)

__all__ = [
    "ConfidenceTier",
    "FusionResult",
    "PriorityTier",
    "SubjectiveOpinion",
    "create_opinion",
    "dogmatic_opinion",
    "fuse_dossier_evidence",
    "fuse_multi_opinions",
    "fuse_opinions",
    "map_geospatial_kinematics_to_opinion",
    "map_ocr_extraction_to_opinion",
    "map_silt_density_to_opinion",
    "map_temporal_sequence_to_opinion",
    "map_visual_similarity_to_opinion",
    "vacuous_opinion",
]
