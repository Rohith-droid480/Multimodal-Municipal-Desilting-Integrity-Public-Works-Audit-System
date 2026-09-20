# MuniAudit-AI — Core Context & Project Invariants

**System Identity:** MuniAudit-AI  
**Domain:** Multimodal Municipal Desilting Integrity & Public-Works Audit System  
**Status:** ARCHITECTURE LOCKED (v1.0)  
**Governing Document:** `MuniAudit-AI-Final-Locked-Architecture-v1.0.md`  
**Repository:** `Rohith-droid480/Multimodal-Municipal-Desilting-Integrity-Public-Works-Audit-System`  

---

## 1. Executive Purpose & Problem Boundary

MuniAudit-AI is an evidence-reconciliation and investigative decision-support system designed for municipal vigilance officers and auditors reviewing storm-water-drain desilting claims and public-works billing dossiers.

Contractors submit heterogeneous evidence:
1. Site photographs (pre-, during-, post-desilting)
2. Weighbridge receipts / slips (gross, tare, net vehicle weights)
3. Vehicle trip logs & transport records
4. Municipal drain reach geometries & KML GIS tracks
5. Measurement books and contract metadata

### Core Epistemic Principle
> **The system does not decide whether a contractor is guilty or commit automated payment freezes. It determines whether submitted evidence is internally consistent, flags objective physical and contractual anomalies, and prioritizes what a human auditor should inspect next.**

---

## 2. Epistemic Taxonomy & Non-Negotiable Invariants

All outputs, findings, and logs must strictly segregate epistemic categories:
- `FACT`: Cryptographically verified or direct sensor/document observations (e.g., image SHA-256 digest, raw weighbridge ticket timestamp).
- `MODEL_OUTPUT`: Statistical and machine learning model predictions (e.g., SSCD image similarity embedding distance, OCR text extraction confidence).
- `RULE_RESULT`: Deterministic civil engineering or mathematical calculations (e.g., Haversine velocity rule, mass-balance volumetric envelope).
- `INFERENCE`: Probabilistic fusion opinion or anomaly score combining multiple signals.
- `RECOMMENDATION`: Suggested follow-up actions for the human vigilance officer.

### Administrative Classifications
- `VERIFIED_COMPLIANT`: Evidence independently reconciled with no material exceptions.
- `SUBSTANTIVE_INCONSISTENCY`: Material discrepancy identified between independent evidence artifacts.
- `INCONCLUSIVE_DATA`: Insufficient evidence to verify or refute claimed work.
- `TECHNICAL_ABSTENTION`: System processing failure, malformed payload, or service timeout.

> [!CRITICAL]
> **Missing evidence or technical failure is NOT proof of fraud or wrongdoing.**

---

## 3. System Architecture Summary

The system is architected as a **Modular Monolith**:
- **Application Runtime:** FastAPI (Python 3.13/3.14) containerized for Amazon ECS Express Mode / local Docker Compose.
- **System of Record:** PostgreSQL 16 + PostGIS (spatial queries) + pgvector (512-d SSCD copy detection).
- **Evidence Storage:** Amazon S3 with Object Lock (governance mode) and SHA-256 content verification. Local filesystem adapter for Build-It local parity.
- **Asynchronous Processing:** Amazon SQS Standard Queue + Dead-Letter Queue (DLQ). Workers execute idempotent analysis tasks.
- **Authentication:** Role-Based Access Control (RBAC) via Amazon Cognito (`AUDITOR`, `ENGINEER`, `CONTRACTOR`, `ADMIN`).
- **Explainability:** Transparent evidence trails tracing each finding back to source artifact SHA-256 and mathematical calculation.

---

## 4. Layer & Dependency Direction

Dependencies flow strictly inward:
```text
Presentation (UI) → Application (FastAPI) → Domain (Pure Entities & Epistemic Rules)
                                                  ↑
                                   Infrastructure & ML Adapters
```
1. Domain code must never import database drivers, web frameworks, or cloud SDKs.
2. UI must never communicate directly with the database or execute ML models.
3. Workers and analysis components must be idempotent and testable in isolation.
