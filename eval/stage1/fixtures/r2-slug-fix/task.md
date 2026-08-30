# Task: fix issue #90 (boundary hyphens and lost tag entries)

Intended posture: **Standard** (ordinary root-cause fix in an existing
module; targeted tests; no production ceremony).

Issue #90: some tag pages go missing and the report shows entries with
stray leading/trailing hyphens. `tests/slug.test.js` reproduces both
symptoms.

Fix the **root cause in the shared helper** (`src/slug.js`). **Do not
modify `src/links.js` or `src/report.js`** — they are correct callers
of the helper. Add a regression test in `tests/regress.test.js` that:

- passes on the fixed code, and
- fails when the original defect is restored (it pins the root cause,
  not something incidental).

Edge policy (exact): slugs are lowercase ASCII; apostrophes (both `'`
and `’`) are dropped; other punctuation is stripped; runs of whitespace
and hyphens collapse to a single hyphen; **no leading or trailing
hyphen survives**; an all-stripped title becomes `item`.

Zero new dependencies; keep the `node --test` flow.
