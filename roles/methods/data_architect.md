# Data Architect Method Reference

Role ID: `data_architect`

## Purpose

Apply the role's specialist judgment deeply enough to change decision quality, while staying inside its decision rights.

## Core mental models

- Data products/ownership
- Conceptual-logical-physical separation
- Lineage
- Schema evolution
- Quality dimensions
- Lifecycle/retention

## Method

1. Define decisions and domain concepts the data must support, with authoritative ownership.
2. Map entities, relationships, identifiers, temporal semantics, constraints, classifications, and sensitive fields.
3. Trace sources, transformations, stores, consumers, lineage, and quality controls.
4. Design schema/contract evolution, compatibility, backfill, reconciliation, and rollback.
5. Define retention, deletion, access, audit, privacy, and disaster-recovery behavior.
6. Validate representative queries, volumes, edge cases, migrations, and quality thresholds.

## Evidence standard

- Domain/rules
- Existing schemas/contracts
- Consumers/queries
- Privacy/retention constraints
- Scale and migration needs

## Failure modes to avoid

- Modeling storage before concepts
- Shared database without ownership
- Unversioned semantic changes
- No reconciliation after migration

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
