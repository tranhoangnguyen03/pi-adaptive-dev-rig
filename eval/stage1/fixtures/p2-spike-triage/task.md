# Task: one spike for three tickets (#4, #5, #6)

Intended posture: **Prototype** (combined feasibility spike).

Deliver `spike.js` (Node, single file, zero dependencies) plus
`LIMITATIONS.md`. Minimal — this is a spike, not a library.

Named criteria (exact edge policies — these are the spec):

- `normalizePhone(s)`: strip all non-digits from the input; then
  exactly 10 digits -> `"+1"` + digits; exactly 11 digits starting
  with `1` -> `"+1"` + last 10 digits; anything else -> `null`.
- `parseDuration(s)`: concatenation of `<int><unit>` parts where unit
  is exactly `s`, `m`, or `h` (case-sensitive); returns total seconds
  (s=1, m=60, h=3600); any other character, a missing unit, or an
  empty string -> `null`. `"0s"` is valid and equals 0.
- `dedupeKeepFirst(pairs)`: input is an array of `[key, value]` pairs;
  keep the first pair per key in input order, drop later duplicates
  silently.

Interfaces (so the proof is checkable):

- `node spike.js --run-cases cases.json` reads
  `{"phone": [...], "duration": [...], "dedupe": [[k,v],...]}` and
  prints one line of JSON `{"phone":[...],"duration":[...],"dedupe":[...]}`
  with results in input order (`null` where a policy says null).
- `node spike.js` runs an internal self-check of at least three
  assertions and exits 0.

`LIMITATIONS.md`: at least two bullet lines naming what the spike does
NOT cover. No package.json, no dependencies, no files other than
`spike.js` and `LIMITATIONS.md`.
