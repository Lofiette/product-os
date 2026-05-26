Read the Codex Product Team 2.0 bootstrap instructions.

Load only these files first:
- AGENTS.md
- TASK.md
- CHRONICLE.md
- docs/BOOTSTRAP_INDEX.md
- docs/QUESTION_TREE.md
- docs/LANGUAGE_POLICY.md

Start in Intake Mode.

Do not implement yet.
Do not spawn real subagents yet.
Do not load all playbooks or all skills.
Do not assume a design system exists or does not exist.

Your first job:
1. Briefly confirm loaded bootstrap sources.
2. Classify the request if already provided, or ask the smallest useful set of briefing questions.
3. Determine likely complexity tier and work mode.
4. If the task may affect UI, identify whether design-recon will be required.
5. Propose the next operation.
6. Propose roles, skills, and orchestration mode for that next operation.
7. Clearly separate:
   - roles to spawn as real subagents;
   - roles to simulate in the main thread;
   - system services;
   - skills to load.
8. Ask for approval before spawning real subagents or starting implementation.

Output in Russian. Keep TASK.md/CHRONICLE.md updates in compact English unless I ask otherwise.
