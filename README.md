# pi-adaptive-dev

A [Pi](https://github.com/earendil-works/pi) package that bundles the
[pi-superpowers](https://github.com/coctostan/pi-superpowers) workflow skills
with the Stage-1-validated right-sizing instruction.

You get the full toolkit — 13 workflow skills plus the plan tracker — and one
instruction, appended to the system prompt on every agent start, that keeps the
toolkit sized to the task:

> Right-size the process to the task. Prototype/exploratory work needs only
> the smallest convincing implementation plus named limitations. Ordinary
> maintainable changes need targeted tests and fresh verification, not full
> production ceremony. Reserve comprehensive hardening for consequential or
> production-facing work. Skip heavyweight workflow phases the delivery claim
> doesn't need.
>
> Before claiming completion, run the relevant checks and cite fresh evidence.

In a preregistered head-to-head evaluation, superpowers + this instruction
matched both the bare-superpowers and full adaptive-architecture arms on every
preregistered operand, while halving superpowers' median token burn
(182k→104k) — the instruction suppresses package over-compliance. Verdicts and
limitations: [`spikes/eval/stage1/RESULTS.md`](spikes/eval/stage1/RESULTS.md).

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

- `extensions/right-sizing.ts` uses the documented `before_agent_start` hook;
  appends the instruction to the chained system prompt. Idempotent within a
  prompt chain; no persisted messages, no conversation mutation.
- `pi-superpowers` is bundled (MIT) and pinned at commit `c339ba2`: its 13
  skills and plan-tracker extension load from `node_modules/`. Update = change
  the pinned ref and republish.
- Installing this package replaces installing `pi-superpowers` separately.

## Verify

```bash
# package contents: extensions/ + bundled node_modules/pi-superpowers
npm pack --dry-run

# loads under Pi with no model spend (control: bogus path exits nonzero)
pi -e . --offline --no-session --mode rpc </dev/null
```

## Licenses

Apache-2.0 (this package) and MIT
([pi-superpowers](https://github.com/coctostan/pi-superpowers), bundled under
`node_modules/pi-superpowers/` with its LICENSE).

## Repository layout

The npm package is the repo root. Research, decisions, and evaluation
corpora live in [`spikes/`](spikes/RIG.md) and are not published.
