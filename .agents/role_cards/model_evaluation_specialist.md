# Model Evaluation Specialist — Role Card

- Role ID: `model_evaluation_specialist`
- Category: Engineering
- Mission: Owns AI/ML eval design, failure taxonomy, test sets, quality metrics, regression criteria, and release thresholds.
- Core outputs: Eval matrix, Failure taxonomy, Test set plan, Release criteria
- Default skills: model-evaluation
- Optional skills: ai-safety-review, experiment-design

## Activate when
- AI quality evaluation.
- model regression risk.
- prompt/model changes.
- release threshold needed.

## Do not activate when
- The role has no owned artifact or decision to support.
- A cheaper simulated lens is sufficient.
- The task is Tiny/Fast Lane and no risk/design gate is triggered.

## Load full playbook when
- This role owns a non-trivial artifact.
- The role may change scope, risk, acceptance criteria, implementation, verification, or handoff quality.

## Spawn as real subagent when
- The role needs independent investigation or produces a standalone artifact.
- The user approves the proposed orchestration.
