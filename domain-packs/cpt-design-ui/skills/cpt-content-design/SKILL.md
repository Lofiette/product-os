---
name: cpt-content-design
description: Use to design or review UX copy, terminology, messages, content realism, and localization readiness; not for brand campaigns.
---

# CPT Content Design

## Use when

- User-facing labels, instructions, CTA, errors, empty states, success, confirmation, or realistic prototype content matter.

## Do not use when

- The task is long-form marketing content.
- No user-facing language changes or content risks exist.

## Required inputs

- User intent, product terminology, flow/state matrix, voice/tone, audience, localization requirements, and constraints.

## Method

1. Define content goal, user question, action, and required information at each state.
2. Establish terminology and object/action naming; resolve synonyms and internal jargon.
3. Write labels, CTA, guidance, empty/error/success/confirmation/destructive messages with recovery.
4. Check brevity, specificity, blame, trust, accessibility, and consistency.
5. Use realistic data/content to test hierarchy, length, edge cases, and comprehension.
6. Check variables, pluralization, formats, text expansion, locale assumptions, and hardcoded strings.
7. Create message/content matrix and flag unresolved product behavior.

## Output contract

Produce a compact artifact containing:

- `Terminology and content rules.`
- `Message/content matrix by state.`
- `Realism and localization findings.`
- `Final copy, alternatives, and open decisions.`

## Evidence standard

- Content cannot hide missing product behavior or recovery.

## Stop and escalate

- The underlying action/state is undefined.
- Legal/compliance language requires qualified review.

## Failure modes to avoid

- Using “Something went wrong” when recovery is known.
- Exposing internal identifiers to users.
