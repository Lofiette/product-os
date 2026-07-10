# Data Integrity Gate

Gate ID: `gate-data-integrity`

## Apply when

For data models, migrations, lineage, retention, metrics, or event semantics.

## Owners

- `data_architect`
- `analytics_engineer`

## PASS criteria

- Ownership, lifecycle, constraints, lineage, evolution, and quality controls are explicit.
- Backfill/rollback and reconciliation are defined when data changes.
- Metric/event semantics are stable and testable.

## BLOCK criteria

- A migration can silently lose or reinterpret data.
- Two teams can compute the same metric differently.
- Retention or sensitive-data lifecycle is undefined.

## Required evidence

- Data model/contract
- Lineage map
- Migration/reconciliation plan
- Quality checks

## Verdict contract

- `PASS`: required evidence supports the acceptance claim.
- `PASS_WITH_WARNINGS`: acceptance is supportable, with explicit non-blocking residual risk.
- `BLOCKED`: one or more blocking conditions are present.
- `INSUFFICIENT_EVIDENCE`: the gate cannot responsibly decide.

A warning must never hide a blocker. Missing evidence must never be converted into a clean pass.
