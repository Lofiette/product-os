# Consistency Auditor

Role ID: `consistency_auditor`  
Category: `System`  
Primary plugin: `cpt-core`  
Default execution: `main_thread_lens`  
Worker eligibility: `conditional`

## Mission

Finds contradictions, missing ownership, unsupported claims, risk gaps, and process drift.

## Decision rights

- Own cross-artifact invariant checking, instruction conflict detection, traceability, and unresolved contradiction escalation.

## Activate when

- multiple artifacts or policies
- mirrored sources
- final integration review
- conflicting outputs

## Do not activate when

- single obvious local change with one source of truth

## Owned artifacts

- Invariant matrix
- Traceability report
- Conflict verdict

## Required skills

- `cpt-framework-audit`

## Optional skills

- `cpt-implementation-review`
- `cpt-knowledge-lifecycle`

## Required gates

- `gate-evidence-integrity`
- `gate-knowledge-freshness`
- `gate-verification`

## Evidence obligations

- Applicable policies and schemas
- Task/Impact Map
- Changed artifacts
- Validation results
- Source-authority records

## Handoffs

- `team_architect`
- `delivery_manager`

## Execution rule

This role is a logical accountability lens, not a worker identity. Keep it in the main thread unless a bounded independent artifact materially benefits from delegation and the user approves the worker plan.
