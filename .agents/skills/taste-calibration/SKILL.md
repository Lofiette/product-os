---
name: taste-calibration
description: Turn user references, adjectives, product context, DS mode, and good/bad examples into a compact Taste Profile and quality bar.
---


# taste-calibration

## Purpose

Calibrate taste before design/product/UI work so decisions are guided by explicit preferences instead of vague “make it good”.

## When to use

- New product/interface concept.
- Redesign or prototype.
- No design system or incomplete design system.
- User provides adjectives, references, good/bad examples, or asks for better taste.
- Team needs visual/content quality bar before implementation.

Do not use for Tiny/Fast Lane mechanical changes unless user asks.

## Inputs

- TASK.md product context and DS mode.
- docs/TASTE_PROFILE.md.
- User-provided good examples and bad examples.
- Existing product screens / DS docs / brand rules, if available.

## Process

1. Identify whether taste calibration can change the decision.
2. Ask at most 3 missing taste questions if needed.
3. Convert adjectives and examples into operational rules.
4. Separate taste preferences from evidence.
5. Define anti-taste: what must not be produced.
6. Add or update TASK.md taste fields.
7. Define whether `taste-review` is required later.

## Output schema

```markdown
## Taste Calibration

### Taste profile source
user-provided / inferred from DS / default / mixed

### Desired feel

### Product adjectives

### Good examples
| Example | What to borrow | What not to copy |
|---|---|---|

### Bad examples / anti-examples
| Example | What to avoid | Why it hurts |
|---|---|---|

### Operational taste rules

### Anti-taste rules

### Quality bar

### Required follow-up
```

## BLOCKED conditions

- Design direction depends on taste but no taste profile or default was accepted.
- User-provided bad examples are ignored in the proposed design direction.
