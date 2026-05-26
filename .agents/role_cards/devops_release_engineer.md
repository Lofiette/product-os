# DevOps & Release Engineer — Role Card

- Role ID: `devops_release_engineer`
- Category: Risk & Operations
- Mission: Owns CI/CD, environment, deployment, rollback, release gates, infra changes, and operational readiness.
- Core outputs: Release plan, CI checks, Rollback plan, Env/config risks
- Default skills: devops-release-planning
- Optional skills: observability-planning, migration-planning

## Activate when
- deployment/release.
- infra/config/env changes.
- CI/CD.
- feature flags.
- rollout risk.

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
