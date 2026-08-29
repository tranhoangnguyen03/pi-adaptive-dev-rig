# Task: fix issue #88 (duplicate rows across page boundaries)

Intended posture: **Standard** (ordinary root-cause fix in an existing
module; targeted tests; no production ceremony).

Issue #88: exports intermittently contain duplicate rows across page
boundaries; audit counts look wrong too. `tests/export.test.js`
reproduces both symptoms.

Fix the root cause (not the symptoms in one caller), keep both callers
correct, and add a regression test in `tests/regress.test.js` that:

- passes on the fixed code, and
- fails when the original defect is restored (i.e. it actually pins the
  root cause, not something incidental).

Edge policy (exact): the server cursor (README + src/server.js) is
exclusive — a page resumes strictly after the cursor id; page size 4;
ids `id-001..id-012`; order is preserved.

Zero new dependencies; keep the `node --test tests/` flow.
