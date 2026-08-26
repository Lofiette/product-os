# Codex Product Team 2.0 — Simulation Challenge Audit

## Verdict

**PASS WITH IMPORTANT RUNTIME + UI QUALITY FIXES.**

2.0 is materially stronger than 1.5: it has explicit role/skill/subagent separation, no codenames, Product Designer, Design Engineer, design-system modes, UI quality gates, and orchestration approval. The architecture is good enough for controlled real-world experiments.

However, the simulations show that the kit can still fail in practical UI work in four ways:

1. It may propose the right roles but not actually spawn them unless the prompt explicitly asks and the user approves.
2. The UI/design skills exist, but most `SKILL.md` files are still generic workflow shells rather than executable professional protocols.
3. The design-system enforcement layer is conceptually right, but the actual scripts are too weak; one script is currently syntactically broken.
4. The kit handles screen-level work better than module-level or production-service work; it needs phased orchestration and module-level artifacts.

---

## Structural check

Built-in validator result:

```text
VALIDATION PASSED: 49 roles, 55 skills, 12 scenarios.
```

Additional checks performed:

- `TEAM.md`, `ROLE_INDEX.json`, playbooks, role cards, and `.codex/agents/*.toml` are aligned.
- 49 role IDs exist across index, cards, playbooks, and custom agents.
- 55 skill directories exist and match `SKILL_INDEX.json`.
- Scenario test references point to existing roles/skills.
- Stage 0 bootstrap size is about **9,281 chars**, much better than older builds.
- Skills initial list from `.agents/skills/*/SKILL.md` descriptions is about **6,913 chars**, likely within the rough Codex skill-list budget.

Blocking technical issue found:

```text
scripts/find-raw-ui-values.mjs
```

This script is syntactically invalid because regex/newline escaping was written incorrectly. `node --check scripts/find-raw-ui-values.mjs` fails.

Also, `scripts/check-component-imports.mjs` is only a placeholder; it prints manifest component names but does not scan code for violations.

---

## Simulation 1: Concept redesign of existing system, quick prototype, no design system

### User task

> Redesign the concept of an existing system as a quick interface prototype. There is no design system.

### Correct classification

```text
Work mode: Design prototype / concept redesign
Complexity: Standard, unless many screens or domain complexity appear
Design-system mode: none
Repo/design recon: required if an existing repo, screenshots, previous UI, or current implementation exists
Implementation: prototype only, no production assumptions
```

### Expected Codex first response

```markdown
## Понял задачу
Это быстрый концепт-редизайн существующей системы без дизайн-системы.

## Нужно уточнить 3–5 вещей
1. Что именно редизайним: один экран, поток или набор экранов?
2. Что сейчас в системе плохо: непонятность, визуальная усталость, слабая навигация, низкая конверсия, перегрузка?
3. Какие материалы есть: ссылка/скриншоты/код/описание текущего UI?
4. Это throwaway prototype или design prototype, который позже может лечь в основу реализации?
5. На каком языке должен быть интерфейс?

## Предлагаемый следующий шаг
Operation: Design recon + concept direction
Orchestration mode: hybrid or role_simulation

Roles:
- product_designer: owns redesign concept and Screen Design Spec
- ux_writer: copy/states if user-facing text matters
- visual_design_director: visual direction if redesign is materially visual
- design_engineer: only if code prototype will be built
- design_system_guardian: optional, to define lightweight local UI rules because no DS exists

Skills:
- design-recon
- screen-redesign
- state-matrix
- ui-heuristic-audit
- creative-improvement-loop, only if ideation is requested

Approval needed before spawning real subagents.
```

### What 2.0 gets right

- `No design system UI prototype` routing exists.
- `product_designer` and `design_engineer` are required in the scenario.
- `DESIGN_SYSTEM_MODES.md` explicitly says mode `none` should create lightweight local UI rules without overbuilding a DS.
- `UI_OBVIOUS_ERRORS_CHECKLIST.md` catches many obvious interface mistakes.

### Where it can break

1. **No-DS mode is underspecified.** The docs say to create lightweight local UI rules, but there is no dedicated skill/template for a `Prototype UI Kit Contract`.
2. **Design System Guardian is optional**, but for no-DS prototype work, someone still needs to enforce local consistency. It should be required in “no DS but multi-screen prototype” and optional only for one-screen throwaway sketches.
3. **Visual Design Director may be skipped**, although a concept redesign often needs visual direction, hierarchy, and composition.
4. **Creative methods are not automatically bounded to design alternatives.** `creative-improvement-loop` can help, but the output should become alternatives in Screen Design Spec, not a loose idea cloud.
5. **If Codex jumps straight to implementation**, it may produce a visually inconsistent prototype, because the design-system gate is weaker when DS mode is `none`.

### Recommended patch

Add:

```text
.agents/skills/prototype-ui-kit/SKILL.md
.agents/templates/prototype-ui-kit-contract.md
```

The prototype UI kit contract should include:

- typography scale;
- spacing scale;
- color roles;
- button/input/card/list/dialog patterns;
- icon usage;
- density rules;
- state rules;
- responsive assumptions;
- explicit “do not build a full DS” note.

Routing update:

```text
No DS + one screen + throwaway → product_designer + design_engineer, role simulation ok.
No DS + multi-screen design prototype → product_designer + design_system_guardian + design_engineer required.
Concept redesign with visual direction → add visual_design_director.
```

---

## Simulation 2: Design a whole product module; developer will rebuild it later; must follow DS rules

### User task

> Design a full product module. A developer will rebuild it later. Everything must follow design-system rules.

### Correct classification

```text
Work mode: Design module / design handoff, not implementation
Complexity: Complex if multiple screens/states/permissions
Design-system mode: documented_ds or governed_ds, depending on DS source
Implementation: no code unless explicitly requested
Primary artifact: Module Design Package, not just Screen Design Spec
```

### Expected Codex first response

```markdown
## Предлагаемый следующий шаг
Operation: Module design planning + DS recon
Orchestration mode: true_subagent_workflow or hybrid

Before design, I need to run design-recon against the DS source of truth.

Suggested spawned agents:
| Agent | Artifact | Skills |
|---|---|---|
| product_designer | Module Design Package | design-recon, module-design, state-matrix |
| design_system_guardian | DS Constraints & Component Matrix | design-recon, design-system-manifest, design-system-compliance |
| information_architect | Navigation/object model | information-architecture |
| ux_writer | Content Matrix | content-pattern-review |

Simulated or later:
- design_engineer: implementation feasibility and handoff fidelity, not code
- qa_engineer: acceptance/checklist
- frontend_architect: optional feasibility check if dev handoff needs engineering constraints

Approval needed before spawning.
```

### What 2.0 gets right

- It can detect governed DS folder via `DESIGN_SYSTEM_MODES.md`.
- It has Design System Guardian, Product Designer, Information Architect, UX Writer, Design Engineer.
- It has design-system manifest and compliance skills.
- It has templates for Screen Design Spec and Design Diff Summary.

### Where it can break

1. **There is no module-level design skill.** `screen-redesign` is screen-level. Designing a whole module needs a `module-design` or `product-module-design` skill.
2. **There is no Module Design Package template.** The module requires flow map, object model, navigation, screen inventory, permissions/states, component matrix, acceptance criteria, and developer handoff.
3. **Design Engineer may be misused.** In this scenario the developer rebuilds later. Design Engineer should produce an implementation-fidelity/handoff constraint report, not implement code.
4. **QA Engineer default skill is `implementation-review`,** which is too code-oriented for design-only module planning. Need a design-handoff QA skill.
5. **The process might still over-spawn.** For a design-only module, backend/security/devops roles should not activate unless the module includes API/data/security decisions.

### Recommended patch

Add:

```text
.agents/skills/module-design/SKILL.md
.agents/skills/design-handoff-qa/SKILL.md
.agents/templates/module-design-package.md
.agents/templates/ds-component-matrix.md
.agents/templates/developer-rebuild-brief.md
```

Module Design Package should include:

- module goal;
- user roles and permissions;
- entity/object model;
- navigation map;
- screen inventory;
- flow diagrams in text;
- state matrix per screen;
- DS component matrix;
- content matrix;
- responsive rules;
- accessibility rules;
- edge cases;
- open decisions;
- developer rebuild instructions;
- non-goals.

Routing update:

```text
Whole product module, design-only → product_designer + information_architect + design_system_guardian + ux_writer required.
Design Engineer → optional/handoff mode unless implementation is requested.
QA Engineer → design-handoff QA, not implementation-review.
```

---

## Simulation 3: Production web service, design system in code

### User task

> Design and build a production web service. The design system exists in code.

### Correct classification

```text
Work mode: Production web service
Complexity: Complex or High-risk, depending on auth/data/privacy/payments/AI
Design-system mode: component_library or documented_ds, possibly governed_ds if code DS has docs
Repo recon: required
Design recon: required
Implementation: gated, staged, not one giant operation
```

### Expected Codex first response

```markdown
## Нужно уточнить risk-critical вопросы
1. Что делает сервис и для кого?
2. Есть ли auth, роли, персональные данные, платежи, AI, файлы, уведомления?
3. Это greenfield или существующий repo?
4. Где DS source of truth в коде?
5. Какие production gates обязательны: tests, lint, typecheck, e2e, security review, deploy?
6. Что считается MVP/production done?

## Предлагаемая стратегия
Не спавнить всех сразу. Идти фазами.

Phase 1 — Recon:
- repo-recon
- design-recon

Phase 2 — Product/architecture plan:
Spawn or simulate:
- product_strategist
- solution_architect
- frontend_architect
- backend_architect
- api_contract_guardian if API exists
- data_architect if persistent data exists

Phase 3 — UI/DS plan:
- product_designer
- design_system_guardian
- design_engineer
- ux_writer

Phase 4 — Risk plan:
- security_reviewer if auth/data/actions
- privacy_compliance_reviewer if personal/sensitive data
- performance_engineer if scale/latency matters
- devops_release_engineer if deployment required

Phase 5 — Implementation/review:
- qa_engineer
- code_reviewer
- design_engineer for UI fidelity
```

### What 2.0 gets right

- It has all necessary roles.
- It has DS-in-code handling.
- It has repo/design recon.
- It has risk roles and quality gates.
- It has explicit approval before real subagents.

### Where it can break

1. **No phased orchestration policy.** Current docs have role budgets, but not a phase plan that prevents spawning 12–15 agents at once.
2. **ROLE_ROUTING_MATRIX is too thin for production services.** It has Backend/API change and AI agent, but not “production web service” as a first-class route.
3. **DS enforcement scripts are weak.** One script is broken; one is placeholder.
4. **Visual QA is underspecified.** There is no Playwright/screenshot state capture plan.
5. **Production readiness is scattered.** Security/privacy/performance/devops/release gates exist, but there is no single Production Readiness Checklist tying them together.
6. **Skills are mostly generic.** High-risk production work needs concrete method bodies, not generic “produce compact artifact” shells.

### Recommended patch

Add:

```text
src-independent docs:
- docs/PHASED_ORCHESTRATION.md
- docs/PRODUCTION_READINESS_GATES.md
- docs/WEB_SERVICE_ROUTING.md

skills:
- production-service-planning
- production-readiness-review
- e2e-visual-state-capture
- ds-code-contract-enforcement
```

Routing update:

```text
Production web service → phased orchestration required.
High-risk roles activate only when their triggers are confirmed.
No implementation until recon + architecture + DS plan + risk posture are approved.
```

---

## Cross-cutting issues

### P0 — must fix before calling 2.0 operationally reliable

1. **Fix broken `find-raw-ui-values.mjs`.** It currently fails syntax check.
2. **Replace placeholder `check-component-imports.mjs` with a real scan.** It should identify imports, duplicate custom UI, and forbidden components.
3. **Make UI skills executable, not generic.** `design-recon`, `screen-redesign`, `state-matrix`, `visual-qa-loop`, `ui-heuristic-audit`, `design-qa`, `component-contract-scan` need concrete step-by-step checklists and output tables.
4. **Add module-level design flow.** Current kit is screen-strong but module-light.
5. **Add phased orchestration.** Production service work should not spawn a huge team at once.
6. **Add runtime guarantee after user approval.** After approval, Codex must explicitly say: “Now spawning: …” or “No real subagents spawned.”
7. **Add no-DS prototype contract.** Without this, no-DS prototypes may become inconsistent.

### P1 — quality improvements

1. Replace huge `ROLE_INDEX.json` with a small `ROLE_MINI_INDEX.json` for runtime routing. Current `ROLE_INDEX.json` is about 41k chars.
2. Keep `TEAM.md` and full `ROLE_INDEX.json` as reference docs, not runtime docs.
3. Add executable routing tests: `scripts/test-routing.py` should validate scenario expected roles/skills/modes.
4. Add `Design QA` as a required final gate for UI tasks, not a barely referenced skill.
5. Add `Module Design Package` and `Developer Rebuild Brief` templates.
6. Add `DS Evidence Map`: every DS decision should reference component docs, code paths, or approved deviations.
7. Add screenshot capture recipes for common stacks: Vite/React, Next.js, Storybook.
8. Add “do not implement yet” guard to design-only tasks where developer rebuilds later.

### P2 — cleanup / legacy reduction

1. Move `ROLE_METHOD_LIBRARY.md` to reference-only or split into role-specific references.
2. Merge `ROLE_OUTPUT_SCHEMAS.md` with templates or make it authoritative; right now it is too generic.
3. Keep `SELF_AUDIT_REPORT.md` but mark it as build-time only, not runtime.
4. Expand `VALIDATOR_RULES.md` to include script syntax checks and generic-skill detection.
5. Remove or rewrite generic skill boilerplate. 51/55 skills are currently “generic-ish” by content shape.

---

## Practical conclusion

2.0 now has the right conceptual architecture:

```text
Role = accountability
Skill = method
Custom agent = spawnable role executor
Spawned subagent = real delegated thread
```

But for real UI/product work, the next improvement is not more roles. It is stronger **runtime enforcement**:

- executable UI skills;
- real design-system scripts;
- module-level design artifacts;
- phased orchestration;
- no-DS prototype contract;
- explicit spawn confirmation after approval;
- production service gates.

If applied, the next version should be:

```text
Codex Product Team 2.1 — Operational UI & Production Hardening
```

Goal:

```text
Make the system not only select the right experts, but force the right artifacts and checks before Codex claims the task is done.
```
