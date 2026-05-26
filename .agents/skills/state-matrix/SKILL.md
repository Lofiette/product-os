---
name: state-matrix
description: Define UI states and behaviors across empty, loading, success, error, disabled, permission, overflow, responsive, and edge-case conditions.
---


# state-matrix

## Purpose

Make UI behavior testable across real states instead of designing only the happy path.

## Procedure

1. Identify objects/entities and their lifecycle states.
2. Identify async/data states: loading, partial, stale, empty, error, success.
3. Identify interaction states: default, hover/focus, active, disabled, validation, destructive confirmation.
4. Identify permission and role states.
5. Identify overflow and responsive states.
6. Define copy, components, and expected behavior per state.
7. Mark blockers and states intentionally out of scope.

## Output schema

```markdown
## State Matrix

| State | User need | UI behavior | Copy | Component/pattern | Edge cases | Verification |
|---|---|---|---|---|---|---|
```

## BLOCKED conditions

- Form/screen has error or empty cases but no defined behavior.
- Disabled state exists without explanation or alternative path.

## Stop conditions

- Required evidence is missing and the next step would require guessing.
- The skill would change approved scope.
- A risk gate requires user approval.
- Another role owns the decision and has not been consulted.

