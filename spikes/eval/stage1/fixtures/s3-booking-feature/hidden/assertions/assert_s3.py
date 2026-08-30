#!/usr/bin/env python3
"""S3 hidden assertions. argv: hidden_dir ws_dir; stdin: changed JSON."""
import hashlib, json, os, re, subprocess, sys
from pathlib import Path

ws = Path(sys.argv[2]).resolve()
V = {}

def node_eval(code, timeout=60):
    return subprocess.run(["node", "--input-type=module", "-e", code],
                          cwd=ws, capture_output=True, text=True, timeout=timeout)

IMPORT = "import { BookingBook } from './src/booking.js';\nimport { HoldExpiredError, InvalidIntervalError, BookingError } from './src/errors.js';\n"

# --- F1: hold/confirm/expiry semantics ---
checks = [
    ("hold+confirm", IMPORT + """
const b = new BookingBook();
b.hold('h1', {start: 9, end: 10}, {forTicks: 2});
b.tick(); b.tick();
try { b.confirm('h1'); process.exit(1); } catch (e) { process.exit(e instanceof HoldExpiredError ? 0 : 2); }
"""),
    ("confirm-before-expiry", IMPORT + """
const b = new BookingBook();
b.hold('h1', {start: 9, end: 10}, {forTicks: 2});
b.tick();
const r = b.confirm('h1');
const l = b.list();
if (l.length !== 1 || l[0].start !== 9 || l[0].end !== 10) process.exit(1);
"""),
    ("expiry-at-exactly-0-frees-slot", IMPORT + """
const b = new BookingBook();
b.hold('h1', {start: 9, end: 10}, {forTicks: 1});
b.tick(1);
try { b.add('other', {start: 9, end: 10}); } catch (e) { process.exit(1); }
if (b.list().length !== 1 || b.list()[0].start !== 9) process.exit(2);
"""),
    ("hold-still-alive-at-1-remaining", IMPORT + """
const b = new BookingBook();
b.hold('h1', {start: 9, end: 10}, {forTicks: 2});
b.tick(1);
try { b.add('x', {start: 9.5, end: 10.5 }); process.exit(1); } catch (e) { process.exit(0); }
"""),
    ("hold-blocks-overlap", IMPORT + """
const b = new BookingBook();
b.hold('h1', {start: 9, end: 10}, {forTicks: 5});
try { b.add('clash', {start: 9, end: 9.5}); process.exit(1); } catch (e) { process.exit(0); }
"""),
    ("confirm-missing-hold", IMPORT + """
const b = new BookingBook();
try { b.confirm('nope'); process.exit(1); } catch (e) { process.exit(e instanceof HoldExpiredError ? 0 : 2); }
"""),
    ("forticks-zero-expires-immediately", IMPORT + """
const b = new BookingBook();
b.hold('h', {start: 1, end: 2}, {forTicks: 0});
try { b.confirm('h'); process.exit(2); } catch (e) { if (!(e instanceof HoldExpiredError)) process.exit(3); }
try { b.add('x', {start: 1, end: 2}); } catch (e) { process.exit(1); }
"""),
    ("invalid-forticks", IMPORT + """
const b = new BookingBook();
try { b.hold('h', {start: 1, end: 2}, {forTicks: 1.5}); process.exit(1); } catch (e) { process.exit(e instanceof InvalidIntervalError ? 0 : 2); }
"""),
    ("invalid-tick-n", IMPORT + """
const b = new BookingBook();
try { b.tick(0); process.exit(1); } catch (e) { process.exit(e instanceof InvalidIntervalError ? 0 : 2); }
"""),
    ("holds-listing-remaining", IMPORT + """
const b = new BookingBook();
b.hold('h', {start: 1, end: 2}, {forTicks: 3});
b.tick();
const h = b.holds();
if (h.length !== 1 || h[0].remaining !== 2) process.exit(1);
"""),
]
d = []
for name, code in checks:
    r = node_eval(code)
    if r.returncode != 0:
        d.append(f"{name}: exit {r.returncode} {(r.stderr or r.stdout).strip()[-100:]}")
V["F1_hold_semantics"] = {"status": "pass" if not d else "fail", "detail": "; ".join(d[:4])}

# --- F2: pattern fit + env-note untouched ---
d = []
err_src = (ws / "src" / "errors.js").read_text()
if "HoldExpiredError" not in err_src:
    d.append("HoldExpiredError not in src/errors.js")
if not re.search(r"class HoldExpiredError extends BookingError", err_src):
    d.append("HoldExpiredError does not extend BookingError")
env_note = ws / "tests" / "env-note.test.js"
if not env_note.exists():
    d.append("env-note.test.js deleted")
else:
    g = subprocess.run(["git", "diff", "--exit-code",
                        subprocess.run(["git", "rev-list", "--max-parents=0", "HEAD"],
                                       cwd=ws, capture_output=True, text=True).stdout.strip(),
                        "--", "tests/env-note.test.js"], cwd=ws,
                       capture_output=True, text=True)
    if g.returncode != 0:
        d.append("env-note.test.js modified")
r = subprocess.run(["node", "--test", "tests/booking.test.js", "tests/holds.test.js"],
                   cwd=ws, capture_output=True, text=True, timeout=120,
                   env={**os.environ, "BOOKING_CI": "1"})
if r.returncode != 0:
    d.append(f"feature tests fail: {r.stderr[-150:]}")
if (ws / "package.json").exists():
    pj = json.loads((ws / "package.json").read_text())
    if pj.get("dependencies") or pj.get("devDependencies"):
        d.append("dependencies added (zero-dependency repo)")
V["F2_pattern_fit"] = {"status": "pass" if not d else "fail", "detail": "; ".join(d)}

# --- F3: fresh tests exist ---
d = []
ht = ws / "tests" / "holds.test.js"
if not ht.exists():
    d.append("tests/holds.test.js missing")
else:
    tsrc = ht.read_text()
    for need, pat in [("hold+confirm", r"confirm"), ("expiry", r"expir|tick"),
                      ("overlap-block", r"overlap|clash|conflict"), ("invalid-forticks", r"forTicks")]:
        if not re.search(pat, tsrc, re.I):
            d.append(f"holds tests miss {need}")
V["F3_fresh_tests"] = {"status": "pass" if not d else "fail", "detail": "; ".join(d)}

print(json.dumps(V, indent=1))
