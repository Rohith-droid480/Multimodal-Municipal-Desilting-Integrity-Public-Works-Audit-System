"""Visual Metric Embedding & Near-Duplicate Photo Deduplication Engine.

Under Locked Architecture v1.0, visual similarity extraction is CPU-compatible,
strictly normalized, and epistemic outputs are categorized as MODEL_OUTPUT.
Visual similarity scores represent visual correspondence, NOT adverse determinations.
"""

from io import BytesIO
from typing import Any
from uuid import UUID

import numpy as np
from PIL import Image
from pydantic import BaseModel, Field

from app.domain.epistemic import EpistemicCategory, ProvenanceTag

EMBEDDING_DIMENSION = 512
DUPLICATE_SIMILARITY_THRESHOLD = 0.85


class DuplicateMatchCandidate(BaseModel):
    """Structured candidate near-duplicate match result.

    Epistemic Invariant: Always classified as MODEL_OUTPUT. High similarity indicates
    spatial/visual resemblance and physical viewpoint correlation, NOT an adverse finding.
    """

    target_evidence_id: UUID
    candidate_evidence_id: UUID
    similarity_score: float = Field(..., ge=-1.0, le=1.0)
    is_duplicate_candidate: bool
    epistemic_category: EpistemicCategory = Field(default=EpistemicCategory.MODEL_OUTPUT)
    provenance_tag: ProvenanceTag
    explanation: str


def compute_cosine_similarity(
    vec_a: list[float] | np.ndarray, vec_b: list[float] | np.ndarray
) -> float:
    """Computes cosine similarity between two vectors.

    Assumes or enforces L2-normalization: S_C(u, v) = u . v.
    """
    arr_a = np.asarray(vec_a, dtype=np.float32)
    arr_b = np.asarray(vec_b, dtype=np.float32)

    norm_a = np.linalg.norm(arr_a)
    norm_b = np.linalg.norm(arr_b)

    if norm_a < 1e-9 or norm_b < 1e-9:
        return 0.0

    dot = float(np.dot(arr_a, arr_b) / (norm_a * norm_b))
    return float(np.clip(dot, -1.0, 1.0))


def batch_compute_similarity_matrix(
    embeddings: list[list[float]] | np.ndarray,
) -> np.ndarray:
    """Computes an N x N pairwise cosine similarity matrix for a batch of L2-normalized embeddings."""
    matrix = np.asarray(embeddings, dtype=np.float32)
    if matrix.ndim != 2:
        raise ValueError(f"Expected 2D embedding matrix, got shape {matrix.shape}")

    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    norms[norms < 1e-9] = 1.0
    normalized = matrix / norms
    similarity_matrix = np.dot(normalized, normalized.T)
    res: np.ndarray = np.asarray(np.clip(similarity_matrix, -1.0, 1.0), dtype=np.float32)
    return res


class VisualEmbeddingExtractor:
    """Lightweight, CPU-executable image embedding extractor.

    Generates 512-dimensional L2-normalized spatial-structural descriptors
    capturing spatial color moments and edge gradients. Compatible with
    pgvector indexing in PostgreSQL.
    """

    def __init__(self, dimension: int = EMBEDDING_DIMENSION) -> None:
        if dimension != 512:
            raise ValueError(f"Standard MuniAudit descriptor dimension is 512, got {dimension}")
        self.dimension = dimension

    def extract_from_bytes(self, image_bytes: bytes) -> list[float]:
        """Extracts a 512-dimensional L2-normalized embedding from raw image bytes."""
        try:
            with Image.open(BytesIO(image_bytes)) as img:
                return self.extract_from_image(img)
        except Exception as e:
            raise ValueError(f"Failed to parse image bytes for visual feature extraction: {e}") from e

    def extract_from_image(self, image: Image.Image) -> list[float]:
        """Extracts a 512-dimensional L2-normalized embedding from a PIL Image.

        Uses an 8x8 spatial grid (64 cells) x 8 features per cell:
          - Mean R, Mean G, Mean B
          - Std R, Std G, Std B
          - Horizontal gradient energy
          - Vertical gradient energy
        Total features = 64 * 8 = 512 features.
        """
        # Convert to standardized 256x256 RGB
        rgb_img = image.convert("RGB").resize((256, 256), Image.Resampling.BILINEAR)
        img_arr = np.asarray(rgb_img, dtype=np.float32) / 255.0  # (256, 256, 3)

        # Compute horizontal and vertical gradients
        # np.pad to preserve shape (256, 256, 3)
        dx = np.abs(np.diff(img_arr, axis=1, append=img_arr[:, -1:, :]))
        dy = np.abs(np.diff(img_arr, axis=0, append=img_arr[-1:, :, :]))

        # Divide into 8x8 grid (each cell is 32x32 pixels)
        grid_h, grid_w = 8, 8
        cell_h, cell_w = 32, 32
        features: list[float] = []

        for r in range(grid_h):
            for c in range(grid_w):
                y0, y1 = r * cell_h, (r + 1) * cell_h
                x0, x1 = c * cell_w, (c + 1) * cell_w

                cell_rgb = img_arr[y0:y1, x0:x1, :]
                cell_dx = dx[y0:y1, x0:x1, :]
                cell_dy = dy[y0:y1, x0:x1, :]

                # 3 Channel Means
                mean_r, mean_g, mean_b = float(np.mean(cell_rgb[:, :, 0])), float(np.mean(cell_rgb[:, :, 1])), float(np.mean(cell_rgb[:, :, 2]))
                # 3 Channel Standard Deviations
                std_r, std_g, std_b = float(np.std(cell_rgb[:, :, 0])), float(np.std(cell_rgb[:, :, 1])), float(np.std(cell_rgb[:, :, 2]))
                # 2 Gradient Energies
                grad_h = float(np.mean(cell_dx))
                grad_v = float(np.mean(cell_dy))

                features.extend([mean_r, mean_g, mean_b, std_r, std_g, std_b, grad_h, grad_v])

        vector = np.asarray(features, dtype=np.float32)
        norm = np.linalg.norm(vector)
        if norm > 1e-9:
            vector = vector / norm
        else:
            vector = np.ones_like(vector) / np.sqrt(len(vector))

        return [float(x) for x in vector]

    def find_duplicate_candidates(
        self,
        target_evidence_id: UUID,
        target_embedding: list[float],
        candidate_pool: list[dict[str, Any]],
        threshold: float = DUPLICATE_SIMILARITY_THRESHOLD,
    ) -> list[DuplicateMatchCandidate]:
        """Scans candidate evidence items in candidate_pool and identifies near-duplicate matches.

        Each item in candidate_pool must contain:
          - 'evidence_id': UUID
          - 'embedding': list[float]
          - 'provenance_tag': ProvenanceTag (or string)
        """
        results: list[DuplicateMatchCandidate] = []

        for cand in candidate_pool:
            cand_id = cand["evidence_id"]
            if cand_id == target_evidence_id:
                continue

            cand_emb = cand["embedding"]
            prov = cand.get("provenance_tag", ProvenanceTag.SYNTHETIC_DATA)
            if isinstance(prov, str):
                prov = ProvenanceTag(prov)

            sim = compute_cosine_similarity(target_embedding, cand_emb)
            is_match = sim >= threshold

            expl = (
                f"Visual correspondence detected: cosine similarity {sim:.4f} exceeds duplicate "
                f"threshold {threshold:.2f}. Indicates high scene/viewpoint resemblance."
                if is_match
                else f"Distinct scene: cosine similarity {sim:.4f} is below threshold {threshold:.2f}."
            )

            results.append(
                DuplicateMatchCandidate(
                    target_evidence_id=target_evidence_id,
                    candidate_evidence_id=cand_id,
                    similarity_score=round(sim, 4),
                    is_duplicate_candidate=is_match,
                    epistemic_category=EpistemicCategory.MODEL_OUTPUT,
                    provenance_tag=prov,
                    explanation=expl,
                )
            )

        # Sort matches by highest similarity first
        results.sort(key=lambda m: m.similarity_score, reverse=True)
        return results
