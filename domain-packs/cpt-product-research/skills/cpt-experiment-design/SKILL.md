---
name: cpt-experiment-design
description: Use to design A/B tests, pilots, quasi-experiments, hypotheses, guardrails, sample logic, and decision rules.
---

# CPT Experiment Design

## Use when

- Competing product solutions can be evaluated with measurable outcomes.
- A staged pilot is needed before broad rollout.

## Do not use when

- The decision is safety-critical and randomization is inappropriate.
- The question can be answered by simple usability research.

## Required inputs

- Decision, causal hypothesis, unit, audience, baseline, metrics, constraints, risks, and implementation options.

## Method

1. State falsifiable hypothesis, mechanism, and expected direction.
2. Choose experiment type, assignment unit, control, exposure, and duration.
3. Define primary metric, guardrails, segments, novelty/ramp effects, and instrumentation.
4. Estimate sample/power or justify pilot decision thresholds.
5. Plan SRM, contamination, multiple testing, peeking, missing data, and stopping rules.
6. Define rollout, rollback, ethical constraints, and analysis plan before launch.
7. Specify interpretation for positive, null, mixed, and harmful outcomes.

## Output contract

Produce a compact artifact containing:

- `Experiment design and hypothesis.`
- `Assignment/exposure and metric definitions.`
- `Sample/duration/analysis plan.`
- `Guardrails, stopping, rollout, and decision matrix.`

## Evidence standard

- Do not promise causality from an observational comparison.

## Stop and escalate

- Instrumentation or randomization unit is unreliable.
- Risk cannot be bounded by guardrails.

## Failure modes to avoid

- Changing metrics after seeing results.
- Running an A/B test for an obvious usability defect.
