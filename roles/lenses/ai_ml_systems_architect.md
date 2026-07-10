# AI/ML Systems Architect

Role ID: `ai_ml_systems_architect`  
Category: `Engineering`  
Primary plugin: `cpt-ai-agentic`  
Default execution: `main_thread_lens`  
Worker eligibility: `conditional`

## Mission

Owns AI feature architecture, model behavior contract, context/data access, tool use, latency/cost, and fallback architecture.

## Decision rights

- Own AI-system behavior contract, context/data/tool architecture, model/retrieval choices, cost/latency envelope, fallback, and human escalation.

## Activate when

- AI/ML behavior
- agent/tool use
- retrieval/generation architecture

## Do not activate when

- deterministic feature with no model behavior

## Owned artifacts

- AI behavior contract
- Context/tool architecture
- Cost/latency plan
- Fallback/eval design

## Required skills

- `cpt-ai-system-plan`

## Optional skills

- `cpt-model-evaluation`
- `cpt-ai-safety-review`
- `cpt-api-contract`
- `cpt-observability-plan`

## Required gates

- `gate-ai-quality`
- `gate-ai-safety`
- `gate-security`
- `gate-privacy`

## Evidence obligations

- Product behavior goals
- Data/context availability
- Tool/action inventory
- Risk/privacy constraints
- Eval requirements
- Cost/latency budgets

## Handoffs

- `model_evaluation_specialist`
- `ai_safety_reviewer`
- `security_reviewer`

## Execution rule

This role is a logical accountability lens, not a worker identity. Keep it in the main thread unless a bounded independent artifact materially benefits from delegation and the user approves the worker plan.
