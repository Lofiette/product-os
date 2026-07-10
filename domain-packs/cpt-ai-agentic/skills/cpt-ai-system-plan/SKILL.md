---
name: cpt-ai-system-plan
description: Use to design AI/agent behavior, context/data access, tools, permissions, latency/cost, fallback, and human escalation.
---

# CPT AI System Plan

## Use when

- A product feature uses models, retrieval, agents, tools, or probabilistic behavior.

## Do not use when

- The task only consumes a fixed deterministic API.

## Required inputs

- User job, behavior scope, model/tool options, data/context sources, permissions, latency/cost budget, safety/privacy, evaluation, and operations.

## Method

1. Define behavior contract: inputs, outputs, uncertainty, unsupported cases, and user expectations.
2. Map context/data sources, provenance, freshness, privacy, retrieval, and prompt boundaries.
3. Define tool/action permissions, confirmation, idempotency, rollback, and human escalation.
4. Choose model/architecture with quality, latency, cost, availability, and vendor trade-offs.
5. Design deterministic scaffolding, structured outputs, validation, fallbacks, retries, and degradation.
6. Specify evaluation, monitoring, prompt/model/version management, and incident response.
7. Separate prototype assumptions from production requirements.

## Output contract

Produce a compact artifact containing:

- `AI behavior contract.`
- `Context/data/tool permission map.`
- `Model/architecture trade-offs.`
- `Fallback/escalation, eval, monitoring, and rollout plan.`

## Evidence standard

- Model capability claims require eval evidence for the intended task/domain.

## Stop and escalate

- Irreversible tool permissions or sensitive data access lack controls.
- No measurable behavior contract exists.

## Failure modes to avoid

- Starting with model choice.
- Treating a prompt as the whole system.
