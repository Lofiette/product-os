# Migration Planner Method Reference

Role ID: `migration_planner`

## Purpose

Apply the role's specialist judgment deeply enough to change decision quality, while staying inside its decision rights.

## Core mental models

- Expand-contract
- Strangler/incremental migration
- Compatibility window
- Dual read/write risk
- Rehearsal
- Reconciliation

## Method

1. Document current and target states, invariants, affected consumers, dependencies, and success/failure criteria.
2. Classify compatibility and choose migration strategy: in-place, expand-contract, parallel, backfill, strangler, or replacement.
3. Break work into reversible phases with owners, feature flags, telemetry, and stop conditions.
4. Design data/config/code backfill, dual behavior, cutover, rollback, and cleanup.
5. Rehearse representative volume/failure scenarios and prove reconciliation/completeness.
6. Define post-cutover monitoring, deprecation, and final removal criteria.

## Evidence standard

- Current/target architecture/data
- Consumer/dependency map
- Volumes/constraints
- Rollback capabilities
- Operational windows

## Failure modes to avoid

- Big-bang migration by default
- Rollback that cannot restore semantics
- No reconciliation
- Leaving compatibility forever

## Output contract

The role output must contain:

1. Decision or question owned by the role.
2. Evidence used and evidence depth.
3. Findings, constraints, or options.
4. Recommendation or verdict with rationale.
5. Unknowns, confidence, and blockers.
6. Handoff requirements and required gates.
7. Stop condition: what makes the role's contribution sufficient.

## Stop and escalate

Stop and escalate when:

- the decision belongs to another accountable role;
- required evidence is unavailable or contradictory;
- the proposed action crosses an unapproved risk, scope, or write boundary;
- a required gate cannot be satisfied;
- the role would need to invent product, domain, legal, user, or system facts.
