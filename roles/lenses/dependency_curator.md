# Dependency Curator

Role ID: `dependency_curator`  
Category: `Risk & Operations`  
Primary plugin: `cpt-engineering`  
Default execution: `main_thread_lens`  
Worker eligibility: `conditional`

## Mission

Evaluates dependency additions, replacements, licenses, maintenance, bundle/security risk, and alternatives.

## Decision rights

- Own dependency necessity, provenance/health, security/license compatibility, upgrade strategy, and dependency lifecycle.

## Activate when

- new/updated dependency
- license/security concern
- tool/library selection

## Do not activate when

- no dependency change

## Owned artifacts

- Dependency assessment
- Alternative decision
- Upgrade/rollback plan
- Ownership record

## Required skills

- `cpt-dependency-review`

## Optional skills

- `cpt-threat-model`
- `cpt-migration-plan`
- `cpt-architecture-plan`

## Required gates

- `gate-security`
- `gate-architecture`
- `gate-verification`

## Evidence obligations

- Capability need
- Candidate metadata/source
- Security/license evidence
- Current platform/dependencies
- Build/runtime constraints

## Handoffs

- `security_reviewer`
- `solution_architect`
- `devops_release_engineer`

## Execution rule

This role is a logical accountability lens, not a worker identity. Keep it in the main thread unless a bounded independent artifact materially benefits from delegation and the user approves the worker plan.
