---
name: opportunity-event-triage
description: Classify new ideas/signals as OE-0..OE-4 and decide ignore/log/improve/re-plan/block.
---

# opportunity-event-triage

## Purpose

Classify new ideas/signals as OE-0..OE-4 and decide ignore/log/improve/re-plan/block.

## When to use

Use only when this workflow can improve decision quality, risk detection, implementation, verification, or handoff.

## Inputs

- CURRENT.md and active task ticket current scope.
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
## Skill output: opportunity-event-triage

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


## Anticipation integration

If an opportunity event reveals a likely future expectation, also classify it through the Anticipation Branch A-0..A-4 levels. Scope-changing ideas require user approval.
