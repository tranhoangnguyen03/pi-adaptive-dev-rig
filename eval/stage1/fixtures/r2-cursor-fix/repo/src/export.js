// Caller 1: export all rows (uses the shared pager).
import { CursorPager } from "./pager.js";
import { fetchPage } from "./server.js";

export function exportAll() {
  return CursorPager.pageAll(fetchPage).map((x) => x.id);
}
