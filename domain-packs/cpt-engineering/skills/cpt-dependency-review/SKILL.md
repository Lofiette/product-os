---
name: cpt-dependency-review
description: Use to assess dependency necessity, alternatives, maintenance, license, security, bundle/runtime cost, integration, and rollback.
---

# CPT Dependency Review

## Use when

- Adding, replacing, upgrading, or removing a third-party dependency.

## Do not use when

- The dependency decision is already governed and the change is routine lockfile refresh.

## Required inputs

- Capability need, current stack, candidate package/version, alternatives, usage scope, platform, security/license requirements, and maintenance horizon.

## Method

1. Define required capability and whether existing platform/code can satisfy it.
2. Compare alternatives on API fit, maturity, maintenance, adoption, release cadence, ownership, and lock-in.
3. Review license, provenance, security advisories, transitive dependencies, install scripts, and supply-chain risk.
4. Measure bundle/runtime/build cost and compatibility.
5. Design wrapper/boundary, fallback, update policy, and observability.
6. Plan proof of concept, migration, rollback, and removal criteria.

## Output contract

Produce a compact artifact containing:

- `Need/alternatives decision matrix.`
- `Security/license/maintenance/performance findings.`
- `Integration boundary, test, update, and rollback plan.`

## Evidence standard

- Popularity is not maintenance or security evidence.

## Stop and escalate

- License/security provenance is unacceptable or unknown for material use.

## Failure modes to avoid

- Adding a library for a one-line utility.
- Importing dependency APIs throughout the codebase without a boundary.
