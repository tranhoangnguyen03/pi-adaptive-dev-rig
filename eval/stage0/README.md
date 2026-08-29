# Stage 0 — pinned environment record and freeze manifest

Stage 0 is a **non-evidentiary readiness gate** (D-014): it builds Stage 1
prerequisites and removes mechanical defects. Nothing recorded here or in the
evaluation workspace is evidence for or against any hypothesis, cannot affect
advancement rules, margins, or H5, and never calibrates Stage 1 margins.

## Pinned environment (recorded 2026-08-29, before any fixture cell)

| Item | Value |
|---|---|
| Host | macOS 26.4 (25E246) |
| Pi CLI | 0.84.4 |
| Node | v24.14.1 |
| Python | 3.14.4 |
| Model | `9-router/glm-5.3`, `--thinking high`, identical for all six cells (owner decision D9) |
| Tool set | `--tools read,bash,edit,write`, identical for all systems |
| This repository | branch `stage0` from `main` @ `ee3568df7beb63259f67ab38a499c1b64cee158c` |
| pi-superpowers | `https://github.com/coctostan/pi-superpowers` @ `efe1d158691bf064c24f0460fd4e46ca58de0055`, MIT — fresh local clone into the evaluation workspace (live checkout is dirty: modified `package-lock.json`; untouched) |
| Evaluation workspace | `../pi-adaptive-dev-rig-evalruns/stage0/` (outside repository state, FOUNDATION §8.4) |

## System invocations (symmetric isolation — A1)

All three systems share an identical clean base:

```
pi -p --provider 9-router --model 9-router/glm-5.3 --thinking high \
    --tools read,bash,edit,write \
    --no-skills --no-extensions --no-context-files --no-prompt-templates \
    --session-dir <workspace>/sessions/<cell> --mode json --name stage0-<cell> \
    -- <prompt>
```

Differences are the tested treatment only:

1. **unaided** — base only.
2. **superpowers-rival** — base + 13 `--skill` flags (one per skill directory
   in the pinned clone's `skills/`, per package manifest) + `-e
   <clone>/extensions/plan-tracker.ts` (manifest-enabled extension; step 0
   probe E confirmed clean load) + the right-sizing instruction appended to
   the task prompt (D6: prompt-append).
3. **adaptive** — base + four `--skill` flags (explore-design, debug,
   test-verify, review) + `--append-system-prompt header/posture-header.md`.

Unaided semantics: clean stripped base for all systems (owner decision;
"normal harness without this package or Pi-superpowers" per EVALUATION §4 —
the owner's global plugin set is not part of any treatment).

## Step 0 mechanism probes (tiny calls, not fixture cells)

All probes exited 0 (`../pi-adaptive-dev-rig-evalruns/stage0/step0.json`):

- A-base: stripped flags + `-p` + `--mode json` → JSONL event stream on stdout;
  usage available per assistant `message` event (`usage.input/output/totalTokens/cost`).
- B-skill-with-ns: explicit `--skill` coexists with `--no-skills` — confirmed.
- C-adaptive: 4 guidance skills + header append — confirmed.
- D-rival: 13 superpowers skills — confirmed.
- E-rival-extension: + `plan-tracker.ts` via `-e` — confirmed clean load.

Telemetry note: `--mode json` emits JSONL, not a single object; the runner
sums usage across assistant messages (fallback documented if absent).

## Assertion validation gate (passed before any model cell)

`python3 runner/run.py validate` — mechanical discrimination proven in both
directions on both fixtures (known-good ×2 and known-faulty ×2 each):

- prototype-feasibility: A1 (hidden-sample exact output match via entrypoint
  contract), A2 (proportionality: ≤3 new files, no scaffolding).
- standard-rootcause: H1 (sibling caller `export`), H2 (root-cause contract
  edges), H3 (regression protection: ≥1 new-or-modified test fails on
  pristine-lib revert; pre-existing symptom test excluded from the check).

One assertion-mechanism misfire was found and fixed during validation
(verbose-output parser replaced with per-module exit codes) — recorded as a
Stage 0 infrastructure-validation result.

## Run matrix and caps

Fixed order P1 P2 P3 S1 S2 S3 (Stage 0 only — non-evidentiary; Stage 1 must
randomize order). Caps (D-014): 6 base runs + at most 2 diagnostic reruns
(8 total); at most 2 header revision cycles, then freeze.

D11 diagnostic-rerun criteria (predeclared): runner crash, pi nonzero
exit/crash, provider API failure, timeout before first tool call,
assertion-harness bug, workspace prep error, **header defect** (calibrated
artifact itself; a named Stage 0 defect class per EVALUATION §3). Never to
rescue undesirable model output.

## Decision log

- D9 model: `9-router/glm-5.3`, thinking high (owner).
- D6 rival instruction: appended to task prompt (owner).
- D14 Stage 1 margins: propose adopting EVALUATION §6 provisional values
  verbatim, including H1's "no new universal-protection violation or
  unsupported completion claim" and H5's "no worse protection record";
  owner-approved margins are recorded into `docs/EVALUATION.md` §6 before
  Stage 1 (§12 step 5). Stage 0 data plays no part.
- Unaided semantics: clean stripped base (owner).
- Council amendments A1–A11 (2026-08-29 review) applied.

## Freeze manifest

SHA-256 over every frozen Stage 0 file except this README (recorded at
freeze; see `freeze-manifest.txt` generated by the runner's freeze step).

## Freeze (completed after the six cells — see end of this file)
