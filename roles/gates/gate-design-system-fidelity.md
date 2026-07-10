# Design-System Fidelity Gate

Gate ID: `gate-design-system-fidelity`

## Apply when

Whenever a design system, component library, token system, or governed UI source applies.

## Owners

- `design_system_guardian`
- `design_engineer`

## PASS criteria

- Canonical components, variants, tokens, and patterns are identified.
- Custom UI or deviations have explicit rationale and approval.
- Rendered result follows the source authority, not a self-generated manifest.

## BLOCK criteria

- An existing component is reimplemented locally without approval.
- Raw values or one-off variants bypass governed sources.
- A manifest created during the same task is used as sole proof of compliance.

## Required evidence

- Component/token usage map
- Source-authority record
- Approved deviation
- Rendered comparison

## Verdict contract

- `PASS`: required evidence supports the acceptance claim.
- `PASS_WITH_WARNINGS`: acceptance is supportable, with explicit non-blocking residual risk.
- `BLOCKED`: one or more blocking conditions are present.
- `INSUFFICIENT_EVIDENCE`: the gate cannot responsibly decide.

A warning must never hide a blocker. Missing evidence must never be converted into a clean pass.
