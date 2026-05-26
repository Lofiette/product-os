# SUBAGENT_ORCHESTRATION.md

## Critical distinction

Selected role ≠ spawned subagent.
Loaded playbook ≠ spawned subagent.
Consulted role card ≠ spawned subagent.
Only explicit spawn instruction creates a real subagent workflow.

## Orchestration modes

- `main_thread_only`: no role simulation, no subagents.
- `role_simulation`: main thread applies role lenses; no real subagents.
- `true_subagent_workflow`: spawn selected custom agents; wait for results; consolidate.
- `hybrid`: spawn only roles that need independent artifacts; simulate or service the rest.

## Mandatory approval

Before spawning real subagents, present this table and ask approval unless user explicitly requested auto-orchestration:

| Agent | Role | Why spawned | Artifact | Skills | Read/write | Stop condition |
|---|---|---|---|---|---|---|

## Spawn protocol

For each spawned agent:
- use exact `.codex/agents/<role_id>.toml` `name`;
- give bounded task;
- specify files/docs to read;
- specify skills to use;
- specify read/write permission;
- specify output schema;
- specify stop condition;
- require evidence labels.

After spawning:
- wait for all results;
- consolidate conflicts;
- run Consistency Auditor when needed;
- update TASK.md and CHRONICLE.md.
