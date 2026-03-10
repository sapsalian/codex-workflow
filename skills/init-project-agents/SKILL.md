---
name: init-project-agents
description: Create or refresh the minimal AGENTS.md file in the current project so Codex consistently reads CLAUDE.md first and uses the develop workflow.
---

# Init Project Agents

## Purpose
Create or refresh a minimal project-local `AGENTS.md`.

This skill exists because Codex reads `AGENTS.md` from the current project, not from `~/.codex` globally.

## Before writing
Check the current project root.

Verify:
- whether `AGENTS.md` already exists
- whether `CLAUDE.md` exists
- whether `.claude/plans/` exists

If `CLAUDE.md` or `.claude/plans/` is missing, warn the user that [claude-workflow](https://github.com/sapsalian/claude-workflow) should be applied first.

## Target content
Write this exact minimal structure unless the user explicitly wants project-specific additions:

```md
# AGENTS.md

- Read `CLAUDE.md` first for project-specific structure, commands, constraints, and domain rules.
- Use the `develop` workflow or `develop` skill for implementation work whenever possible.
- Keep `CLAUDE.md` updated when implementation changes project structure, commands, architecture notes, constraints, or other project context.
```

## Update rules
- If `AGENTS.md` already exists and has unrelated project-specific rules, preserve them unless the user asked to overwrite them.
- If the file is already equivalent in intent, report that no change is needed.
- Keep the file short. Do not copy full develop workflow details into `AGENTS.md`.

## Completion
Summarize:
- whether `AGENTS.md` was created or updated
- whether `CLAUDE.md` is present
- whether `.claude/plans/` is present
