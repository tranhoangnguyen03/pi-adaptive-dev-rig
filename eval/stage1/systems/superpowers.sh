#!/usr/bin/env bash
# Stage 1 system 2 — current pinned Pi-superpowers, package as shipped
# (skills + extension from the pinned clone in the evaluation workspace).
# Clean base identical to unaided.sh. The right-sizing instruction is NOT
# present here — that is system 3's only difference (prompt-appended,
# D6). Compare with cmp superpowers.sh superpowers-instruction.sh.
set -euo pipefail
WS="$1"; PROMPT_FILE="$2"
CLONE="${STAGE1_SUPERPOWERS:?}"
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
  --session-dir "${STAGE1_SESSION_DIR:?}" \
  --mode json \
  --name "${STAGE1_CELL:-stage1}" \
  -- "$(cat "$PROMPT_FILE")"
