---
name: develop
description: Use this skill when the user wants to run the /develop workflow for implementation work. Read the project's CLAUDE.md first, then drive Q&A, planning, phased execution, and plan tracking.
---

# Develop

## Required project context
Before planning or implementation, read `CLAUDE.md` in the current project root.

Use `CLAUDE.md` for:
- project structure
- build, test, and lint commands
- architecture notes
- domain-specific rules
- recent project changes

If `CLAUDE.md` is missing, warn the user and continue with best-effort local discovery.

## Workflow goal
Use `/develop` for structured implementation work:
- clarify the requirement
- create or resume a plan in `.claude/plans/`
- execute work phase by phase
- keep `CLAUDE.md` updated when project context changes

## Step 1: Existing plan check
Inspect `.claude/plans/*.md`.

Rules:
- If plan files exist, show them and ask whether to resume or start a new plan.
- If a phase is `[🔄 진행 중]` or `[⏳ 대기]`, resume from that phase unless the user chooses otherwise.
- If no plan file exists, continue to Step 2.

## Step 2: Whole-plan Q&A
Run at least 3 Q&A rounds for whole-plan design.

Purpose:
- technical review
- requirement clarification
- scope alignment
- success criteria agreement

Whole-plan checklist:
- requirement clarification: problem, goal, included scope, excluded scope
- user scenario: who uses it and in what flow
- expected outcome: what counts as done
- architecture/technology
- UI/UX
- API/interface
- data model
- error handling
- performance/constraints
- test strategy

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
- 3 rounds minimum even if questions appear resolved early.
- Continue past round 3 if derived concerns remain.
- Ask whenever requirement meaning, scope, expected behavior, or success criteria are unclear.
- Ask on all real tradeoffs.
- Auto-decide only obvious technical facts.

## Step 3: Create or update project plan
Write the plan file at:
- `.claude/plans/YYYY-MM-DD-<slug>.md`

Use phase-based planning where each phase is independently meaningful.
Split complex phases into sub-steps.

Template:

```md
# <task-title>
<!-- Created: YYYY-MM-DD | Status: in-progress -->

## Context
<why this work is needed and what success means>

## Phases

### Phase 1: <title> [⏳ 대기]
<goal>
- Step 1: ...
- Step 2: ...
```

## Step 4: Phase-by-phase execution
For each phase:

### 4-1. Phase design Q&A
Run at least 3 Q&A rounds.

Purpose:
- clarify expected phase behavior
- confirm phase boundaries
- define success criteria
- resolve edge cases before implementation

Phase checklist:
- phase requirement clarification: must-have behavior, excluded behavior
- success criteria
- UI components
- UI states
- user interactions
- data flow
- implementation order
- edge cases

Update the phase status to `[🔄 진행 중]`.
If sub-steps exist, use `[🔄 진행 중] (0/N)`.

### 4-2. Phase implementation
Use TDD.

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
- Keep `CLAUDE.md` updated when the work changes project structure, commands, architecture notes, or constraints
