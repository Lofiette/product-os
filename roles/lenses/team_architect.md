# Team Architect

Role ID: `team_architect`  
Category: `System`  
Primary plugin: `cpt-core`  
Default execution: `main_thread_lens`  
Worker eligibility: `never`

## Mission

Assembles the smallest sufficient team, maps roles to skills, and chooses orchestration mode without wasting context.

## Decision rights

- Own the minimal expertise composition, role-to-decision ownership, skill/gate routing, and proposed execution mode.

## Activate when

- multiple decision domains
- uncertain role ownership
- worker proposal

## Do not activate when

- single-domain micro change with obvious owner

## Owned artifacts

- Expertise contract
- Role/skill/gate plan
- Execution-mode proposal
- Skipped-role rationale

## Required skills

- `cpt-task-planning`

## Optional skills

- `cpt-delegation`
- `cpt-framework-audit`
- `cpt-cross-cutting-risk`

## Required gates

- `gate-task-scope`
- `gate-evidence-integrity`

## Evidence obligations

- Task brief
- Role registry
- Skill registry
- Risk triggers
- Artifact and gate requirements

## Handoffs

- `delivery_manager`
- `consistency_auditor`

## Execution rule

This role is a logical accountability lens, not a worker identity. Keep it in the main thread unless a bounded independent artifact materially benefits from delegation and the user approves the worker plan.
