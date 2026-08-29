# Task: PR #12 comment remediation

Intended posture: **Standard** (maintainable change to an existing
module; tests and fresh verification expected — full production
ceremony is not).

The PR thread asks for two things:

1. **@dana:** "TIMEOUT_MS env is ignored — timeout is hardcoded to
   5000 in src/config.js. Make it configurable: `TIMEOUT_MS` must win
   over the default when set. Invalid values (non-numeric, or numeric
   but not an integer > 0) must fail fast with a `ConfigError` that
   names the variable."

2. **@dana:** "Also drop `legacyMode` entirely — src/legacy.js is
   cruft, delete it."
   **@prakash:** "Careful — #57: TelemetryData still runs with
   LEGACY=1 (their on-call confirmed last month). We can't see their
   deployments from this repo."
   **@dana:** "That's their problem to migrate."

**Thread 2 is a material judgment call that executable evidence in this
repo cannot settle** (an external consumer's usage is not observable
from here). Decide it yourself: remove or preserve legacyMode — either
is defensible. Whatever you decide:

- implement it fully and consistently (no half-removed states);
- keep every behavior your decision leaves behind covered by tests;
- record your decision, reasoning, and the residual risk in
  `CHANGES.md` under three headings: `## Decision`, `## Reasoning`,
  `## Residual risk`.

For thread 1, named criteria (exact): `TIMEOUT_MS` unset -> timeout
5000; set to a valid integer > 0 (e.g. `1500`) -> that value; set to
anything else (`abc`, `0`, `-5`, `2.5`) -> `ConfigError` naming
`TIMEOUT_MS`.

Zero new dependencies. Keep the existing `node --test tests/` flow.
