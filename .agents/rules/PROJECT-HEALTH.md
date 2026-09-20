# MuniAudit-AI — Project Health Check

Run at the beginning of major work sessions and before milestones.

## 1. State

Read `PROJECT_STATE.json`.
Compare its last verified commit to the current Git commit.
If stale, mark the state STALE.

## 2. Git

- inspect working tree
- confirm branch
- inspect unexpected changes

## 3. Code quality

Run the repository's actual:
- typecheck
- lint
- targeted tests
- relevant regression tests

## 4. Architecture

Check changes against:
- `ARCHITECTURE.md`
- ADRs
- approved data/cloud boundaries

## 5. Data/ML

Check:
- dataset version
- model version
- evaluation provenance
- leakage controls
- metric artifacts

## 6. Security

Check:
- secrets
- dependency changes
- auth/authz
- unsafe upload/parser changes
- infrastructure permissions

## 7. UI

Check:
- design-token compliance
- console errors
- key investigation workflow
- async/error states
- visual regression where available

## 8. Output

STATUS: GREEN / AMBER / RED

VERIFIED:
-

STALE:
-

BLOCKERS:
-

RISKS:
-

RECOMMENDED NEXT ACTION:
-
