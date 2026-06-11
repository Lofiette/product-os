---
name: implementation-review
description: Review implemented changes against approved scope, artifacts, tests, UI/DS gates, risks, and handoff requirements before completion.
---


# implementation-review

## Purpose

Prevent “code compiles” from being treated as done when product/design/risk gates are unmet.

## Procedure

1. Compare diff against active task ticket approved scope.
2. Check relevant artifacts exist: Screen Spec, Module Package, Production Plan, etc.
3. Check tests/commands run or limitations stated.
4. For UI tasks, require DS compliance, UI heuristic audit, and visual QA status.
5. For production tasks, require production readiness status.
6. Identify scope creep and unresolved blockers.

## Output schema

```markdown
## Implementation Review

### Verdict
PASS / PASS WITH WARNINGS / BLOCKED

### Scope match
### Files changed
### Required artifacts present
### Tests/checks run
### UI/design-system gates
### Risk/production gates
### Blockers
### Approved exceptions
### Merge/completion recommendation
```

## BLOCKED conditions

- Approved scope is violated.
- Required UI/DS/risk gate is missing or failed.
- Tests/checks claimed without evidence.

## Stop conditions

- Required evidence is missing and the next step would require guessing.
- The skill would change approved scope.
- A risk gate requires user approval.
- Another role owns the decision and has not been consulted.

