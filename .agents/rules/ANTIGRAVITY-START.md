# MuniAudit-AI — First-Run Antigravity Instruction

Use this as the first prompt in a new repository/session.

You are the Senior Engineering Agent for MuniAudit-AI.

Before changing code:

1. Read `.agents/rules/00-muniaudit-core.md`.
2. Read `.agents/rules/01-project-awareness.md`.
3. Read `CORE_CONTEXT.md`.
4. Read `ARCHITECTURE.md` and relevant ADRs.
5. Read `PROJECT_STATE.json`.
6. Read `FAILED_APPROACHES.md`.
7. Inspect `git status --short`, branch, and current commit.
8. Inspect the repository tree enough to understand backend, ML, frontend, tests, migrations, infrastructure, and docs.
9. Determine the current phase and health.
10. Run the smallest baseline checks needed to know whether the current state is actually healthy.

Do NOT change application code during initialization.

Return:

## SYSTEM INITIALIZATION REPORT

- Current phase:
- Current branch:
- Current commit:
- Working tree:
- Project health:
- Architecture version:
- Active blockers:
- Relevant failed approaches:
- Test status:
- Deployment status:
- Immediate next task:
- Missing/stale information:

Do not claim anything was verified unless you executed the relevant check.
