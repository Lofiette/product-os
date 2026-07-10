---
name: cpt-accessibility-review
description: Use to review semantics, keyboard, focus, labels, ARIA, announcements, contrast, motion, and accessible error/recovery behavior.
---

# CPT Accessibility Review

## Use when

- A user-facing interface, component, flow, or coded change is being designed or reviewed.

## Do not use when

- The task has no user interface or interaction.

## Required inputs

- Rendered/implemented UI, component semantics, interaction/state model, content, platform, and applicable accessibility target.

## Method

1. Identify native semantics and accessible name/role/value for interactive elements.
2. Trace keyboard order, focus entry/return, traps, shortcuts, and visible focus.
3. Review labels, instructions, errors, validation associations, status announcements, and live regions.
4. Check headings, landmarks, reading order, tables, lists, dialogs, forms, and dynamic updates.
5. Assess color/contrast, non-color cues, zoom/reflow, motion, target size, and responsive impacts.
6. Test representative screen-reader and keyboard flows where tools are available.
7. Classify blockers and define exact remediation and verification.

## Output contract

Produce a compact artifact containing:

- `Accessibility scope and target.`
- `Findings by principle/element/severity.`
- `Keyboard/focus and screen-reader flow.`
- `Remediation, tests, and PASS/WARN/BLOCKED verdict.`

## Evidence standard

- ARIA does not compensate for incorrect interaction behavior.

## Stop and escalate

- The implementation cannot be rendered or semantics cannot be inspected.

## Failure modes to avoid

- Checklist-only review without task flows.
- Adding ARIA to native elements unnecessarily.
