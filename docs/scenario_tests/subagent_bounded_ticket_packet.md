# Scenario: subagent_bounded_ticket_packet

- **description**: Spawned subagents should receive the active ticket and operation packet, not all project memory.
- **max_questions**: 3

## required_roles
- `team_architect`

## required_skills
- `subagent-run-contract`
- `ui-review-packet`
- `ticket-router`

## must_not_load
- `archive/*`
- `chronicle/*`
- `all tickets`
