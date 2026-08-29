import test from "node:test";
import assert from "node:assert/strict";
import { exportAll } from "../src/export.js";
import { audit } from "../src/audit.js";

// Issue #88: exports intermittently contain duplicate rows across page
// boundaries; audit counts look wrong too.
test("export returns each row exactly once, in order", () => {
  const ids = exportAll();
  assert.equal(ids.length, 12);
  assert.equal(new Set(ids).size, 12);
  assert.deepEqual(ids[0], "id-001");
  assert.deepEqual(ids[11], "id-012");
});

test("audit count and sum are correct", () => {
  assert.deepEqual(audit(), { count: 12, sum: 78, unique: 12 });
});
