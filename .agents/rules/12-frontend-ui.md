---
trigger: glob
globs:
  - "frontend/**/*"
  - "app/**/*.{ts,tsx,css}"
  - "src/**/*.{tsx,ts,css}"
description: MuniAudit-AI forensic UI and anti-vibe-coding rules.
---

# Frontend / UI Engineering Rules

## Prime directive

Build a professional forensic investigation workspace, not a generic AI dashboard.

Priorities:
1. evidence
2. hierarchy
3. trust
4. actionability
5. polish

## Before changing frontend

Read:
- `DESIGN.md`
- relevant UI specification
- current route/layout
- existing components
- relevant tests

Do not invent a new visual system for a single component.

## Design-system discipline

Use existing design tokens.

Do not introduce:
- arbitrary colors
- one-off gradients
- random radii
- inconsistent typography
- new UI libraries for isolated convenience

Prefer repository-local components.

## Domain language

Communicate:
- evidence review
- cross-source reconciliation
- geospatial investigation
- uncertainty
- human audit

Avoid generic crypto/gaming/chatbot/consumer-SaaS aesthetics.

## Investigation workspace

Keep related evidence together where practical:
- evidence viewer
- findings panel
- map
- timeline
- explainability

Do not fragment the primary investigation flow across unnecessary pages.

## Epistemic UI

Always distinguish:

FACT
MODEL OUTPUT
RULE RESULT
INFERENCE
RECOMMENDATION

Severity cannot be encoded by color alone.

## Required states

Every important asynchronous flow must handle:
- idle
- loading
- processing
- ready
- empty
- partial
- inconclusive
- error
- retry
- technical abstention
- review required

## Evidence interaction

A finding should let a reviewer answer:

What happened?
What evidence supports it?
What did the model produce?
What rule was applied?
What is uncertain?
What should I review?

## Motion

Use motion for orientation, feedback, state transition, and evidence correlation. Avoid decorative animation.

## Accessibility

Preserve:
- keyboard focus
- readable contrast
- semantic labels
- text + icon status encoding
- reduced-motion behavior

## UI completion

Before declaring completion:
- typecheck
- lint
- relevant tests
- browser/screenshot check where available
- inspect intended viewport
- inspect loading/error states
- verify design-token compliance
- inspect Git diff
