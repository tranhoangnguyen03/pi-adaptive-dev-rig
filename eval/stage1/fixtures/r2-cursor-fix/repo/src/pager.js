// Shared cursor pagination for the demo API. Deterministic (no I/O):
// the "server" is a fixed list.
export class CursorPager {
  // pageAll(fetchPage): walks pages until next_cursor is null.
  // fetchPage(cursor) -> {items: [...], next_cursor: string|null}
  static pageAll(fetchPage) {
    const out = [];
    let cursor = null;
    while (true) {
      const page = fetchPage(cursor);
      out.push(...page.items);
      if (page.next_cursor == null) return out;
      // BUG (#88): the server cursor is exclusive, but we re-derive it
      // one id early — every next page re-serves the boundary row.
      const m = /^id-(\d+)$/.exec(page.next_cursor);
      cursor = `id-${String(Number(m[1]) - 1).padStart(3, "0")}`;
    }
  }
}
