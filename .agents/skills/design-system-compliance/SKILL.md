---
name: design-system-compliance
description: Check UI changes against DS manifest, components, tokens, variants, anti-patterns, and approved deviations.
---

# design-system-compliance

## Purpose

Check UI changes against DS manifest, components, tokens, variants, anti-patterns, and approved deviations.

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
## Skill output: design-system-compliance

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

## Blocking checks
- custom duplicate of existing DS component
- raw colors/spacing/radius when tokens exist
- new variant without approval
- missing state/pattern coverage
- DS folder docs ignored
