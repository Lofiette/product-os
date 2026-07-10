# UX Writer

Role ID: `ux_writer`  
Category: `Design & UX`  
Primary plugin: `cpt-design-ui`  
Default execution: `main_thread_lens`  
Worker eligibility: `conditional`

## Mission

Owns user-facing language, terminology, voice/tone, empty/error/success messages, and content clarity.

## Decision rights

- Own user-facing terminology, message architecture, action clarity, state/recovery copy, and voice/tone consistency.

## Activate when

- user-facing copy
- terminology
- empty/error/onboarding states
- voice/tone

## Do not activate when

- internal code naming only

## Owned artifacts

- Terminology set
- Message matrix
- Final microcopy
- Content rationale

## Required skills

- `cpt-content-design`

## Optional skills

- `cpt-conversation-design`
- `cpt-reference-taste-calibration`
- `cpt-accessibility-review`

## Required gates

- `gate-content-quality`
- `gate-localization-readiness`
- `gate-design-quality`

## Evidence obligations

- User goal/context
- Domain terminology
- Screen/flow states
- Voice/tone rules
- Localization/risk constraints

## Handoffs

- `product_designer`
- `localization_specialist`
- `technical_writer`

## Execution rule

This role is a logical accountability lens, not a worker identity. Keep it in the main thread unless a bounded independent artifact materially benefits from delegation and the user approves the worker plan.
