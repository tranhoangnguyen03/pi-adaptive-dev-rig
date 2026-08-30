import test from "node:test";
import assert from "node:assert/strict";
import { loadConfig } from "../src/config.js";

test("defaults: timeout 5000, legacy off", () => {
  const c = loadConfig({});
  assert.equal(c.timeout, 5000);
  assert.equal(c.legacyMode, false);
});

test("LEGACY=1 enables legacy mode", () => {
  assert.equal(loadConfig({ LEGACY: "1" }).legacyMode, true);
});
