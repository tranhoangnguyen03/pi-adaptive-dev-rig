// Shared slug generation for user-supplied titles.
export function slugify(title) {
  let s = String(title).toLowerCase();
  s = s.replace(/['’]/g, "");
  s = s.replace(/[^a-z0-9\s-]/g, "");
  s = s.trim().replace(/[\s-]+/g, "-");
  return s || "item";
}
