# Pi Adaptive Dev Rig

An evidence-calibrated development harness for [Pi](https://github.com/earendil-works/pi).

## Status

**Design exploration. No implementation exists yet.**

This repository materializes the foundation developed through user interviews, landscape research, and independent reviews by Claude, Codex, and Antigravity.

## Product thesis

Pi-superpowers contains valuable engineering capabilities, but exposes them through a workflow that assumes high process rigor for nearly every change. That is appropriate for some hardened work and disproportionate for prototypes and ordinary, limited-scale development.

Pi Adaptive Dev Rig separates three concerns:

1. **Activity** — explore, design, troubleshoot, implement, review, promote.
2. **Delivery posture** — Prototype, Standard, or Hardened.
3. **Capability** — debugging, planning, testing, verification, review, isolation, delegation, and other techniques selected when useful.

> The posture defines the claim and evidence bar. The model chooses the least costly capabilities needed to support it.

This is a **jig, not an assembly line**: stable posture, progressive guidance, executable project truth, and narrow safety boundaries without a mandatory development sequence.

## Documents

Read these in order when starting a fresh design or implementation session:

1. [`docs/DECISIONS.md`](docs/DECISIONS.md) — authoritative status of accepted, recommended, unresolved, and deferred choices.
2. [`docs/FOUNDATION.md`](docs/FOUNDATION.md) — product, user experience, agent model, postures, and provisional architecture.
3. [`docs/RESEARCH.md`](docs/RESEARCH.md) — source material and candidate landscape.
4. [`docs/EVALUATION.md`](docs/EVALUATION.md) — staged experiments and falsification criteria required before expanding the system.

Agents should also read [`AGENTS.md`](AGENTS.md).

## Working vocabulary

- **Delivery posture:** the breadth and strength of evidence needed before making a delivery claim.
- **Prototype:** answer the key question with the smallest convincing implementation and visible limitations.
- **Standard:** make a maintainable repository change with targeted regression protection and fresh acceptance evidence.
- **Hardened:** establish defensible confidence against the material consequences of failure.
- **Capability:** an optional engineering technique, not a mandatory workflow phase.
- **Promotion:** deliberately move an existing deliverable to a stronger posture.
- **Posture header:** short portable guidance communicating the active posture and evidence rule.
- **Delivery kernel:** an optional Pi runtime extension for posture state, reconstruction, and UI, justified only if evaluation shows it prevents meaningful drift.

“Rig” names the product, “harness” names the system, and “jig” is its operating metaphor.

## Non-goals

The project is not intended to become:

- three duplicated workflows;
- an agent-managed Jira replacement;
- a mandatory plan/document generator;
- a universal TDD, worktree, or subagent policy;
- a label that substitutes for evidence;
- a broad policy engine attempting to mechanize engineering judgment.

## License

Apache-2.0 — see [LICENSE](LICENSE).

## Immediate next step

Stage 0 is complete and frozen (`eval/stage0/README.md`). Run the Stage 1 pilot per `docs/EVALUATION.md` §3 to decide whether the guidance architecture deserves a larger validation program; entry conditions and the Stage 1 handoff are recorded in `eval/stage0/README.md`. Do not build the delivery kernel or port the full Pi-superpowers skill suite upfront.
