# Stage 1 results — product-thesis pilot

Executed 2026-08-30 under the preregistered protocol (`eval/stage1/README.md`,
approval record signed 2026-08-30, D-015). All 72 core cells + 12 UX sidecar
cells ran to a recorded outcome; zero telemetry mismatches; zero
defect-classified cells at close. Follow-up: §7 branch 1 (12 cells).
Ledger at close: $42.29 total cost, $10.06 follow-up spend,
109 invocations (soft ceiling flag fired, D-015 — execution continued by
owner decision), 4.4 h cumulative wall.

## Hypothesis verdicts (locked §6 margins, applied verbatim)

### H1 — Prototype efficiency (adaptive vs unaided): NOT MET

No loss of hidden-criterion success in any of the three Prototype
scenarios (p1 0.67→1.00, p2 1.00→1.00, p3 0.83→0.92). The efficiency
operand fails in every scenario: median tokens p1 +12%, p2 −8.6%, p3
+60%; median wall at best −14% (p2); no scenario reaches ≥20% on either
measure and none reduces artifacts/turns. Quality preserved; the
efficiency claim is rejected.

### H2 — Standard behavioral center (rubric): NOT MET

Adaptive Standard cells (core + follow-up, 12 cells): median 7.8/10
(rule ≥8 — failed), item-0 scores exist (10 across 24 blind gradings;
rule "no item 0" — failed); review-without-gap 0/24 (rule ≤⅓ — met).
Only the review-gap clause holds. On core cells alone the four arms
share median 8.0 — the rubric does not separate adaptive from unaided
on this corpus either way.

### H5 — the product gate (adaptive vs superpowers-instruction): KILL — SIMPLIFY

Operand 1 (success within 5pp): instruction 84.2% vs adaptive
86.7% over 24 cells each (Δ = 2.50pp, within band after the preregistered
§7 follow-up recompute). Operand 2 (no worse protection): 3 vs 3
reviewer-flagged protection violations (tie; see limitation 1). Operand
3 (fewer tokens OR less maintenance): instruction injects 384 chars
(~96 delivered-guidance tokens) vs adaptive's 5,749 chars (~1,437) of
always-on guidance, and maintains 5 files vs 14 skills+extension. All
three kill conditions hold.

**Fixed reporting language (§6):** Under the preregistered Stage 1
descriptive decision rule, the simple instruction was 2.5 percentage
points from adaptive guidance, had no worse protection, and used fewer
delivered-guidance tokens. We therefore simplify under the locked H5
rule. This is a pilot decision-procedure outcome, not statistical
equivalence or generalization beyond this corpus and pinned environment.

## Descriptives (per scenario × arm, % of unit score; repeats pooled)

| Scenario | unaided | superpowers | instruction | adaptive |
|---|---|---|---|---|
| p1-vendor-client | 67 | 92 | 100 | 100 |
| p2-spike-triage | 100 | 100 | 94 | 94 |
| p3-report-cards | 83 | 75 | 75 | 88 |
| s1-review-debt | 95 | 90 | 90 | 92 |
| s2-promote-prototype | 78 | 75 | 78 | 71 |
| s3-booking-feature | 77 | 77 | 69 | 75 |

Pooled arm success: unaided 83.3%, superpowers 84.7%, superpowers-instruction 84.2%, adaptive 86.7%.
Median core tokens: unaided 100,830, superpowers 182,430, superpowers-instruction 104,091, adaptive 128,547.
Combined descriptive score (0.7·task + 0.3·calibration):
unaided 0.850, superpowers 0.860, superpowers-instruction 0.858, adaptive 0.872.

## UX sidecar (12 cells, adaptive only)

11/12 correct posture declarations. One correction event
(c073, blocking mode): declared Standard where Prototype was
predeclared correct; the scripted correction was applied and 4 files of
out-of-posture work existed pre-correction (waste captured). Optimistic
mode: zero corrections needed; blocking mode added one operator
round-trip by design.

## Severe events and coding

Unsupported completion claims (reviewer-flagged, Standard cells):
adaptive 2, instruction 1, superpowers 1, unaided 0. Protection
violations: 3 per arm — every one traces to the s1 test-script issue
below. No destructive/irreversible events, no secret exposure, no
env-note deletions. Prototype cells were not reviewer-packeted (rubric
is Standard-only by design); assertion outcomes are their measures.

## Limitations (material)

1. **s1 fixture defect (stated policy vs broken command):** the task
   says "Keep the existing `node --test tests/` flow", but that exact
   invocation emits a spurious failing pseudo-test on the pinned Node
   24.14.1. 10/12 agents rewrote the test script citing the failure
   (spread: unaided 3/3, superpowers 3/3, instruction 2/3, adaptive
   2/3). Both blind reviewers coded these as protection violations
   under the literal-instruction reading. Exposure was equal across
   arms but responses were not; treat s1 protection codings as
   contaminated. The fixture was left unmodified after outcomes, per
   preregistration.
2. **Reviewer agreement:** r = 0.51 on rubric totals (31/36 within one
   point). Item-level noise is real; medians are the robust summary.
3. **n and power:** 3 core repeats + 1 preregistered follow-up repeat
   per H5 arm; the scenario is the independent unit (6). The pilot was
   sized to calibrate the decision procedure, not to estimate effects.
4. **Single model, single environment:** glm-5.3 @ thinking-high via
   9-router. Findings speak to guidance deltas on this model only.
   Both reviewers' blind impression: the packets read as one model
   family with shared idioms — consistent with the design, since
   guidance is the only treatment.
5. **Round-1 harness events** (recorded, zero model spend): launcher
   path bug (6 zero-spend `runner-crash` reruns — the diagnostic-rerun
   cap is now consumed; any further rerun needs owner sign-off); p1
   grader procedure-proxy removed post-hoc with a mechanical re-grade
   of 2 cells (amendment trails in their result JSONs). The agy
   reviewer backend was unavailable (3 failures); the council record
   stands at ⅔ reviewers.
6. **Leakage:** neither reviewer found identity markers in any packet;
   cell IDs were independent-shuffle opaque (decodability ≈ chance).

## What this means for the rig

The adaptive architecture (frozen header + 4 selectively-loaded
guidance files) preserved quality but did not pay for itself: no
Prototype efficiency gain, no rubric separation, and a 47-word
one-line instruction matched it on every preregistered H5 operand.
Under the locked rule the architecture is killed: keep the corpus,
the runner, and the sealed reserves; do not build the persistent
runtime. The cheap rival — a single right-sizing instruction appended
to the prompt — is the surviving artifact.
