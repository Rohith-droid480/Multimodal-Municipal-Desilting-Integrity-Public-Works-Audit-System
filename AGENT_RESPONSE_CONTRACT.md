# MuniAudit-AI — Agent Response Contract

All engineering task completion reports must strictly adhere to the following schema:

---

## 1. Task Metadata
- **Task ID:**
- **Current Phase:**
- **Objective:**

## 2. Epistemic Understanding
- **Requirement Satisfied:**
- **Governing Specification:** (Architecture ADR / Spec section)

## 3. Changes Made
- **Modified Files:**
- **Created Files:**
- **Deleted Files:**
- **Dependencies Changed:**

## 4. Verification Evidence
- **Commands Executed:**
- **Observed Results:** (Exit status, output snippets)
- **Tests Executed:** (Targeted, regression, coverage)

## 5. Architecture Self-Check
- **Architecture Preserved:** YES/NO
- **Interfaces Changed:** YES/NO
- **Schema Changed:** YES/NO
- **New Service Introduced:** YES/NO
- **Security Impact:** NONE/LOW/MEDIUM/HIGH

## 6. Risks & Limitations
- Document any unresolved edge cases or technical debt.

## 7. State Update
- **PROJECT_STATE Updated:** YES/NO
- **Git Commit Checkpoint:**
- **Last Verified Commit:**

## 8. Next Action
- Exactly one logical subsequent task.
