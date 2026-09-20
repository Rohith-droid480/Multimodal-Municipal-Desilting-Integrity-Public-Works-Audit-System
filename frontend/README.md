# MuniAudit-AI Auditor Workspace Frontend

## Overview
This is the **Auditor Workspace & Forensic Investigation Console** for **MuniAudit-AI** (WeMakeDevs Bharat Builds Tour 2026).
The application is an evidence-first audit workspace designed for Municipal Accounts Officers, Vigilance Officers, and Executive Engineers to inspect consistency across municipal public-works billing dossiers.

## Tech Stack
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript (Strict Mode)
- **Styling**: Tailwind CSS
- **Primitives**: Lucide React, accessible Radix-style UI tokens
- **Test Runner**: Vitest & React Testing Library

## Key Principles & Epistemic Invariants
1. **Evidence is the Hero**: The workspace prioritizes primary source records (site photos, weighbridge slips, GPS records, measurement books).
2. **Epistemic Separation**: The UI strictly separates:
   - `FACT` (`#0EA5E9`) — Raw extracted observations
   - `MODEL_OUTPUT` (`#8B5CF6`) — Probabilistic model scores (OCR confidence, SSCD similarity, anomaly scores)
   - `RULE_RESULT` (`#F59E0B`) — Deterministic arithmetic and physical checks
   - `INFERENCE` (`#3B82F6`) — Corroborated cross-evidence patterns
   - `RECOMMENDATION` (`#10B981`) — Human reviewer action items
3. **Dual Encoding**: Severity and status are **never encoded by color alone**; every status pairs `color + icon + text`.
4. **No Fraud Probability**: The system never outputs a "fraud probability". It computes an **Evidence Consistency Score (ECS)** and an **Audit Review Priority Index (ARPI)** for human triage.

## Getting Started

### Prerequisites
- Node.js LTS (v20+ or v24+)
- npm 10+

### Installation
```bash
npm install
```

### Development
```bash
npm run dev
```
Open [http://localhost:3000](http://localhost:3000) with your browser.

### Verification Commands
```bash
# Typecheck
npm run typecheck

# Lint
npm run lint

# Unit tests
npm run test

# Production build
npm run build
```
