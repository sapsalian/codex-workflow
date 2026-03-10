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

**Q&A 라운드 가이드라인 (전체 설계)**
- 전체 설계 Q&A는 **3라운드 필수**
- 3라운드 이후에도 파생 고려사항이 있으면 4라운드, 5라운드로 계속 진행

전체 설계 시 검토 체크리스트:
- 아키텍처/기술: 기술 스택 선택, 패키지 추가 여부, 기존 패턴과 일관성
- UI/UX: 레이아웃 구조, 네비게이션 흐름, 반응형, 빈 상태/로딩/에러 상태 처리
- API/인터페이스: 엔드포인트 설계, 요청/응답 형식, 버전 관리
- 데이터 모델: 필드 구조, 타입, 관계, 영속화 방식
- 에러 처리: 사용자에게 노출할 에러 메시지, 복구 흐름
- 성능/제약: 페이지네이션, 캐싱, 동시성 처리 필요 여부
- 테스트 전략: 단위/통합/e2e 범위, 모킹 대상

라운드마다 아래 형식으로 고려사항 먼저 출력:

```
## 고려 사항 정리 (라운드 N)

### 검토한 사항
- [사항]: [판단]

### 자동 결정한 사항 (명백한 기술적 사실만)
- [사항]: [결정] — 이유: [근거]

### 사용자에게 질문할 사항
- [질문들]
```

Q&A 규칙:
- 전체 설계 3라운드 필수: 질문이 없더라도 3라운드까지 진행
- 3라운드 이후 연장: 파생 고려사항이 남으면 계속 진행
- 종료 조건: 3라운드 완료 후 파생 고려사항이 없고 모든 사항이 확정된 경우
- 적극적으로 질문: 트레이드오프가 있는 결정은 반드시 질문
- 자동 결정은 명백한 기술적 사실에만 한정

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
- Phase 세부 설계 Q&A도 **3라운드 필수**, 이후 파생 고려사항 있으면 계속 진행
- 라운드 시작 전 아래 체크리스트를 검토하고 고려사항 요약 출력

Phase 세부 설계 시 검토 체크리스트:
- UI 컴포넌트: 컴포넌트 분해 방식, props 인터페이스, 상태 관리 위치
- UI 상태: 로딩/에러/빈 상태/성공 상태 표현 방식
- 사용자 인터랙션: 클릭/입력/드래그 흐름, 피드백 방식(토스트/인라인/모달)
- 데이터 흐름: 상위→하위 props 전달 vs 전역 상태 vs 로컬 상태
- 구현 순서: 의존성 고려한 sub-step 순서, 병렬 가능 여부
- 엣지 케이스: 경계값, 권한, 중복 요청 방지

- Plan 파일 해당 Phase를 `[🔄 진행 중]`으로 업데이트
- sub-step이 있으면 `[🔄 진행 중] (0/N)` 형식 사용

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
4. 중간 커밋

**3-3. Phase 완료**
1. 빌드 실행 → 성공해야만 완료 처리
2. Plan 파일 해당 Phase를 `[✅ 완료]`로 업데이트
3. **Phase 완료 커밋 수행 (필수)**
4. 다음 Phase → 3-1, 없으면 종료

### 4. 전체 완료

- 모든 Phase `[✅]` 확인
- 최종 빌드 + 테스트 통과
- Plan 파일 상단 Status를 `complete`로 변경

### Plan 파일 관리 원칙

- 경로: `{프로젝트 루트}/.claude/plans/YYYY-MM-DD-<task-slug>.md`
- Phase 상태 마커: `[✅ 완료]` `[🔄 진행 중]` `[⏳ 대기]`
- 시스템 plan 파일(`~/.claude/plans/`)과 프로젝트 plan 파일(`.claude/plans/`)을 둘 다 유지
  - 시스템 plan 파일: ExitPlanMode 승인 UI용 (임시)
  - 프로젝트 plan 파일: 영구 기록 + Phase 상태 추적
