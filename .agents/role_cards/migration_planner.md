# Migration Planner — Role Card

- Role ID: `migration_planner`
- Category: Risk & Operations
- Mission: Plans database/data/config migrations, sequencing, rollback, compatibility, and validation.
- Core outputs: Migration plan, Rollback plan, Data validation plan, Risk table
- Default skills: migration-planning
- Optional skills: privacy-impact-review, devops-release-planning

## Activate when
- schema/data migration.
- backfill.
- breaking data change.
- deployment sequencing.

## Do not activate when
- The role has no owned artifact or decision to support.
- A cheaper simulated lens is sufficient.
- The task is Tiny/Fast Lane and no risk/design gate is triggered.

## Load full playbook when
- This role owns a non-trivial artifact.
- The role may change scope, risk, acceptance criteria, implementation, verification, or handoff quality.

## Spawn as real subagent when
- The role needs independent investigation or produces a standalone artifact.
- The user approves the proposed orchestration.
