# Codex Product Team ULTIMATE — Pro Audit & Efficiency Review

**Artifact audited:** `TEMPLATE-codex-product-team-ultimate.zip`  
**Audit date:** 2026-05-25  
**Verdict:** **PASS WITH BLOCKING FIXES FOR FINAL POLISH**

The kit is structurally strong and already usable as an advanced Codex operating system. However, this audit found one important integrity issue and several resource-efficiency opportunities. The key point: the next improvements should not reduce quality. They should move information to the moment when it actually changes a decision.

---

## 1. Executive verdict

### What is solid

- `scripts/validate_kit.py` passes: `VALIDATION PASSED: 42 roles, 12 skills, 9 scenarios.`
- Required docs, playbooks, skills, TOML agents, scenario tests, language policy, evidence policy, risk gates, and complexity model are present.
- The process model is mature: staged loading, Intake A/B, role routing, approval gates, review mode, Chronicle, and risk escalation.
- The kit now clearly supports Russian user communication plus compact English durable artifacts.
- The complexity model is the right strategic direction: “maximum capability, minimum necessary ceremony.”

### What must be fixed before calling it truly ULTIMATE

1. **Codename inconsistency between `TEAM.md`/TOML and playbooks.**  
   Role IDs are stable, but several codenames disagree. This can confuse routing, handoff summaries, and user-facing role reports.

2. **Stage 1 still loads too much.**  
   Current Stage 1 asks Codex to read ~71k characters of docs before the task is understood. This is not catastrophic, but it violates the spirit of minimum sufficient ceremony.

3. **Playbooks are stronger than before, but still contain repeated boilerplate.**  
   They are operationally usable, but some “professional depth” is still generalized rather than truly role-specific.

4. **Scenario tests are good as documentation, but not yet a real test harness.**  
   JSON is machine-readable, but validator checks only basic consistency, not whether routing decisions match expected behavior under simulation.

5. **Resource management is implicit, not measured.**  
   The kit has complexity tiers, but no runtime “context budget ledger”: what was loaded, which roles were activated, how many questions were asked, what was skipped, and why.

---

## 2. Structural audit results

### Validator result

```text
VALIDATION PASSED: 42 roles, 12 skills, 9 scenarios.
```

### Counts

| Area | Count | Status |
|---|---:|---|
| Playbooks | 42 | Present |
| Custom agent TOML files | 42 | Present |
| Skills | 12 | Present |
| Scenario tests JSON | 9 | Present |
| Markdown scenario tests | 9 | Present |
| Backup/temp files | 0 found | Clean |
| Required root/docs files | Present | Pass |
| TOML parse | Pass | Pass |
| Self-escalation loops | 0 found | Pass |
| Missing required playbook sections | 0 found | Pass |

---

## 3. Blocking issue: codename drift

The biggest actual issue is that several role IDs have one codename in `TEAM.md` and `.codex/agents/*.toml`, but a different codename in the playbook header.

| Role ID | `TEAM.md` / TOML | Playbook header | Impact |
|---|---|---|---|
| `performance_engineer` | Sabin / Performance Engineer | Prompto / Performance Engineer | Confuses performance vs support routing |
| `dependency_curator` | Edge / Dependency Curator | Wakka / Dependency Curator | Confuses dependency risk references |
| `migration_planner` | Freya / Migration Planner | Faris / Migration Planner | Collides with localization naming |
| `devops_release_engineer` | Cidolfus / DevOps & Release Engineer | Edgar / DevOps & Release Engineer | Release docs use Cidolfus |
| `observability_engineer` | Barret / Observability Engineer | Quina / Observability Engineer | Risk/routing docs use Barret |
| `incident_investigator` | Cecil / Incident Investigator | Sephiroth / Incident Investigator | Incident routing uses Cecil |
| `experimentation_specialist` | Setzer / Experimentation Specialist | Laguna / Experimentation Specialist | Scenario/routing may drift |
| `localization_specialist` | Faris / Localization & Internationalization Specialist | Ysayle / Localization Specialist | Role title and codename drift |
| `customer_support_analyst` | Prompto / Customer Support Analyst | Ignis / Customer Support Analyst | Prompto is already referenced for support in docs |
| `refactoring_specialist` | Locke / Refactoring Specialist | Freya / Refactoring Specialist | Collides with migration naming |

### Recommendation

Make `role_id` the only true primary key, but make codenames consistent everywhere.

Preferred source of truth:

1. `TEAM.md`
2. `.codex/agents/*.toml`
3. playbook headers and codename fields
4. routing docs and ownership docs

Then add validator checks:

- parse `TEAM.md` role ID → codename/title;
- parse playbook role ID → codename/title;
- parse TOML `description` → codename/title;
- fail if any mismatch exists.

This is a quality fix, not cosmetics. If Codex reports “Prompto / Performance Engineer” while routing docs call Prompto the support analyst, the user loses trust in the team model.

---

## 4. Resource-efficiency audit

The kit correctly tries to avoid spawning all roles. The main remaining waste is not agents. It is **documents loaded too early**.

### Current Stage 1 loading cost

Current `FIRST_PROMPT.md` Stage 1 loads 19 files:

- `AGENTS.md`
- `TASK.md`
- `CHRONICLE.md`
- `TEAM.md`
- `docs/QUESTION_TREE.md`
- `docs/WORK_MODES.md`
- `docs/ROLE_ROUTING_MATRIX.md`
- `docs/OWNERSHIP_MATRIX.md`
- `docs/QUALITY_GATES.md`
- `docs/RISK_POLICY.md`
- `docs/EVIDENCE_POLICY.md`
- `docs/LANGUAGE_POLICY.md`
- `docs/FAST_LANE.md`
- `docs/COMPLEXITY_MODEL.md`
- `docs/ROLE_OUTPUT_SCHEMAS.md`
- `docs/ROLE_METHOD_LIBRARY.md`
- `docs/EXTERNAL_EVIDENCE_PROTOCOL.md`
- `docs/FINAL_FANTASY_CODENAME_POLICY.md`
- `docs/SCENARIO_TESTS.json`

Measured size:

| Stage 1 variant | Files | Characters | Words | Rough token estimate by chars/4 |
|---|---:|---:|---:|---:|
| Current Stage 1 | 19 | 70,989 | 9,349 | ~17,747 |
| Optimized Stage 1 | 14 | 25,306 | 3,781 | ~6,326 |
| Ultra-lean Stage 1 | 10 | 20,857 | 3,128 | ~5,214 |

The exact token count depends on tokenizer and language, but the direction is clear: Stage 1 can likely be reduced by around **60–70%** without losing quality.

### What to remove from Stage 1

Move these out of Stage 1:

| File | Why not Stage 1 | Load when |
|---|---|---|
| `TEAM.md` | Huge role catalog; routing matrix is enough for first triage | Stage 2, only if role details are needed |
| `docs/ROLE_METHOD_LIBRARY.md` | Deep methods are not needed before role selection | Stage 2/3, only selected sections |
| `docs/ROLE_OUTPUT_SCHEMAS.md` | Output schema matters after roles are selected | Stage 2 |
| `docs/SCENARIO_TESTS.json` | Test asset, not runtime instruction | Self-audit / validator / routing-debug mode |
| `docs/OWNERSHIP_MATRIX.md` | Useful for handoffs, not first questions | Stage 2 planning |

### Keep in Stage 1

- `AGENTS.md`
- `TASK.md`
- `CHRONICLE.md`
- `docs/QUESTION_TREE.md`
- `docs/WORK_MODES.md`
- `docs/ROLE_ROUTING_MATRIX.md`
- `docs/QUALITY_GATES.md`
- `docs/RISK_POLICY.md`
- `docs/EVIDENCE_POLICY.md`
- `docs/LANGUAGE_POLICY.md`
- `docs/FAST_LANE.md`
- `docs/COMPLEXITY_MODEL.md`
- `docs/EXTERNAL_EVIDENCE_PROTOCOL.md`
- `docs/FINAL_FANTASY_CODENAME_POLICY.md`

### Add one small file

Add `docs/BOOTSTRAP_INDEX.md`, under ~2k characters, containing:

- work mode list;
- complexity tier summary;
- role budget summary;
- must-load docs by stage;
- “do not load deep playbooks until selected.”

Then Stage 1 can load:

```text
AGENTS.md
TASK.md
CHRONICLE.md
docs/BOOTSTRAP_INDEX.md
docs/QUESTION_TREE.md
docs/LANGUAGE_POLICY.md
```

That would make startup much lighter while preserving safety.

---

## 5. Simulation: Tiny copy change

### Task

“Переименуй кнопку `Send` в `Submit feedback` на экране feedback form.”

### Current framework behavior

Expected:

- Complexity: Tiny/Fast Lane
- Questions: 0–2
- Roles: `intake_orchestrator`, `ux_writer`, optional `frontend_architect`, optional `code_reviewer`
- No market, CX, AI, release, privacy, security, architecture planning.

Potential waste:

- Current Stage 1 loads ~71k characters before knowing the task is tiny.
- Required playbooks for `intake_orchestrator` + `ux_writer` add ~14k characters.
- This means a one-line copy change may start with ~85k characters of process context before touching code.

### Optimized behavior

Use **Micro Intake**:

1. Load only `AGENTS.md`, `TASK.md`, `CHRONICLE.md`, `BOOTSTRAP_INDEX.md`, `FAST_LANE.md`, `LANGUAGE_POLICY.md`.
2. Ask at most one question only if screen/file is unknown.
3. Use role cards, not full playbooks:
   - `ux_writer`: confirm wording and product language.
   - `frontend_architect`: locate file if needed.
4. Update `TASK.md` in one compact block only if files change.
5. Run minimal check: targeted test/build/lint if available.
6. Chronicle compact update.

Quality impact: **no quality loss**. The omitted docs cannot change the next decision.

---

## 6. Simulation: Greenfield UX MVP

### Task

“Собери MVP веб-приложения для сбора UX-инсайтов: проекты, интервью, инсайты, теги, карта повторяющихся тем, localStorage, без auth/backend.”

### Current expected routing

Required roles:

- `intake_orchestrator`
- `product_strategist`
- `ux_interaction_reviewer`
- `design_system_guardian`
- `frontend_architect`
- `qa_engineer`
- `chronicle_keeper`

Optional:

- `ux_writer`
- `delivery_manager`
- `code_reviewer`
- `team_architect`

This is a good Standard-tier routing.

### Current approximate loading

- Stage 1: ~70,989 characters
- Required playbooks: ~48,152 characters
- Total before repository code: ~119,141 characters

### Optimized routing

1. Stage 1 optimized: ~25,306 characters or less.
2. Load selected role summaries first, not full playbooks.
3. Load full playbooks only for roles whose artifact changes the plan:
   - Product Strategist: full
   - UX Interaction Reviewer: full
   - Frontend Architect: full
   - QA Engineer: full
   - Design System Guardian: summary/full depending on whether UI system is actually created
   - Chronicle Keeper: compact
4. Make `UX Writer` conditional:
   - required if UI copy is non-trivial, product language is important, onboarding/errors/empty states matter;
   - optional if copy can be placeholder-level.

Quality impact: **positive**. The plan becomes more decision-driven and less ceremonial.

---

## 7. Simulation: AI tool-using agent feature

### Task

“Add an AI agent that can read user data and perform irreversible actions after user confirmation.”

### Current routing

Required roles are correct:

- `intake_orchestrator`
- `ai_ml_systems_architect`
- `model_evaluation_specialist`
- `ai_safety_reviewer`
- `security_reviewer`
- `privacy_compliance_reviewer`
- `backend_architect`
- `qa_engineer`
- `chronicle_keeper`
- `consistency_auditor`

Optional roles are also reasonable:

- `api_contract_guardian`
- `observability_engineer`
- `performance_engineer`
- `devops_release_engineer`
- `ux_writer`

### Key recommendation

For AI tool-use, add a mandatory **Tool Permission Matrix** and **Irreversible Action Gate**.

Required artifact:

| Tool/action | Data access | Side effect | Risk | Confirmation required | Rollback possible | Owner | Tests/evals |
|---|---|---|---|---|---|---|---|

Also require:

- model behavior contract;
- prompt injection threat model;
- fallback/human escalation matrix;
- eval dataset strategy;
- monitoring signals;
- user-facing copy review for overpromising.

Quality impact: **positive**. This prevents the most dangerous AI-agent failure modes without adding unnecessary roles.

---

## 8. Process optimizations

### 8.1 Add “Decision-impact question rule”

Every intake question should pass this test:

> “Can the answer change scope, risk, team composition, acceptance criteria, verification, or approval gates?”

If not, do not ask it now.

Add to `QUESTION_TREE.md` and `task-intake/SKILL.md`.

### 8.2 Split Intake A into Micro / Standard / Risk-first

Current Intake A is one mechanism with budgets. Make it explicit:

| Intake type | Use when | Questions | Docs |
|---|---|---:|---|
| Micro Intake | Tiny/Fast Lane | 0–3 | minimal bootstrap |
| Standard Intake | normal feature/fix | 3–7 | routing + risk docs |
| Risk-first Intake | AI/security/privacy/migration/release | 5–9 + targeted | risk docs + relevant role summary |

### 8.3 Add role cards

Create `.agents/role_cards/*.md`, each under ~400–700 characters:

- role ID;
- codename;
- when to activate;
- artifact;
- must not do;
- load full playbook when.

Stage 2 should load role cards before full playbooks. Full playbooks are loaded only for selected roles that must produce artifacts.

### 8.4 Add `CONTEXT_BUDGET.md`

This is the most important resource optimization.

Track:

```markdown
## Context budget log
- Complexity tier:
- Question budget used:
- Role budget used:
- Core docs loaded:
- Playbooks loaded:
- Skills loaded:
- Repository areas inspected:
- Skipped docs/roles and rationale:
- Reason for any complexity escalation:
```

This makes resource discipline visible. Invisible budgets rot.

### 8.5 Add “selected role contract”

When Team Architect selects roles, each role should have:

| Role | Why selected | Artifact | Decision it supports | Stop condition |
|---|---|---|---|---|

If no artifact or decision exists, the role should be skipped.

### 8.6 Make Consistency Auditor more surgical

Current Squall can be expensive if always loaded fully. Add two modes:

- **Squall Lite**: 5-point check for Standard tasks.
- **Squall Full**: contradiction/risk/evidence/ownership audit for Complex/High-risk.

Squall Lite checklist:

1. Does plan match `TASK.md`?
2. Are risk gates respected?
3. Are selected roles justified?
4. Are assumptions labeled?
5. Is verification clear?

### 8.7 Add “review before code” caching pattern

For complex work:

1. Produce plan.
2. User approves.
3. Implementation prompt references only approved plan sections, not the whole planning conversation.
4. Chronicle stores compact decisions.

This improves quality and reduces token load in later implementation turns.

---

## 9. Role and methodology improvements

### 9.1 Fix role codename source of truth

Adopt `TEAM.md` and TOML descriptions as source of truth, then update playbooks.

### 9.2 Reduce boilerplate in playbooks

Repeated phrases found:

| Phrase | Count across playbooks |
|---|---:|
| `senior/principal-level specialist` | 42 |
| `role-specific method below` | 42 |
| `Operational checks:` | 42 |
| `explicit task-fit criteria...` | 309 |
| `applies this capability through the...` | 309 |

The problem is not repetition itself. The problem is that repeated expertise bullets make roles feel less genuinely specialized.

Recommendation:

- Keep universal sections short.
- Move universal instructions to `AGENTS.md` or `ROLE_OUTPUT_SCHEMAS.md`.
- In each playbook, replace generic expertise bullets with role-specific heuristics and concrete artifacts.

### 9.3 Create “top 15 deep protocols”

`ROLE_METHOD_LIBRARY.md` currently has deep protocols for key roles. Expand it to the top 15–18 most-used roles and keep it section-loadable.

Priority additions:

- Frontend Architect
- Backend Architect
- API Contract Guardian
- Data Architect
- Analytics Engineer
- Accessibility Specialist
- Performance Engineer
- Observability Engineer
- DevOps & Release Engineer
- Dependency Curator
- Migration Planner
- Delivery Manager
- Team Architect
- Chronicle Keeper

### 9.4 Separate “research planning” from “research execution”

Market/UX/CX roles should have two modes:

- **Planning mode:** produce protocol, sources, screener, search plan.
- **Execution mode:** synthesize actual evidence.

This prevents fake research when evidence is missing.

---

## 10. Scenario-test improvements

### Current state

`SCENARIO_TESTS.json` is good as a source of truth. Markdown scenarios are synchronized by count and ID.

### Missing layer

The validator does not simulate routing logic. It only checks that scenario role IDs exist and counts are valid.

### Recommended test harness

Add `scripts/run_scenario_tests.py` that checks:

- required roles are selected;
- forbidden roles are not selected;
- role count ≤ `max_roles`;
- question count ≤ `max_questions`;
- complexity tier matches expected;
- high-risk scenarios include relevant gates;
- review scenarios are read-only;
- language scenario obeys artifact/user language split.

Because Codex is not deterministic, this test harness can validate **expected routing declarations** and **prompt outputs** when pasted into test fixtures.

---

## 11. Suggested ULTIMATE Pro Backlog

### P0 — must fix

1. Fix codename drift between `TEAM.md`, TOML, playbooks, and docs.
2. Add validator check for codename/title consistency.
3. Move `TEAM.md`, `ROLE_METHOD_LIBRARY.md`, `ROLE_OUTPUT_SCHEMAS.md`, `SCENARIO_TESTS.json`, and `OWNERSHIP_MATRIX.md` out of mandatory Stage 1.
4. Add `BOOTSTRAP_INDEX.md` for lean startup.
5. Add `CONTEXT_BUDGET.md` or a context-budget section in `TASK.md`/`CHRONICLE.md`.

### P1 — high-value optimization

6. Add role cards and load them before full playbooks.
7. Add Decision-impact question rule.
8. Add Micro/Standard/Risk-first intake modes.
9. Add Squall Lite / Squall Full modes.
10. Add Tool Permission Matrix for AI tool-use scenarios.
11. Add selected-role contract table.

### P2 — quality depth

12. Replace repetitive expertise boilerplate with role-specific heuristics.
13. Expand `ROLE_METHOD_LIBRARY.md` to top 15–18 roles.
14. Split research planning vs research execution.
15. Add stricter output schemas for AI/security/privacy/API/migration/release.

### P3 — telemetry and continuous improvement

16. Add lightweight usage telemetry fields:
    - roles proposed;
    - roles used;
    - roles skipped;
    - docs loaded;
    - questions asked;
    - verification run;
    - rework needed.
17. Add retrospective prompt after failed/reworked tasks.
18. Add over-routing detection:
    - if more than 30% selected roles produce no decision-changing output, update routing rules.

---

## 12. Final recommendation

Do not add more roles now. The team is already large enough.

The next version should be:

**Codex Product Team ULTIMATE Pro v1.4 — Routing Integrity & Context Budget Patch**

The goal should be:

- fix codename integrity;
- make startup leaner;
- add context-budget observability;
- make role activation more decision-driven;
- keep quality gates strict;
- reduce resource usage by loading deep expertise only when it changes the next decision.

This is not “optimization for optimization’s sake.” It improves quality because it reduces noise, prevents role confusion, and makes every selected role accountable for a concrete decision-support artifact.
