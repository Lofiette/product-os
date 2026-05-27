---
name: reference-fidelity
description: Extract a visual reference contract and compare implemented UI against it. Required when the user provides a reference screenshot/mock/example for UI/design work.
---

# reference-fidelity

## Trigger

Use when a reference image, screenshot, mock, Figma export, good example, bad example, or explicit visual comparison is part of the task.

## Inputs

- User-provided reference(s)
- Current task scope
- Taste Profile, if any
- DS mode and sources, if any
- Actual screenshot/render, if implementation exists

## Process

1. Read `docs/REFERENCE_FIDELITY.md`.
2. Extract `Reference Fidelity Spec` before implementation.
3. Identify must-match, may-adapt, and must-not-copy traits.
4. Ask for user approval when deviations are ambiguous.
5. After implementation, compare actual rendered UI to the reference.
6. Produce an Actual vs Reference Delta Table.
7. Do not accept “looks similar” as evidence.
8. Return PASS / PASS WITH WARNINGS / BLOCKED.

## Blocking conditions

- Reference exists but no reference contract was created.
- Implemented UI diverges from a must-match trait without approval.
- Actual screenshot/render is missing when screenshot comparison is possible.
- Reference fidelity is claimed using technical checks only.

## Output

Use `.agents/templates/reference-fidelity-spec.md` and `.agents/templates/actual-vs-reference-delta.md`.
