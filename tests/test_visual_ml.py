"""Unit & Property Tests for Visual Metric Embedding Engine."""

from uuid import uuid4

import numpy as np
from PIL import Image, ImageEnhance

from app.domain.epistemic import EpistemicCategory, ProvenanceTag
from app.ml.visual_embeddings import (
    DUPLICATE_SIMILARITY_THRESHOLD,
    EMBEDDING_DIMENSION,
    VisualEmbeddingExtractor,
    batch_compute_similarity_matrix,
    compute_cosine_similarity,
)


def _create_sample_scene(color_base: tuple[int, int, int] = (100, 150, 200)) -> Image.Image:
    """Creates a deterministic synthetic test image with spatial gradients."""
    arr = np.zeros((256, 256, 3), dtype=np.uint8)
    for y in range(256):
        for x in range(256):
            arr[y, x, 0] = (color_base[0] + x // 2) % 256
            arr[y, x, 1] = (color_base[1] + y // 2) % 256
            arr[y, x, 2] = (color_base[2] + (x + y) // 4) % 256
    return Image.fromarray(arr, mode="RGB")


def test_embedding_dimension_and_l2_norm() -> None:
    extractor = VisualEmbeddingExtractor()
    img = _create_sample_scene((80, 120, 160))

    vec = extractor.extract_from_image(img)
    assert len(vec) == EMBEDDING_DIMENSION

    # Verify L2-normalization: ||v||_2 == 1.0
    l2_norm = float(np.linalg.norm(np.asarray(vec, dtype=np.float32)))
    assert abs(l2_norm - 1.0) < 1e-4


def test_identical_images_similarity_unity() -> None:
    extractor = VisualEmbeddingExtractor()
    img = _create_sample_scene((50, 100, 150))

    vec1 = extractor.extract_from_image(img)
    vec2 = extractor.extract_from_image(img.copy())

    sim = compute_cosine_similarity(vec1, vec2)
    assert abs(sim - 1.0) < 1e-4


def test_transformed_image_high_similarity() -> None:
    extractor = VisualEmbeddingExtractor()
    base_img = _create_sample_scene((60, 130, 200))

    # Apply subtle brightness enhancement and mild crop
    enhancer = ImageEnhance.Brightness(base_img)
    perturbed_img = enhancer.enhance(1.04)  # 4% brightness change

    vec_base = extractor.extract_from_image(base_img)
    vec_pert = extractor.extract_from_image(perturbed_img)

    sim = compute_cosine_similarity(vec_base, vec_pert)
    # Cosine similarity on near-duplicate should exceed duplicate threshold
    assert sim >= DUPLICATE_SIMILARITY_THRESHOLD


def test_distinct_images_low_similarity() -> None:
    extractor = VisualEmbeddingExtractor()
    # Scene A: Blue-dominant
    img_a = _create_sample_scene((10, 20, 220))
    # Scene B: Red/Yellow-dominant
    img_b = _create_sample_scene((220, 180, 15))

    vec_a = extractor.extract_from_image(img_a)
    vec_b = extractor.extract_from_image(img_b)

    sim = compute_cosine_similarity(vec_a, vec_b)
    # Different scenes must yield low cosine similarity
    assert sim < 0.70


def test_batch_compute_similarity_matrix() -> None:
    extractor = VisualEmbeddingExtractor()
    img1 = _create_sample_scene((10, 20, 30))
    img2 = _create_sample_scene((100, 120, 140))
    img3 = _create_sample_scene((200, 210, 220))

    embs = [
        extractor.extract_from_image(img1),
        extractor.extract_from_image(img2),
        extractor.extract_from_image(img3),
    ]

    sim_matrix = batch_compute_similarity_matrix(embs)
    assert sim_matrix.shape == (3, 3)

    # Diagonal must be 1.0
    for i in range(3):
        assert abs(sim_matrix[i, i] - 1.0) < 1e-4


def test_find_duplicate_candidates_epistemic_classification() -> None:
    extractor = VisualEmbeddingExtractor()
    base_img = _create_sample_scene((90, 110, 130))
    near_dup = ImageEnhance.Brightness(base_img).enhance(1.02)
    distinct_arr = np.zeros((256, 256, 3), dtype=np.uint8)
    distinct_arr[::16, :, 0] = 255
    distinct_arr[:, ::16, 1] = 255
    distinct_img = Image.fromarray(distinct_arr)

    target_id = uuid4()
    near_dup_id = uuid4()
    distinct_id = uuid4()

    target_emb = extractor.extract_from_image(base_img)
    candidate_pool = [
        {
            "evidence_id": near_dup_id,
            "embedding": extractor.extract_from_image(near_dup),
            "provenance_tag": ProvenanceTag.SYNTHETIC_DATA,
        },
        {
            "evidence_id": distinct_id,
            "embedding": extractor.extract_from_image(distinct_img),
            "provenance_tag": ProvenanceTag.REAL_MUNICIPAL_DATA,
        },
    ]

    matches = extractor.find_duplicate_candidates(
        target_evidence_id=target_id,
        target_embedding=target_emb,
        candidate_pool=candidate_pool,
        threshold=0.85,
    )

    assert len(matches) == 2
    top_match = matches[0]
    assert top_match.candidate_evidence_id == near_dup_id
    assert top_match.is_duplicate_candidate is True
    assert top_match.similarity_score >= 0.85
    # Strict Epistemic Invariant: Output is MODEL_OUTPUT, not an accusation
    assert top_match.epistemic_category == EpistemicCategory.MODEL_OUTPUT

    distinct_match = matches[1]
    assert distinct_match.candidate_evidence_id == distinct_id
    assert distinct_match.is_duplicate_candidate is False
