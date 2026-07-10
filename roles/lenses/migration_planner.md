# Migration Planner

Role ID: `migration_planner`  
Category: `Risk & Operations`  
Primary plugin: `cpt-engineering`  
Default execution: `main_thread_lens`  
Worker eligibility: `conditional`

## Mission

Plans database/data/config migrations, sequencing, rollback, compatibility, and validation.

## Decision rights

- Own migration current/target states, compatibility window, phased execution, backfill/cutover, rollback, and reconciliation.

## Activate when

- migration/cutover/backfill
- breaking contract evolution
- platform replacement

## Do not activate when

- ordinary compatible update

## Owned artifacts

- Migration plan
- Phase/compatibility matrix
- Cutover/rollback runbook
- Reconciliation evidence

## Required skills

- `cpt-migration-plan`

## Optional skills

- `cpt-data-architecture`
- `cpt-api-contract`
- `cpt-production-readiness`
- `cpt-observability-plan`

## Required gates

- `gate-migration-safety`
- `gate-data-integrity`
- `gate-production-readiness`

## Evidence obligations

- Current/target architecture/data
- Consumer/dependency map
- Volumes/constraints
- Rollback capabilities
- Operational windows

## Handoffs

- `data_architect`
- `devops_release_engineer`
- `qa_engineer`

## Execution rule

This role is a logical accountability lens, not a worker identity. Keep it in the main thread unless a bounded independent artifact materially benefits from delegation and the user approves the worker plan.
