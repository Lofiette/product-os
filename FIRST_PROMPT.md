Read the Codex Product Team 2.0 beta 1 bootstrap instructions.

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
Do not treat a selected role as a spawned subagent.

Your first job:
1. Briefly confirm loaded bootstrap sources.
2. Classify the request if already provided, or ask the smallest useful set of briefing questions.
3. Determine likely complexity tier, work mode, and whether this is design-only, implementation, review, research, or production planning.
4. If the task affects an existing repo, propose `repo-recon` before product or technical decisions.
5. If the task affects UI, propose `design-recon` before UI design or implementation.
6. If no design system is found, propose `prototype-ui-kit` before UI prototyping.
7. If the user asks for a module to be designed for later developer rebuild, use design-only handoff mode and propose `module-design` plus `design-handoff-qa`.
8. If the task is production web/service work, propose phased orchestration and production readiness gates.
9. After intake, load `docs/ROLE_MINI_INDEX.json`, `docs/SKILL_INDEX.json`, and only relevant role cards before proposing a lineup.
10. Propose the next operation with roles, skills, orchestration mode, read/write permissions, and gates.
11. Clearly separate:
    - roles to spawn as real subagents;
    - roles to simulate in the main thread;
    - system services;
    - skills to load;
    - scripts/checks to run.
12. Ask for approval before spawning real subagents or starting implementation.
13. After user approval, explicitly state either:
    - `Now spawning real subagents: ...`; or
    - `No real subagents spawned; using role simulation/main thread only.`

Output to the user in Russian. Keep TASK.md/CHRONICLE.md updates in compact English unless I ask otherwise.
