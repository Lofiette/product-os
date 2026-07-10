---
name: cpt-visual-acceptance-review
description: Use to review rendered UI and coded interaction against specs, references, design system, states, taste, responsiveness, and obvious defects.
---

# CPT Visual Acceptance Review

## Use when

- A UI screen, prototype, or implementation needs visual/product-quality acceptance.

## Do not use when

- No rendered evidence or inspectable implementation exists and only planning is requested.

## Required inputs

- Rendered screenshots/page states, screen/module spec, reference/taste contract, design-system sources, changed files, state matrix, and verification results.

## Method

1. Build a compact review packet with target route, states, screenshots, changed files, source authority, and missing evidence.
2. Inspect information hierarchy, primary action, density, spacing, alignment, typography, content, component use, states, responsive behavior, and accessibility basics.
3. Compare actual vs reference/spec using explicit deltas, not visual impression.
4. Check empty/loading/error/success/disabled/permission/destructive/debug states.
5. Use screenshot capture across critical breakpoints/states when possible.
6. Separate code-contract findings, visual findings, UX findings, and missing evidence.
7. Fix or block avoidable issues; final PASS requires sufficient rendered evidence.

## Output contract

Produce a compact artifact containing:

- `Review packet and evidence list.`
- `Actual-vs-target delta table.`
- `Blockers/major/minor findings with impact and fix.`
- `PASS/WARN/BLOCKED verdict and unverified areas.`

## Evidence standard

- Build/console success is not visual acceptance.
- No screenshot/reference evidence means no clean visual PASS.

## Stop and escalate

- Rendered evidence is unavailable for a claim requiring visual inspection.
- Design-system authority is unresolved.

## Failure modes to avoid

- Self-reviewing with the same assumptions used to implement.
- Reporting zero scanner findings as design quality.
