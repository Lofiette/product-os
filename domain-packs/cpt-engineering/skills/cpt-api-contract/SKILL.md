---
name: cpt-api-contract
description: Use for API/data-shape prewarm or review of schemas, compatibility, errors, idempotency, pagination, versioning, and contract tests.
---

# CPT API Contract

## Use when

- A frontend/backend integration, public/internal API, event contract, or data shape may change.
- Product onboarding needs frontend-facing contract knowledge without backend deep dive.

## Do not use when

- The task is internal implementation with no boundary change.

## Required inputs

- Consumer/provider needs, current schemas/types, endpoint/event definitions, compatibility policy, usage evidence, error/idempotency/pagination expectations, and rollout constraints.

## Method

1. Choose mode: contract prewarm, new contract design, change review, or compatibility audit.
2. Identify consumers, providers, ownership, version/source of truth, and lifecycle.
3. Review request/response/event schemas, required/optional/null/default semantics, identifiers, timestamps, enums/open strings, and secret fields.
4. Classify change as compatible, conditionally compatible, or breaking for each consumer.
5. Define errors, retries, timeouts, idempotency, concurrency, pagination/filtering, auth/permission, and partial failure.
6. Plan schema validation, generated types, contract tests, rollout, deprecation, and rollback.
7. Keep backend internals out unless they affect the contract.

## Output contract

Produce a compact artifact containing:

- `Contract map or prewarm brief.`
- `Compatibility/change classification.`
- `Error/idempotency/pagination/security semantics.`
- `Tests, rollout/deprecation plan, and unknowns.`

## Evidence standard

- Route names/types support contract candidates; runtime behavior requires implementation or test evidence.

## Stop and escalate

- Provider/consumer source of truth is unclear.
- A breaking change lacks migration and versioning decision.

## Failure modes to avoid

- Treating TypeScript types as complete runtime validation.
- Using open-ended status strings as closed enums.
