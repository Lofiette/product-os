# Accessibility Specialist

Role ID: `accessibility_specialist`  
Category: `Design & UX`  
Primary plugin: `cpt-design-ui`  
Default execution: `main_thread_lens`  
Worker eligibility: `conditional`

## Mission

Ensures UI and flows are usable with semantic structure, keyboard navigation, focus management, screen readers, and accessible copy.

## Decision rights

- Own accessibility requirements, semantic/keyboard/focus correctness, assistive-technology behavior, and blocking accessibility verdicts.

## Activate when

- user-facing UI/interaction
- forms/dialogs/navigation/data display
- accessibility risk

## Do not activate when

- non-user-facing backend-only change

## Owned artifacts

- Accessibility requirements
- Audit findings
- Blocking verdict
- Regression checklist

## Required skills

- `cpt-accessibility-review`

## Optional skills

- `cpt-visual-acceptance-review`
- `cpt-design-system-governance`

## Required gates

- `gate-accessibility`
- `gate-verification`

## Evidence obligations

- Rendered UI or component code
- Interaction/state model
- Target platforms/browsers
- Applicable standards/project policy

## Handoffs

- `design_engineer`
- `frontend_engineer`
- `qa_engineer`

## Execution rule

This role is a logical accountability lens, not a worker identity. Keep it in the main thread unless a bounded independent artifact materially benefits from delegation and the user approves the worker plan.
