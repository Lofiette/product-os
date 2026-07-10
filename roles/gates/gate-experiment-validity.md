# Experiment Validity Gate

Gate ID: `gate-experiment-validity`

## Apply when

For experiments, feature flags used as experiments, or causal claims.

## Owners

- `experimentation_specialist`
- `analytics_engineer`

## PASS criteria

- Hypothesis, unit, exposure, primary/guardrail metrics, sample/duration, analysis and stopping rules are defined.
- Decision rule is known before results.

## BLOCK criteria

- Users are analyzed without reliable exposure.
- Multiple metrics enable post-hoc success.
- The experiment cannot distinguish implementation failure from hypothesis failure.

## Required evidence

- Experiment design
- Instrumentation validation
- Analysis plan
- Result decision

## Verdict contract

- `PASS`: required evidence supports the acceptance claim.
- `PASS_WITH_WARNINGS`: acceptance is supportable, with explicit non-blocking residual risk.
- `BLOCKED`: one or more blocking conditions are present.
- `INSUFFICIENT_EVIDENCE`: the gate cannot responsibly decide.

A warning must never hide a blocker. Missing evidence must never be converted into a clean pass.
