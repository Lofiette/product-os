---
name: cpt-design-handoff
description: Use to produce and validate design-to-development handoff so implementation does not require guessing structure, states, components, content, or constraints.
---

# CPT Design Handoff

## Use when

- A design/module is delivered for later implementation or rebuild.

## Do not use when

- The same task includes immediate implementation by the same agent with sufficient specs already present.

## Required inputs

- Approved screen/module design, component/state/content matrices, design-system references, responsive/accessibility rules, product acceptance, and known technical constraints.

## Method

1. Package goal, scope, surfaces, flow, information hierarchy, and component tree.
2. Map each UI element to existing component/variant/token or approved deviation.
3. Include state, data, permission, responsive, content, accessibility, and edge-case requirements.
4. Specify interactions, transitions, loading/error/recovery, and unresolved product decisions.
5. Provide asset/reference links and exact source authority.
6. Write developer rebuild brief and behavior-level acceptance criteria.
7. Run handoff QA: identify every place a developer would need to invent behavior, structure, or copy.

## Output contract

Produce a compact artifact containing:

- `Developer Rebuild Brief.`
- `Component/content/state/responsive matrices.`
- `Acceptance and Design QA checklist.`
- `PASS/WARN/BLOCKED handoff verdict and open decisions.`

## Evidence standard

- A screenshot alone is not a handoff specification.

## Stop and escalate

- Critical product behavior or component choice is unresolved.

## Failure modes to avoid

- Documenting pixels but not states.
- Leaving API/data assumptions implicit.
