#!/usr/bin/env python3
"""R1 hidden assertions (sealed reserve). argv: hidden_dir ws_dir."""
import json, subprocess, sys, re
from pathlib import Path

ws = Path(sys.argv[2]).resolve()
V = {}

OPS1 = [["set", "a", 1], ["set", "b", 2], ["del", "a"], ["set", "a", 9],
        ["del", "zz"], ["set", "c", 3], ["del", "b"], ["set", "b", 7],
        ["del", "c"]]
OPS2 = [["set", "x", 1], ["set", "x", 2], ["set", "y", 0], ["del", "y"],
        ["del", "x"], ["set", "x", 5], ["set", "z", 9]]
CASES = [(OPS1, ["a", "b"]), (OPS2, ["x", "z"])]

d = []
for i, (ops, want) in enumerate(CASES):
    cf = ws / f".grader_ops{i}.json"
    cf.write_text(json.dumps(ops))
    try:
        p = subprocess.run(["node", "parity.js", "--ops", cf.name], cwd=ws,
                           capture_output=True, text=True, timeout=60)
        if p.returncode != 0:
            raise RuntimeError(f"exit {p.returncode}: {(p.stderr or p.stdout)[-150:]}")
        lines = [l for l in p.stdout.splitlines() if l.strip()]
        got = json.loads(lines[-1])
        if got.get("flat") != want or got.get("log") != want or got.get("agree") is not True:
            d.append(f"case{i}: got {json.dumps(got)[:150]} want flat=log={want}, agree=true")
    except Exception as e:
        d.append(f"case{i}: {e}")
    finally:
        cf.unlink(missing_ok=True)
V["G1_runner_exact"] = {"status": "pass" if not d else "fail", "detail": "; ".join(d)}

try:
    p = subprocess.run(["node", "parity.js"], cwd=ws, capture_output=True, text=True, timeout=60)
    V["G2_self_check"] = {"status": "pass" if p.returncode == 0 else "fail",
                          "detail": "" if p.returncode == 0 else f"exit {p.returncode}"}
except Exception as e:
    V["G2_self_check"] = {"status": "fail", "detail": str(e)}

d = []
vd = ws / "VERDICT.md"
if not vd.exists():
    d.append("VERDICT.md missing")
else:
    txt = vd.read_text()
    lines = [l for l in txt.splitlines() if l.strip()]
    if len(lines) > 10: d.append(f"{len(lines)} lines (>10)")
    if not re.search(r"identical|differ|diverg", txt, re.I): d.append("no verdict stated")
    if not re.search(r"limitation", txt, re.I): d.append("no limitation")
V["G3_verdict"] = {"status": "pass" if not d else "fail", "detail": "; ".join(d)}

print(json.dumps(V, indent=1))
