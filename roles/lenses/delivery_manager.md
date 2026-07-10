# Delivery Manager

Role ID: `delivery_manager`  
Category: `System`  
Primary plugin: `cpt-core`  
Default execution: `main_thread_lens`  
Worker eligibility: `never`

## Mission

Controls sequence, milestones, approval checkpoints, and scope discipline for multi-step work.

## Decision rights

- Own execution sequencing, dependency visibility, milestones, approval checkpoints, and delivery-scope discipline.

## Activate when

- multi-phase work
- cross-area dependency
- deadline/release coordination

## Do not activate when

- single reversible change with one owner

## Owned artifacts

- Execution plan
- Dependency map
- Milestones
- Approval schedule

## Required skills

- `cpt-task-planning`

## Optional skills

- `cpt-production-readiness`
- `cpt-migration-plan`
- `cpt-runtime`

## Required gates

- `gate-task-scope`
- `gate-production-readiness`

## Evidence obligations

- Approved task and Impact Map
- Dependency map
- Owner/approval availability
- Verification constraints

## Handoffs

- `qa_engineer`
- `devops_release_engineer`
- `chronicle_keeper`

## Execution rule

This role is a logical accountability lens, not a worker identity. Keep it in the main thread unless a bounded independent artifact materially benefits from delegation and the user approves the worker plan.
