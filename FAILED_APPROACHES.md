# MuniAudit-AI — Negative Learning Bank (FAILED_APPROACHES.md)

This document records rejected implementation patterns, runtime failure autopsies, and architectural anti-patterns observed during engineering cycles.

Before executing any task, the engineering agent must consult this file to verify that the planned approach does not duplicate a previously failed strategy.

---

## Prohibited Patterns Index

| ID | Technology / Component | Forbidden Pattern | Root Cause / Rationale | Authoritative Alternative |
|:---|:---|:---|:---|:---|
| **FP-001** | Database Layer | Proliferation of separate vector/document databases (e.g., Pinecone, Milvus, Redis, DynamoDB) | Introduces multi-master sync failures, increased AWS bill, and operational complexity. | Single PostgreSQL 16 RDS instance with PostGIS and pgvector extensions. |
| **FP-002** | Decision Engine | Autonomous "Fraud Probability" classification models | Epistemic invalidity; algorithmic black boxes cannot establish legal intent or satisfy civil audit standards. | Evidence Consistency Score (ECS) & Audit Review Priority Index (ARPI) with human auditor review. |
| **FP-003** | Civil Engineering Rules | Static arbitrary vehicle velocity thresholds without geospatial geodesic calculation | Inaccurate trip distance estimations result in false positive transport anomalies. | WGS-84 Haversine/Vincenty geodesic calculation with terrain and road curvature slack factor. |
| **FP-004** | Cloud Architecture | Deprecated AWS App Runner configuration for new deployments | AWS has frozen App Runner to new customers and officially advises ECS Express Mode / Fargate. | Amazon ECS Express Mode / Fargate container deployment. |
| **FP-005** | Storage Layer | Blind binary ingestion without client/server cryptographic hashing | Prevents tamper-evident non-repudiation in audit proceedings. | Dual-stage SHA-256 computation and S3 Object Lock governance mode. |

---

## Failure Autopsies

*No runtime autopsies recorded yet. Entries will be appended when a debugging cycle reaches Strike 3 or an architectural dead-end is encountered.*
