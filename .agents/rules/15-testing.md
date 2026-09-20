---
trigger: always-on
description: Verification, regression, and Definition-of-Done rules for MuniAudit-AI.
---

# Testing & Verification Rules

## Test hierarchy

Use the smallest sufficient check, then broaden:

1. syntax/typecheck
2. targeted unit tests
3. subsystem/integration tests
4. relevant regression suite
5. end-to-end tests
6. benchmark/evaluation
7. browser/deployment smoke tests

## Change-to-test mapping

Python logic:
→ targeted pytest + type/lint

Shared utility/interface:
→ targeted + affected regression suite

Database/migration:
→ migration + integration tests

ML:
→ unit + controlled benchmark + regression benchmark as required

UI:
→ typecheck/lint + component tests + browser/screenshot checks

Infrastructure:
→ syntax/plan validation + deployment smoke test

## Test integrity

Never delete tests, weaken assertions, skip to hide defects, alter test data to improve metrics, or claim a test passed without executing it.

## Definition of done

A task is complete only when:
- acceptance criteria are satisfied
- relevant tests pass
- static checks pass
- no unexpected files changed
- architecture/security are preserved
- documentation/state are synchronized when required

## Three-strike debugging

Strike 1:
reproduce and make a targeted repair.

Strike 2:
inspect callers/dependencies/environment and reassess.

Strike 3:
STOP, preserve diagnostics, record failure, escalate. No speculative fourth patch.

## False completion

"Implementation exists" does not mean "feature works."
