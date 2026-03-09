# Project Notes for Claude

## Coding Guidelines

- 명확한 네이밍을 우선한다.
- 구조 변경 시 문서(`AGENTS.md`, `docs/DEVELOP_WORKFLOW.md`)를 함께 업데이트한다.

## Workflow Guidelines

- 상태 정본은 `.claude/plans/*.md` 파일이다.
- 구현 작업은 `/develop` 워크플로우와 TDD를 기본으로 수행한다.
- 커밋 전 테스트를 반드시 실행한다.

## Python Environment

```bash
# Use this Python/pytest for running tests
.venv/bin/python -m pytest
```

## Test Commands

```bash
# Run all tests
.venv/bin/python -m pytest

# Run workflow tests only
.venv/bin/python -m pytest tests/tools/test_devflow.py -v
```

## Project Structure (Template)

```
.claude/plans/            # Workflow progress source of truth
AGENTS.md                 # Agent instructions and /develop workflow
CLAUDE.md                 # Project notes for Claude/Codex
README.md                 # Onboarding and usage guide
docs/
└── DEVELOP_WORKFLOW.md   # Codex execution runbook
tools/
├── __init__.py
└── devflow.py            # Workflow helper CLI
tests/
└── tools/
    └── test_devflow.py   # Regression tests for workflow CLI
```
