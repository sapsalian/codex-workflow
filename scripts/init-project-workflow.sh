#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 || $# -gt 2 ]]; then
  echo "Usage: $0 <project-root> [--force]" >&2
  exit 1
fi

TARGET_ROOT="$1"
FORCE_MODE="false"
if [[ ${2:-} == "--force" ]]; then
  FORCE_MODE="true"
fi

if [[ ! -d "$TARGET_ROOT" ]]; then
  echo "error: project root not found: $TARGET_ROOT" >&2
  exit 1
fi

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

copy_file() {
  local src="$1"
  local dst="$2"

  if [[ -f "$dst" && "$FORCE_MODE" != "true" ]]; then
    echo "skip: $dst (already exists)"
    return
  fi

  mkdir -p "$(dirname "$dst")"
  cp "$src" "$dst"
  echo "copied: $dst"
}

copy_file "$REPO_ROOT/AGENTS.md" "$TARGET_ROOT/AGENTS.md"

if [[ ! -d "$TARGET_ROOT/.claude/plans" ]]; then
  echo "error: missing $TARGET_ROOT/.claude/plans" >&2
  echo "hint: install/apply https://github.com/sapsalian/claude-workflow to this project first" >&2
  exit 1
fi

if [[ ! -f "$TARGET_ROOT/CLAUDE.md" ]]; then
  echo "warning: missing $TARGET_ROOT/CLAUDE.md" >&2
  echo "hint: keep project-specific structure, commands, and architecture notes in CLAUDE.md" >&2
fi

echo "done: project workflow template applied"
