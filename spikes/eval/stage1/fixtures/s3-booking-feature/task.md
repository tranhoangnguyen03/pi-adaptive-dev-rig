# Task: reservation holds on BookingBook

Intended posture: **Standard** (multi-file feature following repository
patterns; targeted tests; no production ceremony).

Add reservation holds to `src/booking.js` (same class — follow how the
module is structured today):

Named behavior contract (policies are exact — no real clocks; ticks are
logical integers):

- `hold(slotId, spec, { forTicks })` books `slotId` (a booking id) with
  a hold that expires after exactly `forTicks` **logical ticks**.
  `forTicks` must be an integer >= 0 (else `InvalidIntervalError`).
- A hold occupies the slot exactly like a booking for overlap checks.
- `book.tick(n = 1)` advances logical time by `n` ticks (n integer >= 1;
  else `InvalidIntervalError`). A hold is **expired** once its
  remaining ticks reach 0 — at exactly 0 remaining the hold is gone.
- `confirm(slotId)` converts an active hold into a normal booking
  (identity of the interval is preserved). On an expired or missing
  hold: `HoldExpiredError`. On a slot never held: `HoldExpiredError` as
  well (callers treat both as "nothing to confirm").
- An expired hold's slot becomes freely bookable again.
- `holds()` lists active holds (any stable order) as
  `{ id, start, end, remaining }`.

Follow repo patterns: new error kinds (`HoldExpiredError`, and reuse
`InvalidIntervalError` for bad tick/forTicks inputs) go in
`src/errors.js` as `BookingError` subclasses; tests in
`tests/holds.test.js` (`node:test` style) covering at least: hold+
confirm, expiry-at-exactly-0, hold blocks overlapping add, invalid
forTicks. Zero dependencies.

Note: `tests/env-note.test.js` fails locally by design (README, CI
notes). Leave it exactly as it is; do not let it mask or fail your
work — `node --test tests/holds.test.js` is the natural check.
