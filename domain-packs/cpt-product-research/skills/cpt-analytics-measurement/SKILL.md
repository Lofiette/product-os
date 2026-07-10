---
name: cpt-analytics-measurement
description: Use to define event taxonomy, metrics, properties, data sources, segmentation, dashboards, and data-quality checks.
---

# CPT Analytics Measurement

## Use when

- A product decision, launch, or experiment needs observable behavior and success measures.

## Do not use when

- The task requires data-model architecture rather than product measurement.

## Required inputs

- Product outcome, user journey, decisions, existing instrumentation, data constraints, privacy rules, and reporting audience.

## Method

1. Translate outcomes into behavioral metrics and guardrails.
2. Define event names, triggers, actors, object IDs, properties, context, and deduplication rules.
3. Map each metric to events/data sources and specify numerator, denominator, window, exclusions, and segmentation.
4. Identify leading/lagging metrics and counter-metrics.
5. Define validation, QA, identity/session issues, late events, schema evolution, and backfill needs.
6. Design dashboards/alerts around decisions rather than vanity reporting.
7. Record baselines, caveats, owners, and retention/privacy constraints.

## Output contract

Produce a compact artifact containing:

- `Metric tree and decision map.`
- `Event/property taxonomy.`
- `Metric definitions and data lineage.`
- `QA, dashboard, alert, and caveat plan.`

## Evidence standard

- A metric without a data source and decision use is not ready.

## Stop and escalate

- Identity or event semantics are unresolved.
- Measurement would collect unnecessary sensitive data.

## Failure modes to avoid

- Calling page views engagement.
- Changing event meaning without versioning.
