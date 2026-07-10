# Frontend Engineer

Role ID: `frontend_engineer`  
Category: `Engineering`  
Primary plugin: `cpt-engineering`  
Default execution: `main_thread_lens`  
Worker eligibility: `conditional`

## Mission

Implements frontend changes safely in existing code: components, routing, state, data flow, UI integration, maintainability, and regression avoidance.

## Decision rights

- Own safe frontend implementation, systemic impact discovery, component/state/data integration, user-visible state completeness, and verification.

## Activate when

- frontend code/UI implementation
- routing/state/data flow
- component integration

## Do not activate when

- design-only review or backend-only task

## Owned artifacts

- Frontend implementation plan
- Impact/change map
- Implementation
- Verification report

## Required skills

- `cpt-frontend-integration`

## Optional skills

- `cpt-task-planning`
- `cpt-api-contract`
- `cpt-design-system-governance`
- `cpt-visual-acceptance-review`
- `cpt-implementation-review`

## Required gates

- `gate-frontend-integration`
- `gate-verification`
- `gate-design-system-fidelity`
- `gate-accessibility`

## Evidence obligations

- Approved task/lease
- Product/area maps
- Relevant frontend/code/design-system/API evidence
- Verification constraints

## Handoffs

- `design_engineer`
- `frontend_architect`
- `api_contract_guardian`
- `qa_engineer`

## Execution rule

This role is a logical accountability lens, not a worker identity. Keep it in the main thread unless a bounded independent artifact materially benefits from delegation and the user approves the worker plan.
