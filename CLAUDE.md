# Project Notes for Claude

## Coding Guidelines
- 명확한 네이밍을 우선한다.
- 구조 변경 시 문서(`AGENTS.md`, `README.md`)를 함께 업데이트한다.

## Workflow Guidelines
- 상태 정본은 `.claude/plans/*.md` 파일이다.
- 구현 작업은 `/develop` 워크플로우와 TDD를 기본으로 수행한다.
- 커밋 전 테스트를 반드시 실행한다.

## Project Structure (Template)

```
.claude/plans/            # Workflow progress source of truth
AGENTS.md                 # Agent instructions and /develop workflow
CLAUDE.md                 # Project notes for Claude/Codex
README.md                 # Onboarding and usage guide
```

## Project-Specific Commands

```bash
# Fill this section with your project's real commands.
# Example:
# .venv/bin/python -m pytest
# npm test
```
