"""Hidden assertions for the standard-rootcause fixture (grader-only).

Preconditions: workspace is a git repo, initial commit = pristine fixture,
`changed_files` is the pre-injection diff snapshot (list of
{path, status} with status A/M/D), and hidden tests have NOT yet been
copied into the workspace.

H1 — sibling caller: hidden tests/test_export.py passes against the work.
H2 — root-cause contract: hidden tests/test_windows_edges.py passes.
H3 — regression protection: at least one new-or-modified file under tests/
      fails when lib/ is reverted to the pristine (buggy) version. Only
      new/modified test files are considered, so the pre-existing failing
      symptom test cannot mask the check.
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path


def _run_module(mod: str, timeout=120):
    return subprocess.run(
        [sys.executable, "-m", "unittest", mod],
        capture_output=True, text=True, timeout=timeout,
    )


def _with_hidden_tests(hidden_dir: Path, fn):
    copied = []
    for test in (hidden_dir / "tests").glob("test_*.py"):
        dest = Path("tests") / test.name
        shutil.copy(test, dest)
        copied.append(dest)
    try:
        return fn()
    finally:
        for dest in copied:
            dest.unlink(missing_ok=True)


def check_h1_h2(hidden_dir: Path) -> dict:
    """H1/H2 via per-module exit codes — no output parsing."""
    def inner():
        results = {}
        for key, mod in (("H1", "tests.test_export"), ("H2", "tests.test_windows_edges")):
            proc = _run_module(mod)
            tail = (proc.stdout + proc.stderr)[-400:]
            results[key] = ("pass" if proc.returncode == 0 else "fail", tail)
        return results
    return _with_hidden_tests(hidden_dir, inner)


def check_h3(changed_files: list) -> dict:
    changed_tests = [
        f["path"] for f in changed_files
        if f["path"].startswith("tests/") and f.get("status") in ("A", "M")
        and f["path"] != "tests/__init__.py"
    ]
    if not changed_tests:
        return {"H3": ("fail", "no new or modified test files")}
    pristine = subprocess.run(
        ["git", "rev-list", "--max-parents=0", "HEAD"], capture_output=True, text=True
    ).stdout.strip()
    # Snapshot the agent's lib/ so restore never depends on git state
    # (the agent may have committed or left work uncommitted).
    lib_backup = Path(".h3_lib_backup")
    if lib_backup.exists():
        shutil.rmtree(lib_backup)
    shutil.copytree("lib", lib_backup)
    subprocess.run(["git", "checkout", pristine, "--", "lib/"], check=True)
    try:
        any_fail = False
        details = []
        for path in changed_tests:
            mod = path.replace("/", ".").removesuffix(".py")
            proc = subprocess.run(
                [sys.executable, "-m", "unittest", mod, "-v"],
                capture_output=True, text=True, timeout=120,
            )
            failed = proc.returncode != 0
            any_fail = any_fail or failed
            details.append(f"{path}:{'FAIL' if failed else 'ok'}")
        status = "pass" if any_fail else "fail"
        return {"H3": (status, "; ".join(details))}
    finally:
        shutil.rmtree("lib")
        lib_backup.rename("lib")
        subprocess.run(["git", "add", "-A"], check=True)


def run_assertions(hidden_dir: Path, changed_files: list) -> dict:
    results = check_h1_h2(hidden_dir)
    verdict = {k: {"status": v[0], "detail": v[1]} for k, v in results.items()}
    h3 = check_h3(changed_files)
    verdict.update({k: {"status": v[0], "detail": v[1]} for k, v in h3.items()})
    return verdict


if __name__ == "__main__":
    hidden = Path(sys.argv[1]).resolve()
    changed = json.loads(sys.stdin.read() or "[]")
    print(json.dumps(run_assertions(hidden, changed), indent=2))
