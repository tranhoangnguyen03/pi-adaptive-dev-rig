#!/usr/bin/env bash
# Stage 1 system 4 — adaptive guidance-only. Clean base (identical to
# unaided.sh) plus the four FROZEN Stage 0 capability guidance skills and
# the FROZEN posture header appended to the system prompt. No stored
# state, no extensions. Stage 0 assets are referenced, never copied or
# modified (verify: shasum -c eval/stage0/freeze-manifest.txt).
set -euo pipefail
WS="$1"; PROMPT_FILE="$2"
STAGE0_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../stage0" && pwd)"
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
  --session-dir "${STAGE1_SESSION_DIR:?}" \
  --mode json \
  --name "${STAGE1_CELL:-stage1}" \
  -- "$(cat "$PROMPT_FILE")"
