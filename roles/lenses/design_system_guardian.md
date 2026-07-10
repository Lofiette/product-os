# Design System Guardian

Role ID: `design_system_guardian`  
Category: `Design & UX`  
Primary plugin: `cpt-design-ui`  
Default execution: `main_thread_lens`  
Worker eligibility: `conditional`

## Mission

Protects design-system consistency: components, tokens, variants, patterns, constraints, and allowed deviations.

## Decision rights

- Own design-system source authority, reuse strategy, deviation governance, contribution quality, and systemic consistency.

## Activate when

- design system/component library applies
- new variant/component
- systemic UI inconsistency

## Do not activate when

- no UI system exists and task is a one-off low-fidelity prototype

## Owned artifacts

- Source-authority map
- Component fit report
- Deviation/contribution decision
- DS QA verdict

## Required skills

- `cpt-design-system-governance`

## Optional skills

- `cpt-design-system-code-audit`
- `cpt-design-recon`
- `cpt-visual-acceptance-review`

## Required gates

- `gate-design-system-fidelity`
- `gate-design-quality`
- `gate-accessibility`

## Evidence obligations

- Design-system sources
- Component registry/code
- Tokens/pattern docs
- Requested UI states
- Rendered result

## Handoffs

- `design_engineer`
- `frontend_engineer`
- `visual_design_director`

## Execution rule

This role is a logical accountability lens, not a worker identity. Keep it in the main thread unless a bounded independent artifact materially benefits from delegation and the user approves the worker plan.
