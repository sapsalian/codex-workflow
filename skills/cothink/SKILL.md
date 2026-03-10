---
name: cothink
description: Run Q&A rounds then execute request. Useful for complex one-off tasks, analysis, or decisions that don't need a full plan.
---

# Cothink

## Request
$ARGUMENTS (or described in the conversation)

## Step 1: Gather context

Read `CLAUDE.md` first.

Explore files and code relevant to the request:
- Read related files
- Understand current state
- Identify scope of impact

## Step 2: Q&A rounds (minimum 3)

At the start of each round, output:

```
## 고려 사항 정리 (라운드 N)

### 검토한 사항
- [사항]: [판단]

### 자동 결정한 사항 (명백한 기술적 사실만)
- [사항]: [결정] — 이유: [근거]

### 사용자에게 질문할 사항
- [질문들]
```

Rules:
- 3 rounds minimum. Earlier answers may introduce new concerns — always check.
- Continue past round 3 if open items remain.
- Ask on all real tradeoffs. Auto-decide only obvious technical facts.

## Step 3: Decision summary

Before executing, output:

```
## Confirmed Decisions

- [Decision 1]
- [Decision 2]
- ...
```

## Step 4: Execute

Carry out the request based on confirmed decisions.
Additional Q&A is allowed if unexpected situations arise during execution.
