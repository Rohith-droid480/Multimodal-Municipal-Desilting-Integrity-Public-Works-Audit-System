"""MuniAudit-AI — Explainability and Reporting Subsystem.

Provides Yellow Book (GAGAS) finding memoranda, executive triage formatters,
visual canvas inspection overlays, and deterministic dossier exporters.
"""

from app.explainability.exporter import export_dossier_json, export_dossier_markdown
from app.explainability.memo import (
    AuditFindingMemorandum,
    GAGASElements,
    build_finding_memorandum,
    sanitize_lexical_tokens,
)
from app.explainability.triage import ExecutiveTriageDossier, format_executive_triage
from app.explainability.visual_inspection import (
    OCROverlayInspection,
    OCROverlayToken,
    VisualDuplicateComparison,
    VisualInspectionPackage,
    build_visual_inspection_package,
)

__all__ = [
    "AuditFindingMemorandum",
    "ExecutiveTriageDossier",
    "GAGASElements",
    "OCROverlayInspection",
    "OCROverlayToken",
    "VisualDuplicateComparison",
    "VisualInspectionPackage",
    "build_finding_memorandum",
    "build_visual_inspection_package",
    "export_dossier_json",
    "export_dossier_markdown",
    "format_executive_triage",
    "sanitize_lexical_tokens",
]
