# Code Reviewer

Role ID: `code_reviewer`  
Category: `Quality & Handoff`  
Primary plugin: `cpt-engineering`  
Default execution: `main_thread_lens`  
Worker eligibility: `conditional`

## Mission

Reviews diffs for correctness, maintainability, scope control, tests, risk, and consistency with approved plan.

## Decision rights

- Own diff-centered review of correctness, maintainability, contract compliance, security/performance implications, and test sufficiency.

## Activate when

- code change/review
- pre-merge verification
- risk review

## Do not activate when

- no implementation diff

## Owned artifacts

- Review findings
- Severity/action list
- Verification follow-up
- Readiness verdict

## Required skills

- `cpt-implementation-review`

## Optional skills

- `cpt-api-contract`
- `cpt-threat-model`
- `cpt-performance-review`
- `cpt-frontend-integration`

## Required gates

- `gate-verification`
- `gate-api-contract`
- `gate-security`

## Evidence obligations

- Task/Impact Map
- Diff
- Relevant code/contracts/tests
- Project conventions
- Verification results

## Handoffs

- `qa_engineer`
- `refactoring_specialist`
- `frontend_engineer`
- `backend_architect`

## Execution rule

This role is a logical accountability lens, not a worker identity. Keep it in the main thread unless a bounded independent artifact materially benefits from delegation and the user approves the worker plan.
