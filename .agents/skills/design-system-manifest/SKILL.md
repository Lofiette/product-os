---
name: design-system-manifest
description: Create or update a compact machine-readable manifest of DS components, tokens, patterns, forbidden raw UI, and approved deviations.
---


# design-system-manifest

## Purpose

Turn DS evidence into a compact contract that Codex and scripts can use.

## Procedure

1. Use design-recon evidence only.
2. Create or update `docs/design-system/DESIGN_SYSTEM_MANIFEST.json` when appropriate.
3. Include component imports, token conventions, pattern docs, forbidden raw UI rules, and approved deviations.
4. Keep uncertain items in `unknowns`, not as facts.
5. Do not invent components that do not exist.

## Output schema

```json
{
  "ds_mode": "none|emerging|component_library|documented_ds|governed_ds",
  "component_imports": { "Button": ["@/components/ui/button"] },
  "tokens": { "spacing": [], "colors": [], "radius": [], "typography": [] },
  "patterns": { "empty_state": "docs/..." },
  "forbidden": {
    "raw_colors": true,
    "arbitrary_px_spacing": true,
    "inline_styles": true,
    "custom_duplicate_components": true
  },
  "approved_deviations": [],
  "unknowns": []
}
```

## BLOCKED conditions

- Governed/documented DS exists but no DS manifest or source-of-truth summary is produced.

## Stop conditions

- Required evidence is missing and the next step would require guessing.
- The skill would change approved scope.
- A risk gate requires user approval.
- Another role owns the decision and has not been consulted.

