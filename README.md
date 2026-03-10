# Codex Home Repo

이 저장소는 `~/.codex` 자체를 Git으로 관리하기 위한 저장소입니다.

목적:
- 전역 Codex skill 관리
- 전역 prompt 관리
- 새 프로젝트에 최소 `AGENTS.md`를 생성하는 부트스트랩 제공

이 저장소는 더 이상 "프로젝트 템플릿 배포 저장소"가 아닙니다.
프로젝트별 파일은 각 프로젝트 루트에 두고, 전역 워크플로우는 이 저장소에서 관리합니다.

## 선행 조건

각 실제 프로젝트에는 먼저 [claude-workflow](https://github.com/sapsalian/claude-workflow)가 적용되어 있어야 합니다.

이유:
- `.claude/plans/` 구조는 `claude-workflow`가 담당
- 프로젝트별 구조, 명령, 아키텍처 메모는 각 프로젝트의 `CLAUDE.md`가 담당
- 이 저장소는 Codex 전역 skill/prompt와 최소 `AGENTS.md` 부트스트랩만 담당

## 설치

권장 설치 경로는 `~/.codex`입니다.

```bash
git clone git@sapsalian:sapsalian/codex-workflow.git ~/.codex
cd ~/.codex
```

이미 `~/.codex`가 있으면 적절히 백업하거나 별도 위치에서 확인 후 교체합니다.

## 제공 항목

- `skills/develop/SKILL.md`
  - 구현 작업용 전역 워크플로우
  - 프로젝트의 `CLAUDE.md`를 먼저 읽고 Q&A, plan 생성/재개, phase 진행 수행
- `skills/permission-bootstrap/SKILL.md`
  - 안전한 비파괴 명령 위주의 `prefix_rule` 승인 부트스트랩
- `skills/init-project-agents/SKILL.md`
  - 프로젝트 루트에 최소 `AGENTS.md` 생성/갱신
- `prompts/permission-bootstrap.prompt.md`
  - 권한 부트스트랩 호출용 저장 프롬프트

## 기본 사용 순서

### 1. 프로젝트 준비

대상 프로젝트에 아래가 이미 있어야 합니다.

- `.claude/plans/`
- `CLAUDE.md`

즉, 먼저 `claude-workflow`를 적용합니다.

### 2. 최소 `AGENTS.md` 생성

Codex 채팅에서:

```text
init-project-agents 사용해줘
```

이 skill의 역할:
- 프로젝트 루트의 `CLAUDE.md`를 우선 참고하라고 명시
- 구현 작업은 `develop` workflow/skill을 우선 사용하라고 명시
- 작업으로 프로젝트 맥락이 바뀌면 `CLAUDE.md`를 업데이트하라고 명시

생성 대상 파일:
- `AGENTS.md`

이 파일은 프로젝트 루트에 남겨두는 운영 파일입니다. 사용 후 삭제하지 않습니다.

### 3. 권한 부트스트랩

Codex 채팅에서:

```text
permission-bootstrap 사용해줘
```

동작:
- 넓은 범위의 안전한 prefix 승인 요청
- optional 확장 세트는 선택사항이라고 먼저 안내
- 위험 명령(`rm -rf`, `git reset --hard`, `git clean`, `git push --force` 등)은 제외

### 4. 구현 작업 시작

Codex 채팅에서:

```text
/develop <요구사항>
```

또는:

```text
develop 사용해줘. <요구사항>
```

`develop` skill은:
- 프로젝트의 `CLAUDE.md`를 먼저 읽고
- 요구사항 구체화 + 기술 검토 Q&A를 진행하고
- `.claude/plans/*.md` 기준으로 계획을 생성/재개하고
- phase 단위로 구현을 진행합니다.

## 프로젝트에 실제로 필요한 파일

각 프로젝트에 유지되어야 하는 파일:
- `AGENTS.md`
- `CLAUDE.md`
- `.claude/plans/` 이하 plan 파일들

각 프로젝트에 복사하지 않는 파일:
- `skills/`
- `prompts/`
- 이 저장소의 `README.md`

즉:
- 전역 파일은 `~/.codex`
- 프로젝트 로컬 파일은 각 프로젝트 루트

## 업데이트 방법

이 저장소를 업데이트하면 전역 skill/prompt도 함께 업데이트됩니다.

```bash
cd ~/.codex
git pull
```

프로젝트 로컬 `AGENTS.md`는 자동 갱신되지 않습니다.
필요하면 다시 `init-project-agents` skill을 실행해 현재 표준으로 맞춥니다.

## 운영 원칙

- 전역 workflow 로직은 이 저장소의 `skills/`에서 관리
- 프로젝트별 맥락은 각 프로젝트의 `CLAUDE.md`에서 관리
- 프로젝트 공통 최소 가드레일은 각 프로젝트의 `AGENTS.md`에서 관리
