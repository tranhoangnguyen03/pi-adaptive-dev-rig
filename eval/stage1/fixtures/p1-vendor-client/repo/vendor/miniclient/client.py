"""Demo-service client. Deterministic; no I/O, no clocks.

Quirks (see vendor/README.md):
  * /items paginates with opaque next_cursor; follow until null.
  * Cursor page 4 rate-limits ONCE per Client instance; pass retries>=1
    to .get() to retry internally (the service recovers immediately).
  * Unknown cursors return HTTP 400 {"error": "bad_cursor"} — terminal.
"""
from . import routes


class ApiError(Exception):
    def __init__(self, status, payload):
        super().__init__(f"HTTP {status}: {payload}")
        self.status = status
        self.payload = payload


class RateLimitedError(ApiError):
    pass


class Response:
    def __init__(self, status, payload):
        self.status = status
        self.json = payload

    def ok(self):
        return self.status == 200


class Client:
    """One Client instance = one demo session (rate-limit state is per instance)."""

    def __init__(self):
        self._hit_rate_page = False

    def get(self, path, cursor=None, retries=0):
        if path != "/items":
            return Response(404, {"error": "not_found"})
        key = cursor or "start"
        pages = routes.page_chain()
        if key not in pages:
            return Response(400, {"error": "bad_cursor"})
        if key == routes.RATE_CURSOR and not self._hit_rate_page:
            self._hit_rate_page = True
            if retries < 1:
                raise RateLimitedError(429, {"error": "rate_limited", "retry_after": 1})
        items, nxt = pages[key]
        return Response(200, {"items": items, "next_cursor": nxt})
