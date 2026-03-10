---
name: dev-design
description: Q&A + plan creation only. Design phase only — implementation can be done anytime via dev-impl (Claude or Codex).
---

# Dev-Design

## Required project context
Read `CLAUDE.md` in the current project root before starting.

## Step 1: Existing plan check
Inspect `.claude/plans/*.md`.

**If plan files exist:**
→ Show the list and ask whether to resume or start a new plan.
→ If resuming, find the first Phase with an empty `세부 설계` section → jump to Step 4.

**If no plan file exists:**
→ Continue to Step 2.

## Step 2: Whole-plan Q&A

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

Write the plan file at `.claude/plans/YYYY-MM-DD-<slug>.md`.

Template:

```md
# <task-title>
<!-- Created: YYYY-MM-DD | Status: in-progress -->

## Context
<why this work is needed and what success means>

## Phases

### Phase 1: <title> [⏳ 대기]
**Goal**: <한 줄 목표>

#### 세부 설계
<!-- dev-design Phase Q&A 완료 후 채워짐 -->

#### Sub-steps
<!-- dev-design Phase Q&A 완료 후 채워짐 -->
- [ ] Step 1: ...
```

After writing the plan, ask: **"Shall we proceed with Phase 1 detailed design Q&A? (yes/no)"**
- yes → proceed to Step 4
- no → stop. Resume next time with `/dev-design` from Step 4.

## Step 4: Phase detailed design (design only, no implementation)

For each Phase N:

1. Run at least 3 Q&A rounds using the phase checklist:
   - must-have behavior, excluded behavior, success criteria
   - UI components, UI states, user interactions
   - data flow, implementation order, edge cases

2. Fill in the `세부 설계` and `Sub-steps` sections in the plan file.

3. After filling, ask:
   - **If not the last phase**: **"Shall we start Phase N+1 detailed design? (yes/no)"**
     - yes → continue to next phase design
     - no → stop. Resume next time from next empty `세부 설계` phase.
   - **If the last phase**: **"All phase designs are complete. Would you like to start implementation with dev-impl now, or later? (now/later)"**
     - Both answers → stop. Implementation runs separately via `/dev-impl`.

## Completion

> "Design is complete. You can start implementation using /dev-impl (Claude Code or Codex) whenever you're ready."

No forced handoff — implementation timing is up to you.
