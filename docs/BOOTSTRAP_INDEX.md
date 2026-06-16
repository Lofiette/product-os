# BOOTSTRAP_INDEX.md — 3.0 runtime index

This is the compact startup map. It is not a full manual.

## Tier 0 startup files

Load only these files before intake decisions:

1. `AGENTS.md`
2. `CURRENT.md`
3. `TASK_INDEX.md`
4. `CHRONICLE.md`
5. `docs/BOOTSTRAP_INDEX.md`
6. `docs/LANGUAGE_POLICY.md`

Do not load all tickets, archive logs, old snapshots, release notes, full role indexes, all playbooks, all skills, or reference-only docs at startup.

## Runtime flow

1. Identify active ticket from `CURRENT.md`.
2. Decide whether the user request continues the active ticket, creates a new ticket, resumes from snapshot, or requires context pruning.
3. Load the active ticket only.
4. Ask only questions that can change scope, risk, role/skill routing, acceptance criteria, implementation, verification, or approval gates. Load `docs/QUESTION_TREE.md` only when structured intake is needed.
5. If repo exists, propose `repo-recon` before implementation decisions.
6. If UI/design is affected, propose `design-recon` before UI decisions.
7. If taste, examples, or visual feel can change quality, consider `taste-calibration` and `example-taste-board`.
8. If a visual reference exists, use `reference-fidelity` before implementation and `screenshot-reference-comparison` after render.
9. If DS manifest/registry is created, changed, or used, use `design-source-authority` and `manifest-freeze-check`.
10. After intake, classify routing cost first: `Tiny/Micro` should not load indexes by default; no role/skill indexes by default for obvious Tiny/Micro work; `Fast Lane` loads tiny indexes only when the route is unclear; `Standard+` may use `docs/SKILL_ROUTER_INDEX.json` for ultra-light domain routing, then `docs/ROLE_TINY_INDEX.json` and `docs/SKILL_TINY_INDEX.json`. Load mini/full indexes or role cards only if needed.
11. Propose roles, skills, orchestration mode, gates, and scripts.
12. Ask approval before real subagent spawn or implementation.
13. After approval, explicitly report spawned vs simulated execution.
14. Run selected skills and gates.
15. Update `CURRENT.md`, active ticket, `TASK_INDEX.md` if needed, and compact `CHRONICLE.md`.

## Quick triggers

- Existing repo → `repo-recon`.
- UI/design affected → `design-recon`.
- UI without DS → `prototype-ui-kit`.
- UI with DS → `design-system-compliance` and DS scripts.
- Current rendered page review → `ui-review-packet` + `current-page-ui-review`.
- Module for later developer rebuild → `module-design` + `design-handoff-qa`.
- Production web/service → phased orchestration + `production-readiness-review`.
- Generated/sample content → `content-realism-review`.
- Visible debug/prototype controls → `debug-control-review`.
- New idea/signal → `expectation-anticipation`; scope changes require approval.

## Runtime stability docs

Load only when relevant:

- `docs/SUBAGENT_RUN_CONTRACT.md` before real subagent spawn.
- `docs/SUBAGENT_FAILURE_POLICY.md` when spawned agents stall/fail/duplicate.
- `docs/UI_REVIEW_PACKET.md` before current-page UI review.
- `docs/UI_REVIEW_RUNBOOK.md` for bounded rendered UI review.

## Non-negotiables

- `TASK.md` is a deprecated compatibility pointer only.
- Selected role is not a spawned subagent.
- Generated artifacts cannot validate themselves.
- Technical checks alone never equal design PASS.
- “Looks similar” is not evidence.
- Use exact agent IDs only; ignore UI-generated personal/thread labels in formal artifacts.


## Skill discovery

For critical workflows, do not rely on implicit skill discovery. Load `docs/SKILL_DISCOVERY_POLICY.md` only when skill selection appears unreliable, the task is Standard+, or a previous run missed required skills/gates.

## 3.0 Product Knowledge

Use `docs/PRODUCT_KNOWLEDGE_SYSTEM.md`, `docs/PRODUCT_ONBOARDING.md`, `docs/BOUNDED_DISCOVERY.md`, and `docs/IMPACT_MAP_PROTOCOL.md` for task routing and context engineering.
