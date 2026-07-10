---
name: cpt-architecture-plan
description: Use to plan system boundaries, interfaces, NFRs, trade-offs, sequencing, and architecture decisions; not for trivial local implementation.
---

# CPT Architecture Plan

## Use when

- A change introduces or reshapes services, modules, integration boundaries, or major non-functional requirements.

## Do not use when

- The task is a local implementation following established architecture.

## Required inputs

- Business/product outcome, current architecture, constraints, scale, reliability/security/privacy needs, team/operational context, and migration boundary.

## Method

1. Define architecture-driving requirements and measurable NFRs.
2. Map current context, components, boundaries, data flows, dependencies, trust zones, and ownership.
3. Generate alternatives with explicit trade-offs in complexity, cost, coupling, operability, and evolution.
4. Define interfaces/contracts, failure behavior, consistency, deployment, observability, and security.
5. Plan incremental implementation/migration with compatibility and rollback.
6. Record decisions and rejected alternatives in ADR-ready form.
7. Validate architecture against product scope and operational capability.

## Output contract

Produce a compact artifact containing:

- `Context/boundary/data-flow architecture.`
- `Alternatives and trade-off matrix.`
- `Selected decision, interfaces, NFRs, risks, and ADRs.`
- `Implementation/migration sequence and verification.`

## Evidence standard

- NFRs should be measurable or explicitly provisional.

## Stop and escalate

- Critical scale, ownership, or compliance constraints are unknown.

## Failure modes to avoid

- Choosing technology before requirements.
- Producing a diagram without failure/operational behavior.
