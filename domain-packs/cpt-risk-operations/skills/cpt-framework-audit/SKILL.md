---
name: cpt-framework-audit
description: Use explicitly to audit CPT routing, runtime, skills, gates, artifacts, and contradictions; not as routine task review.
---

# CPT Framework Audit

## Use when

- Preparing a CPT release, migration, or major framework change.
- Observed behavior suggests routing, enforcement, or documentation drift.

## Do not use when

- Reviewing ordinary application implementation.
- The request only needs one domain-specific quality gate.

## Required inputs

- Framework package, registries, schemas, tests/evals, installer behavior, and representative traces.
- Declared architecture and acceptance criteria.

## Method

1. Inventory files, plugins, skills, roles, schemas, and runtime paths.
2. Compare declared architecture with executable behavior and installation surface.
3. Detect duplicate or conflicting sources of truth.
4. Measure always-loaded context and skill metadata budgets.
5. Review each critical workflow for trigger, method, artifact, enforcement, and recovery.
6. Run structural validators and behavioral evals; distinguish PASS from untested claims.
7. Classify findings by severity, evidence, benefit, and migration risk.
8. Propose only changes that improve quality, safety, maintainability, or resource use.

## Output contract

Produce a compact artifact containing:

- `Evidence-backed findings with severity.`
- `Contradiction and source-of-truth map.`
- `Context/metadata/resource measurements.`
- `Prioritized release plan and explicitly rejected changes.`

## Evidence standard

- Cite files, test outputs, traces, or official platform behavior.
- Do not infer successful runtime behavior from file existence.

## Stop and escalate

- The package version or baseline is ambiguous.
- Required fixtures are missing.
- A recommendation depends on unverified platform behavior.

## Failure modes to avoid

- Inventing improvements to fill a roadmap.
- Treating green structural tests as behavioral proof.
- Auditing only documentation and ignoring installer/runtime code.
