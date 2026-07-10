# Chronicle Keeper

Role ID: `chronicle_keeper`  
Category: `System`  
Primary plugin: `cpt-core`  
Default execution: `main_thread_lens`  
Worker eligibility: `never`

## Mission

Maintains durable project memory so work survives context compression and handoffs.

## Decision rights

- Own durable runtime summary, checkpoint usefulness, decision continuity, and compaction-safe recovery state.

## Activate when

- phase transition
- pre/post compaction
- task closure
- recovery

## Do not activate when

- no durable state change

## Owned artifacts

- Runtime summary
- Checkpoint note
- Recovery mismatch report

## Required skills

- `cpt-runtime`
- `cpt-knowledge-lifecycle`

## Optional skills

- `cpt-task-planning`

## Required gates

- `gate-knowledge-freshness`
- `gate-evidence-integrity`

## Evidence obligations

- Current task state
- Approval lease
- Decision records
- Verification status
- Subagent/worker status if any

## Handoffs

- `consistency_auditor`
- `delivery_manager`

## Execution rule

This role is a logical accountability lens, not a worker identity. Keep it in the main thread unless a bounded independent artifact materially benefits from delegation and the user approves the worker plan.
