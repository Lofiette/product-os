---
name: design-handoff-qa
description: Check design-only handoff packages so a developer can rebuild without guessing structure, components, states, copy, or constraints.
---


# design-handoff-qa

## Purpose

Validate that a human developer can rebuild the designed module/screen without guessing core decisions.

## Procedure

1. Confirm this is design-only or developer-rebuild mode.
2. Check Module Design Package or Screen Design Spec.
3. Verify component matrix, state matrix, content matrix, accessibility notes, responsive rules.
4. Verify developer rebuild brief includes files/patterns to inspect and non-goals.
5. Mark missing items as blockers.

## Output schema

```markdown
## Design Handoff QA

### Verdict
PASS / PASS WITH WARNINGS / BLOCKED

### Developer can rebuild without guessing?
yes/no

### Missing or ambiguous items
| Area | Issue | Required fix |

### Approved limitations
### Next implementation recommendations
```

## BLOCKED conditions

- Developer must infer core layout, components, states, or copy.
- DS component matrix is missing while DS rules apply.

## Stop conditions

- Required evidence is missing and the next step would require guessing.
- The skill would change approved scope.
- A risk gate requires user approval.
- Another role owns the decision and has not been consulted.

