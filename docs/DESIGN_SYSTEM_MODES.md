# DESIGN_SYSTEM_MODES.md

Design system may be absent or highly formal. Do not assume.

## Modes

### none
No reusable components/tokens found. Create lightweight local UI rules and a small component plan before implementation.

### emerging
Some reusable components or style conventions exist, but no formal registry. Document discovered conventions in Design Recon Brief.

### component_library
Reusable components exist in code. Use them. Custom equivalents are blocked unless approved.

### documented_ds
Components plus docs/instructions exist. Load relevant DS docs, not the whole folder unless needed.

### governed_ds
Formal DS folder, tokens, specs, registry, Storybook/Figma links, or contribution rules exist. DS compliance is blocking.

## Design-system folder handling

If user provides or repo contains a DS folder:
1. Locate entry docs/index/README.
2. Identify component registry, token rules, patterns, anti-patterns, contribution rules.
3. Load only relevant component/pattern docs for the current task.
4. Update or create `docs/design-system/DESIGN_SYSTEM_MANIFEST.json`.
5. Record loaded DS docs in TASK.md context budget.

## No DS handling

If no DS exists:
- Product Designer defines lightweight screen spec.
- Design Engineer creates minimal component structure only as needed.
- Design System Guardian may create a lightweight manifest for local consistency.
- Avoid overbuilding a DS for a prototype.
