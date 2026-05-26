---
name: ds-code-contract-enforcement
description: Enforce DS code contracts with manifest, import checks, raw value scans, component duplication scans, and explicit deviation records.
---


# ds-code-contract-enforcement

## Purpose

Turn DS compliance into an enforceable implementation gate.

## Procedure

1. Ensure DS Manifest exists or run design-system-manifest.
2. Run import/component scan when scripts exist.
3. Run raw UI value scan when scripts exist.
4. Check new components against registry and deviation log.
5. Require approved deviations for custom UI.
6. Return enforcement verdict.

## Output schema

```markdown
## DS Code Contract Enforcement

### Commands run
### Manifest used
### Import/component findings
### Raw UI findings
### New components/variants
### Approved deviations
### Verdict
PASS / PASS WITH WARNINGS / BLOCKED
```

## BLOCKED conditions

- Custom duplicate component found without approval.
- Raw UI value introduced in documented/governed DS mode without approval.

## Stop conditions

- Required evidence is missing and the next step would require guessing.
- The skill would change approved scope.
- A risk gate requires user approval.
- Another role owns the decision and has not been consulted.

