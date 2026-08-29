#!/usr/bin/env python3
"""Stage 0 runner — validate / step0 / run / report.

Zero dependencies beyond the Python stdlib and git. Writes only to the
evaluation workspace (FOUNDATION.md §8.4); never mutates the repository.

Commands:
  validate  mechanically prove assertion discrimination on known-good and
            known-faulty patches (no model spend)
  step0     mechanism probes for the three system invocations (tiny model
            calls, recorded, not fixture cells)
  run       execute the six calibration cells in fixed order
  report    summarize results into the workspace
"""
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

STAGE0 = Path(__file__).resolve().parents[1]
REPO_ROOT = STAGE0.parents[1]
FIXTURES = STAGE0 / "fixtures"
SYSTEMS = STAGE0 / "systems"
WS = Path(os.environ.get("STAGE0_WORKSPACE", REPO_ROOT.parent / "pi-adaptive-dev-rig-evalruns" / "stage0"))
CELL_TIMEOUT_S = 20 * 60

CELLS = [
    ("P1", "prototype-feasibility", "unaided"),
    ("P2", "prototype-feasibility", "superpowers-rival"),
    ("P3", "prototype-feasibility", "adaptive"),
    ("S1", "standard-rootcause", "unaided"),
    ("S2", "standard-rootcause", "superpowers-rival"),
    ("S3", "standard-rootcause", "adaptive"),
]

GIT_ENV = {**os.environ, "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_SYSTEM": "/dev/null"}


def sh(args, cwd=None, timeout=None, env=None, input_text=None):
    return subprocess.run(
        args, cwd=cwd, capture_output=True, text=True,
        timeout=timeout, env=env or GIT_ENV, input=input_text,
    )


def prep_workspace(fixture: str, tag: str) -> Path:
    ws = WS / "work" / tag
    if ws.exists():
        shutil.rmtree(ws)
    ws.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(FIXTURES / fixture / "repo", ws)
    sh(["git", "init", "-q"], cwd=ws)
    sh(["git", "add", "-A"], cwd=ws)
    sh(["git", "-c", "user.name=stage0", "-c", "user.email=stage0@localhost",
        "commit", "-q", "-m", "pristine fixture"], cwd=ws)
    return ws


def initial_commit(ws: Path) -> str:
    return sh(["git", "rev-list", "--max-parents=0", "HEAD"], cwd=ws).stdout.strip()


def changed_files(ws: Path) -> list:
    """Pre-injection snapshot: [{path, status}] vs the pristine commit."""
    sh(["git", "add", "-A"], cwd=ws)
    out = sh(["git", "diff", "--name-status", initial_commit(ws)], cwd=ws).stdout
    files = []
    for line in out.splitlines():
        parts = line.split("\t")
        if len(parts) == 2:
            files.append({"status": parts[0][:1], "path": parts[1]})
    return files


def run_assertions(fixture: str, ws: Path, changed: list) -> dict:
    hidden = FIXTURES / fixture / "hidden"
    script = next((hidden / "assertions").glob("assert_*.py"))
    proc = sh([sys.executable, str(script), str(hidden)], cwd=ws,
              timeout=300, input_text=json.dumps(changed))
    if proc.returncode != 0:
        return {"RUNNER_ERROR": {"status": "fail",
                                 "detail": (proc.stderr or proc.stdout)[-800:]}}
    return json.loads(proc.stdout)


def verdict_matches(verdict: dict, expected: dict) -> bool:
    return all(verdict.get(k, {}).get("status") == v for k, v in expected.items())


def cmd_validate():
    print(f"workspace: {WS}")
    ok = True
    for fixture in ("standard-rootcause", "prototype-feasibility"):
        hidden = FIXTURES / fixture / "hidden"
        expectations = json.loads((hidden / "expectations.json").read_text())
        patches = hidden / "patches"

        if fixture == "standard-rootcause":
            ws = prep_workspace(fixture, "validate-baseline")
            proc = sh([sys.executable, "-m", "unittest", "discover", "-s", "tests"],
                      cwd=ws, timeout=120)
            broken = proc.returncode != 0
            print(f"[baseline] {fixture}: visible suite "
                  f"{'FAILS as designed' if broken else 'PASSES — FIXTURE DEFECT'}")
            ok = ok and broken

        for patch_name, expected in expectations.items():
            ws = prep_workspace(fixture, f"validate-{patch_name}")
            proc = sh(["git", "apply", str(patches / patch_name)], cwd=ws)
            if proc.returncode != 0:
                print(f"[patch ] {fixture}/{patch_name}: APPLY FAILED\n{proc.stderr}")
                ok = False
                continue
            changed = changed_files(ws)
            verdict = run_assertions(fixture, ws, changed)
            match = verdict_matches(verdict, expected)
            ok = ok and match
            summary = ", ".join(f"{k}={v['status']}" for k, v in verdict.items())
            print(f"[assert] {fixture}/{patch_name}: {summary} -> "
                  f"{'OK' if match else 'MISMATCH vs ' + json.dumps(expected)}")
            if not match:
                for k, v in verdict.items():
                    if v.get("detail"):
                        print(f"         {k}: {v['detail'][:300]}")
    print("VALIDATE:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def _pi_probe(name, extra_flags, workdir):
    """Tiny mechanism probe ('Reply with the single word OK.') — not a fixture cell."""
    session_dir = WS / "sessions" / f"step0-{name}"
    session_dir.mkdir(parents=True, exist_ok=True)
    cmd = ["pi", "-p",
           "--provider", "9-router", "--model", "9-router/glm-5.3", "--thinking", "high",
           "--tools", "read,bash,edit,write",
           "--no-skills", "--no-extensions", "--no-context-files", "--no-prompt-templates",
           *extra_flags,
           "--session-dir", str(session_dir), "--mode", "json", "--name", f"step0-{name}",
           "--", "Reply with the single word OK."]
    started = time.time()
    try:
        proc = sh(cmd, cwd=workdir, timeout=240, env={**os.environ})
        record = {"cmd": cmd, "exit_code": proc.returncode, "wall_s": round(time.time() - started, 1),
                  "stdout_head": proc.stdout[:400], "stderr_tail": proc.stderr[-400:]}
        try:
            events = [json.loads(l) for l in proc.stdout.splitlines() if l.strip()]
            record["json_mode"] = bool(events)
            record["usage_keys"] = sorted({k for e in events if isinstance(e, dict)
                                           for k in e if "usage" in k.lower() or "token" in k.lower()})
        except json.JSONDecodeError:
            record["json_mode"] = False
            record["usage_keys"] = []
    except subprocess.TimeoutExpired:
        record = {"cmd": cmd, "exit_code": None, "timeout": True}
    return record


def cmd_step0():
    WS.mkdir(parents=True, exist_ok=True)
    probe_dir = WS / "step0"
    if probe_dir.exists():
        shutil.rmtree(probe_dir)
    probe_dir.mkdir(parents=True)
    stage0_abs = str(STAGE0.resolve())
    guidance = [str((STAGE0 / "guidance" / f).resolve())
                for f in ("explore-design.md", "debug.md", "test-verify.md", "review.md")]
    header = str((STAGE0 / "header" / "posture-header.md").resolve())
    results = {
        "A-base": _pi_probe("A-base", [], probe_dir),
        "B-skill-with-ns": _pi_probe("B-skill-with-ns", ["--skill", guidance[0]], probe_dir),
        "C-adaptive": _pi_probe("C-adaptive",
                                ["--skill", guidance[0], "--skill", guidance[1],
                                 "--skill", guidance[2], "--skill", guidance[3],
                                 "--append-system-prompt", header], probe_dir),
    }
    clone_skills = WS / "superpowers" / "skills"
    if clone_skills.is_dir():
        skill_flags = []
        for entry in sorted(clone_skills.iterdir()):
            if (entry / "SKILL.md").is_file():
                skill_flags += ["--skill", str(entry)]
        results["D-rival"] = _pi_probe("D-rival", skill_flags, probe_dir)
        results["D-rival"]["skill_count"] = len(skill_flags) // 2
        ext = WS / "superpowers" / "extensions" / "plan-tracker.ts"
        if ext.is_file():
            results["E-rival-extension"] = _pi_probe("E-rival-extension",
                                                     skill_flags + ["-e", str(ext)], probe_dir)
    else:
        results["D-rival"] = {"status": "skipped", "reason": "pinned clone not present"}
    out = WS / "step0.json"
    out.write_text(json.dumps(results, indent=2))
    for name, rec in results.items():
        print(f"[{name}] exit={rec.get('exit_code')} json={rec.get('json_mode')} "
              f"usage_keys={rec.get('usage_keys')} timeout={rec.get('timeout', False)}")
    print(f"wrote {out}")
    return 0


def extract_usage(stdout: str):
    """Sum usage across assistant messages in the JSONL event stream."""
    usage = None
    for line in stdout.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        msg = event.get("message") or {}
        if event.get("type") == "message" and msg.get("role") == "assistant" and msg.get("usage"):
            u = msg["usage"]
            if usage is None:
                usage = {"input": 0, "output": 0, "totalTokens": 0,
                         "cost_total": 0.0, "assistant_messages": 0}
            usage["input"] += u.get("input", 0)
            usage["output"] += u.get("output", 0)
            usage["totalTokens"] += u.get("totalTokens", 0)
            usage["cost_total"] += (u.get("cost") or {}).get("total", 0.0)
            usage["assistant_messages"] += 1
    return usage


def build_prompt(cell_id: str, fixture: str, system: str) -> str:
    task = (FIXTURES / fixture / "task.md").read_text()
    if system == "superpowers-rival":
        instruction = (SYSTEMS / "right-sizing-instruction.md").read_text()
        return f"{task}\n\n{instruction}"
    return task


def cmd_run(only=None):
    WS.mkdir(parents=True, exist_ok=True)
    (WS / "results").mkdir(exist_ok=True)
    (WS / "prompts").mkdir(exist_ok=True)
    for cell_id, fixture, system in CELLS:
        if only and cell_id not in only:
            continue
        result_path = WS / "results" / f"{cell_id}.json"
        if result_path.exists():
            print(f"[{cell_id}] already recorded — skipping (cap discipline)")
            continue
        ws = prep_workspace(fixture, cell_id)
        prompt_file = WS / "prompts" / f"{cell_id}.md"
        prompt_file.write_text(build_prompt(cell_id, fixture, system))
        script = SYSTEMS / f"{system}.sh"
        session_dir = WS / "sessions" / cell_id
        session_dir.mkdir(parents=True, exist_ok=True)
        env = {**os.environ, "STAGE0_CELL": f"stage0-{cell_id}",
               "STAGE0_SESSION_DIR": str(session_dir),
               "STAGE0_SUPERPOWERS": str(WS / "superpowers"),
               "STAGE0_WS": str(ws), "STAGE0_PROMPT": str(prompt_file)}
        started = time.time()
        proc, timed_out, stderr_tail = None, False, ""
        try:
            proc = sh(["bash", str(script), str(ws), str(prompt_file)],
                      cwd=ws, timeout=CELL_TIMEOUT_S, env=env)
        except subprocess.TimeoutExpired as exc:
            timed_out = True
            stderr_tail = (exc.stderr or b"").decode()[-800:] if exc.stderr else ""
        wall_s = round(time.time() - started, 1)

        changed = changed_files(ws) if not timed_out else []
        verdict = run_assertions(fixture, ws, changed) if not timed_out else \
            {"RUNNER_ERROR": {"status": "fail", "detail": "cell timeout"}}

        usage = extract_usage(proc.stdout) if proc is not None else None
        stdout_json = None
        diff_stat = sh(["git", "diff", "--stat", initial_commit(ws)], cwd=ws).stdout
        defect = None
        if timed_out:
            defect = "timeout"
        elif proc is None or proc.returncode != 0:
            defect = "nonzero-exit"
        elif "RUNNER_ERROR" in verdict:
            defect = "assertion-harness"

        result = {
            "cell": cell_id, "fixture": fixture, "system": system,
            "started": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(started)),
            "wall_s": wall_s, "timeout": timed_out,
            "exit_code": None if proc is None else proc.returncode,
            "defect_class": defect,
            "usage": usage, "stdout_bytes": 0 if proc is None else len(proc.stdout),
            "stderr_tail": stderr_tail or ("" if proc is None else proc.stderr[-800:]),
            "changed_files": changed, "diff_stat_tail": diff_stat[-600:],
            "assertions": verdict,
        }
        result_path.write_text(json.dumps(result, indent=2))
        summary = ", ".join(f"{k}={v['status']}" for k, v in verdict.items())
        print(f"[{cell_id}] {fixture}/{system} wall={wall_s}s defect={defect} "
              f"assertions: {summary}")
    return 0


def cmd_report():
    rows = []
    defects = []
    for cell_id, fixture, system in CELLS:
        path = WS / "results" / f"{cell_id}.json"
        if not path.exists():
            rows.append(f"| {cell_id} | {system} | {fixture} | MISSING | | | |")
            continue
        r = json.loads(path.read_text())
        summary = "<br>".join(f"{k}: {v['status']}" for k, v in r["assertions"].items())
        rows.append(f"| {cell_id} | {system} | {fixture} | {summary} | "
                    f"{r['wall_s']}s | {r['usage'] or 'n/a'} | {r['defect_class'] or '-'} |")
        if r["defect_class"]:
            defects.append(r)
    lines = ["# Stage 0 results (infrastructure validation only — non-evidentiary, D-014)", "",
             "| cell | system | fixture | assertions | wall | usage | defect |",
             "|---|---|---|---|---|---|---|", *rows, ""]
    if defects:
        lines += ["## Defect-classified cells (D11)"]
        lines += [f"- {d['cell']}: {d['defect_class']} — {d['stderr_tail'][:200]}" for d in defects]
    (WS / "summary.md").write_text("\n".join(lines))
    print(f"wrote {WS / 'summary.md'}")
    return 0


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("validate", "step0", "run", "report"):
        print(__doc__)
        return 2
    cmd = sys.argv[1]
    if cmd == "run":
        return cmd_run(sys.argv[2:] or None)
    return {"validate": cmd_validate, "step0": cmd_step0, "report": cmd_report}[cmd]()


if __name__ == "__main__":
    sys.exit(main())
