# **Ultimate Antigravity Engineering Intelligence & Governance System for MuniAudit-AI**

## **1\. Executive Summary & Antigravity Capability Verification**

Autonomous AI coding agents operating without strict governance suffer from context drift, architectural divergence, hallucinated dependencies, and the silent modification of critical design decisions. In complex multimodal applications like **MuniAudit-AI**, an unconstrained agent will treat civil engineering constraints as negotiable suggestions, invent cloud services, overwrite working database migrations, or replace calibrated evidence fusion with arbitrary machine learning heuristics.

&nbsp;

This system establishes an authoritative operational framework that converts Google Antigravity (powered by Gemini 3.8) from an autocomplete assistant into a disciplined, self-verifying senior software engineer.

&nbsp;

### **Official Antigravity Architecture & Capabilities Matrix**

The following table reflects the verified operational capabilities and constraints of the Google Antigravity runtime environment.

&nbsp;

| Capability / Primitive | Official Architecture / Format | Current Status | Hard Operational Limits | Practical Application in MuniAudit-AI |
| :---- | :---- | :---- | :---- | :---- |
| **Agent Rules** | Markdown files in .agents/rules/\*.md with YAML frontmatter. | Native / Fully Supported | 12,000 characters per rule file. Auto-loaded based on trigger (always-on, glob match, or @mention). | Enforce immutable project invariants (such as physical mass-balance equations, UI design tokens, and AWS service boundaries). |
| **Agent Skills** | Directory bundles in .agents/skills/\<name\>/SKILL.md containing metadata and optional scripts. | Native / Standardized | Progressive disclosure: startup loads only name and description. Full body loads on semantic match. | On-demand execution protocols (e.g., executing test suites, running ML evaluation benchmarks, verifying spatial schemas). |
| **Agent Hooks** | JSON schema in .agents/hooks.json intercepting lifecycle events. | Native / Fully Supported | Handlers run synchronously; 6-minute absolute timeout; non-zero exits block execution. | Intercepts PreToolUse and PostToolUse to block destructive commands, scan for secrets, and enforce clean Git trees. |
| **Specialized Subagents** | Configured via .agents/agents/\*.md or invoke\_subagent calls. | Native / Supported | Subagents run isolated context loops; cannot mutate parent state without returning structured artifacts. | Dedicated reviewers (e.g., architecture-reviewer, security-auditor, ui-qa-specialist) running independent verification. |
| **Browser Agent** | Chrome extension driving headless/interactive browser tasks. | Native / Supported | Restricted by URL allowlist; requires local display server or virtual framebuffer. | End-to-end UI verification, split-canvas inspection testing, and automated visual regression checks. |
| **Context Management** | Dynamic context compilation with token compression and file loading. | Native / Multi-tier | Large context window (\~1M tokens), but reasoning quality degrades past 200k active tokens. | Multi-tier context injection: Global rules, project manifests, task contracts, and explicit file reads. |
| **Tool Execution** | Bash/Zsh subprocesses with permission tiers (auto, confirm, deny). | Native / Supported | Subprocess environment inherits active terminal PATH; requires absolute paths in headless configurations. | Executes Python test runners, Alembic migrations, ONNX runtime benchmarks, and Git checkpointing. |

## **2\. Autonomous Coding-Agent Failure Model**

To ensure reliability, the governance architecture defines explicit countermeasures for twenty-eight documented failure modes observed in autonomous coding agents:

&nbsp;

| \# | Agent Failure Mode | Root Cause Mechanism | Preventive Control | Runtime Detection Method | Recovery & Escalation Protocol |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **1** | **Context Drift** | Conversational history pushes initial requirements out of effective attention. | Keep conversational history short; bind authoritative context to local repository markdown files. | Pre-flight check compares task goals against CORE\_CONTEXT.md. | Re-ground session by reading CORE\_CONTEXT.md and clearing conversational memory. |
| **2** | **Forgotten Constraints** | Prompt instructions are treated as transient preferences rather than hard rules. | Embed non-negotiable rules in .agents/rules/muniaudit-engineering.md marked as always-on. | Hook intercepts tool execution if hard-coded constraints are violated. | Abort tool call immediately; display rule violation narrative in session log. |
| **3** | **Architectural Drift** | Agent selects familiar generic web patterns over project-specific architectures. | Architecture Decision Records (ADRs) in docs/adr/\*.md with explicit architectural boundaries. | Linting hook compares modified module imports against allowed architecture layers. | Halt task; generate structural deviation alert; require human confirmation. |
| **4** | **Scope Creep** | Agent attempts to resolve unrequested secondary bugs observed while reading code. | Restrict allowed file modifications to an explicit whitelist defined in the task contract. | Pre-flight inspection checks the proposed diff against the declared task scope. | Revert unrequested file modifications using git checkout \-- \<file\>. |
| **5** | **Neighboring-File Corruption** | Overlapping edits introduce syntax errors or broken imports in untouched files. | Run full compiler/linter checks across all staged files prior to task completion. | Automated PostToolUse execution of npm run typecheck or mypy. | Revert uncommitted changes in neighboring files; isolate edits to target file. |
| **6** | **Premature Abstraction** | Agent constructs unnecessary generic factories, wrappers, and multi-tenant layers. | Explicit rule mandate: "Three concrete instances required before creating an abstraction." | Code review subagent inspects AST for single-use abstractions and interfaces. | Refactor code back to inline, readable procedural or functional blocks. |
| **7** | **Hallucinated Dependencies** | Agent imports non-existent libraries or packages with plausible names. | Explicit package manifest locks (poetry.lock, package-lock.json). | Pre-flight check scans package imports against the installed package database. | Block pip install or npm install unless explicitly approved in the task contract. |
| **8** | **Incorrect API Usage** | Agent relies on outdated training data for rapidly evolving third-party SDKs. | Require the agent to consult local cached documentation or run test queries first. | Unit tests verify API client responses against mock schemas. | Strike 1 debugging protocol: verify current API signatures against official documentation. |
| **9** | **Outdated Documentation** | Agent references legacy library syntax or deprecated AWS SDK patterns. | Maintain an authoritative docs/api-contracts/ directory containing exact schemas. | Schema validator rejects responses lacking required current-generation fields. | Update local API contract file; re-run client generation. |
| **10** | **Over-Trust in AI Code** | Agent assumes previously generated code is fully functional without testing. | Enforce mandatory verification: every implementation task must be followed by tests. | Test runner hook checks whether new code paths have corresponding executed tests. | Require execution of unit tests with terminal output logging. |
| **11** | **Endless Retry Loops** | Agent repeats identical failed edits while trying to fix an error message. | Three-strike rule enforced by a session hook tracking command signatures. | Hook counts identical consecutive failing test invocations. | Terminate execution after Strike 3; dump error diagnostics to FAILED\_APPROACHES.md. |
| **12** | **Test Gaming** | Agent alters assertions (assert True) or removes tests to achieve a passing build. | Lock test directory permissions; changes to tests/ require dedicated test tasks. | Git diff check detects deletions or modifications in test assertion blocks. | Immediate rejection of git commit; restore test file from HEAD. |
| **13** | **False Completion** | Agent reports a feature is "Done" when code is written but untested or broken. | Definition of Done (DoD) validation script verifying tests, types, and git diff. | Task exit script verifies that TASK\_CONTRACT.md criteria have passed. | Block completion state transition; require missing verification output. |
| **14** | **Silently Skipped Requirements** | Agent ignores difficult boundary conditions mentioned in long prompt paragraphs. | Structured task contracts with granular checkboxes for each acceptance criterion. | Post-flight auditor checks off criteria one by one against test assertions. | Keep task in IN\_PROGRESS status until all checklist criteria pass. |
| **15** | **Destructive Commands** | Agent runs rm \-rf, git reset \--hard, or drops database tables during debugging. | Hook script blocks destructive commands by regex filtering tool inputs. | Shell interceptor scans run\_command arguments for dangerous operations. | Intercept and drop command; notify user with an explicit security warning. |
| **16** | **Inconsistent Naming** | Agent invents inconsistent names (dossier\_id vs claimId vs audit\_case\_ref). | Central data dictionary in docs/DATA\_DICTIONARY.md enforced via types. | Static analysis checks variable and column names against schema definitions. | Renaming refactor applied across the task diff before final commit. |
| **17** | **Duplicate Implementations** | Agent writes a duplicate utility function because it did not find the existing one. | Mandate global utility index check in src/utils/ prior to writing helpers. | Subagent inspects codebase for functional duplicates using symbol lookups. | Remove duplicate; replace calls with the authoritative shared utility. |
| **18** | **State Inconsistency** | PROJECT\_STATE.md claims tests are green, but local working tree has failing code. | Machine-readable PROJECT\_STATE.json linked to specific Git commit SHAs. | State validation script checks current Git commit against last\_verified\_commit. | Mark state as STALE; trigger automated background verification suite. |
| **19** | **Stale Assumptions** | Agent assumes a database column exists when a recent migration removed it. | Always read active database migration files (alembic/versions/) before writing SQL. | Database integration tests run against an ephemeral test instance. | Update local query to match current schema; update dependency documentation. |
| **20** | **Hidden Technical Debt** | Agent uses temporary mocks or @ts-ignore to bypass build errors quickly. | Zero-warning policy: linters reject build if suppressions are added. | Pre-commit hook scans diff for TODO, FIXME, @ts-ignore, and \# type: ignore. | Require explicit architectural exception approval before allowing suppression. |
| **21** | **Local Fix, Global Breakage** | Modifying a shared utility resolves one test but breaks three downstream modules. | Full test suite execution required before merging any shared utility modification. | Continuous test runner runs the full test suite on shared file modifications. | Rollback local edit; re-implement using an overload or backwards-compatible parameter. |
| **22** | **Blind Interface Changes** | Changing a function signature without updating downstream caller files. | Strict TypeScript / Python type checking across the entire project tree. | npm run typecheck or mypy src/ executed after any public interface change. | Update all downstream callers identified by compiler errors. |
| **23** | **Repeating Failed Approaches** | Agent tries an approach that failed two days ago because conversational context was lost. | Durable repository memory in FAILED\_APPROACHES.md indexing rejected attempts. | Pre-flight protocol checks task against entries in FAILED\_APPROACHES.md. | Alert agent: "Approach previously failed due to \[reason\]. Select alternative." |
| **24** | **Benchmark Misinterpretation** | Agent claims model achieved 98% accuracy on real data using synthetic evaluation. | Strict labeling taxonomy: separate synthetic sensitivity from real performance. | Metric reporting script validates data source labels before generating charts. | Correct evaluation text: "Achieved 98% sensitivity on synthetic perturbation suite." |
| **25** | **Data Conflation** | Agent treats procedurally generated weighbridge slips as authentic municipal records. | Enforce evidentiary tags: REAL\_MUNICIPAL, DERIVED, SYNTHETIC, SIMULATED. | Data loader verifies that all synthetic records carry metadata watermarks. | Strip false authenticity claims from documentation and generated dossiers. |
| **26** | **UI Regression** | Agent modifies layout styling, breaking responsive viewports or design tokens. | Enforce DESIGN.md tokens; automated visual verification via Browser Agent. | Browser agent captures screenshots before and after edits; flags element shifts. | Revert CSS diff; restore alignment using standardized design tokens. |
| **27** | **Infrastructure Drift** | Agent adds a cloud resource to code without updating deployment templates. | Infrastructure-as-Code (IaC) parity: all resources defined in App Runner/Terraform. | Build validation script checks application service calls against the cloud topology. | Update IaC template to reflect required resource, or refactor code to eliminate it. |
| **28** | **Security Regression** | Agent disables CORS, CSRF, or authentication guards to make an API test pass. | Security tests are immutable; authentication bypasses cause immediate failure. | Automated security test suite (pytest tests/security/) run on every PR. | Immediate rollback of insecure commit; escalate to human reviewer. |

## **3\. Project Brain Architecture**

Conversational context is temporary and degrades as tokens accumulate. The durable memory of MuniAudit-AI must reside entirely within version-controlled repository artifacts. The Project Brain consists of ten authoritative files, each with strict ownership, update cadences, and staleness detection mechanisms.

&nbsp;

\+----------------------------------------------------------------------------------------------------+

|                                    PROJECT BRAIN ARCHITECTURE                                      |

\+--------------------------+-----------------------+-------------------------+-----------------------+

| Repository Artifact      | Operational Scope     | Update Cadence          | Staleness Detection   |

\+--------------------------+-----------------------+-------------------------+-----------------------+

| CORE\_CONTEXT.md          | Invariants & Domain   | Immutable / Rare        | Hash check in commit  |

| PROJECT\_STATE.json       | Machine State Machine | Every Verified Step     | Commit SHA comparison |

| ARCHITECTURE.md          | Subsystem Boundaries  | Milestones only         | Interface drift audit |

| TASK\_CONTRACT.md         | Active Task Agreement | Per Task Lifecycle      | Session ID check      |

| AGENT\_RESPONSE\_CONTRACT  | Work Output Audit     | Per Completed Task      | Pre-commit gate check |

| FAILED\_APPROACHES.md     | Negative Memory Bank  | On Every Strike 3       | Keyword scan in plan  |

| DEPENDENCY\_GRAPH.json    | Component Linkages    | Auto-generated (build)  | AST import comparison |

| DESIGN.md                | UI & Token Specs      | Design freeze milestone | CSS class linting     |

| AGENT\_ESCALATION.md      | Human Approval Queue  | On Blocked Triggers     | Unresolved item count |

| CHANGELOG.md             | Historical Milestones | On Every State Advance  | Git tag comparison    |

\+--------------------------+-----------------------+-------------------------+-----------------------+

&nbsp;

### **Knowledge Artifact Specifications**

1. CORE\_CONTEXT.md  
2. 

   * **Purpose:** Defines the problem statement, core purpose, non-negotiable boundaries, and high-level architecture.  
   * &nbsp;  
   * **Owner:** Human Technical Lead.  
   * &nbsp;  
   * **Update Cadence:** Locked at project initialization; modified only upon unanimous team consent.  
   * &nbsp;  
   * **Modification Permission:** Read-only for AI agent.  
   * &nbsp;  
   * **Staleness Detection:** Pre-flight hook asserts that the file SHA-256 matches the baseline digest stored in .agents/manifest.json.  
   * &nbsp;  
3. PROJECT\_STATE.json  
4. 

   * **Purpose:** Single machine-readable source of truth tracking current project phase, completed features, active blockers, and passing test counts.  
   * &nbsp;  
   * **Owner:** AI Agent (Antigravity) with programmatic schema validation.  
   * &nbsp;  
   * **Update Cadence:** Updated after every verified task completion.  
   * &nbsp;  
   * **Modification Permission:** Agent-modifiable via structured script (update\_state.py).  
   * &nbsp;  
   * **Staleness Detection:** Hook compares last\_verified\_commit inside the JSON against the output of git rev-parse HEAD. If they diverge by more than one commit without an update, state is flagged as STALE.  
   * &nbsp;  
5. TASK\_CONTRACT.md  
6. 

   * **Purpose:** Ephemeral agreement defining the current task objective, affected files, forbidden files, architectural boundaries, and test acceptance criteria.  
   * &nbsp;  
   * **Owner:** AI Agent (drafted) \+ Human Engineer (approved).  
   * &nbsp;  
   * **Update Cadence:** Created at the start of every task; archived upon task completion.  
   * &nbsp;  
   * **Modification Permission:** Frozen during task execution.  
   * &nbsp;  
7. FAILED\_APPROACHES.md  
8. 

   * **Purpose:** Institutional memory recording every failed implementation strategy, the technical reason for failure, and the forbidden pattern.  
   * &nbsp;  
   * **Owner:** AI Agent (appends diagnostics).  
   * &nbsp;  
   * **Update Cadence:** Updated whenever a debugging cycle reaches Strike 3 or an approach is abandoned.  
   * &nbsp;  
   * **Modification Permission:** Append-only for AI agent.  
   * &nbsp;  
   * **Staleness Detection:** Verified against task keywords during pre-flight checks.  
   * &nbsp;

## **4\. Formal Project State Machine**

To prevent the agent from performing downstream tasks (such as writing frontend visual components) before upstream dependencies (such as the database schema or core ML extractors) are tested and stable, the project operates under a formal finite state machine:

&nbsp;

\+----------------------------------------------------------------------------------------------------+

|                                    PROJECT STATE MACHINE FLOW                                      |

\+----------------------------------------------------------------------------------------------------+

&nbsp;\[ 01\_PROBLEM\_LOCKED \]

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;▼

&nbsp;\[ 02\_DATA\_LOCKED \]

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;▼

&nbsp;\[ 03\_ARCHITECTURE\_LOCKED \]

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;▼

&nbsp;\[ 04\_SCAFFOLDING\_READY \]

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;▼

&nbsp;\[ 05\_DATA\_PIPELINE \]

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;▼

&nbsp;\[ 06\_CORE\_ML\_IMPLEMENTATION \]

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;▼

&nbsp;\[ 07\_DETERMINISTIC\_RULES \]

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;▼

&nbsp;\[ 08\_EVIDENCE\_FUSION \]

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;▼

&nbsp;\[ 09\_API\_AND\_SERVICES \]

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;▼

&nbsp;\[ 10\_FRONTEND\_WORKSPACE \]

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;▼

&nbsp;\[ 11\_EVALUATION\_AND\_BENCHMARK \]

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;▼

&nbsp;\[ 12\_DEMO\_HARDENING \]

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;▼

&nbsp;\[ 13\_SUBMISSION\_FROZEN \]

&nbsp;

### **State Definitions and Invariants**

| State Name | Allowed Actions | Forbidden Actions | Required Artifacts | Exit Criteria |
| :---- | :---- | :---- | :---- | :---- |
| **01\_PROBLEM\_LOCKED** | Draft problem specs, review audit literature, map operational personas. | Writing application code, installing UI dependencies, creating database tables. | CORE\_CONTEXT.md, docs/PROBLEM\_STATEMENT.md | Human approval of core problem statement and scope boundaries. |
| **02\_DATA\_LOCKED** | Download public KMLs, fetch RDD2022 image samples, generate synthetic slips. | Training deep learning models, configuring cloud deployment pipelines. | data/raw/, data/schemas/, DATA\_DICTIONARY.md | Successful execution of data schema validation script across all inputs. |
| **03\_ARCHITECTURE\_LOCKED** | Author ADRs, lock API contracts, draft component specifications. | Modifying core architectural boundaries, adding unapproved cloud services. | ARCHITECTURE.md, docs/adr/\*.md | All subsystem interfaces defined with strict Pydantic/TypeScript schemas. |
| **04\_SCAFFOLDING\_READY** | Initialize git repository, configure linting, setup Docker Compose, install test harnesses. | Implementing business logic, executing exploratory data transformations. | docker-compose.yml, pyproject.toml, .agents/ | pytest and npm test execute and pass on empty sample tests. |
| **05\_DATA\_PIPELINE** | Implement KML parsers, receipt generators, dataset loaders, coordinate normalizers. | Building frontend UI views, running visual copy-detection queries. | src/data/, tests/test\_data\_pipeline.py | 100% of benchmark data files ingested and validated without runtime errors. |
| **06\_CORE\_ML\_IMPLEMENTATION** | Package Meta SSCD ONNX model, implement Textract/PaddleOCR wrappers. | Building end-to-end billing endpoints, writing UI components. | src/ml/, tests/test\_ml\_components.py | SSCD embedding extraction verified on CPU ($\< 90\\text{ ms}$); OCR extracts test vouchers. |
| **07\_DETERMINISTIC\_RULES** | Implement physical mass-balance checks, Haversine velocity rules, Vahan class lookups. | Writing generative AI prompt templates, modifying database schemas. | src/rules/, tests/test\_deterministic\_rules.py | 100% of rule unit tests pass across edge cases ($\\Delta \= 0$, $v \> 90\\text{ km/h}$). |
| **08\_EVIDENCE\_FUSION** | Implement Subjective Logic consensus operator ($\\oplus$), ECS, and ARPI score calculators. | Connecting live frontend components, modifying core invariant rules. | src/fusion/, tests/test\_fusion\_math.py | Mathematical verification of opinion spaces; zero division errors on full conflict. |
| **09\_API\_AND\_SERVICES** | Implement FastAPI endpoints, SQS background worker loops, S3 presigned handlers. | Modifying analytical fusion algorithms, changing visual feature dimensions. | src/api/, src/workers/, tests/test\_api.py | Integration tests pass: upload dossier $\\to$ process $\\to$ inspect findings. |
| **10\_FRONTEND\_WORKSPACE** | Implement Next.js 3-column workspace, Leaflet map, SIFT canvas, OCR viewer. | Altering backend validation logic, modifying database relational tables. | frontend/, DESIGN.md, Playwright tests | UI components pass visual QA; zero hydration errors; demo hotkey operational. |
| **11\_EVALUATION\_AND\_BENCHMARK** | Run N=250 benchmark, calculate mAP, CER, and ECE metrics, generate precision curves. | Changing model architectures, tweaking test parameters to game results. | results/benchmark\_metrics.json, docs/EVALUATION.md | Full benchmark run completes; results logged with cryptographic data hashes. |
| **12\_DEMO\_HARDENING** | Rehearse 3-minute scripted sequence, test offline demo mode, optimize query latency. | Adding new product features, upgrading package dependencies. | demo/fixtures/, DEMO\_PLAYBOOK.md | 5 consecutive clean runs of the 180-second demo script with zero errors. |
| **13\_SUBMISSION\_FROZEN** | Build production containers, freeze git tags, export documentation, archive codebase. | Any code modification without explicit emergency human override token. | git tag v1.0.0-final, compiled submission ZIP | Working branch clean; CI/CD pipeline green; documentation complete. |

## **5\. Continuous Situational Awareness Protocol**

To prevent the agent from operating blindly, Antigravity must execute an automated situational grounding routine before processing any prompt. Rather than consuming context by rereading every file in the repository, the agent applies an efficient **Layered Context Hierarchy**:

&nbsp;

\+----------------------------------------------------------------------------------------------------+

|                                    LAYERED CONTEXT COMPILATION                                     |

\+----------------------------------------------------------------------------------------------------+

&nbsp;Level 1: Global Invariants (\~1,500 tokens)

&nbsp;&nbsp;&nbsp;└── .agents/rules/muniaudit-engineering.md (Always-on identity, non-negotiable rules)

&nbsp;Level 2: Project Essence (\~2,000 tokens)

&nbsp;&nbsp;&nbsp;└── CORE\_CONTEXT.md (Problem definition, locked architecture, domain boundaries)

&nbsp;Level 3: Active State (\~800 tokens)

&nbsp;&nbsp;&nbsp;└── PROJECT\_STATE.json (Current phase, active blockers, verified commit SHA)

&nbsp;Level 4: Subsystem Context (\~3,000 tokens)

&nbsp;&nbsp;&nbsp;└── Loaded dynamically based on task type (e.g., DESIGN.md for UI; schemas for DB)

&nbsp;Level 5: Active Task Contract (\~1,500 tokens)

&nbsp;&nbsp;&nbsp;└── TASK\_CONTRACT.md (Objective, affected files, acceptance criteria, boundaries)

&nbsp;Level 6: Atomic Source Code (\~4,000 to 12,000 tokens)

&nbsp;&nbsp;&nbsp;└── The exact target implementation files and their immediate test counterparts

&nbsp;

### **Situational Awareness Execution Loop**

1. **Verify State:** Read PROJECT\_STATE.json. Confirm the current phase permits the requested task.  
2. &nbsp;  
3. **Verify Freshness:** Execute git status \-s and git rev-parse HEAD. Confirm the working directory is clean and matches last\_verified\_commit.  
4. &nbsp;  
5. **Verify Constraints:** Check CORE\_CONTEXT.md and active ADRs for invariants governing the affected modules.  
6. &nbsp;  
7. **Scan Negative Memory:** Check FAILED\_APPROACHES.md to ensure the planned implementation does not repeat a documented failed attempt.  
8. &nbsp;  
9. **Formulate Plan:** Draft TASK\_CONTRACT.md defining objective, target files, and definition of done.  
10. &nbsp;

## **6\. Pre-Flight and Post-Flight Protocols**

### **6.1 The Mandatory Pre-Flight Protocol**

Before modifying any file, the agent must output a concise Pre-Flight Declaration verifying nine structural criteria:

&nbsp;

### **PRE-FLIGHT VERIFICATION**

1. Active State: \[e.g., 07\_DETERMINISTIC\_RULES\] \-\> Task is permitted.  
2. &nbsp;  
3. Task Objective: Implement container bulk density invariant check in src/rules/mass\_envelope.py.  
4. &nbsp;  
5. Relevant Requirement: REQ-PHYS-002 (Mass \<= Bed Volume \* 1.90 t/m³).  
6. &nbsp;  
7. Governing Architecture: ARCHITECTURE.md Section 5 (Physical Mass-Envelope Invariant).  
8. &nbsp;  
9. Files Allowed to Modify:  
10. 

    * src/rules/mass\_envelope.py  
    * &nbsp;  
    * tests/test\_mass\_envelope.py  
    * &nbsp;  
11. Files Explicitly Forbidden:  
12. 

    * alembic/\* (Database schema is frozen)  
    * &nbsp;  
    * src/api/\* (Interface changes forbidden in this task)  
    * &nbsp;  
13. Negative Memory Check: Checked FAILED\_APPROACHES.md. Approach does not use hardcoded density scalars.  
14. &nbsp;  
15. Smallest Safe Change: Pure function taking (net\_mass\_kg, bed\_volume\_m3) returning boolean and residual.  
16. &nbsp;  
17. Verification Method: Execute pytest tests/test\_mass\_envelope.py \-v.  
18. &nbsp;

### **6.2 The Mandatory Post-Flight Protocol**

Immediately following code modifications, the agent must execute its verification pipeline and output an immutable status summary:

&nbsp;

### **POST-FLIGHT VERIFICATION**

1. Compilation / Types: npm run typecheck or mypy src/ \-\> 0 errors.  
2. &nbsp;  
3. Lint / Formatting: ruff check src/ or eslint \-\> Clean.  
4. &nbsp;  
5. Unit Test Execution: pytest tests/test\_mass\_envelope.py \-\> 8 passed in 0.24s.  
6. &nbsp;  
7. Regression Check: pytest tests/ \-\> 64 passed, 0 failed.  
8. &nbsp;  
9. Scope Audit: git status \-s confirms ONLY allowed files were modified.  
10. &nbsp;  
11. Documentation Sync: Invariant equations in docs/RULES.md match code implementation.  
12. &nbsp;  
13. State Transition: Updated PROJECT\_STATE.json with new test count and commit hash.  
14. &nbsp;  
15. Git Checkpoint: Created atomic commit: feat(rules): implement physical container density envelope check.  
16. &nbsp;

## **7\. Agent Memory and the Negative-Learning Bank**

AI agents frequently forget failures that occurred earlier in an engineering cycle. If a specific library version, ONNX export flag, or spatial projection formula fails, the agent will often retry that exact failure mode when prompted by a different user session.

&nbsp;

### **The Negative Memory Protocol (**FAILED\_APPROACHES.md**)**

When an approach fails three consecutive verification attempts (Strike 3\) or is abandoned due to an architectural dead-end, the agent is required to write a diagnostic autopsy to FAILED\_APPROACHES.md.

&nbsp;

#### **Invariant Rules for Agent Memory:**

1. **Mandatory Query:** During the pre-flight protocol of every task, the agent must search FAILED\_APPROACHES.md using keywords matching the task components (e.g., pgvector, textract, sift, haversine).  
2. &nbsp;  
3. **Active Block:** If the agent's planned implementation matches an entry in FAILED\_APPROACHES.md, it must halt planning, log an explicit warning to the user, and switch to an alternative pattern.  
4. &nbsp;  
5. **Autopsy Schema:** Every autopsy must document:  
6. 

   * Approach attempted.  
   * &nbsp;  
   * Target component.  
   * &nbsp;  
   * Exact failure symptom or error output.  
   * &nbsp;  
   * Underlying technical mechanism causing the failure.  
   * &nbsp;  
   * Concrete alternative approach adopted.  
   * &nbsp;

## **8\. Architectural Self-Check Protocol**

The AI coding agent has **zero authority** to modify architectural boundaries, introduce new cloud services, or alter database schemas autonomously.

&nbsp;

\+----------------------------------------------------------------------------------------------------+

|                                  ARCHITECTURAL SELF-CHECK GATEWAY                                  |

\+----------------------------------------------------------------------------------------------------+

&nbsp;Proposed change touches:

&nbsp;&nbsp;&nbsp;├── Service boundary (e.g., adding an external API client)

&nbsp;&nbsp;&nbsp;├── Database schema (e.g., modifying an Alembic migration)

&nbsp;&nbsp;&nbsp;├── Cloud topology (e.g., introducing an unapproved AWS service)

&nbsp;&nbsp;&nbsp;└── Algorithmic paradigm (e.g., replacing Subjective Logic with deep neural fusion)

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;▼

&nbsp;\[ AUTOMATIC AGENT HALT \]

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── 1\. Generate Architecture Deviation Notice

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── 2\. Draft Proposed Architecture Decision Record (ADR)

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── 3\. Place task in BLOCKED state in PROJECT\_STATE.json

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── 4\. Append entry to AGENT\_ESCALATION.md

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;▼

&nbsp;\[ AWAIT HUMAN LEAD EXPLICIT SIGN-OFF \]

&nbsp;

### **Prohibited Architectural Modifications**

* **No Database Proliferation:** The agent is barred from adding Redis, DynamoDB, MongoDB, or OpenSearch. All relational, spatial, vector, and JSON data must reside in **Amazon RDS PostgreSQL** (postgis \+ pgvector).  
* &nbsp;  
* **No "ECS Express Mode":** The agent must reject any instruction referencing this non-existent AWS service and default to **AWS App Runner** or **ECS Fargate**.  
* &nbsp;  
* **No Direct Fraud Classification:** The agent must never write code that outputs an autonomous prediction of "fraud probability." All outputs must adhere to the **Evidence Consistency Score (ECS)** and **Audit Review Priority Index (ARPI)** schemas.  
* &nbsp;

## **9\. Dependency-Aware Reasoning and Change Impact Analysis**

To prevent changes in low-level modules from causing silent regressions in downstream interfaces, the agent consults an explicit dependency matrix before executing edits.

&nbsp;

\+----------------------------------------------------------------------------------------------------+

|                                 SYSTEM COMPONENT DEPENDENCY GRAPH                                  |

\+----------------------------------------------------------------------------------------------------+

&nbsp;\[ Raw Data Assets (KML, RDD2022, SROIE, Gazette S.O. 3467(E)) \]

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;▼

&nbsp;\[ Data Ingestion & Normalization Tier (Pydantic Models) \]

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;┌───────┴───────────────────────────────┐

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;▼                                       ▼

&nbsp;\[ ML Extraction (SSCD, Textract) \]   \[ Spatial Processing (PostGIS LRS) \]

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│                                       │

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└───────┬───────────────────────────────┘

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;▼

&nbsp;\[ Deterministic Validation Rules (Mass, Velocity, Classification) \]

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;▼

&nbsp;\[ Evidence Fusion Engine (Subjective Logic Consensus: b, d, u) \]

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;▼

&nbsp;\[ API Layer (FastAPI Schemas & Endpoints) \]

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;┌───────┴───────────────────────────────┐

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;▼                                       ▼

&nbsp;\[ Reviewer UI (Next.js / Leaflet) \]  \[ Statutory Report Generator (PDF/A-3) \]

&nbsp;

### **Change-Risk Classification and Autonomy Protocol**

| Risk Level | Triggering Operations | Permitted Autonomy | Mandatory Validation Pipeline |
| :---- | :---- | :---- | :---- |
| **LOW** | Internal function logic, unit test additions, CSS utility token adjustments, documentation edits. | Fully Autonomous | Local unit tests pass; linter clean; git diff verified. |
| **MEDIUM** | API endpoint response schema edits, new rule implementations, UI component refactoring. | Bounded Autonomy | Full test suite passes; contract tests verify API compatibility; typecheck clean. |
| **HIGH** | Database schema changes, Alembic migrations, vector embedding dimension edits, SQS message schemas. | Approval Required | Draft migration; verify forward/backward compatibility; await human approval before apply. |
| **CRITICAL** | Core architectural boundaries, authentication policies, S3 Object Lock configurations, legal terminology changes. | Strict Human Oversight | Halt immediately; create proposed ADR; require signed human engineering approval. |

## **10\. Tiered Autonomy Levels and Stop Conditions**

MuniAudit-AI implements a seven-level autonomy model defining exactly what tools and actions the agent may execute without real-time human intervention:

&nbsp;

\+----------------------------------------------------------------------------------------------------+

|                                      TIERED AUTONOMY MODEL                                         |

\+----------------------------------------------------------------------------------------------------+

&nbsp;LEVEL 0: READ-ONLY ANALYSIS         Inspect files, run read-only queries, explain architecture.

&nbsp;&nbsp;&nbsp;&nbsp;│

&nbsp;LEVEL 1: ISOLATED IMPLEMENTATION    Edit single implementation file \+ update corresponding unit test.

&nbsp;&nbsp;&nbsp;&nbsp;│

&nbsp;LEVEL 2: COMPONENT SLICE            Multi-file edits within a single domain package (e.g., \`src/rules/\`).

&nbsp;&nbsp;&nbsp;&nbsp;│

&nbsp;LEVEL 3: DEPENDENCY MODIFICATION    \[GATE\] Install approved packages listed in package manifest.

&nbsp;&nbsp;&nbsp;&nbsp;│

&nbsp;LEVEL 4: DATABASE MIGRATIONS        \[GATE\] Author and apply Alembic schema migrations.

&nbsp;&nbsp;&nbsp;&nbsp;│

&nbsp;LEVEL 5: CLOUD PROVISIONING         \[GATE\] Execute Terraform or AWS deployment commands.

&nbsp;&nbsp;&nbsp;&nbsp;│

&nbsp;LEVEL 6: PRODUCTION DEPLOYMENT      \[GATE\] Tag release versions, deploy to production endpoints.

&nbsp;

### **Mandatory Stop Conditions**

The agent must immediately halt execution, log diagnostics to AGENT\_ESCALATION.md, and await human input under any of the following triggers:

&nbsp;

1. **Third-Strike Debugging Failure:** The same unit test or compilation command fails three consecutive times despite attempted repairs.  
2. &nbsp;  
3. **Interface Incompatibility:** An upstream API or data asset lacks a required attribute specified in the system design.  
4. &nbsp;  
5. **Ambiguous Statutory Criteria:** A civil engineering or procurement rule is missing an exact numerical tolerance or threshold.  
6. &nbsp;  
7. **Security Invariant Breach:** Proposed code introduces an unauthenticated endpoint, bypasses input sanitization, or exposes an AWS credential.  
8. &nbsp;  
9. **Architectural Contradiction:** A user prompt requests an implementation that contradicts CORE\_CONTEXT.md or an approved ADR.  
10. &nbsp;  
11. **Destructive Command Triggered:** The tool execution pipeline identifies a shell command containing file deletion, branch resets, or database drops.  
12. &nbsp;

## **11\. Three-Strike Debugging Protocol**

To prevent the agent from entering endless, context-consuming hallucination loops when code fails, Antigravity enforces a strict, graduated debugging protocol:

&nbsp;

\[ TEST / BUILD EXECUTION FAILS \]

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├──► STRIKE 1: Atomic In-Place Repair

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│      • Isolate exact line and error traceback.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│      • Apply targeted fix without altering interfaces.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│      • Re-run specific failing test.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├──► STRIKE 2: Deep Contextual Diagnostics

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│      • If Strike 1 fails, read full implementation file \+ caller definitions.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│      • Check git diff against working baseline.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│      • Verify assumptions against dependencies.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│      • Apply revised fix; re-run test suite.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└──► STRIKE 3: MANDATORY STOP & ESCALATION

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Halt all tool invocations immediately.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Execute \`git checkout \-- \<modified\_files\>\` to revert broken edits.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Write diagnostic autopsy to \`FAILED\_APPROACHES.md\`.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Format structured escalation block in \`AGENT\_ESCALATION.md\`.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Output help request to user and enter IDLE state.

&nbsp;

### **Invariant Rules for Debugging:**

* **Never Game Tests:** The agent is strictly prohibited from modifying test assertion values or skipping tests (pytest.mark.skip) to clear an error message.  
* &nbsp;  
* **Preserve Working State:** Reverting to the last clean Git commit is always preferable to stacking unverified speculative fixes on top of broken code.  
* &nbsp;

## **12\. Git, Testing, and ML Intelligence Directives**

### **12.1 Git Intelligence as Repository Memory**

* **Branch Strategy:** Work executes on isolated feature branches (feat/rules-mass-envelope, fix/ocr-bounding-box). Direct commits to main are blocked by hook policies.  
* &nbsp;  
* **Atomic Checkpointing:** Commits must represent atomic logical units of work conforming to the Conventional Commits specification (feat, fix, test, refactor, docs).  
* &nbsp;  
* **Safe Recovery:** The agent is prohibited from using git reset \--hard, git clean \-fd, or git push \--force. All rollbacks must use clean checkouts (git checkout \-- \<file\>) or non-destructive reverts (git revert \<commit\>).  
* &nbsp;

### **12.2 Testing Intelligence and Execution Hierarchy**

The agent maps every code change to its position in the testing pyramid, running only the relevant test slices during development before executing the full regression suite:

&nbsp;

\+----------------------------------------------------------------------------------------------------+

|                                      TEST EXECUTION PYRAMID                                        |

\+----------------------------------------------------------------------------------------------------+

&nbsp;LEVEL 1: Static Typecheck & Lint    mypy src/ && ruff check src/                \[ Runs on every edit \]

&nbsp;LEVEL 2: Unit Tests                 pytest tests/unit/test\_\<target\>.py          \[ Runs on every edit \]

&nbsp;LEVEL 3: Integration Tests          pytest tests/integration/                   \[ Runs per slice \]

&nbsp;LEVEL 4: Invariant Verification     pytest tests/rules/                         \[ Runs on rule edits \]

&nbsp;LEVEL 5: End-to-End Pipeline        pytest tests/e2e/test\_dossier\_reconcile.py  \[ Runs pre-milestone \]

&nbsp;LEVEL 6: ML Benchmark Validation    python scripts/run\_benchmark.py \--sample 50 \[ Runs pre-freeze \]

&nbsp;

### **12.3 Machine Learning Intelligence and Evidentiary Boundaries**

The agent must treat machine learning code with strict statistical rigor, avoiding common data science fallacies:

&nbsp;

1. **Never Invent Model Metrics:** The agent must never output fabricated precision, recall, or accuracy scores in comments or documentation. All reported numbers must originate from executed benchmark scripts outputting to results/.  
2. &nbsp;  
3. **Prevent Data Leakage:** The agent must strictly verify that evaluation datasets enforce geodetic buffer separations ($\> 2.0\\text{ km}$) and contractor holdouts, ensuring models do not memorize background textures.  
4. &nbsp;  
5. **Deterministic Seed Locking:** All stochastic processes (data splits, augmentation, k-means clustering) must explicitly declare and lock random seeds (seed=42).  
6. &nbsp;  
7. **Distinguish Sensitivity from Real Performance:** The agent must never describe synthetic benchmark performance as "real-world fraud detection accuracy." All descriptions must state: *"Model sensitivity evaluated against controlled synthetic perturbation suites."*  
8. &nbsp;

## **13\. Domain, UI, AWS, and Security Directives**

### **13.1 Project-Specific Domain Directives**

* **MuniAudit-AI is an Evidentiary Triage Instrument:** The system does not predict criminal intent, make autonomous accusations, or replace human authority. Its sole purpose is to cross-reconcile multi-source evidence and prioritize high-exposure dockets for human auditor review.  
* &nbsp;  
* **Ternary Legal Status:** Every audit check must output one of three administrative states:  
* 

  * VERIFIED\_COMPLIANT: Evidence corroborated across independent sources within statutory bounds.  
  * &nbsp;  
  * SUBSTANTIVE\_INCONSISTENT: Mathematical, physical, or statutory rule invariant breached.  
  * &nbsp;  
  * INCONCLUSIVE\_DATA: Optical degradation, missing metadata, or sensor dropout requiring human inspection without penalty.  
  * &nbsp;

### **13.2 UI/UX Architectural Directives**

* **Enforce the** DESIGN.md **Token System:** The agent is strictly prohibited from inventing arbitrary hex colors, linear gradients, or ad-hoc Tailwind classes. All UI surfaces must strictly use Slate/Zinc tokens (\#090D16, \#0F172A, \#1E293B) paired with high-contrast neutral evidence viewports.  
* &nbsp;  
* **Double-Encode All Statuses:** Color alone must never represent an audit state. Every severity indicator must pair an accessible color with an explicit semantic icon and text label (e.g., Red Octagon CRITICAL \[Physical Law Breach\]).  
* &nbsp;  
* **Cognitive Forcing Functions:** Action buttons (Affirm Disallowance, Execute Override) must remain programmatically locked until the user has clicked all primary evidence bounding boxes and satisfied the inspection dwell timer.  
* &nbsp;

### **13.3 AWS Cloud Engineering Directives**

* **Zero Hallucinated Cloud Primitives:** The agent must verify cloud service names against official AWS documentation. Any reference to "ECS Express Mode" or "SageMaker Serverless GPU" must be rejected.  
* &nbsp;  
* **Strict Cost Optimization:** Prohibit the provisioning of unneeded high-cost resources (such as AWS NAT Gateways at $32.40/month, SageMaker Real-Time instances at $737/month, or OpenSearch Serverless at $345/month). Consolidate vector, spatial, and relational operations inside **Amazon RDS PostgreSQL** (postgis \+ pgvector).  
* &nbsp;  
* **Payload Flattening for Document Ingestion:** To prevent PDF /ToUnicode font-mapping exploits, all incoming PDF documents must be rasterized to flat 300 DPI PNG images before passing to OCR extractors.  
* &nbsp;

## **14\. Subagents, Skills, and Hooks Specifications**

### **14.1 Specialized Subagent Roster**

\+----------------------------------------------------------------------------------------------------+

|                                    SPECIALIZED SUBAGENT ROSTER                                     |

\+----------------------+----------------------+-----------------------+------------------------------+

| Subagent Name        | Primary Role         | Allowed Tools         | Invocation Condition         |

\+----------------------+----------------------+-----------------------+------------------------------+

| architecture-auditor | Enforces ADR & specs | read\_file, grep\_search| Pre-commit on core files     |

| test-engineer        | Author & run tests   | run\_command, edit\_file| Post-implementation phase    |

| security-reviewer    | Scans OWASP/secrets  | read\_file, grep\_search| Pre-deployment security gate |

| visual-qa-agent      | Browser UI inspector | browser\_action, click | Post-frontend modification   |

| data-integrity-guard | Validates schemas/LRS| read\_file, run\_command| Post-data ingestion tasks    |

\+----------------------+----------------------+-----------------------+------------------------------+

&nbsp;

### **14.2 Reusable Agent Skills (**.agents/skills/**)**

1. skills/preflight-check: Verifies Git status, reads active state machine, scans negative memory, and generates TASK\_CONTRACT.md.  
2. &nbsp;  
3. skills/run-verification: Executes the targeted test suite, linter, and typechecker; asserts zero regressions.  
4. &nbsp;  
5. skills/audit-git-diff: Analyzes staged changes against allowed file whitelists; rejects scope creep.  
6. &nbsp;  
7. skills/check-ml-integrity: Asserts random seed locking, verifies geodetic buffer holdouts, and checks metric calculation logic.  
8. &nbsp;  
9. skills/update-project-state: Programmatically updates PROJECT\_STATE.json with commit SHAs and test execution counts.  
10. &nbsp;

### **14.3 Lifecycle Interceptor Hooks (**.agents/hooks.json**)**

* PreToolUse (run\_command): Intercepts shell commands. Blocks dangerous patterns (rm \-rf, git reset \--hard, DROP TABLE, unapproved package installs).  
* &nbsp;  
* PostToolUse (edit\_file / write\_file): Automatically executes syntax validation and formatting on the modified file.  
* &nbsp;  
* Stop: Evaluates the Definition of Done before the session terminates; blocks completion if uncommitted modifications or failing tests remain.  
* &nbsp;

## **15\. Task Contract & Response Contract Protocols**

Every engineering engagement with Antigravity must follow a strict input/output contract.

&nbsp;

### **15.1 Task Initiation Contract**

The user or orchestrating script provides the task definition following this template:

&nbsp;

TASK\_ID: TASK-RULE-004

STATE: 07\_DETERMINISTIC\_RULES

OBJECTIVE: Implement the kinematic travel-time feasibility validator in src/rules/kinematics.py.

REQUIREMENT: REQ-KIN-001 (Implied transit speed v \= d / Δt \<= 90.0 km/h).

GOVERNING\_SPEC: ARCHITECTURE.md Section 6 & Geospatial Reasoning Architecture.

FILES\_TO\_INSPECT:

&nbsp;

* src/schemas/telematics.py  
* &nbsp;  
* docs/adr/004-geodesic-speed-bounds.md  
* FILES\_ALLOWED\_TO\_MODIFY:  
* &nbsp;  
* src/rules/kinematics.py  
* &nbsp;  
* tests/rules/test\_kinematics.py  
* FILES\_FORBIDDEN:  
* &nbsp;  
* src/api/\*  
* &nbsp;  
* alembic/\*  
* SUCCESS\_CRITERIA:  
* &nbsp;  
* Pure function evaluating Haversine distance over elapsed time in seconds.  
* &nbsp;  
* Returns structured KinematicResult(is\_feasible, implied\_speed\_kmh, violation\_severity).  
* &nbsp;  
* 100% test pass on tests/rules/test\_kinematics.py.  
* &nbsp;

### **15.2 Agent Response Contract**

Antigravity must structure its final response using this standard reporting template, completely eliminating conversational fluff:

&nbsp;

### **1\. SUMMARY OF IMPLEMENTATION**

Implemented the deterministic kinematic travel-time feasibility rule using great-circle Haversine distance and calibrated urban tortuosity factors.

&nbsp;

### **2\. FILES MODIFIED**

* src/rules/kinematics.py: Added evaluate\_kinematic\_feasibility() enforcing the 90.0 km/h physical invariant and 60.0 km/h urban threshold.  
* &nbsp;  
* tests/rules/test\_kinematics.py: Added 12 unit tests covering stationary pings, compliant transit, urban traffic bounds, and teleportation violations.  
* &nbsp;

### **3\. VERIFICATION EVIDENCE**

* Typecheck: mypy src/rules/kinematics.py \-\> Clean (0 errors).  
* &nbsp;  
* Unit Tests: pytest tests/rules/test\_kinematics.py \-v \-\> 12 passed in 0.18s.  
* &nbsp;  
* Full Suite: pytest tests/ \-\> 76 passed in 1.42s.  
* &nbsp;

### **4\. ARCHITECTURAL & DEPENDENCY IMPACT**

* Downstream impact: src/fusion/engine.py can now consume KinematicResult.  
* &nbsp;  
* Interface changes: None. Public API contracts remain untouched.  
* &nbsp;

### **5\. STATE TRANSITION & NEXT STEP**

* Updated PROJECT\_STATE.json (Commit: a8f3b19, Phase: 07\_DETERMINISTIC\_RULES).  
* &nbsp;  
* Next Recommended Task: TASK-RULE-005 (Integrate kinematic results into Subjective Logic opinion mapper).  
* &nbsp;

## **16\. Authoritative Governance Deliverables (Copy-Paste Ready)**

The following deliverables are fully formulated and ready to be committed directly into the MuniAudit-AI repository to instantiate the engineering governance system immediately.

&nbsp;

### **Deliverable A: Master Agent Rules File**

**Path:** .agents/rules/muniaudit-engineering.md

&nbsp;

## **trigger: always-on description: Senior Engineering Invariants and Governance Rules for MuniAudit-AI**

# **Master Engineering Invariants: MuniAudit-AI**

You are an expert principal software engineer and municipal infrastructure auditor building MuniAudit-AI. You are not a generic conversational assistant. You operate under strict engineering discipline, bounded autonomy, and immutable architectural invariants.

&nbsp;

## **1\. Foundational Project Invariants**

1. Core Mission: MuniAudit-AI is an evidentiary reconciliation platform that identifies cross-sensor discrepancies in public works billing to prioritize human audit reviews. It is NOT an autonomous fraud judge.  
2. &nbsp;  
3. Anti-Accusation Rule: You must NEVER generate code, schemas, or summaries that assert criminal guilt, "fraud probability," or intent (mens rea). Outputs must strictly represent objective metrological variances, statutory noncompliance, and calibrated review priorities.  
4. &nbsp;  
5. Decoupled Processing: Machine learning is strictly confined to perceptual feature extraction (SSCD visual embeddings, Textract OCR). All physical, geometric, temporal, and legal validations must be executed deterministically.  
6. &nbsp;  
7. Epistemic Separation: Maintain strict visual and structural separation across five tiers: FACT, MODEL OUTPUT, RULE RESULT, INFERENCE, and RECOMMENDATION.  
8. &nbsp;

## **2\. Architectural Boundaries**

1. Database Consolidation: All relational, spatial, vector, and audit ledger records must reside in Amazon RDS PostgreSQL (using PostGIS and pgvector). You are strictly forbidden from introducing DynamoDB, OpenSearch, MongoDB, or Redis.  
2. &nbsp;  
3. No Phantom Cloud Primitives: Do not reference or configure "ECS Express Mode." Use AWS App Runner or Amazon ECS Fargate.  
4. &nbsp;  
5. Local/Cloud Parity: All core algorithms must run identically in local Docker Compose (using PaddleOCR and CPU ONNX Runtime) and in AWS (using Textract and App Runner).  
6. &nbsp;  
7. No Live Government Scraping: Never write web scrapers against live Vahan or Parivahan portals. All lookups must query local mock database tables.  
8. &nbsp;

## **3\. Implementation and Safety Directives**

1. Smallest Safe Change: Implement the minimal code necessary to satisfy the task contract. Do not refactor unrelated code.  
2. &nbsp;  
3. Whitelist Discipline: Modify ONLY files explicitly listed in the task contract's allowed whitelist. Do not touch forbidden files.  
4. &nbsp;  
5. Three-Strike Rule: If a command or test fails three consecutive times, you must HALT, revert changes via git checkout, write an autopsy to FAILED\_APPROACHES.md, and log an escalation in AGENT\_ESCALATION.md.  
6. &nbsp;  
7. No Test Gaming: You are strictly forbidden from modifying test assertion values, skipping tests, or disabling linters to make a build pass.  
8. &nbsp;  
9. Definition of Done: A task is not done until code compiles, types pass, tests pass, documentation is updated, git is committed, and PROJECT\_STATE.json is refreshed.  
10. &nbsp;

## **4\. Operational Execution Sequence**

On every prompt, execute the Senior Engineer Loop:

&nbsp;

1. Ground: Read PROJECT\_STATE.json and CORE\_CONTEXT.md.  
2. &nbsp;  
3. Check: Verify git branch and ensure working tree is clean.  
4. &nbsp;  
5. Memory: Scan FAILED\_APPROACHES.md for forbidden patterns.  
6. &nbsp;  
7. Contract: Formulate and verify the pre-flight declaration.  
8. &nbsp;  
9. Implement: Apply minimal code edits to whitelisted files.  
10. &nbsp;  
11. Verify: Run compiler, linter, and unit test suite.  
12. &nbsp;  
13. Audit: Inspect git diff to ensure zero unintended changes.  
14. &nbsp;  
15. State: Update PROJECT\_STATE.json with commit SHA and test counts.  
16. &nbsp;  
17. Report: Emit structured AGENT\_RESPONSE\_CONTRACT.  
18. &nbsp;

### **Deliverable B: Core Project Context File**

**Path:** CORE\_CONTEXT.md

&nbsp;

# **CORE\_CONTEXT.md: MuniAudit-AI Ground Truth**

## **1\. Problem Definition**

Municipal stormwater drain desilting across Indian Urban Local Bodies (ULBs) suffers from an evidentiary air gap. Auditing relies on disconnected manual records (paper Measurement Books, curled thermal weighbridge receipts, vehicle challans, and unindexed photos). Contractors exploit this by billing ghost dumpers, recycling photos from prior years, substituting construction debris for sludge, and inflating scale tickets.

&nbsp;

## **2\. Locked Technical Architecture**

* Ingestion: Multipart upload via FastAPI \-\> S3 Object Lock (WORM storage).  
* &nbsp;  
* Processing Queue: Amazon SQS FIFO queue with Dead-Letter Queue (DLQ) isolation.  
* &nbsp;  
* Visual Forensics: Meta AI SSCD (ResNet-50 512-d ONNX) \-\> pgvector HNSW index (tau \>= 0.82) \-\> OpenCV SIFT \+ RANSAC homography inlier verification.  
* &nbsp;  
* Document Intelligence: Preprocessing (CLAHE, deskew) \-\> Amazon Textract Queries (fallback: PaddleOCR v4) \-\> Closed arithmetic check: |Gross \- Tare \- Net| \<= 20 kg.  
* &nbsp;  
* Geospatial & Kinematics: PostGIS LRS linear chainage locate (ST\_LineLocatePoint) within 15m canal buffer \-\> Haversine great-circle distance with 1.35 urban tortuosity factor \-\> Physical speed ceiling: v\_geodesic \<= 90.0 km/h.  
* &nbsp;  
* Vehicle Taxonomy: Local SQL mirror of Vahan registry \-\> MoRTH Gazette S.O. 3467(E) axle-load limits \-\> Physical container bulk density ceiling: Net Mass \<= Bed Volume \* 1.90 t/m³.  
* &nbsp;  
* Evidence Fusion: Subjective Logic consensus operator (omega \= b, d, u, a) combining deterministic hard gates with soft discrepancy signals \-\> Output: Evidence Consistency Score (ECS: 0.0 to 1.0) and Audit Review Priority Index (ARPI: 0 to 100).  
* &nbsp;  
* Explainability: Granular GAGAS-compliant causality chain \-\> PDF/A-3 export with Section 63 Bharatiya Sakshya Adhiniyam (BSA) 2023 cryptographic provenance.  
* &nbsp;  
* UI Design Language: Forensic Split-Canvas Workspace \-\> Deep Slate shell (\#090D16) with neutral light artifact containers (\#FFFFFF) \-\> Double-encoded severity indicators \-\> Cognitive Forcing Gate with dwell timers.  
* &nbsp;

## **3\. Absolute Prohibitions**

* DO NOT predict "fraud probability" or make criminal accusations.  
* &nbsp;  
* DO NOT use unweighted heuristic risk sums or black-box neural late fusion.  
* &nbsp;  
* DO NOT provision DynamoDB, OpenSearch, or multi-AZ Aurora clusters.  
* &nbsp;  
* DO NOT execute live scraping against government web portals.  
* &nbsp;

### **Deliverable C: Machine-Readable Project State Schema & Initial State**

**Path:** PROJECT\_STATE.json

&nbsp;

JSON

{

&nbsp;&nbsp;"$schema": "http://json-schema.org/draft-07/schema\#",

&nbsp;&nbsp;"title": "MuniAuditProjectState",

&nbsp;&nbsp;"type": "object",

&nbsp;&nbsp;"required": \[

&nbsp;&nbsp;&nbsp;&nbsp;"schema\_version",

&nbsp;&nbsp;&nbsp;&nbsp;"project\_name",

&nbsp;&nbsp;&nbsp;&nbsp;"current\_phase",

&nbsp;&nbsp;&nbsp;&nbsp;"current\_branch",

&nbsp;&nbsp;&nbsp;&nbsp;"last\_verified\_commit",

&nbsp;&nbsp;&nbsp;&nbsp;"last\_verified\_at",

&nbsp;&nbsp;&nbsp;&nbsp;"system\_health",

&nbsp;&nbsp;&nbsp;&nbsp;"active\_task",

&nbsp;&nbsp;&nbsp;&nbsp;"completed\_tasks",

&nbsp;&nbsp;&nbsp;&nbsp;"blocked\_tasks",

&nbsp;&nbsp;&nbsp;&nbsp;"test\_metrics",

&nbsp;&nbsp;&nbsp;&nbsp;"active\_invariants"

&nbsp;&nbsp;\],

&nbsp;&nbsp;"properties": {

&nbsp;&nbsp;&nbsp;&nbsp;"schema\_version": { "type": "string", "enum": \["1.0.0"\] },

&nbsp;&nbsp;&nbsp;&nbsp;"project\_name": { "type": "string", "enum": \["MuniAudit-AI"\] },

&nbsp;&nbsp;&nbsp;&nbsp;"current\_phase": {

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"type": "string",

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"enum": \[

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"01\_PROBLEM\_LOCKED",

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"02\_DATA\_LOCKED",

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"03\_ARCHITECTURE\_LOCKED",

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"04\_SCAFFOLDING\_READY",

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"05\_DATA\_PIPELINE",

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"06\_CORE\_ML\_IMPLEMENTATION",

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"07\_DETERMINISTIC\_RULES",

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"08\_EVIDENCE\_FUSION",

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"09\_API\_AND\_SERVICES",

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"10\_FRONTEND\_WORKSPACE",

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"11\_EVALUATION\_AND\_BENCHMARK",

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"12\_DEMO\_HARDENING",

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"13\_SUBMISSION\_FROZEN"

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\]

&nbsp;&nbsp;&nbsp;&nbsp;},

&nbsp;&nbsp;&nbsp;&nbsp;"current\_branch": { "type": "string" },

&nbsp;&nbsp;&nbsp;&nbsp;"last\_verified\_commit": { "type": "string", "pattern": "^\[0-9a-f\]{7,40}$" },

&nbsp;&nbsp;&nbsp;&nbsp;"last\_verified\_at": { "type": "string", "format": "date-time" },

&nbsp;&nbsp;&nbsp;&nbsp;"system\_health": { "type": "string", "enum": \["GREEN", "AMBER", "RED"\] },

&nbsp;&nbsp;&nbsp;&nbsp;"active\_task": {

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"type": \["object", "null"\],

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"properties": {

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"task\_id": { "type": "string" },

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"description": { "type": "string" },

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"strike\_count": { "type": "integer", "minimum": 0, "maximum": 3 }

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;}

&nbsp;&nbsp;&nbsp;&nbsp;},

&nbsp;&nbsp;&nbsp;&nbsp;"completed\_tasks": {

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"type": "array",

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"items": { "type": "string" }

&nbsp;&nbsp;&nbsp;&nbsp;},

&nbsp;&nbsp;&nbsp;&nbsp;"blocked\_tasks": {

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"type": "array",

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"items": { "type": "string" }

&nbsp;&nbsp;&nbsp;&nbsp;},

&nbsp;&nbsp;&nbsp;&nbsp;"test\_metrics": {

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"type": "object",

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"required": \["unit\_tests\_passing", "unit\_tests\_failing", "code\_coverage\_pct"\],

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"properties": {

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"unit\_tests\_passing": { "type": "integer" },

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"unit\_tests\_failing": { "type": "integer" },

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"code\_coverage\_pct": { "type": "number" }

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;}

&nbsp;&nbsp;&nbsp;&nbsp;},

&nbsp;&nbsp;&nbsp;&nbsp;"active\_invariants": {

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"type": "object",

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"required": \["mass\_balance\_tolerance\_kg", "geodesic\_speed\_ceiling\_kmh", "max\_silt\_density\_t\_m3"\],

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"properties": {

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"mass\_balance\_tolerance\_kg": { "type": "number", "enum": \[20.0\] },

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"geodesic\_speed\_ceiling\_kmh": { "type": "number", "enum": \[90.0\] },

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"max\_silt\_density\_t\_m3": { "type": "number", "enum": \[1.90\] }

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;}

&nbsp;&nbsp;&nbsp;&nbsp;}

&nbsp;&nbsp;}

}

&nbsp;

### **Deliverable D: Task Contract Template**

**Path:** TASK\_CONTRACT.md

&nbsp;

# **TASK\_CONTRACT: \[TASK\_ID\]**

## **1\. Task Metadata**

* Task ID: TASK-000  
* &nbsp;  
* Phase: \[e.g., 07\_DETERMINISTIC\_RULES\]  
* &nbsp;  
* Author: \[AI Agent / Human Lead\]  
* &nbsp;  
* Timestamp: 2026-09-19T10:00:00Z  
* &nbsp;

## **2\. Objective & Justification**

* Objective: \[Single sentence describing the atomic change\]  
* &nbsp;  
* Why: \[Explain which user journey, requirement, or failure mode this resolves\]  
* &nbsp;  
* Requirement ID: \[e.g., REQ-PHYS-002\]  
* &nbsp;  
* Governing Specification: \[Document and section reference\]  
* &nbsp;

## **3\. Bounded Scope**

* Allowed Files to Modify:  
* 

  * src/...  
  * &nbsp;  
  * tests/...  
  * &nbsp;  
* Explicitly Forbidden Files:  
* 

  * alembic/\*  
  * &nbsp;  
  * CORE\_CONTEXT.md  
  * &nbsp;  
  * .agents/rules/\*  
  * &nbsp;

## **4\. Implementation Plan**

* Step 1: Write failing unit test in tests/...  
* &nbsp;  
* Step 2: Implement minimal logic in src/...  
* &nbsp;  
* Step 3: Verify execution passes typecheck and unit test suite  
* &nbsp;

## **5\. Acceptance Criteria**

* \[ \] Code compiles with zero TypeScript / MyPy warnings  
* &nbsp;  
* \[ \] Unit test executes and passes cleanly  
* &nbsp;  
* \[ \] Zero changes made outside allowed file whitelist  
* &nbsp;  
* \[ \] Documentation updated to reflect interface contracts  
* &nbsp;  
* \[ \] PROJECT\_STATE.json refreshed with commit hash  
* &nbsp;

### **Deliverable E: Agent Response Contract Template**

**Path:** AGENT\_RESPONSE\_CONTRACT.md

&nbsp;

# **AGENT\_RESPONSE\_CONTRACT: \[TASK\_ID\]**

## **1\. Executive Summary**

\[Concise 2-sentence explanation of what was built and verified.\]

&nbsp;

## **2\. Change Manifest**

* Modified Files:  
* 

  * src/... (Line delta: \+42, \-5)  
  * &nbsp;  
  * tests/... (Line delta: \+28, \-0)  
  * &nbsp;  
* New Dependencies Added: NONE (Prohibited without Level 3 approval)  
* &nbsp;

## **3\. Empirical Verification Evidence**

* Linter / Typecheck Command: mypy src/path/to/module.py \-\> Output: Clean (0 errors)  
* &nbsp;  
* Unit Test Command: pytest tests/path/to/test.py \-\> Output: 6 passed in 0.14s  
* &nbsp;  
* Full Regression Command: pytest tests/ \-\> Output: 72 passed, 0 failed in 1.28s  
* &nbsp;

## **4\. Architectural Self-Check**

* \[x\] Confirmed zero deviation from locked architecture in CORE\_CONTEXT.md  
* &nbsp;  
* \[x\] Confirmed no unapproved database, cloud, or algorithmic primitives introduced  
* &nbsp;  
* \[x\] Confirmed all physical, legal, and operational tolerances strictly maintained  
* &nbsp;

## **5\. State & Memory Updates**

* Git Commit SHA: \[7-char hash\] \- feat(scope): conventional commit title  
* &nbsp;  
* PROJECT\_STATE.json Updated: Yes (Passing tests: 72, Failing: 0\)  
* &nbsp;  
* FAILED\_APPROACHES.md Entry Added: None (Task succeeded on Strike 1\)  
* &nbsp;

## **6\. Next Recommended Action**

\[Identify the immediate next dependent task from the master roadmap.\]

&nbsp;

### **Deliverable F: Failed Approaches Memory Bank**

**Path:** FAILED\_APPROACHES.md

&nbsp;

# **FAILED\_APPROACHES.md: Negative Memory Bank**

This document records failed technical approaches, broken dependencies, and dead ends.

ANTIGRAVITY MUST CONSULT THIS FILE BEFORE COMMENCING ANY TASK.

REPEATING A DOCUMENTED FAILED APPROACH IS A STRICT PROTOCOL BREACH.

&nbsp;

## **ENTRY 001: Direct Monocular Depth Estimation for Silt Volume**

* Date: 2026-09-17  
* &nbsp;  
* Component: src/ml/depth\_estimation.py  
* &nbsp;  
* Approach: Deployed Metric3D zero-shot depth model on smartphone RGB photos to calculate stockpile volume.  
* &nbsp;  
* Failure Symptom: Scale drift exceeded 40%; volumetric error calculated at 68% against known test stockpile.  
* &nbsp;  
* Underlying Mechanism: Monocular depth lacks an absolute metric scale anchor without physical ground targets. Scale factor ambiguity propagates cubically into volume calculations.  
* &nbsp;  
* Permanent Prohibition: Do not attempt single-image volumetric depth calculations.  
* &nbsp;  
* Adopted Alternative: Enforce physical container capacity envelope bounds based on Vahan Gross Vehicle Weight and certified bed volumes.  
* &nbsp;

## **ENTRY 002: Perceptual Hash (pHash) as Visual Copy Prefilter**

* Date: 2026-09-18  
* &nbsp;  
* Component: src/ml/visual\_forensics.py  
* &nbsp;  
* Approach: Applied a 64-bit DCT perceptual hash as a fast prefilter before querying SSCD vector embeddings.  
* &nbsp;  
* Failure Symptom: Legitimate photographic copies with a 15% edge crop or 10-degree rotation were silently dropped by pHash before SSCD could evaluate them.  
* &nbsp;  
* Underlying Mechanism: Perceptual hashing lacks affine invariance; spatial crops disrupt global low-frequency DCT grids.  
* &nbsp;  
* Permanent Prohibition: Never use pHash as an initial gate for cropped or rotated image deduplication.  
* &nbsp;  
* Adopted Alternative: Query Meta AI SSCD 512-d descriptors directly against the PostgreSQL pgvector HNSW index.  
* &nbsp;

## **ENTRY 003: Sauvola Binarization Prior to Amazon Textract**

* Date: 2026-09-18  
* &nbsp;  
* Component: src/ocr/preprocessor.py  
* &nbsp;  
* Approach: Applied Sauvola local adaptive binarization to thermal weighbridge scans before dispatching to Amazon Textract.  
* &nbsp;  
* Failure Symptom: Textract character extraction confidence dropped from 94% to 58%; dotted fonts broke into disjoint pixel clusters.  
* &nbsp;  
* Underlying Mechanism: Textract's neural vision-language models expect 8-bit grayscale gradient context. Converting to 1-bit binary removes stroke antialiasing.  
* &nbsp;  
* Permanent Prohibition: Do not pass Sauvola-binarized images to Amazon Textract.  
* &nbsp;  
* Adopted Alternative: Use CLAHE and bilateral filtering for Textract; reserve Sauvola binarization strictly for the local PaddleOCR fallback.  
* &nbsp;

### **Deliverable G: Human Escalation Register**

**Path:** AGENT\_ESCALATION.md

&nbsp;

# **AGENT\_ESCALATION.md: Human Escalation Register**

This queue tracks blocked agent tasks requiring human authority.

&nbsp;

| Escalation ID | Task ID | Trigger Type | Blocker Summary | Action Required by Human Lead | Status |
| :---- | :---- | :---- | :---- | :---- | :---- |
| ESC-001 | TASK-INIT | BASELINE | System initialization baseline. | Verify and approve CORE\_CONTEXT.md and initial state. | RESOLVED |

### **Deliverable H: Core Reusable Agent Skills**

#### **1\. Skill: Pre-Flight Verification**

**Path:** .agents/skills/preflight-check/SKILL.md

&nbsp;

## **name: preflight-check description: Mandatory pre-flight verification protocol. Executes before any code modification to ground situational awareness, check project state, verify git clean status, and inspect negative memory.**

# **Pre-Flight Verification Skill**

When invoked, execute the following operational sequence:

&nbsp;

1. Inspect Project State:  
2. 

   * Read PROJECT\_STATE.json. Confirm that the requested task is permitted in the current current\_phase.  
   * &nbsp;  
   * Read CORE\_CONTEXT.md to re-ground domain invariants and boundaries.  
   * &nbsp;  
3. Verify Git Cleanliness:  
4. 

   * Run git status \-s.  
   * &nbsp;  
   * If uncommitted changes exist, halt and warn user: "Working tree is dirty. Stash or commit before starting a new task."  
   * &nbsp;  
5. Scan Negative Memory:  
6. 

   * Read FAILED\_APPROACHES.md. Search for keywords relevant to the current task.  
   * &nbsp;  
   * Assert that the proposed implementation strategy does not match a documented failure.  
   * &nbsp;  
7. Generate Task Contract:  
8. 

   * Formulate TASK\_CONTRACT.md detailing the objective, allowed files, forbidden files, and acceptance criteria.  
   * &nbsp;  
   * Output the formatted PRE-FLIGHT VERIFICATION block to the console.  
   * &nbsp;

#### **2\. Skill: Test and Self-Verification**

**Path:** .agents/skills/test-and-verify/SKILL.md

&nbsp;

## **name: test-and-verify description: Comprehensive self-verification pipeline. Runs compilers, linters, typecheckers, unit tests, and regression suites, reporting exact empirical results.**

# **Test and Self-Verification Skill**

When invoked, execute the following operational sequence:

&nbsp;

1. Static Type and Lint Check:  
2. 

   * Run mypy src/ (or npm run typecheck). If errors occur, log as Strike 1\.  
   * &nbsp;  
   * Run ruff check src/ (or npm run lint). Clean trivial formatting issues.  
   * &nbsp;  
3. Targeted Unit Test Execution:  
4. 

   * Run the specific test file associated with the modified module: pytest tests/path/to/test\_\<module\>.py \-v.  
   * &nbsp;  
   * Capture exact passed/failed counts and runtime duration.  
   * &nbsp;  
5. Regression Verification:  
6. 

   * Run the broader test suite: pytest tests/unit/.  
   * &nbsp;  
   * Verify that no neighboring or downstream components broke.  
   * &nbsp;  
7. Scope Compliance Check:  
8. 

   * Run git status \-s.  
   * &nbsp;  
   * Verify that changes are confined strictly to files whitelisted in TASK\_CONTRACT.md.  
   * &nbsp;  
9. Update State:  
10. 

    * If all checks pass, invoke python scripts/update\_state.py to refresh PROJECT\_STATE.json with the new commit hash and test metrics.  
    * &nbsp;

### **Deliverable I: Specialized Subagent Definitions**

#### **1\. Subagent: Architecture Auditor**

**Path:** .agents/agents/architecture-auditor.md

&nbsp;

name: architecture-auditor

description: Specialized architectural compliance reviewer. Inspects diffs to detect unapproved services, database proliferation, layer leakage, and design deviations.

tools:

&nbsp;

* read\_file  
* &nbsp;  
* grep\_search  
* &nbsp;  
* file\_search  
* &nbsp;

# **Architecture Auditor Subagent**

You are an adversarial architectural auditor for MuniAudit-AI. Your sole duty is to inspect proposed code changes and verify 100% compliance with CORE\_CONTEXT.md and approved ADRs.

&nbsp;

Review Checklist:

&nbsp;

1. Database Integrity: Did the change add any database client other than PostgreSQL (psycopg, sqlalchemy, asyncpg)? If yes, REJECT.  
2. &nbsp;  
3. Invariant Protection: Did the change weaken physical mass-balance bounds (20 kg tolerance), geodesic speed limits (90 km/h), or bulk density ceilings (1.90 t/m³)? If yes, REJECT.  
4. &nbsp;  
5. Decoupling Verification: Did machine learning code attempt to output a direct "fraud prediction" or calculate billing disallowances? If yes, REJECT.  
6. &nbsp;  
7. Layer Boundaries: Did frontend components import backend database models directly? If yes, REJECT.  
8. &nbsp;

Output Format:

Emit a structured verdict: STATUS: \[APPROVED | REJECTED\], followed by itemized citations to specific lines and architecture clauses.

&nbsp;

### **Deliverable J: Antigravity Lifecycle Hooks Configuration**

**Path:** .agents/hooks.json

&nbsp;

JSON

{

&nbsp;&nbsp;"hooks": {

&nbsp;&nbsp;&nbsp;&nbsp;"PreToolUse": \[

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"matcher": "run\_command",

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"hooks": \[

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"type": "command",

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"command": ".agents/hooks/security-guard.sh",

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"timeout": 15

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;}

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\]

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;}

&nbsp;&nbsp;&nbsp;&nbsp;\],

&nbsp;&nbsp;&nbsp;&nbsp;"PostToolUse": \[

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"matcher": "edit\_file|write\_file",

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"hooks": \[

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"type": "command",

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"command": ".agents/hooks/syntax-validate.sh",

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"timeout": 30

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;}

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\]

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;}

&nbsp;&nbsp;&nbsp;&nbsp;\],

&nbsp;&nbsp;&nbsp;&nbsp;"Stop": \[

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"hooks": \[

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"type": "command",

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"command": ".agents/hooks/definition-of-done.sh",

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"timeout": 30

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;}

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\]

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;}

&nbsp;&nbsp;&nbsp;&nbsp;\]

&nbsp;&nbsp;}

}

&nbsp;

**Path:** .agents/hooks/security-guard.sh

&nbsp;

Bash

\#\!/usr/bin/env bash

\# Intercepts shell commands to block destructive operations and secret exposure.

set \-euo pipefail

&nbsp;

input\_json=$(cat)

&nbsp;

\# Extract command string using jq or python fallback

if command \-v jq \>/dev/null 2\>&1; then

&nbsp;&nbsp;cmd=$(echo "$input\_json" | jq \-r '.toolCall.args.CommandLine // .toolCall.args.command // ""')

else

&nbsp;&nbsp;cmd=$(echo "$input\_json" | python3 \-c 'import sys, json; d=json.load(sys.stdin); print(d.get("toolCall",{}).get("args",{}).get("CommandLine",""))')

fi

&nbsp;

\# Blacklisted destructive commands

if echo "$cmd" | grep \-qE '\\b(rm\\s+-rf\\s+/|git\\s+reset\\s+--hard|git\\s+clean\\s+-fd|DROP\\s+DATABASE|DROP\\s+TABLE)\\b'; then

&nbsp;&nbsp;echo '{"allow\_tool": false, "deny\_reason": "SECURITY VIOLATION: Destructive command detected and blocked by policy."}'

&nbsp;&nbsp;exit 0

fi

&nbsp;

\# Block unapproved pip installs during locked phases

if echo "$cmd" | grep \-qE '\\b(pip\\s+install|npm\\s+install)\\b' && \! echo "$cmd" | grep \-qE '\\b(--dry-run)\\b'; then

&nbsp;&nbsp;\# Check if project state allows package additions

&nbsp;&nbsp;if grep \-q '"current\_phase": "13\_SUBMISSION\_FROZEN"' PROJECT\_STATE.json 2\>/dev/null; then

&nbsp;&nbsp;&nbsp;&nbsp;echo '{"allow\_tool": false, "deny\_reason": "PHASE VIOLATION: Package modifications forbidden in frozen submission state."}'

&nbsp;&nbsp;&nbsp;&nbsp;exit 0

&nbsp;&nbsp;fi

fi

&nbsp;

echo '{"allow\_tool": true}'

exit 0

&nbsp;

**Path:** .agents/hooks/syntax-validate.sh

&nbsp;

Bash

\#\!/usr/bin/env bash

\# Validates syntax of modified Python or TypeScript files immediately after editing.

set \-euo pipefail

&nbsp;

input\_json=$(cat)

&nbsp;

if command \-v jq \>/dev/null 2\>&1; then

&nbsp;&nbsp;filepath=$(echo "$input\_json" | jq \-r '.toolCall.args.path // .toolCall.args.file\_path // ""')

else

&nbsp;&nbsp;filepath=$(echo "$input\_json" | python3 \-c 'import sys, json; d=json.load(sys.stdin); print(d.get("toolCall",{}).get("args",{}).get("path",""))')

fi

&nbsp;

if \[\[ "$filepath" \=\~ \\.py$ \]\] && \[ \-f "$filepath" \]; then

&nbsp;&nbsp;python3 \-m py\_compile "$filepath" 2\>/dev/null || {

&nbsp;&nbsp;&nbsp;&nbsp;echo "{\\"decision\\": \\"warn\\", \\"message\\": \\"Syntax error detected in modified Python file: $filepath\\"}"

&nbsp;&nbsp;&nbsp;&nbsp;exit 0

&nbsp;&nbsp;}

fi

&nbsp;

echo '{"decision": "allow"}'

exit 0

&nbsp;

### **Deliverable K: First-Run Antigravity Initialization Prompt**

Copy and paste this prompt into the Antigravity chat panel upon opening the repository for the first time:

&nbsp;

Initialize your session as the Senior Engineering Agent for MuniAudit-AI.

&nbsp;

Execute the following initialization sequence:

&nbsp;

1. Load and read .agents/rules/muniaudit-engineering.md. These are your always-on governing rules.  
2. &nbsp;  
3. Read CORE\_CONTEXT.md to understand the project problem statement, locked architecture, and strict legal/epistemic boundaries.  
4. &nbsp;  
5. Read PROJECT\_STATE.json to identify the current operational phase and verify that your working tree is clean.  
6. &nbsp;  
7. Scan FAILED\_APPROACHES.md to index all documented negative memory and forbidden implementation patterns.  
8. &nbsp;  
9. Check git status and confirm that all test harnesses are operational by running the baseline smoke test suite.  
10. &nbsp;

Once completed, respond strictly using the AGENT\_RESPONSE\_CONTRACT format summarizing:

&nbsp;

* Current system phase and health status  
* &nbsp;  
* Verification that all invariants and boundaries are indexed  
* &nbsp;  
* The immediate next task ready for implementation  
* Do not write or modify application code in this turn.  
* &nbsp;

### **Deliverable L: Daily Project-Health Prompt**

Copy and paste this prompt at the start of every hackathon work sprint:

&nbsp;

Run a comprehensive Project Health and Situational Awareness Check for MuniAudit-AI.

&nbsp;

Execute the following diagnostic routine:

&nbsp;

1. State Audit: Compare git rev-parse HEAD against last\_verified\_commit in PROJECT\_STATE.json. Is the state record fresh or stale?  
2. &nbsp;  
3. Git Hygiene: Verify that the current branch conforms to naming conventions and that no uncommitted file modifications exist.  
4. &nbsp;  
5. Code Integrity: Execute the full static typecheck (mypy src/ or npm run typecheck) and linter (ruff check src/).  
6. &nbsp;  
7. Regression Verification: Run the automated test suite (pytest tests/). Report the exact number of passing, failing, and skipped tests.  
8. &nbsp;  
9. Architectural Self-Check: Invoke the architecture-auditor subagent to verify that no unauthorized databases, cloud primitives, or uncalibrated scoring patterns have drifted into code.  
10. &nbsp;  
11. Documentation Sync: Verify that docs/DATA\_DICTIONARY.md matches active database model definitions.  
12. &nbsp;

Emit a structured Health Report identifying:

&nbsp;

* Overall System Status: \[GREEN / AMBER / RED\]  
* &nbsp;  
* Discrepancies or drift detected  
* &nbsp;  
* Recommended remediation tasks  
* &nbsp;

### **Deliverable M: Pre-Deployment Agent Prompt**

Copy and paste this prompt before pushing code to AWS App Runner or initiating a staging deployment:

&nbsp;

Execute the Pre-Deployment Verification Protocol for MuniAudit-AI.

&nbsp;

Verify the following production deployment gates:

&nbsp;

1. State Machine: Confirm that PROJECT\_STATE.json is at phase 12\_DEMO\_HARDENING or higher.  
2. &nbsp;  
3. Test Suite: Assert that 100% of unit, integration, and rule invariant tests pass with zero skips or warnings.  
4. &nbsp;  
5. Offline Parity: Verify that the local Docker Compose build (docker compose up \--build) launches cleanly and passes the health check endpoint (GET /healthz).  
6. &nbsp;  
7. Security Audit: Scan all staged code for hardcoded secrets, AWS access keys, private certificates, or open CORS wildcards (\*).  
8. &nbsp;  
9. Cloud Topology: Verify that all AWS SDK clients target approved services (S3, SQS, RDS PostgreSQL, Textract, Bedrock Nova Micro). Assert that zero references to NAT Gateways, SageMaker GPU endpoints, or OpenSearch exist.  
10. &nbsp;  
11. Legal / Epistemic Check: Verify that all user-facing strings and report templates cite Section 63 of the Bharatiya Sakshya Adhiniyam, 2023 (BSA), and that zero autonomous accusations of "fraud" exist in generated payloads.  
12. &nbsp;

Report deployment clearance status: \[APPROVED FOR DEPLOYMENT / BLOCKED\].

&nbsp;

### **Deliverable N: Final Hackathon Freeze Prompt**

Copy and paste this prompt six hours before the final hackathon submission deadline:

&nbsp;

Execute the Final Hackathon Freeze Protocol for MuniAudit-AI.

&nbsp;

Perform the following final stabilization tasks:

&nbsp;

1. Transition State Machine: Update PROJECT\_STATE.json to phase 13\_SUBMISSION\_FROZEN.  
2. &nbsp;  
3. Activate Demo Mode: Assert that NEXT\_PUBLIC\_DEMO\_MODE=true is set and verify that the instant-reset hotkey (Ctrl \+ Shift \+ R) reloads the primary demonstration fixture in under 500 ms.  
4. &nbsp;  
5. Dependency Freeze: Verify that lockfiles (poetry.lock, package-lock.json) are committed and that all installation scripts run with frozen immutable flags (\--frozen-lockfile).  
6. &nbsp;  
7. Rehearse Demo Flow: Execute the automated Playwright 3-minute scripted demonstration test (tests/e2e/test\_demo\_flow.py). Assert that all three visual, kinematic, and gravimetric anomaly alerts render cleanly with zero console warnings.  
8. &nbsp;  
9. Lock Working Tree: Create signed git tag v1.0.0-hackathon-final. Ensure the working branch is completely clean.  
10. &nbsp;

Provide the final executive sign-off confirming that the project is completely frozen, verified, and ready for judging.

&nbsp;