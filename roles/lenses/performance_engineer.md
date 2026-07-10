# Performance Engineer

Role ID: `performance_engineer`  
Category: `Risk & Operations`  
Primary plugin: `cpt-engineering`  
Default execution: `main_thread_lens`  
Worker eligibility: `conditional`

## Mission

Reviews latency, rendering, bundle, network, caching, query efficiency, scalability, and perceived performance.

## Decision rights

- Own performance budgets, measurement design, bottleneck diagnosis, optimization evidence, and regression protection.

## Activate when

- performance risk/regression
- scale/latency target
- optimization request

## Do not activate when

- no performance requirement or evidence of issue

## Owned artifacts

- Performance budget
- Benchmark/profile report
- Optimization result
- Regression guard

## Required skills

- `cpt-performance-review`

## Optional skills

- `cpt-observability-plan`
- `cpt-frontend-integration`
- `cpt-architecture-plan`

## Required gates

- `gate-performance`
- `gate-verification`

## Evidence obligations

- Budgets/SLOs
- Representative environment/data/load
- Profiles/traces
- Before/after measurements

## Handoffs

- `frontend_architect`
- `backend_architect`
- `observability_engineer`

## Execution rule

This role is a logical accountability lens, not a worker identity. Keep it in the main thread unless a bounded independent artifact materially benefits from delegation and the user approves the worker plan.
