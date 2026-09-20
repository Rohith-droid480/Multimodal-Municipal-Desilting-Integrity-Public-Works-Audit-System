# MuniAudit-AI — Task Contract

## Task Metadata
- **TASK_ID:** ALPHA-10-SYSTEM-INTEGRATION-E2E
- **PHASE:** `09_EXPLAINABILITY_REPORTS → 10_SYSTEM_INTEGRATION_E2E`
- **AUTHOR:** ALPHA Engineering Agent
- **DATE:** 2026-09-20

## Objective
Implement end-to-end multimodal pipeline orchestration in `app/api/main.py` including `POST /dossiers/{id}/audit`, triage inspection endpoints (`GET /dossiers/{id}/triage`), visual inspection endpoints (`GET /dossiers/{id}/visual-package`), and forensic export endpoints (`GET /dossiers/{id}/export/json`, `GET /dossiers/{id}/export/markdown`), validated by comprehensive end-to-end tests in `tests/test_e2e_pipeline.py`.

## Why
Delivers a fully functional, end-to-end integrated audit system that connects evidence ingestion, document OCR, visual embedding copy detection, civil engineering deterministic rules, Subjective Logic evidential fusion, GAGAS finding memoranda, and forensic report generation under Locked Architecture v1.0.

## Governing Spec
- `MuniAudit-AI-Final-Locked-Architecture-v1.0.md`
- `docs/research/MuniAudit System Architecture Design.md`
- `.agents/rules/00-muniaudit-core.md`
- `.agents/rules/21-testing-validation.md`

## Files Allowed To Modify / Create
- `app/api/main.py`
- `tests/test_e2e_pipeline.py`
- `PROJECT_STATE.json`, `TASK_CONTRACT.md`, `CHANGELOG.md`, `DEPENDENCY_GRAPH.json`

## Files Explicitly Forbidden
- `frontend/**` (Beta-owned)
- `CORE_CONTEXT.md` (Read-only project context)
- `migrations/versions/001_initial_schema.py` (Baseline locked)

## Acceptance Criteria
- [ ] `POST /dossiers/{id}/audit` orchestrates evidence extraction, deterministic rules, Subjective Logic fusion, and finding memo generation.
- [ ] `GET /dossiers/{id}/triage` serves `ExecutiveTriageDossier` with LOO operational attributions and technical data gap notices.
- [ ] `GET /dossiers/{id}/visual-package` serves `VisualInspectionPackage` with normalized $[0.0, 1.0]$ bounding boxes and near-duplicate comparisons.
- [ ] `GET /dossiers/{id}/export/json` and `GET /dossiers/{id}/export/markdown` serve deterministic offline-filing audit workpapers.
- [ ] Full lifecycle tests in `tests/test_e2e_pipeline.py` covering compliant, adversarial, missing data, and idempotent scenarios.
- [ ] 100% passing Pytest suite with zero test gaming.
- [ ] Ruff and Mypy pass with zero errors across all source files.
