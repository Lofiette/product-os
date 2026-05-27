# Scenario: agent_id_no_personal_names

Description: Subagent reporting must use exact agent IDs and ignore UI-generated personal/thread labels

Required roles: team_architect

Optional roles: none

Required skills: subagent-orchestration

Expected behavior:
- Use staged loading.
- Propose roles, skills, orchestration mode, and gates before execution.
- Ask approval before real subagent spawn or scope-changing proposals.
- Produce compact artifacts and gate verdicts.
