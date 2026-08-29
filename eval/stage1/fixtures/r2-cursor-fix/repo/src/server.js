// Deterministic demo server: ids id-001..id-012, page size 4,
// cursor = last id of previous page, exclusive (returns id > cursor).
const ALL = Array.from({ length: 12 }, (_, i) => ({ id: `id-${String(i + 1).padStart(3, "0")}`, n: i + 1 }));
const SIZE = 4;

export function fetchPage(cursor) {
  let start = 0;
  if (cursor != null) {
    const m = /^id-(\d+)$/.exec(cursor);
    if (!m) throw new Error(`bad cursor: ${cursor}`);
    start = ALL.findIndex((x) => x.n === Number(m[1]) + 1); // exclusive
    if (start === -1) start = ALL.length;
  }
  const items = ALL.slice(start, start + SIZE);
  const last = items[items.length - 1];
  return { items, next_cursor: last && ALL.indexOf(last) < ALL.length - 1 ? last.id : null };
}
