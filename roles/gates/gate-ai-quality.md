# AI Quality Gate

Gate ID: `gate-ai-quality`

## Apply when

For model behavior, retrieval, classification, generation, ranking, or agent quality.

## Owners

- `model_evaluation_specialist`
- `ai_ml_systems_architect`

## PASS criteria

- Behavior contract, evaluation set, metrics/rubrics, slices, baseline, threshold, and regression plan are explicit.
- Uncertainty and fallback are handled.

## BLOCK criteria

- A few demos are treated as sufficient evaluation.
- Critical slices or failure classes are absent.
- Quality cannot be reproduced.

## Required evidence

- Eval dataset/version
- Metrics/rubric
- Baseline comparison
- Failure taxonomy

## Verdict contract

- `PASS`: required evidence supports the acceptance claim.
- `PASS_WITH_WARNINGS`: acceptance is supportable, with explicit non-blocking residual risk.
- `BLOCKED`: one or more blocking conditions are present.
- `INSUFFICIENT_EVIDENCE`: the gate cannot responsibly decide.

A warning must never hide a blocker. Missing evidence must never be converted into a clean pass.
