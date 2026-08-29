#!/usr/bin/env python3
"""P2 hidden assertions. argv: hidden_dir ws_dir; stdin: changed JSON."""
import json, re, subprocess, sys
from pathlib import Path

ws = Path(sys.argv[2]).resolve()
V = {}

CASES = {
  "phone": ["(555) 010-9999", "5550108888", "15550107777", "555-010-666", "441234567890123", "abc", "555.010.666 x2"],
  "duration": ["90s", "1m30s", "2h", "1h1m1s", "45", "90S", "", "1m30", "0s"],
  "dedupe": [["a", "1"], ["b", "2"], ["a", "3"], ["c", "4"], ["b", "5"]],
}
EXPECTED = {
  "phone": ["+15550109999", "+15550108888", "+15550107777", None, None, None, "+15550106662"],
  "duration": [90, 90, 7200, 3661, None, None, None, None, 0],
  "dedupe": [["a", "1"], ["b", "2"], ["c", "4"]],
}
KEYS = ["phone", "duration", "dedupe"]

try:
    cf = ws / ".grader_cases.json"
    cf.write_text(json.dumps(CASES))
    p = subprocess.run(["node", "spike.js", "--run-cases", cf.name], cwd=ws,
                       capture_output=True, text=True, timeout=60)
    cf.unlink(missing_ok=True)
    if p.returncode != 0:
        raise RuntimeError(f"exit {p.returncode}: {(p.stderr or p.stdout)[-200:]}")
    lines = [l for l in p.stdout.splitlines() if l.strip()]
    got = json.loads(lines[-1])
    for i, k in enumerate(KEYS):
        V[f"B{i+1}_{k}_exact"] = {"status": "pass" if got.get(k) == EXPECTED[k] else "fail",
            "detail": "" if got.get(k) == EXPECTED[k] else f"got {json.dumps(got.get(k))[:200]}"}
except Exception as e:
    for i, k in enumerate(KEYS):
        V[f"B{i+1}_{k}_exact"] = {"status": "fail", "detail": f"run failed: {e}"}

d = []
src = (ws / "spike.js").read_text() if (ws / "spike.js").exists() else ""
if (ws / "package.json").exists():
    d.append("package.json present")
bad = re.findall(r"require\(['\"]([^'\"]+)['\"]\)|from\s+['\"]([^'\"]+)['\"]", src)
mods = {a or b for a, b in bad} - {"node:fs", "node:path", "fs", "path", "node:assert", "assert"}
if mods:
    d.append(f"non-builtin requires: {sorted(mods)}")
lim = ws / "LIMITATIONS.md"
if not lim.exists():
    d.append("LIMITATIONS.md missing")
else:
    bullets = [l for l in lim.read_text().splitlines() if l.strip().startswith(("-", "*"))]
    if len(bullets) < 2:
        d.append(f"LIMITATIONS.md has {len(bullets)} bullets (<2)")
V["B4_scope_and_limitations"] = {"status": "pass" if not d else "fail", "detail": "; ".join(d)}

print(json.dumps(V, indent=1))
