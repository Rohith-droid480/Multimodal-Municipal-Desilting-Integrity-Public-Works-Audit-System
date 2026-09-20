---
trigger: glob
globs:
  - "backend/**/*.py"
  - "src/**/*.py"
  - "tests/**/*.py"
description: Backend Python, API, worker, and data-layer rules for MuniAudit-AI.
---

# Backend Engineering Rules

## Architecture

Respect:

API
→ application/service layer
→ domain/rules/ML adapters
→ persistence/infrastructure

Do not let:
- frontend import database models directly
- domain logic depend on HTTP unnecessarily
- ML modules mutate unrelated application state
- infrastructure-specific code leak into domain logic without an adapter

## Python

Use the repository's pinned Python version and dependency lockfile.

Prefer:
- typed functions
- Pydantic v2 where used by the repository
- explicit exceptions
- structured return values
- deterministic pure functions for forensic rules

Avoid:
- hidden global state
- broad exception swallowing
- magic constants
- unnecessary abstractions
- speculative refactoring

Require repeated concrete use cases before adding a generalized abstraction.

## API

For endpoint changes:
1. inspect existing schemas
2. inspect callers/tests
3. preserve compatibility where possible
4. define validation/error behavior
5. add API tests
6. run typecheck/lint/tests
7. run integration tests when contracts change

Never return success when processing actually failed.

## Workers

Workers must be:
- idempotent
- observable
- retry-aware
- bounded in side effects

Do not acknowledge a queue job before required durable results exist.

## Database

Use the approved PostgreSQL/PostGIS/pgvector architecture.

Never modify an already-applied migration in place. Create a new approved migration.

Check indexes, constraints, transactions, and nullability before altering queries.

## Forensic semantics

Keep these separate:

FACT
MODEL_OUTPUT
RULE_RESULT
INFERENCE
RECOMMENDATION

Never turn missing data into a violation.

## Completion

Backend work is complete only when relevant tests, typecheck, lint, scope audit, and requirements are satisfied.
