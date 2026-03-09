# AGENTS.md

Purpose: help Codex/agents quickly understand project workflow and house rules.

## Golden Rules
- Use clear, self-explanatory names (functions/variables/classes).
- When changing structure or adding files, update docs (this file and/or CLAUDE.md).
- Keep plan/resume behavior intact; avoid breaking plan status markers.
- Prefer small, testable changes and run relevant tests.

## Companion Global Workflow (Required)
- This template must be used with `git@sapsalian:sapsalian/claude-workflow.git` in `~/.claude`.
- Required global components: `settings.json`, `CLAUDE.md`, `hooks/auto-approve-exit-plan.sh`, `skills/develop/SKILL.md`.
- Workflow state source of truth for this project remains `.claude/plans/*.md` under project root.

## Quick Commands
- Update this section per project (build/test/lint commands).

## Project Layout (Template)
- `.claude/plans/`: workflow state source of truth
- `AGENTS.md`: agent instructions and /develop workflow
- `CLAUDE.md`: project notes template
- `README.md`: onboarding and usage guide

## Docs to Keep in Sync
- `AGENTS.md`: agent rules
- `CLAUDE.md`: local project notes
- `README.md`: usage guide

---

## /develop 워크플로우

사용자가 "develop 워크플로우 사용", "/develop", 또는 새 기능/작업 구현을 요청하면 아래 절차를 따른다.

### 1. 기존 Plan 확인

`.claude/plans/*.md` 목록 확인:
- plan 파일이 있으면 목록 보여주고 재개 여부 물어보기
- `[🔄]` / `[⏳]` 상태 Phase가 있으면 해당 Phase부터 재개
- 없으면 Step 2로 진행

### 2. 전체 계획 수립 (Q&A → Plan 파일)

**Q&A 라운드 (최대 3회)** — 라운드마다 아래 형식으로 고려사항 먼저 출력:

```
## 고려 사항 정리 (라운드 N)

### 검토한 사항
- [사항]: [판단]

### 자동 결정한 사항 (명백한 기술적 사실만)
- [사항]: [결정] — 이유: [근거]

### 사용자에게 질문할 사항
- [질문들]
```

검토 항목: 아키텍처/기술 스택, UI/UX 흐름, API/데이터 모델, 에러 처리, 성능 제약, 테스트 전략.
질문할 사항이 없으면 조기 종료. **트레이드오프가 있는 결정은 반드시 질문.**

Q&A 완료 후 Plan 파일 생성:
- 경로: `.claude/plans/YYYY-MM-DD-<slug>.md`
- Phase 단위로 구성 (각 Phase = 독립 동작 가능한 상태)
- 복잡한 Phase는 sub-step으로 분해

```markdown
# <task-title>
<!-- Created: YYYY-MM-DD | Status: in-progress -->

## Context
<왜 필요한지, 목표>

## Phases

### Phase 1: <title> [⏳ 대기]
<목표>
- Step 1: ...
- Step 2: ...

### Phase 2: <title> [⏳ 대기]
<목표>
```

### 3. Phase 반복 실행

각 Phase마다:

**3-1. Phase 세부 설계**
- Phase 세부 Q&A (최대 3회): UI 컴포넌트/상태, 데이터 흐름, 엣지 케이스
- Plan 파일 해당 Phase를 `[🔄 진행 중]` (sub-step 있으면 `[🔄 진행 중] (0/N)`)으로 업데이트

**3-2. Phase 구현 (TDD)**

sub-step이 있으면 각 step마다:
1. 테스트 먼저 작성
2. 기능 구현
3. 테스트 실행 → 통과해야만 다음 step
4. 중간 커밋
5. Plan 파일 카운터 업데이트: `(N/M)`

sub-step이 없으면:
1. 테스트 먼저 작성
2. 기능 구현
3. 테스트 + 빌드 → 통과해야만 다음 단계
4. 커밋

**3-3. Phase 완료**
1. 빌드 실행 → 성공해야만 완료 처리
2. Plan 파일 해당 Phase를 `[✅ 완료]`로 업데이트
3. **Phase 완료 커밋 수행 (필수)**
4. 다음 Phase → 3-1, 없으면 종료

### 4. 전체 완료

- 모든 Phase `[✅]` 확인
- 최종 빌드 + 테스트 통과
- Plan 파일 상단 Status를 `complete`로 변경

### 상태 정본 원칙

- Codex Plan Mode 대화 상태(`~/.codex/...`)는 참고용이다.
- 워크플로우 운영 상태의 정본은 프로젝트 `.claude/plans/*.md`이다.
