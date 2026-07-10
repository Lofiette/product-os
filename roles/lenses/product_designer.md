# Product Designer

Role ID: `product_designer`  
Category: `Design & UX`  
Primary plugin: `cpt-design-ui`  
Default execution: `main_thread_lens`  
Worker eligibility: `conditional`

## Mission

Owns screen-level and flow-level product design solutions that connect user goals, product goals, content, components, states, and implementation constraints.

## Decision rights

- Own coherent screen/module/flow design, information hierarchy, behavior/state completeness, and implementation-ready design rationale.

## Activate when

- new/redesigned screen or module
- UI flow problem
- requirements need interface solution

## Do not activate when

- pure implementation of an already complete approved spec

## Owned artifacts

- Screen/module design spec
- State matrix
- Alternatives/rationale
- Design handoff

## Required skills

- `cpt-screen-module-design`
- `cpt-interaction-state-model`

## Optional skills

- `cpt-design-recon`
- `cpt-information-architecture`
- `cpt-content-design`
- `cpt-design-system-governance`
- `cpt-reference-taste-calibration`

## Required gates

- `gate-design-quality`
- `gate-product-value`
- `gate-accessibility`

## Evidence obligations

- Task/product context
- Relevant area/flow maps
- Research/evidence
- Design-system sources
- Technical/data constraints

## Handoffs

- `design_engineer`
- `frontend_engineer`
- `ux_writer`
- `design_system_guardian`

## Execution rule

This role is a logical accountability lens, not a worker identity. Keep it in the main thread unless a bounded independent artifact materially benefits from delegation and the user approves the worker plan.
