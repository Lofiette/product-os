# Skill Consolidation

## Outcome

- Legacy skills inventoried: **95**
- Active 4.0 skills: **45**
- Active plugins: **6**
- Legacy aliases installed as skills: **0**
- Legacy mappings with an active target: **95 / 95**

The migration is loss-aware rather than name-preserving. Every legacy skill maps to exactly one active method in `migration/SKILL_MIGRATION.csv`; several legacy fragments may intentionally map to one coherent skill.

## Consolidation tests

A legacy capability is consolidated when at least one condition is true:

1. It is an alternate name for an existing method.
2. It is a setup, review, or reporting fragment that is not useful independently.
3. It shares the same trigger, evidence, method, and output contract with another skill.
4. Separate activation would create routing collisions or repeated context loading.
5. Its responsibility belongs to runtime lifecycle rather than a domain method.

A capability remains separate when it has distinct decision rights, evidence, artifact, risk, or common independent use.

## Package boundaries

- `cpt-core`: runtime lifecycle, task planning, and Product Knowledge lifecycle.
- `cpt-product-research`: product framing, evidence, research, measurement, journeys, and opportunities.
- `cpt-design-ui`: interaction/interface/content/system/accessibility/visual methods.
- `cpt-engineering`: architecture, frontend integration, API/data, delivery, performance, review, and operations methods.
- `cpt-risk-operations`: threat, privacy, cross-cutting risk, real delegation, and framework assurance.
- `cpt-ai-agentic`: AI system planning, evaluation, and safety.

The engineering pack is intentionally combined in Alpha 3 because its metadata remains within profile budget and many engineering tasks cross frontend/API/data boundaries. A future split requires behavioral evidence that it improves discovery or installation ergonomics.

## Important distinctions

- Skills are methods, not decision owners. Logical roles are migrated in Phase 4.
- Skills do not imply real workers. Delegation is an explicit-only method.
- Domain packs are optional. Installing every pack is not the default usage model.
- Removed aliases remain visible in migration records but do not consume active discovery metadata.

## Migration behavior

When an old instruction references a legacy skill:

1. Resolve it through `SKILL_MIGRATION.json`.
2. Use the canonical active target.
3. Do not install a compatibility alias unless a later migration tool proves it necessary.
4. Re-evaluate whether the target pack should be enabled for the task.

## Deferred work

Alpha 3 does not yet map the 50 logical roles onto the new skills, gates, or worker archetypes. That is Phase 4. It also does not claim that metadata proxy evals prove model behavior; executable Codex trace evals arrive in the Evaluation Plane phase.
