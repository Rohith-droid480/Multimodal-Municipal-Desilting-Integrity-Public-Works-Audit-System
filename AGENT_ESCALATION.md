# MuniAudit-AI — Agent Escalation Queue (AGENT_ESCALATION.md)

This queue records critical architectural decisions, security exceptions, and blocker items requiring explicit human sign-off before implementation.

---

## Active Escalation Items

*No unresolved escalations currently pending.*

---

## Escalation Protocol

An escalation must be logged whenever an agent encounters:
1. Architectural deviations from `MuniAudit-AI-Final-Locked-Architecture-v1.0.md`
2. Introduction of unapproved external cloud services or third-party paid APIs
3. Alterations to canonical database schemas affecting primary/foreign keys
4. Weakening of authentication, authorization, or evidence integrity checks
5. Repeated failure across three distinct debugging attempts (Strike 3)
