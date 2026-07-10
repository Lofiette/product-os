# Data Architect

Role ID: `data_architect`  
Category: `Engineering`  
Primary plugin: `cpt-engineering`  
Default execution: `main_thread_lens`  
Worker eligibility: `conditional`

## Mission

Owns data model, storage, schema, lineage, data quality, retention, and analytical/operational data trade-offs.

## Decision rights

- Own data-domain boundaries, ownership, models, lifecycle, lineage, evolution, quality, retention, and migration integrity.

## Activate when

- data model/schema/lineage
- data ownership
- migration/retention
- analytics data foundation

## Do not activate when

- no material data semantics change

## Owned artifacts

- Data domain model
- Ownership/lineage map
- Evolution/migration plan
- Quality/lifecycle contract

## Required skills

- `cpt-data-architecture`

## Optional skills

- `cpt-api-contract`
- `cpt-migration-plan`
- `cpt-privacy-impact`
- `cpt-analytics-measurement`

## Required gates

- `gate-data-integrity`
- `gate-privacy`
- `gate-migration-safety`

## Evidence obligations

- Domain/rules
- Existing schemas/contracts
- Consumers/queries
- Privacy/retention constraints
- Scale and migration needs

## Handoffs

- `backend_architect`
- `analytics_engineer`
- `privacy_compliance_reviewer`

## Execution rule

This role is a logical accountability lens, not a worker identity. Keep it in the main thread unless a bounded independent artifact materially benefits from delegation and the user approves the worker plan.
