// Config loading for conflow.
export class ConfigError extends Error {}

export function loadConfig(env = process.env) {
  // Timeout is hardcoded — see PR #12 thread (review comment from @dana).
  return {
    timeout: 5000,
    legacyMode: env.LEGACY === "1",
  };
}
