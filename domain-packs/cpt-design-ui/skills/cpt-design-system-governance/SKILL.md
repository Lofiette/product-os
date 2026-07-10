---
name: cpt-design-system-governance
description: Use to establish design-source authority, component/token contracts, manifest lifecycle, compliance, and approved deviations.
---

# CPT Design System Governance

## Use when

- A design system or component library governs UI decisions.
- Sources conflict, a manifest is generated, or a deviation/new component is proposed.

## Do not use when

- No reusable system is intended and the task is a disposable one-screen exploration.

## Required inputs

- Authoritative design/code sources, component registry, tokens, patterns, manifest, governance policy, and proposed UI.

## Method

1. Establish source hierarchy and classify each source as authoritative, provisional, reference, generated, or stale.
2. Freeze pre-task manifest/source revision before implementation.
3. Map components, variants, tokens, patterns, state/accessibility requirements, and forbidden raw UI.
4. Evaluate reuse, composition, extension, or new-component choice with systemic cost.
5. Record deviations with reason, owner, scope, expiry/review trigger, and migration path.
6. Prevent self-validation: task-generated manifest changes cannot prove compliance without approval.
7. Return PASS/WARN/BLOCKED with source evidence.

## Output contract

Produce a compact artifact containing:

- `Source Authority Report.`
- `Component/token/pattern contract.`
- `Manifest changes and approved deviations.`
- `Compliance verdict and required remediation.`

## Evidence standard

- Compliance requires actual component/token/source references, not visual resemblance.

## Stop and escalate

- No authoritative source can be established.
- A proposed deviation changes the system without ownership.

## Failure modes to avoid

- Writing a manifest after implementation and using it to approve the same UI.
- Creating local lookalikes of existing components.
