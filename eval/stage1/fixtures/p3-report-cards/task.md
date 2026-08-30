# Task: one-page report proof

Intended posture: **Prototype** (idea proof — not production work).

Write `build_report.py` (single file, Python stdlib only) that builds
`report.html` from a metrics file.

Interface: `python3 build_report.py --input <file.json> --output <file.html>`.

Named criteria (exact edge policies — these are the spec):

- A record is **excluded** if: its `score` is missing/null or not a
  number, OR its `id` duplicates an earlier record's id (keep first,
  string-exact comparison). Everything else is included.
- The table has one row per included record, **sorted by score
  descending; ties broken by id ascending**.
- The totals row shows: exact sum of included scores and the count,
  both as they come out of the policy above (sum formatted to 2
  decimals, count as integer).
- A footnote line contains exactly `Excluded: N` with N the count of
  excluded records.
- Single file, stdlib only; no JavaScript; no external CSS (a small
  inline <style> block is fine); no template engine.

Explicitly out of scope (Prototype): pagination, charts, i18n,
streaming, HTML escaping beyond `&`, `<`, `>` (escape those three).
