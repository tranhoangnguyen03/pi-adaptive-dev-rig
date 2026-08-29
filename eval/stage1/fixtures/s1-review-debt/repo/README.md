# conflow

Tiny flow config client. Node >= 20, zero dependencies, `node:test`.

## Consumers

- Internal services use `createClient` with default env.
- **TelemetryData** (external team) imports conflow with `LEGACY=1`
  (issue #57; their on-call confirmed usage last month). Coordinate
  with them before changing legacy behavior.
