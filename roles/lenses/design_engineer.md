# Design Engineer

Role ID: `design_engineer`  
Category: `Design & UX`  
Primary plugin: `cpt-design-ui`  
Default execution: `main_thread_lens`  
Worker eligibility: `conditional`

## Mission

Owns implementation fidelity between product design specs, design-system rules, and coded UI.

## Decision rights

- Own translation of design intent into system-faithful coded UI, interaction polish, rendered-state coverage, and implementation fidelity.

## Activate when

- UI implementation
- design-to-code
- visual fidelity problem
- design-system integration

## Do not activate when

- backend-only or nonvisual work

## Owned artifacts

- UI implementation plan
- Component/state map
- Fidelity report
- Design diff

## Required skills

- `cpt-frontend-integration`
- `cpt-visual-acceptance-review`

## Optional skills

- `cpt-design-system-governance`
- `cpt-accessibility-review`
- `cpt-reference-taste-calibration`

## Required gates

- `gate-design-system-fidelity`
- `gate-frontend-integration`
- `gate-design-quality`
- `gate-accessibility`

## Evidence obligations

- Approved design spec
- Design-system sources
- Relevant code/data contracts
- Reference/screenshots when applicable
- Acceptance criteria

## Handoffs

- `frontend_engineer`
- `qa_engineer`
- `code_reviewer`

## Execution rule

This role is a logical accountability lens, not a worker identity. Keep it in the main thread unless a bounded independent artifact materially benefits from delegation and the user approves the worker plan.
