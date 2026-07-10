---
name: cpt-data-architecture
description: Use to review data models, storage, lineage, quality, retention, access, lifecycle, and evolution; not for product analytics instrumentation alone.
---

# CPT Data Architecture

## Use when

- A task changes persistent entities, ownership, lineage, retention, migration, or data quality.

## Do not use when

- Only frontend display mapping changes.

## Required inputs

- Domain concepts, current schemas/storage, access patterns, scale, consistency, quality, privacy/retention, lineage, and migration constraints.

## Method

1. Model entities, identities, relationships, invariants, lifecycle, and ownership.
2. Separate operational, analytical, event, cache, search, and derived data needs.
3. Review normalization/denormalization, indexing, partitioning, consistency, transactions, concurrency, and deletion.
4. Map lineage, source of truth, transformations, quality checks, and observability.
5. Define access control, encryption, retention, archival, export, and erasure.
6. Plan schema evolution, backfill, compatibility, validation, and rollback.
7. Test model against key queries, failure modes, and future change.

## Output contract

Produce a compact artifact containing:

- `Conceptual/logical data model.`
- `Storage/access/lineage/lifecycle decisions.`
- `Quality/privacy/retention controls.`
- `Migration and verification plan.`

## Evidence standard

- Entity semantics must come from domain/product evidence, not table names alone.

## Stop and escalate

- Identity/source-of-truth or retention requirements are unresolved.

## Failure modes to avoid

- Designing tables without lifecycle and access patterns.
- Using analytics data as operational source of truth.
