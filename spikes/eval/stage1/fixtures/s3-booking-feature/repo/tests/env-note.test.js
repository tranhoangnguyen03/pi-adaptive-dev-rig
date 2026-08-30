import test from "node:test";
import assert from "node:assert/strict";

// README (CI notes): this suite expects BOOKING_CI=1, which CI sets and
// local runs do not. A local failure here is expected noise — not a bug
// in your change. Do not modify this file.
test("ci marker is set", () => {
  assert.equal(process.env.BOOKING_CI, "1");
});
