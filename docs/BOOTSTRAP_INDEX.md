# BOOTSTRAP_INDEX.md — 2.0 beta 1 runtime index

Read this file at startup after `AGENTS.md`, `TASK.md`, `CHRONICLE.md`, `QUESTION_TREE.md`, and `LANGUAGE_POLICY.md`.

## Runtime flow

1. Intake: classify request, complexity, work mode, UI/design-system impact, repo impact, risk impact.
2. If repo exists: propose `repo-recon` before implementation decisions.
3. If UI/design is affected: propose `design-recon` before UI decisions.
4. After intake: load `docs/ROLE_MINI_INDEX.json`, `docs/SKILL_INDEX.json`, and relevant role cards.
5. Propose next operation with roles, skills, orchestration mode, gates, and scripts.
6. Ask approval before spawning real subagents or starting implementation.
7. After approval, explicitly state spawned vs simulated execution.
8. Run selected skills and produce their required artifacts.
9. Apply gates: quality, UI, DS, risk, production, review.
10. Update `TASK.md` and `CHRONICLE.md` compactly when useful.

## UI quality shortcuts

- UI without DS: use `prototype-ui-kit`.
- UI with DS: use `design-system-compliance` and DS scripts.
- Module design for developer rebuild: use `module-design` and `design-handoff-qa`.
- Production web/service: use `phased orchestration` and `production-readiness-review`.
- Implemented UI: use `visual-qa-loop`, `ui-heuristic-audit`, and `Design Diff Summary`.

## Real subagent transparency

Selected role is not a spawned subagent. Spawned subagents must be named explicitly after approval.
