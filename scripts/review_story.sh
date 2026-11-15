#!/usr/bin/env bash
# Deliverable 6: run the reviewer subagent headless on the S-3 files changed since the lock,
# and save a JSON report that must match agent/review-schema.json.
# Run from the repository root, under the normal permission rules in .claude/settings.json
# (no --dangerously-skip-permissions, no bypass mode, no --bare).
set -euo pipefail
cd "$(dirname "$0")/.."

FILES=$(git diff --name-only m2-tests-locked HEAD -- src)
PROMPT="Use the reviewer subagent to review these files against
docs/design/S-3.md and its acceptance criteria.
Report only what the reviewer finds. Files: $FILES"

claude -p "$PROMPT" --output-format json \
  --json-schema "$(cat agent/review-schema.json)" < /dev/null > evidence/headless-review.json

echo "Saved evidence/headless-review.json (report in its structured_output field)."
