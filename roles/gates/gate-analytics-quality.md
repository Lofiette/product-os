# Analytics Quality Gate

Gate ID: `gate-analytics-quality`

## Apply when

For event instrumentation, metrics, dashboards, funnels, or experiment analysis.

## Owners

- `analytics_engineer`
- `experimentation_specialist`

## PASS criteria

- Decision, metric formula, event grain, properties, segmentation, and data-quality checks align.
- Exposure and attribution rules are defined where applicable.

## BLOCK criteria

- A metric name lacks an executable formula.
- Events cannot distinguish user intent or outcome.
- Experiment exposure or denominator is ambiguous.

## Required evidence

- Metric/event specification
- Validation queries
- Dashboard/experiment review

## Verdict contract

- `PASS`: required evidence supports the acceptance claim.
- `PASS_WITH_WARNINGS`: acceptance is supportable, with explicit non-blocking residual risk.
- `BLOCKED`: one or more blocking conditions are present.
- `INSUFFICIENT_EVIDENCE`: the gate cannot responsibly decide.

A warning must never hide a blocker. Missing evidence must never be converted into a clean pass.
