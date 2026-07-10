# Codex Product Operating System 4.0 Alpha 5 — Role Expertise and Routing Audit

Date: 2026-07-10  
Version: `4.0.0-alpha.5`  
Phase: **Phase 4 — Role Expertise and Routing Overhaul**

## Verdict

**PASS for Alpha 5 role-layer scope, with worker orchestration, live-model routing, and automated gate enforcement explicitly deferred.**

Alpha 5 preserves the Alpha 1 Runtime Kernel, Alpha 2 distribution model, and Alpha 3 skill consolidation. It rewrites the complete 50-role library as typed accountability lenses, connects roles to the 45 canonical skills and 25 evidence-based gates, and keeps the installed project footprint below the distribution budget.

## Implemented

- all 50 logical roles from `codex-product-team-3.0-ultra-beta2` retained;
- zero new logical roles and zero deprecated roles;
- 50 compact role lenses;
- 50 deep, role-specific method references;
- explicit decision rights, activation/non-activation, artifacts, evidence, handoffs, skills, gates, task types, execution modes, and worker eligibility;
- 25 quality gates with four-state verdict contracts;
- 14 task routing profiles;
- role-to-skill and role-to-gate matrices;
- complete role migration registry;
- compact runtime expertise bundle inside `cpt-core`;
- deterministic role trigger and routing proxy evaluations;
- preserved installer/update/uninstall/runtime behavior.

## Inventory

| Metric | Result |
|---|---:|
| Logical roles | 50 |
| Roles retained from 3.0 | 50 / 50 |
| New roles | 0 |
| Role lenses | 50 |
| Deep role methods | 50 |
| Canonical skills | 45 |
| Quality gates | 25 |
| Routing profiles | 14 |
| Role trigger cases | 150 |
| Routing-profile cases | 14 |
| Role proxy cases passed | 164 / 164 |
| Lens lines | 3,325 |
| Method-reference lines | 3,083 |
| Gate-contract lines | 988 |
| Team-mode project framework files | 19 |

## Role distribution

| Plugin | Primary roles |
|---|---:|
| `cpt-core` | 6 |
| `cpt-product-research` | 9 |
| `cpt-design-ui` | 12 |
| `cpt-engineering` | 18 |
| `cpt-risk-operations` | 2 |
| `cpt-ai-agentic` | 3 |

## Role model

Alpha 5 enforces the following separation:

```text
Role   = accountable professional lens
Skill  = reusable method
Gate   = evidence required to accept a result
Worker = bounded execution container, deferred to the Execution Plane
```

Roles default to the main thread. Worker eligibility records whether a bounded independent contribution could be delegated later; it never grants spawn permission.

## Expertise depth

Every role now includes:

- explicit decision rights;
- at least two professional mental models;
- a role-specific multi-step method;
- evidence requirements;
- professional anti-patterns;
- an output contract;
- stop and escalation rules;
- canonical skill and gate mappings.

The legacy role-card/playbook template was not copied forward as the active method. The stable role IDs and competency coverage were preserved, while the method content was rewritten.

## Quality gates

Twenty-five gates cover:

- scope and evidence integrity;
- product value and research validity;
- design, design-system fidelity, content, accessibility, localization;
- frontend, architecture, API, data, analytics;
- security, privacy, performance;
- AI quality and AI safety;
- production, migration, experimentation, verification;
- incident learning and knowledge freshness.

Every gate supports:

```text
PASS
PASS_WITH_WARNINGS
BLOCKED
INSUFFICIENT_EVIDENCE
```

A warning cannot hide a blocker, and missing evidence cannot become a clean pass.

## Runtime loading

The full role library remains in the distribution package for authoring, audit, and migration.

The installed core plugin carries one task-planning reference file:

```text
references/EXPERTISE_BUNDLE.json
```

It contains the compact role router, routing profiles, selected deep methods, and gate contracts. It is loaded only after `cpt-task-planning` is invoked; it does not add skill-discovery metadata.

The team-mode project footprint remains at 19 framework files.

## Migration

`migration/ROLE_MIGRATION.json` and `.csv` map all 50 source roles to the same stable role IDs with status:

```text
retained_rewritten
```

Migration adds:

- typed ownership;
- skill/gate routing;
- method depth;
- worker-eligibility separation;
- canonical runtime references.

It does not install legacy role aliases or 50 custom agents.

## Static and proxy validation

```text
ROLE VALIDATION PASSED: 50 logical roles, 25 gates, 14 routing profiles
ROLE ROUTING PROXY EVAL: 164/164 passed
SKILL VALIDATION PASSED: 45 active skills, 95 unique legacy mappings, 6 plugins
TRIGGER PROXY EVAL: 135/135 passed
DISTRIBUTION STATIC VALIDATION PASSED
```

Validated:

- exact 50-role preservation;
- role IDs, plugins, skills, gates, and handoffs;
- lens/method/gate required sections;
- method depth and evidence obligations;
- one accountable role per routing profile;
- complete migration coverage;
- plugin role inventories;
- compact expertise-bundle consistency;
- trigger/routing case coverage;
- absence of one-custom-agent-per-role packaging.

## Behavioral distribution tests

All 15 distribution cases passed, including:

- local Git-clean installation;
- team installation below 20 framework files;
- tracked `AGENTS.md` protection;
- runtime-state-preserving update;
- managed-file conflict detection;
- safe uninstall;
- marketplace preservation;
- independent domain-pack lifecycle;
- core metadata budget;
- doctor and legacy-skill resolution.

Role tests: 4 / 4 PASS.  
Skill tests: 5 / 5 PASS.

## Honest limitations

- Role selection evaluation is a deterministic metadata proxy, not a live Codex trace.
- Quality gates are contracts, not hook-enforced runtime barriers yet.
- Worker archetypes, timeout, cancellation, quorum, and worktree isolation are not implemented.
- Product Knowledge schemas and claim provenance are not migrated.
- Role method references do not yet include a curated external bibliography or worked example for every domain.
- The runtime expertise bundle is intentionally compact in file count but can still be context-heavy if a model reads it indiscriminately; `cpt-task-planning` instructs router-first, selected-method loading.
- No SQLite, MCP, external adapters, or observability backend are included.

## Phase 4 exit assessment

| Criterion | Status |
|---|---|
| Preserve all 50 logical roles | PASS |
| Add no unproven new roles | PASS |
| Replace generic role methods | PASS |
| Define decision rights and evidence | PASS |
| Map roles to canonical skills | PASS |
| Map roles to evidence gates | PASS |
| Add routing profiles | PASS |
| Separate roles from workers | PASS |
| Preserve distribution file budget | PASS |
| Add role migration and proxy evals | PASS |
| Live Codex role-routing certification | DEFERRED |
| Executable worker archetypes | DEFERRED to Execution Plane |

## Recommendation

Freeze Alpha 5 as the role/expertise baseline and proceed to Phase 5: Product Knowledge Schema and Lifecycle.

The next phase should type Product Map, Knowledge Index, Area/Flow Maps, Decision Records, API/Data contracts, claim provenance, freshness dependencies, and task-specific context packets without expanding the always-on runtime surface.
