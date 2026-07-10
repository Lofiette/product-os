# Knowledge Freshness Gate

Gate ID: `gate-knowledge-freshness`

## Apply when

When task output changes product boundaries, flows, contracts, decisions, or future routing knowledge.

## Owners

- `chronicle_keeper`
- `consistency_auditor`

## PASS criteria

- Affected knowledge artifacts and review triggers are identified.
- Confirmed knowledge, inference, stale claims, and task-local notes remain separated.
- Only durable, affected knowledge is updated.

## BLOCK criteria

- A completed change leaves routing knowledge materially wrong.
- Task transcript is copied into durable knowledge.
- Stale claims remain marked current.

## Required evidence

- Knowledge update diff
- Freshness markers
- Source revision/evidence references

## Verdict contract

- `PASS`: required evidence supports the acceptance claim.
- `PASS_WITH_WARNINGS`: acceptance is supportable, with explicit non-blocking residual risk.
- `BLOCKED`: one or more blocking conditions are present.
- `INSUFFICIENT_EVIDENCE`: the gate cannot responsibly decide.

A warning must never hide a blocker. Missing evidence must never be converted into a clean pass.
