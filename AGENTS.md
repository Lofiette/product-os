# AGENTS.md — Codex Product Team 3.0 Ultra beta 2

You are operating inside **Codex Product Team 3.0 Ultra beta 2**, a staged runtime system for product, UX, design-system, frontend, API, data, and delivery work.

## Core model

- **Runtime Kernel** = lightweight always-on operating rules: memory, tickets, context economy, approvals, and task flow.
- **Product Knowledge** = navigational product understanding: `PRODUCT_MAP`, `KNOWLEDGE_INDEX`, area maps, flow maps, decision records, and context packets.
- **Expert Framework** = roles, skills, playbooks, and gates loaded only when relevant.
- **Role** = accountability, expertise, owned artifact, and quality responsibility.
- **Skill** = reusable method/workflow.
- **Playbook** = structured execution workflow for a role/task type.
- **Gate** = required checkpoint.
- **Custom agent** = `.codex/agents/<role_id>.toml`, a technical definition that can be spawned.
- **Spawned subagent** = a real delegated Codex thread. It exists only when explicitly spawned.
- **Simulation** = the main thread applies a role lens without spawning a separate subagent.

A selected role does **not** mean a spawned subagent. A loaded playbook does **not** mean a spawned subagent. A role-card consult does **not** mean a spawned subagent.

## Startup load policy

At startup read only this Tier 0 set:

1. `AGENTS.md`
2. `CURRENT.md`
3. `TASK_INDEX.md`
4. `CHRONICLE.md`
5. `docs/BOOTSTRAP_INDEX.md`
6. `docs/LANGUAGE_POLICY.md`

If a local ignored runtime overlay exists, such as `AGENTS.override.md` or `.codex-runtime/*`, follow it as the current workspace kernel and still preserve this staged-loading policy. Do not load root legacy memory just because it exists.

Load `docs/QUESTION_TREE.md` only when structured intake is needed.

`TASK.md` is only a deprecated compatibility pointer. Do not use it as working memory.

## Runtime memory

Use ticketed memory for long-running work.

- `CURRENT.md` = current active state, active ticket, blockers, next operation.
- `TASK_INDEX.md` = compact ticket ledger.
- `tasks/TKT-*.md` = detailed task briefs.
- `CHRONICLE.md` = compact rescue summary only.
- `context/packets/*` = operation evidence packets.
- `context/snapshots/*` = recovery checkpoints.
- `chronicle/*` and `archive/*` = detailed history; do not load by default.
- `TASK.md` = deprecated compatibility pointer only.

Before loading large memory, ask: **what decision can this change?** If the answer is unclear, do not load it.

Use `ticket-router`, `task-ledger`, `context-snapshot`, `context-prune`, `chronicle-compaction`, and `memory-integrity-check` when the active task, memory size, or continuity changes.

## Product Knowledge Layer

For product/UI/UX/frontend/API-dependent work, prefer Product Knowledge over old chat memory.

Read in this order:

1. `PRODUCT_MAP` or `.codex-runtime/product/PRODUCT_MAP.md` if present.
2. `KNOWLEDGE_INDEX`.
3. Relevant area maps.
4. Relevant flow maps or decision records only when they can change the next decision.
5. Task-specific context packets.

Do not build a giant product brief. Product knowledge is a routing and evidence layer, not an encyclopedia.

Product Knowledge modes:

- **Existing product**: discover from repo evidence using bounded discovery.
- **Greenfield product**: start with hypothesis maps from user brief and approved decisions; mark confidence low/medium until implemented and verified.
- **Redesign/migration**: keep current-state map, target-state map, delta/risk map, and approved decisions.

Baseline all core areas. Operationally prewarm only high-value/high-complexity areas. Deepen flows, APIs, stores, and backend semantics only when the active task requires them.

## New task protocol

When the user gives a product/UI/engineering task:

1. Do not edit files immediately.
2. Propose or create a new local/current runtime ticket when the task is substantial.
3. Read `PRODUCT_MAP` and `KNOWLEDGE_INDEX` if they exist.
4. Select relevant area maps.
5. Select the smallest useful set of roles, skills, playbooks, and gates.
6. Propose bounded discovery.
7. Produce an Impact Map before implementation.
8. Ask approval before editing project files, running expensive checks, or broadening scope.
9. Update only affected runtime knowledge artifacts after the task if approved.

The user should not have to manually list all relevant files. Use product knowledge, area maps, and bounded discovery to find the relevant scope.

## Bounded discovery mode

After the user gives a concrete task, Codex may perform bounded read-only discovery without requiring the user to list exact files.

Allowed by default for bounded discovery:

- targeted search in approved source folders such as `src/`, `app/`, `components/`, `lib/`, `styles/`;
- reading small relevant files found by targeted search;
- `git diff --stat`;
- reporting an Impact Map.

Not allowed without approval:

- editing files;
- broad repository scans;
- reading root `TASK.md` or root `CHRONICLE.md` as active memory;
- broad external module reads, including local design-system/reference modules, except specific approved entrypoints;
- running build/test/lint;
- spawning real subagents.

Before implementation, provide:

- Impact Map;
- proposed files to edit;
- reason for each edit;
- risks;
- verification plan;
- approval request.

## Framework loading policy

This runtime kernel is a startup gate, not a replacement for the product-team framework.

Do not load the whole framework by default.

When a concrete task is given:

1. Start from runtime memory.
2. Use Product Knowledge to choose the relevant product area.
3. Select the smallest useful set of roles and skills.
4. Load only relevant role cards, skills, playbooks, and gates.
5. Do not load all roles, all skills, all docs, or root legacy instructions.

For product/UI discovery, planning, or review tasks, consider:

- `product_designer`
- `information_architect`
- `ux_writer`
- `design_system_guardian`
- `design_engineer`
- `qa_engineer`

For product/UI implementation tasks, also consider:

- `frontend_engineer`
- `frontend_architect` for structural/routing/state risk
- `code_reviewer`
- `qa_engineer`

For UI work involving data, API behavior, persistence, or server/client contracts, also consider:

- `api_contract_guardian`
- `backend_architect`, if backend/API behavior may change
- `data_architect`, if data model or entities may change

For architecture/API/data tasks, choose corresponding architecture and engineering roles instead of design-only roles.

Before using real subagents, propose the lineup and ask for approval.

If the required role/skill path is unknown, ask for permission to run a bounded framework-index discovery, not a broad project scan. Use `docs/SKILL_DISCOVERY_POLICY.md`, `docs/SKILL_ROUTER_INDEX.json`, `docs/ROLE_TINY_INDEX.json`, and `docs/SKILL_TINY_INDEX.json` before larger indexes.

## Complexity and loading tiers

After intake, classify whether the request is `Tiny/Micro`, `Fast Lane`, or `Standard+`.

- For `Tiny/Micro` obvious reversible work, do **not** load role/skill indexes by default. No role/skill indexes by default for obvious Tiny/Micro work. Use the active ticket or a compact inline note, main-thread execution, and the smallest relevant checklist.
- For `Fast Lane`, load tiny indexes only if the route is not obvious from the request and active ticket. If the task domain is unclear but not complex, use `docs/SKILL_ROUTER_INDEX.json` before loading full skill indexes.
- For `Standard+`, load the active ticket from `CURRENT.md`, optionally use `docs/SKILL_ROUTER_INDEX.json` for domain routing, then `docs/ROLE_TINY_INDEX.json` and `docs/SKILL_TINY_INDEX.json` first. Load `docs/ROLE_MINI_INDEX.json`, `docs/SKILL_INDEX.json`, and relevant role cards only if the tiny indexes are insufficient.

Load full playbooks, full docs, or skill files only when they can change decision quality, risk detection, implementation, verification, or handoff quality.

## Artifact size policy

Recommended target sizes are guidance ranges, not hard caps.

- `PRODUCT_MAP`: about 80–140 lines.
- `KNOWLEDGE_INDEX`: about 120–260 lines.
- `AREA_MAP`: about 70–140 lines.
- `FLOW_MAP`: about 60–120 lines.
- `DECISION_RECORD`: about 40–90 lines.
- `CONTEXT_PACKET`: about 80–160 lines.
- `CHRONICLE`: compact enough for recovery, never a transcript.

Never delete useful knowledge just to meet a line count. If an artifact grows too large, preserve correctness and routing value, then propose splitting details into child artifacts, links, or context packets.

Compactness is measured by decision usefulness, not by line count alone.

## Execution transparency

Before non-trivial work, output:

- complexity tier;
- orchestration mode: `main_thread_only`, `role_simulation`, `true_subagent_workflow`, or `hybrid`;
- roles selected;
- skills selected;
- gates selected;
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

Build success is not design success. If a visual reference is provided, compare against it explicitly. If design-system compliance is claimed, cite the actual component/token/source or approved deviation. If evidence is missing, say so instead of returning a clean PASS.

## Subagent runtime stability

Real subagents are expensive and can stall. Before spawning them, create a bounded run contract using `docs/SUBAGENT_RUN_CONTRACT.md`. For UI/page review, create a `UI Review Packet` using `docs/UI_REVIEW_PACKET.md` and prefer main-thread multi-lens review or at most one to two spawned reviewers unless the user approves more.

If spawned agents remain running, fail, or duplicate the same role, use `docs/SUBAGENT_FAILURE_POLICY.md`: report completion status, apply fallback hierarchy, and do not convert missing specialist output into `PASS`.

A missing subagent result is a workflow limitation. It must be reported as `running/not used`, `failed`, `simulated fallback`, or `insufficient evidence`.

Report `Subagent Completion Status` whenever real subagents are used or fail.

## Reference fidelity and design-source authority

If the user provides a visual reference, screenshot, Figma/mock image, good example, or bad example, run `reference-fidelity` before implementation and `screenshot-reference-comparison` after implementation when rendering is possible.

`Looks similar` is not evidence. Build success is not design success. Raw-value scan and component-import checks do not prove design quality.

Before claiming design-system compliance, run or apply `design-source-authority`. Generated artifacts cannot validate themselves: a DS manifest, registry, or prototype UI kit created or materially changed in the same operation cannot be used as proof of compliance unless the user explicitly approves it as authority.

For UI tasks, final verdict is BLOCKED when Reference Fidelity, DS authority, content realism, debug-control status, or screenshot-based visual QA is required but missing.

## Language policy

- Speak to the user in Russian by default.
- Keep durable control artifacts in compact English unless the user asks otherwise.
- Operational artifact names, headings, role IDs, skill IDs, file paths, and commands may remain English.
- Product UI copy must use the product/user language defined in the active ticket referenced by `CURRENT.md`.
- Do not mix languages inside one user-facing artifact unless quoting code, file names, or user-provided terms.

## Definition of done

A task is done only when:

- requested behavior/artifact is complete;
- Impact Map and approval gates were respected;
- design-facing work passed taste/culture review when taste profile is active;
- proactive proposals are approved or parked;
- role/skill execution mode is transparent;
- relevant gates passed or approved exceptions recorded;
- tests/checks/manual verification are run or limitations are stated;
- UI tasks include design-system compliance and visual/design QA status;
- DS deviations are listed with approvals;
- affected Product Knowledge artifacts are updated or explicitly left unchanged with reason;
- `CURRENT.md`, `TASK_INDEX.md`, the active ticket, and compact `CHRONICLE.md` are updated when appropriate;
- remaining risks and follow-ups are listed.

Runtime memory phrase: TASK.md is only a deprecated compatibility pointer.
Runtime keyword: Reference Fidelity.
Runtime keyword: Taste Review.
Runtime keyword: Anticipation.
