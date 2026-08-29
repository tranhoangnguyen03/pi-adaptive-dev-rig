# Task: promote the route-stats prototype into lib/

Intended posture: **Standard** (maintainable component following
repository patterns; targeted tests; no production ceremony).

Promote `scripts/prototype_totals.py` into `lib/totals.py` following the
repo patterns in README.md and exemplified by `lib/clean.py`. The
prototype stays the behavioral spec — **behavior must be preserved
exactly**:

Named behavior contract (policies are exact):

- Input is CSV text, rows of `route,status,ms`.
- A row is **malformed and skipped/counted** if it does not have exactly
  3 fields or `ms` is not parseable as float.
- A **duplicate line** — the exact `(route, status, ms)` triple already
  seen (string-exact route/status, float-exact ms) — is skipped and
  counted; **the first occurrence wins**.
- Output CSV: header `route,count,total_ms`, one row per route sorted by
  route name ascending, count = kept lines for that route, total_ms =
  sum of their `ms` formatted with `%g`.
- Empty input -> header line only. The number of skipped lines is
  reported separately from the CSV output.

Required API (so this is importable and testable):

- `lib/totals.py` exposes `summarize(text: str) -> Tuple[str, int]`
  returning `(csv_out, skipped_count)`.

Also required: `tests/test_totals.py` (unittest, repo style) covering at
least: dedup keep-first, malformed rows counted, empty input, and
sorted output. `scripts/prototype_totals.py` becomes a thin wrapper
calling `lib.totals.summarize` (or is removed — either is fine; state
which you chose in a one-line note in the PR description).

Out of scope: new dependencies, CLI flags, percentiles, logging.
