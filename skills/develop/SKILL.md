---
name: develop
description: Full cycle — Q&A + planning + phase-by-phase implementation. No handoff needed. (dev-full)
---

# Develop (dev-full)

## Required project context
Before planning or implementation, read `CLAUDE.md` in the current project root.

If `CLAUDE.md` is missing, warn the user and continue with best-effort local discovery.

## Step 1: Existing plan check
Inspect `.claude/plans/*.md`.

**If plan files exist:**
→ Show the list and ask which plan to pick up (or start a new one).
→ Once a plan is selected, read it in full (Context + all Phase sections).
→ Proceed to **Prescription Review** below.

**If no plan file exists:**
→ Continue to Step 2.

---

## Prescription Review
*Only when a plan was picked up in Step 1.*

Read the entire plan as an implementer. Actively review it and report:

```
## Prescription Review

### Implementation Concerns
- [Design decisions that may cause problems, feasibility issues, missing edge cases]

### Optional Improvements
- [Areas that could be enhanced]

### Needs Confirmation Before Starting
- [Undecided items that require user input]
```

- No concerns → "Review complete. Starting implementation." and proceed.
- Concerns found → present and resolve before proceeding.

---

## Step 2: Whole-plan Q&A
*Only when no plan file exists.*

Run at least 3 Q&A rounds for whole-plan design.

Whole-plan checklist:
- requirement clarification: problem, goal, included scope, excluded scope
- user scenario: who uses it and in what flow
- expected outcome: what counts as done
- architecture/technology
- UI/UX, API/interface, data model
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
<!-- Phase Q&A 완료 후 채워짐 -->

#### Sub-steps
<!-- Phase Q&A 완료 후 채워짐 -->
- [ ] Step 1: ...
```

## Step 4: Phase-by-phase execution

For each phase:

### 4-1. Phase design Q&A (conditional)

**Check the `세부 설계` section:**

- **Filled** → Skip Q&A. Read 세부 설계 and proceed to implementation.
- **Empty** → Run at least 3 Q&A rounds using the phase checklist:
  - must-have behavior, success criteria, UI components/states, user interactions, data flow, edge cases
  - Fill in the `세부 설계` section before implementing.

Update phase status to `[🔄 진행 중]`.

### 4-2. Phase implementation
Use TDD. Q&A during implementation is allowed.

If sub-steps exist:
1. Write tests first.
2. Implement.
3. Run tests before moving on.
4. Make an intermediate commit.
5. Update the sub-step counter.

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
- Status markers: `[⏳ 대기]`, `[🔄 진행 중]`, `[✅ 완료]`
- Keep `CLAUDE.md` updated when the work changes project context
