"""Deterministic demo-service route table. No I/O, no clocks."""
ITEMS = [f"item-{i:02d}" for i in range(1, 21)]  # item-01 .. item-20
PAGE_SIZE = 3
RATE_CURSOR = "c4"  # this page rate-limits once per Client instance

def page_chain():
    """cursor -> (items, next_cursor). Start cursor: "start"; end: next_cursor None."""
    chain, page = {}, 0
    for k in range(0, len(ITEMS), PAGE_SIZE):
        page += 1
        cur = "start" if page == 1 else f"c{page}"
        nxt = f"c{page + 1}" if k + PAGE_SIZE < len(ITEMS) else None
        chain[cur] = (ITEMS[k:k + PAGE_SIZE], nxt)
    return chain
