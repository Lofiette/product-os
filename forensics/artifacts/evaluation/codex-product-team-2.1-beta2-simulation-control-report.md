# Codex Product Team 2.1 beta 2 — Simulation & Context-Economy Control Audit

Verdict: **PASS WITH TARGETED FIXES BEFORE 2.1 beta 3 / RC**

This audit checks the uploaded `codex-product-team-2.1-beta2.zip` as a working runtime system, with special focus on context economy, ticketed memory, skill routing, UI/DS quality gates, and whether `SKILL_TINY_INDEX.json` can be reduced without harming effectiveness.

## 1. Automated checks

Executed from unpacked archive:

```text
python3 scripts/validate_kit.py
python3 scripts/test-routing.py
node scripts/check-memory-integrity.mjs
node --check scripts/*.mjs
python3 -m py_compile scripts/*.py
unzip -t codex-product-team-2.1-beta2.zip
```

Results:

```text
VALIDATION PASSED: 49 roles, 84 skills, 28 scenarios.
ROUTING TEST PASSED: 28 scenarios, 49 roles, 84 skills.
MEMORY INTEGRITY PASSED.
Node syntax checks: PASS.
Zip integrity: PASS.
```

Important exception:

```text
./scripts/validate_kit.py
```

fails when executed directly because the file begins with an extra backslash before the shebang:

```text
\
#!/usr/bin/env python3
```

Running it via `python3 scripts/validate_kit.py` works, but executable mode is broken. This should be a P0 fix because validators must be boring and reliable.

---

## 2. Ticketed memory simulation

The 2.1 memory architecture is conceptually correct:

```text
CURRENT.md          — current control panel
TASK_INDEX.md       — compact ticket ledger
tasks/TKT-*.md      — detailed active task context
CHRONICLE.md        — compact rescue summary
TASK.md             — deprecated compatibility pointer only
context/packets/*   — operation evidence packets
context/snapshots/* — recovery checkpoints
chronicle/*         — detailed logs, not runtime default
archive/*           — old material, never runtime default
```

Current sizes:

```text
AGENTS.md                9,311 chars
CURRENT.md               2,176 chars
TASK_INDEX.md              703 chars
CHRONICLE.md             1,256 chars
docs/BOOTSTRAP_INDEX.md  3,200 chars
docs/LANGUAGE_POLICY.md    435 chars
Tier 0 total            17,081 chars
```

Tier 0 is now healthy. The ticketed model is doing its job: `TASK.md` is only 807 bytes and no longer stores scope, acceptance criteria, or history.

### Memory simulation outcome

For a long-running task, the architecture should work well if Codex follows the policy:

1. Load Tier 0.
2. Identify active ticket.
3. Load only active ticket.
4. Load relevant skill/gate docs for the current operation.
5. Use `context/packets/*` for evidence.
6. Use `context-snapshot` and `context-prune` after major phases or compression.

### Runtime risk

`FIRST_PROMPT.md` and `AGENTS.md` still instruct Codex to load both `ROLE_TINY_INDEX.json` and `SKILL_TINY_INDEX.json` after intake for role/skill routing. This is right for Standard+ tasks, but unnecessary for obvious Tiny tasks.

Recommended adjustment:

```text
Tiny/Micro tasks:
- do not load tiny indexes by default;
- use direct main-thread handling unless routing is ambiguous.

Fast/Standard+ tasks:
- load ROLE_TINY_INDEX and SKILL_TINY_INDEX after intake.
```

This saves context without reducing quality.

---

## 3. SKILL_TINY_INDEX analysis

Current index sizes:

```text
docs/SKILL_TINY_INDEX.json   10,206 bytes
docs/SKILL_INDEX.json        15,226 bytes
```

`SKILL_TINY_INDEX.json` contains 84 entries with only:

```json
{"id":"skill-id","tr":"short trigger description"}
```

This is already close to the minimum useful shape. It does **not** contain long descriptions, schemas, examples, or category metadata.

### Can it be reduced without harming effectiveness?

**Not much by shortening entries.** The current `tr` field is doing useful routing work. Cutting descriptions further would risk reducing recall, especially for subtle skills such as:

```text
reference-fidelity
manifest-freeze-check
design-source-authority
expectation-anticipation
content-realism-review
subagent-failure-recovery
```

The better optimization is **conditional loading**, not aggressive shrinking.

### Recommended approach

Keep `SKILL_TINY_INDEX.json` readable enough for effective routing, but add a smaller first-stage router:

```text
docs/SKILL_ROUTER_INDEX.json
```

Example:

```json
{
  "ui_design": ["design-recon", "screen-redesign", "prototype-ui-kit", "taste-review"],
  "design_system": ["design-system-compliance", "manifest-freeze-check", "component-contract-scan"],
  "memory": ["ticket-router", "task-ledger", "context-prune", "memory-integrity-check"],
  "subagents": ["subagent-run-contract", "subagent-failure-recovery"],
  "production": ["production-service-planning", "production-readiness-review"],
  "ai": ["ai-ml-planning", "model-evaluation", "ai-safety-review"]
}
```

Then the runtime can do:

```text
1. Use SKILL_ROUTER_INDEX for domain shortlist.
2. Load SKILL_TINY_INDEX only for selected domains or when routing is unclear.
3. Load SKILL_INDEX or SKILL.md only after selecting the operation.
```

This improves context economy without weakening routing quality.

Conclusion: **do not aggressively shrink `SKILL_TINY_INDEX.json`; change when it is loaded and add a domain router.**

---

## 4. Context budget simulation by task type

Estimated load includes:

```text
Tier 0 + active TKT-000 + ROLE_TINY_INDEX + SKILL_TINY_INDEX + required role cards + required SKILL.md files
```

This is a rough upper-bound estimate; real usage depends on whether Codex actually loads all selected skill files before execution.

| Scenario | Roles | Skills | Approx. chars | Rough tokens /4 | Notes |
|---|---:|---:|---:|---:|---|
| tiny_copy_change | 0 | 0 | 37,133 | 9,283 | Too high if tiny indexes are loaded. Should skip indexes. |
| ui_prototype_no_ds | 3 | 5 | 51,556 | 12,889 | Healthy for Standard UI work. |
| taste_sensitive_ui_concept_no_ds | 2 | 6 | 52,275 | 13,068 | Healthy; taste skills add value. |
| reference_driven_ui_prototype_blocking | 3 | 6 | 51,848 | 12,962 | Healthy; must enforce reference gates. |
| current_page_ui_review_bounded | 3 | 4 | 47,436 | 11,859 | Good, but only if UI Review Packet is bounded. |
| module_design_handoff_ds | 6 | 6 | 56,371 | 14,092 | Acceptable; module design is naturally complex. |
| production_web_service_code_ds | 8 | 7 | 58,802 | 14,700 | Acceptable only with phased orchestration. |
| context_prune_after_long_work | 1 | 3 | 40,401 | 10,100 | Higher than ideal; memory operations can skip role/skill indexes. |

Key finding: **the main waste is not the size of `SKILL_TINY_INDEX`; it is loading indexes when the task is obvious.**

---

## 5. Simulation: Tiny copy change

User task:

```text
Change “Send” to “Submit feedback”.
```

Expected runtime:

```text
Complexity: Tiny
Orchestration: main_thread_only
Roles: none or ux_writer lens only
Skills: none by default
Subagents: forbidden
Questions: 0–1
Memory: Tier 0 + active ticket only, or even direct Fast Lane note
```

Beta 2 issue:

The current staged-loading text says after intake load `ROLE_TINY_INDEX.json` and `SKILL_TINY_INDEX.json`. For tiny mechanical tasks this is unnecessary.

Recommended beta 3 change:

```text
For Tiny/Micro tasks, do not load role/skill indexes unless routing is ambiguous.
```

This improves context economy and does not reduce quality.

---

## 6. Simulation: UI prototype without design system

User task:

```text
Create a fast redesign concept for an existing interface. No design system. Make it calm, premium, clearer.
```

Expected:

```text
Complexity: Standard
DS mode: none
Required roles: product_designer, design_engineer
Usually: design_system_guardian as Prototype UI Kit Guardian, ux_writer if copy/states matter
Skills: design-recon, prototype-ui-kit, taste-calibration, screen-redesign, state-matrix, taste-review
```

Beta 2 is mostly good here:

```text
- prototype-ui-kit exists;
- taste-calibration exists;
- taste-review exists;
- scenario taste_sensitive_ui_concept_no_ds exists;
- no-DS work has local UI contract path.
```

Remaining risk:

`design_system_guardian` is semantically odd when DS mode is `none`. It should be explicitly described as acting as:

```text
Prototype UI Kit Guardian
```

for no-DS prototypes.

Recommended beta 3 change:

```text
Add no-DS alias behavior in design_system_guardian playbook and role card:
When DS mode = none, own local Prototype UI Kit Contract consistency, not DS compliance claims.
```

---

## 7. Simulation: Reference-driven UI prototype

User gives a reference screenshot and asks Codex to implement a similar interface.

Expected:

```text
Before implementation:
- reference-fidelity
- design-source-authority
- manifest-freeze-check if DS manifest exists/is generated
- taste-calibration / example-taste-board if examples matter
- Screen Design Spec or Reference Fidelity Spec

After implementation:
- screenshot-reference-comparison
- visual-qa-loop
- content-realism-review
- debug-control-review if relevant
- final PASS/WARN/BLOCKED
```

Beta 2 has all required skills and scenarios.

Remaining risk:

The scenario layer checks that skills exist, but not that the workflow blocks implementation before Reference Fidelity Spec.

Recommended beta 3 change:

Add behavioral validation in `test-routing.py`:

```text
if scenario.must_not_implement_before_reference_spec == true:
  assert required_skills include reference-fidelity
  assert required_skills include design-source-authority
  assert required_skills include screenshot-reference-comparison for post-render
  assert scenario requires approval/gate before implementation
```

---

## 8. Simulation: Current rendered page UI review

User asks to review a current page or prototype.

Expected:

```text
1. ui-review-packet
2. current-page-ui-review
3. max 1–2 spawned reviewers by default
4. subagent-run-contract before spawn
5. subagent-failure-recovery if any agent hangs
6. no PASS if evidence is missing
```

Beta 2 has these skills and scenario:

```text
current_page_ui_review_bounded
subagent_hang_recovery
subagent_bounded_ticket_packet
```

Good.

Remaining risk:

The scenario checks existence more than behavior. It should verify:

```text
max_spawned_agents_default <= 2
requires_approval_before_spawn == true
ui-review-packet is required
current-page-ui-review is required
subagent-failure-recovery scenario exists
```

---

## 9. Simulation: Module design for developer rebuild

User task:

```text
Design a full product module for later developer rebuild using documented design-system rules. Do not implement code.
```

Expected:

```text
Mode: design_only_handoff
Roles: product_designer, information_architect, design_system_guardian, ux_writer, design_engineer, qa_engineer
Skills: design-recon, module-design, design-system-manifest, design-system-compliance, design-handoff-qa, handoff-docs
Must not implement code.
```

Beta 2 scenario correctly includes:

```text
must_not_implement: true
must_not_spawn_without_approval: true
requires_approval_before_spawn: true
```

Remaining issue:

There is no separate `developer-rebuild-brief` skill, although the template exists conceptually in the process.

Recommended beta 3 change:

Either:

```text
Option A: add `developer-rebuild-brief` skill.
Option B: explicitly upgrade `handoff-docs` to own Developer Rebuild Brief when mode = design_only_handoff.
```

For context economy, Option B is enough unless real tests show ambiguity.

---

## 10. Simulation: Production web service with DS in code

Expected phased flow:

```text
Phase 1: repo-recon + design-recon
Phase 2: product/design/architecture plan
Phase 3: risk/readiness gates
Phase 4: implementation or handoff
Phase 5: verification/review
```

Required skills in scenario:

```text
repo-recon
design-recon
production-service-planning
production-readiness-review
design-system-compliance
ds-code-contract-enforcement
implementation-review
```

Good.

Remaining risks:

1. `visual-qa-loop` is not required in `production_web_service_code_ds`, even though production UI with DS in code should include visual QA when UI is affected.
2. `component-contract-scan` is not explicitly required.
3. Risk-first intake is described but not strongly scenario-tested.

Recommended beta 3 change:

```text
Add visual-qa-loop and component-contract-scan to production UI scenarios.
Add scenario flag: must_use_risk_first_intake.
Add test-routing checks for this flag.
```

---

## 11. Script simulation: strict DS scanner

A synthetic test was run:

```tsx
export function App(){ return <><button>Bad native</button><input /></> }
```

With a manifest defining DS `Button` and `Input`, running:

```bash
node scripts/check-component-imports.mjs src --manifest DESIGN_SYSTEM_MANIFEST.json --fail-on-violation
```

returns warnings, but exits `0`:

```text
WARNING native-primitive-used-while-ds-component-exists ... Button
WARNING native-primitive-used-while-ds-component-exists ... Input
0 violation(s), 2 warning(s).
exit:0
```

This is too soft for documented/governed DS mode.

Recommended beta 3 change:

```text
Add --strict-ds or --fail-on-warning.
When DS mode is documented_ds/governed_ds, native primitives that duplicate DS components should fail unless file is inside DS component source or an approved exception list.
```

---

## 12. Legacy / inconsistencies found

### 12.1 `implementation-review` index description still says TASK

In `docs/SKILL_INDEX.json` and `docs/SKILL_TINY_INDEX.json`:

```text
Review implementation against TASK...
```

The skill file itself is correct and says active ticket. The indexes should be corrected to:

```text
Review implementation against active ticket, approved plan, tests, gates, risks...
```

### 12.2 `ROLE_ROUTING_MATRIX.md` and `SKILL_ROUTING_MATRIX.md` contain duplicated taste sections

This is not breaking, but it increases ambiguity and context noise.

Recommendation:

```text
Merge duplicate taste/anticipation sections into one canonical block per file.
```

### 12.3 Release notes/self-audit docs remain in docs/

They are reference-only but still live next to runtime docs:

```text
docs/SELF_AUDIT_REPORT.md
docs/RELEASE_NOTES_*.md
```

Recommendation:

```text
Move to archive/release-notes/ and archive/audits/.
```

---

## 13. Recommended beta 3 scope

### P0 — must fix

1. Remove leading `\` from `scripts/validate_kit.py`.
2. Add executable/shebang validation to `validate_kit.py`.
3. Add strict DS mode to `check-component-imports.mjs`:
   - `--strict-ds`
   - `--fail-on-warning`
   - ignore DS component source files to avoid false positives.
4. Change Tiny/Micro policy: do not load role/skill tiny indexes by default for obvious tiny tasks.
5. Fix `implementation-review` index descriptions to say active ticket, not TASK.

### P1 — should fix

6. Add `SKILL_ROUTER_INDEX.json` by domain; keep `SKILL_TINY_INDEX.json` mostly as-is.
7. Strengthen `test-routing.py` to validate behavioral scenario fields.
8. Add `visual-qa-loop` and `component-contract-scan` to production UI scenario where UI is affected.
9. Clarify no-DS behavior for `design_system_guardian` as Prototype UI Kit Guardian.
10. Merge duplicate taste/anticipation routing sections.

### P2 — nice / cleanup

11. Move release notes and self-audit docs to archive.
12. Normalize executable bits on scripts or document invocation style consistently.
13. Add a direct memory simulation test for context-prune/context-snapshot lifecycle.

---

## 14. Final answer on SKILL_TINY_INDEX

Do **not** aggressively shrink `SKILL_TINY_INDEX.json` itself. It is already minimal enough and carries useful trigger text. Shrinking it further risks worse routing.

The better optimization is:

```text
- do not load it for Tiny/Micro tasks;
- add a smaller SKILL_ROUTER_INDEX.json for domain-level shortlist;
- load SKILL_TINY_INDEX only after domain/routing uncertainty remains;
- load full SKILL.md only for selected operation.
```

This preserves effectiveness while improving context economy.

## 15. Overall verdict

2.1 beta 2 is a solid context-economy release. Ticketed memory is correctly implemented and should materially reduce context bloat. The main remaining issues are not conceptual; they are runtime polish and enforcement:

```text
validator executable bug;
strict DS enforcement too soft;
tiny indexes loaded too often;
behavioral scenario checks still shallow;
a few legacy TASK references in indexes;
routing docs contain duplicate taste sections.
```

The right beta 3 is not a big rewrite. It should be a focused hardening patch.
