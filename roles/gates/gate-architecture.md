# Architecture Gate

Gate ID: `gate-architecture`

## Apply when

For changes to boundaries, shared infrastructure, quality attributes, system decomposition, or platform architecture.

## Owners

- `solution_architect`
- `frontend_architect`
- `backend_architect`
- `mobile_architect`

## PASS criteria

- Quality attributes and constraints are explicit.
- Alternatives and trade-offs are compared.
- Boundaries, dependencies, failure modes, and migration/rollback are defined.

## BLOCK criteria

- Architecture is selected by familiarity alone.
- A cross-cutting dependency is introduced without ownership.
- The design cannot explain failure containment or evolution.

## Required evidence

- Architecture decision record
- Boundary/context diagram
- Trade-off matrix
- Validation plan

## Verdict contract

- `PASS`: required evidence supports the acceptance claim.
- `PASS_WITH_WARNINGS`: acceptance is supportable, with explicit non-blocking residual risk.
- `BLOCKED`: one or more blocking conditions are present.
- `INSUFFICIENT_EVIDENCE`: the gate cannot responsibly decide.

A warning must never hide a blocker. Missing evidence must never be converted into a clean pass.
