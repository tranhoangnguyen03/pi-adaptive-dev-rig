#!/usr/bin/env python3
"""R2 hidden assertions (sealed reserve). argv: hidden_dir ws_dir."""
import json, shutil, subprocess, sys
from pathlib import Path

hidden, ws = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
V = {}

def node_eval(code):
    return subprocess.run(["node", "--input-type=module", "-e", code],
                          cwd=ws, capture_output=True, text=True, timeout=60)

r = node_eval("""
import { slugify } from './src/slug.js';
import { tagMap } from './src/links.js';
import { slugReport } from './src/report.js';
const cases = [["  Hello, World!  ", "hello-world"], ["Don't Stop", "dont-stop"],
               ["Don’t Stop", "dont-stop"], ["Café?", "caf"], [" -- leading -- ", "leading"],
               ["trailing --", "trailing"], ["!!!", "item"], ["", "item"]];
for (const [input, want] of cases) {
  const got = slugify(input);
  if (got !== want) { console.error(JSON.stringify({input, got, want})); process.exit(1); }
}
const titles = ["  Hello, World!  ", "Don't Stop", " -- leading -- "];
const m = tagMap(titles);
if (m.size !== 3 || JSON.stringify([...m.keys()].sort()) !== JSON.stringify(["tag:dont-stop","tag:hello-world","tag:leading"])) {
  console.error('tagMap broken'); process.exit(2);
}
if (JSON.stringify(slugReport([" -- leading -- ", "trailing --"])) !== JSON.stringify(["leading","trailing"])) {
  console.error('report broken'); process.exit(3);
}
""")
V["H1_callers_correct"] = {"status": "pass" if r.returncode == 0 else "fail",
    "detail": "" if r.returncode == 0 else (r.stderr or r.stdout).strip()[-200:]}

d = []
slug = ws / "src" / "slug.js"
src = slug.read_text() if slug.exists() else ""
for caller in ("links.js", "report.js"):
    cs = ws / "src" / caller
    if cs.exists() and ("replace(" in cs.read_text() or "startsWith('-')" in cs.read_text()):
        d.append(f"symptom masking inside {caller}")
g = subprocess.run(["git", "diff", "--exit-code",
                    subprocess.run(["git", "rev-list", "--max-parents=0", "HEAD"], cwd=ws,
                                   capture_output=True, text=True).stdout.strip(),
                    "--", "src/links.js", "src/report.js"], cwd=ws, capture_output=True, text=True)
if g.returncode != 0:
    d.append("callers modified (fix belongs in the shared helper)")
V["H2_root_cause"] = {"status": "pass" if not d else "fail", "detail": "; ".join(d)}

graded = slug.read_bytes()
try:
    d = []
    t = subprocess.run(["node", "--test", "tests/regress.test.js"], cwd=ws,
                       capture_output=True, text=True, timeout=120)
    if t.returncode != 0:
        d.append(f"regress suite fails on the work: {t.stderr[-150:]}")
    else:
        shutil.copy(hidden / "pristine-bug" / "slug.js", slug)
        t2 = subprocess.run(["node", "--test", "tests/regress.test.js"], cwd=ws,
                            capture_output=True, text=True, timeout=120)
        if t2.returncode == 0:
            d.append("regress suite PASSES with the defect restored (does not pin the bug)")
    V["H3_regression_pinned"] = {"status": "pass" if not d else "fail", "detail": "; ".join(d)}
finally:
    slug.write_bytes(graded)

t = subprocess.run(["node", "--test"], cwd=ws, capture_output=True, text=True, timeout=120)
V["H4_suite_green"] = {"status": "pass" if t.returncode == 0 else "fail",
    "detail": "" if t.returncode == 0 else t.stderr[-200:]}

print(json.dumps(V, indent=1))
