---
name: prototype-ui-kit
description: Create a lightweight local UI contract for fast prototypes when no design system exists.
---


# prototype-ui-kit

## Purpose

Keep a fast UI prototype visually coherent when no design system exists. This is a small prototype contract, not a full DS.

## When to use

- UI prototype or concept redesign.
- DS mode is `none` or insufficient for the requested surface.
- The user cares about visual/interface quality.

## Procedure

1. Confirm prototype mode: throwaway, design prototype, or MVP prototype.
2. Define visual/product tone in one sentence.
3. Define a tiny token set: typography, spacing, color roles, radius, density.
4. Define core components: Button, Input, Card, Modal/Dialog, EmptyState, Notice, List/Table pattern as needed.
5. Define state patterns: empty, loading, error, success, disabled.
6. Define do-not-create rules to prevent screen-by-screen drift.
7. Add the contract to the design artifact before implementation.

## Output schema

```markdown
## Prototype UI Kit Contract

### Product/prototype tone
### Typography scale
### Spacing scale
### Color roles
| Role | Value | Usage |
### Radius/shadow/density
### Core components
| Component | Anatomy | Variants | States |
### State patterns
### Responsive assumptions
### Do-not-create rules
### Approved deviations
```

## BLOCKED conditions

- Multiple prototype screens are implemented with no DS and no local UI contract.
- New visual variants are introduced without a reason.

## Stop conditions

- Required evidence is missing and the next step would require guessing.
- The skill would change approved scope.
- A risk gate requires user approval.
- Another role owns the decision and has not been consulted.



## Taste examples requirement

A Prototype UI Kit Contract must include at least 2 good examples and 2 anti-examples for the current task when no design system exists. Examples may be textual if screenshots/references are unavailable.

The contract should make “bad” concrete: raw spacing drift, inconsistent button hierarchy, vague CTAs, decorative empty states, one-off cards, or arbitrary colors.
