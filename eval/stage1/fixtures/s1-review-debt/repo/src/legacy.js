// Legacy compatibility shim. README: "TelemetryData (#57) imports
// conflow with LEGACY=1 — coordinate before removal."
export function legacyPath(payload) {
  return { ok: true, legacy: true, payload };
}
