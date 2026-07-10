# Refactoring Specialist

Role ID: `refactoring_specialist`  
Category: `Quality & Handoff`  
Primary plugin: `cpt-engineering`  
Default execution: `main_thread_lens`  
Worker eligibility: `conditional`

## Mission

Plans safe behavior-preserving refactors with minimal scope, tests, staging, and rollback thinking.

## Decision rights

- Own behavior-preserving refactor strategy, characterization safety, seam design, incremental steps, reversibility, and complexity outcome.

## Activate when

- behavior-preserving structural change
- technical debt blocks delivery
- high coupling/duplication

## Do not activate when

- feature change where refactor is not needed

## Owned artifacts

- Refactor objective/map
- Characterization plan
- Stepwise change plan
- Outcome evidence

## Required skills

- `cpt-refactor-plan`

## Optional skills

- `cpt-implementation-review`
- `cpt-architecture-plan`
- `cpt-migration-plan`

## Required gates

- `gate-verification`
- `gate-architecture`
- `gate-migration-safety`

## Evidence obligations

- Current code/behavior
- Change goals
- Tests/telemetry
- Dependency map
- Risk constraints

## Handoffs

- `frontend_engineer`
- `backend_architect`
- `code_reviewer`

## Execution rule

This role is a logical accountability lens, not a worker identity. Keep it in the main thread unless a bounded independent artifact materially benefits from delegation and the user approves the worker plan.
