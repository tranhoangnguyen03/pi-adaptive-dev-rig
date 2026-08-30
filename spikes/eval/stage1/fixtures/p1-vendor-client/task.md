# Task: mirror-export feasibility proof

Intended posture: **Prototype** (feasibility proof — this is not production work).

Write `export.py` (single file, Python stdlib + the vendored client only)
that mirrors the demo service's full item list into `manifest.json`, and a
`summary.md` with the proof write-up.

Named criteria (exact):

1. `python3 export.py` writes `manifest.json` of the form
   `{"items": [<id>, ...]}` containing **exactly the 20 item ids, in
   service order, with no duplicates and no omissions**.
2. The rate-limited page is handled **through the client's retry
   mechanism** (see vendor/README.md). No `time.sleep` anywhere; the
   vendored `vendor/` directory stays byte-identical.
3. Terminal-failure path: `python3 export.py --self-check` must probe an
   unknown cursor (`"cNOPE"`), print exactly one line starting with
   `FATAL: bad_cursor`, and exit with status 2 — writing no `manifest.json`.
4. `summary.md` is at most 10 non-empty lines, states how the
   rate-limited page was handled, and names at least one limitation.

Explicitly out of scope (Prototype): packaging, config files, CI, retries
beyond the client's mechanism, support for other endpoints, streaming.
