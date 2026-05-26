---
name: incident-review
description: Investigate incidents with timeline, impact, root cause, contributing factors, remediation, prevention.
---

# incident-review

## Purpose

Investigate incidents with timeline, impact, root cause, contributing factors, remediation, prevention.

## When to use

Use only when this workflow can improve decision quality, risk detection, implementation, verification, or handoff.

## Inputs

- TASK.md current scope.
- Relevant role playbook or role card.
- Relevant repo/design/research evidence.
- Approved orchestration mode.

## Process

1. Confirm this skill is needed for the current operation.
2. Load only relevant files/docs.
3. Separate evidence, assumptions, and hypotheses.
4. Produce the required compact artifact.
5. Report blockers and handoffs.

## Output schema

```markdown
## Skill output: incident-review

### Context

### Steps performed

### Findings

### Evidence / assumptions

### Blockers

### Handoff
```

## Stop conditions

- Required evidence is missing.
- Skill use would change approved scope.
- A risk gate requires user approval.
- Another role owns the decision.
