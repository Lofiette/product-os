# Product Design Quality Gate

Gate ID: `gate-design-quality`

## Apply when

For new or redesigned screens, flows, modules, or interaction behavior.

## Owners

- `product_designer`
- `ux_interaction_reviewer`

## PASS criteria

- User goal, information hierarchy, primary action, states, and edge cases are explicit.
- The design can be handed off without inventing missing behavior.
- Alternatives and rationale are visible for material decisions.

## BLOCK criteria

- The screen is visually composed but behavior/states are undefined.
- Multiple primary actions compete without rationale.
- The implementation team must infer core interaction decisions.

## Required evidence

- Screen/module design spec
- State matrix
- Interaction rationale
- Design QA notes

## Verdict contract

- `PASS`: required evidence supports the acceptance claim.
- `PASS_WITH_WARNINGS`: acceptance is supportable, with explicit non-blocking residual risk.
- `BLOCKED`: one or more blocking conditions are present.
- `INSUFFICIENT_EVIDENCE`: the gate cannot responsibly decide.

A warning must never hide a blocker. Missing evidence must never be converted into a clean pass.
