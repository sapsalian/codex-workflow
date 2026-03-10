---
name: permission-bootstrap
description: Use this skill when the user wants broad non-destructive command prefix approvals in Codex across projects, while explicitly excluding dangerous commands.
---

# Permission Bootstrap

## Purpose
Register a broad set of safe `prefix_rule` approvals so repetitive approval prompts are reduced across projects.

This skill does not bypass Codex safety checks.

## Hard Safety Exclusions
Never request prefixes for destructive/high-risk commands.

Excluded examples:
- `rm`, `rm -rf`
- `git reset`, `git reset --hard`
- `git clean`
- `git push --force`
- `git branch -D`
- `sudo rm`

## Prefix Sets

### Core Set (recommended first)
- `["git", "push"]`
- `["git", "pull"]`
- `["git", "fetch"]`
- `["git", "add"]`
- `["git", "commit", "-m"]`
- `["git", "remote", "add"]`
- `["npm", "install"]`
- `["npm", "run", "dev"]`
- `["npm", "run", "build"]`
- `["npm", "run", "lint"]`
- `["npm", "run", "test"]`
- `["pip", "install"]`
- `["pytest"]`

### Optional Expansion Set (user-selectable)
Tell the user these are optional and ask whether to include them.

- `["git", "status"]`
- `["git", "log"]`
- `["git", "diff"]`
- `["git", "show"]`
- `["git", "checkout", "-b"]`
- `["git", "switch", "-c"]`
- `["npm", "run", "preview"]`
- `["npm", "ci"]`
- `["pnpm", "install"]`
- `["pnpm", "run", "dev"]`
- `["pnpm", "run", "build"]`
- `["pnpm", "run", "lint"]`
- `["pnpm", "run", "test"]`
- `["yarn", "install"]`
- `["yarn", "dev"]`
- `["yarn", "build"]`
- `["yarn", "lint"]`
- `["yarn", "test"]`

## Execution Flow
1. Tell the user you will register core safe prefixes and offer optional expansion.
2. Run harmless help/read commands with `sandbox_permissions=require_escalated` and `prefix_rule`.
3. If a tool is missing, skip that prefix and continue.
4. Summarize approved/skipped prefixes.

## Suggested harmless commands
- `git push --help` for `["git", "push"]`
- `git pull --help` for `["git", "pull"]`
- `git fetch --help` for `["git", "fetch"]`
- `git add -h` for `["git", "add"]`
- `git commit -h` for `["git", "commit", "-m"]`
- `git remote -h` for `["git", "remote", "add"]`
- `git status -sb` for `["git", "status"]`
- `git log -1 --oneline` for `["git", "log"]`
- `git diff --name-only` for `["git", "diff"]`
- `git show -s --oneline` for `["git", "show"]`
- `npm install --help` for `["npm", "install"]`
- `npm run --help` for all `npm run ...` prefixes
- `pnpm --help` for `pnpm` prefixes
- `yarn --help` for `yarn` prefixes
- `pip install --help` for `["pip", "install"]`
- `pytest --help` for `["pytest"]`
