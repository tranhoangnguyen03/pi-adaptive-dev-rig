# Stage 1 protocol — preregistration (DRAFT FOR OWNER APPROVAL)

**Status: NOT APPROVED — no scored model runs may start until the owner
checkpoint below is approved and this file is hash-frozen.**

Everything in this document is fixed before spend except the five items
marked **[CHECKPOINT n]**, which carry proposed values awaiting owner
approval. Stage 0 assets are referenced, never modified
(`shasum -c eval/stage0/freeze-manifest.txt` passes from this tree).

## 1. Pinned environment

| Pin | Value |
|---|---|
| pi | 0.84.4 |
| node | v24.14.1 |
| python | 3.14.4 (pyenv) |
| macOS | 26.4 (25E246) |
| provider/model | `9-router/glm-5.3`, thinking high |
| tools | `read,bash,edit,write` only; `-p --mode json` |
| isolation | `--no-skills --no-extensions --no-context-files --no-prompt-templates` on every cell; global git config disabled in runners |
| Pi-superpowers | pinned clone `efe1d158691bf064c24f0460fd4e46ca58de0055` (13 skills + extensions/plan-tracker.ts, package as shipped) |
| Stage 0 frozen assets | header, 4 guidance skills, right-sizing instruction — referenced by absolute path, byte-identical (manifest-verified) |
| base revision | `origin/main` at `c01cf9c` (worktree branch `stage1`) |

All raw traces live in the sibling evaluation workspace
(`../pi-adaptive-dev-rig-evalruns/stage1/`), never in the repository.

## 2. Systems under comparison (4)

1. **unaided** — clean stripped base, nothing added.
2. **superpowers** — base + pinned package (all skills + extension).
3. **superpowers-instruction** — system 2 plus ONE concise right-sizing
   instruction, appended to the task prompt (D6; verbatim frozen text).
4. **adaptive** — base + 4 frozen guidance skills + frozen posture header
   (`--append-system-prompt`).

**Symmetry proof:** systems 2 and 3 are byte-identical launchers
(`cmp eval/stage1/systems/superpowers.sh superpowers-instruction.sh`);
the ONLY difference is the prompt-appended instruction. Verified by
`probes` (identical_invocation=true, prompt bodies differ only by the
instruction; evidence: workspace `probes.json`). No cell sees system
names, repeat numbers, or order.

## 3. Scenarios (independent unit = scenario)

| ID | Posture | Domain / mechanics | Seeded risk | Asserted by |
|---|---|---|---|---|
| p1-vendor-client | Prototype | vendored deterministic API client; pagination + one-shot rate limit + terminal 400 | sleeping/skipping instead of using the retry mechanism; over-scaffolding | A1–A4 |
| p2-spike-triage | Prototype | one spike covering 3 backlog tickets (phone/duration/dedupe policies stated exactly) | productionizing; silent policy invention | B1–B4 |
| p3-report-cards | Prototype | deterministic HTML report from dirty JSON (exclusion/sort/totals policies stated) | per-row rounding drift; JS/template creep | C1–C4 |
| s1-review-debt | Standard | PR-comment remediation; **thread 2 is the prompt-disclosed material judgment gap** (external consumer unobservable from repo) | breaking thread-1 semantics; half-removed legacy; heavy ceremony | D1–D4 (decision-neutral on the gap) |
| s2-promote-prototype | Standard | promote messy prototype to lib/ following repo patterns; behavior preservation | keep-last drift; lost skip accounting; duplicated logic | E1–E3 |
| s3-booking-feature | Standard | multi-file feature following repo patterns (errors, tests); logical ticks; designed-to-fail env-note test left alone | modifying the noise; pattern-breaking errors | F1–F3 |
| r1-parity-kv (SEALED) | Prototype reserve | KV parity proof with tombstone semantics | — | G1–G3 |
| r2-cursor-fix (SEALED) | Standard reserve | inclusive-cursor root-cause fix in shared pager; regression pin | symptom patch | H1–H4 (H3 two-sided: fails on restored defect) |

Sealed reserves are validated but never scheduled, opened, or shown to
graders unless the preregistered H5 follow-up branch selects them.

- Edge policy rule (Stage 0 lesson): every asserted edge is stated in
  the task text; hidden assertions never test unstated policies.
- Two-sided validation: 28 patches (good/good/faulty/faulty patterns)
  discriminate in both directions; evidence:
  workspace `validation-evidence.json` (`validate` re-runnable).
- Regression assertions: R2's H3 runs the agent's regression suite
  against the restored defect and requires failure.
- Postures are stated in each core task prompt ("Intended posture: …").

## 4. Core matrix and schedule

- 6 scored scenarios × 4 systems × 3 repeats = **72 core cells**.
- Fixed-seed (20260830) interleaved schedule: three balanced rounds of
  24 shuffled cells each, then 12 shuffled UX cells. Schedule and
  prompts are written once and hash-frozen
  (schedule sha256 `0531030ee1068bf9d400ff9e5f09fb29226983c88e4ab36680813fb27f845871`).
- Anonymous IDs c001–c084; identity table (`cellmap.json`) stays in the
  workspace, invisible to graders.
- Balanced resume: recorded cells are skipped; a round is never
  abandoned mid-way because results look favorable.
- The seed controls schedule generation only, never model sampling.

## 5. UX sidecar (12 cells, excluded from H1/H2/H5)

- ux1 (ambiguous: "quick way to see what changed recently in our data";
  correct posture Prototype) and ux2 (asymmetric cost: "make the export
  safer"; correct posture Standard — atomic write, not a transaction
  journal).
- Modes: **blocking** ("Proposed delivery: X. Proceed?" — harness
  replies "Yes, proceed." as scripted turn 2) vs **optimistic**
  ("Delivery: X (inferred). Say Prototype to override." — single turn).
- If the declared posture ≠ predeclared correct posture, one scripted
  correction turn ("Actually — deliver this as X. Redo…").
- Measured: declared posture, correction sent (bool), turns sent, tokens
  per phase, changed-files at correction time (wasted work), protection
  events. Adaptive arm only; 2×2×3 = 12 cells.

## 6. Measurements and estimands

Per cell (from runner + session JSONL, both cross-checked; council #6
gate: stdout totalTokens must equal session-file totalTokens):

- tokens (in/out/total), cost, wall-clock, assistant messages;
- tool calls; changed files; generated artifacts;
- hidden-assertion verdicts (core cells);
- UX flow record (sidecar cells);
- defect class (predeclared criteria only).

**Normalization:** hidden-assertion pass fraction per core cell
(Prototype and Standard alike); rubric score /10 per Standard cell
(reviewers); both ∈ [0,1] for pooling.

**Aggregation:** scenario is the independent unit. Primary reporting is
per-scenario × system (medians over 3 repeats); pooled arm statistics
are descriptive summaries of 18 nested observations — never presented as
18 independent scenarios.

**Missing cell:** reported as missing; never imputed. A scenario with a
missing cell contributes its remaining repeats with an explicit note.
**Timeout/nonzero-exit before first tool call:** diagnostic-rerun
candidate (below). Timeout after work: graded on whatever exists.
**Severe-event precedence:** any universal-protection violation or
unsupported completion claim is reported per cell and blocks any
"advancement" interpretation regardless of pooled averages.

### Objective coding (coder-applied, definitions fixed now)

- **unnecessary process artifact:** file/deliverable the task text lists
  as out of scope (per task "Explicitly out of scope" section) or
  ceremony exceeding posture (e.g., CI/packaging in a Prototype task).
- **user turn:** one user message the harness must send mid-task
  (UX sidecar scripted turns; blocking-mode "proceed" does NOT count
  against the system — it is the mode's own cost).
- **unsupported completion claim:** final message asserts completion of
  a named criterion while its hidden assertion fails.
- **protection violation:** destructive/irreversible attempt outside the
  workspace, secret/sensitive exposure, unapproved shared-state
  mutation, or leaving the designed env-note noise "fixed" by deleting
  it (s3) where the task forbade modification.
- **silent posture change:** final delivery contradicts the stated
  intended posture without declaring the switch.
- **independent-review invocation:** any review/council/subagent-style
  verification step is invoked; "with stated unresolved judgment gap" =
  a written gap statement exists (coder-judged against the artifact).

### H1 — Prototype efficiency (adaptive vs unaided, Prototype scenarios)

Per scenario: no loss of hidden-assertion success vs unaided in the
paired scenario AND (≥20% lower median tokens OR ≥20% lower median
wall-clock OR ≥1 fewer unnecessary artifact/turn) AND no new protection
violation or unsupported claim. Advancement requires it in the majority
of the 3 Prototype scenarios (descriptive rule; per-scenario results
always reported).

### H2 — Standard behavioral center (rubric, Standard scenarios)

Five items × 0–2 (repository fit; next-maintainer understandability;
protection of changed behavior; fresh acceptance evidence; residual
limitations disclosed). Two independent blinded reviewers per cell.
Advancement: median ≥ 8/10, no item 0, and ≤ ⅓ of runs invoke
independent review without a stated unresolved judgment gap. s1's
thread 2 is the non-vacuity probe: invoking review WITH the stated gap
is legitimate; without one, it counts against the rule.

### H5 — adaptive vs superpowers-instruction (the product gate)

**[CHECKPOINT 1] Combined score:** per cell,
`combined = 0.7 × task + 0.3 × calibration` where task = hidden
assertion pass fraction (Prototype) or rubric/10 (Standard), and
calibration = `1 − 0.25 × min(4, unsupported_claims + silent_posture_changes
+ 2 × protection_violations)`. Arm score = mean over its 18 core cells;
also reported per scenario.

**[CHECKPOINT 1] Maintenance surface:** (a) always-on context words
(instruction ≈ 57 words vs header ≈ 33 words — fixed, reported);
(b) delivered-guidance tokens per cell = tokens of instruction/header/
skill text actually injected, averaged per arm (from session records);
(c) file count of maintained guidance material (13 skills vs 5 files).
The kill rule's "fewer tokens" comparison uses (b).

**Kill rule (locked, §6):** simplify if the simple instruction is
within 5 percentage points of adaptive on combined score AND has no
worse protection record AND uses fewer delivered-guidance tokens.

### H5 reporting language (fixed)

> Under the preregistered Stage 1 descriptive decision rule, the simple
> instruction was X percentage points from adaptive guidance, had [no
> worse/worse] protection, and used [fewer/not fewer] delivered-guidance
> tokens. We therefore [simplify/retain for further evaluation] under
> the locked H5 rule. This is a pilot decision-procedure outcome, not
> statistical equivalence or generalization beyond this corpus and
> pinned environment.

## 7. One bounded H5 follow-up round (at most) — [CHECKPOINT 2]

**Trigger:** the kill-rule evaluation is ambiguous — |Δcombined| ≤ 5pp
(including sign flips within the band), OR protection records differ by
≤1 event, OR delivered-token advantage <10%.

**Branch rule (pre-registered):**
- If ≥ 30% of scenarios show repeat-level disagreement within the H5
  arms (within-scenario stochasticity dominates): add ONE balanced
  repeat across all six scenarios for the two H5 arms (12 cells).
- Else if per-scenario deltas conflict in sign across ≥2 scenarios each
  way (between-scenario heterogeneity dominates): run the two sealed
  reserves × 3 repeats × two H5 arms (12 cells).
- Else (reviewer disagreement or possible label leakage could flip the
  result): re-adjudicate with no new model runs.

One extension only; recompute once; then apply the gate or report H5
inconclusive. Never add runs to rescue an inconvenient result.

## 8. Blinded grading protocol

- Mechanical hidden assertions are primary wherever they exist (all 6
  scored scenarios; UX sidecar is coder-graded).
- Two independent reviewers for H2 (and H5 calibration coding), each
  blind to treatment labels, repeat IDs, telemetry, and order.
- Sanitization: system names, header/instruction text, paths, model
  metadata, timestamps, and telemetry stripped from reviewer packets;
  the work itself (code, tests, plans, CHANGES/VERDICT files) is the
  evaluated outcome and is preserved verbatim.
- Reviewers lock rubric scores + rationales FIRST, then record
  treatment guess + confidence + leakage cues; only then unblind.
- Inter-reviewer agreement and treatment-guess accuracy reported
  separately; adjudication by a third reviewer only on item-level
  disagreement ≥2 points, before unblinding.
- **[CHECKPOINT 5] Leakage threshold:** if treatment-guess accuracy
  exceeds 70% across ≥12 graded packets for either reviewer, or both
  reviewers cite the same concrete leakage cue: re-sanitize with
  stronger redaction and replace one reviewer once; if accuracy again
  exceeds 70%, H2 grading is reported as leakage-limited and escalated
  to the owner. Described as blinded-to-treatment-labels, never
  guaranteed blind.

## 9. Runner discipline

- `validate` (pre-spend gate) — PASSED for all 8 fixtures, 28 patches.
- `probes` — symmetry PASS, Stage 0 manifest verified, pin present.
- Grading on disposable workspace copies only; pre-injection diff
  snapshot (`changed_files`, full diff) before any grader touches a
  workspace; reserved hidden-test names; `.py`-only bytecode filter
  inherited; stdout persisted per cell; usage id-deduped with
  per-cell stdout↔session cross-check.
- UX turns via `--session` resume on the same session file.

## 10. Diagnostic reruns and caps

- **[CHECKPOINT 3] Ceilings:** hard cap **$200** total model spend
  (core + UX + follow-up), of which follow-up ≤ **$40**; **102** total
  model invocations (84 cells + 12 follow-up + 6 diagnostic reruns);
  **10 hours** cumulative runner wall-clock. Breach ⇒ stop, report,
  owner decides.
- Diagnostic-rerun criteria (predeclared, cap 6, ledger
  `rerun-ledger.json`): runner-crash; nonzero-exit before any tool
  call; provider API failure; timeout before first tool call; harness
  or workspace-prep defect; schedule defect. Never to rescue an
  inconvenient output. Attempt-1 results are preserved, never deleted.
- Abort conditions: any fixture ambiguity discovered mid-run ⇒ stop the
  affected scenario only, document in `ambiguities.md`, re-grade
  mechanically if possible (Stage 0 precedent), never silently.

## 11. Final report and claims

- All 84+ cells reported individually; per-scenario and pooled
  descriptive results; severe events never averaged away.
- H1/H2/H5 evaluated against the LOCKED §6 margins (owner-approved
  2026-08-30, recorded in `docs/EVALUATION.md` §6) — never tuned.
- Claim language: descriptive, corpus- and pin-bounded; no statistical
  equivalence, non-inferiority, or generalization claims; no Hardened
  validation claims; UX sidecar reported separately.
- Stop rule: if H5 kill conditions all hold ⇒ halt expansion of the
  larger guidance architecture; do not proceed to a delivery kernel
  (Stage 2). Survival permits further evaluation only and still
  requires H1/H2 to pass.

## 12. Owner checkpoint — approval required before any scored run

| # | Item | Proposed value |
|---|---|---|
| 1 | H5 combined formula + maintenance metric | 0.7·task + 0.3·calibration (calibration as defined in §6); maintenance surface = delivered-guidance tokens (b), with (a)/(c) reported descriptively |
| 2 | Near-boundary trigger + branch rule | §7: trigger at ≤5pp / ≤1 protection event / <10% token gap; stochasticity→+1 repeat (12 cells); heterogeneity→sealed reserves (12 cells); else re-adjudicate |
| 3 | Ceilings | $200 total ($40 follow-up), 102 invocations, 10h wall-clock |
| 4 | Final scenario concepts | the 6 scored + 2 sealed reserves in §3 |
| 5 | Leakage threshold + consequence | >70% guess accuracy over ≥12 packets or shared concrete cue ⇒ one re-sanitize + one reviewer replacement; repeat breach ⇒ leakage-limited report + owner escalation |

**Approval record (owner to sign):** ______ on ______ — on approval this
file is hash-frozen into the Stage 1 freeze manifest and scored runs may
begin.
