---
name: cpt-data-visualization-review
description: Use to design or review charts, dashboards, reports, metric semantics, scales, aggregation, comparison, and cognitive load.
---

# CPT Data Visualization Review

## Use when

- The interface communicates quantitative data or supports data-driven decisions.

## Do not use when

- The task is generic page layout without data visualization.

## Required inputs

- User decision, metric definitions, data shape/quality, comparison needs, uncertainty, audience, and interaction constraints.

## Method

1. Define the question and decision each visualization supports.
2. Verify metric semantics, units, aggregation, baseline, denominator, filters, and uncertainty.
3. Choose encoding based on task: comparison, trend, distribution, composition, relationship, ranking, or status.
4. Check scale, zero baseline, truncation, binning, dual axes, color, ordering, and misleading emphasis.
5. Design annotations, thresholds, empty/loading/error/stale states, and data-quality caveats.
6. Reduce chart junk and progressive-disclose detail without hiding critical context.
7. Test comprehension, accessibility, responsiveness, export, and localization.

## Output contract

Produce a compact artifact containing:

- `Decision/metric/visual mapping.`
- `Visualization recommendation and alternatives.`
- `Misleading-risk and data-quality findings.`
- `Interaction/state/accessibility requirements.`

## Evidence standard

- A chart cannot fix an undefined metric.

## Stop and escalate

- Metric semantics or source quality is unresolved.

## Failure modes to avoid

- Choosing chart type for aesthetics.
- Using color as the only meaning carrier.
