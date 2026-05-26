---
name: visual-qa-loop
description: Render or inspect implemented UI states, capture screenshots when possible, compare against spec/DS, and fix visual/UI blockers.
---


# visual-qa-loop

## Purpose

Inspect the actual rendered UI, not only the code.

## Procedure

1. Identify route/page/component states to inspect.
2. Start the app or Storybook if possible.
3. Capture screenshots or use available visual output.
4. Inspect at least relevant breakpoints/states.
5. Compare against Screen/Module Design Spec and DS compliance report.
6. Run UI obvious errors checklist.
7. Produce blockers and required fixes.
8. If rendering is impossible, state exactly why visual QA was not completed.

## Output schema

```markdown
## Visual QA Report

### Render environment
### Screens/states inspected
### Screenshots captured
yes/no, path/list if available
### Visual hierarchy issues
### Layout/spacing/density issues
### Responsive issues
### State coverage issues
### DS fidelity issues
### Blockers fixed
### Remaining risks
### Verdict
PASS / PASS WITH WARNINGS / BLOCKED / NOT RUN
```

## BLOCKED conditions

- Visual QA reveals unclear primary action, missing critical state, broken responsive layout, or DS violation.
- Visual QA is required by scope but cannot be run and no limitation is reported.

## Stop conditions

- Required evidence is missing and the next step would require guessing.
- The skill would change approved scope.
- A risk gate requires user approval.
- Another role owns the decision and has not been consulted.

