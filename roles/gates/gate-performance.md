# Performance Gate

Gate ID: `gate-performance`

## Apply when

For latency, throughput, bundle/runtime cost, rendering, query, scaling, or resource-sensitive changes.

## Owners

- `performance_engineer`
- `frontend_architect`
- `backend_architect`

## PASS criteria

- Budget and baseline are defined.
- Measurements isolate the bottleneck.
- Before/after evidence and regression protection exist.

## BLOCK criteria

- Optimization is made without measurement.
- A visible regression exceeds the agreed budget.
- Load or scale assumptions are untested.

## Required evidence

- Budget
- Profile/benchmark
- Before/after result
- Regression check

## Verdict contract

- `PASS`: required evidence supports the acceptance claim.
- `PASS_WITH_WARNINGS`: acceptance is supportable, with explicit non-blocking residual risk.
- `BLOCKED`: one or more blocking conditions are present.
- `INSUFFICIENT_EVIDENCE`: the gate cannot responsibly decide.

A warning must never hide a blocker. Missing evidence must never be converted into a clean pass.
