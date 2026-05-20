# PROMPT_RECIPES.md

## Start a new task

```text
Use Intake Mode. Read the project instructions, interview me using the adaptive question tree, update TASK.md and CHRONICLE.md, recommend the optimal subagent lineup, run a consistency audit, and ask for approval before implementation.
```

## Continue after context loss

```text
Read TASK.md and CHRONICLE.md. Summarize current task, phase, approved scope, decisions, selected roles, verification status, risks, and next recommended action. Do not implement until I confirm.
```

## Plan with subagents

```text
Use Team Architect to select the smallest sufficient specialist team. Spawn only the selected subagents, wait for all findings, consolidate the plan, run Consistency Auditor, and ask for approval before implementation.
```

## Approve implementation

```text
I approve the plan in TASK.md. Implement only the approved scope. Keep the diff minimal. Follow QUALITY_GATES.md. Update tests/checks as planned. Update CHRONICLE.md before final summary.
```

## Review a diff

```text
Use implementation-review. Compare the diff against TASK.md and approved plan. Involve QA Engineer and any triggered risk roles. Return blocking issues, non-blocking issues, missing tests, risk notes, and merge recommendation.
```

## Run self-audit

```text
Use self-audit. Check the current plan, role lineup, TASK.md, CHRONICLE.md, gates, and referenced files for contradictions, missing ownership, missing risk roles, vague scope, and unverified claims.
```
