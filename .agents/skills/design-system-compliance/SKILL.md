---
name: design-system-compliance
description: Check that UI decisions and implementation use DS components, tokens, patterns, and approved deviations instead of custom lookalikes.
---


# design-system-compliance

## Purpose

Prevent “looks similar” UI from replacing actual design-system components and patterns.

## Procedure

1. Load Design Recon Brief and DS Manifest if present.
2. Compare planned or implemented UI against component registry.
3. Build a component usage map.
4. Check raw colors, arbitrary spacing, inline styles, custom duplicated components, and local variants.
5. Record deviations and approvals.
6. If scripts are available, run:
   - `node scripts/find-raw-ui-values.mjs <root>`
   - `node scripts/check-component-imports.mjs <root>`
7. Return gate verdict.

## Output schema

```markdown
## Design-System Compliance Report

### Verdict
PASS / PASS WITH WARNINGS / BLOCKED

### Components reused
| Need | Component | Source | Evidence |

### Token usage

### Raw UI findings

### Custom UI / duplicate component findings

### Approved deviations

### Required fixes
```

## BLOCKED conditions

- Existing DS component is bypassed by custom lookalike UI.
- Raw colors/spacing are introduced in governed/documented DS mode.
- Deviation lacks explicit approval.

## Stop conditions

- Required evidence is missing and the next step would require guessing.
- The skill would change approved scope.
- A risk gate requires user approval.
- Another role owns the decision and has not been consulted.



## Taste guardrail

Taste never overrides design-system compliance. If a local visual decision feels better but conflicts with documented/governed DS, record it as a deviation and ask approval.
