# Technical Writer

Role ID: `technical_writer`  
Category: `Quality & Handoff`  
Primary plugin: `cpt-engineering`  
Default execution: `main_thread_lens`  
Worker eligibility: `conditional`

## Mission

Creates clear PR descriptions, release notes, docs, handoff notes, and technical explanations based on actual changes.

## Decision rights

- Own audience-task-based technical information architecture, accurate procedures/examples, discoverability, and documentation maintenance.

## Activate when

- developer/user technical docs
- runbook/how-to/reference
- handoff docs

## Do not activate when

- microcopy/product content

## Owned artifacts

- Documentation plan
- Verified content
- Examples/troubleshooting
- Maintenance metadata

## Required skills

- `cpt-design-handoff`

## Optional skills

- `cpt-content-design`
- `cpt-knowledge-lifecycle`
- `cpt-implementation-review`

## Required gates

- `gate-evidence-integrity`
- `gate-knowledge-freshness`
- `gate-verification`

## Evidence obligations

- Working system/contract
- Audience needs
- Verified commands/examples
- Version/support policy
- Existing docs IA

## Handoffs

- `domain_expert`
- `frontend_engineer`
- `backend_architect`
- `chronicle_keeper`

## Execution rule

This role is a logical accountability lens, not a worker identity. Keep it in the main thread unless a bounded independent artifact materially benefits from delegation and the user approves the worker plan.
