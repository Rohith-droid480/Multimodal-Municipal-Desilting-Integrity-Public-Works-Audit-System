"""Unit & Boundary Tests for Document OCR & Weighbridge Extraction Engine."""

from PIL import Image

from app.domain.epistemic import AdministrativeState, EpistemicCategory
from app.ingestion.synthetic_generator import (
    WeighbridgeAnomalyType,
    generate_synthetic_receipt_data,
    render_thermal_receipt_image,
)
from app.ml.ocr_engine import DocumentOCREngine


def test_extract_clean_synthetic_slip_text() -> None:
    engine = DocumentOCREngine()
    sample_text = """
    *** MUNICIPAL PUBLIC WORKS AUDIT ***
    WARD-09 CENTRAL DISPATCH WEIGHBRIDGE
    CERTIFIED HEAVY VEHICLE SCALE
    -------------------------------------------
    TICKET NUMBER: WB-2026-BLR-0042
    VEHICLE REG NO: KA-04-E-1042
    MATERIAL CODE: SILT-DESILT-01
    IN-TIME: 2026-09-20 10:15:00
    OUT-TIME: 2026-09-20 10:45:00
    -------------------------------------------
    GROSS WEIGHT: 24,500.0 KG
    TARE WEIGHT: 8,200.0 KG
    NET DISPATCH: 16,300.0 KG
    """

    res = engine.parse_text(sample_text)
    assert res.ticket_id == "WB-2026-BLR-0042"
    assert res.vehicle_registration == "KA-04-E-1042"
    assert res.gross_weight_kg == 24500.0
    assert res.tare_weight_kg == 8200.0
    assert res.net_weight_kg == 16300.0
    assert res.arithmetic_consistent is True
    assert res.mass_discrepancy_kg == 0.0
    assert res.administrative_state == AdministrativeState.VERIFIED_COMPLIANT
    # Epistemic Invariant
    assert res.epistemic_category == EpistemicCategory.MODEL_OUTPUT


def test_extract_from_synthetic_slip_image() -> None:
    engine = DocumentOCREngine()
    slip_data = generate_synthetic_receipt_data(
        anomaly_type=WeighbridgeAnomalyType.NONE,
        ticket_seed=123,
    )
    png_bytes = render_thermal_receipt_image(slip_data)

    res = engine.parse_image(png_bytes)
    assert res.ticket_id == slip_data.ticket_id
    assert res.vehicle_registration == slip_data.vehicle_registration
    assert res.gross_weight_kg == slip_data.gross_weight_kg
    assert res.tare_weight_kg == slip_data.tare_weight_kg
    assert res.net_weight_kg == slip_data.net_weight_kg
    assert res.arithmetic_consistent is True
    assert res.administrative_state == AdministrativeState.VERIFIED_COMPLIANT


def test_token_bounding_boxes_and_confidence() -> None:
    engine = DocumentOCREngine()
    sample_text = """
    TICKET NUMBER: WB-2026-BLR-9999
    VEHICLE REG NO: KA-01-EA-5555
    GROSS WEIGHT: 20,000.0 KG
    TARE WEIGHT: 7,000.0 KG
    NET DISPATCH: 13,000.0 KG
    """
    res = engine.parse_text(sample_text)

    # Check token boxes
    assert "ticket_id" in res.token_boxes
    box = res.token_boxes["ticket_id"]
    assert 0.0 <= box.ymin <= box.ymax <= 1.0
    assert 0.0 <= box.xmin <= box.xmax <= 1.0
    assert box.confidence > 0.80

    assert "gross_weight_kg" in res.token_boxes
    w_box = res.token_boxes["gross_weight_kg"]
    assert 0.0 <= w_box.ymin <= w_box.ymax <= 1.0

    assert res.overall_confidence >= 0.80


def test_safe_failure_degraded_image() -> None:
    engine = DocumentOCREngine()
    # Create a degraded, solid uniform gray image (std dev < 5.0)
    solid_img = Image.new("RGB", (300, 400), color=(128, 128, 128))

    res = engine.parse_image(solid_img)

    # Must flag safe failure: INCONCLUSIVE_DATA
    assert res.administrative_state == AdministrativeState.INCONCLUSIVE_DATA
    # CRITICAL INVARIANT: Missing fields must remain None, NEVER default to 0 kg
    assert res.gross_weight_kg is None
    assert res.tare_weight_kg is None
    assert res.net_weight_kg is None
    assert res.gross_weight_kg != 0
    assert res.overall_confidence == 0.0


def test_substantive_inconsistency_arithmetic_mismatch() -> None:
    engine = DocumentOCREngine()
    # 25,000 - 8,000 = 17,000 != 14,000 (discrepancy = 3,000 kg > 20 kg)
    inconsistent_text = """
    TICKET NUMBER: WB-2026-ANOM-01
    VEHICLE REG NO: KA-02-B-9999
    GROSS WEIGHT: 25,000.0 KG
    TARE WEIGHT: 8,000.0 KG
    NET DISPATCH: 14,000.0 KG
    """
    res = engine.parse_text(inconsistent_text)

    assert res.arithmetic_consistent is False
    assert res.mass_discrepancy_kg == 3000.0
    assert res.administrative_state == AdministrativeState.SUBSTANTIVE_INCONSISTENCY


def test_malformed_bytes_technical_abstention() -> None:
    engine = DocumentOCREngine()
    corrupt_bytes = b"NOT_A_VALID_IMAGE_OR_PNG_STREAM_12345"

    res = engine.parse_image(corrupt_bytes)
    assert res.administrative_state == AdministrativeState.TECHNICAL_ABSTENTION
    assert res.gross_weight_kg is None
