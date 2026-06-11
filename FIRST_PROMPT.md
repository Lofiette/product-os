Read the Codex Product Team 2.1 beta 4 bootstrap instructions.

Load only these Tier 0 files first:
- AGENTS.md
- CURRENT.md
- TASK_INDEX.md
- CHRONICLE.md
- docs/BOOTSTRAP_INDEX.md
- docs/LANGUAGE_POLICY.md

Do not load all tickets, archive logs, old snapshots, all playbooks, all skills, full role indexes, release notes, self-audit reports, or reference-only docs.
Do not use TASK.md as working memory; it is a deprecated compatibility pointer.
Do not rely on implicit skill discovery for critical workflows. If needed, load `docs/SKILL_DISCOVERY_POLICY.md` after Tier 0 and before selecting UI/design/runtime-critical skills.

Start in Intake Mode.

Do not implement yet.
Do not spawn real subagents yet.
Do not assume a design system exists or does not exist.
Do not treat a selected role as a spawned subagent.
Do not assign personal names, fictional names, philosopher names, codenames, or nicknames to agents; report exact agent IDs only.

Your first job:
1. Confirm loaded Tier 0 bootstrap sources.
2. Read `CURRENT.md` and identify the active ticket.
3. Decide whether to continue the active ticket, create a new ticket, resume from a snapshot, or run `context-prune`.
4. If new work is requested, use `ticket-router` and `task-ledger` to route it into an active ticket before planning.
5. Load only the active ticket and operation-relevant docs/skills.
6. If intake requires more structured questions, load `docs/QUESTION_TREE.md`; otherwise ask only decision-changing questions.
7. Classify the request: complexity tier, work mode, design-only vs implementation vs review vs research vs production planning.
8. If the task affects an existing repo, propose `repo-recon` before product or technical decisions.
9. If the task affects UI, propose `design-recon` before UI design or implementation.
10. If the user asks to review a current rendered page or prototype, propose `ui-review-packet` and `current-page-ui-review` before spawning multiple role-specific agents.
11. If no design system is found, propose `prototype-ui-kit` before UI prototyping.
12. If the user asks for a module to be designed for later developer rebuild, use design-only handoff mode and propose `module-design` plus `design-handoff-qa`.
13. If the task is production web/service work, propose phased orchestration and production readiness gates.
14. If the task involves taste, visual feel, UI quality, or examples, propose `taste-calibration`; if good/bad examples exist, propose `example-taste-board`.
15. If the user provides a visual reference, screenshot, good example, or bad example, propose `reference-fidelity` and `design-source-authority`; if UI is implemented or rendered, propose `screenshot-reference-comparison`.
16. If prototype/demo content is generated, propose `content-realism-review`; if debug/prototype controls are visible, propose `debug-control-review`.
17. If the task may benefit from proactive improvements, propose `expectation-anticipation` or `anticipation-radar`, but do not change scope without approval.
18. After intake, classify the request as `Tiny/Micro`, `Fast Lane`, or `Standard+` before loading indexes. For obvious `Tiny/Micro` work, do not load role/skill indexes by default. For `Fast Lane`, load tiny indexes only if the route is not obvious; if only the domain is unclear, use `docs/SKILL_ROUTER_INDEX.json` first. For `Standard+`, optionally use `docs/SKILL_ROUTER_INDEX.json` for domain routing, then load `docs/ROLE_TINY_INDEX.json` and `docs/SKILL_TINY_INDEX.json` first; load `docs/ROLE_MINI_INDEX.json`, `docs/SKILL_INDEX.json`, and relevant role cards only if the tiny indexes are insufficient.
19. Propose the next operation with roles, skills, orchestration mode, read/write permissions, gates, and a subagent run contract when real spawning is proposed.
20. Clearly separate:
    - roles to spawn as real subagents;
    - roles to simulate in the main thread;
    - system services;
    - skills to load;
    - scripts/checks to run;
    - fallback policy if a spawned agent does not return.
21. Ask for approval before spawning real subagents or starting implementation.
22. After user approval, explicitly state either:
    - `Now spawning real subagents: ...`; or
    - `No real subagents spawned; using role simulation/main thread only.`
23. If any spawned agents are still running or fail, use `subagent-failure-recovery` and report Subagent Completion Status.
24. Before ending a non-trivial phase, update `CURRENT.md`, the active ticket, `TASK_INDEX.md` if needed, and compact `CHRONICLE.md`.
25. If memory grew substantially, propose `context-snapshot` and `context-prune`.

Output to the user in Russian. Keep durable control artifacts in compact English unless I ask otherwise.

Runtime adequacy reminders:
- Use a UI Review Packet before current-page UI review.
- Apply SUBAGENT_FAILURE_POLICY when spawned agents hang, fail, or duplicate.
- Do not convert missing specialist output into PASS.
- If a visual reference or good/bad example exists, do not implement until a Reference Fidelity Spec is created or the user explicitly skips it.
- Do not claim DS compliance using a manifest generated or changed in the same task without explicit approval.

Runtime keyword: TASK.md is only a deprecated compatibility pointer.
Runtime keyword: Generated artifacts cannot validate themselves.
Runtime keyword: Looks similar.


If the user reports repeated context compaction, missing gates, or wrong role/skill execution, suggest creating a diagnostic pack with `bash scripts/export-codex-diagnostics-wsl.sh` from the repo root inside WSL.
