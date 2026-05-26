# UI_QUALITY_GATES.md

## Design System Compliance Gate

For UI tasks, report:
- components reused;
- tokens reused;
- custom UI introduced;
- DS deviations;
- approved exceptions;
- raw colors/spacing/styles found;
- state coverage;
- responsive coverage.

If DS component exists, custom UI is BLOCKED unless approved.

## Visual QA Gate

If possible:
- render UI;
- inspect key states;
- capture screenshots;
- compare against Screen Design Spec and DS manifest;
- fix blockers.

If not possible, state that visual QA was not completed.

## UI verdict

Use: PASS / PASS WITH WARNINGS / BLOCKED.
