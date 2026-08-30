# Task: parity proof for mini-kv

Intended posture: **Prototype** (feasibility proof — not production work).

Prove whether `FlatKV` and `LogKV` are behaviorally identical or not.

Named criteria (exact):

- `parity.js` (single file, Node, zero dependencies) exposes a runner:
  `node parity.js --ops ops.json` reads an array of ops
  `["set"|"del", key, value?]` and, for BOTH stores, applies them in
  order, then prints one line of JSON: `{"flat": [k, ...], "log": [k, ...]}`
  with each store's surviving keys (sorted), plus `"agree": true|false`.
  Surviving = present after all ops (a `get` returning undefined does
  not count; only the key set matters here).
- `node parity.js` (no args) runs an internal self-check with at least
  three assertions and exits 0.
- `VERDICT.md` (≤ 10 non-empty lines) states: identical or not; the
  smallest op-sequence that exhibits any divergence (or "none found");
  one limitation.

Edge policy (exact): ops are applied identically to both stores; `del`
of a missing key is a no-op; values are opaque; only final key sets are
compared for `agree`; duplicate `set`s are last-write-wins.

Out of scope (Prototype): performance, persistence, concurrency, value
comparison.
