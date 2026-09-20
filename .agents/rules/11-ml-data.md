---
trigger: glob
globs:
  - "ml/**/*.py"
  - "backend/**/ml/**/*.py"
  - "backend/**/rules/**/*.py"
  - "data/**/*.py"
  - "scripts/eval/**/*.py"
description: ML, data-science, benchmark, and forensic-analysis rules for MuniAudit-AI.
---

# ML & Data Integrity Rules

## ML is not the decision authority

ML may:
- extract
- retrieve
- compare
- score anomalies
- estimate confidence

Deterministic code must handle:
- arithmetic identities
- explicit spatial conditions
- explicit temporal conditions
- configured physical/contractual constraints

Never implement a direct product "fraud probability" classifier.

## Data provenance

Tag all data:

REAL_MUNICIPAL
REAL_PUBLIC
DERIVED
SYNTHETIC
SIMULATED
CONTROLLED_CAPTURE

Never imply synthetic/unrelated public data is real municipal evidence.

## Metrics

All reported metrics must come from executed evaluation code.

Record:
- dataset version/hash
- model version
- code version
- split
- seed
- exact command
- result artifact

Never hand-type a metric into documentation.

## Leakage

Before evaluation verify applicable:
- spatial holdout
- temporal holdout
- contractor/source holdout
- device holdout
- receipt-template holdout
- near-duplicate isolation

## Synthetic benchmarks

Synthetic anomalies can measure controlled algorithmic sensitivity.

They do not establish real-world fraud-detection rates.

Use realistic hard negatives and document generation methods.

## Visual forensics

For instance-level copy detection:
- use the approved SSCD approach
- use vector retrieval for candidates
- use geometric verification where specified
- never make pHash the sole gate for transformed images

Similarity is evidence, not a verdict.

## OCR

Never silently invent low-confidence critical fields.

Use manual review/inconclusive state when confidence is inadequate.

## Fusion

Keep modality confidence and missingness explicit.

Do not turn heterogeneous signals into a pseudo-probability without an approved mathematical specification.

## Reproducibility

Lock seeds where stochastic evaluation is used.

Do not tune evaluation parameters merely to improve the headline score.
