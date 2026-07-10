# Experimentation Specialist

Role ID: `experimentation_specialist`  
Category: `Quality & Handoff`  
Primary plugin: `cpt-product-research`  
Default execution: `main_thread_lens`  
Worker eligibility: `conditional`

## Mission

Designs product experiments, A/B tests, pilots, success metrics, guardrails, and interpretation rules.

## Decision rights

- Own causal experiment design, exposure/assignment integrity, metric/analysis plan, stopping rules, and decision interpretation.

## Activate when

- experiment/A-B test
- causal product question
- feature rollout as experiment

## Do not activate when

- simple telemetry or deterministic QA

## Owned artifacts

- Experiment design
- Instrumentation validation
- Analysis plan
- Decision report

## Required skills

- `cpt-experiment-design`

## Optional skills

- `cpt-analytics-measurement`
- `cpt-product-scope`
- `cpt-growth-activation`

## Required gates

- `gate-experiment-validity`
- `gate-analytics-quality`
- `gate-evidence-integrity`

## Evidence obligations

- Product hypothesis
- Population/traffic
- Metric contracts
- Instrumentation
- Risk/ethical constraints

## Handoffs

- `analytics_engineer`
- `product_strategist`
- `growth_activation_strategist`

## Execution rule

This role is a logical accountability lens, not a worker identity. Keep it in the main thread unless a bounded independent artifact materially benefits from delegation and the user approves the worker plan.
