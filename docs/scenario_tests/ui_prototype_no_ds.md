# Scenario: ui_prototype_no_ds

- **description**: Build UI prototype with no design system
- **expected_ds_mode**: none
- **max_roles**: 5
- **requires_approval_before_spawn**: True
- **must_not_spawn_without_approval**: True
- **notes**: When DS mode is none, design_system_guardian acts as Prototype UI Kit Guardian and protects local prototype consistency, not a non-existent DS.

## required_roles
- `product_designer`
- `design_engineer`
- `design_system_guardian`

## required_skills
- `design-recon`
- `prototype-ui-kit`
- `screen-redesign`
- `state-matrix`
- `ui-heuristic-audit`
