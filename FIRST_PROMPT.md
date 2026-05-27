Read the Codex Product Team 2.0 beta 3 bootstrap instructions.

Load only these files first:
- AGENTS.md
- TASK.md
- CHRONICLE.md
- docs/BOOTSTRAP_INDEX.md
- docs/QUESTION_TREE.md
- docs/LANGUAGE_POLICY.md
- docs/TEAM_CULTURE.md
- docs/AGENT_NAMING_POLICY.md

Start in Intake Mode.

Do not implement yet.
Do not spawn real subagents yet.
Do not load all playbooks or all skills.
Do not assume a design system exists or does not exist.
Do not treat a selected role as a spawned subagent.
Do not assign personal names, fictional names, philosopher names, codenames, or nicknames to agents; report exact agent IDs only.

Your first job:
1. Briefly confirm loaded bootstrap sources.
2. Classify the request if already provided, or ask the smallest useful set of briefing questions.
3. Determine likely complexity tier, work mode, and whether this is design-only, implementation, review, research, or production planning.
4. If the task affects an existing repo, propose `repo-recon` before product or technical decisions.
5. If the task affects UI, propose `design-recon` before UI design or implementation.
6. If the user asks to review a current rendered page or prototype, propose `ui-review-packet` and `current-page-ui-review` before spawning multiple role-specific agents.
7. If no design system is found, propose `prototype-ui-kit` before UI prototyping.
8. If the user asks for a module to be designed for later developer rebuild, use design-only handoff mode and propose `module-design` plus `design-handoff-qa`.
9. If the task is production web/service work, propose phased orchestration and production readiness gates.
10. If the task involves taste, visual feel, UI quality, or examples, propose `taste-calibration`; if good/bad examples exist, propose `example-taste-board`.
11. If the task may benefit from proactive improvements, propose `expectation-anticipation` or `anticipation-radar`, but do not change scope without approval.
12. After intake, load `docs/ROLE_TINY_INDEX.json` or `docs/ROLE_MINI_INDEX.json`, `docs/SKILL_TINY_INDEX.json` or `docs/SKILL_INDEX.json`, and only relevant role cards before proposing a lineup.
13. Propose the next operation with roles, skills, orchestration mode, read/write permissions, gates, and subagent run contract when real spawning is proposed.
14. Clearly separate:
    - roles to spawn as real subagents;
    - roles to simulate in the main thread;
    - system services;
    - skills to load;
    - scripts/checks to run;
    - fallback policy if a spawned agent does not return.
15. Ask for approval before spawning real subagents or starting implementation.
16. After user approval, explicitly state either:
    - `Now spawning real subagents: ...`; or
    - `No real subagents spawned; using role simulation/main thread only.`
17. If any spawned agents are still running or fail, use `subagent-failure-recovery` and report Subagent Completion Status.

Output to the user in Russian. Keep TASK.md/CHRONICLE.md updates in compact English unless I ask otherwise.


## Runtime adequacy reminder

- Use a UI Review Packet before current-page UI review.
- Apply SUBAGENT_FAILURE_POLICY when spawned agents hang, fail, or duplicate.
