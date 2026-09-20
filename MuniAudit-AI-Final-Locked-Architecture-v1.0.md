# MuniAudit-AI — Final Locked Architecture v1.0

**Project:** MuniAudit-AI  
**Purpose:** Multimodal Municipal Evidence Reconciliation & Public-Works Audit Platform  
**Primary Use Case:** Storm-water-drain desilting / municipal public-works billing evidence verification  
**Architecture Status:** LOCKED FOR HACKATHON IMPLEMENTATION  
**Target:** WeMakeDevs Bharat Builds Tour 2026 — Ship It as primary deployment, Build It parity as fallback/local development  
**Team Assumption:** 1–4 student developers  
**Hackathon Assumption:** approximately 3–4 days

---

## 0. Executive Architecture Decision

MuniAudit-AI is a **human-in-the-loop evidentiary verification system**, not an automated fraud classifier.

The system ingests heterogeneous contractor evidence:

- site photographs
- weighbridge receipts
- invoices / measurement records
- vehicle and trip records
- GPS/location evidence
- municipal drain geometry

and performs:

1. **Evidence integrity and normalization**
2. **Visual instance-level copy detection**
3. **Document extraction and validation**
4. **Geospatial and temporal consistency checks**
5. **Deterministic physical / contractual validation**
6. **Nominal-data anomaly analysis**
7. **Uncertainty-aware evidence fusion**
8. **Explainable finding generation**
9. **Human auditor review**
10. **Evidence-backed audit dossier export**

### Core principle

> **Do not decide whether a contractor is guilty. Determine whether the submitted evidence is internally consistent, identify objective exceptions, and prioritize what a human auditor should review.**

This follows the strongest common conclusion across the research set: facts, model outputs, deterministic rule results, statistical inference, and recommendations must remain explicitly separated. The explainability research also requires every finding to trace back to its original source artifact and intermediate computation.  
Source basis: `Municipal Public Works Audit System(1).md`, `MuniAudit AI Explainability Architecture(1).md`, `MuniAudit Evidence Fusion Architecture(1).md`.

---

# 1. Problem Boundary

## 1.1 In scope

The hackathon implementation verifies a **contractor evidence dossier** for a public-works/desilting claim.

Example dossier:

```text
Dossier_Ward09_Bill42/
├── site_photos/
│   ├── photo_001.jpg
│   ├── photo_002.jpg
│   └── ...
├── weighbridge/
│   ├── ticket_001.jpg
│   └── ticket_002.pdf
├── trip_logs.csv
├── measurement_book.pdf
└── contract_metadata.json
```

## 1.2 Out of scope

The locked hackathon architecture does **not**:

- determine criminal guilt
- make autonomous payment decisions
- freeze payment automatically
- scrape live government portals
- query live Vahan services during the demo
- perform exact silt-volume estimation from arbitrary single RGB photographs
- perform underwater optical bathymetry
- run live COLMAP / dense photogrammetry
- deploy a nationwide road-routing cluster
- train a large multimodal foundation model
- use a learned end-to-end fraud classifier
- require proprietary municipal production data

---

# 2. Primary User

## Municipal Auditor / Vigilance Reviewer

The primary user reviews a contractor's billing dossier.

Secondary users:

- Junior Engineer / Site Inspector
- Executive Engineer
- Municipal IT Administrator

The contractor is treated as an external evidence submitter.

### User goal

> "Show me which parts of this dossier are inconsistent, what evidence supports that finding, and what I should inspect next."

---

# 3. Final Architecture at a Glance

```text
                           ┌───────────────────────────┐
                           │      AUDITOR WEB UI       │
                           │ Evidence Upload / Review  │
                           │ Map / Findings / Report   │
                           └─────────────┬─────────────┘
                                         │ HTTPS
                                         ▼
                      ┌────────────────────────────────────┐
                      │ AMAZON ECS EXPRESS MODE            │
                      │ FastAPI + Audit Worker Container   │
                      │                                    │
                      │ API / Auth / Job Orchestration     │
                      │ Evidence Normalization             │
                      │ ML + Rules + Fusion                │
                      └───────┬───────────────┬────────────┘
                              │               │
                 Presigned S3 │               │ SQS Job
                              │               ▼
                              │       ┌─────────────────┐
                              │       │ Amazon SQS       │
                              │       │ Standard + DLQ  │
                              │       └────────┬────────┘
                              │                │
                              ▼                ▼
                    ┌──────────────┐   ┌────────────────┐
                    │ Amazon S3    │   │ Audit Worker   │
                    │ Evidence     │   │ Processing      │
                    │ Store        │   │                │
                    │ Object Lock  │   │ ┌────────────┐ │
                    └──────────────┘   │ │ Visual CV  │ │
                                       │ ├────────────┤ │
                                       │ │ OCR        │ │
                                       │ ├────────────┤ │
                                       │ │ Geo/Time   │ │
                                       │ ├────────────┤ │
                                       │ │ Rules      │ │
                                       │ ├────────────┤ │
                                       │ │ Anomaly    │ │
                                       │ └────────────┘ │
                                       └───────┬────────┘
                                               │
                                               ▼
                                  ┌────────────────────────┐
                                  │ Evidence Fusion Engine │
                                  │ Subjective Logic       │
                                  │ + uncertainty          │
                                  └────────────┬───────────┘
                                               │
                                               ▼
                                  ┌────────────────────────┐
                                  │ Explainability Engine   │
                                  │ Facts + Evidence Chain  │
                                  └────────────┬───────────┘
                                               │
                                  ┌────────────┴───────────┐
                                  ▼                        ▼
                         Amazon Bedrock              PostgreSQL
                      (optional formatter)       PostGIS + pgvector
                                  │                        │
                                  └────────────┬───────────┘
                                               ▼
                                         Auditor Review
```

---

# 4. AWS Architecture — LOCKED

## 4.1 Amazon ECS Express Mode

**Primary application and worker runtime.**

The current architecture uses **Amazon ECS Express Mode**, not App Runner.

The attached Gemini validation incorrectly classified ECS Express Mode as fictitious. Current AWS documentation confirms that ECS Express Mode is a real ECS deployment mode that provisions a Fargate-based service, load balancer, networking, monitoring, and autoscaling with simplified configuration.

References:

- https://docs.aws.amazon.com/AmazonECS/latest/developerguide/express-service-overview.html
- https://docs.aws.amazon.com/AmazonECS/latest/developerguide/express-service-getting-started.html

For the hackathon:

- one Express Mode service
- one primary application container
- minimum 1 task
- maximum 1 task unless actual concurrency requires otherwise
- FastAPI serves API/UI endpoints
- background worker consumes SQS jobs
- health endpoint: `/health`

### Why

- very low infrastructure setup burden
- public HTTPS URL
- Fargate execution
- good Docker/local parity
- avoids App Runner new-customer restriction
- avoids managing an ALB manually

AWS states that App Runner is closed to new customers and recommends ECS Express Mode for migration/new deployments.  
https://docs.aws.amazon.com/apprunner/latest/dg/apprunner-availability-change.html

---

# 5. S3 Evidence Store

## Role

Authoritative binary store for original submitted evidence.

Stores:

- original photos
- receipt images
- PDFs
- CSV / XLSX files
- GIS files
- generated audit package artifacts

## Requirements

Each artifact receives:

```text
evidence_id
sha256_digest
s3_object_key
content_type
byte_size
upload_timestamp
dossier_id
source_type
version_id
```

## Integrity

At ingestion:

1. calculate client-side SHA-256
2. upload using a presigned S3 URL
3. record checksum
4. worker re-verifies downloaded bytes
5. persist artifact digest with evidence metadata

For the hackathon:

- S3 Versioning: ON
- Object Lock: Governance mode

For production:

- Object Lock configuration can be strengthened to Compliance mode after governance / retention requirements are formally validated.

Do not claim that S3 Object Lock itself establishes legal admissibility.

---

# 6. Authentication & Authorization

## Amazon Cognito

Roles:

```text
AUDITOR
ENGINEER
CONTRACTOR
ADMIN
```

The API receives authenticated identity and role information.

Authorization must be enforced at the application/database layer.

### Minimum policy

A contractor may submit and view only its authorized dossiers.

An auditor may review dossiers within its municipal scope.

An admin may manage configuration.

Review actions are recorded.

For the hackathon, a single municipal tenant can be used while preserving tenant-aware IDs in the schema.

---

# 7. Application/API Layer

## FastAPI

FastAPI is the single application boundary.

### Core endpoints

```text
POST   /auth/session
POST   /dossiers
POST   /dossiers/{id}/files
POST   /dossiers/{id}/finalize

GET    /dossiers/{id}
GET    /dossiers/{id}/status
GET    /dossiers/{id}/findings
GET    /dossiers/{id}/evidence/{evidence_id}

POST   /findings/{id}/review
POST   /findings/{id}/override

GET    /dossiers/{id}/report
GET    /health
```

### Important rule

The web request should never wait for the full ML/OCR/geospatial pipeline.

The request creates/updates the dossier and returns a job status.

---

# 8. Dossier Lifecycle

```text
CREATED
   ↓
UPLOADING
   ↓
FINALIZING
   ↓
QUEUED
   ↓
PROCESSING
   ↓
┌───────────────┬──────────────────┬───────────────────┐
│               │                  │
COMPLETED   INCONCLUSIVE     TECHNICAL_ABSTENTION
│               │                  │
▼               ▼                  ▼
REVIEW_READY   HUMAN_REVIEW       RETRY / RESUBMIT
```

If the system identifies objective inconsistencies:

```text
COMPLETED
   ↓
FINDINGS_PRESENT
   ↓
HUMAN_REVIEW
```

---

# 9. Amazon SQS

## Choice

**SQS Standard Queue + DLQ**

Do not use FIFO unless future workload requirements prove ordering is necessary.

The processing system is idempotent, so duplicate delivery is acceptable.

### Message

```json
{
  "job_id": "uuid",
  "dossier_id": "uuid",
  "tenant_id": "uuid",
  "schema_version": "1.0",
  "created_at": "ISO-8601"
}
```

The queue message contains IDs, not the full evidence payload.

Evidence remains in S3.

### Idempotency

The database enforces uniqueness on processing operations.

Recommended pattern:

```text
UNIQUE(dossier_id, pipeline_version)
UNIQUE(dossier_id, evidence_id, processor_version)
```

### DLQ

Jobs that exceed retry policy are moved to a dead-letter queue.

The system shows:

```text
TECHNICAL_ABSTENTION
```

rather than a contractor violation.

---

# 10. PostgreSQL — Single System of Record

## Amazon RDS for PostgreSQL

Use one primary database with:

- PostgreSQL
- PostGIS
- pgvector
- JSONB
- relational constraints

Current AWS documentation confirms RDS for PostgreSQL supports PostGIS and supported pgvector extensions on supported PostgreSQL engine versions.  
https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Appendix.PostgreSQL.CommonDBATasks.Extensions.html

## No extra database in MVP

Do NOT add:

- DynamoDB
- OpenSearch
- graph database
- separate vector DB

unless a measured future workload proves the need.

---

# 11. Canonical Database Schema

```text
municipal_tenants
contracts
contractors
work_orders
drain_reaches
disposal_sites

audit_dossiers
evidence_items
processing_jobs
model_runs

visual_embeddings
weighbridge_slips
trip_records
gps_observations

rule_results
anomaly_signals
fusion_results

audit_findings
audit_reviews
review_comments

audit_ledger
report_artifacts
system_configuration
```

## Key relationships

```text
Tenant
 └── Contract
      └── WorkOrder
           ├── DrainReach
           └── AuditDossier
                 ├── EvidenceItem
                 ├── ProcessingJob
                 ├── RuleResult
                 ├── AnomalySignal
                 ├── FusionResult
                 ├── Finding
                 ├── Review
                 └── ReportArtifact
```

---

# 12. Evidence Provenance Model

Every finding must be traceable:

```text
Finding
  ↓
Rule / Model Run
  ↓
Extracted / Calculated Feature
  ↓
Evidence Item
  ↓
SHA-256
  ↓
S3 Object
```

Each model run records:

```text
model_name
model_version
weights_hash
processor_version
input_schema_version
timestamp
parameters
output_summary
```

This provides reproducibility and traceability.

---

# 13. Visual Evidence Verification Engine

## Locked architecture

```text
image
 ↓
orientation / basic normalization
 ↓
SSCD 512-d embedding
 ↓
pgvector HNSW retrieval
 ↓
candidate pair(s)
 ↓
SIFT/FLANN
 ↓
RANSAC geometric verification
 ↓
visual-copy finding
```

### Critical correction

**Do NOT use pHash as a prefilter before SSCD.**

The research validation correctly identified that pHash can discard cropped/rotated copies before the stronger instance-level model sees them.

pHash may be retained as a constant-time **exact/very-near exact duplicate shortcut**, but it must never be the only gateway into SSCD.

## Locked model

**Meta AI SSCD ResNet-50, 512-dimensional embedding**

Run using:

- ONNX Runtime
- CPU
- container-local inference

Do not make DINOv2 or CLIP the main copy detector.

Do not train a new copy-detection model during the hackathon.

Source basis: `Visual Evidence Verification CV Architecture(1).md`.

---

# 14. Candidate Retrieval

Use `pgvector`.

For the expected hackathon-scale image archive:

```text
embedding vector(512)
```

with HNSW indexing.

Store:

```text
evidence_id
embedding
model_version
created_at
contract_id
reach_id
```

Search can be:

- contract-scoped
- municipal-scope
- historical cross-contract

The system must preserve the distinction between:

```text
same image instance
vs.
same type of infrastructure
```

A semantic match is not automatically a duplicate.

---

# 15. Geometric Verification

For retrieved visual candidates:

```text
SSCD candidate
    ↓
SIFT keypoints
    ↓
descriptor matching
    ↓
RANSAC homography
    ↓
inlier ratio
    ↓
geometric consistency
```

Output:

```json
{
  "candidate_evidence_id": "...",
  "sscd_similarity": 0.91,
  "matched_keypoints": 127,
  "inliers": 81,
  "inlier_ratio": 0.64,
  "classification": "POSSIBLE_COPY"
}
```

Important:

The similarity score is a model output, not proof of fraud.

---

# 16. Visual Tampering Detection

## Hackathon

Use:

- EXIF consistency analysis
- file/container metadata checks
- ELA/compression-artifact heuristics

## Do NOT build

- TruFor
- Noiseprint++
- complex pixel-level tampering model
- C2PA PKI infrastructure

These remain post-hackathon extensions.

Source basis: `Visual Evidence Verification CV Architecture(1).md` and `MuniAudit-AI Security Architecture and Adversarial Threat Model(1).md`.

---

# 17. Thermal Weighbridge Document Intelligence

## Input path

```text
receipt image/PDF
    ↓
format validation
    ↓
PDF → page images where required
    ↓
perspective correction
    ↓
deskew
    ↓
CLAHE / illumination normalization
    ↓
Amazon Textract
    ↓
field extraction
    ↓
confidence gating
    ↓
canonical ReceiptData
```

### Textract

Use:

**Amazon Textract AnalyzeDocument + Queries**

for supported single-page receipt images.

Current AWS quotas confirm synchronous operations are constrained in size/page count; multi-page PDF/TIFF processing uses asynchronous APIs.  
https://docs.aws.amazon.com/textract/latest/dg/limits-document.html

Therefore:

- single-page receipts → synchronous path
- multi-page documents → split/rasterize or use the asynchronous path where justified
- do not send oversized documents directly to synchronous Textract

### Current AWS limit note

Current AWS documentation lists a 10 MB synchronous file limit and a one-page synchronous limit for PDF/TIFF.  
https://docs.aws.amazon.com/textract/latest/dg/limits-document.html

---

# 18. Local OCR Fallback

For Build It/offline mode:

**PaddleOCR**

Pipeline:

```text
receipt
 ↓
document preprocessing
 ↓
PaddleOCR
 ↓
field parser
 ↓
confidence
 ↓
validation
```

Sauvola/local binarization is allowed in the local fallback path where experimentally justified.

Do not assume the exact preprocessing parameters in the research are universal; benchmark them on the actual receipt samples.

---

# 19. Canonical ReceiptData

All OCR engines must normalize into the same internal contract:

```json
{
  "ticket_number": "...",
  "weighbridge_id": "...",
  "vehicle_number": "...",
  "gross_weight_kg": 0,
  "tare_weight_kg": 0,
  "net_weight_kg": 0,
  "timestamp": "...",
  "field_confidence": {
    "ticket_number": 0.0,
    "vehicle_number": 0.0,
    "gross_weight_kg": 0.0,
    "tare_weight_kg": 0.0,
    "net_weight_kg": 0.0
  }
}
```

No downstream component should care whether the data came from Textract or PaddleOCR.

---

# 20. OCR Uncertainty Rules

If a critical field cannot be read reliably:

```text
LOW_CONFIDENCE
      ↓
INCONCLUSIVE_DATA
      ↓
MANUAL_REVIEW_REQUIRED
```

Never silently impute a financial field.

The failure-resilience research explicitly treats unreadable OCR as an abstention/technical condition rather than a contractor violation.  
Source: `Failure-Resilient Architecture for MuniAudit-AI(1).md`.

---

# 21. Deterministic Arithmetic Verification

For a weighbridge receipt:

```text
gross - tare ≈ net
```

Use:

```text
abs((gross - tare) - net) <= scale_tolerance
```

The tolerance must come from:

1. documented scale resolution/specification where available, or
2. clearly documented demo configuration.

Do **not** hard-code a universal tolerance such as 20 kg and present it as a statutory fact.

Output:

```text
PASS
VARIANCE
INCONCLUSIVE
```

---

# 22. Physical Mass Envelope

Use verified vehicle mass parameters when available.

Preferred model:

```text
payload_max = GVW - ULW

claimed_net <= payload_max
```

with any contractual or measurement tolerance explicitly documented.

Do NOT infer third-party tipper-body volume from Vahan.

Do NOT assume Vahan contains custom body dimensions.

Volumetric capacity can be represented through a separate verified manufacturer/body configuration table when data is available.

The volumetric check is a secondary consistency signal, not the central claim of the system.

---

# 23. Geospatial Architecture

## PostGIS is the core spatial engine

Store:

- drain centerlines
- drain reaches
- chainage
- work polygons
- disposal-site polygons
- GPS observations
- vehicle locations

Use:

```text
ST_LineLocatePoint
ST_DWithin
ST_Contains
ST_Intersects
```

where appropriate.

---

# 24. Coordinate Standard

Normalize operational coordinates to:

```text
WGS84 / EPSG:4326
```

while preserving original source coordinates and source CRS metadata.

Never overwrite source data.

---

# 25. Chainage Verification

The contracted drain reach is represented as a measured line.

Input:

```text
GPS/photo coordinate
```

Output:

```text
reach_id
along-track chainage
perpendicular offset
inside/outside authorized corridor
```

This allows the system to distinguish:

```text
PHOTO EXISTS
```

from:

```text
PHOTO IS ASSOCIATED WITH AUTHORIZED WORK LOCATION
```

---

# 26. Kinematic Verification

## Two-tier reasoning

### Physical lower-bound test

Use Haversine/geodesic distance:

```text
d_geodesic
```

and elapsed time:

```text
Δt
```

to calculate:

```text
v_required = d_geodesic / Δt
```

If even the straight-line minimum distance would require a speed above a **verified upper bound for that scenario**, then the recorded trip is physically infeasible.

### Important

Do NOT treat "90 km/h" as a universal law-of-physics speed limit.

Do NOT use arbitrary "60 km/h urban speed = fraud" logic.

The upper bound should be:

- vehicle-specific where possible
- contract/legal where applicable
- otherwise explicitly configurable and classified as an empirical/operational assumption

---

# 27. Route Plausibility

For the hackathon MVP:

**do not deploy OSRM / Valhalla clusters.**

Use:

1. geodesic lower bound
2. PostGIS spatial checks
3. configurable operational plausibility envelopes

If routing is needed later:

- GraphHopper/Valhalla can be introduced post-hackathon
- heavy-vehicle restrictions can then be modeled more realistically

This avoids large routing-graph infrastructure during the event.

---

# 28. Matter-Space Collision Check

Detect impossible vehicle records such as:

```text
Vehicle X
Location A
10:00

Vehicle X
Location B
10:00
```

where A and B are spatially separated beyond what the configured physical bound allows.

The result should be:

```text
MATTER_SPACE_INCONSISTENCY
```

not automatically:

```text
FRAUD
```

The geospatial research strongly supports separating physical invariants from empirical anomalies and legal/contractual rules.  
Source: `Geospatial and Temporal Reasoning Subsystem Architecture(1).md`.

---

# 29. Deterministic Rule Engine

Rules are explicit, testable functions.

Examples:

```text
RULE-001: gross - tare ≈ net
RULE-002: ticket identifier uniqueness
RULE-003: vehicle record/category consistency
RULE-004: authorized drain corridor containment
RULE-005: disposal-site geofence containment
RULE-006: temporal ordering
RULE-007: physical reachability
RULE-008: duplicate evidence linkage
RULE-009: payload upper bound
```

Every rule emits:

```json
{
  "rule_id": "RULE-001",
  "result": "FAIL",
  "severity": "HIGH",
  "inputs": {...},
  "calculation": "...",
  "source_evidence_ids": [...]
}
```

---

# 30. Anomaly Detection

Do not train a "fraud classifier."

Use nominal historical/benchmark data to learn the normal distribution of operational features.

Possible implementation:

- ECOD
- robust z-score / percentile methods
- Isolation Forest only where justified

Candidate features:

```text
trip duration
route distance
load quantity
OCR confidence
visual similarity
image timestamp relation
ticket timing
vehicle reuse frequency
contractor-level variance
```

Output:

```text
ANOMALY_SCORE
```

not:

```text
FRAUD_PROBABILITY
```

---

# 31. Evidence Fusion

## Locked conceptual model

```text
                 HARD GATES
                     │
                     ├── clear physical/contract violation
                     │
                     ▼
              SOFT EVIDENCE
                     │
          anomaly + confidence signals
                     │
                     ▼
              SUBJECTIVE LOGIC
                     │
        ┌────────────┼────────────┐
        │            │            │
       belief     disbelief    uncertainty
        │            │            │
        └────────────┼────────────┘
                     ▼
             REVIEW TRIAGE
```

The evidence-fusion research compares rule scoring, logistic regression, Bayesian approaches, anomaly ensembles and learned multimodal models, and ultimately favors a two-tier approach with deterministic invariants followed by uncertainty-aware evidential fusion.

### Locked implementation

**Tier 1:** deterministic rules

**Tier 2:** nominal anomaly scores → opinion mapping → Subjective Logic consensus

### Do NOT use

- end-to-end multimodal fraud classifier
- arbitrary weighted "fraud score"
- synthetic labels presented as real fraud probabilities

---

# 32. Evidence Consistency Score (ECS)

ECS is an operational consistency indicator.

It must not be described as:

```text
Probability contractor committed fraud
```

It should mean:

```text
How consistently the available evidence supports a procedurally/physically coherent dossier.
```

The exact numerical mapping must be benchmarked and documented before being presented as a scientific metric.

For the hackathon, ECS should be accompanied by:

```text
confidence_tier
missing_modalities
modality_attributions
```

---

# 33. Audit Review Priority Index (ARPI)

ARPI is a **triage ranking**, not a criminal-probability score.

Its purpose is:

```text
Which cases should the human auditor inspect first?
```

Use ordinal tiers:

```text
LOW
MEDIUM
HIGH
CRITICAL
```

A numeric 0–100 display can be used only if the mapping is clearly identified as a review-priority score and is validated against the benchmark.

---

# 34. Missing Modality Semantics

Missing evidence must not become negative evidence.

Example:

```text
No GPS
```

means:

```text
GPS = UNKNOWN
```

not:

```text
GPS = SUSPICIOUS
```

Similarly:

```text
OCR failed
```

means:

```text
DATA_DEFICIENCY
```

not:

```text
CONTRACTOR_VIOLATION
```

This is a locked safety principle.

---

# 35. Explainability Architecture

Each finding uses a canonical chain:

```text
FINDING
 ↓
EVIDENCE
 ↓
EXTRACTED FACT
 ↓
MODEL OUTPUT
 ↓
RULE RESULT
 ↓
CALCULATION
 ↓
UNCERTAINTY
 ↓
RECOMMENDED ACTION
```

Every UI finding must visibly distinguish:

### FACT

Directly observed/extracted.

### MODEL OUTPUT

Generated by ML.

### RULE RESULT

Deterministic computation.

### INFERENCE

Cross-modal statistical interpretation.

### RECOMMENDATION

Human-audit next step.

Source basis: `MuniAudit AI Explainability Architecture(1).md`.

---

# 36. Finding Object

```json
{
  "finding_id": "uuid",
  "type": "TRIP_PHYSICAL_INCONSISTENCY",
  "epistemic_type": "RULE_RESULT",
  "severity": "HIGH",
  "confidence": "HIGH",
  "summary": "Recorded timestamps imply a transit duration inconsistent with the configured physical bound.",
  "facts": [...],
  "model_outputs": [...],
  "rule_results": [...],
  "evidence_ids": [...],
  "calculation": {...},
  "uncertainty": {...},
  "recommendation": "Verify original telematics and scale timestamps."
}
```

---

# 37. Human Review

The auditor must be able to:

```text
CONFIRM
DISMISS
OVERRIDE
REQUEST MORE EVIDENCE
```

Every action creates a ledger event:

```text
reviewer_id
timestamp
action
finding_id
reason_code
comment
previous_state
new_state
```

Manual override requires a structured reason.

The system never hides the fact that an automated finding was overridden.

---

# 38. Cognitive Forcing UI

The reviewer UI should show evidence before the system's conclusion.

Recommended sequence:

```text
SOURCE EVIDENCE
      ↓
CALCULATION
      ↓
MODEL RESULT
      ↓
SYSTEM INTERPRETATION
      ↓
AUDITOR ACTION
```

Avoid presenting:

```text
RED "FRAUD"
```

at the top of the screen.

Instead display:

```text
REVIEW REQUIRED
Why?
• Photo similarity
• Ticket inconsistency
• Trip-time anomaly
```

---

# 39. Bedrock Usage

Amazon Bedrock is **optional** and strictly bounded.

## Allowed

Input:

```text
validated structured facts
+
rule results
+
model outputs
+
recommended action
```

Output:

```text
objective audit summary
```

## Forbidden

Bedrock must not:

- inspect raw arbitrary evidence and decide fraud
- override rules
- modify numerical values
- invent evidence
- issue criminal conclusions
- decide payment
- suppress uncertainty

The system should use constrained prompts and structured JSON output.

---

# 40. Audit Report

Export:

```text
MuniAudit-AI Audit Dossier
```

Contents:

1. dossier metadata
2. evidence inventory
3. artifact hashes
4. extracted receipt fields
5. visual-match findings
6. geospatial calculations
7. deterministic rule results
8. anomaly signals
9. evidence-fusion summary
10. uncertainty/missing-data statement
11. auditor review actions
12. recommendations
13. provenance information

The report should describe objective discrepancies and review recommendations rather than automatically alleging criminal conduct.

---

# 41. Cryptographic Audit Ledger

PostgreSQL table:

```text
audit_ledger
```

Each event contains:

```text
event_id
dossier_id
event_type
event_timestamp
actor_id
payload_hash
previous_event_hash
current_event_hash
```

Hash-chain:

```text
H_n = SHA256(event_payload || H_(n-1))
```

This makes subsequent alteration detectable.

For production, independent archival/checkpoint mechanisms can be added.

---

# 42. Security Architecture

## Hackathon controls

- Cognito authentication
- role-based authorization
- tenant-aware database queries
- S3 least-privilege IAM
- presigned uploads
- object type validation
- payload-size restrictions
- SHA-256 hashing
- S3 versioning/Object Lock
- append-only audit events
- secrets outside source code
- CloudWatch logs

## Threats considered

```text
photo tampering
EXIF spoofing
duplicate evidence
GPS manipulation
vehicle identity spoofing
ticket recycling
OCR manipulation
API IDOR/BOLA
replay
evidence overwrite
reviewer compromise
adversarial visual input
prompt injection
```

Source basis: `MuniAudit-AI Security Architecture and Adversarial Threat Model(1).md`.

---

# 43. Failure-Resilience Architecture

## Four states

```text
NORMAL
DEGRADED
INCONCLUSIVE
TECHNICAL_ABSTENTION
```

### NORMAL

All required evidence and dependencies available.

### DEGRADED

Some secondary inputs fail, but enough reliable evidence remains for a limited analysis.

### INCONCLUSIVE

Evidence quality is too poor for a reliable conclusion.

### TECHNICAL_ABSTENTION

Infrastructure/dependency failure prevents valid computation.

---

# 44. Failure Rules

| Failure | System response |
|---|---|
| OCR unreadable | manual review |
| missing EXIF | continue without metadata-dependent rule |
| routing unavailable | use geodesic lower-bound checks only |
| SQS job failure | retry then DLQ |
| corrupted file | technical deficiency |
| database timeout | technical abstention |
| Bedrock unavailable | use template-based report |
| visual matcher fails | report insufficient visual confidence |
| missing GPS | omit GPS-derived conclusion |

The critical invariant is:

> **System failure must never silently become contractor wrongdoing.**

Source: `Failure-Resilient Architecture for MuniAudit-AI(1).md`.

---

# 45. AWS Service Inventory — Locked

## Required

| AWS service | Purpose |
|---|---|
| ECS Express Mode | FastAPI + worker runtime |
| S3 | evidence storage |
| SQS | async job queue |
| RDS PostgreSQL | relational + spatial + vector data |
| Cognito | authentication |
| Textract | cloud document extraction |
| CloudWatch | logs / metrics |

## Optional

| AWS service | Purpose |
|---|---|
| Bedrock | evidence-grounded audit memo |
| Secrets Manager | production secret handling |
| KMS | stronger production encryption/key management |

## Explicitly not in MVP

```text
OpenSearch Serverless
DynamoDB
SageMaker Real-Time GPU
Step Functions
EventBridge
SNS
OSRM cluster
Valhalla cluster
TruFor
C2PA infrastructure
Kafka
Temporal
A2I
```

These are production/post-hackathon candidates, not hackathon requirements.

---

# 46. Why no OpenSearch?

Expected hackathon-scale embedding volume does not justify a second vector infrastructure layer.

Using:

```text
PostgreSQL
+
pgvector
```

keeps:

```text
contract
+
evidence
+
spatial data
+
embeddings
+
findings
```

inside one consistency boundary.

This was a repeated recommendation across the AWS/system architecture research.

---

# 47. Why no SageMaker?

The hackathon uses a compact pretrained SSCD model through ONNX CPU inference.

A dedicated managed inference endpoint adds:

- deployment work
- endpoint cost
- monitoring complexity
- model-serving overhead

without corresponding value at the hackathon workload.

---

# 48. Why no Step Functions?

For the locked MVP:

```text
API
 ↓
S3
 ↓
SQS
 ↓
Worker
 ↓
PostgreSQL
```

is sufficient.

Step Functions becomes useful when the production system requires:

- durable multi-step orchestration
- long-running workflows
- explicit workflow history
- human wait states

but it is not required for the hackathon.

---

# 49. Why no live Government APIs?

The project must remain demo-reliable.

Use local snapshots / controlled reference datasets for:

- vehicle metadata
- municipal drain geometry
- disposal zones
- benchmark records

External APIs can be integrated later.

Never make the three-minute demo depend on a government portal being available at that moment.

---

# 50. Hackathon BUILD IT Architecture

```text
Docker Compose
├── FastAPI
├── Audit Worker
├── PostgreSQL
│   ├── PostGIS
│   └── pgvector
├── Local evidence store
├── SSCD ONNX
├── PaddleOCR
└── local benchmark / routing data
```

Same domain models and processing contracts as Ship It.

Cloud-specific adapters:

```text
S3Adapter
TextractAdapter
CognitoAdapter
RDSAdapter
```

Local adapters:

```text
LocalStorageAdapter
PaddleOCRAdapter
LocalPostgresAdapter
MockIdentityAdapter
```

---

# 51. Configuration Architecture

Do not hard-code operational assumptions.

Use a versioned configuration object:

```yaml
pipeline_version: "1.0"

visual:
  model: "sscd_resnet50"
  embedding_dim: 512

ocr:
  critical_field_confidence_threshold: 0.65

geospatial:
  coordinate_system: "EPSG:4326"

rules:
  scale_tolerance_kg: <validated_value>
  corridor_buffer_m: <contract_or_demo_value>
  physical_speed_bound_kmh: <scenario_specific_value>

fusion:
  method: "subjective_logic"

output:
  score_semantics: "review_priority"
```

Every finding stores the configuration version used.

---

# 52. ML Experiment Architecture

The benchmark must avoid leakage.

Use:

### Spatial holdout

Different geographic areas.

### Temporal holdout

Different time periods.

### Contractor holdout

Different contractor identities/fleets where available.

### Device holdout

Different image sources where possible.

### Receipt-template holdout

Different weighbridge/template sources.

Do not place transformed copies of the same base image in both train and test.

Do not allow the same dossier to leak across train and test.

Source: `MuniAudit-AI ML Evaluation and Experiment Architecture(1).md`.

---

# 53. Synthetic Benchmark

Because real labeled contractor-fraud corpora are unavailable at useful scale:

Use synthetic anomaly injection for controlled evaluation.

Examples:

```text
visual:
crop
rotation
compression
near-copy

document:
digit alteration
thermal fading
field corruption

geospatial:
timestamp compression
coordinate displacement
duplicate vehicle-time overlap

record:
duplicate ticket
quantity mismatch
```

Also include **hard negatives**:

```text
different drain
similar visual appearance
same printer
legitimate traffic detour
valid high load
```

Synthetic results must always be labeled:

> **performance on the synthetic benchmark**

not:

> **real-world fraud detection accuracy**

---

# 54. Evaluation Metrics

## Visual

- Precision@K
- Recall@K
- mAP where appropriate
- false-positive rate at a chosen recall

## OCR

- CER
- WER
- critical-field exact match

## Spatial

- chainage error
- perpendicular offset
- impossible/possible trip classification

## Rules

- deterministic correctness

## Fusion

- review-flag precision
- false-positive investigation rate
- uncertainty behavior
- calibration metrics where assumptions support them

---

# 55. Latency Strategy

The UI should never block on the full pipeline.

### Fast operations

```text
upload creation
status query
finding retrieval
evidence retrieval
```

### Async operations

```text
SSCD
OCR
geospatial processing
anomaly analysis
fusion
report generation
```

The user sees:

```text
PROCESSING
```

then receives:

```text
REVIEW READY
```

---

# 56. Cost Strategy

Use the lean architecture.

## Avoid

- permanent GPU endpoints
- OpenSearch minimum infrastructure
- unnecessary NoSQL
- unnecessary orchestration
- unnecessary routing clusters

The cost research consistently identified managed GPU/vector infrastructure as disproportionate for hackathon workload.

Current AWS pricing should be checked immediately before deployment because pricing and free-tier conditions can change.

---

# 57. Deployment Flow

```text
Developer
   ↓
Git repository
   ↓
Docker build
   ↓
Amazon ECR
   ↓
ECS Express Mode
   ↓
Public HTTPS URL
```

Required environment configuration:

```text
AWS_REGION
S3_BUCKET
SQS_QUEUE_URL
SQS_DLQ_URL
RDS_HOST
RDS_DB
COGNITO_USER_POOL_ID
COGNITO_CLIENT_ID
BEDROCK_MODEL_ID (optional)
```

Secrets must not be committed.

---

# 58. Repository Structure

```text
muniaudit-ai/
│
├── app/
│   ├── api/
│   ├── auth/
│   ├── domain/
│   ├── ingestion/
│   ├── evidence/
│   ├── visual/
│   ├── documents/
│   ├── geospatial/
│   ├── rules/
│   ├── anomaly/
│   ├── fusion/
│   ├── explainability/
│   ├── review/
│   ├── reports/
│   └── storage/
│
├── models/
│   └── sscd/
│
├── benchmark/
│   ├── raw/
│   ├── synthetic/
│   ├── annotations/
│   └── splits/
│
├── migrations/
│
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── benchmark/
│   └── e2e/
│
├── scripts/
│
├── config/
│
├── Dockerfile
├── docker-compose.yml
├── alembic.ini
└── README.md
```

---

# 59. Testing Strategy

## Unit

- arithmetic rules
- coordinate conversions
- chainage
- hash generation
- feature normalization
- fusion math

## Integration

- S3 upload
- SQS processing
- PostgreSQL
- Textract adapter
- Cognito authorization

## ML

- SSCD retrieval
- geometric verification
- OCR field extraction
- anomaly scoring

## End-to-end

```text
create dossier
→ upload evidence
→ finalize
→ queue
→ process
→ findings
→ human review
→ report
```

The complete e2e demo must run from a clean environment.

---

# 60. Three-Minute Demo — LOCKED

## 0:00–0:20

Show:

```text
Municipality receives contractor billing dossier.
```

Explain the verification gap.

## 0:20–0:45

Upload dossier.

Show S3 evidence storage and processing status.

## 0:45–1:25

### Finding 1 — Visual Evidence

Show:

```text
Current Photo
       ↕
Historical Photo
```

SSCD finds a candidate.

SIFT/RANSAC confirms geometric similarity.

## 1:25–2:05

### Finding 2 — Document + Rule

Show a weighbridge slip.

Textract extracts:

```text
Gross
Tare
Net
Vehicle
Time
```

Rule engine demonstrates:

```text
Gross - Tare ≠ Net
```

or another verified inconsistency.

## 2:05–2:35

### Finding 3 — Geospatial

Show:

```text
Drain
 ↓
Vehicle
 ↓
Weighbridge
 ↓
Disposal site
```

Display the physical/geospatial consistency calculation.

## 2:35–2:50

### Evidence Fusion

Show:

```text
2 deterministic inconsistencies
2 soft anomalies
1 missing modality
↓
HIGH REVIEW PRIORITY
```

## 2:50–3:00

### Explainability

Open:

```text
Why was this flagged?
```

Show source evidence → calculation → finding → recommended human action.

Mention:

```text
AWS:
ECS Express Mode
S3
SQS
RDS PostgreSQL
Textract
Cognito
CloudWatch
```

---

# 61. Demo Data Rules

Do not present synthetic records as real municipal records.

The UI must label demo content:

```text
DEMONSTRATION DATA
Synthetic / Controlled Benchmark
```

When citing real-world case evidence in the pitch, keep the real-world claims separate from the synthetic demonstration.

---

# 62. Final Locked Model Stack

| Task | Locked method |
|---|---|
| Visual copy detection | Meta SSCD ResNet-50 |
| Visual similarity search | pgvector HNSW |
| Fine visual verification | SIFT + FLANN + RANSAC |
| Basic visual metadata | EXIF / container analysis |
| OCR — Ship It | Amazon Textract |
| OCR — Build It | PaddleOCR |
| Image preprocessing | OpenCV |
| Spatial DB | PostGIS |
| Geodesic distance | Haversine |
| Temporal validation | deterministic Python rules |
| Anomaly detection | ECOD / robust nominal anomaly analysis |
| Evidence fusion | Subjective Logic |
| Final priority | ECS + ARPI semantics |
| Summary generation | Bedrock, optional |
| Report | deterministic template + optional Bedrock wording |

---

# 63. Explicit Model Rejections

## Rejected for MVP

### CLIP

Not appropriate as the primary instance-copy detector.

### DINOv2

Useful representation model, but not the primary copy-detection model.

### pHash

Allowed only as an exact duplicate shortcut; never as the main candidate gate.

### TruFor

Post-hackathon.

### SuperPoint + LightGlue

Post-hackathon for a heavier geometric verifier; SIFT/RANSAC is sufficient for MVP.

### Deep multimodal transformer

Rejected due to lack of genuine labeled fraud corpus and high deployment/validation cost.

### Large LLM reasoning over raw evidence

Rejected from the decision path.

### Monocular exact volume estimation

Rejected.

### Underwater RGB bathymetry

Rejected.

---

# 64. Production Evolution

After the hackathon, the platform can evolve toward:

```text
Hackathon
  ↓
ECS Express Mode
  ↓
Separate web + worker ECS services
  ↓
Step Functions / EventBridge
  ↓
heavier ML inference
  ↓
advanced tamper detection
  ↓
real routing engine
  ↓
larger vector infrastructure
  ↓
multi-tenant municipal deployment
```

Potential production additions:

- ECS Fargate worker fleet
- SageMaker where GPU inference is justified
- dedicated vector search where volume justifies it
- GraphHopper / Valhalla
- advanced image-tampering models
- C2PA where provenance infrastructure exists
- stronger key management
- centralized secrets
- RDS Proxy
- dedicated observability
- formal data governance

These are not required for the hackathon.

---

# 65. Final Architectural Invariants

The following are LOCKED:

### Invariant 1

**Raw evidence is immutable/tamper-evident and hash-addressed.**

### Invariant 2

**ML extracts or scores evidence; deterministic rules verify explicit invariants.**

### Invariant 3

**Missing evidence creates uncertainty, not wrongdoing.**

### Invariant 4

**The system produces review priorities, not criminal guilt probabilities.**

### Invariant 5

**Every finding must be traceable to source evidence.**

### Invariant 6

**Every model output carries model/version metadata.**

### Invariant 7

**Every deterministic rule is reproducible from its inputs and configuration.**

### Invariant 8

**Synthetic benchmark performance is never represented as field fraud-detection performance.**

### Invariant 9

**The hackathon path must remain functional without live government APIs.**

### Invariant 10

**The three-minute demo must show an end-to-end working workflow, not isolated components.**

---

# 66. Final Architecture Status

## LOCKED

The final hackathon architecture is:

```text
                         MuniAudit-AI

                    ┌───────────────────┐
                    │    Web Auditor    │
                    └─────────┬─────────┘
                              │
                              ▼
                 ┌────────────────────────┐
                 │ ECS EXPRESS MODE        │
                 │ FastAPI + Worker        │
                 └───────────┬────────────┘
                             │
                    ┌────────┴────────┐
                    │                 │
                    ▼                 ▼
                  S3             SQS + DLQ
               Evidence               │
                    │                 ▼
                    │          Multimodal Worker
                    │                 │
                    │      ┌──────────┼───────────┐
                    │      ▼          ▼           ▼
                    │   Visual      OCR       Geo/Time
                    │   SSCD      Textract     PostGIS
                    │      │          │           │
                    │      └──────────┼───────────┘
                    │                 ▼
                    │          Deterministic Rules
                    │                 │
                    │                 ▼
                    │          Nominal Anomalies
                    │                 │
                    │                 ▼
                    │        Subjective Logic Fusion
                    │                 │
                    │                 ▼
                    │        Explainable Findings
                    │                 │
                    └────────────┬────┘
                                 ▼
                     RDS PostgreSQL
                     ├── relational data
                     ├── PostGIS
                     ├── pgvector
                     ├── findings
                     ├── reviews
                     └── audit ledger
                                 │
                                 ▼
                         Human Auditor
                                 │
                                 ▼
                         Audit Dossier PDF
```

---

# 67. Final "Do Not Change" List During the Hackathon

Do not change architecture merely because a new framework looks more impressive.

Do not add:

- OpenSearch
- DynamoDB
- SageMaker GPU
- Kafka
- Temporal
- Step Functions
- routing clusters
- massive VLMs

unless an actual blocker forces the decision and the architecture is consciously re-baselined.

Do not replace SSCD with a generic semantic embedding model without benchmark evidence.

Do not turn ARPI into "fraud probability."

Do not make exact silt tonnage from arbitrary photos the headline capability.

Do not let Bedrock become the decision-maker.

Do not let a technical failure create an adverse contractor finding.

---

# 68. Source Set Used to Build This Locked Architecture

This architecture synthesizes the uploaded research files:

1. `Municipal Public Works Audit System(1).md`
2. `MuniAudit System Architecture Design(1).md`
3. `AWS Cloud Architecture for MuniAudit-AI(1).md`
4. `Research the cost and performance architecture of...(1).md`
5. `Visual Evidence Verification CV Architecture(1).md`
6. `Thermal Weighbridge Receipt Document Intelligence Architecture(1).md`
7. `Geospatial and Temporal Reasoning Subsystem Architecture(1).md`
8. `MuniAudit Evidence Fusion Architecture(1).md`
9. `MuniAudit AI Explainability Architecture(1).md`
10. `Failure-Resilient Architecture for MuniAudit-AI(1).md`
11. `MuniAudit-AI Security Architecture and Adversarial Threat Model(1).md`
12. `MuniAudit-AI ML Evaluation and Experiment Architecture(1).md`

Current AWS fact checks additionally used:

- Amazon ECS Express Mode:
  https://docs.aws.amazon.com/AmazonECS/latest/developerguide/express-service-overview.html
- Amazon ECS Express Mode getting started:
  https://docs.aws.amazon.com/AmazonECS/latest/developerguide/express-service-getting-started.html
- AWS App Runner availability change:
  https://docs.aws.amazon.com/apprunner/latest/dg/apprunner-availability-change.html
- Amazon Textract quotas:
  https://docs.aws.amazon.com/textract/latest/dg/limits-document.html
- Amazon RDS PostgreSQL extensions:
  https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Appendix.PostgreSQL.CommonDBATasks.Extensions.html
- Amazon RDS PostGIS:
  https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Appendix.PostgreSQL.CommonDBATasks.PostGIS.html

---

# 69. One-Sentence Architecture Definition

> **MuniAudit-AI is a cloud-deployed, human-in-the-loop multimodal evidence reconciliation engine that combines instance-level computer vision, document intelligence, geospatial reasoning, deterministic physical/contract checks, nominal anomaly detection, and uncertainty-aware evidence fusion to identify and explain public-works billing inconsistencies without autonomously determining criminal guilt.**