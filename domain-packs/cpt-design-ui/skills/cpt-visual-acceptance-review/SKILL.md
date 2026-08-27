---
name: cpt-visual-acceptance-review
description: Use to review rendered UI against product goals, specs, sources, design system, UI craft, states, responsiveness, accessibility, and defects.
---

# CPT Visual Acceptance Review

## Use when

- A UI screen, prototype, or implementation needs visual/product-quality acceptance.
- A human or agent design solution needs structured critique or comparison.
- A rendered result must be checked against a screen/module decision and design-system sources.

## Do not use when

- No rendered evidence or inspectable implementation exists and only planning is requested.
- The decision is purely about information architecture and visual acceptance is intentionally deferred.

## Required inputs

- Rendered screenshots/page states or inspectable implementation.
- Screen/module design decision and intended perception order.
- Product/task context and target review profile.
- Reference/taste contract when applicable.
- Authoritative design-system sources.
- State and responsive matrix.
- Changed files, technical constraints, and verification results.

## Required reference

Use `../cpt-screen-module-design/references/UI_CRAFT_REVIEW_RUBRIC.md` and apply `../cpt-screen-module-design/references/UI_KNOWLEDGE_POLICY.md` when interpreting book-derived criteria.

## Method

1. Build a compact review packet with target route, roles/tasks, states, breakpoints, screenshots, changed files, source authority, and missing evidence.
2. Inspect the rendered result before reading its rationale where practical to reduce confirmation bias.
3. Run the five-second scan: location, state, primary information, primary action, and main groups.
4. Evaluate problem fit, task flow, state/recovery, IA, hierarchy, grouping, alignment, rhythm, typography, color, affordance, density, content, responsiveness, system use, accessibility, restraint, and implementation realism.
5. Compare actual versus target and source authority using explicit deltas, not visual impression.
6. Stress representative empty/loading/error/success/disabled/permission/destructive/extreme-data/localized/zoom states.
7. Run the subtraction pass and adversarial critique. When an execution adapter produced the artifact, verify source/provenance and avoid accepting the adapter's own QA as the sole judge.
8. Separate code-contract findings, product/UX findings, visual-craft findings, accessibility findings, and missing evidence.
9. Score dimensions for diagnosis, but let blockers and evidence determine the verdict.
10. Fix or block avoidable issues. Final visual PASS requires sufficient rendered evidence.

## Output contract

Produce a compact artifact containing:

- `Review packet, profile, and evidence list.`
- `Five-second scan and actual-vs-target delta table.`
- `Dimension scorecard with concise evidence.`
- `Blockers/major/minor findings with impact, smallest systemic fix, and verification.`
- `Subtraction opportunities and residual risk.`
- `PASS/PASS_WITH_WARNINGS/BLOCKED/INSUFFICIENT_EVIDENCE verdict.`

## Evidence standard

- Build, lint, test, scanner, or console success is not visual acceptance.
- No screenshot or rendered evidence means no clean visual PASS.
- A numeric score cannot hide a blocker.
- Book-derived recipes are not authoritative when the project design system or current requirements differ.
- A self-review should be independently challenged for material decisions when feasible.
- Tool/provider QA is supporting evidence; it cannot independently certify the same provider's output.

## Stop and escalate

- Rendered evidence is unavailable for a claim requiring visual inspection.
- Product goal, intended hierarchy, or design-system authority is unresolved.
- A specialist accessibility, content, data, or system gate is required and unavailable.

## Failure modes to avoid

- Reviewing only surface similarity.
- Reading rationale first and then seeing only what it claims.
- Treating personal taste as evidence.
- Reporting zero scanner findings as design quality.
- Averaging severe failures into a passing score.
- Ignoring expert efficiency, content realism, or non-happy states.
