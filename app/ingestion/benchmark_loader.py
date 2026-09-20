"""Benchmark Dossier Loader & Fixture Generator for Forensic Evaluation."""

import io
from enum import Enum
from uuid import uuid4

from PIL import Image, ImageDraw

from app.domain.epistemic import (
    DossierStatus,
    EpistemicCategory,
    EvidenceSourceType,
    FindingSeverity,
    ProvenanceTag,
)
from app.domain.models import Dossier, EvidenceItem, Finding
from app.ingestion.synthetic_generator import (
    WeighbridgeAnomalyType,
    generate_synthetic_receipt_data,
    render_thermal_receipt_image,
)
from app.storage.interface import StorageAdapter, get_storage_adapter


class BenchmarkDossierType(str, Enum):
    """Benchmark evaluation categories defined in MuniAudit-AI research."""

    CLEAN_COMPLIANT = "CLEAN_COMPLIANT"
    SUBSTANTIVE_INCONSISTENCY = "SUBSTANTIVE_INCONSISTENCY"
    INCONCLUSIVE_DATA = "INCONCLUSIVE_DATA"


def create_synthetic_site_photo(caption: str = "Pre-Desilting Channel Site Photo") -> bytes:
    """Generates an evidentiary synthetic JPEG/PNG image with watermarks."""
    img = Image.new("RGB", (640, 480), color=(110, 125, 95))
    draw = ImageDraw.Draw(img)

    # Simulated drainage canal channel lines
    draw.polygon([(0, 480), (220, 200), (420, 200), (640, 480)], fill=(75, 85, 65))
    draw.polygon([(220, 200), (320, 100), (360, 100), (420, 200)], fill=(50, 60, 45))

    # Evidence watermark text
    draw.text((20, 20), f"[EVIDENCE] {caption}", fill=(255, 255, 255))
    draw.text((20, 40), "LAT: 12.93524 N  LNG: 77.62448 E", fill=(255, 255, 220))
    draw.text((20, 60), "TIMESTAMP: 2026-05-14 10:15:32 UTC", fill=(255, 255, 220))

    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()


class BenchmarkDossierLoader:
    """Loads and compiles synthetic benchmark evidence dossiers into canonical models."""

    def __init__(self, storage_adapter: StorageAdapter | None = None) -> None:
        self.storage = storage_adapter or get_storage_adapter()

    def build_benchmark_dossier(
        self,
        dossier_type: BenchmarkDossierType,
        work_order_id: str = "WO-2026-BBMP-042",
        contractor_id: str = "CONT-SWD-9021",
        drain_reach_id: str = "REACH-KORAMANGALA-VALLEY-03",
    ) -> Dossier:
        """Constructs an end-to-end dossier fixture with binary artifacts written to storage."""
        dossier_id = uuid4()

        if dossier_type == BenchmarkDossierType.CLEAN_COMPLIANT:
            # 1. Clean weighbridge receipt
            wb_data = generate_synthetic_receipt_data(
                anomaly_type=WeighbridgeAnomalyType.NONE, ticket_seed=42
            )
            wb_img = render_thermal_receipt_image(wb_data)
            wb_uri, wb_hash, wb_size = self.storage.store_artifact(
                str(dossier_id), f"{wb_data.ticket_id}.png", wb_img
            )

            wb_evidence = EvidenceItem(
                evidence_id=uuid4(),
                dossier_id=dossier_id,
                sha256_digest=wb_hash,
                storage_uri=wb_uri,
                source_type=EvidenceSourceType.WEIGHBRIDGE_RECEIPT,
                byte_size=wb_size,
                content_type="image/png",
                provenance_tag=ProvenanceTag.SYNTHETIC_DATA,
                metadata={
                    "ticket_id": wb_data.ticket_id,
                    "gross_weight_kg": wb_data.gross_weight_kg,
                    "tare_weight_kg": wb_data.tare_weight_kg,
                    "net_weight_kg": wb_data.net_weight_kg,
                    "tipper_volume_m3": 10.0,
                    "out_timestamp": wb_data.out_timestamp.isoformat(),
                    "in_timestamp": wb_data.in_timestamp.isoformat(),
                },
            )

            # 2. Clean site photograph
            photo_bytes = create_synthetic_site_photo("Koramangala Valley Bed Desilted")
            photo_uri, photo_hash, photo_size = self.storage.store_artifact(
                str(dossier_id), "site_photo_post.jpg", photo_bytes
            )

            photo_evidence = EvidenceItem(
                evidence_id=uuid4(),
                dossier_id=dossier_id,
                sha256_digest=photo_hash,
                storage_uri=photo_uri,
                source_type=EvidenceSourceType.SITE_PHOTO,
                byte_size=photo_size,
                content_type="image/jpeg",
                provenance_tag=ProvenanceTag.SYNTHETIC_DATA,
            )

            # 3. Clean trip log CSV
            trip_csv = (
                "trip_id,vehicle_reg,origin,destination,start_time,end_time\n"
                f"TRIP-01,{wb_data.vehicle_registration},Koramangala Reach,Mittaganahalli Quarry,10:35,11:45\n"
            ).encode()
            trip_uri, trip_hash, trip_size = self.storage.store_artifact(
                str(dossier_id), "trip_log.csv", trip_csv
            )

            trip_evidence = EvidenceItem(
                evidence_id=uuid4(),
                dossier_id=dossier_id,
                sha256_digest=trip_hash,
                storage_uri=trip_uri,
                source_type=EvidenceSourceType.TRIP_LOG,
                byte_size=trip_size,
                content_type="text/csv",
                provenance_tag=ProvenanceTag.SYNTHETIC_DATA,
                metadata={
                    "start_point": (12.9352, 77.6244),
                    "end_point": (13.0850, 77.6520),
                    "start_time": "2026-05-14T10:35:00",
                    "end_time": "2026-05-14T11:45:00",
                },
            )

            return Dossier(
                dossier_id=dossier_id,
                tenant_id="WARD-09-CENTRAL",
                work_order_id=work_order_id,
                contractor_id=contractor_id,
                drain_reach_id=drain_reach_id,
                claimed_amount_inr=320000.0,
                status=DossierStatus.QUEUED,
                evidence_items=[wb_evidence, photo_evidence, trip_evidence],
                findings=[],
            )

        elif dossier_type == BenchmarkDossierType.SUBSTANTIVE_INCONSISTENCY:
            # Anomalous receipt with impossible haul weight (e.g. 46,500 kg net)
            wb_data = generate_synthetic_receipt_data(
                anomaly_type=WeighbridgeAnomalyType.IMPOSSIBLE_HAUL_WEIGHT, ticket_seed=99
            )
            wb_img = render_thermal_receipt_image(wb_data)
            wb_uri, wb_hash, wb_size = self.storage.store_artifact(
                str(dossier_id), f"{wb_data.ticket_id}_anomalous.png", wb_img
            )

            wb_evidence = EvidenceItem(
                evidence_id=uuid4(),
                dossier_id=dossier_id,
                sha256_digest=wb_hash,
                storage_uri=wb_uri,
                source_type=EvidenceSourceType.WEIGHBRIDGE_RECEIPT,
                byte_size=wb_size,
                content_type="image/png",
                provenance_tag=ProvenanceTag.SYNTHETIC_DATA,
                metadata={
                    "ticket_id": wb_data.ticket_id,
                    "gross_weight_kg": wb_data.gross_weight_kg,
                    "tare_weight_kg": wb_data.tare_weight_kg,
                    "net_weight_kg": wb_data.net_weight_kg,
                    "tipper_volume_m3": 10.0,
                    "out_timestamp": wb_data.out_timestamp.isoformat(),
                    "in_timestamp": wb_data.in_timestamp.isoformat(),
                },
            )

            finding = Finding(
                finding_id=uuid4(),
                dossier_id=dossier_id,
                category="WEIGHBRIDGE",
                epistemic_category=EpistemicCategory.RULE_RESULT,
                severity=FindingSeverity.HIGH,
                title="Vehicle Net Payload Exceeds Axle Maximum",
                description="Reported net silt weight of 46.50 tonnes violates maximum allowable load for registered tipper class.",
                evidence_refs=[wb_hash],
                observed_value="46,500 KG",
                expected_value="<= 16,000 KG",
                rule_reference="REQ-PHYS-002",
                recommendation="Inspect weighbridge calibration certificate and cross-verify with Quarry gate disposal manifest.",
            )

            return Dossier(
                dossier_id=dossier_id,
                tenant_id="WARD-09-CENTRAL",
                work_order_id=work_order_id,
                contractor_id=contractor_id,
                drain_reach_id=drain_reach_id,
                claimed_amount_inr=540000.0,
                status=DossierStatus.COMPLETED,
                evidence_items=[wb_evidence],
                findings=[finding],
            )

        else:  # INCONCLUSIVE_DATA
            # Corrupted / truncated receipt artifact and missing GPS
            corrupted_bytes = b"CORRUPTED_THERMAL_SCAN_BYTES_TRUNCATED"
            uri, sha_hash, size = self.storage.store_artifact(
                str(dossier_id), "unreadable_receipt.bin", corrupted_bytes
            )

            degraded_evidence = EvidenceItem(
                evidence_id=uuid4(),
                dossier_id=dossier_id,
                sha256_digest=sha_hash,
                storage_uri=uri,
                source_type=EvidenceSourceType.WEIGHBRIDGE_RECEIPT,
                byte_size=size,
                content_type="application/octet-stream",
                provenance_tag=ProvenanceTag.SYNTHETIC_DATA,
                metadata={"legibility": "UNREADABLE"},
            )

            inconclusive_finding = Finding(
                finding_id=uuid4(),
                dossier_id=dossier_id,
                category="DOCUMENT_LEGIBILITY",
                epistemic_category=EpistemicCategory.RULE_RESULT,
                severity=FindingSeverity.MEDIUM,
                title="Weighbridge Receipt Illegible",
                description="Uploaded weighbridge ticket cannot be parsed by optical document intelligence due to truncation.",
                evidence_refs=[sha_hash],
                observed_value="Illegible / Truncated byte stream",
                expected_value="Standard 200+ DPI thermal receipt scan",
                rule_reference="REQ-DOC-001",
                recommendation="Request contractor resubmission of original paper weighbridge voucher.",
            )

            return Dossier(
                dossier_id=dossier_id,
                tenant_id="WARD-09-CENTRAL",
                work_order_id=work_order_id,
                contractor_id=contractor_id,
                drain_reach_id=drain_reach_id,
                claimed_amount_inr=150000.0,
                status=DossierStatus.INCONCLUSIVE,
                evidence_items=[degraded_evidence],
                findings=[inconclusive_finding],
            )
