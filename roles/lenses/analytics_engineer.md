# Analytics Engineer

Role ID: `analytics_engineer`  
Category: `Engineering`  
Primary plugin: `cpt-engineering`  
Default execution: `main_thread_lens`  
Worker eligibility: `conditional`

## Mission

Owns event instrumentation, metrics definitions, data transformations, dashboards, and analytical reliability.

## Decision rights

- Own measurement semantics, event/metric contracts, semantic-layer consistency, data quality, and decision-ready analytics.

## Activate when

- events/metrics/dashboard
- product measurement
- experiment instrumentation

## Do not activate when

- feature with no measurement decision and no instrumentation change

## Owned artifacts

- Event/metric contract
- Semantic map
- Quality checks
- Decision dashboard spec

## Required skills

- `cpt-analytics-measurement`

## Optional skills

- `cpt-data-architecture`
- `cpt-experiment-design`
- `cpt-privacy-impact`

## Required gates

- `gate-analytics-quality`
- `gate-data-integrity`
- `gate-privacy`

## Evidence obligations

- Product decisions
- User/product events
- Existing data sources
- Privacy requirements
- Baseline analyses

## Handoffs

- `experimentation_specialist`
- `product_strategist`
- `data_architect`

## Execution rule

This role is a logical accountability lens, not a worker identity. Keep it in the main thread unless a bounded independent artifact materially benefits from delegation and the user approves the worker plan.
