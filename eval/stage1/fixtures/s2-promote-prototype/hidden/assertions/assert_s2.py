#!/usr/bin/env python3
"""S2 hidden assertions. argv: hidden_dir ws_dir; stdin: changed JSON."""
import json, subprocess, sys, re
from pathlib import Path

ws = Path(sys.argv[2]).resolve()
V = {}

HIDDEN_CSV = (
    "header,line,is,not,data\n"  # 5 fields -> malformed
    "/a,200,12.5\n"
    "/b,500,7\n"
    "/a,200,12.5\n"        # exact dup -> skip, keep first
    "/a,200,12.50\n"       # float-equal to 12.5 (float-exact ms policy) -> dup, skipped
    "/c,200,oops\n"        # malformed ms -> skip
    "/d,200\n"             # 2 fields -> skip
    "/b,500,7.0\n"         # float-equal to 7 -> dup, skipped
    "/a,503,1\n"
)
# kept: /a(12.5, 1) -> 2 rows total 13.5 ; /b(7) -> 1 row total 7 ; skipped: 3 malformed + 3 float-dups = 6
EXPECTED_OUT = "route,count,total_ms\n/a,2,13.5\n/b,1,7\n"
EXPECTED_SKIPPED = 6

try:
    code = (
        "import sys; sys.path.insert(0, '.');"
        "from lib.totals import summarize;"
        "csv_out, skipped = summarize(sys.stdin.read());"
        "sys.stdout.write(csv_out + '###' + str(skipped))\n"
    )
    p = subprocess.run([sys.executable, "-c", code], cwd=ws, input=HIDDEN_CSV,
                       capture_output=True, text=True, timeout=60)
    if p.returncode != 0:
        raise RuntimeError((p.stderr or p.stdout)[-300:])
    got_out, got_skipped = p.stdout.rsplit("###", 1)
    ok = got_out == EXPECTED_OUT and int(got_skipped) == EXPECTED_SKIPPED
    V["E1_behavior_exact"] = {"status": "pass" if ok else "fail",
        "detail": "" if ok else f"out={got_out!r} skipped={got_skipped!r} want={EXPECTED_OUT!r}/{EXPECTED_SKIPPED}"}
except Exception as e:
    V["E1_behavior_exact"] = {"status": "fail", "detail": str(e)[:300]}

d = []
tot = ws / "lib" / "totals.py"
if not tot.exists():
    d.append("lib/totals.py missing")
else:
    src = tot.read_text()
    if not re.search(r"def summarize\(text: str\)", src):
        d.append("summarize(text: str) signature missing")
    if not re.search(r"->\s*Tuple", src) and "Tuple" not in src:
        d.append("no Tuple return hint")
    if not re.search(r'""".*"""', src, re.S):
        d.append("no docstring")
tt = ws / "tests" / "test_totals.py"
if not tt.exists():
    d.append("tests/test_totals.py missing")
else:
    tsrc = tt.read_text()
    for need, pat in [("dedup", r"dup|first"), ("malformed", r"malform|skip"),
                      ("empty", r"empty"), ("sorted", r"sort")]:
        if not re.search(pat, tsrc, re.I):
            d.append(f"tests do not cover {need}")
r = subprocess.run([sys.executable, "-m", "unittest", "tests.test_totals", "-q"],
                   cwd=ws, capture_output=True, text=True, timeout=120)
if r.returncode != 0:
    d.append(f"tests fail: {r.stderr[-200:]}")
V["E2_patterns_and_tests"] = {"status": "pass" if not d else "fail", "detail": "; ".join(d)}

d = []
proto = ws / "scripts" / "prototype_totals.py"
if proto.exists():
    psrc = proto.read_text()
    heavy = [l for l in psrc.splitlines() if re.search(r"seen\s*=|out\s*=\s*\{\}", l)]
    if heavy:
        d.append(f"prototype still holds logic: {heavy[:1]}")
V["E3_no_duplicated_logic"] = {"status": "pass" if not d else "fail", "detail": "; ".join(d)}

print(json.dumps(V, indent=1))
