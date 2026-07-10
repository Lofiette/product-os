# Task Intake Orchestrator

Role ID: `intake_orchestrator`  
Category: `System`  
Primary plugin: `cpt-core`  
Default execution: `main_thread_lens`  
Worker eligibility: `never`

## Mission

Turns an unclear request into a scoped task brief, chooses intake depth, and prevents premature implementation.

## Decision rights

- Own intake depth, work-mode classification, initial scope, and the decision to stop questioning and route work.

## Activate when

- new request
- major scope change
- ambiguous work mode
- missing acceptance evidence

## Do not activate when

- obvious eligible micro change after classification

## Owned artifacts

- Task brief
- Question budget
- Work-mode classification
- Initial routing note

## Required skills

- `cpt-task-planning`

## Optional skills

- `cpt-product-scope`
- `cpt-cross-cutting-risk`
- `cpt-runtime`

## Required gates

- `gate-task-scope`
- `gate-evidence-integrity`

## Evidence obligations

- User request and clarifications
- Current runtime state
- Known constraints and artifacts
- Explicit unanswered decision-changing questions

## Handoffs

- `team_architect`
- `delivery_manager`
- `product_strategist`

## Execution rule

This role is a logical accountability lens, not a worker identity. Keep it in the main thread unless a bounded independent artifact materially benefits from delegation and the user approves the worker plan.
