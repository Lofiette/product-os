# Accessibility Gate

Gate ID: `gate-accessibility`

## Apply when

For user-facing interactions, forms, dialogs, navigation, data displays, or component changes.

## Owners

- `accessibility_specialist`
- `design_engineer`

## PASS criteria

- Semantics, keyboard operation, focus, names/labels, announcements, contrast, motion, and recovery are reviewed as applicable.
- Blocking accessibility defects are fixed or explicitly accepted.

## BLOCK criteria

- A primary flow is inaccessible by keyboard.
- Controls lack an accessible name or error association.
- Color is the only carrier of critical meaning.

## Required evidence

- Accessibility checklist
- Keyboard/focus trace
- Automated and manual findings

## Verdict contract

- `PASS`: required evidence supports the acceptance claim.
- `PASS_WITH_WARNINGS`: acceptance is supportable, with explicit non-blocking residual risk.
- `BLOCKED`: one or more blocking conditions are present.
- `INSUFFICIENT_EVIDENCE`: the gate cannot responsibly decide.

A warning must never hide a blocker. Missing evidence must never be converted into a clean pass.
