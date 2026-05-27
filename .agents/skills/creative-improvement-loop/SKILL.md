---
name: creative-improvement-loop
description: Controlled ideation using focal objects, synectics, SCAMPER, TRIZ-lite, pre-mortem, and OST without confusing hypotheses with evidence.
---

# creative-improvement-loop

## Purpose

Controlled ideation using focal objects, synectics, SCAMPER, TRIZ-lite, pre-mortem, and OST without confusing hypotheses with evidence.

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
## Skill output: creative-improvement-loop

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


## Beta 2 anticipation integration

When creative improvement generates a suggestion that changes acceptance criteria, scope, roles, architecture, DS contract, or verification, route it through `anticipation-radar` or `proactive-proposal-review` before adding it to the plan.
