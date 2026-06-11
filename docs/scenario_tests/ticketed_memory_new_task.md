# Scenario: ticketed_memory_new_task

- **description**: A new multi-step task should create or update a ticket instead of expanding TASK.md.
- **max_questions**: 7

## required_roles
- `intake_orchestrator`
- `team_architect`

## required_skills
- `ticket-router`
- `task-ledger`
- `task-intake`

## forbidden_files_to_update_as_working_memory
- `TASK.md`
