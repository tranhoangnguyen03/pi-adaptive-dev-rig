import test from "node:test";
import assert from "node:assert/strict";
import { slugify } from "../src/slug.js";
import { tagMap } from "../src/links.js";
import { slugReport } from "../src/report.js";

// Issue #90: some tag pages go missing and the report shows entries
// with stray leading/trailing hyphens.
test("slug basics", () => {
  assert.equal(slugify("  Hello, World!  "), "hello-world");
  assert.equal(slugify("Don't Stop"), "dont-stop");
  assert.equal(slugify("Café?"), "caf");
});

test("no leading/trailing hyphens anywhere they can occur", () => {
  const titles = ["  Hello, World!  ", "Don't Stop", " -- leading -- "];
  for (const t of titles) {
    const s = slugify(t);
    assert.ok(!s.startsWith("-") && !s.endsWith("-"), `${s} has boundary hyphens`);
  }
});

test("tag map keeps every entry", () => {
  const titles = ["  Hello, World!  ", "Don't Stop", " -- leading -- "];
  const m = tagMap(titles);
  assert.equal(m.size, 3);
  assert.deepEqual([...m.keys()].sort(),
                   ["tag:dont-stop", "tag:hello-world", "tag:leading"]);
});

test("report has no boundary-hyphen entries", () => {
  const titles = [" -- leading -- ", "trailing --"];
  const report = slugReport(titles);
  assert.deepEqual(report, ["leading", "trailing"]);
});
