# Codex Product Team 2.0 beta 2 — Simulation Audit

**Scope:** static validation + practical runtime simulations against the uploaded `codex-product-team-2.0-beta2` archive.

**Verdict:** `PASS WITH IMPORTANT RUNTIME FIXES`

Beta 2 is directionally strong. The framework now has culture, taste, anticipation, UI/design-system gates, role-skill architecture, and explicit spawned/simulated execution transparency. But several practical issues can still cause Codex to produce a polished process report while missing the intended operational behavior.

## 0. Baseline checks

Actual archive results:

```text
VALIDATION PASSED: 49 roles, 66 skills, 16 scenarios.
ROUTING TEST PASSED: 16 scenarios, 49 roles, 66 skills.
Node syntax checks: PASS
Zip integrity: OK
```

Important correction: this archive contains **66 skills and 16 scenarios**, not 69 skills and 20 scenarios.

## 1. Major findings

### P0-1. Custom agent TOML files reference wrong doc paths

All 49 `.codex/agents/*.toml` files contain instructions like:

```text
Use TASK.md, EVIDENCE_POLICY.md, QUALITY_GATES.md, SUBAGENT_ORCHESTRATION.md...
```

But the actual files are under `docs/`:

```text
docs/EVIDENCE_POLICY.md
docs/QUALITY_GATES.md
docs/SUBAGENT_ORCHESTRATION.md
```

**Why this matters:** spawned subagents may fail to load the policy docs we expect them to use, especially evidence, gates, and orchestration rules.

**Fix:** update all TOML files to reference exact paths:

```text
Use TASK.md, docs/EVIDENCE_POLICY.md, docs/QUALITY_GATES.md, docs/SUBAGENT_ORCHESTRATION.md...
```

For design-facing agents, add selective references:

```text
docs/UI_QUALITY_GATES.md
docs/DESIGN_SYSTEM_MODES.md
docs/TASTE_PROFILE.md
docs/TASTE_REVIEW.md
```

Only add those where relevant to avoid doc bloat.

---

### P0-2. Agent naming policy is not a first-class doc

The archive removed codenames, and the core docs require exact `role_id` for spawned agents. Good. But there is no dedicated `docs/AGENT_NAMING_POLICY.md`.

**Observed risk:** Codex UI or the model may still display arbitrary thread labels such as human names. The framework should state that such labels are UI/thread labels only and must not appear in artifacts or role contracts.

**Fix:** add:

```text
docs/AGENT_NAMING_POLICY.md
```

Rules:

```text
- Use only exact role_id / agent_id in artifacts.
- Do not invent names, nicknames, codenames, philosopher names, or persona labels.
- If the Codex UI displays a generated thread label, ignore it in formal outputs.
- Spawn table must use `.codex/agents/<role_id>.toml` name values.
```

Add validator check for the file and phrases.

---

### P0-3. Playbooks contain a confusing self-orchestration rule

All playbooks include:

```text
Do not spawn other agents directly; request orchestration through Team Architect.
```

This is acceptable for specialist roles, but confusing for `team_architect` and `intake_orchestrator`. In real workflow, the main orchestration thread is the one that must spawn approved agents. Team Architect should propose the lineup; the main thread executes spawn.

**Fix:** replace the generic line with role-type-specific wording:

For specialist roles:

```text
Do not spawn subagents. Request additional roles/skills through the main orchestration thread.
```

For `team_architect`:

```text
Own the orchestration proposal. The main thread executes real subagent spawn only after user approval.
```

For `intake_orchestrator`:

```text
Classify and propose routing; do not spawn agents during intake.
```

---

### P1-1. `ROLE_MINI_INDEX.json` is not actually mini enough

File sizes:

```text
docs/ROLE_INDEX.json       43,359 bytes
docs/ROLE_MINI_INDEX.json  25,135 bytes
docs/SKILL_INDEX.json      11,731 bytes
```

After intake, the framework asks Codex to load both role and skill indexes. That is roughly 36 KB before role cards, playbooks, skills, repo files, or design docs.

**Why this matters:** not a correctness bug, but it weakens the resource-efficiency goal.

**Fix:** add:

```text
docs/ROLE_TINY_INDEX.json
docs/SKILL_TINY_INDEX.json
```

Keep only:

```json
{
  "id": "product_designer",
  "category": "Design & UX",
  "triggers": ["screen redesign", "UI prototype"],
  "artifact": "Screen Design Spec",
  "default_skills": ["design-recon", "screen-redesign"]
}
```

Use full mini index only after initial shortlist.

---

### P1-2. Skill discovery may still be too crowded

The skill metadata in `SKILL_INDEX.json` is about 11.7 KB. Codex skills use progressive disclosure, but the initial visible skill list has its own budget and can be shortened/omitted when many skills are installed. This means relying on implicit skill triggering for 66 skills is fragile.

**Fix:** for critical workflows, the framework should explicitly mention selected skills in the orchestration proposal rather than hoping implicit skill discovery finds them.

Critical explicit skills for UI/design work:

```text
design-recon
prototype-ui-kit
screen-redesign
state-matrix
design-system-manifest
design-system-compliance
visual-qa-loop
taste-calibration
taste-review
example-taste-board
```

---

### P1-3. `example-taste-board` is under-routed

Beta 2 added good/bad examples as a taste layer, but scenario tests do not require `example-taste-board` when good/bad examples are central.

**Fix:** add scenario:

```text
taste_examples_redesign
```

Required skills:

```text
taste-calibration
example-taste-board
screen-redesign
taste-review
```

Also update `FIRST_PROMPT.md`: if the user provides good/bad examples, explicitly propose `example-taste-board`.

---

### P1-4. UI prototype without DS lacks mandatory visual QA in scenario

`ui_prototype_no_ds` currently requires:

```text
design-recon
prototype-ui-kit
screen-redesign
state-matrix
ui-heuristic-audit
```

For implementation/prototype tasks, add:

```text
visual-qa-loop
```

Optional but recommended:

```text
e2e-visual-state-capture
```

If no render is possible, final output must state `Visual QA: NOT RUN` with reason.

---

### P1-5. Module design handoff needs a sharper developer rebuild workflow

`module_design_handoff_ds` correctly uses `module-design` and `design-handoff-qa`, but also requires generic `handoff-docs`. The generic skill is weak for this scenario.

**Fix:** either:

1. Add `developer-rebuild-brief` skill, or
2. Upgrade `handoff-docs` with a dedicated branch for developer rebuild.

Also add missing template:

```text
.agents/templates/design-handoff-qa-report.md
```

The skill has an output schema, but the template file is absent.

---

### P1-6. Production web-service route needs risk-first questions

The production scenario marks security/privacy/devops/performance as optional. That is okay if risk triggers drive them. The problem is that `FIRST_PROMPT.md` and `QUESTION_TREE.md` should force a tiny risk-first branch for production work.

Add mandatory production risk questions:

```text
- Does this service handle auth, permissions, personal/sensitive data, payments, file uploads, or user-generated content?
- Is there a production deployment/release target?
- Are there SLA/reliability/performance expectations?
- Are irreversible actions, data deletion, or external side effects involved?
- Is there a rollback strategy requirement?
```

If any answer is yes, risk roles become required, not optional.

---

### P2-1. Design System Guardian role is overloaded in `none` DS mode

In no-DS scenarios, `design_system_guardian` is required to enforce local prototype consistency. This works, but the role title can bias Codex toward searching for a DS that does not exist.

**Fix options:**

- Keep the role, but add a no-DS mode note: “When DS mode is `none`, act as Prototype UI Kit Guardian.”
- Or add a small skill-level alias, not a new role: `prototype-consistency-guardian`.

---

### P2-2. Component scanner can be noisy

`check-component-imports.mjs` is useful and no longer a placeholder. But primitive warnings (`<button>`, `<input>`) may also fire inside DS component implementation files.

**Fix:** suppress primitive warnings in allowed DS source files and DS implementation directories from the manifest.

---

### P2-3. Build-time docs remain in runtime package

Files like `SELF_AUDIT_REPORT.md` and release notes are useful for humans, but should be marked build-time/reference-only. They should not be loaded during runtime tasks.

**Fix:** add `docs/RUNTIME_LOAD_POLICY.md` with:

```text
Runtime docs
Reference-only docs
Build-time docs
Never-load-by-default docs
```

## 2. Simulations

### Simulation A — Concept redesign of existing system, quick prototype, no design system

**Prompt shape:**

```text
Need a quick concept redesign prototype for an existing system. There is no design system. Quality and taste matter.
```

**Expected beta 2 routing:**

```text
Work mode: design prototype / concept redesign
Complexity: Standard
DS mode: none
Orchestration: hybrid or role simulation first
```

**Expected roles:**

```text
Required:
- product_designer
- design_engineer

Usually:
- design_system_guardian as prototype UI kit consistency owner
- ux_writer if user-facing copy/states exist
- visual_design_director if visual direction is open

System services:
- intake_orchestrator
- chronicle_keeper compact update
- consistency_auditor lite if plan changes
```

**Expected skills:**

```text
repo-recon, if existing repo
design-recon
prototype-ui-kit
taste-calibration
screen-redesign
state-matrix
ui-heuristic-audit
taste-review
visual-qa-loop if implementation/render exists
```

**Expected artifacts:**

```text
Taste Profile
Prototype UI Kit Contract
Screen Design Spec
State Matrix
Design Diff Summary
UI Heuristic Audit
Taste Review
Visual QA Report or NOT RUN reason
```

**Passes:**

- `design-recon`, `prototype-ui-kit`, `screen-redesign`, and `state-matrix` exist and are operational.
- Taste layer exists and is well framed as non-roleplay.
- No-DS mode is explicitly handled.

**Potential breakpoints:**

1. `ui_prototype_no_ds` scenario does not require taste-calibration/taste-review unless the separate taste scenario is selected.
2. `visual-qa-loop` is not required in the no-DS prototype scenario.
3. `example-taste-board` is not triggered when user provides good/bad examples.
4. `design_system_guardian` in no-DS mode may be conceptually confusing unless explicitly reframed.

**Recommended patch:**

- Add scenario `concept_redesign_no_ds_taste`.
- Add `example-taste-board` and `visual-qa-loop` to relevant UI prototype routes.
- Add no-DS role note for Design System Guardian.

---

### Simulation B — Full product module design, developer rebuild later, DS rules apply

**Prompt shape:**

```text
Design a full product module. Do not implement code. Developer will rebuild it later using our documented design-system rules.
```

**Expected routing:**

```text
Work mode: design-only handoff
Complexity: Complex
DS mode: documented_ds or governed_ds
Implementation: forbidden unless approved later
```

**Expected roles:**

```text
product_designer
information_architect
design_system_guardian
ux_writer
design_engineer as handoff feasibility reviewer
qa_engineer for design QA
```

**Expected skills:**

```text
design-recon
design-system-manifest
module-design
design-system-compliance
design-handoff-qa
handoff-docs or developer-rebuild-brief
```

**Expected artifacts:**

```text
Design Recon Brief
DS Manifest / DS Source-of-Truth Summary
Module Design Package
Component Matrix
Content Matrix
State Matrix
Developer Rebuild Brief
Design Handoff QA Report
```

**Passes:**

- The scenario exists and correctly says `must_not_implement: true`.
- `module-design` is concrete and useful.
- `design-handoff-qa` protects developer rebuild quality.

**Potential breakpoints:**

1. `handoff-docs` is generic and may produce PR-style notes rather than developer rebuild instructions.
2. No dedicated `developer-rebuild-brief` skill exists, despite template file existing.
3. Missing `design-handoff-qa-report.md` template.
4. Taste/example logic is optional; for a module with a strong desired feel, it should be included.

**Recommended patch:**

- Add `developer-rebuild-brief` skill.
- Add `design-handoff-qa-report.md` template.
- Add DS Evidence Map requirement: every component/pattern decision must reference DS source or approved deviation.

---

### Simulation C — Production web service, design system in code

**Prompt shape:**

```text
Design and implement a production web service in an existing repo. The design system exists in code.
```

**Expected routing:**

```text
Work mode: production web/service
Complexity: High-risk or Complex depending on auth/data/deploy
Orchestration: phased, not one giant team
DS mode: component_library / documented_ds / governed_ds
```

**Expected phases:**

```text
Phase 1: repo-recon + design-recon + DS manifest
Phase 2: product/design/architecture planning
Phase 3: risk/readiness routing
Phase 4: approved implementation or handoff
Phase 5: verification, DS enforcement, visual QA, code review
```

**Expected roles:**

```text
Initial planning:
- product_strategist
- solution_architect
- frontend_architect
- backend_architect
- product_designer
- design_system_guardian
- design_engineer
- qa_engineer

Risk roles triggered by answers:
- security_reviewer
- privacy_compliance_reviewer
- api_contract_guardian
- data_architect
- devops_release_engineer
- performance_engineer
```

**Expected skills:**

```text
repo-recon
design-recon
design-system-manifest
production-service-planning
production-readiness-review
design-system-compliance
ds-code-contract-enforcement
implementation-review
visual-qa-loop
```

**Passes:**

- Phased orchestration exists and is sensible.
- Production scenario exists.
- DS code contract scripts exist and pass syntax check.

**Potential breakpoints:**

1. Risk roles are optional, and intake may not ask enough risk-first questions.
2. Production may try to propose a big team before recon unless Phase 1 is enforced.
3. DS scanners are heuristic and may be noisy or incomplete.
4. `visual-qa-loop` is not part of production scenario required skills, even though production UI with DS in code should include visual/design QA when UI is affected.

**Recommended patch:**

- Add `risk-first-intake` branch for production work.
- Add `visual-qa-loop` and `component-contract-scan` to production UI route when UI affected.
- Enforce “Recon first, then spawn specialists” for production tasks with unknown repo/DS state.

---

### Simulation D — Subagent orchestration transparency

**Prompt shape:**

```text
Use true subagent workflow. Spawn product_designer, design_engineer, design_system_guardian.
```

**Expected behavior:**

```text
Before spawn:
- show approval table if not already approved
- use exact agent IDs

After approval:
- write: Now spawning real subagents: product_designer, design_engineer, design_system_guardian
- wait for results
- consolidate conflicts
```

**Passes:**

- `SUBAGENT_ORCHESTRATION.md` has the critical distinction.
- `FIRST_PROMPT.md` requires spawned vs simulated status.

**Potential breakpoints:**

1. TOML files reference wrong doc paths.
2. No dedicated agent naming policy doc.
3. The UI may display generated thread labels; framework should explicitly ignore them in formal artifacts.
4. Specialist playbooks all say “request orchestration through Team Architect,” including Team Architect itself.

**Recommended patch:**

- Fix TOML paths.
- Add `AGENT_NAMING_POLICY.md`.
- Normalize playbook orchestration language.

---

### Simulation E — Taste, good/bad examples, and anticipation

**Prompt shape:**

```text
Make this prototype feel strict, modern, not corporate-dead. Good example: X. Bad example: Y. Suggest improvements if you see better paths, but ask before changing scope.
```

**Expected routing:**

```text
taste-calibration
example-taste-board
screen-redesign / module-design
creative-tension-review if quality can improve
taste-review
expectation-anticipation for proactive proposal cards
```

**Passes:**

- Taste profile docs are good and operational.
- Taste review is evidence-based and uses PASS/WARN/BLOCKED.
- Expectation anticipation has safe EA classes.

**Potential breakpoints:**

1. `example-taste-board` is not sufficiently wired into `FIRST_PROMPT.md` or scenario tests.
2. Anticipation can still become extra chatter unless tied to “materially changes outcome”.
3. Taste Review might be skipped if the system treats the task as implementation-only.

**Recommended patch:**

- Add explicit route: if good/bad examples are provided, use `example-taste-board`.
- Add final gate: if `TASK.md` taste profile exists, final design/UI output must include Taste Review or an explicit skip.
- Add validator check that taste-driven scenarios include taste-review.

## 3. Unused or legacy-ish parts

### Keep, but mark reference/build-time only

```text
docs/SELF_AUDIT_REPORT.md
docs/RELEASE_NOTES_2.0.md
docs/RELEASE_NOTES_2.0_BETA1.md
docs/RELEASE_NOTES_2.0_BETA2.md
docs/ROLE_METHOD_LIBRARY.md
docs/ROLE_OUTPUT_SCHEMAS.md
```

These are useful, but should not be loaded by default during runtime tasks.

### Needs tightening

```text
docs/ROLE_MINI_INDEX.json
```

It is too large for a “mini” runtime index. Add a truly tiny routing index.

### Missing but useful

```text
docs/AGENT_NAMING_POLICY.md
docs/RUNTIME_LOAD_POLICY.md
.agents/templates/design-handoff-qa-report.md
.agents/skills/developer-rebuild-brief/SKILL.md
```

## 4. Recommended beta 3 patch list

### P0

1. Fix all custom agent TOML doc paths.
2. Add `AGENT_NAMING_POLICY.md` and validator check.
3. Replace generic playbook orchestration language with role-type-specific rules.
4. Add `developer-rebuild-brief` skill or upgrade `handoff-docs` for design-only developer rebuild.
5. Add missing `design-handoff-qa-report.md` template.

### P1

6. Add `ROLE_TINY_INDEX.json` and `SKILL_TINY_INDEX.json`.
7. Add `risk-first-intake` branch for production tasks.
8. Update UI no-DS routes to include taste and visual QA when quality/implementation matters.
9. Wire `example-taste-board` into first prompt, routing, and scenarios.
10. Add production UI route requirements for `visual-qa-loop` and `component-contract-scan`.

### P2

11. Add `RUNTIME_LOAD_POLICY.md`.
12. Suppress DS implementation false positives in component scanner.
13. Add executable scenario tests that verify required/optional/forbidden roles per scenario, not only existence.
14. Add final-output checklist for “spawned vs simulated, gates, artifacts, blockers, deviations.”

## 5. Final assessment

Beta 2 is a serious improvement. The product/design quality layer is now meaningful, and taste is framed as an operational standard instead of emotional roleplay.

The main remaining issue is not missing theory. It is runtime enforcement:

```text
Right docs must be loaded by spawned agents.
Right skills must be explicitly selected.
Right artifacts must be mandatory for each task type.
Right gates must return BLOCKED when violated.
Right indexes must be light enough to use.
```

If beta 3 fixes TOML paths, naming policy, routed taste examples, visual QA requirements, and developer-rebuild handoff, the framework will move much closer to a truly operational 2.0 release candidate.
