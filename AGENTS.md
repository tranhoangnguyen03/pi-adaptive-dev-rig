# Agent guidance

This repository packages `pi-adaptive-dev`, a one-file Pi extension (see issue #5 and its binding v1 contract). The design corpus behind it lives in `spikes/` and is not published.

## Start here

Read completely, in order:

1. `README.md`
2. `spikes/docs/DECISIONS.md`
3. `spikes/docs/FOUNDATION.md`
4. `spikes/docs/RESEARCH.md`
5. `spikes/docs/EVALUATION.md`

`spikes/docs/DECISIONS.md` is authoritative. `spikes/docs/FOUNDATION.md` contains both accepted principles and clearly tagged provisional architecture. Do not silently convert recommendations or unresolved experiments into accepted decisions.

## Design constraints

- Preserve frontier-model judgment; add structure only for an observed failure or an explicit assurance need.
- Keep activity, delivery posture, and engineering capability independent.
- Profiles define outcomes and evidence strength, not mandatory procedures.
- Keep always-on context minimal and use progressive disclosure.
- Prefer code, tests, scripts, schemas, CI, and existing project artifacts over generated process prose.
- Materialize information only when it has a natural future consumer.
- Universal protections remain independent of posture, but distinguish host-enforceable boundaries, model-level invariants, and semantic risks requiring judgment.
- Do not build task IDs, task graphs, evidence ledgers, automatic plan files, or broad semantic gates in v1.
- Do not copy Pi-superpowers wholesale. Reuse its strongest techniques as selectively loaded capabilities.
- Evaluate against unaided Pi, current Pi-superpowers, and simpler alternatives before growing the runtime.

## Before implementation

Stage 0 and Stage 1 are complete (2026-08-30; Stage 0 record on D-014 and `spikes/eval/stage0/README.md`, Stage 1 verdicts in `spikes/eval/stage1/RESULTS.md`). The owner approved building the v1 extension (issue #5 comment); it exists at `extensions/right-sizing.ts` and passed an agy/codex/claude council review. v0.1.0 was instruction-only. By owner decision (2026-08-30, overriding the council's one-file cap), v0.2.0 bundles `pi-superpowers` (pinned `github:coctostan/pi-superpowers#c339ba2`, MIT) plus the instruction — the Stage-1-measured configuration. Published to npm as `pi-adaptive-dev`; the owner judges fitness qualitatively in daily use.

Do not commit, publish, or modify external repositories without explicit user direction.
