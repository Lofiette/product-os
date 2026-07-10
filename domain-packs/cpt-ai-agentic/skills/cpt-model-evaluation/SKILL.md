---
name: cpt-model-evaluation
description: Use to build AI evaluation matrices, cases, rubrics, thresholds, failure taxonomy, and regression criteria.
---

# CPT Model Evaluation

## Use when

- AI/model behavior must be selected, verified, monitored, or protected from regression.

## Do not use when

- The task has no probabilistic model output.

## Required inputs

- Behavior contract, users/tasks, model/prompt/retrieval variants, known failures, risk level, datasets, human-review budget, and deployment decision.

## Method

1. Translate behavior contract into dimensions: correctness, usefulness, faithfulness, safety, style, latency, cost, and tool success.
2. Create representative, edge, adversarial, multilingual, long-context, and historical-regression cases.
3. Define expected outputs, rubrics, graders, inter-rater calibration, and pass thresholds.
4. Separate offline component evals, end-to-end task evals, and online monitoring.
5. Design failure taxonomy and slice metrics by user/task/data conditions.
6. Control leakage, contamination, nondeterminism, judge bias, and repeated-run variance.
7. Define release gate, regression policy, and investigation workflow.

## Output contract

Produce a compact artifact containing:

- `Eval matrix and dataset/case plan.`
- `Rubrics, graders, thresholds, and slices.`
- `Failure taxonomy and regression suite.`
- `Results/decision rules and monitoring handoff.`

## Evidence standard

- A single average score cannot hide critical slice failures.

## Stop and escalate

- No behavior contract or release decision exists.
- Evaluation data violates privacy or leakage constraints.

## Failure modes to avoid

- Using only happy-path examples.
- Letting one model grade its own outputs without calibration.
