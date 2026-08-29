#!/usr/bin/env bash
# System 1 — unaided Pi. Clean base, identical across all three systems
# (A1 symmetric isolation): same provider/model/thinking, same pinned tool
# set, all discovery disabled. No additions.
set -euo pipefail
WS="$1"; PROMPT_FILE="$2"
cd "$WS"
exec pi -p \
  --provider 9-router \
  --model 9-router/glm-5.3 \
  --thinking high \
  --tools read,bash,edit,write \
  --no-skills --no-extensions --no-context-files --no-prompt-templates \
  --session-dir "${STAGE0_SESSION_DIR:?}" \
  --mode json \
  --name "${STAGE0_CELL:-stage0}" \
  -- "$(cat "$PROMPT_FILE")"
