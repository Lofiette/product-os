# DESIGN_SOURCE_AUTHORITY.md

Design quality checks require trustworthy sources. This document defines authority levels and prevents self-validating design artifacts.

## Source hierarchy

Use higher sources before lower sources:

1. User-provided current design-system documentation.
2. Existing code component library and token/theme files.
3. Storybook/component examples and visual regression snapshots.
4. Existing production screens in the same product.
5. User-provided reference screenshots or good/bad examples.
6. Generated `Prototype UI Kit Contract` for no-DS prototypes.
7. Model assumptions.

## Critical rule

Generated artifacts cannot validate themselves.

Examples:
- A `DESIGN_SYSTEM_MANIFEST.json` generated during the current task cannot prove that the current UI is DS-compliant.
- A component registry created after implementation cannot prove component choice was correct.
- A prototype UI kit generated from the finished UI cannot prove the prototype is coherent.

## Manifest authority states

- `authoritative`: existed before task or user explicitly approved it as source of truth.
- `candidate`: generated from discovered DS sources before implementation, not yet approved.
- `provisional`: generated because no DS exists; usable only as a prototype constraint.
- `self_generated`: created or materially changed during the same implementation; cannot be used as proof.

## Required report

Any UI/design task using DS compliance must report:

| Source | Authority | Used for | Evidence | Limitation |
|---|---|---|---|---|

## Blocking conditions

`BLOCKED` if:
- DS compliance is claimed against a self-generated manifest;
- custom UI is introduced while an authoritative component exists and no deviation was approved;
- reference screenshot exists but no reference-fidelity comparison was performed;
- design-system source is unknown and implementation proceeds as if strict DS compliance is proven.
