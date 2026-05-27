# SCREENSHOT_VISUAL_GATE.md

Rendered UI is the source of truth for visual quality.

## Rule

For UI implementation/review, final UI verdict cannot be `PASS` without rendered visual evidence when rendering is technically possible.

If visual evidence is unavailable:
- report `Visual QA: INCOMPLETE`;
- state why;
- maximum verdict is `PASS WITH WARNINGS` unless the user explicitly accepts the limitation.

If the user provided a reference image:
- screenshot/reference comparison is mandatory;
- final UI verdict cannot be `PASS` without comparison.

## Visual evidence can be

- screenshot captured by browser/Playwright;
- screenshot uploaded by user;
- rendered DOM plus visual inspection in Codex UI;
- visual regression artifact.

## Required checks

- screen layout anatomy;
- primary action prominence;
- card/list/table density;
- toolbar/search/filter fidelity;
- empty/loading/error states;
- responsive breakpoints when relevant;
- visible DS/taste deviations;
- debug/prototype controls not meant for users.

## Output

Use `.agents/templates/screenshot-comparison-report.md` when reference or screenshots are involved.
