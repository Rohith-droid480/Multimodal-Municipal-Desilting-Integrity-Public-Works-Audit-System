"""Unit tests for procedural synthetic weighbridge receipt generator."""

from app.domain.epistemic import ProvenanceTag
from app.ingestion.synthetic_generator import (
    ProceduralWeighbridgeGenerator,
    WeighbridgeAnomalyType,
    generate_synthetic_receipt_data,
    render_thermal_receipt_image,
)


def test_generate_clean_receipt_arithmetic():
    data = generate_synthetic_receipt_data(anomaly_type=WeighbridgeAnomalyType.NONE, ticket_seed=123)
    assert data.provenance_tag == ProvenanceTag.SYNTHETIC_DATA
    assert len(data.anomaly_flags) == 0
    # Net = Gross - Tare invariant
    assert abs(data.net_weight_kg - (data.gross_weight_kg - data.tare_weight_kg)) < 1e-4
    assert data.out_timestamp > data.in_timestamp
    assert "KA-" in data.vehicle_registration


def test_anomaly_tare_exceeds_gross():
    data = generate_synthetic_receipt_data(
        anomaly_type=WeighbridgeAnomalyType.TARE_EXCEEDS_GROSS, ticket_seed=456
    )
    assert WeighbridgeAnomalyType.TARE_EXCEEDS_GROSS in data.anomaly_flags
    assert data.tare_weight_kg > data.gross_weight_kg


def test_anomaly_impossible_haul_weight():
    data = generate_synthetic_receipt_data(
        anomaly_type=WeighbridgeAnomalyType.IMPOSSIBLE_HAUL_WEIGHT, ticket_seed=789
    )
    assert WeighbridgeAnomalyType.IMPOSSIBLE_HAUL_WEIGHT in data.anomaly_flags
    assert data.net_weight_kg >= 40000.0


def test_anomaly_timestamp_reversal():
    data = generate_synthetic_receipt_data(
        anomaly_type=WeighbridgeAnomalyType.TIMESTAMP_REVERSAL, ticket_seed=101
    )
    assert WeighbridgeAnomalyType.TIMESTAMP_REVERSAL in data.anomaly_flags
    assert data.out_timestamp < data.in_timestamp


def test_render_thermal_receipt_png_bytes():
    data = generate_synthetic_receipt_data(ticket_seed=202)
    png_bytes = render_thermal_receipt_image(data, add_noise=True, rotation_angle=0.5)

    assert len(png_bytes) > 1000
    # Valid PNG Magic Number
    assert png_bytes[:8] == b"\x89PNG\r\n\x1a\n"


def test_generator_save_to_disk(tmp_path):
    generator = ProceduralWeighbridgeGenerator(output_dir=tmp_path)
    data, png_path = generator.generate_and_save(ticket_seed=303)

    assert png_path.exists()
    assert png_path.stat().st_size > 0
    json_path = tmp_path / f"{data.ticket_id}.json"
    assert json_path.exists()
