# Codex /develop Workflow Template

이 저장소는 Codex 채팅에서 `/develop` 워크플로우를 실행하기 위한 최소 템플릿입니다.

## 목적
- 프로젝트마다 동일한 `/develop` 실행 규칙 유지
- `.claude/plans/*.md`를 워크플로우 상태 정본으로 사용
- 채팅 지시만으로 계획-구현-검증 루프 운영

## Claude Workflow와 함께 사용 (필수)
이 템플릿은 아래 전역 설정 저장소와 **항상 함께** 사용합니다.

- 전역 저장소: `git@sapsalian:sapsalian/claude-workflow.git`
- 전역 위치: `~/.claude`
- 확인된 핵심 파일: `settings.json`, `CLAUDE.md`, `hooks/auto-approve-exit-plan.sh`, `skills/develop/SKILL.md`

### 1) 새 환경 설치 (`~/.claude` 없음)

```bash
git clone git@sapsalian:sapsalian/claude-workflow.git ~/.claude
chmod +x ~/.claude/hooks/auto-approve-exit-plan.sh
```

### 2) 기존 `~/.claude`에 적용

```bash
cd ~/.claude
git init
git remote add origin git@sapsalian:sapsalian/claude-workflow.git
git fetch origin
git checkout main -- settings.json CLAUDE.md hooks/ skills/
chmod +x ~/.claude/hooks/auto-approve-exit-plan.sh
```

### 3) 업데이트

```bash
cd ~/.claude
git pull
chmod +x hooks/auto-approve-exit-plan.sh
```

## 역할 분리
- `~/.claude` (`claude-workflow`): 전역 권한/훅/스킬(특히 `/develop` 스킬)
- 프로젝트 루트 (`codex-workflow` 템플릿): 프로젝트별 실행 규칙과 plan 기록

## 포함 파일 (최소 구성)
- `AGENTS.md`: 에이전트 운영 규칙 + `/develop` 절차
- `CLAUDE.md`: 프로젝트별 메모 템플릿
- `.claude/plans/.gitkeep`: plan 디렉터리 유지
- `.gitignore`: 로컬 plan 파일/캐시 제외 정책

## Codex 채팅에서 실행 방법
다음처럼 채팅에 요청하면 됩니다.

```text
/develop 결제 API 재시도 정책 추가
```

또는 자연어로 요청해도 동일합니다.

```text
develop 워크플로우 사용해서 결제 API 재시도 정책 추가해줘
```

## 실제 동작 원칙
- 에이전트는 `AGENTS.md`의 `/develop 워크플로우`를 따름
- Plan은 `.claude/plans/YYYY-MM-DD-<slug>.md` 형식으로 생성/갱신
- 상태는 `[⏳ 대기]`, `[🔄 진행 중]`, `[✅ 완료]` 마커로 관리
- 최종 완료 시 plan 메타 `Status: complete`로 변경

## 새 프로젝트 적용 순서
1. 이 저장소를 새 레포로 복제
2. 먼저 `~/.claude`에 `claude-workflow` 적용 확인
3. `AGENTS.md`의 `Project Layout`/Quick Commands를 프로젝트 실정에 맞게 수정
4. `CLAUDE.md`의 실행/테스트 명령을 프로젝트 명령으로 교체
5. 이후 구현 요청은 채팅에서 `/develop ...`로 시작

## 운영 팁
- 상태 정본은 항상 `.claude/plans/*.md`
- 구조가 바뀌면 `AGENTS.md`, `CLAUDE.md`를 같이 업데이트
- 각 phase는 독립적으로 동작 가능한 단위로 나누는 것이 안전
