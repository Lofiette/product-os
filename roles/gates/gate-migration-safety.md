# Migration Safety Gate

Gate ID: `gate-migration-safety`

## Apply when

For schema, storage, platform, dependency, API, or architecture migrations.

## Owners

- `migration_planner`
- `data_architect`
- `devops_release_engineer`

## PASS criteria

- Current/target states, compatibility window, phases, backfill, cutover, rollback, observability, and ownership are explicit.
- Rehearsal or validation matches risk.

## BLOCK criteria

- Cutover is irreversible without approval.
- Dual-read/write or compatibility behavior is undefined where needed.
- Backfill/reconciliation cannot prove completeness.

## Required evidence

- Migration plan
- Rehearsal result
- Rollback procedure
- Reconciliation evidence

## Verdict contract

- `PASS`: required evidence supports the acceptance claim.
- `PASS_WITH_WARNINGS`: acceptance is supportable, with explicit non-blocking residual risk.
- `BLOCKED`: one or more blocking conditions are present.
- `INSUFFICIENT_EVIDENCE`: the gate cannot responsibly decide.

A warning must never hide a blocker. Missing evidence must never be converted into a clean pass.
