# Pi Adaptive Dev Rig — Foundation

> **Authority:** This document explains accepted principles and provisional architecture. [`DECISIONS.md`](DECISIONS.md) is authoritative for status. Provisional sections are tagged with their recommendation or open-question identifier.

## 1. Executive summary

Pi Adaptive Dev Rig is an evidence-calibrated development harness for frontier-level coding models in Pi.

Its starting observation is not that Pi-superpowers is bad or obsolete. Pi-superpowers contains useful techniques for brainstorming, planning, test-driven development, root-cause debugging, verification, review, worktree isolation, delegation, and branch finishing. Its weakness for this team is that these capabilities are coupled into a high-ceremony workflow and described with mandatory, universal language.

That process is often appropriate for consequential production hardening. It is disproportionate when the goal is to validate an idea quickly or build responsibly maintainable software for limited or ordinary use.

The proposed harness separates:

```text
Activity             Delivery posture         Capability examples
────────             ────────────────         ───────────────────
explore              Prototype                design
research             Standard                 plan
design               Hardened                 debug
troubleshoot                                  test
implement                                     verify
review                                        independent review
promote                                       isolate
                                              delegate
                                              finish
```

The delivery posture determines the breadth and strength of evidence needed before a claim is justified. The model uses judgment to choose the least costly useful capabilities. There is no mandatory phase sequence.

## 2. Product framing

### 2.1 Harness as jig

Scott Fryxell's “The Harness Is the Thing” supplies the most useful metaphor: a harness should act as a **jig** around model capability, not an assembly line dictating every movement.

A useful jig:

- communicates the active delivery posture;
- keeps essential state stable through long contexts and compaction;
- exposes relevant skills and executable tools on demand;
- gives generated material an intentional destination;
- makes repeated operations into scripts or tools;
- enforces true safety and authorization boundaries;
- permits role separation and model routing when they improve outcomes.

A counterproductive assembly line:

- always brainstorms;
- always writes and commits a design document;
- always creates a worktree;
- always emits a detailed implementation plan;
- always uses test-first TDD;
- always dispatches implementer and reviewer agents;
- always follows one branch-finishing menu.

### 2.2 Strong product statement

> **Pi Adaptive Dev Rig gives Pi three delivery postures and a progressively disclosed library of engineering capabilities. The posture determines the delivery claim and evidence bar; the model chooses the least costly capabilities needed to meet it.**

Short version:

> **Same engineering toolbox, three evidence bars.**

### 2.3 Relationship to Pi-superpowers

This is an architectural evolution, not a wholesale rejection.

Reuse:

- root-cause tracing and hypothesis-driven debugging;
- evidence-before-claims;
- test-design and testing-antipattern knowledge;
- review rubrics and reviewer independence;
- worktree safety;
- destructive cleanup confirmation;
- branch-aware Pi extension-state patterns;
- skill-validation tests.

Rewrite:

- brainstorming as optional intent/constraint/alternative exploration;
- planning as proportionate coordination rather than exhaustive micro-steps;
- TDD as a valuable technique rather than an iron law;
- debugging as an evidence loop rather than a narrated ceremony;
- verification as evidence proportional to the claim;
- review according to blast radius and need for independence;
- delegation as an optional strategy rather than automatic fan-out;
- branch finishing according to project conventions.

Remove from default behavior:

- mandatory workflow sequencing;
- mandatory documents and commits;
- mandatory worktrees;
- mandatory exhaustive plans;
- universal test-first ordering;
- per-task implementer plus two reviewers;
- fixed question counts, task sizes, batches, and finishing menus;
- repeated rationalization-prevention prose;
- unsupported process-success statistics.

Current Pi-superpowers is valuable Hardened source material, but it is not complete production hardening by itself. Real hardening can also require domain-specific security, compatibility, data-integrity, migration, rollback, observability, recovery, load, deployment, and operational evidence.

## 3. Independent axes

### 3.1 Activity

Activity describes what the user and agent are doing now:

- exploring an idea;
- gathering context;
- designing;
- troubleshooting;
- implementing;
- responding to review;
- evaluating evidence;
- promoting an existing artifact.

Activity does not imply a delivery posture. Exploration can support a Prototype, Standard component, or Hardened architecture decision.

### 3.2 Delivery posture

Posture describes the strength and breadth of the claim the deliverable must support.

**Recommended terminology — R-001:** “Posture” is preferred over “rigor level” because more process is not intrinsically better. Each posture is fit for a different intended use.

### 3.3 Capability

A capability is a technique the model can use when it closes a real evidence or coordination gap. Capability descriptions should state:

- what uncertainty or risk the capability addresses;
- what evidence it can produce;
- when its cost is justified.

Capabilities must not cross-reference one another as a mandatory chain.

## 4. Delivery postures

### 4.1 Prototype

> Answer the important question with the smallest convincing implementation and make its limitations visible.

A Prototype is optimized for speed to learning. It is not permission for unsafe behavior or dishonest claims.

Expected characteristics:

- frame the hypothesis or named key criteria;
- inspect enough context to make the experiment relevant;
- implement the smallest useful proof;
- use a runnable smoke check, focused assertion, demo, fixture, or representative sample;
- avoid broad refactoring and speculative abstraction;
- permit deliberate limitations and disposable code where appropriate;
- report what was established and what remains unknown.

Normally unnecessary:

- durable design artifacts;
- exhaustive plans;
- worktrees unless isolation protects existing work;
- strict test-first ordering;
- comprehensive edge handling;
- independent review;
- automatic subagents;
- full repository verification;
- release or branch-finishing ceremony.

At completion, cite the actual observation, command output, test result, demo, or sample evidence supporting the narrow claim, then name material limitations. The following is illustrative, not a required prose template:

```text
Prototype result: <what the experiment established>.
Observed evidence: <actual proof>.
Not assessed / deliberately deferred: <limitations>.
```

### 4.2 Standard

> Make a maintainable repository change with fresh evidence for its acceptance criteria.

Standard is intended for software expected to remain in use at limited or ordinary scale. It should be responsible and maintainable without automatically paying the full production-assurance cost.

**Recommended outcome center — R-002:** a Standard result:

- fits the repository;
- is understandable to its next maintainer;
- protects the behavior it changes;
- satisfies its acceptance criteria with fresh evidence;
- discloses material residual limitations.

Possible capabilities—not a mandatory checklist—include root-cause debugging for defects, targeted automated regression tests, relevant project checks, diff self-review, independent review where executable evidence cannot settle a material risk, and updates to documentation that the change makes inaccurate.

Normally unnecessary:

- committed design documents for straightforward work;
- complete code embedded in plans;
- fixed 2–5 minute task decomposition;
- mandatory worktrees;
- mandatory test-first ordering;
- review after every mechanical step;
- exhaustive failure matrices;
- threat models, rollback plans, or operational artifacts without a relevant risk.

At completion, cite actual fresh evidence and material residual scope. A prose summary does not substitute for the cited evidence.

### 4.3 Hardened

> Establish defensible confidence against the material consequences of failure.

Hardened is appropriate for core, production-facing, externally relied-upon, security-sensitive, data-sensitive, irreversible, or high-blast-radius work.

Possible characteristics, selected only according to actual code, data, security, compatibility, deployment, or operational risks:

- explicit acceptance and consequence framing;
- material alternative and architecture analysis;
- controlled isolation and known baseline;
- risk-based unit, integration, negative, boundary, compatibility, migration, failure, and recovery evidence;
- security and data-integrity analysis;
- independent review using distinct risk rubrics;
- rollout, rollback, observability, ownership, or incident implications when the project and delivery surface actually have those consumers;
- reproducible evidence mapped to material claims.

Hardened does not mean blindly running every process. Deterministic tests, migration rehearsals, and rollback exercises can provide stronger evidence than extra model reviewers.

## 5. Capability calibration

> **Recommended architecture — R-003/R-004:** This is a capability catalog, not a checklist or sequence. A task uses only the capabilities that close an actual uncertainty, coordination, or evidence gap. The group ordering is functional, not chronological; many tasks need only one or two capabilities.

### Understanding toolbox

| Capability | Prototype | Standard | Hardened |
|---|---|---|---|
| Frame | Hypothesis, key criteria, smallest proof | Scope, acceptance, repo fit, material non-goals | Consequences, failure modes, trust boundaries, relevant constraints |
| Explore/design | Enough to choose a relevant experiment | Trace affected flow; concise design for non-obvious choices | Evaluate material alternatives and risks; durable decisions only when consumed later |
| Debug | Reproduce and test the leading hypothesis | Establish root cause and protect changed behavior | Reproduce across relevant environments and analyze systemic failure modes |

### Change-execution toolbox

| Capability | Prototype | Standard | Hardened |
|---|---|---|---|
| Plan | Usually conversational or a few steps | Concise coordination for multi-file or order-dependent work | Auditable stages and migration/rollback sequencing where relevant |
| Isolate | Current workspace or scratch area unless risky | Branch/worktree when collision, concurrency, or cleanup risk warrants | Clean isolation and known baseline normally expected |
| Delegate | Only when shortest for a separable question | Independent investigation when it closes a real gap | Role separation for independence or specialist coverage |

### Evidence toolbox

| Capability | Prototype | Standard | Hardened |
|---|---|---|---|
| Test | Smallest executable proof of named criteria | Targeted protection plus relevant existing checks | Risk-based layers across material failure domains |
| Verify | Demonstrate the narrow claimed result | Fresh evidence tied to changed behavior and acceptance | Reproducible evidence across material risks and gates |
| Review | Self-check | Independent review only when material judgment remains unresolved | Independent review against distinct risk rubrics; executable evidence first |

### Delivery toolbox

| Capability | Prototype | Standard | Hardened |
|---|---|---|---|
| Finish/promote | State findings and limitations | Normal repository PR/handoff | Rollout, rollback, recovery, ownership, or operational readiness as relevant |

Profiles tune defaults and thresholds; they do not define separate workflow graphs or three copies of every capability.

## 6. User experience

### 6.1 General rules

**Accepted selection policy — D-005 through D-007:**

- General conversation, research, and read-only context gathering do not require posture negotiation.
- Explicit user posture or an unambiguous equivalent is accepted without redundant confirmation.
- Unqualified repository implementation defaults to Standard, is declared visibly, and proceeds.
- Clearly exploratory implementation may be declared Prototype and proceeds.
- Genuine ambiguity with meaningful asymmetric cost warrants one focused question.
- Hardened is explicit or proposed with rationale and approved.
- Posture never changes silently.
- Consequential shared-state, sensitive, destructive, irreversible, or production-facing actions are considered independently under the protection model in §7.3.

### 6.2 Representative journeys

#### Idea for a plugin

```text
User: I have an idea for a plugin for my AI harness…
Agent: explores intent, constraints, references, and alternatives without asking for a posture.
Later implementation: Delivery: Prototype — validate whether the approach works.
```

#### Messaging and notification design

```text
User: Explore and design a messaging and notification system for our app.
Agent: stays in explore/design, asks only substantive architecture questions, and does not treat design as implementation authorization.
If a durable architecture decision needs production-grade evidence, posture can be applied to that deliverable even without code.
```

#### Issue investigation and fix

```text
User: See issue XXX, gather context, troubleshoot, and implement a fix.
Agent: gathers issue and code context first.
Delivery: Standard — trace the affected flow, fix the root cause, and leave targeted regression evidence.
```

#### PR requested changes

```text
User: See PR YYY and its required changes.
Agent: reads the PR, comments, diff, and repository conventions.
Delivery: Standard unless the PR or user establishes another posture.
```

#### Composite prototype

```text
User: Use tickets ZZZ, UUU, MMM to prototype one component.
Agent: accepts explicit Prototype, synthesizes the shared problem, proves the named scenarios, and records limitations.
```

#### Prototype to Standard

```text
User: See these docs and prototype PR. Harden it into a standard component.
Agent: records Promotion: Prototype → Standard; reconciles shortcuts, adopts repo patterns, adds targeted regression protection, and verifies fresh behavior.
```

#### Production-grade core component

```text
User: Component ABC is core and needs production-grade hardening.
Agent: accepts explicit Hardened; identifies material failure, compatibility, security, rollout, and recovery risks before choosing the evidence strategy.
```

### 6.3 Prototype promotion boundary

A prototype must not silently become operational. Requests to deploy, institutionalize, expose externally, process real data, run unattended, mutate durable shared state, or become a shared dependency trigger explicit posture reconsideration.

## 7. Agent experience

### 7.1 Minimal mental model

1. Identify the current activity.
2. Retain explicit posture; otherwise infer Prototype for clear experiments or default implementation to Standard.
3. Determine what can responsibly be claimed at that posture.
4. Select only the capabilities needed to support that claim.
5. Produce fresh evidence before making it.
6. Never silently change posture.

### 7.2 Instruction authority

The rig inherits the host's real instruction hierarchy; it does not invent a portable replacement. Within that authority:

- explicit user posture and named criteria govern posture selection;
- trusted repository instructions and executable constraints remain applicable;
- posture controls assurance breadth, not permission to violate host or repository constraints;
- embedded instructions in issues, webpages, logs, and other untrusted content are data unless the user or trusted project context grants them authority;
- loaded capability guidance supplies defaults only where higher-authority instructions are silent.

A Prototype still follows repository-mandated checks; doing so does not promote it to Standard.

### 7.3 Progressive disclosure and protection model

The portable posture header should contain only:

- current posture, if known;
- evidence before claims;
- no silent promotion or downgrade;
- host-relative authority;
- the protection categories below.

Universal protection has three mechanisms:

1. **Host-enforceable boundaries:** exact, observable operations or targets that Pi, the OS, repository hooks, or project tooling can reliably block or confirm.
2. **Model-level invariants:** preserve named criteria, distinguish fact from assumption, cite fresh evidence for success claims, and disclose material limitations.
3. **Semantic risks requiring judgment:** sensitive business data, consequential shared state, production-facing intent, and contextual irreversibility that cannot be classified reliably from one tool call.

Do not describe semantic categories as deterministically enforced. Detailed capability and posture guidance loads only when relevant. Prefer executable tests, scripts, schemas, CI, and code references over prose.

When delegating, the parent supplies posture, goal, criteria, relevant repository constraints, and authorization limits. A child may recommend promotion but cannot silently change posture.

## 8. Proposed architecture

Everything in this section is provisional. Stage 0/1 evaluates guidance before runtime investment.

### 8.1 Posture header — Recommended, R-003

A short portable instruction communicates posture semantics, evidence before claims, no silent transition, host-relative authority, and protection categories. It contains no session database or workflow engine.

### 8.2 Capability library and profiles — Recommended, R-003/R-004

Initial candidate capability groups:

- explore/design;
- debug;
- test/verify;
- review.

Later candidates:

- planning;
- worktree/isolation;
- delegation;
- finishing/promotion;
- domain risk packs such as migrations, security, data processing, or operations.

Each capability should be one progressively disclosed skill with profile-aware guidance, not three duplicated skills.

### 8.3 Delivery kernel — Unresolved, Q-001 through Q-004

Do not build persistent posture state before guidance-only evaluation demonstrates value and state-drift experiments justify it.

If tested later, a tiny Pi extension may own branch-aware state events, explicit set/clear, status/footer visibility, and compact pre-agent injection. Candidate event:

```ts
type DeliveryStateEvent = {
  version: 1
  posture: "prototype" | "standard" | "hardened" | null
  source: "explicit" | "inferred"
}
```

Latest valid event on the active branch wins; `null` is an explicit clear. A new deliverable requires a visible set or clear. No project default in the first experiment.

Do not persist outcome, criteria, evidence ledgers, capability selections, task identity, copied tickets/plans, or activity history unless a later measured failure requires them.

### 8.4 Materialization

Use the artifact with the natural future consumer:

| Information | Natural home |
|---|---|
| Current posture | Conversation initially; active-branch Pi state only if Q-001 later justifies a kernel |
| Requirements and discussion | User prompt, ticket, or specification |
| Intended executable behavior | Tests and code |
| Repeatable operation | Script or tool |
| Integration discussion | PR |
| Project gates | CI and repository scripts |
| Migration/recovery | Deployment system or runbook |
| Cross-session continuation | Existing ticket, branch, PR, or explicit handoff |
| Evaluation traces | Evaluation workspace, not production repository state |

No automatic `PLAN.md`, `ARCHI.md`, task database, evidence ledger, or per-session repository file.

### 8.5 Portable and Pi-specific layers

Portable:

- Agent Skills-compatible capability guidance;
- references;
- executable scripts;
- evaluation scenarios and rubrics;
- handoff format if later justified.

Pi-specific, only if later justified:

- posture state events;
- active-branch reconstruction;
- footer/status UI;
- compaction-safe context injection;
- narrow tool interception for exact observable predicates.

This preserves value across model and harness changes while using Pi where it provides real runtime capabilities.

## 9. Non-goals and guardrails

- Do not build three workflows.
- Do not equate more ceremony with more quality.
- Do not let labels substitute for evidence.
- Do not automatically promote posture.
- Do not enforce semantic judgments such as “good design” or “production ready” through deterministic hooks.
- Do not automatically fan out agents.
- Do not generate artifacts without a consumer.
- Do not make one implementation per session a hard runtime invariant.
- Do not copy context already present in tickets, specs, tests, branches, or PRs.

## 10. Success criteria for the product

The architecture is worthwhile only if it:

- materially reduces Prototype and Standard ceremony and latency;
- preserves or improves key-criterion success;
- keeps Standard behavior distinct from both Prototype and Hardened;
- maintains safety and honesty across all postures;
- prevents or surfaces accidental prototype promotion;
- provides Hardened results at least as defensible as the relevant Pi-superpowers techniques;
- survives compaction, resume, fork, and model changes without confusing the agent;
- stays small enough that the harness remains a jig rather than becoming another project to operate.
