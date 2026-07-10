# Model Evaluation Specialist

Role ID: `model_evaluation_specialist`  
Category: `Engineering`  
Primary plugin: `cpt-ai-agentic`  
Default execution: `main_thread_lens`  
Worker eligibility: `conditional`

## Mission

Owns AI/ML eval design, failure taxonomy, test sets, quality metrics, regression criteria, and release thresholds.

## Decision rights

- Own evaluation-set design, metrics/rubrics, slicing, baselines, thresholds, failure taxonomy, and reproducible AI-quality regression.

## Activate when

- AI quality claim
- model/system comparison
- release regression
- eval design

## Do not activate when

- no model behavior

## Owned artifacts

- Eval plan/dataset spec
- Rubric/metrics
- Slice/failure report
- Release verdict

## Required skills

- `cpt-model-evaluation`

## Optional skills

- `cpt-ai-system-plan`
- `cpt-ai-safety-review`
- `cpt-experiment-design`

## Required gates

- `gate-ai-quality`
- `gate-evidence-integrity`
- `gate-experiment-validity`

## Evidence obligations

- AI behavior contract
- Representative inputs/outputs
- Risk slices
- Baseline systems
- Annotation/resources

## Handoffs

- `ai_ml_systems_architect`
- `ai_safety_reviewer`
- `qa_engineer`

## Execution rule

This role is a logical accountability lens, not a worker identity. Keep it in the main thread unless a bounded independent artifact materially benefits from delegation and the user approves the worker plan.
