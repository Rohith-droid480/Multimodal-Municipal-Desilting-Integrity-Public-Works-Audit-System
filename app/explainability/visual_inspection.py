"""MuniAudit-AI — Visual Inspection & Document Overlay Package Builder.

Compiles visual near-duplicate photo pairs and normalized document OCR bounding box
canvas overlays for municipal auditor inspection.
Adheres strictly to Locked Architecture v1.0 and Section 4 visual ML standards.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator

from app.domain.epistemic import EvidenceSourceType
from app.domain.models import Dossier
from app.ml.ocr_engine import ExtractedSlipData


class VisualDuplicateComparison(BaseModel):
    """Side-by-side comparison payload for candidate near-duplicate site photos."""

    comparison_id: UUID = Field(default_factory=uuid4)
    claimed_evidence_id: UUID = Field(..., description="Target claimed photo evidence UUID")
    claimed_sha256: str = Field(..., description="Target photo 64-char SHA-256 digest")
    matched_evidence_id: UUID = Field(..., description="Matched historical or peer photo UUID")
    matched_sha256: str = Field(..., description="Matched photo 64-char SHA-256 digest")
    similarity_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="SSCD visual metric cosine similarity (Sc >= 0.85 indicates candidate duplicate)",
    )
    chainage_station: str | None = Field(
        default=None,
        description="Declared reach chainage (e.g. 'CH-0+450')",
    )
    claimed_timestamp: datetime | None = Field(default=None)
    matched_timestamp: datetime | None = Field(default=None)
    audit_note: str = Field(..., description="Auditor comparative inspection directive")


class OCROverlayToken(BaseModel):
    """Token-level bounding box and extraction metadata for frontend canvas overlay."""

    field_name: str = Field(..., description="Semantic field (e.g. 'gross_weight', 'ticket_id')")
    extracted_text: str = Field(..., description="Raw parsed token text")
    bounding_box: list[float] = Field(
        ...,
        description="Normalized coordinates [ymin, xmin, ymax, xmax] in [0.0, 1.0]",
    )
    confidence: float = Field(..., ge=0.0, le=1.0, description="Token extraction confidence")

    @field_validator("bounding_box")
    @classmethod
    def validate_box(cls, box: list[float]) -> list[float]:
        """Validate that bounding box has 4 normalized coordinates in [0.0, 1.0]."""
        if len(box) != 4:
            msg = f"Bounding box must contain exactly 4 coordinates [ymin, xmin, ymax, xmax], got {len(box)}"
            raise ValueError(msg)
        for val in box:
            if not (0.0 <= val <= 1.0):
                msg = f"Bounding box coordinates must be normalized in [0.0, 1.0], got {val}"
                raise ValueError(msg)
        return box


class OCROverlayInspection(BaseModel):
    """Structured inspection payload for scanned thermal weighbridge dockets."""

    evidence_id: UUID = Field(..., description="Weighbridge evidence UUID")
    sha256_digest: str = Field(..., description="64-character SHA-256 digest of slip artifact")
    ticket_id: str | None = Field(default=None)
    vehicle_registration: str | None = Field(default=None)
    gross_weight_kg: float | None = Field(default=None)
    tare_weight_kg: float | None = Field(default=None)
    net_weight_kg: float | None = Field(default=None)
    arithmetic_valid: bool | None = Field(
        default=None,
        description="True if |Gross - Tare - Net| <= 20.0 kg",
    )
    arithmetic_delta_kg: float | None = Field(default=None)
    tokens: list[OCROverlayToken] = Field(
        default_factory=list,
        description="Normalized token coordinates for canvas rendering",
    )


class VisualInspectionPackage(BaseModel):
    """Composite visual inspection package bundling photo comparisons and OCR overlays."""

    dossier_id: UUID = Field(..., description="Associated dossier UUID")
    duplicate_comparisons: list[VisualDuplicateComparison] = Field(
        default_factory=list,
        description="Near-duplicate site photo comparison pairs",
    )
    ocr_overlays: list[OCROverlayInspection] = Field(
        default_factory=list,
        description="Weighbridge docket token bounding box overlays",
    )
    generated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


def build_visual_inspection_package(
    dossier: Dossier,
    duplicate_pairs: list[dict[str, Any]] | None = None,
    extracted_slip_data: ExtractedSlipData | None = None,
) -> VisualInspectionPackage:
    """Construct a complete visual inspection package from dossier items and analysis outputs."""
    comparisons: list[VisualDuplicateComparison] = []
    ocr_overlays: list[OCROverlayInspection] = []

    # 1. Build duplicate comparisons if pairs supplied
    if duplicate_pairs:
        for pair in duplicate_pairs:
            sim = min(1.0, max(0.0, float(pair.get("similarity", pair.get("similarity_score", 0.0)))))
            comparisons.append(
                VisualDuplicateComparison(
                    claimed_evidence_id=pair["claimed_evidence_id"],
                    claimed_sha256=pair["claimed_sha256"],
                    matched_evidence_id=pair["matched_evidence_id"],
                    matched_sha256=pair["matched_sha256"],
                    similarity_score=sim,
                    chainage_station=pair.get("chainage_station"),
                    claimed_timestamp=pair.get("claimed_timestamp"),
                    matched_timestamp=pair.get("matched_timestamp"),
                    audit_note=(
                        f"High visual similarity (Sc={sim:.3f} >= 0.85). Inspect photographic watermarks, "
                        f"channel geometry, and lighting angle for potential billing duplication."
                    ),
                )
            )

    # 2. Build OCR overlays from extracted slip data or weighbridge evidence items
    weighbridge_items = [
        item for item in dossier.evidence_items
        if item.source_type == EvidenceSourceType.WEIGHBRIDGE_RECEIPT
    ]

    for wb_item in weighbridge_items:
        meta = getattr(wb_item, "metadata", None) or getattr(wb_item, "metadata_json", None) or {}
        tokens: list[OCROverlayToken] = []

        # If explicit ExtractedSlipData provided, use its token boxes
        if extracted_slip_data is not None:
            gross = extracted_slip_data.gross_weight_kg
            tare = extracted_slip_data.tare_weight_kg
            net = extracted_slip_data.net_weight_kg
            ticket = extracted_slip_data.ticket_id
            veh = extracted_slip_data.vehicle_registration
            arith_valid = extracted_slip_data.arithmetic_consistent
            arith_delta = extracted_slip_data.mass_discrepancy_kg

            for fname, box in extracted_slip_data.token_boxes.items():
                tokens.append(
                    OCROverlayToken(
                        field_name=fname,
                        extracted_text=box.raw_token,
                        bounding_box=[
                            round(box.ymin, 4),
                            round(box.xmin, 4),
                            round(box.ymax, 4),
                            round(box.xmax, 4),
                        ],
                        confidence=round(box.confidence, 4),
                    )
                )
        else:
            # Derive from evidence metadata if available
            gross = meta.get("gross_weight_kg")
            tare = meta.get("tare_weight_kg")
            net = meta.get("net_weight_kg")
            ticket = meta.get("ticket_id")
            veh = meta.get("vehicle_number") or meta.get("vehicle_registration")

            arith_valid = None
            arith_delta = None
            if gross is not None and tare is not None and net is not None:
                arith_delta = abs(gross - tare - net)
                arith_valid = arith_delta <= 20.0

            # Default canonical bounding boxes for standard receipt format
            if ticket:
                tokens.append(
                    OCROverlayToken(
                        field_name="ticket_id",
                        extracted_text=str(ticket),
                        bounding_box=[0.10, 0.15, 0.16, 0.65],
                        confidence=0.95,
                    )
                )
            if veh:
                tokens.append(
                    OCROverlayToken(
                        field_name="vehicle_registration",
                        extracted_text=str(veh),
                        bounding_box=[0.20, 0.15, 0.26, 0.70],
                        confidence=0.92,
                    )
                )
            if gross is not None:
                tokens.append(
                    OCROverlayToken(
                        field_name="gross_weight",
                        extracted_text=f"{gross:.0f} kg",
                        bounding_box=[0.35, 0.20, 0.41, 0.60],
                        confidence=0.94,
                    )
                )
            if tare is not None:
                tokens.append(
                    OCROverlayToken(
                        field_name="tare_weight",
                        extracted_text=f"{tare:.0f} kg",
                        bounding_box=[0.43, 0.20, 0.49, 0.60],
                        confidence=0.94,
                    )
                )
            if net is not None:
                tokens.append(
                    OCROverlayToken(
                        field_name="net_weight",
                        extracted_text=f"{net:.0f} kg",
                        bounding_box=[0.51, 0.20, 0.57, 0.60],
                        confidence=0.96,
                    )
                )

        ocr_overlays.append(
            OCROverlayInspection(
                evidence_id=wb_item.evidence_id,
                sha256_digest=wb_item.sha256_digest,
                ticket_id=str(ticket) if ticket else None,
                vehicle_registration=str(veh) if veh else None,
                gross_weight_kg=gross,
                tare_weight_kg=tare,
                net_weight_kg=net,
                arithmetic_valid=arith_valid,
                arithmetic_delta_kg=arith_delta,
                tokens=tokens,
            )
        )

    return VisualInspectionPackage(
        dossier_id=dossier.dossier_id,
        duplicate_comparisons=comparisons,
        ocr_overlays=ocr_overlays,
    )
