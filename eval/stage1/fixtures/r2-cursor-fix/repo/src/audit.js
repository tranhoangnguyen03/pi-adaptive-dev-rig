// Caller 2: audit — count + checksum (uses the shared pager too).
import { CursorPager } from "./pager.js";
import { fetchPage } from "./server.js";

export function audit() {
  const rows = CursorPager.pageAll(fetchPage);
  const sum = rows.reduce((a, x) => a + x.n, 0);
  return { count: rows.length, sum, unique: new Set(rows.map((x) => x.id)).size };
}
