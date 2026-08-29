# booking

Deterministic booking core: no clocks, no I/O, no dependencies
(Node >= 20, `node:test`).

## Patterns

- Errors: extend the matching `BookingError` subclass in `src/errors.js`
  (add new subclasses there when a new failure kind appears).
- Tests: `node:test` + `assert/strict` in `tests/*.test.js`, one
  behavior per test.
- `src/schedule.js` shows how callers use the module.

## CI notes

`tests/env-note.test.js` asserts `BOOKING_CI=1`; CI sets it, local runs
do not. The local failure is expected noise — leave that file alone.
