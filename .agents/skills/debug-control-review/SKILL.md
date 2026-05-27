---
name: debug-control-review
description: Classify visible prototype/dev/debug controls and block accidental exposure in user-facing UI.
---

# debug-control-review

## Trigger

Use when UI includes toggles, fixture selectors, state switches, model controls, debug panels, route selectors, or any unexplained control in a toolbar/settings area.

## Process

1. Read `docs/DEBUG_CONTROL_GATE.md`.
2. List visible controls that could be dev/prototype-only.
3. Classify each as user-facing, dev-only, prototype-only, or unknown.
4. If unknown, ask for clarification or mark BLOCKED.
5. Require removal/segregation/labeling of non-user controls.

## Output

Use `.agents/templates/debug-control-report.md`.
