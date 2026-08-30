#!/usr/bin/env bash
# System 2 — current Pi-superpowers + one concise right-sizing instruction
# (H5's rival). Clean base identical to unaided.sh, plus the pinned
# pi-superpowers package: all 13 skills from the package manifest
# (skills/), loaded from the frozen clone in the evaluation workspace.
# The right-sizing instruction is appended to the task prompt (D6:
# prompt-append, mirrors real-world use), handled by the runner.
#
# Deviation note: the package manifest also enables extensions/plan-tracker.ts.
# Step 0 probe E confirmed it loads cleanly under -p with exit 0, so it is
# included per the manifest (A1: package as shipped). The env record in
# README.md carries the probe evidence.
set -euo pipefail
WS="$1"; PROMPT_FILE="$2"
CLONE="${STAGE0_SUPERPOWERS:?}"
SKILLS_DIR="$CLONE/skills"
SKILL_FLAGS=()
for entry in "$SKILLS_DIR"/*/; do
  [ -f "$entry/SKILL.md" ] && SKILL_FLAGS+=(--skill "${entry%/}")
done
cd "$WS"
exec pi -p \
  --provider 9-router \
  --model 9-router/glm-5.3 \
  --thinking high \
  --tools read,bash,edit,write \
  --no-skills --no-extensions --no-context-files --no-prompt-templates \
  "${SKILL_FLAGS[@]}" \
  -e "$CLONE/extensions/plan-tracker.ts" \
  --session-dir "${STAGE0_SESSION_DIR:?}" \
  --mode json \
  --name "${STAGE0_CELL:-stage0}" \
  -- "$(cat "$PROMPT_FILE")"
