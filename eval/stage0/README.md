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

SHA-256 over every frozen Stage 0 file except this README and the manifest
itself (`freeze-manifest.txt` records the exact generating command; fixture
repo READMEs are included; bytecode excluded). Immutable workspace traces
are hashed separately in `../pi-adaptive-dev-rig-evalruns/stage0/manifest-traces.txt`.

## Run accounting (complete)

Model invocations, all recorded:
- **7 fixture runs** (cap 8): 6 base cells + 1 predeclared diagnostic rerun (P1, fixture failure).
- **5 step-0 mechanism probes** (tiny "Reply OK" calls, no fixture content): A-base,
  B-skill-with-ns, C-adaptive, D-rival, E-rival-extension.
- Cap interpretation (recorded for the owner): D-014's "6–8 total runs" governs
  fixture cells and their diagnostic reruns; mechanism probes belong to
  environment verification (EVALUATION §4 "before each stage, record exact
  versions…"), not the comparison matrix. Both classes are enumerated here so
  nothing is unrecorded.

## Freeze (completed 2026-08-30)

**Status: Stage 0 complete. Frozen.** 7 model runs total (≤8 cap): six base
cells + one predeclared diagnostic rerun (P1, fixture failure). Header
revision cycles used: **0 of 2** — the posture header ran defect-free and is
frozen as-is for Stage 1.

### Cell outcomes (defect detection; NOT hypothesis evidence)

| cell | system | fixture | assertions | wall | tokens | cost |
|---|---|---|---|---|---|---|
| P1 | unaided | prototype | A1 pass, A2 pass | 90s | 61,800 | $0.31 |
| P2 | superpowers-rival | prototype | A1 pass, A2 pass | 80s | 47,815 | $0.25 |
| P3 | adaptive | prototype | A1 pass, A2 pass | 160s | 90,694 | $0.48 |
| S1 | unaided | standard | H1 pass, H2 pass, H3 pass | 260s | 74,477 | $0.30 |
| S2 | superpowers-rival | standard | H1 pass, H2 pass, H3 pass | 96s | 90,975 | $0.30 |
| S3 | adaptive | standard | H1 pass, H2 pass, H3 pass | 227s | 208,763 | $0.65 |

(Telemetry corrected in remediation round 2 — session-canonical, stdout↔session
agreement 6/6; diagnostic-rerun attempt P1a: 84,439 tokens, $0.39.)

No cell exhibited a D11 defect (all exit 0, no timeouts, no harness
failures). Harness/fixture defects were found and fixed *within* the gate
(dedup ambiguity → diagnostic rerun; two assertion-mechanism defects →
mechanical re-grade of preserved workspaces, no reruns). Full traces:
`../pi-adaptive-dev-rig-evalruns/stage0/` (`summary.md`, `results/`,
`sessions/`, `stdout/`, `work/`, `ambiguities.md`).

### Remediation round 2 (post-freeze council review — codex/agy/claude, 2026-08-30)

Council verdict on the completed work: 2× REMEDIATE-FIRST, 1× APPROVE.
All remediations landed with **zero model runs**; findings verified before
fixing:

6. **Telemetry inflation (codex)** — streamed stdout events without message
   ids were double-counted (P1 123,600 vs true 61,800; P2 95,630 vs 47,815).
   Fixed: id-dedup (event-level ids) + end-only counting for id-less
   streams; stdout↔session agreement now holds 6/6 cells. Corrected costs:
   P1 $0.31, P2 $0.25, P3 $0.48, S1 $0.30, S2 $0.30, S3 $0.65 (attempt1 $0.39).
7. **Grader collision + workspace mutation (codex)** — hidden tests named
   `test_export.py`/`test_windows_edges.py` overwrote and then deleted the
   agents' own identically-named files in all three S workspaces. Fixed:
   reserved hidden names (`test_h1_hidden_export.py`, `test_h2_hidden_edges.py`)
   — collision-*resistant*, not absolutely collision-proof — and fully
   non-mutating grading in throwaway workspace copies (both fixtures as of
   round 3). Damaged agent files restored byte-exact from session
   transcripts (S1/S2/S3 `tests/test_export.py`).
8. **H3 could be satisfied by any nonzero exit (codex)** — a test failing
   even on the completed work certified "protection". Fixed: a changed test
   qualifies only if it PASSES on the work AND FAILS on pristine-lib revert.
   Re-grade: S1/S2/S3 H1/H2/H3 pass with every changed test genuinely
   certifying protection.
9. **Manifest/git hygiene (codex+agy)** — committed `__pycache__` untracked
   (`.gitignore` added); manifest regenerated path-anchored (fixture repo
   READMEs now included, bytecode excluded); false "runner's freeze step"
   attribution corrected; workspace traces hashed (`manifest-traces.txt`).
   A1 hardened against non-dict JSON shapes.

Also verified during remediation: rival prompts for P2/S2 contained the
right-sizing instruction (prompt-fidelity check); pinned superpowers clone
remains at `efe1d15`.

### Remediation round 3 (council pass 2, 2026-08-30 — final)

Codex's pass-2 nits, all zero-spend: README outcome table updated to the
corrected telemetry; prototype grading made non-mutating (throwaway copy,
matching the standard fixture); trace manifest regenerated after the final
ambiguities.md amendment with corrected scope note (work/ excluded as a
legitimately-amended artifact, not an immutable trace); manifest entry
counts reconciled (freeze manifest: 38 hashed entries + header; trace
manifest regenerated below). Freeze manifest regenerated (assert_proto.py
changed).

### Council decision (owner-delegated, pass 2)

Verdicts: agy APPROVE-FREEZE (flipped from REMEDIATE-FIRST), claude
APPROVE-FREEZE (held), codex APPROVE conditional on this round's mechanical
fixes. **Collective decision: freeze APPROVED; D14 margins adopted
verbatim** (EVALUATION.md §6 values including H1's protection clause and
H5's no-worse-protection clause; no margin derived from Stage 0 data);
recorded in docs/EVALUATION.md §6. Run-cap interpretation ratified
(7 fixture runs + 5 mechanism probes, all enumerated above).

### Stage 1 entry conditions

- Header, guidance, fixtures, assertions, environment: frozen (manifest
  above + this branch's commits).
- Owner review complete: D14 margins approved and recorded in
  `docs/EVALUATION.md` §6 (2026-08-30).
- Sacrificial fixtures remain excluded from Stage 1's scored set.

## Stage 1 handoff

For the agent implementing the Stage 1 pilot (`docs/EVALUATION.md` §3 Stage 1
/ §12). Entry conditions are met; this is the operating brief.

### Reuse as-is (frozen — mid-Stage-1 modification invalidates the comparison)

- `header/posture-header.md` — 0 of 2 revision cycles used; frozen.
- `systems/*.sh` — the three system invocations: symmetric stripped base;
  rival = pinned package as shipped (13 skills + extension) with the
  right-sizing instruction prompt-appended; adaptive = 4 guidance skills +
  header via `--append-system-prompt`.
- `runner/run.py` — `validate` gate (run before any model spend), `run`,
  `report`; JSONL telemetry extraction with message-id dedup.
- Graders — non-mutating (throwaway workspace copies), reserved hidden
  names, two-sided H3.

### Fixture-authoring rules (paid for in Stage 0 — findings #1–#3, #6–#8)

1. Assert only what the task text explicitly states; underdetermined edges
   are left unasserted.
2. Every edge-case policy (e.g. equal start/end semantics) must appear in
   the task/issue text itself, or it is not assertable.
3. Hidden artifacts use reserved names (`test_h1_*`, `test_h2_*`) so they
   cannot collide with agent-authored files.
4. Regression assertions are two-sided: pass on the completed work AND fail
   on the reverted defect.
5. Snapshot the workspace diff BEFORE injecting anything; grade only on
   disposable copies.
6. Cross-check telemetry per cell: stdout-derived totals must equal
   session-file totals.

### Stage 1 deltas (do not inherit Stage 0 defaults blindly)

- New scenarios from `docs/EVALUATION.md` §5; the two sacrificial fixtures
  are banned from the scored set.
- Four systems (adds current Pi-superpowers without the instruction).
- ≥3 repeats per system/scenario if cost permits; otherwise report the
  pilot as exploratory.
- Randomize run order (Stage 0's fixed order was non-evidentiary
  convenience only).
- Blinded grading against hidden assertions + the H2 rubric.
- Margins recorded in §6 are locked — never tuned after outcomes.

### Where the evidence lives

- Workspace: `../pi-adaptive-dev-rig-evalruns/stage0/` (results with
  in-file amendment trails, sessions, stdout, prompts, work/,
  `manifest-traces.txt`, `ambiguities.md`).
- Verify: `shasum -a 256 -c eval/stage0/freeze-manifest.txt` (repo root)
  and the trace manifest (workspace root).
- Cost calibration: ≈$2.7 for 7 small runs (largest cell 209k tokens /
  $0.65) — use for Stage 1 budgeting.
