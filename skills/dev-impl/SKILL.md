---
name: dev-impl
description: Pick up plan → prescription review → implement phase by phase.
---

# Dev-Impl

## Required project context
Read `CLAUDE.md` in the current project root before starting.

## Step 1: Existing plan check
Inspect `.claude/plans/*.md`.

**If plan files exist:**
→ Show the list and ask which plan to pick up (or start a new one).
→ Once a plan is selected, read it in full (Context + all Phase sections including 세부 설계).
→ Skip Step 2 (whole Q&A). Proceed to **Prescription Review** below.

**If no plan file exists:**
→ Continue to Step 2.

---

## Prescription Review
*Only when a plan was picked up in Step 1.*

Read the entire plan as an implementer. Actively review it and report to the user:

```
## 처방 검토 결과

### 구현 관점 우려 사항
- [설계 결정이 구현 시 문제가 될 수 있는 부분, 실현 가능성, 누락된 엣지 케이스 등]

### 보완 제안 (선택적)
- [구현하면 더 나은 부분이 있다면]

### 구현 전 확인 필요 사항
- [결정되지 않아 구현을 시작하기 전 사용자 확인이 필요한 항목]
```

- No concerns → "검토 완료, 구현을 시작합니다." and proceed.
- Concerns found → present and resolve before proceeding.
- Q&A on the plan is allowed at this stage.

---

## Step 2: Whole-plan Q&A
*Only when no plan file exists.*

Run at least 3 Q&A rounds for whole-plan design.

Whole-plan checklist:
- requirement clarification: problem, goal, included scope, excluded scope
- user scenario: who uses it and in what flow
- expected outcome: what counts as done
- architecture/technology, UI/UX, API/interface, data model
- error handling, performance/constraints, test strategy

At the start of each round, output:

```md
## 고려 사항 정리 (라운드 N)

### 검토한 사항
- [사항]: [판단]

### 자동 결정한 사항 (명백한 기술적 사실만)
- [사항]: [결정] — 이유: [근거]

### 사용자에게 질문할 사항
- [질문들]
```

Rules:
- 3 rounds minimum. Continue if derived concerns remain.
- Ask on all real tradeoffs. Auto-decide only obvious technical facts.

## Step 3: Create project plan
*Only when no plan file exists (after Step 2).*

Write the plan file at `.claude/plans/YYYY-MM-DD-<slug>.md`.

## Step 4: Phase-by-phase execution

### 4-1. Phase design Q&A (conditional)

**Check the `세부 설계` section of the current phase:**

- **세부 설계 섹션이 채워진 경우** (dev-design에서 Q&A 완료):
  → Skip Q&A. Read the 세부 설계 section and proceed directly to implementation (4-2).

- **세부 설계 섹션이 비어있는 경우**:
  → Inform the user:
  > "이 Phase는 세부 설계가 필요합니다.
  >  Claude Code에서 먼저 Q&A를 진행하거나,
  >  여기서 Q&A를 진행하시겠습니까?"
  → If user wants Q&A here, run at least 3 Q&A rounds using the phase checklist below.
  → Fill in the `세부 설계` section in the plan file before implementing.

Phase checklist (when Q&A is needed):
- phase requirement clarification: must-have behavior, excluded behavior
- success criteria, UI components, UI states, user interactions
- data flow, implementation order, edge cases

Update the phase status to `[🔄 진행 중]`.
If sub-steps exist, use `[🔄 진행 중] (0/N)`.

### 4-2. Phase implementation
Use TDD. Q&A during implementation is allowed.

If sub-steps exist:
1. Write tests first.
2. Implement.
3. Run tests before moving on.
4. Make an intermediate commit.
5. Update the sub-step counter in the plan.

If no sub-steps:
1. Write tests first.
2. Implement.
3. Run tests and build.
4. Make an intermediate commit.

### 4-3. Phase completion
1. Run build and required tests.
2. Mark the phase `[✅ 완료]`.
3. Make the required phase completion commit.

## Step 5: Final completion
- Confirm all phases are `[✅ 완료]`
- Run final build and test checks
- Update the plan header status to `complete`

## Plan tracking rules
- Keep plan files in `.claude/plans/`
- Status markers: `[⏳ 대기]`, `[🔄 진행 중]`, `[✅ 완료]`
- Keep `CLAUDE.md` updated when the work changes project context
