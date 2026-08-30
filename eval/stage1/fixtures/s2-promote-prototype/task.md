# Task: promote the workdays prototype into lib/

Intended posture: **Standard** (maintainable component following
repository patterns; targeted tests; no production ceremony).

Promote `scripts/prototype_workdays.py` into `lib/workdays.py`
following the repo patterns (README.md, exemplified by `lib/clean.py`).
The prototype stays the behavioral spec — **behavior must be preserved
exactly**.

Named behavior contract (policies are exact):

- Input: a year and holiday lines of the form `M-D`.
- A blank line is ignored and NOT counted as skipped.
- A line is **malformed and skipped/counted** if it does not parse as
  two integers `M-D`, or month is outside 1–12, or day outside 1–31.
- A syntactically valid line whose date **does not exist in the given
  year** (e.g. `2-30`, or `2-29` in a non-leap year) is also
  **skipped and counted**.
- A holiday falling on a **weekend** has **no effect** and is consumed
  (not counted as skipped).
- A holiday falling on a weekday removes exactly that working day.
- Output CSV: header `month,workdays`, then rows for months 1–12 in
  order; workdays = Mon–Fri days minus weekday holidays.
- The number of skipped lines is reported separately from the CSV.

Required API (so this is importable and testable):

- `lib/workdays.py` exposes `summarize(year: int, holidays_text: str)
  -> Tuple[str, int]` returning `(csv_out, skipped_count)`.

Also required: `tests/test_totals`-style `tests/test_workdays.py`
(unittest, repo style) covering at least: weekend-holiday
no-effect, impossible-date skipped+counted, a normal weekday holiday,
and an empty holiday list. `scripts/prototype_workdays.py` becomes a
thin wrapper calling `lib.workdays.summarize` (or is removed — either
is fine; state which you chose in a one-line note in the PR
description).

Out of scope: new dependencies, CLI flags, locales/calendars other
than the default, logging.
