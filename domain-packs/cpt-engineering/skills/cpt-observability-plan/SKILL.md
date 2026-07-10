---
name: cpt-observability-plan
description: Use to design logs, metrics, traces, dashboards, alerts, debug context, and runbook signals around decisions and failures.
---

# CPT Observability Plan

## Use when

- A service, migration, release, incident-prone flow, or complex feature needs operational visibility.

## Do not use when

- The task is product analytics rather than system observability.

## Required inputs

- Architecture/flow, SLOs, failure modes, operators, existing telemetry, privacy/security constraints, and incident workflow.

## Method

1. Define critical user/system journeys and observable success/failure.
2. Choose RED/USE or domain-specific metrics and trace boundaries.
3. Define structured logs with event names, correlation IDs, context, levels, sampling, and redaction.
4. Map traces/spans across boundaries and async work.
5. Design dashboards for diagnosis and alerts for actionable symptoms with ownership.
6. Add release/migration markers, audit signals, and debug breadcrumbs.
7. Define retention, cost, cardinality, access, and runbook response.

## Output contract

Produce a compact artifact containing:

- `Signal map: logs/metrics/traces.`
- `Dashboard/alert/runbook design.`
- `Correlation, sampling, privacy, and cost controls.`
- `Validation and missing-instrumentation plan.`

## Evidence standard

- Every alert needs an owner and action.

## Stop and escalate

- SLO/failure ownership is undefined.

## Failure modes to avoid

- Logging sensitive payloads.
- Alerting on every error rather than user impact.
