# Production Readiness Gate

Gate ID: `gate-production-readiness`

## Apply when

Before production release or enabling a production-facing capability.

## Owners

- `devops_release_engineer`
- `qa_engineer`
- `observability_engineer`

## PASS criteria

- Build/test/review evidence, rollout, rollback, configuration, observability, ownership, runbook, and support readiness are sufficient.
- Open risks are accepted explicitly.

## BLOCK criteria

- No rollback exists for a material change.
- Critical telemetry or ownership is missing.
- Verification is incomplete for the release risk.

## Required evidence

- Readiness report
- Rollout/rollback plan
- Runbook
- Release evidence

## Verdict contract

- `PASS`: required evidence supports the acceptance claim.
- `PASS_WITH_WARNINGS`: acceptance is supportable, with explicit non-blocking residual risk.
- `BLOCKED`: one or more blocking conditions are present.
- `INSUFFICIENT_EVIDENCE`: the gate cannot responsibly decide.

A warning must never hide a blocker. Missing evidence must never be converted into a clean pass.
