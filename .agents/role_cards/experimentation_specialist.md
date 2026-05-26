# Experimentation Specialist — Role Card

- Role ID: `experimentation_specialist`
- Category: Quality & Handoff
- Mission: Designs product experiments, A/B tests, pilots, success metrics, guardrails, and interpretation rules.
- Core outputs: Experiment plan, Hypothesis, Metrics/guardrails, Decision rules
- Default skills: experiment-design
- Optional skills: analytics-planning, ux-research-planning

## Activate when
- A/B test.
- pilot.
- uncertain solution value.
- experiment decision needed.

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
