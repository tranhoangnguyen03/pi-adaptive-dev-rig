import test from "node:test";
import assert from "node:assert/strict";
import { BookingBook } from "../src/booking.js";
import { BookingConflictError, InvalidIntervalError } from "../src/errors.js";

test("add then list is sorted by start", () => {
  const b = new BookingBook();
  b.add("late", { start: 14, end: 15 });
  b.add("early", { start: 9, end: 10 });
  assert.deepEqual(b.list(), [{ start: 9, end: 10 }, { start: 14, end: 15 }]);
});

test("overlapping add rejects with BookingConflictError", () => {
  const b = new BookingBook();
  b.add("a", { start: 9, end: 10 });
  assert.throws(() => b.add("b", { start: 9.5, end: 10.5 }), BookingConflictError);
});

test("end <= start rejects with InvalidIntervalError", () => {
  assert.throws(() => new BookingBook().add("x", { start: 5, end: 5 }), InvalidIntervalError);
});
