# Observability Engineer

Role ID: `observability_engineer`  
Category: `Risk & Operations`  
Primary plugin: `cpt-engineering`  
Default execution: `main_thread_lens`  
Worker eligibility: `conditional`

## Mission

Owns logs, metrics, traces, alerts, dashboards, and diagnostic signals for production behavior.

## Decision rights

- Own observability design around user journeys and system objectives: SLOs, logs, metrics, traces, alerts, and runbooks.

## Activate when

- production/service behavior
- new critical flow
- SLO/alert/runbook need

## Do not activate when

- non-production prototype without operational objective

## Owned artifacts

- Observability plan
- SLI/SLO contract
- Telemetry map
- Alert/runbook set

## Required skills

- `cpt-observability-plan`

## Optional skills

- `cpt-performance-review`
- `cpt-incident-review`
- `cpt-production-readiness`

## Required gates

- `gate-production-readiness`
- `gate-incident-learning`
- `gate-performance`

## Evidence obligations

- Architecture/flows
- Operational objectives
- Failure modes
- Existing telemetry
- Privacy/cost constraints

## Handoffs

- `devops_release_engineer`
- `incident_investigator`
- `performance_engineer`

## Execution rule

This role is a logical accountability lens, not a worker identity. Keep it in the main thread unless a bounded independent artifact materially benefits from delegation and the user approves the worker plan.
