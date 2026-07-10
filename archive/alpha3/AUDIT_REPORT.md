# Codex Product Operating System 4.0 Alpha 3 — Skills Consolidation Audit

Date: 2026-07-10  
Version: `4.0.0-alpha.3`  
Phase: **Phase 3 — Skills Consolidation**

## Verdict

**PASS for Alpha 3 Skills Consolidation, with explicitly documented behavioral-evaluation and role-integration boundaries.**

Alpha 3 preserves the Alpha 2 Runtime Kernel and distribution split, replaces the 3.x skill sprawl with a complete canonical migration, and keeps realistic activation profiles below the package metadata budget. It does not yet claim live-model routing certification or integration of the 50 logical roles.

## Implemented

- complete inventory of 95 legacy skills;
- one-to-one legacy mapping coverage with no duplicate source mappings;
- 45 active canonical skills;
- one required core plugin and five optional domain plugins;
- exact `cpt-pack-v2` inventories and legacy provenance;
- domain-specific method, output contract, evidence standard, stop conditions, and failure modes for every active skill;
- `agents/openai.yaml` for every active skill;
- implicit/explicit invocation policy;
- central skill registry and migration registry;
- 135 deterministic trigger proxy cases;
- pack and working-profile metadata-budget validation;
- bundled-pack installation and independent removal;
- preserved Alpha 2 install/update/doctor/uninstall behavior;
- preserved Alpha 1 task, micro-change, lease, checkpoint, and recovery runtime.

## Inventory and consolidation metrics

| Metric | Result |
|---|---:|
| Legacy skills | 95 |
| Active canonical skills | 45 |
| Consolidation ratio | 52.6% fewer active skills |
| Legacy source mappings | 95 / 95 |
| Active compatibility aliases | 0 |
| Plugins | 6 total: 1 core + 5 domain |
| Implicit skills | 41 |
| Explicit-only skills | 4 |
| Trigger cases | 135 |
| Trigger proxy result | 135 / 135 PASS |
| Duplicate active method bodies | 0 |
| Skills missing output/evidence/stop/failure sections | 0 |
| Skills missing `agents/openai.yaml` | 0 |

Explicit-only skills:

- `cpt-delegation`;
- `cpt-design-system-code-audit`;
- `cpt-framework-audit`;
- `cpt-opportunity-ideation`.

## Plugin inventory

| Plugin | Active skills | Legacy skills represented | Estimated discovery metadata |
|---|---:|---:|---:|
| `cpt-core` | 3 | 18 | 564 chars |
| `cpt-product-research` | 10 | 19 | 2,052 chars |
| `cpt-design-ui` | 12 | 31 | 2,555 chars |
| `cpt-engineering` | 12 | 16 | 2,547 chars |
| `cpt-risk-operations` | 5 | 8 | 994 chars |
| `cpt-ai-agentic` | 3 | 3 | 568 chars |

The combined engineering pack is an intentional Alpha 3 decision. Its metadata remains within the domain-pack budget, while common UI/API/data tasks frequently cross the proposed frontend/backend boundary. Future splitting requires live routing evidence rather than file-count preference.

## Supported activation-profile budgets

| Profile | Packs | Estimated metadata |
|---|---|---:|
| Core only | core | 564 chars |
| Product discovery | core + product/research | 2,616 chars |
| UI review | core + design/UI | 3,119 chars |
| UI implementation | core + design/UI + engineering | 5,666 chars |
| Risk review | core + risk/operations | 1,558 chars |
| AI product | core + product/research + AI + risk/operations | 4,178 chars |

All supported default profiles stay below the Alpha 3 release target of 7,000 estimated characters. Enabling every optional pack yields about 9,280 characters and is intentionally **not** a supported default discovery profile.

## Consolidation quality

The migration removes active aliases rather than preserving them as metadata-consuming skills. Examples:

- runtime, intake, ticket, context, and checkpoint fragments consolidate into `cpt-runtime`;
- bounded discovery, repo recon, framework loading, Impact Map, and team routing consolidate into `cpt-task-planning`;
- greenfield/onboarding/freshness/update fragments consolidate into `cpt-knowledge-lifecycle`;
- reference, taste, example-board, and critique fragments consolidate into `cpt-reference-taste-calibration`;
- UI review, screenshot comparison, heuristic audit, and visual QA fragments consolidate into `cpt-visual-acceptance-review`;
- subagent orchestration, bounded contract, and failure recovery consolidate into explicit-only `cpt-delegation`.

Every canonical method has a unique method body and a named output contract. The 3.x five-step generic placeholder procedure is rejected by validation.

## Static validation

```text
SKILL VALIDATION PASSED: 45 active skills, 95 legacy mappings, 6 plugins
TRIGGER PROXY EVAL: 135/135 passed
DISTRIBUTION STATIC VALIDATION PASSED
PYTHON COMPILE PASS
```

Validated:

- skill frontmatter and exact path/name identity;
- discriminative description length and trigger-oriented wording;
- eight required operational sections;
- minimum method depth;
- output-contract depth;
- absence of legacy boilerplate and duplicate method bodies;
- valid `agents/openai.yaml`, display metadata, and boolean invocation policy;
- exact trigger-case coverage;
- exact 95-source migration coverage;
- active registry / installed skill identity;
- `cpt-pack-v2` exact inventories and legacy provenance;
- pack catalog/profile references;
- plugin manifests and marketplace paths;
- compact root `AGENTS.md` loader;
- absence of private product/design-system names in universal package files.

## Behavioral distribution tests

Passed individually:

1. local install remains Git-clean and below repo-file budget;
2. team install with repo core remains below budget;
3. existing tracked `AGENTS.md` is preserved in local mode;
4. update preserves mutable runtime state;
5. update blocks modified managed tooling without force;
6. uninstall preserves application source;
7. personal marketplace preserves unrelated entries;
8. domain pack removal preserves core;
9. team uninstall preserves pre-existing AGENTS content;
10. personal core survives project uninstall by default;
11. core metadata budget remains small;
12. bundled domain pack installs by name and removes independently;
13. doctor passes after local installation.

## Runtime and pack integration

A clean local installation successfully:

```text
installed cpt-core
installed cpt-design-ui and cpt-engineering independently
reported Git-clean project state
created and activated a Standard Task
created a scoped lease
created a checkpoint
validated runtime pointers and schemas
reported doctor PASS
```

All five bundled domain packs were also exposed through a synthetic personal marketplace and selected packs were removed without changing the remaining entries.

## Safety and context behavior

- only `cpt-core` is required;
- optional domain packs are independently enabled;
- no active legacy aliases consume metadata;
- real delegation is explicit-only;
- framework audits and broad design-system code audits are explicit-only;
- realistic profiles stay below release metadata budget;
- all-pack activation is measured and clearly documented as non-default;
- canonical task/runtime state remains in the repo scaffold rather than plugin state;
- installer still performs no `git add`, commit, branch, reset, or clean.

## Honest limitations

- The trigger evaluator is a deterministic metadata proxy, not a live Codex trace.
- The 50 logical roles and role-to-skill/gate routing are not migrated yet.
- Domain plugins are exposed but not automatically enabled by installation.
- Hooks, rules, native approval profiles, SQLite, MCP, Product Knowledge schemas, workers, and external adapters are absent.
- Legacy aliases require migration lookup; they are not executable compatibility skills.
- The authorization lease remains a runtime contract, not a sandbox boundary.
- Full production CI across all operating systems and Codex hosts remains later work.

## Phase 3 exit assessment

| Criterion | Status |
|---|---|
| Inventory every 3.x skill | PASS |
| Map every legacy skill exactly once | PASS |
| Remove active aliases and obvious fragments | PASS |
| Replace generic active skills with domain methods | PASS |
| Add output/evidence/stop/failure contracts | PASS |
| Add invocation metadata | PASS |
| Keep supported profiles within metadata budget | PASS |
| Add trigger regression proxy | PASS |
| Preserve Alpha 2 distribution behavior | PASS |
| Live Codex routing evals | DEFERRED to Evaluation Plane |
| Logical-role integration | DEFERRED to Phase 4 |

## Recommendation

Freeze this package as the **Alpha 3 Skills Consolidation baseline** and proceed to Phase 4: Role Expertise and Routing Overhaul. Do not add new skills by default; Phase 4 should connect the preserved 50 logical roles to these 45 methods, gates, and a smaller worker-archetype surface.
