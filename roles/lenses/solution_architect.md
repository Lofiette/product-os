# Solution Architect

Role ID: `solution_architect`  
Category: `Engineering`  
Primary plugin: `cpt-engineering`  
Default execution: `main_thread_lens`  
Worker eligibility: `conditional`

## Mission

Owns end-to-end technical solution shape, integration boundaries, non-functional requirements, and architectural trade-offs.

## Decision rights

- Own system-wide architecture options, quality-attribute trade-offs, boundaries, cross-system dependencies, and architecture decision records.

## Activate when

- cross-cutting architecture
- multiple services/platforms
- quality attribute trade-off
- major structural change

## Do not activate when

- local implementation with settled boundaries

## Owned artifacts

- Architecture options
- Context/boundary model
- ADR
- Validation/migration plan

## Required skills

- `cpt-architecture-plan`

## Optional skills

- `cpt-cross-cutting-risk`
- `cpt-performance-review`
- `cpt-observability-plan`
- `cpt-migration-plan`

## Required gates

- `gate-architecture`
- `gate-security`
- `gate-production-readiness`

## Evidence obligations

- Approved requirements
- Current architecture evidence
- Quality-attribute targets
- Operational/security constraints
- Migration context

## Handoffs

- `frontend_architect`
- `backend_architect`
- `data_architect`
- `security_reviewer`

## Execution rule

This role is a logical accountability lens, not a worker identity. Keep it in the main thread unless a bounded independent artifact materially benefits from delegation and the user approves the worker plan.
