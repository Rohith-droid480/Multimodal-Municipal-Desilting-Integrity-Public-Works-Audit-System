"""Epistemic Categories & Administrative Status Invariants for MuniAudit-AI."""

from enum import Enum


class EpistemicCategory(str, Enum):
    """Rigorous epistemic boundaries required for evidence reconciliation."""

    FACT = "FACT"
    MODEL_OUTPUT = "MODEL_OUTPUT"
    RULE_RESULT = "RULE_RESULT"
    INFERENCE = "INFERENCE"
    RECOMMENDATION = "RECOMMENDATION"


class AdministrativeState(str, Enum):
    """Non-criminal audit determinations made by vigilance officers or the system."""

    VERIFIED_COMPLIANT = "VERIFIED_COMPLIANT"
    SUBSTANTIVE_INCONSISTENCY = "SUBSTANTIVE_INCONSISTENCY"
    INCONCLUSIVE_DATA = "INCONCLUSIVE_DATA"
    TECHNICAL_ABSTENTION = "TECHNICAL_ABSTENTION"


class EvidenceSourceType(str, Enum):
    """Heterogeneous multimodal evidence source categories."""

    SITE_PHOTO = "SITE_PHOTO"
    HISTORICAL_PHOTO = "HISTORICAL_PHOTO"
    WEIGHBRIDGE_RECEIPT = "WEIGHBRIDGE_RECEIPT"
    TRIP_LOG = "TRIP_LOG"
    MEASUREMENT_BOOK = "MEASUREMENT_BOOK"
    CONTRACT_METADATA = "CONTRACT_METADATA"
    DRAIN_GEOMETRY = "DRAIN_GEOMETRY"


class ProvenanceTag(str, Enum):
    """Evidentiary provenance tags to ensure synthetic data is never disguised as real."""

    REAL_MUNICIPAL_DATA = "REAL_MUNICIPAL_DATA"
    REAL_INFRASTRUCTURE_DATA = "REAL_INFRASTRUCTURE_DATA"
    REAL_DOCUMENT_BENCHMARK = "REAL_DOCUMENT_BENCHMARK"
    REAL_TRANSPORT_DATA = "REAL_TRANSPORT_DATA"
    DERIVED_STATUTORY_DATA = "DERIVED_STATUTORY_DATA"
    SYNTHETIC_DATA = "SYNTHETIC_DATA"
    SIMULATED_DATA = "SIMULATED_DATA"


class DossierStatus(str, Enum):
    """Lifecycle states of a municipal billing evidence dossier."""

    CREATED = "CREATED"
    UPLOADING = "UPLOADING"
    FINALIZING = "FINALIZING"
    QUEUED = "QUEUED"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    INCONCLUSIVE = "INCONCLUSIVE"
    TECHNICAL_ABSTENTION = "TECHNICAL_ABSTENTION"


class FindingSeverity(str, Enum):
    """Severity classification for evidentiary anomalies."""

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"
