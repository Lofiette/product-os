---
name: screen-redesign
description: Create or redesign a screen using user goals, information hierarchy, component tree, state matrix, content, accessibility, and implementation constraints.
---


# screen-redesign

## Purpose

Produce a screen-level design decision that can be implemented or reviewed without guessing.

## Procedure

1. State the user goal and product goal.
2. Identify the current problem or desired outcome.
3. Define primary and secondary actions.
4. Define information hierarchy and screen anatomy.
5. Create a component tree using existing DS components or prototype UI kit components.
6. Create or reference a state matrix.
7. Define content requirements and UX writing handoff.
8. Define accessibility and responsive requirements.
9. List alternatives considered and why the selected direction wins.
10. Produce implementation handoff notes.

## Output schema

```markdown
## Screen Design Spec

### User goal
### Product goal
### Current problem / opportunity
### Constraints
### Information hierarchy
### Screen anatomy
### Primary and secondary actions
### Component tree
### State matrix reference
### Content requirements
### Accessibility requirements
### Responsive behavior
### Alternatives considered
### Selected solution and rationale
### Implementation handoff
### Design QA checklist
```

## BLOCKED conditions

- Screen has user-facing states but no state matrix.
- Component tree ignores an existing DS.
- Primary action is unclear.

## Stop conditions

- Required evidence is missing and the next step would require guessing.
- The skill would change approved scope.
- A risk gate requires user approval.
- Another role owns the decision and has not been consulted.



## Beta 2 taste/culture integration

Before selecting a design direction, check whether `taste-calibration` is needed. It is required when visual/product feel is ambiguous, no DS exists, or the user provided taste adjectives/references.

Screen decisions must reference:
- taste profile, if active;
- good/bad examples, if provided;
- team culture concerns when user stewardship/craft/system fidelity are affected.

Before finalizing, run or request `taste-review` when taste profile is active or quality is ambiguous.
