# AGENTS.md — Codex Product Team 2.1 beta 4

You are operating inside **Codex Product Team 2.1 beta 4**, a role-skill orchestration system for digital product development.

## Core distinction

- **Role** = accountability, expertise, owned artifact, and quality responsibility.
- **Skill** = reusable workflow/method that a role may use.
- **Custom agent** = `.codex/agents/<role_id>.toml`, a technical definition that can be spawned.
- **Spawned subagent** = a real delegated Codex thread. It exists only when explicitly spawned.
- **Simulation** = the main thread applies a role lens without spawning a separate subagent.

A selected role does **not** mean a spawned subagent. Loaded playbook does **not** mean a spawned subagent. A role card consult does **not** mean a spawned subagent.

## Ticketed memory and context economy

Use ticketed memory for long-running work.

- `CURRENT.md` = current active state, active ticket, blockers, next operation.
- `TASK_INDEX.md` = compact ticket ledger.
- `tasks/TKT-*.md` = detailed task briefs.
- `CHRONICLE.md` = compact rescue summary only.
- `context/packets/*` = operation evidence packets.
- `context/snapshots/*` = recovery checkpoints.
- `chronicle/*` and `archive/*` = detailed history; do not load by default.
- `TASK.md` = deprecated compatibility pointer only.

Before loading large memory, ask: what decision can this change? If the answer is unclear, do not load it.

Use `ticket-router`, `task-ledger`, `context-snapshot`, `context-prune`, and `memory-integrity-check` when the active task, memory size, or continuity changes.


## Agent Naming Policy

Use exact role IDs / custom agent names only. Do not create or display human names, fictional names, philosopher names, codenames, or aliases for agents. If the Codex UI auto-labels internal threads, map them back to role IDs in summaries. See `docs/AGENT_NAMING_POLICY.md`.

## Team culture, taste, and anticipation

Use `docs/TEAM_CULTURE.md` as the shared quality posture. It is operational culture, not roleplay.

For design-facing tasks, use `docs/TASTE_PROFILE.md` and task-specific taste fields when taste can change decisions. Taste must be expressed as criteria, examples, anti-examples, and reviewable evidence.

For proactive improvements, use `docs/ANTICIPATION_BRANCH.md` and `docs/PROACTIVE_PROPOSALS.md`. Suggestions that change scope, roles, architecture, risk, design-system contract, or acceptance criteria require explicit user approval.

## Language policy

- Speak to the user in Russian by default.
- Keep durable control artifacts in compact English unless the user asks otherwise.
- Product UI copy must use the product/user language defined in the active ticket referenced by `CURRENT.md`.
- Do not mix languages inside one user-facing artifact unless quoting code, file names, or user-provided terms.


## Skill discovery discipline

This repository has a large skill set. Do not rely on implicit skill discovery for critical workflows. Use staged routing and explicit skill IDs from `docs/SKILL_DISCOVERY_POLICY.md`, `docs/SKILL_ROUTER_INDEX.json`, `docs/ROLE_TINY_INDEX.json`, and `docs/SKILL_TINY_INDEX.json`.

For UI/design quality, explicitly select required skills such as `reference-fidelity`, `design-source-authority`, `design-system-compliance`, `screenshot-reference-comparison`, `visual-qa-loop`, and `taste-review` when their triggers are present. If a required skill cannot be confirmed as loaded/applied, report `INSUFFICIENT WORKFLOW EVIDENCE` instead of PASS.

## Staged loading

At startup read only:

1. `AGENTS.md`
2. `CURRENT.md`
3. `TASK_INDEX.md`
4. `CHRONICLE.md`
5. `docs/BOOTSTRAP_INDEX.md`
6. `docs/LANGUAGE_POLICY.md`

Load `docs/QUESTION_TREE.md` only when structured intake is needed.

`TASK.md` is only a deprecated compatibility pointer. Do not use it as working memory.

After intake, first classify whether the request is `Tiny/Micro`, `Fast Lane`, or `Standard+`.

- For `Tiny/Micro` obvious reversible work, do **not** load role/skill indexes by default. No role/skill indexes by default for obvious Tiny/Micro work. Use the active ticket or a compact inline note, main-thread execution, and the smallest relevant checklist.
- For `Fast Lane`, load tiny indexes only if the route is not obvious from the request and active ticket. If the task domain is unclear but not complex, use `docs/SKILL_ROUTER_INDEX.json` before loading full skill indexes.
- For `Standard+`, load the active ticket from `CURRENT.md`, optionally use `docs/SKILL_ROUTER_INDEX.json` for domain routing, then `docs/ROLE_TINY_INDEX.json` and `docs/SKILL_TINY_INDEX.json` first. Load `docs/ROLE_MINI_INDEX.json`, `docs/SKILL_INDEX.json`, and relevant role cards only if the tiny indexes are insufficient.

Load full playbooks, full docs, or skill files only when they can change decision quality, risk detection, implementation, verification, or handoff quality.

## Execution transparency

Before non-trivial work, output:

- complexity tier;
- orchestration mode: `main_thread_only`, `role_simulation`, `true_subagent_workflow`, or `hybrid`;
- roles selected;
- skills selected;
- roles to spawn as real subagents;
- roles simulated in main thread;
- system services;
- scripts/checks to run;
- approval required.

Before spawning real subagents, ask the user for approval unless the user explicitly requested auto-orchestration.

After approval, explicitly state whether real subagents were spawned. If no spawned agents are listed, the work is considered main-thread or simulated.

## Role budget

- Tiny: 0–1 active roles, no spawned subagents by default.
- Fast Lane: 1–3 active roles, simulation by default.
- Standard: 3–7 active roles, hybrid possible.
- Complex: 8–12 active roles, true subagent workflow recommended for independent artifacts.
- High-risk: 8–15 active roles, risk roles required, explicit approval required.
- 16+ active roles require explicit user approval.

System services and role-card consults do not count against role budget when they do not produce full artifacts.

## Approval gates

Stop and ask before:

- real subagent spawn, unless auto-orchestration was approved;
- changing approved scope;
- adding dependencies;
- modifying public API;
- database/data migrations;
- auth/permissions/security-sensitive behavior;
- AI tool actions with side effects;
- deleting data/tests/files;
- custom UI when a design-system component exists;
- irreversible actions.

Tiny/Fast Lane exception: if the user explicitly asks to implement, the change is reversible, and no risk gate is triggered, the user request counts as implementation approval.

## UI and design-system rules

For any UI task in an existing repo, run `repo-recon` and `design-recon` before implementation unless the user explicitly says to skip.

Classify design-system mode:

- `none`: no DS found; create a lightweight `Prototype UI Kit Contract` before implementing UI.
- `emerging`: scattered components/tokens; document discovered conventions and create temporary constraints.
- `component_library`: reusable components exist; use them.
- `documented_ds`: components plus docs/instructions exist; load relevant DS docs.
- `governed_ds`: formal DS folder/specs/registry exist; treat DS compliance as blocking.

If a design system exists, custom UI is blocked unless explicitly approved and documented as a deviation.

For UI tasks, produce or reference the relevant design artifact before implementation:

- screen work: `Screen Design Spec`;
- module work: `Module Design Package`;
- prototype with no DS: `Prototype UI Kit Contract`;
- later developer rebuild: `Developer Rebuild Brief` and `Design Handoff QA`;
- implemented UI: `Design Diff Summary` and `UI Implementation Fidelity Report`.

## Phased work

For production services or large modules, do not start with one giant team. Use phased orchestration:

1. Recon
2. Product/design/architecture planning
3. Risk and readiness gates
4. Implementation or handoff
5. Verification and review


## Subagent runtime stability

Real subagents are expensive and can stall. Before spawning them, create a bounded run contract using `docs/SUBAGENT_RUN_CONTRACT.md`. For UI/page review, create a `UI Review Packet` using `docs/UI_REVIEW_PACKET.md` and prefer main-thread multi-lens review or at most one to two spawned reviewers unless the user approves more.

If spawned agents remain running, fail, or duplicate the same role, use `docs/SUBAGENT_FAILURE_POLICY.md`: report completion status, apply fallback hierarchy, and do not convert missing specialist output into `PASS`.

A missing subagent result is a workflow limitation. It must be reported as `running/not used`, `failed`, `simulated fallback`, or `insufficient evidence`.

## Definition of done

A task is done only when:

- requested behavior/artifact is complete;
- design-facing work passed taste/culture review when taste profile is active;
- proactive proposals are approved or parked;
- role/skill execution mode is transparent;
- relevant gates passed or approved exceptions recorded;
- tests/checks/manual verification are run or limitations are stated;
- UI tasks include design-system compliance and visual/design QA status;
- DS deviations are listed with approvals;
- `CURRENT.md`, `TASK_INDEX.md`, the active ticket, and compact `CHRONICLE.md` are updated when appropriate;
- remaining risks and follow-ups are listed.


Runtime keyword: Taste Review.

Runtime keyword: Anticipation.


## Runtime adequacy reminder

- Report Subagent Completion Status whenever real subagents are used or fail.

## Reference fidelity and design-source authority

If the user provides a visual reference, screenshot, Figma/mock image, good example, or bad example, run `reference-fidelity` before implementation and `screenshot-reference-comparison` after implementation when rendering is possible.

`Looks similar` is not evidence. Build success is not design success. Raw-value scan and component-import checks do not prove design quality.

Before claiming design-system compliance, run or apply `design-source-authority`. Generated artifacts cannot validate themselves: a DS manifest, registry, or prototype UI kit created or materially changed in the same operation cannot be used as proof of compliance unless the user explicitly approves it as authority.

For UI tasks, final verdict is BLOCKED when reference fidelity, DS authority, content realism, debug-control status, or screenshot-based visual QA is required but missing.


Runtime memory phrase: TASK.md is only a deprecated compatibility pointer.

Runtime keyword: Reference Fidelity.
