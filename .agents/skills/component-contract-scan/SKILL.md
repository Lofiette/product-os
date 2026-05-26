---
name: component-contract-scan
description: Inspect component imports, duplicate local components, raw JSX primitives, and DS manifest compliance using code heuristics.
---


# component-contract-scan

## Purpose

Run a practical code scan for DS component contract violations.

## Procedure

1. Confirm DS manifest exists or run design-recon/design-system-manifest first.
2. Run `node scripts/check-component-imports.mjs <root>` if available.
3. Review findings for false positives before declaring blockers.
4. Map each finding to a component, file, and required fix.

## Output schema

```markdown
## Component Contract Scan

### Command run
### Findings
| Severity | File | Line | Finding | Fix |
### False positives / limitations
### Verdict
```

## BLOCKED conditions

- DS component exists but duplicate local component is introduced.
- UI imports known DS component names from non-DS sources without approved deviation.

## Stop conditions

- Required evidence is missing and the next step would require guessing.
- The skill would change approved scope.
- A risk gate requires user approval.
- Another role owns the decision and has not been consulted.

