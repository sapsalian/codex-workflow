# Codex Home Repo

`~/.codex`를 Git으로 관리하는 저장소. 전역 Codex skill과 prompt를 담당하며, 프로젝트 로컬 파일은 각 프로젝트 루트에서 관리합니다.

## Claude Code와의 협업

Codex와 Claude Code는 **피어(peer) 관계**입니다.

| 역할 | 담당 |
|------|------|
| 의사 (처방) | Claude Code — 전체 설계 Q&A, 각 Phase 세부 설계 Q&A, plan 파일 작성 |
| 간호사 (처방 검토 + 시술) | Codex — plan 픽업, 처방 검토, 순수 구현 |

### 권장 라우팅 전략

**Claude Code에서 할 일:**
1. 전체 설계 Q&A → plan 파일 생성
2. 각 Phase 세부 설계 Q&A → plan 파일의 `세부 설계` 섹션 채우기
3. 세부 설계 완료 시 Codex로 전환 안내

**Codex에서 할 일:**
1. plan 파일 픽업
2. 처방 검토 — 구현 관점에서 설계의 문제점, 보완 제안, 미결 사항 보고
3. 순수 구현 (구현 중 불명확한 사항은 Q&A 허용)

**전환 트리거:**
- Claude Code → Codex: 구현할 Phase의 `세부 설계` 섹션이 채워진 시점
- Codex → Claude Code 복귀: 복잡한 디버깅, 구조 변경, 설계 재검토가 필요할 때
- 컨텍스트 소진 시: plan 파일을 그대로 넘겨 Codex가 이어받을 수 있음

### 핸드오프 프로토콜

**공유 상태**: `.claude/plans/*.md` plan 파일

**구현 준비 신호**: plan 파일 각 Phase의 `#### 세부 설계` 섹션이 채워진 상태

```markdown
### Phase N: <title> [⏳ 대기]
**Goal**: <한 줄 목표>

#### 세부 설계
<!-- 비어있으면 = Claude Code 세부 설계 Q&A 필요 -->
<!-- 채워져 있으면 = 구현 준비 완료, Codex가 바로 구현 시작 -->

#### Sub-steps
- [ ] Step 1: ...
```

### CLAUDE.md 상태

- git으로 추적하지 않음 (`.gitignore`에 포함)
- 로컬 전용, 각 프로젝트 루트에 존재
- Claude Code와 Codex 양쪽 모두 이 파일을 읽음

## 선행 조건

각 프로젝트에 [claude-workflow](https://github.com/sapsalian/claude-workflow)가 적용되어 있어야 합니다 (`.claude/plans/`, `CLAUDE.md` 제공).

## 제공 항목

- `skills/develop/SKILL.md` — plan 픽업 → 처방 검토 → phase별 구현
- `skills/permission-bootstrap/SKILL.md` — 안전한 비파괴 명령 위주의 prefix_rule 승인 부트스트랩
- `skills/init-project-agents/SKILL.md` — 프로젝트 루트에 최소 `AGENTS.md` 생성/갱신
- `prompts/permission-bootstrap.prompt.md` — 권한 부트스트랩 호출용 저장 프롬프트

## 신규 프로젝트 시작

claude-workflow 적용 → `init-project-agents` → `permission-bootstrap` → `/develop <요구사항>`

## 업데이트

```bash
cd ~/.codex && git pull
```

## 운영 원칙

- 전역 workflow 로직: `~/.codex/skills/`
- 프로젝트 맥락: 각 프로젝트의 `CLAUDE.md` (로컬 전용)
- 프로젝트 가드레일: 각 프로젝트의 `AGENTS.md`
- plan 파일: 각 프로젝트의 `.claude/plans/` (Claude Code ↔ Codex 공유 상태)
