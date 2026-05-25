---
name: design-ux-planning
description: Use for UI, interaction, UX writing, visual, design system, accessibility, or localization work.
---

# Skill: design-ux-planning

## When to use
Use for UI, interaction, UX writing, visual, design system, accessibility, or localization work.

## Procedure
1. Map primary and secondary flows.
2. Build a state matrix: empty, loading, success, error, disabled, partial, permission, offline if relevant.
3. Define content requirements: labels, CTAs, empty/error/success messages, confirmations, helper text.
4. Check design-system fit: existing components, tokens, patterns, variants, responsive rules.
5. Check accessibility: semantics, focus, keyboard, labels, dynamic state announcements, contrast assumptions.
6. Check localization/product language rules from LANGUAGE_POLICY.md and TASK.md.
7. Produce UX acceptance criteria and handoffs to Frontend, QA, UX Writer, Accessibility, Design System.

## Output rules
- Use evidence labels from `docs/EVIDENCE_POLICY.md`.
- Respect `docs/QUALITY_GATES.md` and `docs/RISK_POLICY.md`.
- Follow `docs/LANGUAGE_POLICY.md`.
- Update `TASK.md` and/or `CHRONICLE.md` only when the procedure calls for it.
- Do not implement unless the approved work mode and approval gate allow implementation.


## Complexity guardrail

Before executing this skill, classify the task tier with `docs/COMPLEXITY_MODEL.md`. Use the smallest role set and shortest artifact that can safely support the next decision.

## Output schema rule

Use `docs/ROLE_OUTPUT_SCHEMAS.md` for role outputs. If this skill needs a stricter schema, state it before producing recommendations.
