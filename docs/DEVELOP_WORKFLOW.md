# /develop Execution Workflow (Codex)

This file is a local runbook for executing `/develop` workflow in Codex.
The source of truth for workflow progress is project plan files under `.claude/plans/*.md`.

## Why this exists
- Claude-only hooks (`PermissionRequest`, `EnterPlanMode`, `ExitPlanMode`) are unavailable in Codex runtime.
- Codex can still execute the same workflow quality with explicit commands and plan files.

## Workflow
1. Start or resume planning.
2. Run Q&A rounds and lock decisions.
3. Build by phase with TDD.
4. Gate each phase with tests, git-state checks, and conventional commit message validation.
5. Mark phase completion (local update by default).
6. Mark plan `Status: complete` only after all phases are complete.

## Plan file rules
- Path: `.claude/plans/YYYY-MM-DD-<slug>.md`
- Phase markers:
  - `[⏳ 대기]`
  - `[🔄 진행 중]`
  - `[✅ 완료]`
- Header meta:
  - `<!-- Created: YYYY-MM-DD | Status: in-progress -->`
  - completion: `<!-- Created: ... | Status: complete | Completed: YYYY-MM-DD -->`

## Codex vs Plan Mode storage
- Codex Plan Mode conversation is saved in `~/.codex` session/state storage.
- Operational workflow state must be maintained in `.claude/plans/*.md`.

## CLI
Use the local CLI:

```bash
python -m tools.devflow new "요구사항"
python -m tools.devflow resume
python -m tools.devflow check-phase --phase 1 --message "feat(devflow): gate phase"
python -m tools.devflow complete-phase --phase 1 --message "feat(devflow): complete phase"
python -m tools.devflow complete-plan --message "chore: complete workflow plan"
```

Optional:
- `--plan <path>`: explicitly target a plan file.
- `--test-cmd "..."`: override default test command (`.venv/bin/python -m pytest`).
- `--commit`: commit immediately after `complete-phase`/`complete-plan`.

## Failure recovery
- Test failed: fix implementation or tests, rerun `check-phase`.
- Commit message invalid: rewrite in conventional style.
- Untracked files blocked: stage or remove unexpected files before `complete-*`.
- Wrong phase selected: use `resume` and validate target phase first.
