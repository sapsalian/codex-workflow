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
2. Run harmless verification commands with `sandbox_permissions=require_escalated` and `prefix_rule`.
3. Make the executed command start with the exact target prefix. Do not use generic help forms that change the saved prefix, such as `npm run --help` or `git remote -h`, when the goal is `npm run dev` or `git remote add`.
4. It is acceptable for the verification command to exit non-zero if it only prints usage/help and performs no side effect.
5. If a tool is missing, skip that prefix and continue.
6. Summarize approved/skipped prefixes, and call out any prefix that appears to have been saved too narrowly.

## Suggested harmless commands
- `git push --help` for `["git", "push"]`
- `git pull --help` for `["git", "pull"]`
- `git fetch --help` for `["git", "fetch"]`
- `git add -h` for `["git", "add"]`
- `git commit -m codex-prefix-check --dry-run --allow-empty` for `["git", "commit", "-m"]`
- `git remote add` for `["git", "remote", "add"]`
- `git status -sb` for `["git", "status"]`
- `git log -1 --oneline` for `["git", "log"]`
- `git diff --name-only` for `["git", "diff"]`
- `git show -s --oneline` for `["git", "show"]`
- `npm install --help` for `["npm", "install"]`
- `npm run dev --help` for `["npm", "run", "dev"]`
- `npm run build --help` for `["npm", "run", "build"]`
- `npm run lint --help` for `["npm", "run", "lint"]`
- `npm run test --help` for `["npm", "run", "test"]`
- `npm run preview --help` for `["npm", "run", "preview"]`
- `npm ci --help` for `["npm", "ci"]`
- `pnpm install --help` for `["pnpm", "install"]`
- `pnpm run dev --help` for `["pnpm", "run", "dev"]`
- `pnpm run build --help` for `["pnpm", "run", "build"]`
- `pnpm run lint --help` for `["pnpm", "run", "lint"]`
- `pnpm run test --help` for `["pnpm", "run", "test"]`
- `yarn install --help` for `["yarn", "install"]`
- `yarn dev --help` for `["yarn", "dev"]`
- `yarn build --help` for `["yarn", "build"]`
- `yarn lint --help` for `["yarn", "lint"]`
- `yarn test --help` for `["yarn", "test"]`
- `pip install --help` for `["pip", "install"]`
- `pytest --help` for `["pytest"]`
