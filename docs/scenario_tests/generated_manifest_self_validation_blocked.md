# Scenario: generated_manifest_self_validation_blocked

- **description**: DS manifest is generated/changed in same task; it cannot be used as proof of DS compliance without approval.
- **max_questions**: 5
- **must_block_self_validating_manifest**: True

## required_roles
- `design_system_guardian`
- `design_engineer`
- `consistency_auditor`

## required_skills
- `design-source-authority`
- `manifest-freeze-check`
- `design-system-compliance`
