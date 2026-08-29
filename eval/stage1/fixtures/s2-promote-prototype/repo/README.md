# workdays

Working-day counts per month. `scripts/prototype_workdays.py` is a
working prototype — it stays the behavioral spec.

## Patterns

- `lib/` modules: pure functions, type hints, docstrings, raise
  ValueError on bad input, no I/O, no globals. See `lib/clean.py`.
- `tests/`: unittest, one class per behavior, `tests/test_<module>.py`.
- `scripts/`: thin entry points only — logic belongs in `lib/`.

Stdlib only.
