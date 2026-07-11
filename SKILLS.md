# CPT OS 4.0 Alpha 7 Skills

Alpha 7 preserves the Alpha 3 consolidation of **95** legacy 3.x skills into **45** active methods distributed across one required core plugin and five optional domain plugins.

## Inventory

| Plugin | Skills | Purpose |
|---|---:|---|
| `cpt-core` | 3 | Runtime lifecycle, bounded task planning, Product Knowledge lifecycle |
| `cpt-product-research` | 10 | Product scope, evidence, market/UX research, journeys, analytics, experiments, opportunities |
| `cpt-design-ui` | 12 | Interface, content, state, design-system, reference, accessibility, handoff, visual acceptance |
| `cpt-engineering` | 12 | Architecture, frontend, API/data, dependencies, migration, performance, observability, readiness, review |
| `cpt-risk-operations` | 5 | Threat, privacy, cross-cutting risk, real delegation, framework assurance |
| `cpt-ai-agentic` | 3 | AI system planning, model evaluation, AI safety |

Only `cpt-core` is required. Domain packs should be enabled according to the current working profile.

## Catalog and installation

```bash
python tools/cpt_dist.py pack-catalog
python tools/cpt_dist.py pack-add --name cpt-design-ui --scope personal
python tools/cpt_dist.py pack-add --name cpt-engineering --scope repo --project /path/to/repo
python tools/cpt_dist.py pack-remove --name cpt-design-ui --scope personal
```

Marketplace exposure does not guarantee automatic plugin enablement. Restart Codex and enable the plugin through the available plugin UI when required.

## Canonical registry

- `skills/SKILL_REGISTRY.json` lists every active skill, plugin, invocation mode, trigger cases, and legacy sources.
- `migration/SKILL_MIGRATION.csv` maps all 95 legacy skills to one canonical target.
- `evaluation/skill-trigger-cases.json` is the central trigger-case registry.
- `agents/openai.yaml` controls display metadata and implicit invocation per skill.

## Usage rule

Do not enable all domain packs by default. Choose a profile or smaller subset whose skills change a decision, artifact, risk gate, or verification step. The full-suite metadata total is measured for transparency but is not a supported default activation mode.

## Quality boundary

Alpha 7 preserves the skill validation, migration coverage, metadata budgets, role/gate routing, and typed Product Knowledge lifecycle. It adds optional hooks, rules profiles, lease-aware policy checks, compaction checkpoints, freshness automation, audit records, and worker lifecycle records. Managed worker orchestration is available through the optional worker pack. Live Codex behavioral certification, SQLite/MCP adapters, and external observability remain deferred.
