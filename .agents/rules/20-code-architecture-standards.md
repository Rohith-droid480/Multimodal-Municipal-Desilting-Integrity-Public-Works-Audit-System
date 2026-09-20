---
trigger: always-on
description: MuniAudit-AI code architecture, engineering standards, dependency boundaries, and implementation discipline.
---

# MuniAudit-AI — Code Architecture & Coding Standards

## 0. Mission

You are the coding agent for MuniAudit-AI.

Build a production-quality prototype using disciplined software engineering. The project is a multimodal municipal public-works evidence-reconciliation system. It combines visual forensics, document extraction, geospatial/temporal validation, deterministic rules, anomaly analysis, evidence fusion, explainability, and a human reviewer interface.

You are not permitted to turn the codebase into a generic AI application.

The repository must remain:
- understandable by a human engineer
- testable
- modular
- deterministic where appropriate
- reproducible
- observable
- secure
- easy to extend after the hackathon

---

# 1. Authoritative architecture

The architecture is a MODULAR MONOLITH with explicit domain boundaries.

High-level flow:

```text
UI
  ↓
API / Application Services
  ↓
Canonical Domain Schemas
  ↓
┌───────────────┬────────────────┬─────────────────────┐
│ Visual ML     │ Document ML    │ Geospatial/Temporal │
│ SSCD          │ Textract/OCR   │ PostGIS + rules     │
└───────────────┴────────────────┴─────────────────────┘
  ↓
Deterministic Validation
  ↓
Nominal Anomaly Analysis
  ↓
Evidence Fusion
  ↓
Explainable Findings
  ↓
Human Review
  ↓
Report / Export
```

The implementation must preserve this separation.

Do not reorganize the system into microservices merely to make the architecture look sophisticated.

---

# 2. Layer model

Use these logical layers.

## Layer A — Presentation

Frontend/UI only.

Responsibilities:
- rendering
- user interaction
- local UI state
- API calls through a client/service boundary
- visualization

Forbidden:
- direct database access
- direct filesystem access
- business-rule implementation
- ML inference
- direct AWS SDK calls unless an explicit frontend adapter is approved

## Layer B — API / Application

Responsibilities:
- authentication context
- request parsing
- orchestration
- command/query handlers
- response serialization
- job creation
- error translation

Forbidden:
- embedding ML implementation
- handwritten SQL scattered through route handlers
- UI logic
- duplicated domain rules

## Layer C — Domain / Business Rules

Responsibilities:
- canonical entities
- validation rules
- domain invariants
- findings
- evidence semantics
- status transitions

This layer should prefer pure functions and deterministic logic.

It should not depend on FastAPI, AWS SDKs, browser code, or UI libraries.

## Layer D — Analysis / ML

Responsibilities:
- SSCD inference
- OCR adapters
- anomaly scoring
- feature extraction
- model-specific preprocessing/postprocessing

ML code must return structured domain-compatible results.

ML code must not:
- directly modify unrelated database records
- make legal/criminal conclusions
- bypass domain validation

## Layer E — Infrastructure

Responsibilities:
- PostgreSQL/PostGIS/pgvector
- S3
- SQS
- Cognito integration
- Textract
- Bedrock
- external clients
- filesystem adapters
- logging/telemetry

Infrastructure implementations are adapters around stable interfaces.

## Layer F — Workers / Jobs

Responsibilities:
- asynchronous dossier processing
- retry handling
- orchestration of analysis components
- persistence of job state/results

Workers must be idempotent.

---

# 3. Dependency direction

Dependencies should flow inward:

```text
Presentation
    ↓
Application
    ↓
Domain
    ↑
Analysis adapters
    ↑
Infrastructure
```

Practical rule:

- domain code must not import infrastructure
- UI must not import database models
- routes should call application services
- application services should call domain logic and infrastructure interfaces
- infrastructure adapters implement interfaces required by the application/domain
- analysis modules should be independently testable without a database

If a proposed import violates this direction, stop and explain why before proceeding.

---

# 4. Repository structure

Use a clear structure similar to:

```text
muniaudit-ai/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── application/
│   │   ├── domain/
│   │   ├── analysis/
│   │   │   ├── visual/
│   │   │   ├── documents/
│   │   │   ├── anomaly/
│   │   │   └── fusion/
│   │   ├── infrastructure/
│   │   │   ├── db/
│   │   │   ├── storage/
│   │   │   ├── queues/
│   │   │   └── aws/
│   │   ├── workers/
│   │   └── main.py
│   ├── tests/
│   ├── migrations/
│   └── pyproject.toml
│
├── frontend/
│   ├── app/
│   ├── components/
│   ├── features/
│   ├── lib/
│   ├── hooks/
│   ├── types/
│   └── tests/
│
├── data/
├── models/
├── scripts/
├── docs/
├── .agents/
└── docker-compose.yml
```

If the existing repository uses another structure, inspect it first. Do not move files solely to match this example.

---

# 5. Python coding standards

Use the repository's pinned Python version.

Prefer:
- type annotations
- small functions
- explicit return types for public functions
- immutable/value-like domain objects where appropriate
- Pydantic models for API/domain data where already adopted
- `pathlib` rather than string path manipulation
- structured logging
- explicit exceptions

Avoid:
- wildcard imports
- mutable global configuration
- hidden singleton state
- giant functions
- giant modules
- broad `except Exception` without a recovery strategy
- magic constants
- duplicated parsing logic
- untyped public interfaces
- unused compatibility wrappers

A function should have one clear reason to change.

Do not optimize code before correctness and profiling evidence justify it.

---

# 6. FastAPI standards

FastAPI routers should be thin.

Preferred:

```text
router
  → application service
  → domain logic
  → repository/adapter
```

Avoid:

```text
router
  → 150 lines of business logic + SQL + ML
```

Use separate `APIRouter`s for bounded API areas. FastAPI officially documents multi-file applications and `APIRouter` as the standard mechanism for organizing larger APIs. citeturn246312search4

API contracts must use explicit schemas.

For every endpoint define:
- request model
- response model
- expected status codes
- validation errors
- authentication requirement
- authorization rule
- idempotency behavior where relevant

Do not silently change a response schema.

---

# 7. Database standards

Use PostgreSQL as the primary system of record, with PostGIS and pgvector where approved by the locked architecture.

Rules:
- no raw SQL scattered across route handlers
- centralize persistence operations
- use transactions deliberately
- define constraints in the database where integrity matters
- use migrations for schema evolution
- never modify an already-applied migration in place
- use indexes based on query needs
- preserve provenance fields
- preserve timestamps
- preserve evidence hashes

Keep database models separate from API response schemas.

Do not expose ORM entities directly through the public API.

---

# 8. ML standards

All ML components must have an explicit contract:

```text
Input schema
→ preprocessing
→ model inference
→ postprocessing
→ structured result
→ confidence / uncertainty
```

For every model record:
- model name
- model version
- weights/version identifier
- preprocessing version
- output schema

Never hard-code benchmark results.

Never train a model merely to make the project look more advanced.

ML output is evidence or an analytical signal; it is not automatically a legal conclusion.

---

# 9. MuniAudit forensic semantics

The code must distinguish:

```text
FACT
MODEL_OUTPUT
RULE_RESULT
INFERENCE
RECOMMENDATION
```

Example:

```text
FACT:
Receipt net weight = 12,400 kg

RULE_RESULT:
Gross - Tare = 12,320 kg

INFERENCE:
Weight fields are internally inconsistent

RECOMMENDATION:
Human review of original ticket
```

Never turn this into:

```text
FRAUD = TRUE
```

Missing information means:
- UNKNOWN
- INCONCLUSIVE
- TECHNICAL_ABSTENTION

not wrongdoing.

---

# 10. Visual forensics standards

The approved pipeline is:

```text
image
→ SSCD embedding
→ pgvector retrieval
→ candidate verification
→ SIFT/RANSAC where required
→ structured visual finding
```

Do not make perceptual hash a mandatory gate for transformed-image detection.

Do not replace the approved model simply because another model is fashionable.

If an alternative is proposed:
- benchmark it
- compare false positives/negatives
- record an ADR
- obtain approval before replacing the locked method

---

# 11. OCR/document standards

Normalize every OCR backend into one canonical schema.

Example:

```text
OCR engine
→ adapter
→ ReceiptData
```

The application must not care whether the data came from Textract or a local OCR fallback.

Critical numeric fields must never be silently guessed.

Low confidence should produce:
- explicit uncertainty
- manual review
- or an inconclusive state

---

# 12. Geospatial/rules standards

Geospatial calculations belong in dedicated modules.

Do not mix:
- coordinate parsing
- database queries
- UI formatting
- audit prose

inside one function.

Separate:
- spatial facts
- physical invariants
- contractual rules
- empirical anomaly signals

Do not turn an empirical threshold into a "law" without an authoritative basis.

All operational thresholds must be configurable and documented.

---

# 13. Evidence and provenance standards

Every evidence item needs stable identity and provenance.

At minimum preserve:

```text
evidence_id
dossier_id
source_type
storage_location
sha256
created_at
processing_status
processor_version
```

Derived artifacts must reference their source evidence.

A finding must be traceable back to its source artifact.

Never destroy the original evidence when generating a processed copy.

---

# 14. Configuration standards

Do not hard-code environment-specific values.

Use:
- environment variables
- typed settings
- versioned configuration
- explicit defaults

Keep domain thresholds in configuration rather than burying them inside algorithms.

Every sensitive assumption must have a clear name and documentation.

---

# 15. Error-handling standards

Errors must be classified.

Use categories such as:

```text
VALIDATION_ERROR
NOT_FOUND
AUTHORIZATION_ERROR
DEPENDENCY_ERROR
PROCESSING_ERROR
MODEL_ERROR
DATA_QUALITY_ERROR
TECHNICAL_ABSTENTION
```

Do not:
- swallow exceptions
- return HTTP 200 for failed processing
- convert timeouts into successful findings
- hide upstream dependency failure

Log enough information to reproduce the error without exposing secrets or sensitive data.

---

# 16. Logging

Use structured logs.

Include:
- timestamp
- request/job ID
- dossier ID where appropriate
- component
- event
- status
- duration
- error type

Do not log:
- passwords
- access tokens
- secret keys
- complete sensitive evidence payloads
- unnecessary personal data

---

# 17. Async job standards

Every asynchronous job must have:

```text
job_id
dossier_id
state
attempt
created_at
started_at
completed_at
error_code
result_reference
processor_version
```

Required job states:

```text
QUEUED
PROCESSING
COMPLETED
INCONCLUSIVE
RETRYING
FAILED
TECHNICAL_ABSTENTION
```

A worker must be safe to retry.

Use idempotency keys or unique database constraints where needed.

---

# 18. Frontend architecture standards

The frontend must communicate with APIs through a typed client boundary.

Do not:
- put business rules inside React components
- duplicate API types manually in many files
- put complex data transformations in JSX
- create huge page components
- make one component responsible for fetching, transforming, rendering, and mutation

Prefer:

```text
page
→ feature container
→ presentational components
→ typed API/query layer
```

The existing MuniAudit UI design system is authoritative. Read `DESIGN.md` before frontend work.

---

# 19. UI state standards

Every async operation must have explicit states:

```text
IDLE
LOADING
PROCESSING
READY
PARTIAL
INCONCLUSIVE
ERROR
RETRYING
REVIEW_REQUIRED
```

Do not let a failed API call render as a plausible success state.

Do not fabricate metrics while backend processing is incomplete.

---

# 20. Testing-friendly design

Write code so that:
- domain rules are unit-testable
- infrastructure can be mocked through interfaces
- ML components can run against fixtures
- API contracts can be tested without real cloud dependencies
- end-to-end flows have controlled fixtures

Avoid tightly coupling every test to live AWS services.

Use real AWS integration tests selectively.

---

# 21. Dependency management

Before adding a dependency:

1. confirm the package exists
2. confirm compatibility with the pinned runtime
3. inspect license
4. inspect maintenance/security posture
5. check whether an existing dependency already solves the problem
6. update the correct lockfile
7. run the relevant test suite

Do not install packages speculatively.

Do not add an entire UI library for one missing icon/component.

---

# 22. Documentation standards

Update documentation when behavior or interface changes.

Required documentation for important changes:
- purpose
- interface
- assumptions
- examples
- validation
- known limitations

Do not write documentation that claims capabilities the code does not implement.

---

# 23. Refactoring standard

Do not refactor unrelated code during a feature task.

Refactor when:
- duplication is demonstrated
- a module has an objectively unclear responsibility
- tests expose architectural coupling
- a public interface requires correction

Before a broad refactor:
- explain why
- list affected modules
- identify tests
- estimate risk
- get approval for HIGH/CRITICAL changes

---

# 24. Implementation workflow

For every task:

```text
READ STATE
→ READ SPEC
→ INSPECT CODE
→ IDENTIFY DEPENDENCIES
→ WRITE TASK CONTRACT
→ PLAN MINIMAL CHANGE
→ IMPLEMENT
→ RUN TARGETED TESTS
→ RUN STATIC CHECKS
→ INSPECT DIFF
→ RUN REGRESSION TESTS
→ UPDATE STATE
→ REPORT
```

Never skip the inspection stage.

---

# 25. What "good code" means here

Good code is:

- boring where it should be boring
- explicit
- testable
- understandable
- observable
- deterministic where possible
- replaceable through interfaces
- secure
- easy for another teammate to debug

Do not optimize for:
- cleverness
- maximum abstraction
- maximum framework usage
- shortest code
- number of packages
- number of AWS services

Optimize for system correctness and maintainability.
