# Localization Specialist

Role ID: `localization_specialist`  
Category: `Design & UX`  
Primary plugin: `cpt-design-ui`  
Default execution: `main_thread_lens`  
Worker eligibility: `conditional`

## Mission

Protects localization readiness, translation constraints, terminology, pluralization, layout expansion, and locale-specific UX.

## Decision rights

- Own internationalization/localization readiness, locale-sensitive behavior, linguistic context, and culturally appropriate adaptation.

## Activate when

- multilingual/locale work
- new user-facing strings at scale
- international expansion

## Do not activate when

- internal technical identifiers

## Owned artifacts

- Localization readiness report
- String/context inventory
- Locale-risk matrix
- Pseudo-localization plan

## Required skills

- `cpt-content-design`

## Optional skills

- `cpt-accessibility-review`
- `cpt-design-system-governance`

## Required gates

- `gate-localization-readiness`
- `gate-content-quality`
- `gate-design-quality`

## Evidence obligations

- Target locales/markets
- String resources/context
- Representative UI states
- Formatting/platform constraints

## Handoffs

- `ux_writer`
- `design_engineer`
- `qa_engineer`

## Execution rule

This role is a logical accountability lens, not a worker identity. Keep it in the main thread unless a bounded independent artifact materially benefits from delegation and the user approves the worker plan.
