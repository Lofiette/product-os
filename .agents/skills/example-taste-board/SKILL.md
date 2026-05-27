---
name: example-taste-board
description: Capture good and bad examples as reusable taste evidence and convert them into design rules and anti-patterns.
---


# example-taste-board

## Purpose

Turn good/bad examples into concrete design rules. This prevents “taste” from staying abstract.

## When to use

- User provides references, screenshots, links, previous screens, or verbal examples.
- Project has no DS or an incomplete DS.
- Redesign/concept work needs a quality bar.
- Team disagrees about what “good” means.

## Process

1. List good examples and bad examples separately.
2. For each good example, extract transferable qualities, not surface copying.
3. For each bad example, extract anti-patterns and user/product harm.
4. Map examples to UI, content, DS, density, hierarchy, motion, and state rules.
5. Mark what is evidence, taste preference, or hypothesis.
6. Feed results into `taste-calibration` or `taste-review`.

## Output schema

```markdown
## Example Taste Board

### Good examples
| Example | Transferable quality | Boundary / do not copy | Related rule |
|---|---|---|---|

### Bad examples
| Example | Anti-pattern | Why harmful | Avoidance rule |
|---|---|---|---|

### Derived taste rules

### Derived anti-taste rules

### Open taste questions
```

## Stop conditions

- Examples are not available and the user does not want default taste.
- Applying an example would conflict with DS constraints or product context.
