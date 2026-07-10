# Security Gate

Gate ID: `gate-security`

## Apply when

For auth, permissions, sensitive actions, network boundaries, dependencies, secrets, or elevated risk.

## Owners

- `security_reviewer`
- `solution_architect`

## PASS criteria

- Assets, actors, trust boundaries, attack paths, controls, and residual risk are explicit.
- Security-critical behaviors are verified, not assumed.

## BLOCK criteria

- An irreversible or privileged action lacks authorization/confirmation.
- Untrusted input crosses a boundary without validation.
- A critical threat has no control or explicit acceptance.

## Required evidence

- Threat model
- Control map
- Security tests/findings
- Residual-risk decision

## Verdict contract

- `PASS`: required evidence supports the acceptance claim.
- `PASS_WITH_WARNINGS`: acceptance is supportable, with explicit non-blocking residual risk.
- `BLOCKED`: one or more blocking conditions are present.
- `INSUFFICIENT_EVIDENCE`: the gate cannot responsibly decide.

A warning must never hide a blocker. Missing evidence must never be converted into a clean pass.
