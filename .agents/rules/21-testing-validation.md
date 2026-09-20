---
trigger: always-on
description: Milestone testing, manual validation, release gates, and cross-tool verification protocol for MuniAudit-AI.
---

# MuniAudit-AI — Testing & Milestone Validation Protocol

## 0. Purpose

This file governs HOW the team proves that MuniAudit-AI is working.

The coding agent must understand the project's current stage, what is expected to be working, how it is tested, and what human validation must happen before moving forward.

Use:

- Antigravity Gemini 3.8 → implementation + command execution + test execution
- ChatGPT Go → independent reasoning/review, architecture and test-result interpretation
- Gemini Pro → independent research/validation/red-team, especially current external facts and high-risk assumptions

No tool is allowed to declare a milestone complete solely from its own generated explanation.

Actual execution evidence is authoritative for code/test claims.

---

# 1. Verification hierarchy

Use four levels:

## Level 1 — Static verification

Examples:
- syntax
- typecheck
- lint
- formatting
- import checks

## Level 2 — Automated behavior verification

Examples:
- unit tests
- integration tests
- API contract tests
- database tests
- worker tests

## Level 3 — System verification

Examples:
- end-to-end dossier processing
- browser tests
- local Docker workflow
- AWS deployment smoke tests

## Level 4 — Human acceptance verification

A human manually confirms:
- workflow makes sense
- output is correct
- UI is understandable
- evidence is traceable
- failure behavior is safe
- demo works

Passing Level 1 does not imply passing Level 4.

---

# 2. Every task has a Definition of Done

A task is complete only when applicable criteria are satisfied:

```text
REQUIREMENT
+
IMPLEMENTATION
+
AUTOMATED TEST
+
STATIC CHECKS
+
DIFF AUDIT
+
MANUAL CHECK (when applicable)
+
DOCUMENTATION
+
PROJECT STATE
```

If manual validation was required but not performed, the task is not fully verified.

---

# 3. Every task must report evidence

Antigravity must report:

```text
COMMAND:
<exact command>

RESULT:
<actual output summary>

EXIT CODE:
<actual code>

FILES CHANGED:
<actual files>

TESTS:
<actual counts>

LIMITATIONS:
<known unverified items>
```

Never generate fictional test output.

Never estimate test counts.

---

# 4. Milestone model

Use these project milestones:

```text
M0 — Repository / Scaffolding Ready
M1 — Data Pipeline Working
M2 — Core ML Components Working
M3 — Deterministic Rules Working
M4 — Evidence Fusion Working
M5 — API + Async Processing Working
M6 — Investigation UI Working
M7 — End-to-End System Working
M8 — Benchmark / Evaluation Verified
M9 — Security / Reliability Hardened
M10 — AWS Deployment Verified
M11 — Demo Hardened
M12 — Submission Frozen
```

The exact project phase is stored in `PROJECT_STATE.json`.

Do not advance the phase automatically just because code exists.

---

# 5. M0 — Repository / Scaffolding Ready

## Automated validation

Run the repository's actual:
- dependency install/check
- lint
- typecheck
- backend smoke test
- frontend smoke test
- Docker build
- minimal startup test

## Manual validation

Human checks:
- repository opens cleanly
- expected services/directories exist
- environment configuration is understandable
- README setup works from a clean checkout
- no accidental secrets are present

## Gate

Move to M1 only when:
- clean install/build works
- test harness works
- application starts
- project structure is understandable

---

# 6. M1 — Data Pipeline Working

## Automated validation

Test:
- dataset loading
- schema validation
- coordinate normalization
- evidence metadata creation
- duplicate detection
- provenance/hash generation
- synthetic-data labeling

## Manual validation

Open representative records and verify:

- values are correct
- source type is correct
- real/synthetic labels are correct
- units are correct
- IDs link correctly
- source files are traceable

### Human question

"Could another engineer understand exactly where this record came from?"

If not, milestone is not complete.

---

# 7. M2 — Core ML Components Working

## Visual ML

Automated:
- fixture inference
- embedding shape
- deterministic preprocessing
- retrieval test
- geometric verification test

Manual:
- inspect true duplicate pair
- inspect transformed duplicate
- inspect hard negative
- confirm the UI/result doesn't call normal visual similarity a confirmed copy

## OCR

Automated:
- extraction fixtures
- critical-field parsing
- low-confidence path
- malformed receipt handling

Manual:
- inspect original receipt
- compare extracted fields against the document
- inspect uncertainty
- confirm no silent field invention

## Gate

Do not progress based only on model load success.

A representative input must pass through the full component contract.

---

# 8. M3 — Deterministic Rules Working

For every rule, test:

- nominal case
- boundary case
- invalid case
- missing-data case
- unit conversion case
- rounding/tolerance case

Examples:
- gross − tare ≈ net
- ticket uniqueness
- vehicle category compatibility
- coordinate containment
- temporal ordering
- physical reachability

## Manual validation

Use a hand-calculated example.

Human verifies:

```text
input
→ calculation
→ rule result
```

matches an independent calculation.

A rule is not accepted because its test is green if the assertion itself is wrong.

---

# 9. M4 — Evidence Fusion Working

Automated validation:

- full agreement
- conflicting modalities
- missing modality
- all-uncertain input
- zero/edge cases
- numerical stability
- repeatability

Manual validation:

Create at least these dossiers:

```text
CASE A — strong consistent evidence
CASE B — one clear deterministic inconsistency
CASE C — conflicting modalities
CASE D — missing data
CASE E — technical failure
```

For each case verify:
- findings
- uncertainty
- attribution
- final review priority
- evidence links

Human must be able to answer:

"Why did the system reach this review state?"

---

# 10. M5 — API + Async Processing Working

Automated:

```text
create dossier
→ upload
→ finalize
→ queue
→ worker
→ persist result
→ fetch status
→ fetch findings
```

Test:
- retry
- duplicate delivery
- timeout
- malformed payload
- missing artifact
- worker crash/restart
- idempotency

Manual:
- submit a full dossier
- watch status transition
- refresh the browser during processing
- confirm the final result remains consistent
- retry a failed job
- verify no duplicate finding is created

---

# 11. M6 — Investigation UI Working

Automated:
- TypeScript/typecheck
- lint
- component tests
- route tests
- browser tests where configured

Manual:

### Workflow test

1. Open a dossier.
2. Find a flagged image.
3. Open the source evidence.
4. Inspect the matched historical image.
5. Open the relevant receipt.
6. Inspect extracted values.
7. Open the map.
8. Inspect the geospatial finding.
9. Open "Why flagged?"
10. Confirm facts/model output/rule result are visibly distinct.
11. Perform human review action.
12. Confirm review action is recorded.

### UI failure test

Manually simulate:
- slow network
- failed API
- missing image
- empty evidence set
- OCR failure
- partial dossier

Verify the interface never presents missing information as a successful finding.

---

# 12. M7 — End-to-End System Working

This is the first MAJOR system gate.

Required flow:

```text
Evidence upload
→ storage
→ async processing
→ visual analysis
→ document analysis
→ geospatial analysis
→ rules
→ anomaly analysis
→ fusion
→ findings
→ reviewer UI
→ human review
→ report
```

## Automated

Have at least one deterministic E2E fixture.

## Manual

A human performs the entire workflow on a clean environment.

Record:
- duration
- failures
- confusing steps
- missing evidence
- output correctness

### Gate

Do not call the product "end-to-end working" if any major step was manually faked or bypassed.

---

# 13. M8 — Benchmark / Evaluation Verified

Before running the benchmark, verify:

- dataset version
- data hash
- split
- seed
- model version
- code commit
- evaluation command

Automated:
- benchmark executes
- metrics are generated from code
- result file contains provenance
- no train/test leakage checks fail

Manual:
- inspect several predictions
- inspect false positives
- inspect false negatives
- inspect hard negatives
- verify synthetic vs real labels

Never present synthetic benchmark sensitivity as real-world fraud-detection accuracy.

---

# 14. M9 — Security / Reliability Hardened

Automated checks:
- secret scan
- dependency audit
- authentication tests
- authorization tests
- object-level authorization tests
- upload validation
- path traversal tests
- SQL injection tests where applicable
- worker retry tests
- failure-state tests

Manual red-team:
- upload unexpected file
- access another dossier
- replay an upload
- submit malformed data
- remove metadata
- provide contradictory records
- attempt an unauthorized review action

Gate:
- no critical security issue open
- no known authentication bypass
- no secret in repository
- all critical paths have failure behavior

---

# 15. M10 — AWS Deployment Verified

## Before deployment

Antigravity:
- run complete relevant test suite
- build container
- validate environment configuration
- inspect infrastructure
- report planned resources

ChatGPT Go:
- perform independent architecture review of the deployment plan

Gemini Pro:
- independently verify current high-risk AWS facts/limits where needed

Human:
- approve deployment

## After deployment

Run:
- health check
- API smoke test
- upload test
- processing test
- database test
- log inspection
- browser access test

Manual:
- use the deployed product as a real auditor would
- refresh
- log in/out
- upload
- inspect
- review
- export

Do not call deployment successful because the container merely started.

---

# 16. M11 — Demo Hardened

The demo must work from a known clean fixture.

## Required manual run

Perform the full demo:

```text
Open app
→ open demo dossier
→ show evidence
→ trigger/observe finding
→ inspect visual evidence
→ inspect document
→ inspect map
→ inspect explanation
→ perform human review
→ export/report
```

Run it five times from a clean state.

Track:
- failures
- flaky behavior
- load delays
- browser console errors
- visual regressions
- data reset failures

## Demo rule

Do not add new product features during final demo hardening unless a critical defect requires it.

---

# 17. M12 — Submission Frozen

Before freeze:

Automated:
- full test suite
- frontend build
- backend build
- Docker build
- security scan
- benchmark artifact check
- documentation consistency check
- clean working tree check

Manual:
- clean-machine setup
- three-minute demo
- AWS deployed demo
- final UI walkthrough
- final report export
- final README walkthrough

Then:
- create release tag
- record commit
- record model/data versions
- archive benchmark results
- archive demo fixture version

After freeze, no code changes without an explicit human emergency override.

---

# 18. Milestone Review Protocol

At EVERY milestone:

## Step A — Antigravity

Produce:

```text
MILESTONE:
WHAT WAS BUILT:
FILES CHANGED:
TESTS RUN:
RESULTS:
KNOWN ISSUES:
ARCHITECTURE IMPACT:
NEXT DEPENDENCY:
```

## Step B — ChatGPT Go

Perform an independent review:
- Does the implementation satisfy the requirement?
- Is the architecture still coherent?
- Are claims backed by execution evidence?
- What was not actually verified?
- What regression risks remain?

## Step C — Gemini Pro

Perform an independent red-team/validation review when useful:
- current external facts
- AWS behavior
- ML methodology
- dataset/evaluation concerns
- adversarial edge cases

## Step D — Human

Approve:

```text
PASS
PASS WITH FOLLOW-UP
BLOCKED
```

Only PASS advances the milestone.

---

# 19. Cross-tool responsibilities

## Antigravity Gemini 3.8

Primary:
- inspect repository
- implement
- run commands
- run tests
- debug
- build
- deploy under approval
- capture empirical evidence

Not final authority on:
- architecture changes
- legal interpretation
- uncertain external facts
- its own success claims

## ChatGPT Go

Primary:
- architecture reasoning
- requirement interpretation
- code review
- test-result interpretation
- regression reasoning
- design review
- manual acceptance checklist

Not the source of:
- unexecuted test results
- deployment claims

## Gemini Pro

Primary:
- deep external research
- current API/AWS verification
- independent red-team
- scientific methodology review
- dataset/source validation

Not the source of:
- repository runtime truth
- unexecuted benchmark results

---

# 20. Validation severity

Use:

## GREEN
Verified and stable.

## AMBER
Works, but has a known limitation or manual dependency.

## RED
Broken, unverified, or unsafe.

Project phase should not advance with an unresolved RED issue relevant to the phase.

---

# 21. "What is actually happening?" report

At each milestone, the agent must be able to answer:

```text
WHERE ARE WE?
WHAT IS ALREADY WORKING?
WHAT IS PARTIALLY WORKING?
WHAT IS NOT WORKING?
WHAT WAS ACTUALLY TESTED?
WHAT WAS ONLY REASONED ABOUT?
WHAT IS BLOCKING US?
WHAT DEPENDS ON THIS?
WHAT COMES NEXT?
```

This report is mandatory before major milestone transitions.

---

# 22. Manual validation principle

Manual validation is not optional "demo polish".

For MuniAudit-AI, a human must verify:

- source evidence is correctly displayed
- calculated values are understandable
- findings correspond to real evidence
- uncertainty is visible
- review actions are meaningful
- the UI does not misrepresent model output as fact
- failures are not converted into adverse findings
- the complete workflow is usable by a person who did not build the software

---

# 23. Final release gate

MuniAudit-AI is ready for submission only when:

```text
CODE CORRECT
+
TESTS GREEN
+
END-TO-END WORKS
+
ML RESULTS REPRODUCIBLE
+
DATA PROVENANCE CLEAR
+
SECURITY ACCEPTABLE
+
AWS DEPLOYED
+
UI MANUALLY VERIFIED
+
DEMO REHEARSED
+
DOCUMENTATION ACCURATE
+
WORKING TREE CLEAN
```

A claim of readiness without evidence is not acceptable.
