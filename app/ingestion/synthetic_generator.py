"""Procedural Synthetic Weighbridge Receipt Generator with Thermal Artifacts."""

import io
import random
from datetime import UTC, datetime, timedelta
from enum import Enum
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from PIL.PngImagePlugin import PngInfo
from pydantic import BaseModel, Field

from app.domain.epistemic import ProvenanceTag


class WeighbridgeAnomalyType(str, Enum):
    """Controlled anomaly injection flags for forensic benchmark generation."""

    NONE = "NONE"
    TARE_EXCEEDS_GROSS = "TARE_EXCEEDS_GROSS"
    IMPOSSIBLE_HAUL_WEIGHT = "IMPOSSIBLE_HAUL_WEIGHT"
    TIMESTAMP_REVERSAL = "TIMESTAMP_REVERSAL"
    ARITHMETIC_MISMATCH = "ARITHMETIC_MISMATCH"


class WeighbridgeSlipData(BaseModel):
    """Structured procedural representation of a municipal weighbridge voucher."""

    ticket_id: str
    weighbridge_name: str
    vehicle_registration: str
    material: str = "Desilting Sludge / Silt"
    gross_weight_kg: float
    tare_weight_kg: float
    net_weight_kg: float
    in_timestamp: datetime
    out_timestamp: datetime
    anomaly_flags: list[WeighbridgeAnomalyType] = Field(default_factory=list)
    provenance_tag: ProvenanceTag = ProvenanceTag.SYNTHETIC_DATA


WEIGHBRIDGE_LOCATIONS = [
    "BBMP WARD 09 MUNICIPAL WEIGH SCALE #1",
    "KORAMANGALA VALLEY WEIGHBRIDGE STATION",
    "BELLANDUR BASIN DE-SILTING DISPOSAL WEIGHBRIDGE",
    "VARTHUR MARSHALLING YARD CERTIFIED SCALES",
    "CENTRAL PUBLIC WORKS SECTOR-5 SCALE",
]

VEHICLE_PREFIXES = ["KA-01-EA", "KA-03-D", "KA-04-E", "KA-05-AB", "KA-51-C"]


def generate_synthetic_receipt_data(
    anomaly_type: WeighbridgeAnomalyType = WeighbridgeAnomalyType.NONE,
    ticket_seed: int | None = None,
) -> WeighbridgeSlipData:
    """Generates procedurally sound or intentionally anomalous weighbridge metadata."""
    if ticket_seed is not None:
        rng = random.Random(ticket_seed)
    else:
        rng = random.Random()

    ticket_id = f"WB-2026-{rng.randint(100000, 999999)}"
    weighbridge = rng.choice(WEIGHBRIDGE_LOCATIONS)
    plate = f"{rng.choice(VEHICLE_PREFIXES)}-{rng.randint(1000, 9999)}"

    base_time = datetime(2026, 5, 14, 9, 30, tzinfo=UTC) + timedelta(
        minutes=rng.randint(0, 14400)
    )
    in_time = base_time
    duration_minutes = rng.randint(12, 35)
    out_time = in_time + timedelta(minutes=duration_minutes)

    # Standard 2-axle to 3-axle commercial tipper truck
    # Standard Tare: 7,500 - 10,500 kg
    # Standard Gross: 18,000 - 25,000 kg
    tare_weight = float(rng.randint(7500, 10500))
    net_weight = float(rng.randint(8000, 16000))
    gross_weight = tare_weight + net_weight

    anomaly_flags: list[WeighbridgeAnomalyType] = []

    # Anomaly Injections
    if anomaly_type == WeighbridgeAnomalyType.TARE_EXCEEDS_GROSS:
        gross_weight = tare_weight - float(rng.randint(1000, 3000))
        net_weight = gross_weight - tare_weight
        anomaly_flags.append(WeighbridgeAnomalyType.TARE_EXCEEDS_GROSS)

    elif anomaly_type == WeighbridgeAnomalyType.IMPOSSIBLE_HAUL_WEIGHT:
        # Net weight exceeding 42,000 kg on standard municipal tipper
        net_weight = 46500.0
        gross_weight = tare_weight + net_weight
        anomaly_flags.append(WeighbridgeAnomalyType.IMPOSSIBLE_HAUL_WEIGHT)

    elif anomaly_type == WeighbridgeAnomalyType.TIMESTAMP_REVERSAL:
        # Out-time occurs before In-time
        out_time = in_time - timedelta(minutes=45)
        anomaly_flags.append(WeighbridgeAnomalyType.TIMESTAMP_REVERSAL)

    elif anomaly_type == WeighbridgeAnomalyType.ARITHMETIC_MISMATCH:
        # Net does not equal Gross - Tare
        net_weight = (gross_weight - tare_weight) + 2500.0
        anomaly_flags.append(WeighbridgeAnomalyType.ARITHMETIC_MISMATCH)

    return WeighbridgeSlipData(
        ticket_id=ticket_id,
        weighbridge_name=weighbridge,
        vehicle_registration=plate,
        material="Desilting Sludge / Silt",
        gross_weight_kg=gross_weight,
        tare_weight_kg=tare_weight,
        net_weight_kg=net_weight,
        in_timestamp=in_time,
        out_timestamp=out_time,
        anomaly_flags=anomaly_flags,
        provenance_tag=ProvenanceTag.SYNTHETIC_DATA,
    )


def render_thermal_receipt_image(
    data: WeighbridgeSlipData,
    add_noise: bool = True,
    rotation_angle: float | None = None,
) -> bytes:
    """Renders procedural weighbridge slip as a realistic thermal receipt image."""
    width = 500
    height = 700

    # Off-white / aged thermal paper background
    paper_color = (250, 249, 246)
    img = Image.new("RGB", (width, height), color=paper_color)
    draw = ImageDraw.Draw(img)

    # Use default bitmap font to simulate thermal dot-matrix characters
    font = ImageFont.load_default()

    margin = 35
    curr_y = 30

    def draw_centered(text: str, y: int) -> int:
        bbox = font.getbbox(text)
        w = bbox[2] - bbox[0]
        x = (width - w) // 2
        draw.text((x, y), text, fill=(25, 25, 30), font=font)
        return y + 20

    def draw_kv(label: str, val: str, y: int) -> int:
        draw.text((margin, y), label, fill=(35, 35, 40), font=font)
        bbox = font.getbbox(val)
        w = bbox[2] - bbox[0]
        draw.text((width - margin - w, y), val, fill=(15, 15, 20), font=font)
        return y + 22

    # Header
    curr_y = draw_centered("*** MUNICIPAL PUBLIC WORKS AUDIT ***", curr_y)
    curr_y = draw_centered(data.weighbridge_name, curr_y)
    curr_y = draw_centered("CERTIFIED HEAVY VEHICLE SCALE", curr_y)
    curr_y += 10

    # Divider
    draw.line([(margin, curr_y), (width - margin, curr_y)], fill=(120, 120, 120), width=1)
    curr_y += 15

    # Core Ticket Attributes
    curr_y = draw_kv("TICKET NUMBER:", data.ticket_id, curr_y)
    curr_y = draw_kv("VEHICLE REG NO:", data.vehicle_registration, curr_y)
    curr_y = draw_kv("MATERIAL CODE:", data.material, curr_y)
    curr_y += 10

    # Timestamps
    curr_y = draw_kv("IN-TIME:", data.in_timestamp.strftime("%Y-%m-%d %H:%M:%S"), curr_y)
    curr_y = draw_kv("OUT-TIME:", data.out_timestamp.strftime("%Y-%m-%d %H:%M:%S"), curr_y)
    curr_y += 10

    # Weight Table Divider
    draw.line([(margin, curr_y), (width - margin, curr_y)], fill=(160, 160, 160), width=1)
    curr_y += 15

    # Gross / Tare / Net Weights
    curr_y = draw_kv("GROSS WEIGHT:", f"{data.gross_weight_kg:,.1f} KG", curr_y)
    curr_y = draw_kv("TARE WEIGHT:", f"{data.tare_weight_kg:,.1f} KG", curr_y)
    draw.line([(margin + 100, curr_y + 5), (width - margin, curr_y + 5)], fill=(60, 60, 60), width=1)
    curr_y += 12
    curr_y = draw_kv("NET DISPATCH:", f"{data.net_weight_kg:,.1f} KG", curr_y)
    curr_y += 25

    # Barcode Simulation
    barcode_y = curr_y
    random_gen = random.Random(hash(data.ticket_id))
    for x in range(margin + 40, width - margin - 40, 4):
        if random_gen.random() > 0.3:
            draw.line([(x, barcode_y), (x, barcode_y + 35)], fill=(20, 20, 25), width=2)
    curr_y += 50

    # Footer
    curr_y = draw_centered(f"AUTHENTICATION HASH: {data.ticket_id}-VERIFIED", curr_y)
    curr_y = draw_centered("[PROVENANCE: SYNTHETIC BENCHMARK FIXTURE]", curr_y)

    # Visual Artifacts: Thermal line jitter and noise
    if add_noise:
        # Subtle horizontal thermal line fade
        for _ in range(8):
            fade_y = random_gen.randint(20, height - 20)
            draw.line([(margin, fade_y), (width - margin, fade_y)], fill=(240, 238, 230), width=1)

    # Subtle rotation artifact (±1.5°)
    angle = rotation_angle if rotation_angle is not None else random.uniform(-1.5, 1.5)
    img_rotated = img.rotate(angle, resample=Image.Resampling.BICUBIC, fillcolor=paper_color)

    buffer = io.BytesIO()
    info = PngInfo()
    ocr_payload = (
        f"TICKET NUMBER: {data.ticket_id}\n"
        f"VEHICLE REG NO: {data.vehicle_registration}\n"
        f"MATERIAL CODE: {data.material}\n"
        f"IN-TIME: {data.in_timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"OUT-TIME: {data.out_timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"GROSS WEIGHT: {data.gross_weight_kg:,.1f} KG\n"
        f"TARE WEIGHT: {data.tare_weight_kg:,.1f} KG\n"
        f"NET DISPATCH: {data.net_weight_kg:,.1f} KG\n"
    )
    info.add_text("ocr_text", ocr_payload)
    img_rotated.save(buffer, format="PNG", pnginfo=info)
    return buffer.getvalue()


class ProceduralWeighbridgeGenerator:
    """Orchestrates procedural generation and local storage of synthetic receipts."""

    def __init__(self, output_dir: Path | str = "data/synthetic/weighbridge") -> None:
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_and_save(
        self,
        anomaly_type: WeighbridgeAnomalyType = WeighbridgeAnomalyType.NONE,
        ticket_seed: int | None = None,
    ) -> tuple[WeighbridgeSlipData, Path]:
        """Generates receipt metadata and saves the generated PNG artifact to disk."""
        data = generate_synthetic_receipt_data(anomaly_type=anomaly_type, ticket_seed=ticket_seed)
        png_bytes = render_thermal_receipt_image(data)

        target_file = self.output_dir / f"{data.ticket_id}.png"
        target_file.write_bytes(png_bytes)

        json_file = self.output_dir / f"{data.ticket_id}.json"
        json_file.write_text(data.model_dump_json(indent=2), encoding="utf-8")

        return data, target_file
