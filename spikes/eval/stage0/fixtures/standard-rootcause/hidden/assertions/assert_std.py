"""Hidden assertions for the standard-rootcause fixture (grader-only).

Remediation round 2 (council findings #7/#8):
- NON-MUTATING: grading runs in a throwaway copy of the workspace; the
  preserved workspace is never touched.
- Collision-proof hidden test names (test_h1_hidden_export,
  test_h2_hidden_edges): the original names overwrote and then deleted an
  agent-authored tests/test_export.py during S1 grading.

H1 — sibling caller: hidden export test passes against the work.
H2 — issue-stated root-cause contract only: overnight (22:00->06:00 = 8h)
      and 24:00-ending (20:00->24:00 = 4h) windows parse. Underdetermined
      edges (equal start/end, 00:00->24:00) are deliberately not asserted
      (Stage 0 finding #2).
H3 — regression protection: at least one new-or-modified .py test file
      under tests/ PASSES on the completed work AND FAILS when lib/ is
      reverted to the pristine buggy version. (Finding #8: the old rule
      accepted any nonzero exit, which an always-failing or missing test
      could satisfy spuriously.)
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HIDDEN_TESTS = {"H1": "test_h1_hidden_export.py", "H2": "test_h2_hidden_edges.py"}


def _run(mod: str, cwd: Path, timeout=120):
    return subprocess.run(
        [sys.executable, "-m", "unittest", mod],
        capture_output=True, text=True, timeout=timeout, cwd=cwd,
    )


def check_h1_h2(ws: Path, hidden_dir: Path) -> dict:
    results = {}
    for fname in HIDDEN_TESTS.values():
        shutil.copy(hidden_dir / "tests" / fname, ws / "tests" / fname)
    try:
        for key, fname in HIDDEN_TESTS.items():
            proc = _run(f"tests.{fname[:-3]}", ws)
            tail = (proc.stdout + proc.stderr)[-400:]
            results[key] = ("pass" if proc.returncode == 0 else "fail", tail)
    finally:
        for fname in HIDDEN_TESTS.values():
            (ws / "tests" / fname).unlink(missing_ok=True)
    return results


def check_h3(ws: Path, changed_files: list) -> dict:
    changed_tests = [
        f["path"] for f in changed_files
        if f["path"].startswith("tests/") and f.get("status") in ("A", "M")
        and f["path"].endswith(".py") and "__pycache__" not in f["path"]
        and f["path"] != "tests/__init__.py"
    ]
    if not changed_tests:
        return {"H3": ("fail", "no new or modified test files")}

    # Phase 1: each changed test must pass on the completed work.
    passes_now = {}
    for path in changed_tests:
        mod = path.replace("/", ".").removesuffix(".py")
        proc = _run(mod, ws)
        passes_now[path] = proc.returncode == 0
    if not any(passes_now.values()):
        return {"H3": ("fail", "changed tests do not pass on the completed work: "
                        + "; ".join(f"{p}:{'ok' if v else 'FAIL'}" for p, v in passes_now.items()))}

    # Phase 2: revert lib/ to the pristine buggy version; a qualifying test
    # must now fail.
    pristine = subprocess.run(
        ["git", "rev-list", "--max-parents=0", "HEAD"],
        capture_output=True, text=True, cwd=ws,
    ).stdout.strip()
    subprocess.run(["git", "checkout", pristine, "--", "lib/"], check=True, cwd=ws)
    details = []
    certified = False
    for path, ok_before in passes_now.items():
        if not ok_before:
            details.append(f"{path}:skipped(fails on work)")
            continue
        mod = path.replace("/", ".").removesuffix(".py")
        proc = _run(mod, ws)
        fails_after = proc.returncode != 0
        certified = certified or fails_after
        details.append(f"{path}:{'FailsOnRevert' if fails_after else 'PassesOnRevert'}")
    status = "pass" if certified else "fail"
    return {"H3": (status, "; ".join(details))}


def run_assertions(hidden_dir: Path, workspace: Path, changed_files: list) -> dict:
    tmp = Path(tempfile.mkdtemp(prefix="s0grade-"))
    try:
        ws = tmp / "ws"
        shutil.copytree(workspace, ws, ignore=shutil.ignore_patterns("__pycache__", ".h3_lib_backup"))
        subprocess.run(["git", "add", "-A"], cwd=ws, check=True, capture_output=True)
        verdict = {}
        for key, (status, detail) in check_h1_h2(ws, hidden_dir).items():
            verdict[key] = {"status": status, "detail": detail}
        verdict.update(
            {k: {"status": v[0], "detail": v[1]} for k, v in check_h3(ws, changed_files).items()}
        )
        return verdict
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    hidden = Path(sys.argv[1]).resolve()
    workspace = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else Path.cwd()
    changed = json.loads(sys.stdin.read() or "[]")
    print(json.dumps(run_assertions(hidden, workspace, changed), indent=2))
