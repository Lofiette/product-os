---
name: cpt-design-recon
description: Use to discover design-system mode, components, tokens, patterns, references, and UI constraints before design or coded UI work.
---

# CPT Design Recon

## Use when

- An existing product UI will be designed, redesigned, reviewed, or implemented.
- Design-system authority or available components are unclear.

## Do not use when

- The task has no user interface.
- The design sources and component contract are already current and sufficient.

## Required inputs

- Target surface/task, repository paths, design documents/references, component library, theme/tokens, and authority rules.

## Method

1. Classify design-system mode: none, emerging, component library, documented, or governed.
2. Identify authoritative, provisional, generated, and reference-only sources.
3. Map component imports, tokens, patterns, variants, layouts, states, responsive conventions, and accessibility norms.
4. Sample relevant existing screens and implementation patterns; avoid broad visual archaeology.
5. Identify forbidden raw UI, deviation process, missing components, and unstable sources.
6. Produce a bounded Design Recon Brief with evidence and confidence.

## Output contract

Produce a compact artifact containing:

- `Design-system mode and source-authority hierarchy.`
- `Relevant component/token/pattern registry.`
- `Existing comparable surfaces and constraints.`
- `Gaps, deviations, and next reads.`

## Evidence standard

- A generated manifest cannot validate itself in the same operation.
- “Looks similar” is not source evidence.

## Stop and escalate

- Authoritative source cannot be determined.
- Required reference or component source is unavailable.

## Failure modes to avoid

- Reading the entire design repository.
- Assuming a framework default equals the product design system.
