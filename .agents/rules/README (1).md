# MuniAudit-AI Antigravity Instruction Pack

## Recommended structure

Use **layered instructions**, not one giant file.

### Always-on
- `.agents/rules/00-muniaudit-core.md`
- `.agents/rules/01-project-awareness.md`
- `.agents/rules/14-security.md`
- `.agents/rules/15-testing.md`

### Scoped
- `.agents/rules/10-backend-python.md`
- `.agents/rules/11-ml-data.md`
- `.agents/rules/12-frontend-ui.md`
- `.agents/rules/13-aws-infra.md`

### Working artifacts
- `docs/agent/ANTIGRAVITY-START.md`
- `docs/agent/TASK-CONTRACT.md`
- `docs/agent/AGENT-RESPONSE.md`
- `docs/agent/PROJECT-HEALTH.md`

## Why layered rules?

Keep high-value invariants always available and load subsystem-specific guidance only when needed. This improves maintainability and reduces context clutter.

## Operating principle

Observe → Understand → Plan → Execute → Verify → Reconcile → Record.

The repository is the durable project memory. Chat history is not.
