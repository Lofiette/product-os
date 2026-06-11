# Scenario: agent_id_no_personal_names

- **description**: Subagent reporting must use exact agent IDs and ignore UI-generated personal/thread labels
- **max_questions**: 3

## required_roles
- `team_architect`

## required_skills
- `subagent-orchestration`

## forbidden_terms
- `<personal-display-label>`
- `codename`
- `nickname`
- `fictional name`
- `philosopher name`
