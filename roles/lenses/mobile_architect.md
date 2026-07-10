# Mobile Architect

Role ID: `mobile_architect`  
Category: `Engineering`  
Primary plugin: `cpt-engineering`  
Default execution: `main_thread_lens`  
Worker eligibility: `conditional`

## Mission

Owns mobile architecture, platform conventions, navigation, offline behavior, device constraints, and release implications.

## Decision rights

- Own mobile platform architecture, lifecycle/offline behavior, navigation/state, device capabilities, performance, and release constraints.

## Activate when

- mobile app/platform
- offline/device/lifecycle behavior
- mobile migration

## Do not activate when

- web-only task

## Owned artifacts

- Mobile architecture plan
- Lifecycle/sync model
- Platform decision record
- Release validation matrix

## Required skills

- `cpt-architecture-plan`

## Optional skills

- `cpt-frontend-integration`
- `cpt-api-contract`
- `cpt-performance-review`
- `cpt-production-readiness`

## Required gates

- `gate-architecture`
- `gate-performance`
- `gate-accessibility`
- `gate-production-readiness`

## Evidence obligations

- Product flows
- Platform/device constraints
- Existing mobile architecture
- API/data contracts
- Release/testing requirements

## Handoffs

- `frontend_engineer`
- `api_contract_guardian`
- `qa_engineer`

## Execution rule

This role is a logical accountability lens, not a worker identity. Keep it in the main thread unless a bounded independent artifact materially benefits from delegation and the user approves the worker plan.
