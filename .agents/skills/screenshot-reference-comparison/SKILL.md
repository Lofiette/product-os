---
name: screenshot-reference-comparison
description: Compare actual rendered UI against reference screenshot, screen spec, DS/taste contract, and visual acceptance criteria.
---

# screenshot-reference-comparison

## Trigger

Use when UI was rendered and any reference, taste profile, DS contract, or screen spec exists.

## Process

1. Read `docs/SCREENSHOT_VISUAL_GATE.md` and `docs/VISUAL_ACCEPTANCE_CRITERIA.md`.
2. Collect actual screenshot/render evidence.
3. Collect reference screenshot/spec evidence.
4. Compare layout, hierarchy, density, controls, cards/lists/tables, content tone, DS fidelity, and states.
5. Report missing visual evidence explicitly.
6. Return PASS / PASS WITH WARNINGS / BLOCKED.

## Rule

No final UI PASS without screenshot/reference comparison when reference exists and render is possible.

## Output

Use `.agents/templates/screenshot-comparison-report.md`.
