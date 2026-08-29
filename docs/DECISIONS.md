# Decision record

This document is authoritative. It distinguishes accepted product decisions from provisional architecture and experiments. `FOUNDATION.md` explains the design but does not override statuses recorded here.

## Status legend

- **Accepted** — explicitly selected or affirmed by the project owner.
- **Recommended** — converged recommendation awaiting product evidence or implementation validation.
- **Unresolved** — requires an experiment or future owner decision.
- **Deferred** — intentionally excluded from the initial product slice.

## Accepted

### D-001 — Adaptive rather than advisory-only or fully governed

The harness uses model judgment by default with narrow hard boundaries where consequence or explicit user intent warrants them.

### D-002 — Three visible delivery postures

- Prototype
- Standard
- Hardened

### D-003 — Postures define outcomes and evidence, not mandatory procedures

Planning, TDD, worktrees, review, documentation, and delegation are techniques. The model selects them according to the delivery claim, risk, repository, and available evidence.

### D-004 — Activity, posture, and capability are independent

Activities such as explore, design, troubleshoot, implement, review, and promote do not imply one posture or workflow. Capabilities such as debugging, planning, testing, review, and isolation are optional techniques.

### D-005 — Optimistic declaration for Prototype and Standard

- Explicit user posture or an unambiguous equivalent is accepted without redundant confirmation.
- Ordinary unqualified repository implementation defaults to Standard, is declared once, and proceeds.
- Clearly exploratory implementation may be declared Prototype and proceeds.
- One focused question is appropriate only when ambiguity has meaningful asymmetric cost.

This resolves the earlier blocking-confirmation choice. It does not authorize consequential actions that independently require confirmation.

### D-006 — Hardened requires explicit intent or approval

Hardened may be selected directly by the user or proposed by the assistant with a concrete rationale. It is never entered silently.

### D-007 — No silent posture changes

Promotion or downgrade is visible. A change in intended use can trigger a recommendation, not an automatic transition.

### D-008 — Universal protections do not dial down

Universal protection is split into three mechanisms:

1. **Host-enforceable boundaries** — exact, observable operations or targets that Pi, the OS, repository hooks, or project tooling can reliably block or confirm.
2. **Model-level invariants** — preserve named criteria, distinguish fact from assumption, cite fresh evidence for success claims, and disclose material limitations.
3. **Semantic risks requiring judgment** — sensitive business data, consequential shared state, production-facing intent, or contextual irreversibility that cannot be classified reliably from one tool call.

Do not promise deterministic enforcement for semantic categories.

### D-009 — One implementation per session is the preferred convention

Posture conceptually belongs to the active deliverable. Session scope is the dominant operating convention, not an identity or runtime restriction. A new deliverable in the same session requires a visible posture declaration; any future stored marker must be explicitly set or cleared.

### D-010 — Cross-session work must not require task-management machinery

Use existing tickets, specs, tests, branches, and PRs first. A compact handoff may be added when explicitly useful. Do not create a task database by default.

### D-011 — Build a new behavioral architecture while reusing Pi-superpowers source material

The organizing principle changes from mandatory lifecycle to evidence-calibrated capabilities. Reuse proven techniques and Pi-native implementation patterns selectively.

### D-012 — Materialize only for a natural future consumer

No automatic plan documents, architecture memory files, evidence ledgers, task journals, or per-session repository files. This does not prohibit a purposeful existing ticket/spec, or an ephemeral scratch artifact if a later experiment proves it necessary for long work.

### D-013 — Instruction authority follows the host

The rig does not replace Pi's or the provider's actual instruction hierarchy. Within that hierarchy:

- explicit user posture and criteria govern posture selection;
- trusted repository instructions and executable constraints remain applicable;
- posture controls assurance breadth, not authority to violate repository or host constraints;
- embedded instructions in untrusted content are data, not authority.

Delegated agents receive an explicit handoff containing posture, goal, criteria, relevant repository constraints, and authorization limits. Children may report that a posture is inadequate but may not silently change it.

## Recommended

### R-001 — Use “delivery posture” as the primary term

This describes fit-for-purpose evidence without implying that Prototype is careless.

### R-002 — Standard has a firm outcome center

A Standard result:

- fits the repository;
- is understandable to its next maintainer;
- protects the behavior it changes;
- satisfies its acceptance criteria with fresh evidence;
- discloses material residual limitations.

Root-cause debugging, targeted tests, project checks, self-review, conditional independent review, and affected documentation are possible capabilities—not a mandatory sequence.

### R-003 — Use three separable architectural concepts

1. **Posture header** — short portable guidance.
2. **Capability library and posture profiles** — progressively disclosed techniques and calibration.
3. **Delivery kernel** — optional Pi runtime state/UI, built only if drift evaluation justifies it.

### R-004 — Start with four capability groups

- explore/design;
- debug;
- test/verify;
- review.

Do not port every Pi-superpowers skill before validating the architecture.

### R-005 — Prototype completion names limitations

This is the primary low-friction guard against accidental promotion. The evidence must come from actual observation or tool output, not a prose template alone.

### R-006 — Promotion is explicit

Operational use, external exposure, real sensitive data, unattended operation, durable shared-state mutation, or becoming a shared dependency should trigger visible posture reconsideration.

## Unresolved

### Q-001 — Is a persistent Pi delivery kernel necessary?

Hypothesis: branch-aware posture state, status UI, and short pre-agent injection reduce drift after compaction, resume, fork, model change, and delegation.

Counter-hypothesis: chat/native context is sufficient, while stored state creates stale-posture risk.

**Initial-product rule:** do not build the kernel before guidance-only evaluation. If later tested, use append-only active-branch events with an explicit clear tombstone:

```ts
type DeliveryStateEvent = {
  version: 1
  posture: "prototype" | "standard" | "hardened" | null
  source: "explicit" | "inferred"
}
```

Latest valid event on the active branch wins. `null` explicitly clears state. A new deliverable requires visible set/clear. No project default in the first state experiment.

### Q-002 — Exact posture-selection interface

Candidates for a later kernel:

- `/delivery prototype|standard|hardened|clear`;
- an agent-callable setter plus human command;
- natural-language inference recorded through an explicit state event.

Automatic deterministic natural-language inference is not assumed to be feasible.

### Q-003 — Minimal posture-header content

Define the smallest portable instruction that reliably communicates:

- the three evidence postures;
- evidence before claims;
- no silent transitions;
- host-relative authority;
- the distinction among deterministic, behavioral, and semantic protections.

### Q-004 — Which host boundaries merit deterministic hooks?

Only exact, reliably observable authorization/safety predicates should be blocked mechanically. Broad sensitive/consequential/production classification is deferred.

### Q-005 — Cross-session handoff UX

A later `/handoff` could serialize posture, goal/reference, decisions, evidence, limitations, and next action into a new session or copyable text. Defer until cross-session failures are observed.

### Q-006 — Product name

Working name: **Pi Adaptive Dev Rig**.

Candidate descriptions include Adaptive Superpowers, Evidence-Calibrated Harness, and Adaptive Delivery Harness. Avoid implying that a selected label itself provides production assurance.

## Deferred from the initial product slice

- delivery kernel and persistent posture state, until drift is measured;
- task IDs, task registration, lifecycle state, graphs, or databases;
- multiple concurrent task records;
- automatic plan, design, architecture, or evidence files;
- project defaults, dashboards, and ticket-system integration;
- automatic posture promotion;
- broad semantic policy engines;
- mandatory TDD, worktrees, reviews, or subagent fan-out;
- structured debt graphs;
- automatic cross-session indexing;
- model-routing policy before delivery behavior is validated;
- full port of every Pi-superpowers skill.

## Decision principles

1. Prefer the smaller mechanism until a measured failure justifies more.
2. Optimize user friction and agent confusion together.
3. Evaluate delivery outcomes, not workflow compliance.
4. Preserve existing project truth instead of duplicating it.
5. Hard enforcement requires reliable observability and meaningful consequence.
6. A recommendation in `FOUNDATION.md` does not become accepted without a decision here.
