# MuniAudit-AI — Engineering Changelog

All notable changes to the architecture, codebase, and state machine transitions will be documented in this file.

## [Milestone 10_SYSTEM_INTEGRATION_E2E] - 2026-09-20

### Added
- **Full Multimodal Pipeline Orchestration Endpoint (`POST /dossiers/{id}/audit` in `app/api/main.py`):**
  - Sequentially ingests and processes all evidence channels: Document OCR extraction (`DocumentOCREngine`), pairwise visual embedding deduplication (`VisualEmbeddingExtractor`), vehicle track transit analysis (`MunicipalGISParser`), and civil engineering rule evaluations (`evaluate_dossier_rules`).
  - Executes Two-Tier Evidential Fusion (`fuse_dossier_evidence`), generating the Evidence Consistency Score (ECS), Audit Review Priority Index (ARPI), epistemic confidence tier, and leave-one-out (LOO) marginal attributions.
  - Generates GAGAS finding memoranda, executive triage narratives, and visual inspection packages.
  - Updates dossier state machine atomically (`VERIFIED_COMPLIANT`, `SUBSTANTIVE_INCONSISTENCY`, or `INCONCLUSIVE_DATA`).
- **Forensic Inspection & Triage Endpoints (`app/api/main.py`):**
  - `GET /dossiers/{id}/triage`: Retrieves operational triage dossier with civil engineering narratives and LOO modality attributions.
  - `GET /dossiers/{id}/visual-package`: Retrieves bounding box overlays and near-duplicate photo comparison pairs ($S_C \ge 0.85$).
- **Forensic Export Endpoints (`app/api/main.py`):**
  - `GET /dossiers/{id}/export/json`: Deterministic JSON audit workpaper bundle with SHA-256 evidence digests.
  - `GET /dossiers/{id}/export/markdown`: GAGAS Yellow Book compliant markdown audit workpaper with auditor adjudication block.
- **End-to-End Multimodal Integration Test Suite (`tests/test_e2e_pipeline.py`):**
  - 6 exhaustive end-to-end integration tests verifying compliant dossier lifecycle, adversarial arithmetic tampering, photographic duplicate fraud attempt, unobserved telemetry channel safe failure, audit idempotency, and error handling.
  - Total test suite expanded to **97 passing tests with 87% coverage**.

### Fixed
- **Cosine Similarity Float Precision (`app/explainability/visual_inspection.py` & `app/api/main.py`):** Clamped floating-point dot product results to $[0.0, 1.0]$ (`min(1.0, max(0.0, ...))`) to prevent Pydantic float validation errors from floating-point overshoots.
- **Timezone Standardization in Monotonic Temporal Validation (`app/rules/temporal_sequence.py`):** Standardized parsed string datetimes to timezone-aware UTC datetimes to prevent `TypeError` when comparing naive and aware datetimes.

---

## [Milestone 09_EXPLAINABILITY_REPORTS] - 2026-09-20

### Added
- **Audit Finding Memorandum Builder (`app/explainability/memo.py`):** Structured GAGAS Yellow Book finding memorandum compiler with 5-element format (Criteria, Condition, Cause Hypothesis, Effect, Recommendation), strict 5-tier epistemic breakdown (`FACT`, `MODEL_OUTPUT`, `RULE_RESULT`, `INFERENCE`, `RECOMMENDATION`), pinned 64-char SHA-256 evidence digests, and deterministic lexical filtering programmatically blocking legal conclusion terms ("fraud", "fraudulent", "embezzlement", "bribe", "criminal intent", "guilt").
- **Executive Triage Narrative & Attribution Formatter (`app/explainability/triage.py`):** Translates mathematical Leave-One-Out (LOO) marginal attributions into municipal civil engineering operational language (Running Account Bill, Chainage Stationing, Measurement Book, Lead Chart, Tare/Gross/Net, Disposal Geofence) and provides non-punitive technical data gap explanations for unobserved telemetry channels.
- **Visual Inspection Package & Canvas Overlays (`app/explainability/visual_inspection.py`):** Compiles visual near-duplicate photo comparison pairs ($S_C \ge 0.85$) with timestamps, chainage locations, and image SHA-256 digests. Normalizes token bounding boxes `[ymin, xmin, ymax, xmax]` in $[0.0, 1.0]$ for frontend canvas rendering.
- **Deterministic Dossier Exporter (`app/explainability/exporter.py`):** Serializes complete forensic audit bundles to standard JSON and generates offline-filing ready Markdown audit workpapers complete with GAGAS finding sections, cryptographic chain of custody, and human auditor adjudication/sign-off blocks.
- **Explainability Test Suite (`tests/test_explainability.py`):** 12 unit and integration tests validating lexical filtering, GAGAS 5-element integrity, SHA-256 hash validation, executive triage narratives, normalized bounding box overlays, and JSON/Markdown export generation. Total test suite expanded to **91 passing tests with 86% coverage**.

---

## [Milestone 08_EVIDENCE_FUSION] - 2026-09-20

### Added
- **Subjective Logic Mathematical Operations (`app/fusion/subjective_logic.py`):** Binomial Subjective Logic opinion model ($\omega = (b, d, u, a)$) with strict normalization ($b + d + u = 1.0$), expected value projection ($E = b + a \cdot u$), commutative/associative Jøsang consensus operator ($\oplus$), and vacuous opinion neutral identity.
- **Evidential Modality Mappers (`app/fusion/mappers.py`):** Multi-channel opinion mapping functions for visual duplicate similarity ($S_C \ge 0.85$), OCR token extraction confidence and arithmetic errors, geospatial transit velocities relative to urban ceiling ($80\text{ km/h}$), silt saturation density ($1.90\text{ t/m}^3$), and lifecycle temporal chronology.
- **Two-Tier Evidential Fusion Engine (`app/fusion/engine.py`):**
  - **Tier 1 Hard Gates:** Incontrovertible metrological violations immediately halt to `CRITICAL` triage priority (ARPI: 100.0, ECS $\le 0.10$).
  - **Tier 2 Soft Evidential Fusion:** Subjective Logic opinion consensus across heterogeneous signals yielding the **Evidence Consistency Score (ECS)** $\in [0.0, 1.0]$.
  - **Audit Review Priority Index (ARPI):** Continuous 0–100 triage metric scaled by claimed financial exposure and categorized into `LOW`, `MEDIUM`, `HIGH`, and `CRITICAL` priority tiers.
  - **Epistemic Confidence Tiers:** Uncertainty-driven categorization (`VERY_HIGH`, `HIGH`, `MODERATE`, `LOW`, `INSUFFICIENT_DATA`).
  - **Leave-One-Out (LOO) Modality Attributions:** Marginal attribution vector decomposing composite inconsistency across input channels.
  - **Missing Modality Semantics:** Enforces non-punitive handling where unobserved telemetry channels emit neutral vacuous opinions, increasing uncertainty without creating false accusations.
- **Evidence Fusion Test Suite (`tests/test_evidence_fusion.py`):** 23 unit and integration tests verifying opinion normalization, consensus commutativity/associativity, Zadeh's paradox resilience, Tier 1 hard gate triggering, Tier 2 benchmark dossier reconciliation, missing modality safe failures, and LOO attributions. Total test suite expanded to **79 passing tests with 86% coverage**.

---

## [Milestone 07_DETERMINISTIC_RULES] - 2026-09-20

### Added
- **Base Rule Framework (`app/rules/base.py`):** Pure Pydantic `RuleEvaluationResult` contract and `DeterministicRule` abstract interface with strict `EpistemicCategory.RULE_RESULT` tagging.
- **Weighbridge Mass Balance Rule (`app/rules/mass_balance.py`):** Deterministic verification of $|\text{Gross} - \text{Tare} - \text{Net}| \le 20.0 \text{ kg}$ and physical tare validation ($\text{Gross} > \text{Tare}$).
- **Geospatial Transit Velocity Rule (`app/rules/geospatial_reach.py`):** Great-circle WGS-84 geodesic transit velocity validation enforcing the urban municipal tipper speed ceiling ($V_{\text{max}} = 80.0 \text{ km/h}$) and time-travel impossibility detection.
- **Physical Silt Density Rule (`app/rules/physical_capacity.py`):** Silt mass-to-volume reconciliation enforcing maximum wet desilted sludge saturation density ($\rho_{\text{max}} = 1.90 \text{ t/m}^3$).
- **Temporal Sequence Rule (`app/rules/temporal_sequence.py`):** Monotonic chronological lifecycle validation (Contract Award $\le$ Work Order $\le$ Work Execution $\le$ Weighbridge $\le$ Invoice Submission).
- **Rule Runner Orchestrator (`app/rules/runner.py`):** Unified resilient evaluation function (`evaluate_dossier_rules`) running the full civil engineering rules suite across dossiers with `TECHNICAL_ABSTENTION` fault-isolation.
- **Deterministic Rules Test Suite (`tests/test_deterministic_rules.py`):** 18 automated unit and boundary tests covering nominal, boundary, physical violation, and missing-data safe failures (total test suite expanded to 56 passing tests with 84% coverage).

---

## [Milestone 06_CORE_ML] - 2026-09-20

### Added
- **Visual Metric Embedding & Deduplication Engine (`app/ml/visual_embeddings.py`):** CPU-executable 512-dimensional spatial color moment and gradient feature descriptor extractor with strict L2-normalization ($\Vert v \Vert_2 = 1.0$), batch cosine similarity computation, and candidate duplicate detection ($S_C \ge 0.85$).
- **Document OCR & Slip Extraction Engine (`app/ml/ocr_engine.py`):** Structured thermal weighbridge receipt parser extracting vehicle registration numbers, ticket IDs, gross/tare/net weights, and timestamps. Captures token-level bounding boxes and extraction confidences.
- **Safe Failure & Mass Balance Verification:** Enforces safe failure on degraded/blank inputs (`INCONCLUSIVE_DATA`, no defaulting to 0 kg) and validates civil engineering mass balance identity ($\vert \text{Gross} - \text{Tare} - \text{Net} \vert \le 20.0 \text{ kg}$).
- **Epistemic Invariant Enforced:** All visual embeddings and OCR extracted payloads strictly tagged as `EpistemicCategory.MODEL_OUTPUT`.
- **Core ML Test Suites:** Added `tests/test_visual_ml.py` and `tests/test_ocr_engine.py` (total test suite expanded to 38 passing tests with 83% coverage).

---

## [Milestone 05_DATA_PIPELINE] - 2026-09-20

### Added
- **Directory Hierarchy:** Initialized complete 22-folder immutable dataset hierarchy under `data/raw/`, `data/reference/`, `data/processed/`, `data/synthetic/`, and `data/benchmark/`.
- **Dataset Manifest Engine (`app/ingestion/manifest.py`):** Cryptographic SHA-256 asset registration, JSON manifest compilation, CSV provenance tracking, and tamper detection auditing.
- **Municipal GIS & KML Parser (`app/ingestion/gis_parser.py`):** KML XML and GeoJSON reach parser computing WGS-84 geodesic stationing (Haversine chainage), BBMP municipal jurisdiction bounding checks, and safe failover on malformed data.
- **Procedural Weighbridge Generator (`app/ingestion/synthetic_generator.py`):** Procedural thermal weighbridge slip generator creating JSON metadata and realistic thermal receipt PNG images with dot-matrix rendering, barcode lines, thermal line fades, and controlled anomaly injection (`TARE_EXCEEDS_GROSS`, `IMPOSSIBLE_HAUL_WEIGHT`, `TIMESTAMP_REVERSAL`, `ARITHMETIC_MISMATCH`).
- **Benchmark Dossier Loader (`app/ingestion/benchmark_loader.py`):** Automated fixture compiler creating `CLEAN_COMPLIANT`, `SUBSTANTIVE_INCONSISTENCY`, and `INCONCLUSIVE_DATA` dossiers linked to `LocalStorageAdapter`.
- **Automated Ingestion Test Suites:** Added `tests/test_gis_parser.py`, `tests/test_synthetic_generator.py`, and `tests/test_benchmark_loader.py` (total 26 passing tests).

---

## [Milestone 04_SCAFFOLDING_READY] - 2026-09-20

### Added
- **Project Brain Architecture:** Initialized `CORE_CONTEXT.md`, `PROJECT_STATE.json`, `ARCHITECTURE.md`, `TASK_CONTRACT.md`, `FAILED_APPROACHES.md`, `DEPENDENCY_GRAPH.json`, `CHANGELOG.md`, `DESIGN.md`, `AGENT_RESPONSE_CONTRACT.md`, and `AGENT_ESCALATION.md`.
- **Project Configuration:** Added `pyproject.toml`, `requirements.txt`, `.env.example`, `docker-compose.yml`, and `Dockerfile`.
- **Canonical Domain Models:** Created Pydantic v2 schemas in `app/domain/models.py` and epistemic category definitions in `app/domain/epistemic.py`.
- **FastAPI Application Boundary:** Created `app/api/main.py` with `/health` and core REST routing.
- **Storage Layer:** Created `app/storage/interface.py` with local filesystem storage and SHA-256 tamper-evident integrity checks.
- **Database & Migrations:** Created SQLAlchemy 2.0 ORM models in `app/infrastructure/db/models.py` and configured Alembic in `alembic.ini` and `migrations/`.
- **Automated Verification:** Added unit and integration tests under `tests/`.

---

## [Milestone 03_ARCHITECTURE_LOCKED] - 2026-09-19
### Established
- Locked architecture specification `MuniAudit-AI-Final-Locked-Architecture-v1.0.md`.
- Research documentation under `docs/research/`.
- Engineering governance rules under `.agents/rules/`.
