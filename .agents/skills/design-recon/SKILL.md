---
name: design-recon
description: Discover design-system mode, component registry, tokens, style conventions, UI patterns, DS docs/folders, Storybook/Figma links, and implementation constraints.
---


# design-recon

## Purpose

Identify what design rules already exist before any UI design or implementation.

## Required inputs

- Repo Recon Brief, if an existing repo is present.
- Any DS folder, component library, Storybook, Figma links, UI docs, token files, theme files.
- Current task and UI surface.

## Procedure

1. Locate UI component directories and shared primitives.
2. Locate token/theme/style sources: CSS variables, Tailwind config, theme files, design tokens, style dictionaries.
3. Locate DS docs/instructions: `docs/design-system`, Storybook, README, MDX, Figma/design references.
4. Classify DS mode: `none`, `emerging`, `component_library`, `documented_ds`, `governed_ds`.
5. Build or update a component registry from evidence.
6. Identify patterns for forms, settings, lists, tables, dialogs, empty states, errors, navigation, dashboards.
7. Identify anti-patterns and local deviations.
8. Record compliance gate severity.

## Output schema

```markdown
## Design Recon Brief

### DS mode
none / emerging / component_library / documented_ds / governed_ds

### DS source of truth

### Component registry
| Need | Component/pattern | Source | Notes |
|---|---|---|---|

### Token system

### Existing UI patterns

### Anti-patterns / deviations observed

### Relevant screens/components to inspect

### Required compliance gate

### Recommended next roles/skills
```

## BLOCKED conditions

- UI implementation requested in an existing repo but DS mode cannot be determined.
- A governed/documented DS exists but relevant DS docs are ignored.

## Stop conditions

- Required evidence is missing and the next step would require guessing.
- The skill would change approved scope.
- A risk gate requires user approval.
- Another role owns the decision and has not been consulted.

