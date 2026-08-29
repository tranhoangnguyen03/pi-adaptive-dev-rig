#!/usr/bin/env python3
"""P3 hidden assertions. argv: hidden_dir ws_dir; stdin: changed JSON."""
import json, subprocess, sys, re
from html.parser import HTMLParser
from pathlib import Path

ws = Path(sys.argv[2]).resolve()
V = {}

# hidden input: ties, dup id, None/string/bool scores, 3-dp values, special chars
HIDDEN = [
    {"id": "h01", "name": "plain", "score": 10.5},
    {"id": "h02", "name": "tie-a", "score": 7.25},
    {"id": "h03", "name": "tie-b", "score": 7.25},
    {"id": "h04", "name": "a<b&c", "score": 3.0},
    {"id": "h05", "name": "neg", "score": -2.5},
    {"id": "h01", "name": "dup-should-drop", "score": 99.0},
    {"id": "h06", "name": "null-score", "score": None},
    {"id": "h07", "name": "str-score", "score": "high"},
    {"id": "h08", "name": "bool-score", "score": True},
    {"id": "h09", "name": "three-dp-a", "score": 1.005},
    {"id": "h10", "name": "three-dp-b", "score": 2.005},
    {"id": "h11", "name": "top", "score": 88.75},
]
def numeric(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)

seen, included, excluded = set(), [], 0
for r in HIDDEN:
    if not numeric(r["score"]) or r["id"] in seen:
        excluded += 1
        continue
    seen.add(r["id"])
    included.append(r)
order = sorted(included, key=lambda r: (-r["score"], r["id"]))
sum_input = f"{sum(r['score'] for r in included):.2f}"
sum_sorted = f"{sum(r['score'] for r in order):.2f}"

out = ws / ".grader_report.html"
inp = ws / ".grader_input.json"
inp.write_text(json.dumps(HIDDEN))
try:
    p = subprocess.run([sys.executable, "build_report.py", "--input", inp.name, "--output", out.name],
                       cwd=ws, capture_output=True, text=True, timeout=60)
    if p.returncode != 0:
        raise RuntimeError(f"exit {p.returncode}: {(p.stderr or p.stdout)[-200:]}")
    raw = out.read_text()
    rows_html = re.findall(r"<tr[^>]*>(.*?)</tr>", raw, re.S | re.I)

    class Tbl(HTMLParser):
        def __init__(self):
            super().__init__()
            self.rows, self._r, self._c = [], None, None
        def handle_starttag(self, tag, attrs):
            if tag == "tr": self._r = []
            if tag in ("td", "th") and self._r is not None: self._c = ""
        def handle_data(self, data):
            if self._c is not None: self._c += data
        def handle_endtag(self, tag):
            if tag in ("td", "th") and self._c is not None and self._r is not None:
                self._r.append(self._c.strip()); self._c = None
            if tag == "tr" and self._r is not None:
                self.rows.append(self._r); self._r = None

    t = Tbl(); t.feed(raw)
    id_rows = [r for r in t.rows if r and r[0] in {x["id"] for x in HIDDEN}]
    got_ids = [r[0] for r in id_rows]
    want_ids = [r["id"] for r in order]
    V["C1_rows_sorted"] = {"status": "pass" if got_ids == want_ids else "fail",
        "detail": "" if got_ids == want_ids else f"got {got_ids} want {want_ids}"}

    d = []
    m = re.search(r"Excluded:\s*(\d+)", raw)
    if not m or int(m.group(1)) != excluded:
        d.append(f"footnote Excluded: got {m and m.group(1)}, want {excluded}")
    bad_names = [n for n in ("dup-should-drop", "null-score", "str-score", "bool-score") if n in raw]
    bad_ids = [i for i in ("h06", "h07", "h08") if i in raw]
    if bad_names or bad_ids:
        d.append(f"excluded content leaked: {bad_names + bad_ids}")
    V["C3_exclusion_policy"] = {"status": "pass" if not d else "fail", "detail": "; ".join(d)}

    d = []
    if sum_input not in raw and sum_sorted not in raw:
        d.append(f"sum {sum_input}/{sum_sorted} not found")
    if str(len(included)) not in raw:
        d.append(f"count {len(included)} not found")
    V["C2_totals"] = {"status": "pass" if not d else "fail", "detail": "; ".join(d)}

    d = []
    if re.search(r"<script", raw, re.I): d.append("<script> present")
    if re.search(r"<link[^>]+stylesheet", raw, re.I): d.append("external stylesheet")
    if "&lt;" not in raw: d.append("special chars not escaped")
    pys = {q.name for q in ws.rglob("*.py") if not q.parts[0].startswith(".")}
    if pys - {"build_report.py", ".grader_report.html"}:
        d.append(f"extra .py files: {sorted(pys)}")
    src = (ws / "build_report.py").read_text()
    bad = [i for i in re.findall(r"^\s*(?:import|from)\s+([\w.]+)", src, re.M)
           if i.split(".")[0] not in ("json", "sys", "os", "re", "argparse", "html", "math", "collections")]
    if bad: d.append(f"non-stdlib imports: {bad}")
    V["C4_scope"] = {"status": "pass" if not d else "fail", "detail": "; ".join(d)}
except Exception as e:
    for k in ("C1_rows_sorted", "C2_totals", "C3_exclusion_policy", "C4_scope"):
        V[k] = {"status": "fail", "detail": f"run failed: {e}"}
finally:
    inp.unlink(missing_ok=True); out.unlink(missing_ok=True)

print(json.dumps(V, indent=1))
