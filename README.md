# Codex Workflow

이 저장소는 두 가지를 함께 제공합니다.

- 프로젝트 로컬 워크플로우 템플릿 (`AGENTS.md`, `CLAUDE.md`, `.claude/plans/`)
- Codex 전역 스킬 자산 (`permission-bootstrap`)

## 권장 구조

- `codex-workflow` 저장소는 한 번 클론해서 기준 저장소로 유지
- 각 프로젝트에는 템플릿 파일만 적용
- 전역 스킬은 `~/.codex`에 설치

즉, 한 저장소를 "템플릿 + 전역 자산 배포 소스"로 사용합니다.

중요 제한:
- `AGENTS.md`는 각 프로젝트 루트에 있어야 적용됩니다.
- `~/.codex`에만 두면 프로젝트 규칙으로 자동 적용되지 않습니다.

## 1) 저장소 클론

```bash
git clone git@sapsalian:sapsalian/codex-workflow.git ~/workflows/codex-workflow
cd ~/workflows/codex-workflow
```

## 2) 전역 자산 설치 (`~/.codex`)

```bash
./scripts/install-global-assets.sh
```

설치 대상:
- `~/.codex/skills/permission-bootstrap/SKILL.md`

## 3) 프로젝트에 워크플로우 템플릿 적용

```bash
./scripts/init-project-workflow.sh /path/to/your-project
```

기본 동작:
- 기존 파일이 있으면 덮어쓰지 않음
- 생성/복사 대상:
  - `AGENTS.md`
  - `CLAUDE.md`
  - `.claude/plans/.gitkeep`

강제 덮어쓰기:

```bash
./scripts/init-project-workflow.sh /path/to/your-project --force
```

## 4) Codex에서 권한 부트스트랩 실행

프로젝트 채팅에서:

```text
permission-bootstrap 사용해줘
```

또는:

```text
$permission-bootstrap 사용
```

스킬 동작:
- 비파괴 명령 위주 prefix 승인 요청
- 위험 명령(`rm -rf`, `git reset --hard`, `git clean`, `git push --force` 등)은 제외
- optional 확장 세트는 선택 사항으로 안내 후 진행

## 5) /develop 실행

```text
/develop <요구사항>
```

## 업데이트 정책 (질문 5 답변)

업데이트 정책은 "이 저장소가 바뀌었을 때, 이미 설치된 전역 자산을 언제/어떻게 다시 동기화할지"를 의미합니다.

현재 정책:
- 수동 재동기화(권장)
  1. `cd ~/workflows/codex-workflow && git pull`
  2. `./scripts/install-global-assets.sh` 재실행

이 방식의 장점:
- 언제 전역 설정이 바뀌는지 사용자가 통제 가능
- 예상치 못한 자동 변경 방지

## 포함 파일

- `AGENTS.md`: 공통 /develop 실행 규칙 템플릿
- `CLAUDE.md`: 프로젝트 컨텍스트 템플릿
- `global/skills/permission-bootstrap/SKILL.md`: 전역 권한 부트스트랩 스킬
- `scripts/install-global-assets.sh`: 전역 스킬 설치 스크립트
- `scripts/init-project-workflow.sh`: 프로젝트 템플릿 적용 스크립트
