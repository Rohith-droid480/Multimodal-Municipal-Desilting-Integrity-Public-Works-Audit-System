# MuniAudit-AI — Multimodal Municipal Desilting Integrity & Public-Works Audit System

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16%20%2B%20PostGIS%20%2B%20pgvector-336791.svg)](https://www.postgresql.org/)
[![Status](https://img.shields.io/badge/Status-Scaffolding%20Ready%20(Milestone%2004)-success.svg)]()

MuniAudit-AI is an evidence-reconciliation and investigative decision-support platform designed for municipal vigilance officers and auditors reviewing storm-water-drain desilting claims and public-works billing dossiers.

---

## 🏛️ Core Purpose & Philosophy

Contractors submit disparate evidence sources: site photographs, weighbridge receipts, vehicle trip logs, municipal drain reach geometries, and measurement books. In current workflows, these are reviewed independently, creating a critical verification gap.

MuniAudit-AI automates multi-source cross-verification to identify objective physical, temporal, and spatial discrepancies:
> **The system does not decide whether a contractor is guilty or automate payment freezing. It determines whether submitted evidence is internally consistent, highlights objective anomalies with transparent cryptographic evidence trails, and prioritizes what human auditors should inspect.**

---

## 📐 Architecture Overview

MuniAudit-AI is architected as a **Modular Monolith**:
- **Application Runtime:** FastAPI containerized for Amazon ECS Express Mode / Docker Compose.
- **Database (Single System of Record):** PostgreSQL 16 with PostGIS (geospatial reach geometries) and pgvector (512-d SSCD copy detection).
- **Binary Evidence Storage:** Amazon S3 with Object Lock (governance mode) and SHA-256 tamper-evident verification; Local storage adapter for Build-It local development.
- **Asynchronous Queue:** Amazon SQS Standard Queue + Dead-Letter Queue (DLQ).
- **Epistemic Invariant:** Every finding traces back to source evidence SHA-256 digests and explicit mathematical computations, strictly distinguishing `FACT`, `MODEL_OUTPUT`, `RULE_RESULT`, `INFERENCE`, and `RECOMMENDATION`.

---

## 📂 Repository Structure

```text
.
├── .agents/                    # Governance rules, task contracts, and agent specifications
├── app/
│   ├── api/                    # FastAPI routes, schemas, and endpoints (/health, /dossiers, /findings)
│   ├── core/                   # Application settings and environment configuration
│   ├── domain/                 # Pure domain models (Dossier, EvidenceItem, Finding) and epistemic enums
│   ├── infrastructure/         # Database models (SQLAlchemy 2.0) and adapters
│   └── storage/                # Storage abstraction (LocalStorageAdapter, S3StorageAdapter, SHA-256)
├── data/                       # Local evidence storage & raw benchmark datasets
├── docs/                       # Research documentation and locked architectural specifications
├── migrations/                 # Alembic migration environment and version scripts
├── scripts/                    # Database initialization and maintenance scripts
├── tests/                      # Pytest automated test suites
├── Dockerfile                  # Production container definition for ECS Express Mode
├── docker-compose.yml          # Local multi-container development environment (Postgres + pgvector)
├── pyproject.toml              # Modern Python packaging and dependency specifications
├── requirements.txt            # Pinned requirements
└── README.md                   # System documentation
```

---

## 🚀 Quickstart & Local Development

### 1. Prerequisites
- Python 3.12+ (or 3.13 / 3.14)
- Docker & Docker Compose

### 2. Environment Setup
```bash
# Clone the repository
git clone https://github.com/Rohith-droid480/Multimodal-Municipal-Desilting-Integrity-Public-Works-Audit-System.git
cd Multimodal-Municipal-Desilting-Integrity-Public-Works-Audit-System

# Copy environment variables
cp .env.example .env

# Create Python virtual environment
python -m venv venv
.\venv\Scripts\activate   # Windows
# source venv/bin/activate # Linux/macOS

# Install dependencies
pip install -r requirements.txt
```

### 3. Start Database Stack
```bash
docker compose up -d postgres
```

### 4. Run the API Server
```bash
uvicorn app.api.main:app --host 0.0.0.0 --port 8000 --reload
```
Interactive API documentation is available at: `http://localhost:8000/docs`

---

## 🧪 Running Automated Tests

```bash
# Run all tests
pytest -v

# Run targeted test suites
pytest tests/test_health.py -v
pytest tests/test_domain_schemas.py -v
pytest tests/test_storage.py -v
pytest tests/test_api_dossiers.py -v
```
