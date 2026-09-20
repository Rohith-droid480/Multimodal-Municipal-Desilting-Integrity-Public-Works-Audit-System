import json
import logging
from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

import numpy as np
from fastapi import FastAPI, File, Form, HTTPException, Response, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from app import __version__
from app.core.config import settings
from app.domain.epistemic import (
    AdministrativeState,
    DossierStatus,
    EpistemicCategory,
    EvidenceSourceType,
    FindingSeverity,
    ProvenanceTag,
)
from app.domain.models import AuditReview, Dossier, EvidenceItem, Finding, ProcessingJob
from app.explainability.exporter import export_dossier_json, export_dossier_markdown
from app.explainability.memo import AuditFindingMemorandum, build_finding_memorandum
from app.explainability.triage import ExecutiveTriageDossier, format_executive_triage
from app.explainability.visual_inspection import (
    VisualInspectionPackage,
    build_visual_inspection_package,
)
from app.fusion.engine import ConfidenceTier, FusionResult, PriorityTier, fuse_dossier_evidence
from app.ingestion.gis_parser import MunicipalGISParser
from app.ml.ocr_engine import DocumentOCREngine, ExtractedSlipData
from app.ml.visual_embeddings import VisualEmbeddingExtractor
from app.rules.runner import evaluate_dossier_rules
from app.storage.interface import get_storage_adapter

logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.APP_NAME,
    version=__version__,
    description="Multimodal Municipal Desilting Integrity & Public-Works Audit System API",
)

# Cross-Origin Resource Sharing (CORS) Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage repository for ephemeral local testing and MVP execution
_DOSSIERS_DB: dict[UUID, Dossier] = {}
_FINDINGS_DB: dict[UUID, Finding] = {}
_REVIEWS_DB: dict[UUID, AuditReview] = {}
_JOBS_DB: dict[UUID, ProcessingJob] = {}
_DOSSIER_AUDIT_RESULTS: dict[UUID, FusionResult] = {}
_DOSSIER_TRIAGE: dict[UUID, ExecutiveTriageDossier] = {}
_DOSSIER_PACKAGES: dict[UUID, VisualInspectionPackage] = {}
_DOSSIER_MEMORANDA: dict[UUID, list[AuditFindingMemorandum]] = {}


# Request / Response Schemas
class HealthResponse(BaseModel):
    status: str
    version: str
    environment: str
    timestamp: datetime
    subsystems: dict[str, str]
    invariants: dict[str, Any] = Field(default_factory=dict)


class AuditDossierResponse(BaseModel):
    dossier_id: UUID
    status: DossierStatus
    administrative_state: AdministrativeState
    evidence_consistency_score: float
    audit_review_priority_index: float
    confidence_tier: ConfidenceTier
    priority_tier: PriorityTier
    findings_count: int
    hard_gate_triggered: bool
    audited_at: datetime


class CreateDossierRequest(BaseModel):
    tenant_id: str = "WARD-09-CENTRAL"
    work_order_id: str
    contractor_id: str
    drain_reach_id: str | None = None
    claimed_amount_inr: float = 0.0


class ReviewFindingRequest(BaseModel):
    reviewer_id: str
    auditor_determination: AdministrativeState
    comments: str


@app.get("/health", response_model=HealthResponse, tags=["Diagnostics"])
def health_check():
    """System health check and invariant status."""
    return HealthResponse(
        status="healthy",
        version=__version__,
        environment=settings.APP_ENV,
        timestamp=datetime.now(UTC),
        subsystems={
            "database": "ready",
            "storage": settings.STORAGE_BACKEND,
            "orchestrator": "idle",
        },
        invariants={
            "mass_balance_tolerance_kg": settings.MASS_BALANCE_TOLERANCE_KG,
            "max_silt_density_t_m3": settings.MAX_SILT_DENSITY_T_M3,
            "geodesic_speed_ceiling_kmh": settings.GEODESIC_SPEED_CEILING_KMH,
            "sscd_similarity_threshold": settings.SSCD_SIMILARITY_THRESHOLD,
        },
    )


@app.post(
    "/dossiers", response_model=Dossier, status_code=status.HTTP_201_CREATED, tags=["Dossiers"]
)
def create_dossier(request: CreateDossierRequest):
    """Registers a new contractor public-works billing dossier."""
    dossier = Dossier(
        dossier_id=uuid4(),
        tenant_id=request.tenant_id,
        work_order_id=request.work_order_id,
        contractor_id=request.contractor_id,
        drain_reach_id=request.drain_reach_id,
        claimed_amount_inr=request.claimed_amount_inr,
        status=DossierStatus.CREATED,
    )
    _DOSSIERS_DB[dossier.dossier_id] = dossier
    return dossier


@app.get("/dossiers/{dossier_id}", response_model=Dossier, tags=["Dossiers"])
def get_dossier(dossier_id: UUID):
    """Retrieves a dossier and its submitted evidence items."""
    if dossier_id not in _DOSSIERS_DB:
        raise HTTPException(status_code=404, detail="Dossier not found")
    return _DOSSIERS_DB[dossier_id]


@app.post(
    "/dossiers/{dossier_id}/files",
    response_model=EvidenceItem,
    status_code=status.HTTP_201_CREATED,
    tags=["Evidence"],
)
async def upload_evidence_file(
    dossier_id: UUID,
    file: UploadFile = File(...),
    source_type: EvidenceSourceType = Form(...),
    provenance_tag: ProvenanceTag = Form(ProvenanceTag.SYNTHETIC_DATA),
):
    """Uploads an evidence file to tamper-evident storage and attaches it to the dossier."""
    if dossier_id not in _DOSSIERS_DB:
        raise HTTPException(status_code=404, detail="Dossier not found")

    content = await file.read()
    storage = get_storage_adapter()
    storage_uri, sha256_digest, byte_size = storage.store_artifact(
        dossier_id=str(dossier_id),
        filename=file.filename or "artifact.bin",
        data=content,
    )

    evidence = EvidenceItem(
        evidence_id=uuid4(),
        dossier_id=dossier_id,
        sha256_digest=sha256_digest,
        storage_uri=storage_uri,
        source_type=source_type,
        byte_size=byte_size,
        content_type=file.content_type or "application/octet-stream",
        provenance_tag=provenance_tag,
        metadata={"filename": file.filename},
    )

    dossier = _DOSSIERS_DB[dossier_id]
    dossier.evidence_items.append(evidence)
    dossier.status = DossierStatus.UPLOADING
    return evidence


@app.post("/dossiers/{dossier_id}/finalize", response_model=ProcessingJob, tags=["Dossiers"])
def finalize_dossier(dossier_id: UUID):
    """Finalizes evidence submission and enqueues the asynchronous reconciliation job."""
    if dossier_id not in _DOSSIERS_DB:
        raise HTTPException(status_code=404, detail="Dossier not found")

    dossier = _DOSSIERS_DB[dossier_id]
    dossier.status = DossierStatus.FINALIZING
    dossier.finalized_at = datetime.now(UTC)

    job = ProcessingJob(
        job_id=uuid4(),
        dossier_id=dossier_id,
        status=DossierStatus.QUEUED,
        progress_percent=0,
    )
    _JOBS_DB[job.job_id] = job
    dossier.status = DossierStatus.QUEUED
    return job


@app.get("/dossiers/{dossier_id}/findings", response_model=list[Finding], tags=["Findings"])
def get_dossier_findings(dossier_id: UUID):
    """Retrieves all explainable findings generated for a dossier."""
    if dossier_id not in _DOSSIERS_DB:
        raise HTTPException(status_code=404, detail="Dossier not found")
    return _DOSSIERS_DB[dossier_id].findings


@app.post("/findings/{finding_id}/review", response_model=AuditReview, tags=["Auditor Review"])
def review_finding(finding_id: UUID, request: ReviewFindingRequest):
    """Records an auditor's formal determination and review notes on a specific finding."""
    review = AuditReview(
        review_id=uuid4(),
        finding_id=finding_id,
        reviewer_id=request.reviewer_id,
        auditor_determination=request.auditor_determination,
        comments=request.comments,
    )
    _REVIEWS_DB[review.review_id] = review
    return review


@app.post(
    "/dossiers/{dossier_id}/audit",
    response_model=AuditDossierResponse,
    tags=["Audit Orchestration"],
)
def audit_dossier(dossier_id: UUID):
    """Executes the full end-to-end multimodal audit reconciliation pipeline."""
    if dossier_id not in _DOSSIERS_DB:
        raise HTTPException(status_code=404, detail="Dossier not found")

    dossier = _DOSSIERS_DB[dossier_id]
    storage = get_storage_adapter()
    ocr_engine = DocumentOCREngine()
    visual_engine = VisualEmbeddingExtractor()
    gis_parser = MunicipalGISParser()

    extracted_slips: list[ExtractedSlipData] = []
    duplicate_pairs: list[dict[str, Any]] = []

    # 1. Process Multimodal Evidence Items
    for item in dossier.evidence_items:
        meta = item.metadata
        try:
            raw_bytes = storage.retrieve_artifact(item.storage_uri)
        except (OSError, ValueError, KeyError) as err:
            logger.debug("Failed retrieving artifact %s: %s", item.storage_uri, err)
            raw_bytes = b""

        # A. Weighbridge Thermal Receipt Processing
        if item.source_type == EvidenceSourceType.WEIGHBRIDGE_RECEIPT:
            slip_data: ExtractedSlipData | None = None
            if raw_bytes:
                is_img = raw_bytes.startswith((b"\x89PNG", b"\xff\xd8", b"RIFF", b"BM"))
                if is_img:
                    slip_data = ocr_engine.parse_image(raw_bytes)
                else:
                    slip_data = ocr_engine.parse_text(raw_bytes.decode("utf-8", errors="ignore"))

            if slip_data is not None and slip_data.gross_weight_kg is not None:
                extracted_slips.append(slip_data)
                meta["ocr_confidence"] = slip_data.overall_confidence
                meta["mean_confidence"] = slip_data.overall_confidence
                meta["gross_weight_kg"] = slip_data.gross_weight_kg
                if slip_data.tare_weight_kg is not None:
                    meta["tare_weight_kg"] = slip_data.tare_weight_kg
                if slip_data.net_weight_kg is not None:
                    meta["net_weight_kg"] = slip_data.net_weight_kg
                if slip_data.ticket_id is not None:
                    meta["ticket_id"] = slip_data.ticket_id
                if slip_data.vehicle_registration is not None:
                    meta["vehicle_registration"] = slip_data.vehicle_registration
                if slip_data.out_timestamp is not None:
                    meta["out_timestamp"] = slip_data.out_timestamp
                if slip_data.in_timestamp is not None:
                    meta["in_timestamp"] = slip_data.in_timestamp
                meta.setdefault("tipper_volume_m3", 10.0)

                if slip_data.arithmetic_consistent is False:
                    finding = Finding(
                        finding_id=uuid4(),
                        dossier_id=dossier_id,
                        category="MASS_BALANCE",
                        epistemic_category=EpistemicCategory.RULE_RESULT,
                        severity=FindingSeverity.HIGH,
                        title="Weighbridge Slip Arithmetic Inconsistency",
                        description=(
                            f"Weighbridge slip arithmetic fails mass conservation: Gross ({slip_data.gross_weight_kg} kg) - "
                            f"Tare ({slip_data.tare_weight_kg} kg) != Net ({slip_data.net_weight_kg} kg) with "
                            f"discrepancy {slip_data.mass_discrepancy_kg} kg."
                        ),
                        evidence_refs=[item.sha256_digest],
                        observed_value=f"Discrepancy: {slip_data.mass_discrepancy_kg} kg",
                        expected_value="Gross - Tare = Net (delta <= 20 kg)",
                        rule_reference="R-001-MASS-BALANCE",
                        recommendation="Inspect physical weighbridge ledger and request scale calibration certificate.",
                    )
                    dossier.findings.append(finding)

        # B. Site Photo Visual Feature Extraction
        elif item.source_type == EvidenceSourceType.SITE_PHOTO:
            if raw_bytes and "embedding" not in meta:
                try:
                    emb = visual_engine.extract_from_bytes(raw_bytes)
                    meta["embedding"] = emb
                except (OSError, ValueError, RuntimeError) as err:
                    logger.debug("Visual feature extraction failed for %s: %s", item.evidence_id, err)

        # C. Vehicle Trip Log & GIS Parsing
        elif item.source_type == EvidenceSourceType.TRIP_LOG:
            if raw_bytes:
                try:
                    text_content = raw_bytes.decode("utf-8", errors="ignore")
                    parsed_reach = None
                    if "coordinates" in text_content or "FeatureCollection" in text_content:
                        geojson_res = gis_parser.parse_geojson(text_content)
                        if geojson_res and geojson_res.reaches:
                            meta["gis_reaches_count"] = len(geojson_res.reaches)
                            parsed_reach = geojson_res.reaches[0]
                    elif "<kml" in text_content.lower():
                        kml_res = gis_parser.parse_kml(text_content)
                        if kml_res and kml_res.reaches:
                            meta["gis_reaches_count"] = len(kml_res.reaches)
                            parsed_reach = kml_res.reaches[0]

                    if parsed_reach:
                        meta.setdefault("start_point", (parsed_reach.start_point_lat, parsed_reach.start_point_lng))
                        meta.setdefault("end_point", (parsed_reach.end_point_lat, parsed_reach.end_point_lng))
                        meta.setdefault("start_time", "2026-05-18 18:51:00")
                        meta.setdefault("end_time", "2026-05-18 19:24:00")
                except (OSError, ValueError, KeyError, RuntimeError) as err:
                    logger.debug("GIS parsing failed for %s: %s", item.evidence_id, err)

        # D. Contract Metadata Parsing
        elif item.source_type == EvidenceSourceType.CONTRACT_METADATA:
            if raw_bytes:
                try:
                    parsed_json = json.loads(raw_bytes.decode("utf-8", errors="ignore"))
                    if isinstance(parsed_json, dict):
                        meta.update(parsed_json)
                except (json.JSONDecodeError, UnicodeDecodeError) as err:
                    logger.debug("Contract metadata JSON parse failed for %s: %s", item.evidence_id, err)

    # 2. Pairwise Visual Duplicate Analysis
    photo_items = [
        it for it in dossier.evidence_items
        if it.source_type == EvidenceSourceType.SITE_PHOTO and "embedding" in it.metadata
    ]
    for i in range(len(photo_items)):
        for j in range(i + 1, len(photo_items)):
            p1, p2 = photo_items[i], photo_items[j]
            v1 = np.asarray(p1.metadata["embedding"], dtype=np.float32)
            v2 = np.asarray(p2.metadata["embedding"], dtype=np.float32)
            sim = min(1.0, max(0.0, float(np.dot(v1, v2))))
            p1.metadata["visual_similarity"] = round(sim, 4)
            p2.metadata["visual_similarity"] = round(sim, 4)
            if sim >= settings.SSCD_SIMILARITY_THRESHOLD:
                duplicate_pairs.append(
                    {
                        "claimed_evidence_id": p1.evidence_id,
                        "claimed_sha256": p1.sha256_digest,
                        "matched_evidence_id": p2.evidence_id,
                        "matched_sha256": p2.sha256_digest,
                        "similarity": sim,
                        "similarity_score": sim,
                        "chainage_station": p1.metadata.get("chainage"),
                        "claimed_timestamp": p1.created_at,
                        "matched_timestamp": p2.created_at,
                    }
                )
                dup_finding = Finding(
                    finding_id=uuid4(),
                    dossier_id=dossier_id,
                    category="VISUAL_COPY_DETECTION",
                    epistemic_category=EpistemicCategory.MODEL_OUTPUT,
                    severity=FindingSeverity.CRITICAL,
                    title="Near-Duplicate Photo Submission Detected",
                    description=(
                        f"Photographic evidence exhibits pairwise visual embedding similarity of {sim:.4f}, "
                        f"exceeding the canonical threshold of {settings.SSCD_SIMILARITY_THRESHOLD}."
                    ),
                    evidence_refs=[p1.sha256_digest, p2.sha256_digest],
                    observed_value=f"Similarity: {sim:.4f}",
                    expected_value=f"< {settings.SSCD_SIMILARITY_THRESHOLD}",
                    rule_reference="SSCD-COPY-DETECTION",
                    recommendation="Cross-check photo capture EXIF telematics and conduct physical site verification.",
                )
                dossier.findings.append(dup_finding)

    # 3. Deterministic Rules Evaluation
    rule_results = evaluate_dossier_rules(dossier)
    for res in rule_results:
        if res.status == AdministrativeState.SUBSTANTIVE_INCONSISTENCY and not any(
            f.rule_reference == res.rule_id for f in dossier.findings
        ):
            valid_refs = (
                [item.sha256_digest for item in dossier.evidence_items[:2]]
                if dossier.evidence_items
                else ["0" * 64]
            )
            finding = Finding(
                finding_id=uuid4(),
                dossier_id=dossier_id,
                category=res.rule_id,
                epistemic_category=EpistemicCategory.RULE_RESULT,
                severity=FindingSeverity.CRITICAL,
                title=f"Rule Exception: {res.rule_id}",
                description=res.justification,
                evidence_refs=valid_refs,
                observed_value=str(res.observed_value) if res.observed_value is not None else None,
                expected_value=str(res.expected_value) if res.expected_value is not None else None,
                rule_reference=res.rule_id,
                recommendation="Conduct technical verification of transport telemetry and physical measurement logs.",
            )
            dossier.findings.append(finding)

    # 4. Evidential Fusion Engine
    fusion_result = fuse_dossier_evidence(dossier, rule_results=rule_results)

    # 5. GAGAS Finding Memoranda Assembly
    memoranda: list[AuditFindingMemorandum] = []
    for f in dossier.findings:
        matched_rule = next((r for r in rule_results if r.rule_id in (f.rule_reference or "")), None)
        if isinstance(f.severity, FindingSeverity):
            sev = f.severity
        elif isinstance(f.severity, str) and f.severity in FindingSeverity.__members__:
            sev = FindingSeverity[f.severity]
        else:
            sev = FindingSeverity.HIGH

        clean_hashes = [
            h.lower() for h in f.evidence_refs
            if len(h) == 64 and all(c in "0123456789abcdefABCDEF" for c in h)
        ]
        if not clean_hashes:
            clean_hashes = ["0" * 64]

        memo = build_finding_memorandum(
            dossier_id=dossier.dossier_id,
            title=f.title,
            severity=sev,
            evidence_hashes=clean_hashes,
            rule_result=matched_rule,
        )
        memoranda.append(memo)

    # 6. Executive Triage Compilation
    triage_dossier = format_executive_triage(dossier, fusion_result)

    # 7. Visual Inspection Package Generation
    primary_slip = extracted_slips[0] if extracted_slips else None
    visual_pkg = build_visual_inspection_package(
        dossier=dossier,
        duplicate_pairs=duplicate_pairs if duplicate_pairs else None,
        extracted_slip_data=primary_slip,
    )

    # 8. Persist in memory registries
    _DOSSIER_AUDIT_RESULTS[dossier_id] = fusion_result
    _DOSSIER_TRIAGE[dossier_id] = triage_dossier
    _DOSSIER_PACKAGES[dossier_id] = visual_pkg
    _DOSSIER_MEMORANDA[dossier_id] = memoranda

    # 9. Determine Administrative Classification & Update Dossier Status
    if fusion_result.hard_gate_violation:
        admin_state = AdministrativeState.SUBSTANTIVE_INCONSISTENCY
    elif fusion_result.confidence_tier in (ConfidenceTier.LOW, ConfidenceTier.INSUFFICIENT_DATA):
        admin_state = AdministrativeState.INCONCLUSIVE_DATA
    elif fusion_result.evidence_consistency_score >= 0.70:
        admin_state = AdministrativeState.VERIFIED_COMPLIANT
    else:
        admin_state = AdministrativeState.SUBSTANTIVE_INCONSISTENCY

    dossier.status = DossierStatus.COMPLETED

    return AuditDossierResponse(
        dossier_id=dossier_id,
        status=dossier.status,
        administrative_state=admin_state,
        evidence_consistency_score=fusion_result.evidence_consistency_score,
        audit_review_priority_index=fusion_result.audit_review_priority_index,
        confidence_tier=fusion_result.confidence_tier,
        priority_tier=fusion_result.priority_tier,
        findings_count=len(dossier.findings),
        hard_gate_triggered=fusion_result.hard_gate_violation,
        audited_at=datetime.now(UTC),
    )


@app.get(
    "/dossiers/{dossier_id}/triage",
    response_model=ExecutiveTriageDossier,
    tags=["Explainability"],
)
def get_dossier_triage(dossier_id: UUID):
    """Retrieves the executive triage assessment and operational causal attributions."""
    if dossier_id not in _DOSSIERS_DB:
        raise HTTPException(status_code=404, detail="Dossier not found")
    if dossier_id not in _DOSSIER_TRIAGE:
        raise HTTPException(
            status_code=400,
            detail="Dossier has not been audited yet. Call POST /dossiers/{dossier_id}/audit first.",
        )
    return _DOSSIER_TRIAGE[dossier_id]


@app.get(
    "/dossiers/{dossier_id}/visual-package",
    response_model=VisualInspectionPackage,
    tags=["Explainability"],
)
def get_dossier_visual_package(dossier_id: UUID):
    """Retrieves the visual inspection package with duplicate comparisons and normalized OCR overlays."""
    if dossier_id not in _DOSSIERS_DB:
        raise HTTPException(status_code=404, detail="Dossier not found")
    if dossier_id not in _DOSSIER_PACKAGES:
        raise HTTPException(
            status_code=400,
            detail="Dossier has not been audited yet. Call POST /dossiers/{dossier_id}/audit first.",
        )
    return _DOSSIER_PACKAGES[dossier_id]


@app.get("/dossiers/{dossier_id}/export/json", tags=["Export"])
def get_dossier_export_json(dossier_id: UUID) -> dict[str, Any]:
    """Exports the deterministic JSON forensic audit dossier bundle."""
    if dossier_id not in _DOSSIERS_DB:
        raise HTTPException(status_code=404, detail="Dossier not found")
    if dossier_id not in _DOSSIER_AUDIT_RESULTS:
        raise HTTPException(
            status_code=400,
            detail="Dossier has not been audited yet. Call POST /dossiers/{dossier_id}/audit first.",
        )
    dossier = _DOSSIERS_DB[dossier_id]
    fusion_result = _DOSSIER_AUDIT_RESULTS[dossier_id]
    memoranda = _DOSSIER_MEMORANDA.get(dossier_id, [])
    triage = _DOSSIER_TRIAGE.get(dossier_id)
    return export_dossier_json(dossier, fusion_result, memoranda, triage=triage)


@app.get("/dossiers/{dossier_id}/export/markdown", tags=["Export"])
def get_dossier_export_markdown(dossier_id: UUID) -> Response:
    """Exports the deterministic GAGAS Yellow Book compliant audit workpaper in Markdown format."""
    if dossier_id not in _DOSSIERS_DB:
        raise HTTPException(status_code=404, detail="Dossier not found")
    if dossier_id not in _DOSSIER_AUDIT_RESULTS:
        raise HTTPException(
            status_code=400,
            detail="Dossier has not been audited yet. Call POST /dossiers/{dossier_id}/audit first.",
        )
    dossier = _DOSSIERS_DB[dossier_id]
    fusion_result = _DOSSIER_AUDIT_RESULTS[dossier_id]
    memoranda = _DOSSIER_MEMORANDA.get(dossier_id, [])
    triage = _DOSSIER_TRIAGE.get(dossier_id)
    markdown_content = export_dossier_markdown(dossier, fusion_result, memoranda, triage=triage)
    return Response(content=markdown_content, media_type="text/markdown")

