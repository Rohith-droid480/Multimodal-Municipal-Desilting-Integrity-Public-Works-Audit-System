"""MuniAudit-AI Core ML Package.

Provides CPU-compatible visual metric embeddings and document OCR extraction
under Locked Architecture v1.0 and strict epistemic categorization.
"""

from app.ml.ocr_engine import DocumentOCREngine, ExtractedSlipData, TokenBoundingBox
from app.ml.visual_embeddings import (
    DuplicateMatchCandidate,
    VisualEmbeddingExtractor,
    batch_compute_similarity_matrix,
    compute_cosine_similarity,
)

__all__ = [
    "DocumentOCREngine",
    "DuplicateMatchCandidate",
    "ExtractedSlipData",
    "TokenBoundingBox",
    "VisualEmbeddingExtractor",
    "batch_compute_similarity_matrix",
    "compute_cosine_similarity",
]
