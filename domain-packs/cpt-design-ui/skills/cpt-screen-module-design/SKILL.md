---
name: cpt-screen-module-design
description: Use to create or redesign a screen, flow, module, or prototype with hierarchy, states, components, content, and implementation handoff.
---

# CPT Screen Module Design

## Use when

- The task requires a new or redesigned product interface.
- A module must be designed for later developer implementation.
- No design system exists and a consistent prototype contract is needed.

## Do not use when

- The task is visual QA of an already implemented screen.
- Only information architecture is changing with no screen solution yet.

## Required inputs

- User/product goals, target users, area/flow knowledge, constraints, design recon, taste/reference evidence, content, and technical boundaries.

## Method

1. Define user goal, product outcome, scope, non-goals, and primary decision/action.
2. Model information hierarchy, object/action relationships, navigation, and progressive disclosure.
3. Define screen/module anatomy, component tree, states, edge cases, permissions, responsive behavior, and accessibility requirements.
4. Reuse governed components and patterns; when no system exists, create a minimal local prototype UI contract.
5. Generate alternatives where trade-offs matter and select with explicit criteria.
6. Specify content needs and implementation constraints without designing impossible behavior.
7. Produce screen or module package with acceptance and Design QA criteria.

## Output contract

Produce a compact artifact containing:

- `Screen/Module Design Spec.`
- `Information hierarchy and component tree.`
- `State and responsive matrix.`
- `Alternatives, rationale, constraints, and handoff criteria.`

## Evidence standard

- Design claims must trace to user goal, evidence, system rule, or stated hypothesis.

## Stop and escalate

- Product outcome or key behavior is unresolved.
- Required component/contract decision changes scope.

## Failure modes to avoid

- Drawing a pretty layout without states.
- Inventing API behavior to make the design work.
