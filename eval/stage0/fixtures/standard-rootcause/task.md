See issue #7 in this repository's tracker:

    Overnight maintenance windows are broken. Scheduling "reindex" for
    22:00->06:00 shows up as "invalid window" in `list`, and the nightly
    `export` silently drops every overnight row. Windows ending at "24:00"
    (e.g. 20:00->24:00) fail the same way. Same-day windows work fine.

Investigate and fix. Delivery: Standard.
