# pi-adaptive-dev

A [Pi](https://github.com/earendil-works/pi) extension that right-sizes the
development process to the task — with one file and one hook.

On every agent start it appends this block to the system prompt:

> Right-size the process to the task. Prototype/exploratory work needs only
> the smallest convincing implementation plus named limitations. Ordinary
> maintainable changes need targeted tests and fresh verification, not full
> production ceremony. Reserve comprehensive hardening for consequential or
> production-facing work. Skip heavyweight workflow phases the delivery claim
> doesn't need.
>
> Before claiming completion, run the relevant checks and cite fresh evidence.

That's the entire product. No commands, tools, state, UI, telemetry, or
workflow phases.

## Why this exists

It replaced a 14-file adaptive postures/capabilities architecture and a
13-skill workflow package. In a preregistered head-to-head evaluation
(6 scenarios × 3 arms), the frozen instruction matched the full architecture
on every preregistered operand while delivering ~96 vs ~1,437 guidance
tokens, and halved median token burn at equal quality. Verdicts and
limitations: [`spikes/eval/stage1/RESULTS.md`](spikes/eval/stage1/RESULTS.md).

The final sentence (fresh verification before completion claims) is an
owner-approved refinement added after the trial; see
[`spikes/docs/DECISIONS.md`](spikes/docs/DECISIONS.md).

## Install

```bash
pi install npm:pi-adaptive-dev
```

Try it without installing:

```bash
pi -e npm:pi-adaptive-dev
```

Or load from a checkout:

```bash
pi -e ./path/to/pi-adaptive-dev-rig
```

## Behavior

- Uses the documented `before_agent_start` hook; appends to the chained
  system prompt and returns it. Nothing persisted, no conversation mutation.
- Idempotent within a prompt chain: if the block is already present
  (e.g. extension loaded twice), it makes no modification.
- Single runtime file: `extensions/right-sizing.ts` — type-only import, no
  dependencies, no I/O.

## Verify

```bash
# package contents: only extensions/, README, LICENSE, package.json
npm pack --dry-run

# loads under Pi with no model spend (control: bogus path exits nonzero)
pi -e . --offline --no-session --mode rpc </dev/null
```

## Repository layout

The npm package is the repo root. Research, decisions, and evaluation
corpora live in [`spikes/`](spikes/RIG.md) and are not published.

## License

Apache-2.0 — see [LICENSE](LICENSE).
