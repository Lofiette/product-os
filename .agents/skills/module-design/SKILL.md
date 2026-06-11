---
name: module-design
description: Design a full product module for later implementation or rebuild: IA, flows, screen inventory, component matrix, state matrix, content, accessibility, and developer handoff.
---


# module-design

## Purpose

Design an entire product module, not isolated screens.

## Procedure

1. Define module purpose, users/jobs, scope, and non-goals.
2. Define object model and information architecture.
3. Map main flows and entry/exit points.
4. Create screen inventory with purpose, primary action, and states.
5. Create component matrix against DS or prototype UI kit.
6. Create cross-screen state matrix.
7. Create content matrix.
8. Define accessibility and responsive rules.
9. Define analytics/instrumentation notes if relevant.
10. Create Developer Rebuild Brief.
11. Run `design-handoff-qa` before final handoff.

## Output schema

```markdown
## Module Design Package

### Module purpose
### Users and jobs
### Scope and non-goals
### Object model
### Navigation / IA model
### Main flows
### Screen inventory
| Screen | Purpose | Primary action | States | DS patterns |
### Cross-screen state matrix
### Component matrix
### Content matrix
### Accessibility requirements
### Responsive behavior
### Analytics/instrumentation notes
### Developer Rebuild Brief
### Open questions and risks
### Acceptance criteria
```

## BLOCKED conditions

- Module design has screens but no navigation/IA model.
- Developer is expected to rebuild but there is no component matrix or state matrix.

## Stop conditions

- Required evidence is missing and the next step would require guessing.
- The skill would change approved scope.
- A risk gate requires user approval.
- Another role owns the decision and has not been consulted.



## Anticipation and taste integration

For module design, run `anticipation-radar` once before final handoff to detect likely developer, user, stakeholder, and QA expectations not yet captured. Do not add scope without approval.

If the module has user-facing UI, include taste profile and good/bad examples in the Module Design Package or reference the active task ticket.
