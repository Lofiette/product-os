# Skill Invocation Policy

## Goal

Make the right methods discoverable without recreating the 3.x problem of exposing every capability at once.

## Implicit invocation

Allow implicit invocation when all conditions hold:

- the workflow is common within the enabled pack;
- trigger language is distinctive;
- accidental activation has low cost;
- the skill does not expand scope by itself;
- the output is useful without an additional user decision.

Examples include focused accessibility review, API contract review, UX research planning, and frontend integration review when their domain pack is intentionally active.

## Explicit-only invocation

Set `policy.allow_implicit_invocation: false` when any condition holds:

- the workflow spawns or manages real workers;
- the workflow audits the framework itself;
- it intentionally broadens the solution space, such as opportunity ideation;
- it performs a broad or potentially expensive code/design-system audit;
- activation should represent an explicit user or orchestrator decision.

Explicit-only skills remain available through `$skill-name`.

## Pack activation

`cpt-core` is always sufficient for runtime lifecycle and task planning. Domain packs should be activated by working profile or task class, not all at once.

Recommended profiles are recorded in `domain-packs/PACK_CATALOG.json`:

- core only;
- product discovery;
- UI review;
- UI implementation;
- risk review;
- AI product.

A profile is guidance, not a hard dependency graph. Task planning may enable a smaller subset.

## Metadata budget

Codex initially sees skill names, descriptions, and paths under a bounded metadata budget. Therefore:

- descriptions must be concise and discriminative;
- aliases must not remain active;
- optional packs must remain disabled until relevant;
- realistic profiles must remain below the package budget;
- the “all packs” total is reported but is not a supported default profile.

Run:

```bash
python tools/measure_all_skill_metadata.py
python tools/cpt_dist.py metadata-budget --plugin <plugin-path>
```

## Task-planning relationship

`cpt-task-planning` selects the smallest skill set that changes a decision, artifact, risk gate, or verification step. It must not load skills merely because they might be relevant. If an exact method is unavailable, it should report the gap rather than substitute a vaguely adjacent skill.

## Review rules

Before adding or changing a skill description:

1. identify its nearest competing descriptions;
2. add positive and negative trigger cases;
3. run metadata proxy evals;
4. measure intended profiles;
5. keep expensive workflows explicit-only unless real traces justify implicit activation.
