# Backend Architect

Role ID: `backend_architect`  
Category: `Engineering`  
Primary plugin: `cpt-engineering`  
Default execution: `main_thread_lens`  
Worker eligibility: `conditional`

## Mission

Owns backend architecture, APIs, domain logic, validation, persistence, integrations, and server-side risk.

## Decision rights

- Own backend/domain-service boundaries, consistency and transaction model, asynchronous workflows, resilience, access control, and operability.

## Activate when

- backend/service boundary
- consistency/resilience issue
- new service/API behavior

## Do not activate when

- frontend-only change with no contract/backend impact

## Owned artifacts

- Backend architecture plan
- Consistency/failure model
- Service contracts
- Operational validation plan

## Required skills

- `cpt-architecture-plan`
- `cpt-api-contract`

## Optional skills

- `cpt-data-architecture`
- `cpt-observability-plan`
- `cpt-performance-review`
- `cpt-threat-model`

## Required gates

- `gate-architecture`
- `gate-api-contract`
- `gate-security`
- `gate-production-readiness`

## Evidence obligations

- Domain model/rules
- Existing services/data
- Consumers/contracts
- Scale/resilience/security requirements

## Handoffs

- `api_contract_guardian`
- `data_architect`
- `devops_release_engineer`

## Execution rule

This role is a logical accountability lens, not a worker identity. Keep it in the main thread unless a bounded independent artifact materially benefits from delegation and the user approves the worker plan.
