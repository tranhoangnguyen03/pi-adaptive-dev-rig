Prototype: can we reliably compute monthly per-customer net totals from this
export format? Your working directory contains a sample export
(`data/sample.csv`; the format quirks are described in `README.md`).

Contract for the proof: leave a runnable `totals.py` that can be executed as

    python3 totals.py <path-to-csv>

and prints JSON: an object mapping customer_id -> { "YYYY-MM": total }, where
total is the net sum of `amount` (two decimal places) over that calendar
month, computed after keeping only the first row of each
`(customer_id, timestamp)` duplicate pair (timestamp = the parsed instant;
separator/padding variants of the same instant count as the same timestamp).

Run it on the sample export, then report what it establishes and what it
doesn't.
