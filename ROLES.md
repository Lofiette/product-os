# Roles in Codex Product Operating System 4.0 Alpha 5

Alpha 5 preserves all 50 logical roles from 3.0 and rewrites them as accountable expert lenses.

## Core model

- **Role**: who owns a decision or artifact and which specialist judgment is required.
- **Skill**: a reusable method.
- **Gate**: evidence required to accept a result.
- **Worker**: a bounded execution container, introduced separately in the Execution Plane.

Roles are not installed as 50 custom agents. They normally operate as main-thread lenses selected by `cpt-task-planning`.

## Canonical assets

- `roles/ROLE_REGISTRY.json`
- `roles/ROLE_ROUTING_PROFILES.json`
- `roles/GATE_REGISTRY.json`
- `roles/lenses/*.md`
- `roles/methods/*.md`
- `roles/gates/*.md`
- `roles/ROLE_SKILL_MATRIX.csv`
- `roles/ROLE_GATE_MATRIX.csv`

The core plugin mirrors these assets under the task-planning skill's `references/` directory so they are loaded only after task planning is invoked.

## Selection rules

1. Choose a task routing profile.
2. Identify decisions and artifacts.
3. Assign exactly one accountable role to each meaningful decision/artifact.
4. Add supporting roles only for distinct evidence, risk, gate ownership, or independent challenge.
5. Load compact lenses first; load deep methods only when needed.
6. Keep roles in the main thread by default.
7. Worker eligibility never means automatic spawn.

See `roles/ROLE_ROUTING.md` and `roles/ROLE_WORKER_POLICY.md`.
