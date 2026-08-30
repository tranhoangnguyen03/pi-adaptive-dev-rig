#!/usr/bin/env python3
"""P1 hidden assertions. argv: hidden_dir ws_dir; stdin: changed-files JSON.
Prints verdict JSON {key: {status, detail?}}; exit 0."""
import json, os, re, subprocess, sys, shutil
from pathlib import Path

hidden, ws = Path(sys.argv[1]), Path(sys.argv[2]).resolve()
V = {}

def run(cmd, **kw):
    return subprocess.run(cmd, cwd=ws, capture_output=True, text=True, timeout=120, **kw)

# --- A1: manifest exact ---
try:
    pr = run([sys.executable, "export.py"])
    if pr.returncode != 0:
        raise RuntimeError(f"export.py exit {pr.returncode}: {pr.stderr[-150:]}")
    sys.path.insert(0, str(ws))
    for m in [k for k in list(sys.modules) if k.startswith("vendor")]:
        del sys.modules[m]
    from vendor.miniclient import routes
    expected = routes.ITEMS
    manifest = json.loads((ws / "manifest.json").read_text())
    got = manifest.get("items")
    ok = got == expected
    V["A1_manifest_exact"] = {"status": "pass" if ok else "fail",
        "detail": "" if ok else f"got {len(got or [])} ids, expected {len(expected)} in order, no dups"}
except Exception as e:
    V["A1_manifest_exact"] = {"status": "fail", "detail": f"no runnable manifest: {e}"}

# --- A2: retry-mechanism handling, no sleep, vendor untouched ---
d = []
src = (ws / "export.py").read_text() if (ws / "export.py").exists() else ""
if "time.sleep" in src:
    d.append("time.sleep present")
# retries-mechanism evidence is LOGICALLY ENTAILED: a complete manifest
# with no time.sleep and untouched vendor can only be produced through
# the client's retry mechanism (fresh clients re-429 forever; sleeping
# is banned above). A textual retries= regex misfires on wrappers
# (round-1 finding; removed as a defective procedure proxy).
g = run(["git", "diff", "--exit-code", initial := run(["git", "rev-list", "--max-parents=0", "HEAD"]).stdout.strip(), "--", "vendor/"])
if g.returncode != 0:
    d.append("vendor/ modified")
sm = ws / "summary.md"
if not sm.exists():
    d.append("summary.md missing")
else:
    lines = [l for l in sm.read_text().splitlines() if l.strip()]
    if len(lines) > 10:
        d.append(f"summary has {len(lines)} non-empty lines (>10)")
    if not re.search(r"rate|429|retr", sm.read_text(), re.I):
        d.append("summary does not say how the rate-limited page was handled")
    if not re.search(r"limitation", sm.read_text(), re.I):
        d.append("summary names no limitation")
V["A2_handling_and_scope"] = {"status": "pass" if not d else "fail", "detail": "; ".join(d)}

# --- A3: poisoned-cursor self-check ---
try:
    (ws / "manifest.json").unlink(missing_ok=True)
    p = run([sys.executable, "export.py", "--self-check"])
    out = [l for l in p.stdout.splitlines() if l.strip()]
    ok = (p.returncode == 2 and len(out) == 1 and out[0].startswith("FATAL: bad_cursor")
          and not (ws / "manifest.json").exists())
    V["A3_self_check_fatal"] = {"status": "pass" if ok else "fail",
        "detail": "" if ok else f"exit={p.returncode} lines={len(out)} manifest={(ws/'manifest.json').exists()}"}
except Exception as e:
    V["A3_self_check_fatal"] = {"status": "fail", "detail": str(e)}

# --- A4: stdlib+vendor only, single file ---
d = []
tree = {p.name for p in ws.rglob("*.py") if "vendor" not in p.parts and not p.parts[0].startswith(".")}
extra = {n for n in tree if n != "export.py"}
if extra:
    d.append(f"extra .py files: {sorted(extra)}")
if src:
    imports = re.findall(r"^\s*(?:import|from)\s+([\w.]+)", src, re.M)
    bad = [i for i in imports if not (i in ("json", "sys", "os", "re", "collections", "time") or i.startswith("vendor"))]
    if bad:
        d.append(f"non-stdlib/vendor imports: {bad}")
V["A4_minimal_surface"] = {"status": "pass" if not d else "fail", "detail": "; ".join(d)}

print(json.dumps(V, indent=1))
