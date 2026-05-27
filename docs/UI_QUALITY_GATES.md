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


## Current-page UI review gate

When reviewing a rendered page or prototype, create a `UI Review Packet` before spawning UI/design reviewers. Reviewers must return PASS/WARN/BLOCKED with evidence and at most 5 findings. If reviewer subagents do not complete, apply `SUBAGENT_FAILURE_POLICY.md`; do not mark DS/taste/fidelity gates as PASS solely because a reviewer did not return.


## Runtime adequacy reminder

- Report Subagent Completion Status whenever real subagents are used or fail.

## Reference Fidelity Gate

Required when the user provides a reference screenshot/mock/example.

- Create a Reference Fidelity Spec before implementation.
- Compare actual rendered UI against the reference after implementation.
- Do not accept “looks similar” as evidence.
- Build success, console-clean route, raw-value scan, and component-import scan do not prove reference fidelity.
- Final UI verdict cannot be PASS without screenshot/reference comparison when rendering is possible.

BLOCKED if:
- a must-match reference trait is violated without approval;
- reference exists but no comparison was performed;
- content/taste contradicts explicit bad examples;
- actual screenshot is unavailable and no limitation was accepted.

## Design Source Authority Gate

Before claiming DS compliance, report design-source authority:

- authoritative DS docs/code;
- candidate generated manifest;
- provisional prototype UI contract;
- self-generated artifact.

Generated artifacts cannot validate themselves.

BLOCKED if:
- DS compliance is claimed against a manifest generated or materially changed in the same operation without approval;
- custom UI is introduced when an authoritative DS component exists;
- DS source is unknown but strict compliance is claimed.

## Content Realism Gate

Prototype/demo content must be realistic enough to validate layout, comprehension, and hierarchy.

BLOCKED if placeholder/internal content prevents judging UI quality or target-audience fit.

## Debug Control Gate

Visible dev/prototype controls must be classified. Unknown or dev-only controls in user-facing UI are BLOCKED until removed, segregated, or explicitly accepted.

## Visual Acceptance reminder

Use `docs/VISUAL_ACCEPTANCE_CRITERIA.md`: technical checks are not design success.
