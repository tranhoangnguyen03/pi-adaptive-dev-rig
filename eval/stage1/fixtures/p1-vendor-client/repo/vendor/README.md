# vendored: miniclient (demo service)

Import as `vendor.miniclient`. Deterministic; no network, no clocks.

- `Client.get("/items", cursor=..., retries=...)` follows opaque cursors.
- Pagination: start at `cursor=None`, follow `next_cursor` until `null`.
- One rate-limited page exists (page 4). It 429s once per Client
  instance; pass `retries>=1` to ride through via internal retry.
  The service recovers immediately — never sleep.
- Unknown cursor -> HTTP 400 `{"error": "bad_cursor"}` (terminal).
