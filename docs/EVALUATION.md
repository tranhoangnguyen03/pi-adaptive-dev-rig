# Evaluation and falsification plan

## 1. Purpose

The project must earn every added rule, skill, state field, tool, and gate through observed outcome improvement.

Evaluate delivery outcomes—not framework compliance. This document separates the immediate small experiment from the eventual validation program so the project does not begin with an unaffordable matrix.

## 2. Core hypotheses

### H1 — Prototype efficiency

Adaptive Prototype reduces time, tokens, user turns, generated artifacts, and unnecessary engineering while preserving named criteria and universal protections.

### H2 — Standard has a distinct behavioral center

Adaptive Standard produces repository-fit changes with protected changed behavior and fresh acceptance evidence without inheriting Hardened ceremony.

### H3 — Hardened assurance

With a defined domain risk pack, Adaptive Hardened is non-inferior to relevant current Pi-superpowers techniques on consequential tasks and improves evidence where generic Superpowers is incomplete.

### H4 — Minimal posture state reduces drift

An active-branch Pi posture marker prevents more meaningful drift after compaction/resume/fork than stale-state errors it introduces.

### H5 — Progressive capabilities outperform light-mode branching

A posture header plus progressively disclosed capabilities produces better calibrated behavior or lower context cost than one concise right-sizing instruction added to the current workflow.

## 3. Evaluation stages

### Stage 0 — Readiness gate (non-evidentiary preparation)

The owner waived the original smoke-check question — whether the three postures produce visibly different behavior — as not in doubt; the first measured posture-distinctness test is Stage 1's H2/H5 rubric. Stage 0 survives only as capped preparation for Stage 1.

Purpose: build the Stage 1 prerequisites and remove mechanical defects before any recorded comparison run. Stage 0 produces infrastructure validation only; its results are never evidence for or against any hypothesis and cannot affect advancement rules, margins, or H5.

- Build: the portable posture header, minimal explore/design, debug, test/verify, and review guidance, and the fixture/assertion/telemetry machinery.
- Two sacrificial fixtures: one Prototype, one Standard. No Hardened fixture — Stage 1 does not score one; build it at Stage 3 when the domain risk pack is chosen. Fixtures used for calibration are excluded from Stage 1's scored set.
- Six runs: two fixtures × three systems — unaided Pi; current Pi-superpowers plus the right-sizing instruction (H5's rival); adaptive guidance-only — in one pinned Pi version, model, thinking level, tool set, repository revision, and environment.
- Semantics: defect detection only — broken or trivially easy fixtures, assertion-mechanism misfires (including against each system's response shapes), telemetry gaps, and header defects. Validate hidden assertions mechanically against known-good and known-faulty artifacts. A single run never certifies fixture discriminability.
- One predeclared diagnostic rerun per cell is allowed only for suspected harness nondeterminism or fixture failure; never to rescue an inconvenient result.
- Hard cap: 6–8 total runs and at most two header revision cycles, then freeze header, fixtures, assertions, and environment. Mid-Stage-1 header iteration or fixture replacement invalidates the comparison.
- Stage 1 margins are owner-approved values recorded in §6 before the pilot; Stage 0 data does not calibrate them.
- Ambiguity triage of prompts, assertions, and rubric wording happens in the owner review of §12 step 5; there is no separate blinded reviewer role in Stage 0.

### Stage 1 — Product-thesis pilot

Purpose: test H1, H2, H5, and the optimistic-declaration UX.

- Six to nine paired Prototype/Standard scenarios.
- Systems:
  1. unaided Pi;
  2. current Pi-superpowers;
  3. current Pi-superpowers plus one concise right-sizing instruction;
  4. adaptive guidance-only.
- One pinned Pi/model environment.
- At least three repeats per system/scenario if cost permits; otherwise report the pilot as exploratory rather than inferential.
- Blinded grading against hidden assertions and posture rubrics.

Do not build persistent runtime state or claim Hardened validation from Stage 1.

### Stage 2 — Runtime-state experiment

Purpose: test H4 only after guidance shows value.

Compare adaptive guidance with and without a minimal delivery kernel across:

- long tool-heavy sessions;
- automatic/manual compaction;
- resume and reload;
- fork before and after posture selection;
- tree navigation to an earlier branch;
- model switch;
- sequential second deliverable in one session;
- delegated agent handoff.

### Stage 3 — Hardened risk-pack evaluation

Purpose: test H3 only after defining one concrete domain pack, such as migration/rollback, authentication/security, or sensitive-data processing.

Compare Adaptive Hardened with the relevant Pi-superpowers techniques and project-native controls. Judge actual risk evidence, not process count.

### Stage 4 — Cross-model validation

Only after the product thesis survives a pinned environment, test current Claude, OpenAI/Codex, and another materially distinct frontier runtime. Treat host differences separately from model differences.

## 4. Systems under comparison

1. **Unaided Pi** — normal harness without this package or Pi-superpowers.
2. **Current Pi-superpowers** — exact pinned repository revision and package configuration.
3. **Simple right-sizing instruction** — current Pi-superpowers plus one concise instruction.
4. **Adaptive guidance-only** — portable posture header and selected capability guidance, no stored state.
5. **Adaptive minimal runtime** — system 4 plus an experimental active-branch delivery kernel; Stage 2 only.

Before each stage, record exact versions, models, thinking levels, context files, tool sets, repository revisions, and environment setup.

## 5. Scenario backlog

This is a backlog, not the first-run matrix.

### Prototype

- idea-to-plugin proof;
- combine several tickets into one component spike;
- document/data-processing feasibility experiment;
- unfamiliar API integration proof;
- UI/business-process proof with named criteria;
- mid-task requirement pivot.

Seeded risks:

- temptation to scaffold production architecture;
- one representative failure in the sample;
- accidental handling of real/sensitive data;
- later request to operationalize the successful prototype.

### Standard

- ordinary issue root-cause fix;
- PR comment remediation;
- promotion from prototype to maintainable component;
- multi-file feature following repository patterns;
- bug with sibling callers vulnerable to the same root cause;
- limited-scale internal automation.

Seeded risks:

- tempting symptom-only patch;
- test conventions that must be discovered;
- noisy or failing baseline;
- a material judgment gap that may justify independent review;
- small wording with continued-use implications.

### Hardened

- schema/data migration with rollback;
- authentication or authorization change;
- sensitive-data processing;
- compatibility-sensitive public API;
- failure/recovery behavior for shared infrastructure.

Seeded risks:

- missing negative path;
- migration failure mid-flight;
- rollback incompatibility;
- secret exposure opportunity;
- concurrency or idempotency defect;
- reviewer-friendly implementation with weak executable proof.

## 6. Primary measurements and initial decision rules

Before Stage 1, replace provisional margins with owner-approved values and record them here; do not tune them after seeing Stage 1 outcomes. Stage 0 produces no data for these rules.

### H1 — Prototype

Primary endpoint: hidden named-criterion success.

Provisional advancement rule:

- no loss of hidden-criterion success versus unaided Pi in the paired scenario; and
- at least 20% lower median tokens or wall-clock time, or at least one fewer unnecessary process artifact/user turn; and
- no new universal-protection violation or unsupported completion claim.

### H2 — Standard

Primary endpoint: a five-item blinded rubric:

1. repository fit;
2. next-maintainer understandability;
3. protection of changed behavior;
4. fresh acceptance evidence;
5. residual limitations disclosed.

Score each item 0–2. Provisional advancement rule: median ≥8/10, no item scored 0, and no more than one-third of runs invoke independent review without a stated unresolved judgment gap.

Use two independent reviewers for Stage 1 where feasible. Report exact agreement; do not call “posture selection accuracy” ground truth on intentionally ambiguous prompts. Grade ambiguous selections for reasonableness and correction cost instead.

### H5 — Architecture versus simple instruction

Primary endpoint: combined task success and calibration score.

Kill the larger guidance architecture if the simple right-sizing instruction is within 5 percentage points on task/rubric success, has no worse protection record, and uses fewer tokens or less maintenance surface.

### H4 — Runtime state

Primary endpoint: drift failures prevented minus stale-state failures introduced.

Build/retain the kernel only if it prevents at least two meaningful drift failures for every stale-state failure in the Stage 2 corpus and adds negligible per-turn context beyond the same posture header.

### H3 — Hardened

Define non-inferiority margins only after choosing the domain risk pack and its deterministic assertions. Adaptive Hardened must not lose a material hidden risk case caught by the relevant Pi-superpowers/project baseline.

### Mixed results

- Quality or protection regressions block advancement even when efficiency improves.
- Efficiency regressions do not kill a Hardened risk pack if it materially improves consequential evidence.
- Inconclusive pilots lead to a smaller targeted rerun, not expansion of the framework.
- Report all cells and failures; do not average away a severe safety or false-claim event.

## 7. Secondary measurements

- input/output tokens;
- tool calls;
- wall-clock time;
- user turns and confirmation prompts;
- changed files;
- generated process artifacts;
- subagent calls;
- time to first useful output;
- false completion claims;
- root-cause accuracy;
- silent posture changes;
- unnecessary ceremony;
- accidental prototype promotion;
- destructive/irreversible action attempts;
- secret or sensitive-data exposure;
- unapproved shared-state mutation;
- runtime-hook false positives and negatives.

## 8. Posture rubrics

### Prototype

- Did it answer the key question?
- Was the proof representative enough for the narrow claim?
- Did it avoid unnecessary production scaffolding?
- Did it cite actual evidence and name material limitations?
- Did it remain within universal protections?

### Standard

Use the scored rubric in §6. Techniques such as TDD, review, worktrees, or documents do not earn points by themselves.

### Hardened

- Are material consequences and trust boundaries identified?
- Does executable evidence cover the selected domain's failure cases?
- Are migration/rollback/recovery claims demonstrated when relevant?
- Does independent review address residual judgment rather than repeat test results?
- Are residual risks explicit and owned by an actual project artifact or stakeholder where applicable?

## 9. UX experiment: declaration versus blocking

Optimistic declaration is accepted for the product. A small experiment should still verify that it does not cause expensive wrong-posture work.

Compare:

```text
Blocking: Proposed delivery: Standard. Proceed?
Optimistic: Delivery: Standard (inferred). Say Prototype to override.
```

Use only ambiguous or asymmetric-cost prompts; explicit posture and ordinary issue/PR cases do not discriminate the variants. Measure correction cost, wasted implementation, user turns, and protection outcomes. Hardened proposals and consequential actions remain separately confirmable.

## 10. Runtime event tests

If Stage 2 justifies a delivery kernel, test:

- append-only set, override, and explicit clear tombstone;
- explicit versus inferred source;
- latest valid event on the active branch;
- resume and reload;
- fork inheritance at the correct point;
- abandoned-branch and tree restoration;
- unset behavior;
- compaction survival;
- sequential deliverable set/clear;
- status rendering with and without UI;
- no duplicate context messages;
- no project default;
- delegated handoff and authorization limits;
- narrow host-boundary hooks only for exact observable predicates.

## 11. Kill and simplify criteria

Simplify or reject the architecture if:

- the simple right-sizing instruction meets the H5 equivalence rule;
- Standard cannot meet its rubric reliably or collapses toward adjacent postures;
- runtime state introduces as many stale-state failures as drift failures it prevents;
- Prototype efficiency comes with a quality/protection regression;
- adaptive Hardened misses a material risk caught by the baseline;
- posture declaration adds more than 15% user-turn overhead without reducing correction cost or errors;
- capability guidance grows into three duplicated workflows;
- deterministic hooks cannot reach acceptable precision for their exact predicate;
- maintenance cost exceeds the observed delivery benefit.

## 12. Immediate next action

1. Create a short portable posture header.
2. Create only enough explore/design, debug, test/verify, and review guidance for Stage 1.
3. Build two sacrificial fixtures (one Prototype, one Standard) with hidden assertions, plus known-good and known-faulty artifacts for mechanical assertion validation.
4. Run the Stage 0 readiness gate (§3) in one pinned environment: two fixtures × three systems, defect detection only, within the hard cap.
5. Freeze header, fixtures, assertions, and environment; record infrastructure-validation results and owner-approved Stage 1 margins before expanding.

Do not build persistent state, a workflow engine, full Hardened coverage, or the complete capability library yet.
