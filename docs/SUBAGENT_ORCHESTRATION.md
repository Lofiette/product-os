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


## Agent naming policy

Use exact `.codex/agents/*.toml` `name` values only. Do not invent aliases or display labels such as human names, fictional names, philosopher names, or codenames. If the platform auto-labels threads, map them back to role IDs in summaries.


## Agent naming and UI labels

Use exact `agent_id` / `.codex/agents/<role_id>.toml` `name` values in all reports.

Do not assign personal names, fictional names, philosopher names, codenames, or nicknames to agents. If Codex UI auto-generates thread labels, ignore them in artifacts and summaries. The source of truth is the spawned custom agent name.

Required transparency statement after approval:

```markdown
## Execution transparency
Real subagents spawned: yes/no
Spawned agents by ID: ...
Simulated roles: ...
System services: ...
UI labels ignored: yes, if any appeared
```


## Runtime adequacy patch

Before true subagent workflow, use `docs/SUBAGENT_RUN_CONTRACT.md`. A subagent must receive a bounded task, exact input packet, read/write permission, strict output schema, and stop condition.

For UI/page review, create `UI Review Packet` first. Do not ask multiple role-specific agents to broadly inspect the entire repo or current page without a packet.

If one or more spawned agents remain running or fail to return a usable artifact, apply `docs/SUBAGENT_FAILURE_POLICY.md`. Do not wait indefinitely and do not invent missing specialist results. Proceed with completed agents plus bounded fallback only when quality gates can still be satisfied.

Default max simultaneous spawned reviewers:

- Fast Lane: 0 unless explicitly approved.
- Standard UI review: 1–2.
- Complex/high-risk: 3–5 by phase, not all at once.

Duplicate spawning of the same role is forbidden while an earlier agent for that role is still running unless the user explicitly approves the retry.


## Runtime adequacy reminder

- Report Subagent Completion Status whenever real subagents are used or fail.
