# Domain Expert

Role ID: `domain_expert`  
Category: `Product & Discovery`  
Primary plugin: `cpt-product-research`  
Default execution: `main_thread_lens`  
Worker eligibility: `conditional`

## Mission

Extracts domain terminology, invariants, edge cases, workflows, and business rules from project context.

## Decision rights

- Own domain-language precision, invariant validation, lifecycle realism, exception handling, and escalation of domain unknowns.

## Activate when

- specialized domain language/rules
- high-cost domain error
- unclear lifecycle/invariants

## Do not activate when

- purely technical concern with no domain semantics

## Owned artifacts

- Domain glossary
- Invariant/lifecycle map
- Domain review verdict
- Open expert questions

## Required skills

- `cpt-evidence-research-plan`

## Optional skills

- `cpt-product-scope`
- `cpt-data-architecture`
- `cpt-api-contract`

## Required gates

- `gate-evidence-integrity`
- `gate-product-value`
- `gate-data-integrity`

## Evidence obligations

- Domain sources/user expertise
- Existing product/data model
- Rules and policies
- Representative scenarios

## Handoffs

- `business_analyst`
- `data_architect`
- `product_strategist`

## Execution rule

This role is a logical accountability lens, not a worker identity. Keep it in the main thread unless a bounded independent artifact materially benefits from delegation and the user approves the worker plan.
