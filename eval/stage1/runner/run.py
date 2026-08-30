#!/usr/bin/env python3
"""Stage 1 runner — validate / schedule / probes / run / report.

Zero dependencies beyond stdlib + git + node. Writes only to the
evaluation workspace (FOUNDATION.md §8.4); never mutates the repository
or frozen Stage 0 assets. Grading runs on disposable workspace copies.

Commands:
  validate             two-sided mechanical validation of ALL fixture
                       assertions (incl. sealed reserves) — no model spend
  schedule             generate the seeded, interleaved, anonymous
                       execution schedule into the workspace and freeze
                       its sha256 (refuses to overwrite unless --force)
  probes               flag-level symmetry probes (no model spend);
                       model-touching probes run post-approval only
  run [--cell ID... | --round N | --all | --ux | --followup]
                       execute scheduled cells (balanced resume: recorded
                       cells are skipped; --retry for diagnostic reruns)
  report               per-scenario + pooled summary into the workspace
"""
import hashlib
import json
import os
import random
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

STAGE1 = Path(__file__).resolve().parents[1]
STAGE0 = STAGE1.parent / "stage0"
REPO_ROOT = STAGE1.parents[1]
FIXTURES = STAGE1 / "fixtures"
SYSTEMS = STAGE1 / "systems"
UX = STAGE1 / "ux"
WS = Path(os.environ.get("STAGE1_WORKSPACE",
                         REPO_ROOT.parent / "pi-adaptive-dev-rig-evalruns" / "stage1"))

SEED = 20260830
CORE_TIMEOUT_S = 25 * 60
UX_TIMEOUT_S = 15 * 60
DIAG_RERUN_CAP = 6
CEILING_COST_USD = 200.0     # council r1 #5/#7: enforced, not documentary
CEILING_INVOCATIONS = 102
CEILING_WALL_S = 10 * 3600
FOLLOWUP_CEILING_USD = 40.0

SCORED = ["p1-vendor-client", "p2-spike-triage", "p3-report-cards",
          "s1-review-debt", "s2-promote-prototype", "s3-booking-feature"]
RESERVE = ["r1-parity-kv", "r2-slug-fix"]  # sealed — never scheduled
ARMS = ["unaided", "superpowers", "superpowers-instruction", "adaptive"]
REPEATS = 3
UX_GRID = [("ux1", "blocking"), ("ux1", "optimistic"),
           ("ux2", "blocking"), ("ux2", "optimistic")]

GIT_ENV = {**os.environ, "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_SYSTEM": "/dev/null"}


def sh(args, cwd=None, timeout=None, env=None, input_text=None):
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True,
                          timeout=timeout, env=env or GIT_ENV, input=input_text)


# ----------------------------------------------------------------- shared

def prep_workspace(fixture: str, tag: str) -> Path:
    ws = WS / "work" / tag
    if ws.exists():
        shutil.rmtree(ws)
    ws.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(FIXTURES / fixture / "repo", ws)
    sh(["git", "init", "-q"], cwd=ws)
    sh(["git", "add", "-A"], cwd=ws)
    sh(["git", "-c", "user.name=stage1", "-c", "user.email=stage1@localhost",
        "commit", "-q", "-m", "pristine fixture"], cwd=ws)
    return ws


def initial_commit(ws: Path) -> str:
    return sh(["git", "rev-list", "--max-parents=0", "HEAD"], cwd=ws).stdout.strip()


NOISE = (".pyc", "__pycache__")


def changed_files(ws: Path) -> list:
    sh(["git", "add", "-A"], cwd=ws)
    out = sh(["git", "diff", "--name-status", initial_commit(ws)], cwd=ws).stdout
    files = []
    for line in out.splitlines():
        parts = line.split("\t")
        if len(parts) == 2 and not any(n in parts[1] for n in NOISE):
            files.append({"status": parts[0][:1], "path": parts[1]})
    return files


def diff_text(ws: Path) -> str:
    return sh(["git", "diff", initial_commit(ws), "--", ":!*.pyc",
               ":!**/__pycache__/**"], cwd=ws).stdout


def run_assertions(fixture: str, ws: Path, changed: list) -> dict:
    """Grade on a DISPOSABLE COPY (stage0 remediation r2/r3 pattern)."""
    hidden = FIXTURES / fixture / "hidden"
    script = next((hidden / "assertions").glob("assert_*.py"))
    tmp = WS / "grade-tmp"
    if tmp.exists():
        shutil.rmtree(tmp)
    shutil.copytree(ws, tmp)  # keep .git: graders use git diff for snapshot checks
    try:
        proc = sh([sys.executable, str(script), str(hidden), str(tmp)],
                  cwd=tmp, timeout=600, input_text=json.dumps(changed))
        if proc.returncode != 0:
            return {"RUNNER_ERROR": {"status": "fail",
                                     "detail": (proc.stderr or proc.stdout)[-800:]}}
        return json.loads(proc.stdout)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def extract_usage(stdout: str):
    """Id-deduped usage extraction (stage0 remediation r2; council #6)."""
    per_msg = {}
    for line in stdout.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(event, dict):
            continue
        msg = event.get("message") or {}
        if msg.get("role") != "assistant" or not msg.get("usage"):
            continue
        mid = msg.get("id") or event.get("id")
        if mid:
            per_msg[mid] = msg["usage"]
        elif event.get("type") == "message_end":
            per_msg[f"end{len(per_msg)}"] = msg["usage"]
    if not per_msg:
        return None
    usage = {"input": 0, "output": 0, "totalTokens": 0, "cost_total": 0.0,
             "assistant_messages": len(per_msg)}
    for u in per_msg.values():
        usage["input"] += u.get("input", 0)
        usage["output"] += u.get("output", 0)
        usage["totalTokens"] += u.get("totalTokens", 0)
        usage["cost_total"] += (u.get("cost") or {}).get("total", 0.0)
    return usage


def session_usage_total(session_dir: Path) -> int:
    """Cross-check total tokens from the persisted session files.

    Id-deduped exactly like extract_usage (council r1 #7: the gate must
    not re-introduce the Stage 0 double-count bug)."""
    per_msg = {}
    for f in session_dir.rglob("*.jsonl"):
        for line in f.read_text().splitlines():
            try:
                e = json.loads(line)
            except json.JSONDecodeError:
                continue
            m = e.get("message") or {}
            if m.get("role") != "assistant" or not m.get("usage"):
                continue
            mid = m.get("id") or e.get("id")
            if mid:
                per_msg[mid] = m["usage"]
            elif e.get("type") == "message_end":
                per_msg[f"end{len(per_msg)}"] = m["usage"]
    return sum(u.get("totalTokens", 0) for u in per_msg.values())


# ----------------------------------------------------------------- validate

def verdict_matches(verdict: dict, expected: dict) -> bool:
    return all(verdict.get(k, {}).get("status") == v for k, v in expected.items())


def cmd_validate():
    WS.mkdir(parents=True, exist_ok=True)
    evidence = {}
    ok = True
    for fixture in SCORED + RESERVE:
        hidden = FIXTURES / fixture / "hidden"
        expectations = json.loads((hidden / "expectations.json").read_text())
        evidence[fixture] = {}
        for patch_name, expected in expectations.items():
            ws = prep_workspace(fixture, f"validate-{fixture[:2]}-{patch_name}")
            proc = sh(["git", "apply", str(hidden / "patches" / f"{patch_name}.patch")], cwd=ws)
            if proc.returncode != 0:
                print(f"[patch ] {fixture}/{patch_name}: APPLY FAILED\n{proc.stderr}")
                ok = False
                continue
            changed = changed_files(ws)
            verdict = run_assertions(fixture, ws, changed)
            match = verdict_matches(verdict, expected)
            ok = ok and match
            evidence[fixture][patch_name] = {"expected": expected, "got": verdict,
                                             "match": match}
            summary = ", ".join(f"{k}={v['status']}" for k, v in verdict.items())
            print(f"[assert] {fixture}/{patch_name}: {summary} -> "
                  f"{'OK' if match else 'MISMATCH vs ' + json.dumps(expected)}")
            if not match:
                for k, v in verdict.items():
                    if v.get("detail"):
                        print(f"         {k}: {str(v['detail'])[:300]}")
    (WS / "validation-evidence.json").write_text(json.dumps(evidence, indent=1))
    print("VALIDATE:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


# ----------------------------------------------------------------- schedule

def build_prompts() -> dict:
    """Immutable prompt bodies per (fixture, arm) and UX (prompt, mode)."""
    bodies = {}
    for f in SCORED:
        task = (FIXTURES / f / "task.md").read_text()
        for arm in ARMS:
            body = task
            if arm == "superpowers-instruction":
                body += "\n\n" + (STAGE0 / "systems" / "right-sizing-instruction.md").read_text()
            bodies[(f, arm)] = body
    for name in ("ux1", "ux2"):
        task = (UX / f"{name}.md").read_text()
        for mode in ("blocking", "optimistic"):
            suffix = (UX / "blocking-line.md").read_text() if mode == "blocking" \
                else (UX / "optimistic-line.md").read_text()
            bodies[(name, mode)] = task + "\n\n" + suffix
    return bodies


def canonical_schedule_hash(doc_without_sha):
    blob = json.dumps(doc_without_sha, indent=1, sort_keys=False)
    return hashlib.sha256(blob.encode()).hexdigest()


def cmd_schedule(force=False):
    sched_path = WS / "schedule.json"
    if force and any((WS / "results").glob("*.json")) if (WS / "results").exists() else False:
        print("refusing --force: recorded results exist (immutability guard)")
        return 1
    if sched_path.exists() and not force:
        print(f"schedule exists ({sched_path}); refusing to overwrite without --force")
        return 1
    WS.mkdir(parents=True, exist_ok=True)
    rng = random.Random(SEED)
    cells = []
    for rep in range(1, REPEATS + 1):          # balanced interleaved rounds
        round_cells = [{"kind": "core", "fixture": f, "system": arm,
                        "repeat": rep, "round": rep}
                       for f in SCORED for arm in ARMS]
        rng.shuffle(round_cells)               # execution order
        cells.extend(round_cells)
    ux_cells = [{"kind": "ux", "fixture": f"ux-{name}", "system": "adaptive",
                 "mode": mode, "repeat": i + 1, "round": 3 + i + 1}
                for i in range(REPEATS) for name, mode in UX_GRID]
    rng.shuffle(ux_cells)
    cells.extend(ux_cells)
    # Opaque IDs: assign the ID pool by an INDEPENDENT shuffle so no cell's
    # ID encodes fixture/arm/repeat/position (council: ID de-anonymization).
    id_pool = [f"c{i:03d}" for i in range(1, len(cells) + 1)]
    rng.shuffle(id_pool)
    for cell, anon in zip(cells, id_pool):
        cell["anon"] = anon

    bodies = build_prompts()
    prompts = WS / "prompts"
    prompts.mkdir(parents=True, exist_ok=True)
    for c in cells:
        key = (c["fixture"] if c["kind"] == "core" else c["fixture"][3:],
               c["system"] if c["kind"] == "core" else c["mode"])
        body = bodies[key]
        c["prompt_sha"] = hashlib.sha256(body.encode()).hexdigest()
        pf = prompts / f"{c['anon']}.md"
        pf.write_text(body)

    anon_map = {c["anon"]: {k: v for k, v in c.items() if k != "anon"} for c in cells}
    digest = canonical_schedule_hash({"seed": SEED, "cell_count": len(cells),
                                      "cells": cells})
    doc = {"seed": SEED, "cell_count": len(cells), "sha256": digest, "cells": cells}
    sched_path.write_text(json.dumps(doc, indent=1))
    # identity table stays workspace-side (graders see only anon IDs)
    (WS / "cellmap.json").write_text(json.dumps(anon_map, indent=1))
    print(f"schedule: {len(cells)} cells ({len(cells) - len(ux_cells)} core + "
          f"{len(ux_cells)} ux), seed={SEED}, sha256={digest[:16]}…")
    print(f"wrote {sched_path}")
    return 0


def load_schedule() -> dict:
    return json.loads((WS / "schedule.json").read_text())


# ----------------------------------------------------------------- probes

def arm_command(arm: str, ws: Path, prompt_file: Path, session_dir: Path, name: str):
    base = ["pi", "-p", "--provider", "9-router", "--model", "9-router/glm-5.3",
            "--thinking", "high", "--tools", "read,bash,edit,write",
            "--no-skills", "--no-extensions", "--no-context-files",
            "--no-prompt-templates"]
    if arm == "unaided":
        return base + ["--session-dir", str(session_dir), "--mode", "json",
                       "--name", name, "--", prompt_file.read_text()]
    if arm == "adaptive":
        return base + ["--skill", str(STAGE0 / "guidance" / "explore-design.md"),
                       "--skill", str(STAGE0 / "guidance" / "debug.md"),
                       "--skill", str(STAGE0 / "guidance" / "test-verify.md"),
                       "--skill", str(STAGE0 / "guidance" / "review.md"),
                       "--append-system-prompt", str(STAGE0 / "header" / "posture-header.md"),
                       "--session-dir", str(session_dir), "--mode", "json",
                       "--name", name, "--", prompt_file.read_text()]
    skills = []
    for entry in sorted((WS / "superpowers" / "skills").iterdir()):
        if (entry / "SKILL.md").is_file():
            skills += ["--skill", str(entry)]
    ext = WS / "superpowers" / "extensions" / "plan-tracker.ts"
    return base + skills + ["-e", str(ext),
                            "--session-dir", str(session_dir), "--mode", "json",
                            "--name", name, "--", prompt_file.read_text()]


def cmd_probes():
    """Flag-level probes only (no model spend). Symmetry proof: the two
    superpowers arms differ ONLY in the appended instruction (prompt-side)."""
    WS.mkdir(parents=True, exist_ok=True)
    fake_ws, fake_prompt, fake_sd = Path("/tmp/probe-ws"), Path("/tmp/probe-p.md"), Path("/tmp/probe-sd")
    fake_prompt.write_text("x")
    results = {}
    cmds = {}
    for arm in ARMS:
        cmds[arm] = arm_command(arm, fake_ws, fake_prompt, fake_sd, "probe")
        results[arm] = {"argv_head": cmds[arm][:12], "flag_count": len(cmds[arm])}
    sym = cmds["superpowers"][: -1] == cmds["superpowers-instruction"][: -1]
    # the arms share ONE launcher; the instruction difference is prompt-body,
    # verified by hash instead:
    b1 = hashlib.sha256(build_prompts()[("p1-vendor-client", "superpowers")].encode()).hexdigest()
    b2 = hashlib.sha256(build_prompts()[("p1-vendor-client", "superpowers-instruction")].encode()).hexdigest()
    identical = cmds["superpowers"] == cmds["superpowers-instruction"]
    results["symmetry"] = {
        "identical_invocation": identical,
        "prompt_bodies_differ_only_by_instruction": b1 != b2,
        "instruction_text": (STAGE0 / "systems" / "right-sizing-instruction.md").read_text(),
        "verdict": "PASS" if identical and b1 != b2 else "FAIL",
    }
    # frozen-asset integrity inside the probes report
    proc = sh(["shasum", "-a", "256", "-c", str(STAGE0 / "freeze-manifest.txt")],
              cwd=REPO_ROOT)
    results["stage0_manifest"] = {"verified": proc.returncode == 0}
    clone = WS / "superpowers"
    results["superpowers_pin_present"] = bool((clone / "skills").is_dir())
    pin = "efe1d158691bf064c24f0460fd4e46ca58de0055"
    got = sh(["git", "rev-parse", "HEAD"], cwd=clone).stdout.strip()
    results["superpowers_commit"] = {"expected": pin, "got": got,
                                     "ok": got == pin}
    results["superpowers_pin_present"] = (results["superpowers_pin_present"]
                                          and got == pin)
    out = WS / "probes.json"
    out.write_text(json.dumps(results, indent=1))
    print(json.dumps({k: v for k, v in results.items()
                      if k in ("symmetry", "stage0_manifest", "superpowers_pin_present")}, indent=1))
    return 0 if all([identical, b1 != b2, proc.returncode == 0,
                     results["superpowers_pin_present"],
                     results["superpowers_commit"]["ok"]]) else 1


# ----------------------------------------------------------------- run

def declared_posture(stdout: str) -> str | None:
    """First posture declaration anywhere in the transcript (UX cells)."""
    texts, current = [], None
    for line in stdout.splitlines():
        try:
            e = json.loads(line)
        except json.JSONDecodeError:
            continue
        m = e.get("message") or {}
        if e.get("type") == "message_start" and m.get("role") == "assistant":
            current = {"parts": []}
            texts.append(current)
        if e.get("type") in ("message_update", "message_end") and current is not None:
            for blk in (m.get("content") or []):
                if isinstance(blk, dict) and blk.get("text"):
                    current["parts"].append(blk["text"])
    for t in texts:
        joined = "\n".join(t["parts"])
        mm = re.search(r"(?:delivery|posture)\s*[:=]\s*\**\s*(Prototype|Standard|Hardened)",
                       joined, re.I)
        if mm:
            return mm.group(1).title()
    return None


def final_assistant_text(stdout: str) -> str:
    texts, current = [], None
    for line in stdout.splitlines():
        try:
            e = json.loads(line)
        except json.JSONDecodeError:
            continue
        m = e.get("message") or {}
        if e.get("type") == "message_start" and m.get("role") == "assistant":
            current = {"id": m.get("id"), "parts": []}
            texts.append(current)
        if e.get("type") in ("message_update", "message_end") and current is not None:
            part = m if isinstance(m, dict) else {}
            for blk in (part.get("content") or []):
                if isinstance(blk, dict) and blk.get("text"):
                    current["parts"].append(blk["text"])
    return "\n".join(t["parts"][-1]) if texts and texts[-1]["parts"] else ""


def execute_cell(c: dict, results: Path, rerun_ledger: list) -> None:
    result_path = results / f"{c['anon']}.json"
    if result_path.exists():
        print(f"[{c['anon']}] recorded — skipping (balanced resume)")
        return
    ws = prep_workspace(c["fixture"], c["anon"])
    prompt_file = WS / "prompts" / f"{c['anon']}.md"
    body = prompt_file.read_text()
    if hashlib.sha256(body.encode()).hexdigest() != c.get("prompt_sha"):
        print(f"[{c['anon']}] PROMPT HASH MISMATCH — aborting cell")
        return
    session_dir = WS / "sessions" / c["anon"]
    session_dir.mkdir(parents=True, exist_ok=True)
    script = SYSTEMS / f"{c['system']}.sh"
    env = {**os.environ, "STAGE1_CELL": f"stage1-{c['anon']}",
           "STAGE1_SESSION_DIR": str(session_dir),
           "STAGE1_SUPERPOWERS": str(WS / "superpowers"),
           "STAGE1_WS": str(ws), "STAGE1_PROMPT": str(prompt_file)}
    timeout = UX_TIMEOUT_S if c["kind"] == "ux" else CORE_TIMEOUT_S
    started = time.time()
    proc, timed_out, stderr_tail, partial_stdout = None, False, "", ""
    try:
        proc = sh(["bash", str(script), str(ws), str(prompt_file)],
                  cwd=ws, timeout=timeout, env=env)
    except subprocess.TimeoutExpired as exc:
        timed_out = True
        raw = exc.stdout
        partial_stdout = (raw.decode(errors="replace") if isinstance(raw, bytes)
                          else (raw or ""))
        raw_err = exc.stderr
        stderr_tail = ((raw_err.decode(errors="replace") if isinstance(raw_err, bytes)
                        else (raw_err or ""))[-800:])
    wall_s = round(time.time() - started, 1)

    usage = extract_usage(proc.stdout) if proc is not None else None
    ux_flow = None

    def resume(msg, tag):
        """Continue the SAME session with the SAME pinned arm invocation
        (treatment must be identical on every turn)."""
        sess_files = sorted(session_dir.rglob("*.jsonl"), key=lambda f: f.stat().st_mtime)
        if not sess_files:
            return {"msg": msg, "error": "no session file to resume"}
        base_cmd = arm_command(c["system"], ws, prompt_file, session_dir,
                               f"{c['anon']}-{tag}")
        sep = base_cmd.index("--")
        cmd = base_cmd[:sep] + ["--session", str(sess_files[-1])] + base_cmd[sep:]
        cmd[cmd.index("--") + 1] = msg
        t0 = time.time()
        pr = sh(cmd, cwd=ws, timeout=UX_TIMEOUT_S, env=env)
        (WS / "stdout" / f"{c['anon']}-{tag}.jsonl").write_text(pr.stdout)
        return {"msg": msg, "wall_s": round(time.time() - t0, 1),
                "usage": extract_usage(pr.stdout),
                "exit_code": pr.returncode}

    if c["kind"] == "ux" and proc is not None and proc.returncode == 0:
        expected = "Prototype" if c["fixture"] == "ux-ux1" else "Standard"
        declared = declared_posture(proc.stdout)
        turns = []
        pre_correction_files = None
        if c["mode"] == "blocking":
            turns.append(resume("Yes, proceed.", "t2"))          # scripted proceed
            wrong = declared is not None and declared != expected
            if wrong:
                pre_correction_files = changed_files(ws)   # wasted-work snapshot
                turns.append(resume(f"Actually — deliver this as {expected} "
                                    f"posture. Redo the work from the current state.",
                                    "t3"))
            ux_flow = {"mode": "blocking", "declared": declared,
                       "expected": expected, "correction_sent": wrong,
                       "pre_correction_files": pre_correction_files,
                       "turns": turns}
        else:
            wrong = declared is not None and declared != expected
            if wrong:
                pre_correction_files = changed_files(ws)   # wasted-work snapshot
                turns.append(resume(f"Actually — deliver this as {expected} "
                                    f"posture. Redo the work from the current state.",
                                    "t2"))
            ux_flow = {"mode": "optimistic", "declared": declared,
                       "expected": expected, "correction_sent": wrong,
                       "pre_correction_files": pre_correction_files,
                       "turns": turns}
        if turns:
            merged = dict(usage or {})
            for t in turns:
                for k, v in (t["usage"] or {}).items():
                    merged[k] = merged.get(k, 0) + v
            usage = merged or None

    changed = changed_files(ws)                       # after-work timeouts
    work_happened = bool(changed)                     # ARE graded (council r1)
    verdict = (run_assertions(c["fixture"], ws, changed)
               if c["kind"] == "core" else
               {"UX": {"status": "n/a", "detail": "graded by coder, not mechanically"}})
    stdout_dir = WS / "stdout"
    stdout_dir.mkdir(parents=True, exist_ok=True)
    if proc is not None:
        (stdout_dir / f"{c['anon']}.jsonl").write_text(proc.stdout)
    elif partial_stdout:
        (stdout_dir / f"{c['anon']}.jsonl").write_text(partial_stdout)
    defect = None
    if timed_out and not work_happened:
        defect = "timeout-before-work"                # rerun-eligible
    elif timed_out:
        defect = "timeout-after-work"                 # graded, flagged
    elif proc is None or proc.returncode != 0:
        defect = "nonzero-exit"
    elif "RUNNER_ERROR" in verdict:
        defect = "assertion-harness"
    # telemetry gate (fail-closed): sum all invocation stdouts vs session
    cross = session_usage_total(session_dir)
    stdout_sum = 0
    for sf in list(stdout_dir.glob(f"{c['anon']}*.jsonl")):
        u = extract_usage(sf.read_text())
        stdout_sum += (u or {}).get("totalTokens", 0)
    stdout_total = (usage or {}).get("totalTokens", 0) if proc is not None else None
    telemetry_ok = (stdout_sum == cross) if cross or stdout_sum else True
    if not telemetry_ok:
        defect = defect or "telemetry-mismatch"
    result = {
        "cell": c["anon"], "kind": c["kind"], "fixture": c["fixture"],
        "system": c["system"], "repeat": c["repeat"], "round": c["round"],
        "started": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(started)),
        "wall_s": wall_s, "timeout": timed_out,
        "exit_code": None if proc is None else proc.returncode,
        "defect_class": defect,
        "usage": usage, "session_tokens_crosscheck": cross,
        "telemetry_ok": telemetry_ok,
        "prompt_sha": c.get("prompt_sha"),
        "usage_note": "stdout totalTokens should equal crosscheck "
                      "(council #6 gate; ux cells sum both turns)",
        "changed_files": changed,
        "diff_tail": diff_text(ws)[-4000:] if not timed_out else "",
        "assertions": verdict, "ux_flow": ux_flow,
        "ux_mode": c.get("mode"),
        "rerun_ledger": rerun_ledger,
    }
    result_path.write_text(json.dumps(result, indent=1))
    led = load_ledger()
    led["cost_total"] = round(led["cost_total"] + (usage or {}).get("cost_total", 0.0), 4)
    led["invocations"] += 1 + len((ux_flow or {}).get("turns") or [])
    led["wall_s"] = round(led["wall_s"] + wall_s, 1)
    if c.get("kind") == "followup":
        led["followup_cost"] = round(led["followup_cost"] + (usage or {}).get("cost_total", 0.0), 4)
    (WS / "ledger.json").write_text(json.dumps(led, indent=1))
    summary = ", ".join(f"{k}={v['status']}" for k, v in verdict.items())
    print(f"[{c['anon']}] {c['fixture']}/{c['system']}"
          f"{'' if c['kind'] == 'core' else '/' + c['mode']}"
          f" wall={wall_s}s defect={defect} {summary}")


def load_ledger() -> dict:
    lp = WS / "ledger.json"
    return json.loads(lp.read_text()) if lp.exists() else         {"cost_total": 0.0, "invocations": 0, "wall_s": 0.0, "followup_cost": 0.0}


def preflight_caps(n_new_cells: int) -> list:
    """SOFT ceilings (D-015): warn + flag in the ledger; never stop runs.
    Breaches are raised prominently at evaluation."""
    led = load_ledger()
    flags = []
    if led["cost_total"] >= CEILING_COST_USD:
        flags.append(f"cost ceiling exceeded: ${led['cost_total']:.2f}")
    if led["invocations"] + n_new_cells > CEILING_INVOCATIONS:
        flags.append(f"invocation ceiling will exceed ({led['invocations']}+{n_new_cells}>{CEILING_INVOCATIONS})")
    if led["wall_s"] >= CEILING_WALL_S:
        flags.append(f"wall-clock ceiling exceeded: {led['wall_s']:.0f}s")
    if led.get("followup_cost", 0) >= FOLLOWUP_CEILING_USD:
        flags.append(f"follow-up budget exceeded: ${led['followup_cost']:.2f}")
    if flags:
        existing = {(f.get("flag"), ) for f in led.get("ceiling_flags", [])}
        for f in flags:
            if (f,) not in existing:
                led.setdefault("ceiling_flags", []).append(
                    {"flag": f, "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
        (WS / "ledger.json").write_text(json.dumps(led, indent=1))
    return flags


def preflight_freezes() -> str | None:
    for manifest in (STAGE0 / "freeze-manifest.txt", STAGE1 / "freeze-manifest.txt"):
        if manifest.exists() and sh(["shasum", "-a", "256", "-c", str(manifest)],
                                    cwd=REPO_ROOT).returncode != 0:
            return f"manifest check failed: {manifest}"
    doc = load_schedule()
    recomputed = canonical_schedule_hash({k: v for k, v in doc.items() if k != "sha256"})
    if recomputed != doc.get("sha256"):
        return "schedule self-hash mismatch"
    for c in doc["cells"]:
        pf = WS / "prompts" / f"{c['anon']}.md"
        if not pf.exists() or hashlib.sha256(pf.read_text().encode()).hexdigest() != c["prompt_sha"]:
            return f"prompt hash mismatch: {c['anon']}"
    return None


def cmd_run(args):
    if not (WS / "schedule.json").exists():
        print("no schedule — run `schedule` first")
        return 1
    sched = load_schedule()
    blocker = preflight_freezes()
    if blocker and args[:1] not in (["--retry"],):
        print(f"PREFLIGHT BLOCKED: {blocker}")
        return 1
    cells = sched["cells"]
    results = WS / "results"
    results.mkdir(parents=True, exist_ok=True)
    rerun_ledger = json.loads((WS / "rerun-ledger.json").read_text()) \
        if (WS / "rerun-ledger.json").exists() else []
    sel = []
    if args[:1] == ["--ux"]:
        sel = [c for c in cells if c["kind"] == "ux"]
    elif args[:1] == ["--cell"]:
        want = set(args[1:])
        sel = [c for c in cells if c["anon"] in want]
    elif args[:1] == ["--round"]:
        r = int(args[1])
        sel = [c for c in cells if c["round"] == r and c["kind"] == "core"]
    elif args[:1] == ["--retry"]:
        anon, reason = args[1], " ".join(args[2:])
        if not reason:
            print("--retry requires --cell ID --reason <criteria>")
            return 2
        allowed = ("runner-crash", "nonzero-exit", "provider-failure",
                   "timeout-before-work", "harness-bug", "workspace-prep",
                   "schedule-defect")
        code = reason.split()[0]
        if code not in allowed:
            print(f"reason must start with one of {allowed}")
            return 2
        if len(rerun_ledger) >= DIAG_RERUN_CAP:
            print(f"diagnostic rerun cap ({DIAG_RERUN_CAP}) reached")
            return 2
        # Evidence check (council: no honor-system reruns). attempt-1 must
        # actually exhibit the claimed defect.
        target = results / f"{anon}.json"
        prior = None
        if target.exists():
            prior = json.loads(target.read_text())
        elif (results / f"{anon}.json.attempt1").exists():
            prior = json.loads((results / f"{anon}.json.attempt1").read_text())
        ev_ok, ev_msg = True, "no prior result (runner died before recording)"
        if prior is not None:
            if code == "nonzero-exit":
                ev_ok = prior.get("exit_code") not in (0, None)
                ev_msg = f"exit_code={prior.get('exit_code')}"
            elif code == "timeout-before-work":
                ev_ok = prior.get("timeout") and not prior.get("changed_files")
                ev_msg = f"timeout={prior.get('timeout')} changed={len(prior.get('changed_files') or [])}"
            elif code == "harness-bug":
                ev_ok = "RUNNER_ERROR" in (prior.get("assertions") or {})
                ev_msg = "assertions keys=" + ",".join((prior.get("assertions") or {}).keys())
            elif code == "provider-failure":
                tail = str(prior.get("stderr_tail", ""))
                ev_ok = any(k in tail.lower() for k in ("api", "provider", "connect", "rate", "503", "429"))
                ev_msg = f"stderr markers in: {ev_ok}"
            elif code in ("runner-crash", "workspace-prep", "schedule-defect"):
                ev_ok = len(reason) > len(code) + 20   # requires an operator note
                ev_msg = "operator note required (>20 chars)"
        if not ev_ok:
            print(f"RETRY REFUSED — evidence does not support '{code}' ({ev_msg})")
            return 2
        n = 1
        while (results / f"{anon}.json.attempt{n}").exists():
            n += 1
        if target.exists():
            target.rename(results / f"{anon}.json.attempt{n}")
        rerun_ledger.append({"cell": anon, "reason": reason, "evidence": ev_msg,
                             "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
        (WS / "rerun-ledger.json").write_text(json.dumps(rerun_ledger, indent=1))
        sel = [c for c in cells if c["anon"] == anon]
    elif args[:1] == ["--followup"]:
        # §7 branch 1 (pre-registered): one balanced repeat across all six
        # scenarios x the two H5 arms. Core schedule stays frozen as
        # schedule.core.json; followup cells are appended with fresh opaque IDs.
        if not any(c.get("kind") == "followup" for c in cells):
            core_backup = WS / "schedule.core.json"
            if not core_backup.exists():
                core_backup.write_text(json.dumps(sched, indent=1))
            rng = random.Random(SEED + 1)
            fu = [{"kind": "followup", "fixture": f, "system": arm,
                   "repeat": REPEATS + 1, "round": REPEATS + 1}
                  for f in SCORED for arm in ("superpowers-instruction", "adaptive")]
            rng.shuffle(fu)
            ids = [f"c{100 + i}" for i in range(1, len(fu) + 1)]
            rng.shuffle(ids)
            bodies = build_prompts()
            prompts = WS / "prompts"
            for c, anon in zip(fu, ids):
                c["anon"] = anon
                body = bodies[(c["fixture"], c["system"])]
                c["prompt_sha"] = hashlib.sha256(body.encode()).hexdigest()
                (prompts / f"{anon}.md").write_text(body)
            cells.extend(fu)
            anon_map = json.loads((WS / "cellmap.json").read_text())
            for c in fu:
                anon_map[c["anon"]] = {k: v for k, v in c.items() if k != "anon"}
            (WS / "cellmap.json").write_text(json.dumps(anon_map, indent=1))
            digest = canonical_schedule_hash({"seed": SEED, "cell_count": len(cells),
                                              "cells": cells})
            sched = {"seed": SEED, "cell_count": len(cells), "sha256": digest,
                     "cells": cells, "followup_appended": True}
            (WS / "schedule.json").write_text(json.dumps(sched, indent=1))
            print(f"followup schedule appended: {len(fu)} cells (branch 1)")
        sel = [c for c in cells if c.get("kind") == "followup"]
    else:
        sel = [c for c in cells if c["kind"] == "core"]
    for f in preflight_caps(len(sel)):
        print(f"CEILING FLAG (soft, D-015 — execution continues): {f}")
    for c in sel:
        before = load_ledger()["cost_total"]
        execute_cell(c, results, rerun_ledger)
        if c.get("kind") == "followup":
            led = load_ledger()
            led["followup_cost"] = round(led.get("followup_cost", 0.0)
                                         + max(0.0, led["cost_total"] - before), 4)
            (WS / "ledger.json").write_text(json.dumps(led, indent=1))
    return 0


# ----------------------------------------------------------------- report

def cmd_report():
    sched = load_schedule()
    rows, defects = [], []
    cells_by = {}
    for c in sched["cells"]:
        p = WS / "results" / f"{c['anon']}.json"
        if not p.exists():
            rows.append(f"| {c['anon']} | {c['fixture']} | {c['system']} | MISSING | | | |")
            continue
        r = json.loads(p.read_text())
        key = (c["fixture"], c["system"])
        cells_by.setdefault(key, []).append(r)
        allpass = all(v.get("status") == "pass" for v in r["assertions"].values()) \
            if r["assertions"] else None
        summary = "<br>".join(f"{k}: {v['status']}" for k, v in r["assertions"].items())
        rows.append(f"| {c['anon']} | {c['fixture']} | {c['system']} | {summary} | "
                    f"{'ALL-PASS' if allpass else 'CHECK'} | "
                    f"{(r['usage'] or {}).get('totalTokens', 'n/a')} | "
                    f"{r['defect_class'] or '-'} |")
        if r["defect_class"]:
            defects.append(r)
    lines = ["# Stage 1 run ledger (identity table: workspace cellmap.json)", "",
             "| cell | fixture | system | assertions | verdict | tokens | defect |",
             "|---|---|---|---|---|---|---|", *rows, ""]
    lines += ["## Per-scenario × system (scenario = independent unit)"]
    for (fix, arm), rs in sorted(cells_by.items()):
        toks = sorted((r["usage"] or {}).get("totalTokens", 0) for r in rs)
        walls = sorted(r["wall_s"] for r in rs)
        n = len(rs)
        med_t = toks[n // 2] if n % 2 else (toks[n // 2 - 1] + toks[n // 2]) / 2
        med_w = walls[n // 2] if n % 2 else (walls[n // 2 - 1] + walls[n // 2]) / 2
        lines.append(f"- {fix} / {arm}: cells={n} median_tokens={med_t} "
                     f"median_wall={med_w}s defects="
                     f"{sum(1 for r in rs if r['defect_class'])}")
    led = load_ledger()
    if led.get("ceiling_flags"):
        lines += ["", "## CEILING FLAGS (soft, D-015 — raised for evaluation)"]
        lines += [f"- {f['flag']} — first recorded {f['at']}" for f in led["ceiling_flags"]]
    if defects:
        lines += ["", "## Defect-classified cells (predeclared criteria only)"]
        lines += [f"- {d['cell']}: {d['defect_class']} — {str(d.get('stderr_tail', ''))[:160]}"
                  for d in defects]
    (WS / "summary.md").write_text("\n".join(lines))
    print(f"wrote {WS / 'summary.md'}")
    return 0


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    cmd, args = sys.argv[1], sys.argv[2:]
    if cmd == "validate":
        return cmd_validate()
    if cmd == "schedule":
        return cmd_schedule(force="--force" in args)
    if cmd == "probes":
        return cmd_probes()
    if cmd == "run":
        return cmd_run(args)
    if cmd == "report":
        return cmd_report()
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
