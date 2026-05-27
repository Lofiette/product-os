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


## Taste and Culture Gate

For design-facing tasks with an active taste profile, report:
- taste profile used;
- good/bad examples applied;
- what feels right;
- what feels off with evidence;
- craft defects;
- top fixes without scope expansion.

If taste review is required and not run, final UI verdict cannot be PASS.

BLOCKED if:
- primary action is unclear;
- visual hierarchy contradicts product priority;
- UI violates task taste profile in a user-impacting way;
- implemented UI is “similar” to DS but not using actual DS components where required;
- critical state is missing.


## Taste Review Gate

Use when task affects product/UI/design/prototype/content quality and a Taste Profile exists or can be inferred.

Report:
- taste profile used;
- good examples matched;
- bad examples avoided or violated;
- visible craft issues;
- DS/taste deviations;
- top fixes without scope expansion.

Verdict: PASS / PASS WITH WARNINGS / BLOCKED.

BLOCKED if avoidable UX confusion, DS drift, visible craft failure, or contradiction with explicit bad examples remains unresolved.
