# Codex Product Team 3.0 Ultra — Control Audit

## Verdict

**PASS WITH TARGETED FIXES BEFORE 3.0 RC / beta 2.**

The archive is structurally healthy and much stronger than 2.x architecturally. Built-in validation passes, the full role library is preserved, `frontend_engineer` is present, Product Knowledge / Runtime Kernel concepts are represented, and the package has no obvious dangerous project-specific design-system naming in core docs.

However, the audit found several fixable consistency and runtime-quality issues that should be addressed before treating this as a release candidate.

## Built-in checks

```text
VALIDATION PASSED: 50 roles, 93 skills, 32 scenarios.
ROUTING TEST PASSED: 32 scenarios, 50 roles, 93 skills.
MEMORY INTEGRITY PASSED.
Node syntax checks: PASS.
Zip integrity: PASS.
```

## Structure summary

```text
462 files total
50 role cards
50 playbooks
50 TOML custom agents
93 skills
32 scenarios
```

The role-card, playbook, TOML, and role-index sets are aligned. `frontend_engineer` exists across role card, playbook, TOML, ROLE_INDEX, ROLE_MINI_INDEX, and ROLE_TINY_INDEX.

## High-value positives

1. **Runtime Kernel exists and is light.** `AGENTS.md`, `CURRENT.md`, `TASK_INDEX.md`, compact `CHRONICLE.md`, `TASK.md` shim, and staged loading rules are present.
2. **Product Knowledge System exists.** `PRODUCT_MAP`, `KNOWLEDGE_INDEX`, `AREA_MAP`, `FLOW_MAP`, decision records, context packets, and API/data shape prewarm are represented in docs and templates.
3. **Soft artifact-size policy is correct.** The package says target sizes are guidance ranges, not hard caps, and explicitly forbids deleting useful knowledge just to fit line count.
4. **Full role inventory is preserved.** The package has 50 roles: 49 legacy roles plus `frontend_engineer`.
5. **Local Runtime Overlay is included.** `AGENTS.override.template.md` describes a local ignored runtime without replacing the expert framework permanently.
6. **No Sova-specific core contamination found.** Core docs use neutral terms like external modules / design-system/reference modules.
7. **Product/UI implementation now has frontend responsibility.** `FRAMEWORK_LOADING_POLICY` explicitly includes `frontend_engineer` and distinguishes implementation from design-only work.

## Findings to fix

### P0 / release-blocking before RC

#### 1. Stale version metadata remains

Found stale labels:

```text
.codex/config.toml: project = "codex-product-team-2.0"
docs/ROLE_INDEX.json: version = "2.1-beta3"
docs/ROLE_MINI_INDEX.json: version = "2.1-beta3"
docs/ROLE_TINY_INDEX.json: version = "2.1-beta3"
docs/SCENARIO_TESTS.json: version = "2.1-beta3"
docs/VALIDATOR_RULES.md: required v2.0 docs exist
```

Impact: low runtime risk, high trust/maintenance risk. Codex and humans may infer mixed package lineage.

Recommended fix:

```text
Update all current metadata to 3.0-ultra.
Move old release notes from docs/ to archive/release-notes/ or mark them explicitly reference-only.
Add a validator check for stale version labels outside archive/.
```

#### 2. Role and skill routing matrices are not fully 3.0-aware

`ROLE_ROUTING_MATRIX.md` still routes existing repo UI implementation through `frontend_architect` but not `frontend_engineer`. `SKILL_ROUTING_MATRIX.md` does not include the new 3.0 runtime/product knowledge skills such as:

```text
new-task-protocol
bounded-discovery
impact-map
product-knowledge-onboarding
api-data-shape-prewarm
framework-loading
knowledge-update
greenfield-product-knowledge
knowledge-freshness-review
```

Impact: runtime may still select older 2.x routes and skip the new 3.0 operating model.

Recommended fix:

```text
Update ROLE_ROUTING_MATRIX.md with 3.0 task-type routes.
Update SKILL_ROUTING_MATRIX.md with Runtime Kernel / Product Knowledge / Safe Autonomy / API Data Shape / Greenfield routes.
Remove duplicate taste/anticipation sections while editing.
```

### P1 / important quality fixes

#### 3. New 3.0 skills are too generic internally

Several new skills have good names/descriptions but share a generic procedure:

```text
product-knowledge-onboarding
bounded-discovery
impact-map
knowledge-update
api-data-shape-prewarm
greenfield-product-knowledge
framework-loading
knowledge-freshness-review
```

Impact: skill discovery will find them, but execution quality may be weaker than the docs/protocols because the `SKILL.md` files do not carry enough operational detail.

Recommended fix:

```text
Give each new 3.0 skill a specific procedure, inputs, stop conditions, outputs, and failure modes.
Reference the matching template and protocol in each skill.
```

#### 4. Placeholder ticket state is slightly ambiguous

`CURRENT.md` and `TASK_INDEX.md` mark `TKT-000` as current, while `CHRONICLE.md` says no active task is selected. This is logically acceptable if `TKT-000` means intake placeholder, but the wording is easy to misread.

Recommended fix:

```text
CURRENT.md: Current ticket: TKT-000 (intake placeholder; no active user task)
CHRONICLE.md: No active user task is selected; TKT-000 is the intake placeholder.
```

#### 5. Role inventory policy promises metadata that role cards do not yet expose

`ROLE_INVENTORY_POLICY.md` says every role should have staged-loading metadata and simulated/subagent eligibility. Existing role cards do not consistently expose that metadata.

Recommended fix:

```text
Add lightweight metadata to role cards or role indexes:
- default_execution: simulated | subagent-eligible | service
- load_cost: tiny | standard | heavy
- spawn_default: never | approval-only | recommended-for-independent-artifact
- primary_task_types
```

Do this in index files first to avoid editing 50 long role cards.

#### 6. New scenario markdown files are too generic

The new JSON scenarios are more detailed, but the matching markdown scenario files use generic “runtime first / bounded discovery / Impact Map” wording. They do not stress-test the specific expected behavior deeply enough.

Recommended fix:

```text
Expand scenario markdown for:
- existing_product_knowledge_onboarding
- greenfield_product_creation
- new_task_safe_autonomy
- api_data_shape_contract_prewarm
```

Each should state expected product knowledge artifacts, forbidden reads, expected roles, and approval gates.

#### 7. Mirrored protocol/template docs create drift risk

The same protocol docs exist in both `docs/` and `kernel/` or `product-knowledge/`. They are currently byte-identical, which is good, but future edits can drift.

Recommended fix:

```text
Either make docs/ canonical and keep kernel/product-knowledge as navigation only,
or add validator checks that mirrored files remain identical.
```

### P2 / polish

#### 8. Old 2.1 release notes remain under docs/

`docs/RELEASE_NOTES_2.1_BETA4.md` is not runtime-critical, but old release notes in `docs/` increase retrieval noise.

Recommended fix:

```text
Move to archive/release-notes/.
Keep docs/RELEASE_NOTES_3.0.md only in runtime-near docs.
```

#### 9. Framework directory is mostly a navigation shell

`framework/` contains only README/routing README while the real expert framework is still in `.agents/`, `.codex/agents`, and docs. This is not broken, but it can surprise humans expecting `framework/roles` and `framework/skills`.

Recommended fix:

```text
Either document clearly that framework/ is a nav layer over legacy .agents/ assets,
or add symlink-like index files under framework/roles, framework/skills, framework/playbooks.
```

## Suggested beta 2 fix list

### Must fix

1. Update stale version metadata to `3.0-ultra`.
2. Update ROLE_ROUTING_MATRIX and SKILL_ROUTING_MATRIX for 3.0 runtime/product knowledge/frontend-engineering routes.
3. Expand new 3.0 skills beyond generic procedure.
4. Clarify TKT-000 placeholder state.

### Should fix

5. Add staged-loading/subagent-eligibility metadata to role indexes.
6. Strengthen 3.0 scenario markdown files.
7. Add validator checks for stale version labels and mirrored-doc drift.
8. Move old 2.1 release notes out of docs/.

### Nice to fix

9. Clarify `framework/` as navigation layer or add framework indexes.
10. Add an example local runtime project showing `PRODUCT_MAP`, `KNOWLEDGE_INDEX`, and area maps from an existing product.

## Final verdict

3.0 Ultra is structurally sound and directionally correct. It successfully captures the core discoveries from the live `ai-web` experiment: lightweight runtime, product knowledge navigation, bounded discovery, Impact Map, soft size budgets, role preservation, and staged expert-framework loading.

It should not be called final RC yet. The main remaining work is not structural generation; it is **semantic hardening**: updating stale metadata, teaching routing matrices about the new 3.0 operating model, making new skills operational rather than generic, and adding stronger simulations.
