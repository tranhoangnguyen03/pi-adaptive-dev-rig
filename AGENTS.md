# Agent guidance

This repository is currently a design corpus for Pi Adaptive Dev Rig. There is no approved implementation plan or code architecture yet.

## Start here

Read completely, in order:

1. `README.md`
2. `docs/DECISIONS.md`
3. `docs/FOUNDATION.md`
4. `docs/RESEARCH.md`
5. `docs/EVALUATION.md`

`docs/DECISIONS.md` is authoritative. `docs/FOUNDATION.md` contains both accepted principles and clearly tagged provisional architecture. Do not silently convert recommendations or unresolved experiments into accepted decisions.

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

The next session should implement only the Stage 0 evaluation materials described in `docs/EVALUATION.md`. A product implementation plan, persistent runtime state, or broad capability port waits for Stage 0/1 evidence.

Do not commit, publish, or modify external repositories without explicit user direction.
