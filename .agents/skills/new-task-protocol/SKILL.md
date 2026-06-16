---
name: new-task-protocol
description: Start a new task from lightweight runtime memory, propose or create a ticket, select product knowledge, plan bounded discovery, and request approval before edits.
---

# new-task-protocol

Use when the user gives a concrete task and no active task ticket already covers it.

## Inputs

- User task in natural language.
- `CURRENT.md`, `TASK_INDEX.md`, compact `CHRONICLE.md`.
- Product Knowledge if present: `PRODUCT_MAP`, `KNOWLEDGE_INDEX`, relevant area maps.

## Procedure

1. Classify the request: Tiny/Micro/Fast/Standard/Complex/High-risk.
2. Decide whether a new local/current ticket is needed.
3. If substantial, propose a ticket ID, title, scope, out-of-scope, acceptance criteria, and next operation.
4. Load product knowledge only after task relevance is clear.
5. Select relevant roles, skills, playbooks, and gates through `framework-loading`.
6. Propose bounded discovery rather than asking the user to list every file.
7. Produce or request an `Impact Map` before implementation.
8. Ask approval before editing project files, running expensive commands, broad scans, or spawning real subagents.

## Output artifact

- New Task Proposal:
  - ticket ID/title;
  - relevant product area(s);
  - product knowledge to load;
  - bounded discovery plan;
  - proposed roles/skills/gates;
  - approval request.

## Stop conditions

Stop and ask the user if the task scope is unclear, risky, requires broad/external reads, or would modify tracked files.
