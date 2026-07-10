---
name: cpt-migration-plan
description: Use to plan schema, data, config, API, platform, or dependency migrations with compatibility, backfill, validation, rollback, and observability.
---

# CPT Migration Plan

## Use when

- Existing state or consumers must move safely to a new representation or system.

## Do not use when

- A local refactor has no persisted/external compatibility boundary.

## Required inputs

- Current/target state, consumers, data volume/quality, downtime tolerance, compatibility window, operational ownership, and risk.

## Method

1. Inventory current state, consumers, invariants, data quality, and irreversible actions.
2. Choose strategy: expand-contract, dual write/read, backfill, shadow, blue-green, feature flag, or cutover.
3. Define compatibility adapters, versioning, sequencing, and exit criteria.
4. Plan dry run, backups, backfill batching, checksums/reconciliation, and error handling.
5. Instrument progress, correctness, latency, failures, and business impact.
6. Define rollback point, forward-fix plan, ownership, and runbook.
7. Validate cleanup and removal of compatibility code only after evidence.

## Output contract

Produce a compact artifact containing:

- `Current/target inventory.`
- `Phased migration/cutover plan.`
- `Validation/reconciliation and observability.`
- `Rollback/forward-fix/runbook and risks.`

## Evidence standard

- No irreversible migration without backup/reconciliation evidence.

## Stop and escalate

- Rollback is impossible and risk is unapproved.
- Source data quality is unknown.

## Failure modes to avoid

- Treating deployment as migration completion.
- Deleting compatibility paths before consumers move.
