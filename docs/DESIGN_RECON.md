# DESIGN_RECON.md

Use for any UI work in an existing repo or when a design system may exist.

## Process

1. Find UI/component directories.
2. Find tokens/theme/style files.
3. Detect framework and styling system.
4. Find Storybook/docs/Figma/design links if present.
5. Find existing screen patterns for the target surface.
6. Find form/list/table/dialog/empty/error patterns.
7. Identify DS mode.
8. Identify forbidden custom UI zones.
9. Build Design Recon Brief.
10. Create/update DESIGN_SYSTEM_MANIFEST.json when useful.

## Output: Design Recon Brief

- DS mode
- DS source of truth
- Component registry
- Token system
- Relevant patterns
- Anti-patterns
- Required docs loaded
- Implementation constraints
- DS compliance gate

## Required authority output

Design Recon must report source authority:

- Did DS docs/component registry/manifest exist before task?
- Was any manifest generated or changed during current task?
- Which sources are authoritative vs candidate/provisional/self-generated?
- Which compliance claims are unproven?

If a reference screenshot exists, Design Recon must hand off to `reference-fidelity`.
