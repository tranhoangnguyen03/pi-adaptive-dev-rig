#!/usr/bin/env bash
# System 3 — adaptive guidance-only. Clean base (identical to unaided.sh),
# plus the four capability guidance skills and the posture header appended
# to the system prompt. No stored state, no extensions.
set -euo pipefail
WS="$1"; PROMPT_FILE="$2"
STAGE0_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$WS"
exec pi -p \
  --provider 9-router \
  --model 9-router/glm-5.3 \
  --thinking high \
  --tools read,bash,edit,write \
  --no-skills --no-extensions --no-context-files --no-prompt-templates \
  --skill "$STAGE0_DIR/guidance/explore-design.md" \
  --skill "$STAGE0_DIR/guidance/debug.md" \
  --skill "$STAGE0_DIR/guidance/test-verify.md" \
  --skill "$STAGE0_DIR/guidance/review.md" \
  --append-system-prompt "$STAGE0_DIR/header/posture-header.md" \
  --session-dir "${STAGE0_SESSION_DIR:?}" \
  --mode json \
  --name "${STAGE0_CELL:-stage0}" \
  -- "$(cat "$PROMPT_FILE")"
