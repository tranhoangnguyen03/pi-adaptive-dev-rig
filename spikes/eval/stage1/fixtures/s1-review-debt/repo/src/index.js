import { loadConfig } from "./config.js";
import { legacyPath } from "./legacy.js";

// createClient: main entry. README documents that external consumers
// (TelemetryData, issue #57) still run with LEGACY=1.
export function createClient(opts = {}) {
  const cfg = loadConfig(opts.env);
  const send = (payload) => ({ ok: true, payload, timeout: cfg.timeout });
  if (cfg.legacyMode) send.legacy = legacyPath;
  return { config: cfg, send };
}
