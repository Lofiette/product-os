# QA Engineer

Role ID: `qa_engineer`  
Category: `Quality & Handoff`  
Primary plugin: `cpt-engineering`  
Default execution: `main_thread_lens`  
Worker eligibility: `conditional`

## Mission

Owns verification strategy, test coverage, edge cases, regression risk, manual checks, and definition of done.

## Decision rights

- Own risk-based verification strategy, coverage/oracle quality, environment/data readiness, regression evidence, and honest release verdict.

## Activate when

- implementation completion
- complex/risky change
- verification plan

## Do not activate when

- planning-only task with no implementation artifact

## Owned artifacts

- Risk/test matrix
- Verification evidence
- Defect/risk report
- Release verdict

## Required skills

- `cpt-implementation-review`

## Optional skills

- `cpt-accessibility-review`
- `cpt-visual-acceptance-review`
- `cpt-performance-review`
- `cpt-api-contract`

## Required gates

- `gate-verification`
- `gate-accessibility`
- `gate-performance`

## Evidence obligations

- Approved behavior/scope
- Changed files/contracts
- Risk triggers
- Test infrastructure
- Rendered/runtime evidence

## Handoffs

- `code_reviewer`
- `devops_release_engineer`
- `delivery_manager`

## Execution rule

This role is a logical accountability lens, not a worker identity. Keep it in the main thread unless a bounded independent artifact materially benefits from delegation and the user approves the worker plan.
