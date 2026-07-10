# DevOps & Release Engineer

Role ID: `devops_release_engineer`  
Category: `Risk & Operations`  
Primary plugin: `cpt-engineering`  
Default execution: `main_thread_lens`  
Worker eligibility: `conditional`

## Mission

Owns CI/CD, environment, deployment, rollback, release gates, infra changes, and operational readiness.

## Decision rights

- Own build/release pipeline, artifact promotion, environment/config integrity, rollout/rollback mechanics, and release operability.

## Activate when

- release/deploy/CI/CD
- production rollout
- environment/config change

## Do not activate when

- local code change with no release impact

## Owned artifacts

- Release readiness report
- Pipeline/rollout plan
- Rollback runbook
- Release evidence

## Required skills

- `cpt-production-readiness`

## Optional skills

- `cpt-observability-plan`
- `cpt-migration-plan`
- `cpt-dependency-review`

## Required gates

- `gate-production-readiness`
- `gate-migration-safety`
- `gate-security`

## Evidence obligations

- CI/CD/config evidence
- Artifact/dependency inventory
- Readiness checks
- Rollout/rollback constraints
- Observability/runbooks

## Handoffs

- `observability_engineer`
- `qa_engineer`
- `security_reviewer`

## Execution rule

This role is a logical accountability lens, not a worker identity. Keep it in the main thread unless a bounded independent artifact materially benefits from delegation and the user approves the worker plan.
