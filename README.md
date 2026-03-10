# Codex Home Repo

`~/.codex`를 Git으로 관리하는 저장소. Claude가 자의적으로 진행하지 않도록 제어하는 개발 워크플로우 자동화 — Q&A → 설계 → 구현 각 단계마다 사용자 확인을 강제하고, plan 파일로 상태를 추적합니다. 전역 Codex skill과 prompt를 담당하며, 프로젝트 로컬 파일은 각 프로젝트 루트에서 관리합니다.

## Claude Code와의 협업

Codex와 Claude Code는 **피어(peer) 관계**입니다.

| 스킬 | 용도 |
|---|---|
| `dev-full` | Q&A + 설계 + 구현 전 과정 (독립 실행) |
| `dev-design` | Q&A + plan 생성만. 구현은 언제든 dev-impl로 |
| `dev-impl` | plan 픽업 + 처방 검토 + 구현 |
| `cothink` | plan 없이 Q&A 반복 후 요청 수행 |

### 권장 협업 패턴

**설계와 구현을 분리할 때:**
- Claude Code `/dev-design` → plan 파일의 `세부 설계` 섹션 채우기
- Codex `dev-impl` → plan 픽업 → 처방 검토 → 구현

**양방향 핸드오프:**
- Claude Code → Codex: 세부 설계 완료된 Phase부터 `dev-impl`로
- Codex → Claude Code: 복잡한 디버깅, 구조 변경, 새 Phase 설계가 필요할 때

**핸드오프 신호**: plan 파일 각 Phase의 `#### 세부 설계` 섹션이 채워진 상태

```markdown
### Phase N: <title> [⏳ 대기]
**Goal**: <한 줄 목표>

#### 세부 설계
<!-- 비어있으면 = 설계 Q&A 필요 -->
<!-- 채워져 있으면 = 구현 준비 완료 -->

#### Sub-steps
- [ ] Step 1: ...
```

### CLAUDE.md 상태

- 각 프로젝트 루트에 존재 (git 추적 여부는 프로젝트마다 다름)
- Claude Code와 Codex 양쪽 모두 이 파일을 읽음

## 선행 조건

각 프로젝트에 [claude-workflow](https://github.com/sapsalian/claude-workflow)가 적용되어 있어야 합니다 (`.claude/plans/`, `CLAUDE.md` 제공).

## 제공 항목

### 개발 워크플로우 스킬

| 파일 | 스킬 | 용도 |
|---|---|---|
| `skills/dev-full/SKILL.md` | `dev-full` | Q&A + 설계 + 구현 전 과정 |
| `skills/dev-design/SKILL.md` | `dev-design` | Q&A + plan 생성 전담 |
| `skills/dev-impl/SKILL.md` | `dev-impl` | plan 픽업 + 처방 검토 + 구현 |
| `skills/cothink/SKILL.md` | `cothink` | plan 없이 Q&A 반복 후 요청 수행 |

### 유틸리티 스킬 / 프롬프트

| 파일 | 용도 |
|---|---|
| `skills/permission-bootstrap/SKILL.md` | 안전한 비파괴 명령 위주의 prefix_rule 승인 부트스트랩 |
| `skills/init-project-agents/SKILL.md` | 프로젝트 루트에 최소 `AGENTS.md` 생성/갱신 |
| `prompts/permission-bootstrap.prompt.md` | 권한 부트스트랩 호출용 저장 프롬프트 |

## 신규 프로젝트 시작

1. 프로젝트에 [claude-workflow](https://github.com/sapsalian/claude-workflow) 적용 (`.claude/plans/`, `CLAUDE.md` 생성)
2. `init-project-agents` — 프로젝트 루트에 `AGENTS.md` 생성 (Codex 가드레일)
3. `permission-bootstrap` — 비파괴 명령 위주로 prefix_rule 자동 승인 설정
4. `dev-full <요구사항>` — Q&A → 전체 설계 → Phase별 세부 설계 → 구현 전 과정 진행

## 업데이트

```bash
cd ~/.codex && git pull
```

## 운영 원칙

- 전역 workflow 로직: `~/.codex/skills/`
- 프로젝트 맥락: 각 프로젝트의 `CLAUDE.md` (로컬 전용)
- 프로젝트 가드레일: 각 프로젝트의 `AGENTS.md`
- plan 파일: 각 프로젝트의 `.claude/plans/` (Claude Code ↔ Codex 공유 상태)
