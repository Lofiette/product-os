# PROTOTYPE_UI_KIT.md

Use when a UI prototype is requested and no design system exists.

## Purpose

Prevent fast prototypes from becoming inconsistent visual soup. This is not a full design system. It is a small local UI contract for the current prototype.

## Required output: Prototype UI Kit Contract

```markdown
# Prototype UI Kit Contract

## 1. Product/prototype tone
## 2. Typography scale
## 3. Spacing scale
## 4. Color roles
| Role | Value | Usage |
## 5. Radius/shadow/density rules
## 6. Core components
| Component | Anatomy | Variants | States |
## 7. Layout patterns
## 8. Empty/error/loading/success patterns
## 9. Responsive assumptions
## 10. Do-not-create rules
## 11. Allowed deviations
```

## Gate

If no DS exists, a UI prototype must either use this contract or explicitly state that visual consistency is out of scope.
