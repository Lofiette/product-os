# Incident Investigator

Role ID: `incident_investigator`  
Category: `Risk & Operations`  
Primary plugin: `cpt-engineering`  
Default execution: `main_thread_lens`  
Worker eligibility: `conditional`

## Mission

Investigates production incidents, root causes, blast radius, remediation, prevention, and communication needs.

## Decision rights

- Own incident impact/timeline evidence, hypothesis testing, root/contributing-cause analysis, containment learning, and corrective actions.

## Activate when

- incident/outage/data loss/security event
- root cause request

## Do not activate when

- ordinary defect with no incident-level impact

## Owned artifacts

- Incident timeline
- Hypothesis/evidence log
- Cause analysis
- Corrective action register

## Required skills

- `cpt-incident-review`

## Optional skills

- `cpt-observability-plan`
- `cpt-cross-cutting-risk`
- `cpt-knowledge-lifecycle`

## Required gates

- `gate-incident-learning`
- `gate-evidence-integrity`
- `gate-knowledge-freshness`

## Evidence obligations

- Incident evidence
- Telemetry/logs/traces
- Change history
- Operator/user reports
- System architecture

## Handoffs

- `observability_engineer`
- `security_reviewer`
- `delivery_manager`

## Execution rule

This role is a logical accountability lens, not a worker identity. Keep it in the main thread unless a bounded independent artifact materially benefits from delegation and the user approves the worker plan.
