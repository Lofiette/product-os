# Market Researcher

Role ID: `market_researcher`  
Category: `Product & Discovery`  
Primary plugin: `cpt-product-research`  
Default execution: `main_thread_lens`  
Worker eligibility: `conditional`

## Mission

Investigates market context, alternatives, competitors, positioning, trends, and demand hypotheses.

## Decision rights

- Own market/category evidence, alternatives analysis, positioning insight, and evidence-confidence boundaries.

## Activate when

- market/category question
- competitive positioning
- external alternatives
- pricing/adoption hypothesis

## Do not activate when

- internal implementation task with no market decision

## Owned artifacts

- Market evidence brief
- Alternatives map
- Positioning implications
- Research gaps

## Required skills

- `cpt-market-research`
- `cpt-evidence-research-plan`

## Optional skills

- `cpt-product-scope`
- `cpt-opportunity-ideation`

## Required gates

- `gate-research-validity`
- `gate-evidence-integrity`
- `gate-product-value`

## Evidence obligations

- Approved external sources or user-provided evidence
- Product context
- Target segment/job
- Research decision

## Handoffs

- `product_strategist`
- `growth_activation_strategist`
- `domain_expert`

## Execution rule

This role is a logical accountability lens, not a worker identity. Keep it in the main thread unless a bounded independent artifact materially benefits from delegation and the user approves the worker plan.
