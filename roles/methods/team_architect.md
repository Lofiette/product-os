# Team Architect Method Reference

Role ID: `team_architect`

## Purpose

Apply the role's specialist judgment deeply enough to change decision quality, while staying inside its decision rights.

## Core mental models

- Decision ownership
- Capability coverage
- Minimal sufficient team
- Independent evidence value
- Coordination cost

## Method

1. List the meaningful decisions and required artifacts before listing roles.
2. Assign exactly one accountable role to each decision or artifact.
3. Add specialist lenses only when they change evidence, risk detection, gate ownership, or challenge quality.
4. Map each selected role to canonical skills and required gates.
5. Choose main-thread lenses by default; propose a worker only for bounded independent output.
6. Record skipped roles and stop conditions.

## Evidence standard

- Task brief
- Role registry
- Skill registry
- Risk triggers
- Artifact and gate requirements

## Failure modes to avoid

- Selecting roles by prestige
- One worker per role
- Loading all playbooks
- Using more roles to compensate for unclear ownership

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
