# API Contract Gate

Gate ID: `gate-api-contract`

## Apply when

For endpoint, schema, event, client/server contract, pagination, error, or compatibility changes.

## Owners

- `api_contract_guardian`
- `backend_architect`
- `frontend_engineer`

## PASS criteria

- Consumers and compatibility class are known.
- Schemas, errors, idempotency, pagination, versioning, and deprecation are covered as applicable.
- Contract tests or equivalent verification exist.

## BLOCK criteria

- A breaking change is treated as additive.
- Error or nullability behavior is implicit.
- Frontend behavior depends on undocumented backend semantics.

## Required evidence

- Contract diff
- Compatibility assessment
- Consumer map
- Contract-test evidence

## Verdict contract

- `PASS`: required evidence supports the acceptance claim.
- `PASS_WITH_WARNINGS`: acceptance is supportable, with explicit non-blocking residual risk.
- `BLOCKED`: one or more blocking conditions are present.
- `INSUFFICIENT_EVIDENCE`: the gate cannot responsibly decide.

A warning must never hide a blocker. Missing evidence must never be converted into a clean pass.
