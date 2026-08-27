# Skill Consolidation and New Methods

## Outcome

- Legacy skills inventoried: **95**
- Legacy skills mapped to active targets: **95 / 95**
- New Product Designer 4.1 methods without legacy aliases: **4**
- Active 4.0 skills after the patch: **49**
- Active plugins: **6**
- Legacy aliases installed as skills: **0**

The migration is loss-aware rather than name-preserving. Every legacy skill maps to exactly one active method in `migration/SKILL_MIGRATION.csv`. New methods are recorded separately in `migration/SKILL_MIGRATION.json:new_skills` because inventing false legacy mappings would damage provenance.

## Consolidation tests

A legacy capability is consolidated when at least one condition is true:

1. It is an alternate name for an existing method.
2. It is a setup, review, or reporting fragment that is not useful independently.
3. It shares the same trigger, evidence, method, and output contract with another skill.
4. Separate activation would create routing collisions or repeated context loading.
5. Its responsibility belongs to runtime lifecycle rather than a domain method.

A capability remains separate when it has distinct decision rights, evidence, artifact, risk, or common independent use.

The four vNext2 methods remain separate because pattern selection, form-task design, professional-data interface design, and execution orchestration have distinct triggers, evidence, outputs, stop conditions, and independent use.

## Package boundaries

- `cpt-core`: runtime lifecycle, task planning, and Product Knowledge lifecycle.
- `cpt-product-research`: product framing, evidence, research, measurement, journeys, and opportunities.
- `cpt-design-ui`: interaction/interface/content/system/accessibility/visual methods plus portable execution adapters.
- `cpt-engineering`: architecture, frontend integration, API/data, delivery, performance, review, and operations methods.
- `cpt-risk-operations`: threat, privacy, cross-cutting risk, real delegation, and framework assurance.
- `cpt-ai-agentic`: AI system planning, evaluation, and safety.

## Migration behavior

When an old instruction references a legacy skill:

1. Resolve it through `SKILL_MIGRATION.json`.
2. Use the canonical active target.
3. Do not install a compatibility alias unless a later migration tool proves it necessary.
4. Re-evaluate whether the target pack should be enabled for the task.

When a new 4.1 method is needed, invoke it directly; there is intentionally no fictional 3.x alias.
