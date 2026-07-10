# Privacy Gate

Gate ID: `gate-privacy`

## Apply when

For personal/sensitive data, telemetry, retention, sharing, profiling, or user rights.

## Owners

- `privacy_compliance_reviewer`
- `data_architect`

## PASS criteria

- Data inventory, purpose, minimization, flow, access, retention, deletion, and user-right implications are explicit.
- Unknown legal requirements are escalated rather than invented.

## BLOCK criteria

- Data is collected without an articulated purpose.
- Retention/deletion behavior is undefined.
- Sensitive data appears in logs or prompts without controls.

## Required evidence

- Privacy impact assessment
- Data-flow map
- Retention/access decisions

## Verdict contract

- `PASS`: required evidence supports the acceptance claim.
- `PASS_WITH_WARNINGS`: acceptance is supportable, with explicit non-blocking residual risk.
- `BLOCKED`: one or more blocking conditions are present.
- `INSUFFICIENT_EVIDENCE`: the gate cannot responsibly decide.

A warning must never hide a blocker. Missing evidence must never be converted into a clean pass.
