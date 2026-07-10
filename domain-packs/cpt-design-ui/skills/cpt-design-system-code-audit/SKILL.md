---
name: cpt-design-system-code-audit
description: Use to run deterministic code-level checks for design-system imports, raw values, duplicate primitives, and contract deviations.
---

# CPT Design System Code Audit

## Use when

- A coded UI claims design-system fidelity.
- A governed or documented design system requires enforceable checks.

## Do not use when

- No code exists yet.
- The design system has no machine-readable or code-level contract.

## Required inputs

- Design-system manifest/registry, source paths, allowed primitives/tokens/imports, exceptions, and changed files.

## Method

1. Confirm source authority and strictness mode before scanning.
2. Limit scan to changed/relevant files and exclude design-system implementation files where appropriate.
3. Check imports and use of governed components/variants.
4. Detect raw colors, spacing, radius, typography, shadows, inline styles, and native primitives where forbidden.
5. Detect duplicate local components or one-off visual patterns.
6. Compare findings to approved deviations and distinguish error, warning, and heuristic suspicion.
7. Return machine output plus human interpretation; never equate zero findings with complete design quality.

## Output contract

Produce a compact artifact containing:

- `Scan commands, scope, and tool versions.`
- `Violations by file/rule/severity.`
- `Approved exceptions and false-positive review.`
- `PASS/WARN/BLOCKED code-contract verdict.`

## Evidence standard

- Heuristic scanners prove only the rules they implement.

## Stop and escalate

- Manifest authority is provisional or self-generated.
- Scan scope is too broad or generated code dominates.

## Failure modes to avoid

- Treating import compliance as visual fidelity.
- Failing on native primitives inside the design-system source itself.
