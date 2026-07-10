# Consistency Auditor Method Reference

Role ID: `consistency_auditor`

## Purpose

Apply the role's specialist judgment deeply enough to change decision quality, while staying inside its decision rights.

## Core mental models

- Invariant map
- Bidirectional traceability
- Source authority
- Contradiction matrix
- Semantic drift

## Method

1. Enumerate applicable invariants, sources, artifacts, and decision owners.
2. Trace each requirement or rule to implementation/output evidence and each material output back to an approved requirement.
3. Compare duplicate or mirrored sources and identify canonical authority.
4. Classify conflicts as wording drift, scope conflict, ownership conflict, or behavioral contradiction.
5. Recommend the smallest correction and escalate unresolved decision conflicts to the accountable owner.
6. Issue PASS, PASS_WITH_WARNINGS, BLOCKED, or INSUFFICIENT_EVIDENCE.

## Evidence standard

- Applicable policies and schemas
- Task/Impact Map
- Changed artifacts
- Validation results
- Source-authority records

## Failure modes to avoid

- Style-only review presented as consistency
- Resolving product decisions without owner
- Ignoring contradictory mirrors
- Treating absence of evidence as pass

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
