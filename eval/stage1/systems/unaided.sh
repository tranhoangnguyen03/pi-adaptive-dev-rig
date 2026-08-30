#!/usr/bin/env bash
# Stage 1 system 1 — unaided Pi. Clean symmetric base, identical across
# all four systems (A1 symmetric isolation): same provider/model/thinking,
# pinned tool set, all discovery disabled. No additions.
set -euo pipefail
WS="$1"; PROMPT_FILE="$2"
cd "$WS"
exec pi -p \
  --provider 9-router \
  --model 9-router/glm-5.3 \
  --thinking high \
  --tools read,bash,edit,write \
  --no-skills --no-extensions --no-context-files --no-prompt-templates \
  --session-dir "${STAGE1_SESSION_DIR:?}" \
  --mode json \
  --name "${STAGE1_CELL:-stage1}" \
  -- "$(cat "$PROMPT_FILE")"
