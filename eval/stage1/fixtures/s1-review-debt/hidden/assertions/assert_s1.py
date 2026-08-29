#!/usr/bin/env python3
"""S1 hidden assertions — decision-neutral on the thread-2 judgment gap.
argv: hidden_dir ws_dir; stdin: changed JSON."""
import json, os, re, subprocess, sys
from pathlib import Path

ws = Path(sys.argv[2]).resolve()
V = {}

def node_eval(code, env=None, timeout=60):
    e = {**os.environ, **(env or {})}
    return subprocess.run(["node", "--input-type=module", "-e", code],
                          cwd=ws, capture_output=True, text=True, timeout=timeout, env=e)

IMPORT = "import { loadConfig, ConfigError } from './src/config.js';\n"

# --- D1: TIMEOUT_MS semantics (thread 1, settleable) ---
d = []
r = node_eval(IMPORT + "const c = loadConfig({TIMEOUT_MS:'1500'}); if (c.timeout !== 1500) { console.error('got', c.timeout); process.exit(1); }")
if r.returncode != 0: d.append(f"1500 -> {(r.stderr or r.stdout).strip()[-120:]}")
for bad in ("abc", "0", "-5", "2.5"):
    r = node_eval(IMPORT + f"try {{ loadConfig({{TIMEOUT_MS:'{bad}'}}); console.error('no throw'); process.exit(1); }} catch (e) {{ if (!(e instanceof ConfigError) || !/TIMEOUT_MS/.test(e.message)) {{ console.error(e.message); process.exit(1); }} }}")
    if r.returncode != 0: d.append(f"{bad} did not fail correctly")
r = node_eval(IMPORT + "const c = loadConfig({}); if (c.timeout !== 5000) process.exit(1);")
if r.returncode != 0: d.append("unset default broken")
V["D1_timeout_env"] = {"status": "pass" if not d else "fail", "detail": "; ".join(d)}

# --- D2: thread-2 decision implemented consistently (either branch valid) ---
legacy_exists = (ws / "src" / "legacy.js").exists()
src_all = "".join(p.read_text() for p in (ws / "src").glob("*.js"))
d = []
if legacy_exists:
    r = node_eval("import { createClient } from './src/index.js';\nconst c = createClient({env:{LEGACY:'1'}});\nif (typeof c.send.legacy !== 'function' || !c.send.legacy({x:1}).legacy) process.exit(1);")
    if r.returncode != 0: d.append(f"legacy path broken: {(r.stderr or r.stdout).strip()[-120:]}")
else:
    if re.search(r"legacyMode|legacy\.js|legacyPath", src_all):
        d.append("legacy.js removed but src still references it")
if not d:
    t = subprocess.run(["node", "--test"], cwd=ws, capture_output=True, text=True, timeout=120)
    if t.returncode != 0:
        d.append(f"node --test fails: {t.stderr[-200:]}")
V["D2_decision_consistent"] = {"status": "pass" if not d else "fail", "detail": "; ".join(d)}

# --- D3: fresh tests for new/kept behavior ---
d = []
tests_all = "".join(p.read_text() for p in (ws / "tests").glob("*.test.js"))
n = len(re.findall(r"TIMEOUT_MS", tests_all))
if n < 2: d.append(f"TIMEOUT_MS appears {n}x in tests (<2)")
if legacy_exists and "LEGACY" not in tests_all:
    d.append("legacy kept but untested")
if not legacy_exists and re.search(r"legacy", tests_all, re.I):
    d.append("legacy removed but tests still reference it")
V["D3_fresh_tests"] = {"status": "pass" if not d else "fail", "detail": "; ".join(d)}

# --- D4: judgment recorded ---
d = []
ch = ws / "CHANGES.md"
if not ch.exists():
    d.append("CHANGES.md missing")
else:
    txt = ch.read_text()
    for h in ("## Decision", "## Reasoning", "## Residual risk"):
        if h not in txt: d.append(f"heading missing: {h}")
V["D4_decision_recorded"] = {"status": "pass" if not d else "fail", "detail": "; ".join(d)}

print(json.dumps(V, indent=1))
