// Caller 1: tag routes from titles (uses the shared slug helper).
import { slugify } from "./slug.js";

export function tagMap(titles) {
  const map = new Map();
  for (const t of titles) map.set(`tag:${slugify(t)}`, t);
  return map;
}
