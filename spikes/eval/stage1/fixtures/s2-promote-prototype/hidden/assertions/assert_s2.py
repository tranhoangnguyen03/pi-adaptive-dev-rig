#!/usr/bin/env python3
"""S2 hidden assertions. argv: hidden_dir ws_dir; stdin: changed JSON."""
import calendar, json, subprocess, sys, re
from pathlib import Path

ws = Path(sys.argv[2]).resolve()
V = {}

# hidden input + independent reference implementation
HOLIDAY_LINES = ["7-4", "12-25", "7-5", "2-29", "2-30", "13-1", "abc",
                 "", "   ", "1-1", "10-800", "6-15x", "3-9x"]
YEAR = 2025  # non-leap

def reference(year, lines):
    holidays, skipped = set(), 0
    for ln in lines:
        ln = ln.strip()
        if not ln:
            continue
        try:
            m, d = map(int, ln.split("-"))
            if not (1 <= m <= 12 and 1 <= d <= 31):
                raise ValueError
            if calendar.weekday(year, m, d) >= 5:
                continue
            holidays.add((m, d))
        except ValueError:
            skipped += 1
            continue
    rows = ["month,workdays"]
    for month in range(1, 13):
        days = calendar.monthrange(year, month)[1]
        wd = sum(1 for d in range(1, days + 1)
                 if calendar.weekday(year, month, d) < 5
                 and (month, d) not in holidays)
        rows.append(f"{month},{wd}")
    return "\n".join(rows) + "\n", skipped

WANT_OUT, WANT_SKIPPED = reference(YEAR, HOLIDAY_LINES)
assert WANT_SKIPPED == 7, f"self-check: expected 7 skipped, got {WANT_SKIPPED}"

try:
    code = ("import sys; sys.path.insert(0, '.');"
            "from lib.workdays import summarize;"
            "out, skipped = summarize(%d, sys.stdin.read());"
            "sys.stdout.write(out + '###' + str(skipped))\n" % YEAR)
    p = subprocess.run([sys.executable, "-c", code], cwd=ws,
                       input="\n".join(HOLIDAY_LINES),
                       capture_output=True, text=True, timeout=60)
    if p.returncode != 0:
        raise RuntimeError((p.stderr or p.stdout)[-300:])
    got_out, got_skipped = p.stdout.rsplit("###", 1)
    ok = got_out == WANT_OUT and int(got_skipped) == WANT_SKIPPED
    V["E1_behavior_exact"] = {"status": "pass" if ok else "fail",
        "detail": "" if ok else f"skipped={got_skipped!r} want {WANT_SKIPPED}; "
                                f"first diff at " +
                                next((f"row {a!r} vs {b!r}" for a, b in
                                      zip(got_out.splitlines(), WANT_OUT.splitlines())
                                      if a != b), "n/a")}
except Exception as e:
    V["E1_behavior_exact"] = {"status": "fail", "detail": str(e)[:300]}

d = []
mod = ws / "lib" / "workdays.py"
if not mod.exists():
    d.append("lib/workdays.py missing")
else:
    src = mod.read_text()
    if not re.search(r"def summarize\(year: int, holidays_text: str\)", src):
        d.append("summarize(year: int, holidays_text: str) signature missing")
    if not re.search(r"->\s*Tuple", src):
        d.append("no Tuple return hint")
    if not re.search(r'""".*"""', src, re.S):
        d.append("no docstring")
tt = ws / "tests" / "test_workdays.py"
if not tt.exists():
    d.append("tests/test_workdays.py missing")
else:
    tsrc = tt.read_text()
    for need, pat in [("weekend-holiday", r"weekend|satur|sunday"),
                      ("impossible-date", r"impossible|2-30|2-29|leap"),
                      ("weekday-holiday", r"holiday|7-4"),
                      ("empty", r"empty")]:
        if not re.search(pat, tsrc, re.I):
            d.append(f"tests do not cover {need}")
r = subprocess.run([sys.executable, "-m", "unittest", "tests.test_workdays", "-q"],
                   cwd=ws, capture_output=True, text=True, timeout=120)
if r.returncode != 0:
    d.append(f"tests fail: {r.stderr[-200:]}")
V["E2_patterns_and_tests"] = {"status": "pass" if not d else "fail", "detail": "; ".join(d)}

d = []
proto = ws / "scripts" / "prototype_workdays.py"
if proto.exists():
    psrc = proto.read_text()
    if re.search(r"monthrange|weekday\(", psrc):
        d.append("prototype still holds calendar logic")
V["E3_no_duplicated_logic"] = {"status": "pass" if not d else "fail", "detail": "; ".join(d)}

print(json.dumps(V, indent=1))
