// Caller 2: sorted slug report (uses the shared slug helper too).
import { slugify } from "./slug.js";

export function slugReport(titles) {
  return [...new Set(titles.map(slugify))].sort();
}
