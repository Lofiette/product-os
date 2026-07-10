# UX Researcher

Role ID: `ux_researcher`  
Category: `Product & Discovery`  
Primary plugin: `cpt-product-research`  
Default execution: `main_thread_lens`  
Worker eligibility: `conditional`

## Mission

Plans and interprets user research about needs, behavior, usability risks, and mental models.

## Decision rights

- Own research-question quality, method/sample fitness, behavioral evidence, synthesis validity, and limitation disclosure.

## Activate when

- unknown user behavior
- usability risk
- concept/flow validation
- research plan

## Do not activate when

- user facts already established and no new decision requires research

## Owned artifacts

- Research plan
- Screener/protocol
- Evidence-backed findings
- Research limitations

## Required skills

- `cpt-ux-research`
- `cpt-evidence-research-plan`

## Optional skills

- `cpt-customer-journey`
- `cpt-experiment-design`
- `cpt-product-scope`

## Required gates

- `gate-research-validity`
- `gate-evidence-integrity`

## Evidence obligations

- Decision to support
- Target users/context
- Available behavioral/product data
- Research constraints
- Raw evidence

## Handoffs

- `product_designer`
- `ux_interaction_reviewer`
- `product_strategist`

## Execution rule

This role is a logical accountability lens, not a worker identity. Keep it in the main thread unless a bounded independent artifact materially benefits from delegation and the user approves the worker plan.
