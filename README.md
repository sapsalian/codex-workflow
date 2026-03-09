# Codex Workflow Template

이 저장소는 특정 서비스 코드 없이, Codex 에이전트 협업 워크플로우만 재사용할 수 있도록 만든 템플릿입니다.

핵심 목표는 다음 3가지입니다.
- `/develop` 중심의 계획-구현-검증 루프를 프로젝트별로 동일하게 적용
- `.claude/plans/*.md`를 단일 상태 정본(source of truth)으로 사용
- `tools/devflow.py`로 phase 게이트(테스트/커밋 메시지/깃 상태)를 자동 검증

## 포함된 파일

- `AGENTS.md`: 에이전트 운영 규칙 + `/develop` 워크플로우
- `CLAUDE.md`: 협업 시 참고할 프로젝트 노트 템플릿
- `docs/DEVELOP_WORKFLOW.md`: Codex 런타임에서 워크플로우를 실행하는 런북
- `tools/devflow.py`: plan 생성/재개/phase 점검/완료 자동화 CLI
- `tests/tools/test_devflow.py`: `tools/devflow.py` 회귀 테스트
- `.claude/plans/.gitkeep`: plan 디렉터리 유지용 파일

## 빠른 시작

1. 가상환경 생성

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. 테스트 도구 설치

```bash
pip install -U pip pytest
```

3. 동작 확인

```bash
python -m tools.devflow --help
python -m pytest tests/tools/test_devflow.py -v
```

## Codex 채팅에서 바로 실행하기

CLI를 직접 치지 않아도, 현재 Codex 채팅 세션에서 바로 워크플로우를 실행할 수 있습니다.

- 채팅에 `/develop <요구사항>` 형태로 요청
- 또는 `develop 워크플로우 사용해서 ...`처럼 자연어로 요청
- 에이전트가 `AGENTS.md` 규칙에 맞춰 plan 확인/생성, phase 진행, 테스트/검증까지 순서대로 수행

예시 요청:

```text
/develop 결제 API 재시도 정책 추가
```

## 새 프로젝트에 붙여서 쓰는 방법

1. 이 템플릿을 새 레포로 복제합니다.
2. `AGENTS.md`의 `Project Layout` 섹션을 현재 프로젝트 구조에 맞게 수정합니다.
3. `CLAUDE.md`에 실제 실행/테스트 명령을 적습니다.
4. 개발 요청이 들어오면 `/develop` 워크플로우를 사용해 plan 파일부터 생성합니다.

## /develop 워크플로우 실행 예시

### 1) plan 생성

```bash
python -m tools.devflow new "결제 API 에러 재시도 정책 추가"
```

### 2) 재개할 phase 확인

```bash
python -m tools.devflow resume
```

### 3) phase 진입 전 게이트 체크

```bash
python -m tools.devflow check-phase \
  --phase 1 \
  --message "feat(api): add payment retry policy" \
  --test-cmd ".venv/bin/python -m pytest"
```

### 4) phase 완료 처리

```bash
python -m tools.devflow complete-phase \
  --phase 1 \
  --message "feat(api): complete payment retry policy" \
  --commit
```

### 5) 전체 plan 완료 처리

```bash
python -m tools.devflow complete-plan \
  --message "chore(workflow): complete payment retry plan" \
  --commit
```

## 운영 규칙 요약

- 상태 정본은 반드시 `.claude/plans/*.md`
- phase는 `[⏳ 대기]`, `[🔄 진행 중]`, `[✅ 완료]` 마커 사용
- 커밋 메시지는 Conventional Commit 스타일 강제
- `complete-* --commit`은 `.claude/**`를 자동으로 커밋 제외

## 권장 일상 루틴

1. 작업 시작: `resume`으로 현재 phase 확인
2. 구현 전: 테스트 먼저 작성(TDD)
3. 구현 후: `check-phase` 통과 확인
4. phase 종료: `complete-phase`
5. 마지막: 모든 phase 완료 후 `complete-plan`

## 문제 해결

- `invalid commit message`: `feat(scope): ...` 형식으로 수정
- `unexpected untracked files`: 불필요 파일 정리 또는 스테이징
- `no in-progress plan file found`: `new`로 plan 생성하거나 plan 메타의 Status 확인

## 참고

- 워크플로우 상세 설명: `docs/DEVELOP_WORKFLOW.md`
- 운영 규칙: `AGENTS.md`
- 보조 명령 구현: `tools/devflow.py`
