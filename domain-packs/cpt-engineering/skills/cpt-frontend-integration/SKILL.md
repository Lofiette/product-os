---
name: cpt-frontend-integration
description: Use for coded UI implementation/review across components, routing, state, async data, boundaries, accessibility, performance, and maintainability.
---

# CPT Frontend Integration

## Use when

- A product/UI change will be implemented in frontend code.
- A systemic UI change may affect shared components, routes, state, or data flow.

## Do not use when

- The task is design-only with no code implementation.

## Required inputs

- Approved product/design artifacts, Impact Map, repository conventions, component/design-system contract, API/data contracts, tests, and performance/accessibility constraints.

## Method

1. Identify rendering boundary, route/layout ownership, component reuse, and server/client split.
2. Map state ownership: URL, server cache, local component, shared store, form, optimistic state, and persistence.
3. Define async loading/error/retry/cancellation/race behavior and API contract use.
4. Choose component composition and extension without bypassing design-system or architecture boundaries.
5. Plan accessibility, responsive behavior, performance, code splitting, and error boundaries.
6. Implement smallest coherent change with typed interfaces and minimal duplication.
7. Verify behavior, states, regression, design fidelity, and maintainability.

## Output contract

Produce a compact artifact containing:

- `Frontend integration plan or review.`
- `Component/state/data-flow map.`
- `Files, risks, tests, and performance/accessibility notes.`
- `Implementation or PASS/WARN/BLOCKED review result.`

## Evidence standard

- Do not infer shared usage without import/reference evidence.

## Stop and escalate

- Product behavior, data contract, or state ownership is unresolved.

## Failure modes to avoid

- Putting server state in arbitrary global stores.
- Solving a systemic issue on one screen only.
