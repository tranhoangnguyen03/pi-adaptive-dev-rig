# Ops export — feasibility question

The nightly job drops a CSV export of customer transactions at
`data/sample.csv` with columns:

    customer_id,customer_name,timestamp,amount

Known properties of the exporter (observed, not documented upstream):

- Timestamps are calendar dates, sometimes with a time part. Separators vary:
  `2026-03-04`, `2026-3-4`, `2026-03-04T09:15`, `2026-03-04 09:15`.
  The date part is always year-month-day in that order. When no time is
  present, treat it as midnight.
- The exporter re-sends rows on retry. A re-send carries the **identical
  timestamp text** and identical fields; only the amount can differ (a
  corrected charge). Keep only the **first** occurrence of each
  `(customer_id, timestamp)` pair.
- Refunds are negative amounts. Amounts are decimals with two places.
- Customer names may contain non-ASCII characters and are not part of any
  key.

The open question: can we reliably compute **monthly per-customer net
totals** from this format — per calendar month of the timestamp — without a
heavy pipeline?
