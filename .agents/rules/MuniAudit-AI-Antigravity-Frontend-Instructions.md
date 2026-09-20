# MuniAudit-AI — Antigravity Frontend Engineering Instructions

**Status:** LOCKED  
**Audience:** Google Antigravity coding agent (Gemini 3.8)  
**Project:** MuniAudit-AI — Multimodal Municipal Evidence Reconciliation & Public-Works Audit Platform  
**Primary UI goal:** Build a professional forensic investigation console, not a generic AI/SaaS dashboard.

---

## 0. READ THIS BEFORE TOUCHING FRONTEND CODE

You are the implementation agent.

Your job is to **implement and refine the approved MuniAudit-AI UI system**, not redesign the product concept from scratch.

Before changing any frontend code:

1. Inspect the existing repository.
2. Read `DESIGN.md` if it exists.
3. Read this instruction file completely.
4. Inspect the current component tree and existing tokens.
5. Reuse existing components before creating new ones.
6. Identify the smallest set of files needed for the requested change.
7. Do not modify unrelated backend, ML, database, or infrastructure code unless the requested UI feature genuinely requires an interface contract change.

### NON-NEGOTIABLE PRIORITY ORDER

When requirements conflict, follow this order:

1. User workflow and evidence clarity
2. Correctness and trust
3. Existing approved architecture
4. Accessibility
5. Visual consistency
6. Performance
7. Animation/polish
8. Decorative effects

Never sacrifice evidence clarity for visual effects.

---

# 1. PRODUCT MENTAL MODEL

MuniAudit-AI is an **evidence investigation and reconciliation workspace**.

The auditor is not browsing a marketing website.

The auditor is answering:

> **"Do the independent pieces of evidence in this public-works dossier tell a consistent story?"**

Primary evidence types:

- Site photographs
- Historical photographs
- Weighbridge receipts
- Vehicle information
- GPS/trip records
- Drain geometry
- Work/contract metadata
- Calculated rule results
- ML outputs
- Anomaly signals
- Review history

The UI must make relationships between these evidence sources visible.

## NEVER turn the product into:

- a generic analytics dashboard
- a chatbot
- a crypto/fintech dashboard
- a neon cybersecurity dashboard
- a consumer SaaS landing page
- an AI-agent command center with fake telemetry
- a collection of unrelated cards

The **evidence is the hero**.

---

# 2. PRIMARY USER

Primary persona:

**Municipal Accounts Officer / Pre-Audit Vigilance Officer / Executive Engineer-grade reviewer**

Design for a professional user who needs:

1. Financial exposure
2. Contract / ward / reach identity
3. Specific objective variance or inconsistency
4. Immediate access to primary source evidence
5. Clear explanation of how the system arrived at a finding
6. Human control over the final decision

The user should not need to understand:

- embeddings
- cosine distance
- IoU
- softmax
- transformer internals
- vector databases

Technical details may be exposed in a secondary evidence/provenance layer when useful, but plain operational language comes first.

Use domain terminology where appropriate:

- Running Account (RA) Bill
- Chainage / Stationing
- Measurement Book (MB)
- Lead Chart
- Tare / Gross / Net
- Vehicle Class
- Weighbridge
- Disposal Site
- Evidence
- Finding
- Review
- Inconclusive
- Technical Abstention

---

# 3. CORE UX WORKFLOW

The primary journey is:

```text
INBOX
  ↓
INGEST DOSSIER
  ↓
PROCESSING
  ↓
TRIAGE
  ↓
FORENSIC WORKSPACE
  ↓
INSPECT EVIDENCE
  ↓
UNDERSTAND FINDING
  ↓
COGNITIVE REVIEW GATE
  ↓
ADJUDICATE
  ↓
CERTIFY / EXPORT
```

Do not create unnecessary page transitions.

The central audit workflow should remain inside the **unified forensic workspace** whenever possible.

---

# 4. PRIMARY INFORMATION ARCHITECTURE

## 4.1 Application Shell

Use:

- compact top navigation/header
- primary content workspace
- minimal persistent chrome
- optional bottom/status bar
- no decorative hero section once the user is inside the application

## 4.2 Landing Screen

The landing screen is an **Active Case Triage Console**, not a generic marketing hero.

It should communicate within seconds:

- what the product audits
- current financial exposure
- queue state
- review priorities
- system processing state
- ability to open a dossier

Use an evidence/operations-first structure.

---

# 5. THE FORENSIC WORKSPACE IS THE FLAGSHIP UI

The flagship screen is a synchronized three-column investigation workspace.

```text
┌───────────────────────────────────────────────────────────────┐
│ TOPBAR: ENGAGEMENT / CLAIM / REVIEW PRIORITY                 │
├───────────────┬──────────────────────────────┬───────────────┤
│               │                              │               │
│ EVIDENCE TREE │   CONTEXTUAL EVIDENCE       │   FINDING &   │
│               │   CANVAS                     │   CAUSALITY   │
│ 280px approx  │   Fluid / dominant            │   440px approx│
│               │                              │               │
│ documents     │ document / photo / map       │ finding       │
│ photos        │                              │ evidence      │
│ GPS           │                              │ rules         │
│ trips         │                              │ model output  │
│ tickets       │                              │ uncertainty   │
│               │                              │ actions       │
├───────────────┴──────────────────────────────┴───────────────┤
│ STATUS / PROVENANCE / PIPELINE STATE                         │
└───────────────────────────────────────────────────────────────┘
```

### Column 1 — Evidence Tree

Show:

- Running Account / claim root
- invoices
- weighbridge slips
- site photos
- historical references
- GPS/trip records
- related work records

Every item may show a small severity/attention indicator.

Clicking an item must update both:

- the central evidence canvas
- the right finding inspector

### Column 2 — Contextual Evidence Canvas

The canvas switches between:

1. Document mode
2. Visual comparison mode
3. Geospatial map mode

Do not navigate to separate pages merely to inspect related evidence.

### Column 3 — Finding & Causality Inspector

The inspector explains:

1. What was found
2. Source evidence
3. Extracted fact
4. Model output
5. Rule result
6. Inference
7. Uncertainty
8. Recommended human action

---

# 6. EPISTEMIC VISUAL LANGUAGE

This is a core product identity.

Never mix epistemic categories visually.

## Fact

Token:

```text
#0EA5E9
```

Use for:

- source data
- extracted raw observations
- directly verifiable values

Icon: database/document/check-style neutral icon as appropriate.

## Model Output

Token:

```text
#8B5CF6
```

Use for:

- OCR confidence
- SSCD similarity
- ML anomaly output
- probabilistic extraction

Always label it as model-generated.

## Rule Result

Token:

```text
#F59E0B
```

Use for:

- arithmetic checks
- deterministic invariants
- physical constraints
- explicit rule evaluation

## Inference

Token:

```text
#3B82F6
```

Use for:

- corroborative relationships
- derived cross-evidence patterns
- anomaly links

## Recommendation / Human Action

Token:

```text
#10B981
```

Use for:

- recommended review action
- confirm
- request rescan
- human sign-off state

### Critical rule

Color alone must NEVER communicate meaning.

Always pair:

**color + icon + text**

---

# 7. SEVERITY SYSTEM

Use:

```text
CRITICAL  #EF4444  + AlertOctagon
HIGH      #F97316  + AlertTriangle
MEDIUM    #EAB308  + AlertCircle / Diamond
INCONCLUSIVE / TECHNICAL  #64748B / Zinc + HelpCircle
CLEAN / VERIFIED          #10B981 + ShieldCheck
```

Never use severity color as the only signal.

A faded/low-confidence OCR field is NOT automatically a red alert.

Technical uncertainty must remain neutral/amber depending on context.

---

# 8. IMPORTANT SEMANTIC DISTINCTION

The UI MUST NOT present:

```text
FRAUD PROBABILITY: 94%
```

The system uses:

```text
EVIDENCE CONSISTENCY SCORE (ECS)
AUDIT REVIEW PRIORITY INDEX (ARPI)
```

Explain these as:

- ECS = how coherently the available evidence supports the dossier
- ARPI = review prioritization / triage, not criminal probability

Never imply that ARPI is legal guilt, criminal intent, or probability of fraud.

Use wording such as:

```text
REVIEW REQUIRED
HIGH REVIEW PRIORITY
SUBSTANTIVE INCONSISTENCY
TECHNICAL ABSTENTION
INCONCLUSIVE
```

---

# 9. VISUAL LANGUAGE

The approved visual archetype is:

> **Professional Forensic Engineering & Investigation Console**

Use a compact, technical, evidence-first visual system.

## Application shell

Deep slate / zinc surfaces.

Reference tokens:

```text
--bg-app:           #090D16
--bg-surface:       #0F172A
--bg-surface-elevated:#1E293B
--bg-surface-active:#334155

--border-subtle:    #1E293B
--border-strong:    #334155
--border-focus:     #0EA5E9

--text-primary:     #F8FAFC
--text-secondary:   #94A3B8
--text-muted:       #64748B
```

## Evidence viewport

Use neutral/light evidence surfaces:

```text
--canvas-bg:        #FFFFFF
--canvas-backdrop:  #F1F5F9
```

The reason is functional:

real document scans and site images must remain visually authentic and easy to inspect.

---

# 10. TYPOGRAPHY

The current project UI specification uses:

### Primary UI font

```text
Inter
```

### Monospace/data font

```text
JetBrains Mono
```

Use monospace for:

- vehicle numbers
- ticket IDs
- chainage
- timestamps
- hashes
- numeric metrics
- weights
- coordinates

Do not randomly introduce:

- Roboto
- Arial
- Helvetica
- additional display fonts

unless the project design system is intentionally and explicitly changed.

Typography is a global token, not a per-component decision.

---

# 11. SPACING & RADII

Use a disciplined scale.

Preferred spacing:

```text
p-2 = 8px
p-3 = 12px
p-4 = 16px
p-6 = 24px
p-8 = 32px
```

Use standard Tailwind spacing tokens.

Do NOT create:

```text
p-[17px]
gap-[13px]
mt-[29px]
```

unless a genuinely measured exception has been explicitly approved.

Preferred radii:

```text
xs = 2px
sm = 4px
md = 6px
lg = 8px
```

Avoid excessive nested rounded containers.

---

# 12. COMPONENT FOUNDATION

Use:

- Next.js App Router
- TypeScript
- Tailwind CSS
- shadcn/ui primitives
- Radix-based accessible primitives where used by the selected shadcn setup
- Lucide React
- Framer Motion only for purposeful interaction

Components should live in the repository and remain directly inspectable by the coding agent.

Do not introduce closed component abstractions that the agent cannot inspect or modify.

## Approved baseline primitives

Prefer local repository components such as:

```text
components/ui/button.tsx
components/ui/badge.tsx
components/ui/card.tsx
components/ui/dialog.tsx
components/ui/table.tsx
components/ui/tabs.tsx
components/ui/input.tsx
components/ui/skeleton.tsx
```

Reuse them.

Do not duplicate primitive components.

---

# 13. PROHIBITED UI PATTERNS

Never introduce:

- generic SaaS dashboard templates
- purple/indigo application backgrounds
- neon cyberpunk styling
- crypto-style glowing cards
- decorative mesh gradients
- random radial gradients
- excessive glassmorphism
- floating 3D cards
- particle backgrounds
- decorative spinning 3D objects
- fake terminal animations
- fake infrastructure telemetry
- meaningless KPI gauges
- random charts without real source data
- unnecessary carousels
- huge hero slogans
- excessive rounded cards
- excessive drop shadows
- arbitrary CSS values
- raw inline SVG when an approved icon exists
- fake "AI confidence" percentages
- UI copy claiming unsupported facts
- animations that obstruct evidence inspection

Do not add Aceternity UI, Magic UI, or Tremor unless the project owner explicitly changes the locked design-system decision.

---

# 14. NO FAKE TELEMETRY

Every metric shown in the UI must be:

1. derived from actual application state/data, OR
2. clearly labelled as demo/fixture data.

Never render fake values such as:

```text
99.98% efficiency
4.2k req/s
24ms latency
10M documents processed
```

unless those values actually correspond to the current system or are explicitly labelled as simulated demonstration values.

Avoid dashboard theater.

---

# 15. EVIDENCE-FIRST UI

The product's visual hierarchy must generally be:

```text
SOURCE EVIDENCE
   ↓
EXTRACTED FACT
   ↓
MODEL OUTPUT
   ↓
RULE RESULT
   ↓
INFERENCE
   ↓
HUMAN ACTION
```

Evidence must visually outrank decoration.

When showing a finding, always provide an obvious path to the source artifact.

---

# 16. DOCUMENT VIEWER

The document viewer must support:

- neutral/light evidence canvas
- zoom
- pan
- reset view
- readable receipt rendering
- overlay bounding boxes
- hover synchronization
- confidence indication
- extracted-value panel

For a selected OCR field:

```text
RIGHT PANEL → click value
        ↓
LEFT DOCUMENT → highlight source bbox
```

The viewer must not hide the original document behind a modal if inline inspection is possible.

Low-confidence fields should use an amber/dashed treatment where appropriate.

---

# 17. VISUAL FORENSICS VIEWER

The visual comparison screen must make the visual evidence understandable.

Layout:

```text
CURRENT CLAIM PHOTO        HISTORICAL CANDIDATE
        │                         │
        └──── correspondence ────┘
```

Show:

- contract/source metadata
- capture date
- location
- SSCD similarity
- SIFT/RANSAC correspondence evidence
- match confidence
- provenance

Provide interactions such as:

- split/curtain comparison
- toggle correspondence vectors
- zoom
- reset
- metadata inspection

Do not overwhelm the user with raw embedding dimensions.

---

# 18. GEOSPATIAL VIEW

The map is an investigation tool.

It must support:

- drain centerline
- chainage/stationing
- work reach
- disposal site
- relevant GPS/trip path
- selected evidence point
- spatial exceptions

Interactions should synchronize with the rest of the workspace.

Example:

```text
click PHOTO P-003
   ↓
map focuses on P-003
   ↓
finding inspector loads spatial finding
```

Map markers must have semantic meaning.

Do not use decorative map layers.

---

# 19. FINDING INSPECTOR

Every finding card should answer:

### WHAT?

A concise statement.

### EVIDENCE?

Which artifacts support it?

### FACT?

What was directly observed/extracted?

### MODEL?

What did ML produce?

### RULE?

What deterministic check was applied?

### INFERENCE?

What relationship did the system derive?

### UNCERTAINTY?

What is missing/uncertain?

### ACTION?

What should the auditor inspect or do?

A finding should be understandable without reading the backend implementation.

---

# 20. COGNITIVE FORCING FUNCTION

The UI includes a review gate to reduce automation bias.

The implementation may track:

```text
inspectedItems
elapsedDwellSeconds
```

and maintain mandatory evidence-inspection steps.

However:

- do not fake inspection
- do not silently auto-complete checkboxes
- do not make the user wait merely for visual drama
- do not hard-code a dwell rule without the current approved business specification

If the current product spec requires dwell/checklist gating, implement it transparently.

Show:

```text
Inspection Gate
2 / 3 evidence items verified
Dwell: 8s / 12s
```

Only unlock adjudication when the configured gate is actually satisfied.

---

# 21. ADJUDICATION

Possible human actions:

```text
AFFIRM FINDING
REQUEST RESCAN / CLARIFICATION
MANUAL OVERRIDE
```

Buttons must communicate that the final decision belongs to the human reviewer.

Do not call the action:

```text
EXECUTE FRAUD
```

Do not make payment freezing an autonomous AI action.

---

# 22. OVERRIDE DRAWER

The override form should collect structured justification.

Potential categories from the current product specification:

```text
EXTRACTION_ERROR_OCR
EMERGENCY_PROCUREMENT_WAIVER
APPROVED_DETOUR_CONGESTION
MATERIAL_COMPACTION_VARIANCE
```

Requirements:

- category
- justification
- counter-evidence attachment when required
- validation
- confirmation
- permanent review history

The UI should show that an override creates an audit event.

---

# 23. APPLICATION STATE MACHINE

Every asynchronous view must explicitly support:

```text
IDLE
LOADING
PROCESSING
READY
EMPTY
PARTIAL
INCONCLUSIVE
ERROR
RETRYING
TECHNICAL_ABSTENTION
REVIEW_REQUIRED
COMPLETED
```

Never implement only the happy path.

## Loading

Use layout-preserving skeletons.

## Empty

Explain:

- why there is no data
- what the user should do next

## Error

Explain:

- what failed
- what remains available
- recovery action

## Technical abstention

Use neutral language.

Example:

```text
OCR unavailable
No adverse finding generated.
Rescan or retry is recommended.
```

---

# 24. DEMO MODE

Implement a deterministic demo mode.

Demo mode must:

- use known fixtures
- be resettable
- not depend on fragile live APIs
- preserve the real interaction flow
- clearly label synthetic/fixture data
- avoid fake claims about real production usage

Recommended behavior:

```text
DEMO FIXTURE
Synthetic / Controlled Benchmark
```

Use a reliable reset action.

Do not clear unrelated browser/application state unless explicitly required.

---

# 25. RESPONSIVE STRATEGY

Primary target:

**desktop investigation workstation**

Optimize for:

- 1440×900
- 1600×900
- 1920×1080

Desktop information density is intentional.

Still support graceful narrowing.

Do not break the investigation workspace with uncontrolled horizontal overflow.

For desktop:

- evidence tree remains visible
- inspector remains visible
- central canvas receives most available width

For narrow screens:

- preserve task order
- use deliberate stacking or route changes
- do not simply let three fixed columns collapse into unreadable content

---

# 26. PERFORMANCE RULES

Prioritize stable rendering.

Animate only:

- transform
- opacity

Avoid continuous animation of:

- width
- height
- margin
- padding
- layout geometry
- full-screen blur/filter effects

Do not create animations that interfere with evidence inspection.

Use:

- lazy image loading
- fixed image aspect ratios
- reserved layout space
- memoized expensive components where measured necessary
- virtualization only where actual list size requires it

Performance problems must be diagnosed with measurement, not assumed.

---

# 27. ACCESSIBILITY

Minimum expectations:

- keyboard navigation
- visible focus
- semantic buttons/links
- accessible dialogs
- accessible tabs
- tooltip support where needed
- readable contrast
- color-independent state
- reduced-motion support where appropriate
- aria labels for icon-only controls

Never communicate:

```text red = bad
green = good
```

without text/icon semantics.

---

# 28. FILE ARCHITECTURE

Preferred frontend structure:

```text
frontend/
├── app/
│   ├── layout.tsx
│   ├── page.tsx
│   └── workspace/
│       └── page.tsx
│
├── components/
│   ├── ui/
│   ├── workspace/
│   ├── canvas/
│   ├── inspector/
│   ├── telemetry/
│   └── evidence/
│
├── lib/
│   ├── demo/
│   ├── api/
│   ├── state/
│   └── utils.ts
│
├── public/
│   ├── artifacts/
│   └── geojson/
│
├── DESIGN.md
└── this-instruction-file
```

Do not create dozens of tiny files for trivial fragments.

Keep related subcomponents together until separation materially improves comprehension or reuse.

---

# 29. DATA CONTRACTS FOR UI

UI components must consume typed domain objects.

Examples:

```ts
type EpistemicTier =
  | "FACT"
  | "MODEL_OUTPUT"
  | "RULE_RESULT"
  | "INFERENCE"
  | "RECOMMENDATION";

type SystemState =
  | "idle"
  | "loading"
  | "processing"
  | "ready"
  | "empty"
  | "partial"
  | "inconclusive"
  | "error"
  | "retrying"
  | "technical_abstention"
  | "review_required"
  | "completed";

type FindingSeverity =
  | "CRITICAL"
  | "HIGH"
  | "MEDIUM"
  | "INCONCLUSIVE"
  | "CLEAN";
```

Avoid stringly-typed UI logic scattered across components.

---

# 30. NO UI-ONLY BUSINESS LOGIC

Do not embed audit rules directly into visual components.

Bad:

```text
if (gross - tare !== net) {
  showFraud();
}
```

Good:

```text
rule engine
    ↓
typed RuleResult
    ↓
Finding UI
```

The frontend renders results.

It does not independently invent audit conclusions.

---

# 31. SOURCE-OF-TRUTH RULE

The following are authoritative:

```text
PROJECT ARCHITECTURE
DESIGN.md
DOMAIN TYPES / API CONTRACTS
TESTS
```

AI suggestions are NOT authoritative.

Before changing the design system:

1. identify the existing token
2. identify the reason for change
3. make the smallest coherent change
4. propagate it consistently

Never introduce local visual overrides simply because they make one component look better.

---

# 32. AGENT BEHAVIOR — HOW TO CODE

## Never do this

> "Build the entire MuniAudit dashboard."

## Do this

Build one verified vertical slice at a time.

Recommended sequence:

```text
PHASE 0
inspect repository + design system

PHASE 1
app shell + global layout

PHASE 2
inbox / triage

PHASE 3
three-column forensic workspace

PHASE 4
document viewer

PHASE 5
visual comparison

PHASE 6
geospatial canvas

PHASE 7
finding inspector

PHASE 8
cognitive gate + override

PHASE 9
state/error/degraded handling

PHASE 10
visual polish + accessibility + performance

PHASE 11
demo hardening
```

Each phase must be independently testable.

---

# 33. BEFORE EVERY IMPLEMENTATION TASK

You must first state internally/briefly:

```text
CURRENT STATE
TARGET CHANGE
FILES TO MODIFY
FILES NOT TO MODIFY
DEPENDENCIES
ACCEPTANCE CRITERIA
```

Then implement.

Do not make unrelated refactors.

---

# 34. AFTER EVERY IMPLEMENTATION TASK

Run the appropriate checks:

```text
typecheck
lint
build
tests
browser verification where available
```

Then inspect the rendered result.

Do not assume compile success means UI success.

---

# 35. VISUAL QA CHECKLIST

Before marking UI work complete, verify:

### Domain

Does it look like a public-works forensic tool?

### Hierarchy

Is the important evidence visually dominant?

### Consistency

Are spacing, typography, borders, and colors token-consistent?

### Epistemic meaning

Can the user tell:

FACT
vs
MODEL
vs
RULE
vs
INFERENCE
vs
ACTION?

### States

Are loading/empty/error/inconclusive states implemented?

### Interaction

Can the user move from finding → evidence → calculation → review?

### Performance

Does the interface remain smooth?

### Accessibility

Can state be understood without color alone?

### Demo

Can the screen be understood quickly by a judge?

---

# 36. PRE-DEMO "SWAP TEST"

Replace the municipality/branding context mentally.

Ask:

> "Would this still look like a generic AI dashboard?"

If YES:

- strengthen domain-specific evidence patterns
- reduce generic KPI-card emphasis
- improve evidence visualization
- improve investigative workflow
- remove decorative AI patterns

The UI should feel purpose-built for MuniAudit.

---

# 37. "AI SMELL TEST"

Before completion ask:

Would a human designer intentionally choose this?

If the answer is "the AI probably generated it because it was convenient," reconsider it.

Examples:

- random gradient
- huge meaningless metric
- generic globe graphic
- excessive rounded cards
- fake terminal
- glowing AI icon
- decorative chart
- random floating badge

Remove it.

---

# 38. REFERENCE USE

Visual references may be used for:

- information density
- evidence inspection patterns
- split-pane workspaces
- map interactions
- professional table behavior
- document review

Do not copy a commercial product's visual identity.

Use references to learn interaction patterns, then implement a distinct MuniAudit visual language.

---

# 39. MOTION RULES

Animation should communicate one of:

- state change
- spatial relationship
- causality
- focus
- feedback

Examples:

GOOD:
finding opens → related evidence highlights

GOOD:
click evidence → map gently focuses

GOOD:
document field → bbox highlight

BAD:
constant glowing background

BAD:
floating cards everywhere

BAD:
animation on every button for no reason

---

# 40. AWS UI PROVENANCE

The application may expose cloud-processing status, but only when the status is backed by actual application state.

Preferred:

```text
Evidence stored
Processing queued
OCR complete
Visual analysis complete
Spatial checks complete
Review ready
```

Do not fabricate service latency/cost/throughput.

If a cloud service is unavailable:

```text
TECHNICAL ABSTENTION
```

not:

```text
CONTRACTOR ISSUE
```

---

# 41. BEDROCK UI RULE

If Bedrock is used:

It may generate:

- concise audit summaries
- human-readable explanations from validated structured data

It must NOT become:

- the source of audit facts
- the rule engine
- the final fraud classifier
- the authority that overrides deterministic findings

The UI should make clear that summary language is generated from validated structured findings.

---

# 42. DEMO FIXTURE HONESTY

Fixture data must be marked.

Good:

```text
DEMO FIXTURE
Synthetic / Controlled Benchmark
```

Bad:

```text
LIVE BENGALURU MUNICIPAL DATA
```

unless it actually is.

Do not fabricate official-looking contract names, government approvals, or production status.

---

# 43. DO NOT CLAIM LEGAL STATUS THROUGH UI

Avoid UI copy such as:

- Court-admissible
- legally proven
- criminally established
- fraud confirmed

unless the project owner has independently verified and approved the specific legal claim.

Safer UI language:

- Evidence package
- Source artifact
- Integrity record
- Substantive inconsistency
- Review required
- Technical abstention
- Human adjudication

---

# 44. IMPORTANT UI CONSTRAINTS FOR THE FLAGSHIP WORKSPACE

The core workspace must preserve:

```text
LEFT:
evidence navigation

CENTER:
primary evidence

RIGHT:
explanation + action

BOTTOM:
pipeline / provenance
```

Do not collapse this into a conventional KPI dashboard.

---

# 45. IMPLEMENTATION ACCEPTANCE CRITERIA

A frontend task is complete only when:

1. It follows `DESIGN.md`.
2. It reuses approved local primitives.
3. It introduces no uncontrolled tokens.
4. It supports relevant non-happy-path states.
5. It preserves evidence traceability.
6. It uses accessible semantics.
7. It does not fabricate system outputs.
8. It does not move audit logic into the UI.
9. It passes typecheck/lint/build/tests relevant to the change.
10. It has been visually inspected in the browser.
11. It does not introduce unnecessary dependencies.
12. It does not break the existing workspace.

---

# 46. WHEN ASKED TO "MAKE IT LOOK BETTER"

Do NOT immediately add:

- gradients
- animation
- glow
- more cards
- larger typography
- extra charts

Instead inspect, in order:

1. information hierarchy
2. spacing consistency
3. alignment
4. typography
5. evidence prominence
6. visual contrast
7. component consistency
8. interaction feedback
9. states
10. restrained motion

Make the smallest change that materially improves the experience.

---

# 47. WHEN SOMETHING IS UNCLEAR

Do not invent business meaning.

Use this approach:

```text
KNOWN
UNKNOWN
CURRENT ASSUMPTION
MINIMUM SAFE IMPLEMENTATION
```

If implementation can proceed without changing the business contract, use a safe placeholder.

If the ambiguity changes audit meaning, stop and request clarification rather than inventing a rule.

---

# 48. FINAL AGENT OPERATING LOOP

For every feature:

```text
READ
 ↓
UNDERSTAND
 ↓
PLAN
 ↓
IMPLEMENT
 ↓
TYPECHECK
 ↓
TEST
 ↓
RENDER
 ↓
VISUAL INSPECT
 ↓
FIX
 ↓
RENDER AGAIN
 ↓
REPORT
```

Do not skip the browser/render inspection step for visual work.

---

# 49. FINAL COMMANDMENT

Build MuniAudit-AI as if a professional municipal auditor will use it tomorrow.

The interface must feel:

**calm**
**precise**
**evidence-first**
**technical**
**credible**
**fast**
**deliberate**
**human-controlled**

It must not feel:

**AI-generated**
**decorative**
**generic**
**over-animated**
**accusatory**
**fake**
**prototype-like**

The target is not:

> "Wow, lots of AI UI effects."

The target is:

> **"I immediately understand the evidence, why this case needs review, and exactly where the system got that conclusion."**

---

# 50. FINAL IMPLEMENTATION MANTRA

```text
EVIDENCE OVER DECORATION
CLARITY OVER NOVELTY
TRACEABILITY OVER MAGIC
REAL DATA OVER FAKE TELEMETRY
HUMAN CONTROL OVER AUTOMATION
CONSISTENCY OVER ONE-OFF BEAUTY
POLISH OVER COMPLEXITY
```
