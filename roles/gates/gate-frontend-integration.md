# Frontend Integration Gate

Gate ID: `gate-frontend-integration`

## Apply when

For frontend implementation, component integration, routing, client/server boundaries, state, or data-flow changes.

## Owners

- `frontend_engineer`
- `frontend_architect`

## PASS criteria

- Change location and ownership are correct.
- States, async behavior, errors, accessibility, and responsive behavior are integrated.
- Verification covers systemic usages and regression risk.

## BLOCK criteria

- A systemic pattern is patched on one screen only.
- State ownership or client/server boundary is unclear.
- The result compiles but leaves visible or behavioral regressions.

## Required evidence

- Impact Map
- Changed-file rationale
- Test/render evidence
- Integration notes

## Verdict contract

- `PASS`: required evidence supports the acceptance claim.
- `PASS_WITH_WARNINGS`: acceptance is supportable, with explicit non-blocking residual risk.
- `BLOCKED`: one or more blocking conditions are present.
- `INSUFFICIENT_EVIDENCE`: the gate cannot responsibly decide.

A warning must never hide a blocker. Missing evidence must never be converted into a clean pass.
