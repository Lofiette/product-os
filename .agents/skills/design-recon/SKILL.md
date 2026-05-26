---
name: design-recon
description: Discover design-system level, component registry, tokens, style conventions, UI patterns, Figma/design docs, and implementation constraints.
---

# design-recon

## Purpose

Discover design-system level, component registry, tokens, style conventions, UI patterns, Figma/design docs, and implementation constraints.

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
## Skill output: design-recon

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

## Required Design Recon Brief sections
- DS mode: none / emerging / component_library / documented_ds / governed_ds
- DS source of truth
- Component registry
- Token system
- Relevant patterns
- Anti-patterns
- DS docs loaded
- Required compliance gate
- Recommended next roles/skills
