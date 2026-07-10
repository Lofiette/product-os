---
name: cpt-product-scope
description: Use to frame product outcome, users, scope, MVP slice, non-goals, acceptance, and success measures; not for code-level planning.
---

# CPT Product Scope

## Use when

- A product request is ambiguous, greenfield, or at risk of scope expansion.
- A team needs an MVP or phase boundary before design/engineering.

## Do not use when

- The outcome, scope, and acceptance criteria are already approved.
- The task is purely technical maintenance with no product trade-off.

## Required inputs

- User/stakeholder request, product knowledge, constraints, evidence, business goal, and delivery horizon.

## Method

1. Translate the request into a user or business outcome, not a feature list.
2. Identify target users, jobs, pain, context, and excluded users.
3. Separate assumptions, evidence, and decisions.
4. Define the smallest coherent value slice and explicit non-goals.
5. Specify behavior-level acceptance criteria and success/guardrail metrics.
6. Identify dependencies, risks, sequencing, and decisions requiring validation.
7. Offer alternatives when value, cost, or uncertainty materially differ.

## Output contract

Produce a compact artifact containing:

- `Outcome and target users.`
- `Scope, non-goals, MVP/phase slice.`
- `Acceptance criteria and success/guardrail metrics.`
- `Assumptions, risks, dependencies, and decisions.`

## Evidence standard

- Do not label stakeholder opinion as user evidence.
- Metrics need data source and decision use.

## Stop and escalate

- The core outcome or decision owner is unknown.
- Scope contains incompatible goals.

## Failure modes to avoid

- Defining MVP as a random feature subset.
- Using implementation detail as product acceptance.
