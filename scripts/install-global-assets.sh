#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CODEX_HOME_DIR="${CODEX_HOME:-$HOME/.codex}"

TARGET_SKILL_DIR="$CODEX_HOME_DIR/skills/permission-bootstrap"
TARGET_PROMPT_DIR="$CODEX_HOME_DIR/prompts"

mkdir -p "$TARGET_SKILL_DIR" "$TARGET_PROMPT_DIR"

cp "$REPO_ROOT/global/skills/permission-bootstrap/SKILL.md" "$TARGET_SKILL_DIR/SKILL.md"
cp "$REPO_ROOT/global/prompts/permission-bootstrap.prompt.md" "$TARGET_PROMPT_DIR/permission-bootstrap.prompt.md"

echo "Installed skill: $TARGET_SKILL_DIR/SKILL.md"
echo "Installed prompt: $TARGET_PROMPT_DIR/permission-bootstrap.prompt.md"
echo "Invoke in Codex chat with: permission-bootstrap 사용해줘"
