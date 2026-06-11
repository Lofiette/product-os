# Scenario: context_prune_after_long_work

- **description**: After long work or frequent context compression, memory should be pruned into CURRENT, active ticket, compact CHRONICLE, and archive logs.
- **max_questions**: 3

## required_roles
- `chronicle_keeper`

## required_skills
- `context-snapshot`
- `context-prune`
- `memory-integrity-check`
