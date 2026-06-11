# Scenario: current_page_ui_review_bounded

- **description**: Review a currently rendered page without over-spawning role-specific agents
- **max_spawned_agents_default**: 2
- **requires_approval_before_spawn**: True

## required_roles
- `product_designer`
- `design_engineer`
- `design_system_guardian`

## required_skills
- `ui-review-packet`
- `current-page-ui-review`
- `design-system-compliance`
- `taste-review`
