# BOOTSTRAP_INDEX.md — 2.0 beta 2 runtime index

Read this file at startup after `AGENTS.md`, `TASK.md`, `CHRONICLE.md`, `QUESTION_TREE.md`, , `LANGUAGE_POLICY.md`, `TEAM_CULTURE.md`, and `AGENT_NAMING_POLICY.md`.

## Runtime flow

1. Intake: classify request, complexity, work mode, UI/design-system impact, repo impact, risk impact, taste impact, and anticipation opportunity.
2. If repo exists: propose `repo-recon` before implementation decisions.
3. If UI/design is affected: propose `design-recon` before UI decisions.
4. If design-facing and taste can change quality: consider `taste-calibration`.
5. If proactive improvement could help: consider `anticipation-radar` but ask approval before scope changes.
6. After intake: load `docs/ROLE_MINI_INDEX.json`, `docs/SKILL_INDEX.json`, and relevant role cards.
7. Propose next operation with roles, skills, orchestration mode, gates, and scripts.
8. Ask approval before spawning real subagents or starting implementation.
9. After approval, explicitly state spawned vs simulated execution.
10. Run selected skills and produce their required artifacts.
11. Apply gates: quality, UI, DS, risk, production, review.
12. Update `TASK.md` and `CHRONICLE.md` compactly when useful.

## UI quality shortcuts

- UI without DS: use `prototype-ui-kit`.
- UI with DS: use `design-system-compliance` and DS scripts.
- Module design for developer rebuild: use `module-design` and `design-handoff-qa`.
- Production web/service: use `phased orchestration` and `production-readiness-review`.
- Implemented UI: use `visual-qa-loop`, `ui-heuristic-audit`, and `Design Diff Summary`.

## Real subagent transparency

Selected role is not a spawned subagent. Spawned subagents must be named explicitly after approval.


## Taste and anticipation shortcuts

- New/redesigned interface: consider `taste-calibration` before design decisions.
- Implemented UI: use `taste-review` when taste profile exists or quality feels ambiguous.
- New idea/signal during work: use `anticipation-radar` and classify A-0..A-4.
- Scope-changing proactive ideas require user confirmation.
- Agent identities must remain exact role IDs; no aliases or codenames.


## Taste / culture / anticipation shortcuts

- Team culture applies by default through `docs/TEAM_CULTURE.md`, but load the full file only when culture/taste affects the decision.
- Product/UI/design/prototype work may use `taste-calibration` before design and `taste-review` before final approval.
- If the user provides good/bad examples, use `example-taste-board` and record them in TASK.md.
- Use `expectation-anticipation` for forward-looking proposals that may improve quality, but never implement A2/A3/A4 proposals without approval.
- Use `creative-tension-review` when a product/design decision is adequate but could be materially better.
- Report real spawned agents by exact `agent_id` only. Ignore any UI-generated thread labels or personal names.

## Agent naming policy

Use exact agent IDs. If the UI auto-labels spawned threads, ignore those labels in artifacts and summaries. See `docs/AGENT_NAMING_POLICY.md` when real subagents are used.
