---
name: e2e-visual-state-capture
description: Define and optionally run screenshot/state capture across important UI states and breakpoints for visual verification.
---


# e2e-visual-state-capture

## Purpose

Create a practical screenshot/state capture plan for visual QA.

## Procedure

1. Identify routes/components/stories and states to capture.
2. Identify breakpoints.
3. Prefer existing Storybook/Playwright/Cypress setup.
4. If no tooling exists, provide manual capture steps.
5. Produce expected screenshot list and verification checklist.

## Output schema

```markdown
## Visual State Capture Plan

### Tooling detected
### Routes/stories/states
| Target | State | Viewport | Setup data | Expected evidence |
### Commands or manual steps
### Not run / limitations
```

## BLOCKED conditions

- Visual QA is required but no capture/manual plan is provided.

## Stop conditions

- Required evidence is missing and the next step would require guessing.
- The skill would change approved scope.
- A risk gate requires user approval.
- Another role owns the decision and has not been consulted.

