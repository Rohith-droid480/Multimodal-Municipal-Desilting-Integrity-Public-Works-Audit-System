# MuniAudit-AI — Architectural Specification & Subsystem Boundaries

**Document Version:** 1.0 (Locked for Hackathon Implementation)  
**Authoritative Reference:** [MuniAudit-AI-Final-Locked-Architecture-v1.0.md](file:///c:/Users/Dilip%20Shekar%20K/Downloads/MUNICIPAL%20AUDIT/MUNICIPAL%20AUDIT/MuniAudit-AI-Final-Locked-Architecture-v1.0.md)  
**System Topology:** Modular Monolith on Amazon ECS Express Mode / Local Docker Compose

---

## 1. Modular Monolith Architecture

MuniAudit-AI executes a multi-stage evidence reconciliation pipeline. The system is intentionally architected as a modular monolith to maximize engineering velocity, preserve strict transactional boundaries, and eliminate distributed-system overhead.

```text
                           ┌───────────────────────────┐
                           │      AUDITOR WEB UI       │
                           │ Evidence Upload / Review  │
                           │ Map / Findings / Report   │
                           └─────────────┬─────────────┘
                                         │ HTTPS / REST
                                         ▼
                      ┌────────────────────────────────────┐
                      │ FASTAPI APPLICATION CONTAINER      │
                      │ (Amazon ECS Express Mode / Docker) │
                      │                                    │
                      │ API / RBAC / Job Orchestration     │
                      │ Evidence Normalization             │
                      └───────┬───────────────┬────────────┘
                              │               │
                 Presigned S3 │               │ SQS Message
                              │               ▼
                              │       ┌─────────────────┐
                              │       │ Amazon SQS       │
                              │       │ Standard + DLQ  │
                              │       └────────┬────────┘
                              │                │
                              ▼                ▼
                    ┌──────────────┐   ┌────────────────┐
                    │ Amazon S3 /  │   │ Audit Worker   │
                    │ Local Store  │   │ Processing     │
                    │ SHA-256 Lock │   │ (Idempotent)   │
                    └──────────────┘   └───────┬────────┘
                                               │
                                               ▼
                                  ┌────────────────────────┐
                                  │ Evidence Fusion Engine │
                                  │ Subjective Logic       │
                                  └────────────┬───────────┘
                                               │
                                               ▼
                                  ┌────────────────────────┐
                                  │ Explainability Engine  │
                                  │ Facts + Evidence Chain │
                                  └────────────┬───────────┘
                                               │
                                               ▼
                                     PostgreSQL 16 Engine
                                      PostGIS + pgvector
```

---

## 2. Layer & Subsystem Boundaries

### Layer A: Presentation (`frontend/` - Beta Owned)
- Forensic investigation workspace: 3-column layout, split-screen evidence inspection, Leaflet GIS viewer, SROIE OCR ticket visualizer.
- Strictly interacts with backend via HTTP REST client. Direct DB/S3 access forbidden.

### Layer B: Application & API (`app/api/`, `app/core/` - Alpha Owned)
- FastAPI routing, Cognito JWT verification, request validation, job creation, and error serialization.
- All heavy analysis is dispatched asynchronously to worker queues; web requests return job handles immediately.

### Layer C: Domain & Invariants (`app/domain/` - Alpha Owned)
- Pure domain models: `Dossier`, `EvidenceItem`, `ProcessingJob`, `Finding`, `AuditReview`.
- Epistemic segregation: `FACT`, `MODEL_OUTPUT`, `RULE_RESULT`, `INFERENCE`, `RECOMMENDATION`.
- Zero dependencies on frameworks, databases, or cloud SDKs.

### Layer D: Analysis & ML Adapters (`app/analysis/` - Beta Owned)
- **Visual:** Meta SSCD (Self-Supervised Copy Detection) 512-d embeddings + pgvector cosine similarity search.
- **Documents:** AWS Textract / PaddleOCR for thermal weighbridge slips (gross, tare, net weight, truck registration, date/time).
- **Geospatial & Temporal:** PostGIS trajectory matching, Haversine velocity rules, drain reach bounding envelopes.
- **Deterministic Rules:** Physical mass balance ($M_{\text{net}} \le V_{\text{bed}} \times 1.90\text{ t/m}^3$), speed ceiling ($v \le 80\text{ km/h}$).
- **Evidence Fusion:** Subjective Logic consensus operator ($\oplus$) calculating Evidence Consistency Score (ECS) and Audit Review Priority Index (ARPI).

### Layer E: Infrastructure Adapters (`app/infrastructure/`, `app/storage/` - Alpha Owned)
- Relational, vector, and spatial storage in PostgreSQL 16 (PostGIS + pgvector).
- Binary evidence storage in Amazon S3 (with local filesystem fallback for Build-It local development).
- Message broker in Amazon SQS (with local in-memory/stub queue for offline execution).

---

## 3. Epistemic Constraints & Administrative Outcomes

The system evaluates dossier claims against empirical data and produces one of four administrative states:
1. `VERIFIED_COMPLIANT`: Evidence independently reconciled with zero material anomalies.
2. `SUBSTANTIVE_INCONSISTENCY`: Concrete physical, temporal, or spatial discrepancy detected.
3. `INCONCLUSIVE_DATA`: Evidence payload is incomplete or degraded; unable to verify.
4. `TECHNICAL_ABSTENTION`: System error, malformed input, or model timeout.

Fraud is never declared by the automated system; the human municipal vigilance officer reviews generated evidence trails.
