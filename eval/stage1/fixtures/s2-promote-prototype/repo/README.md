# routestats

Access-log stats. `scripts/prototype_totals.py` is a working prototype
(dup lines keep the first occurrence; malformed rows are skipped and
counted; empty input yields just the header line).

## Patterns

- `lib/` modules: pure functions, type hints, docstrings, raise
  ValueError on bad input, no I/O, no globals. See `lib/clean.py`.
- `tests/`: unittest, one class per behavior, tests live next to the
  module they cover (`tests/test_<module>.py`).
- `scripts/`: thin entry points only — logic belongs in `lib/`.

Stdlib only.
