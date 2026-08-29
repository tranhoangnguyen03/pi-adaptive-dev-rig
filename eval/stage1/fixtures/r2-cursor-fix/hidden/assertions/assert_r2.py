#!/usr/bin/env python3
"""R2 hidden assertions (sealed reserve). argv: hidden_dir ws_dir."""
import json, shutil, subprocess, sys, re
from pathlib import Path

hidden, ws = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
V = {}

def node_eval(code):
    return subprocess.run(["node", "--input-type=module", "-e", code],
                          cwd=ws, capture_output=True, text=True, timeout=60)

# --- H1: both callers correct ---
r = node_eval("""
import { exportAll } from './src/export.js';
import { audit } from './src/audit.js';
const ids = exportAll();
const ok = ids.length === 12 && new Set(ids).size === 12 && ids[0] === 'id-001' && ids[11] === 'id-012';
const a = audit();
if (!ok || JSON.stringify(a) !== JSON.stringify({count:12,sum:78,unique:12})) {
  console.error(JSON.stringify({ids: ids.length, set: new Set(ids).size, a}));
  process.exit(1);
}
""")
V["H1_callers_correct"] = {"status": "pass" if r.returncode == 0 else "fail",
    "detail": "" if r.returncode == 0 else (r.stderr or r.stdout).strip()[-200:]}

# --- H2: root cause fixed in the shared pager ---
d = []
pager = ws / "src" / "pager.js"
src = pager.read_text() if pager.exists() else ""
if "slice(1)" in src: d.append("symptom-hiding slice(1) still in pager")
if "next_cursor" not in src: d.append("pager does not follow next_cursor")
g = subprocess.run(["git", "diff", "--exit-code",
                    subprocess.run(["git", "rev-list", "--max-parents=0", "HEAD"], cwd=ws,
                                   capture_output=True, text=True).stdout.strip(),
                    "--", "src/export.js", "src/audit.js"], cwd=ws, capture_output=True, text=True)
if g.returncode != 0: d.append("callers modified (fix belongs in the shared pager)")
V["H2_root_cause"] = {"status": "pass" if not d else "fail", "detail": "; ".join(d)}

# --- H3: regression test pins the root cause (two-sided) ---
graded_pager = pager.read_bytes()
try:
    d = []
    t = subprocess.run(["node", "--test", "tests/regress.test.js"], cwd=ws,
                       capture_output=True, text=True, timeout=120)
    if t.returncode != 0:
        d.append(f"regress suite fails on the work: {t.stderr[-150:]}")
    else:
        shutil.copy(hidden / "pristine-bug" / "pager.js", pager)
        t2 = subprocess.run(["node", "--test", "tests/regress.test.js"], cwd=ws,
                            capture_output=True, text=True, timeout=120)
        if t2.returncode == 0:
            d.append("regress suite PASSES with the defect restored (does not pin the bug)")
    V["H3_regression_pinned"] = {"status": "pass" if not d else "fail", "detail": "; ".join(d)}
finally:
    pager.write_bytes(graded_pager)

# --- H4: full suite green ---
t = subprocess.run(["node", "--test"], cwd=ws, capture_output=True, text=True, timeout=120)
V["H4_suite_green"] = {"status": "pass" if t.returncode == 0 else "fail",
    "detail": "" if t.returncode == 0 else t.stderr[-200:]}

print(json.dumps(V, indent=1))
