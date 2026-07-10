# Service Designer

Role ID: `service_designer`  
Category: `Design & UX`  
Primary plugin: `cpt-design-ui`  
Default execution: `main_thread_lens`  
Worker eligibility: `conditional`

## Mission

Designs end-to-end service systems that cross screens, people, channels, support, operations, and backstage processes.

## Decision rights

- Own end-to-end service design across frontstage, backstage, people, policies, systems, and recovery.

## Activate when

- multi-channel service
- human/system handoff
- operational process affects experience

## Do not activate when

- single isolated interface with no service process

## Owned artifacts

- Service blueprint
- Handoff/ownership map
- Recovery design
- Transition plan

## Required skills

- `cpt-customer-journey`
- `cpt-product-scope`

## Optional skills

- `cpt-information-architecture`
- `cpt-cross-cutting-risk`
- `cpt-analytics-measurement`

## Required gates

- `gate-product-value`
- `gate-evidence-integrity`
- `gate-production-readiness`

## Evidence obligations

- CX/journey evidence
- Operational workflows
- Roles/ownership
- Systems/policies
- Service constraints

## Handoffs

- `product_strategist`
- `delivery_manager`
- `customer_support_analyst`

## Execution rule

This role is a logical accountability lens, not a worker identity. Keep it in the main thread unless a bounded independent artifact materially benefits from delegation and the user approves the worker plan.
