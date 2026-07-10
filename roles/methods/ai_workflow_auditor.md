# AI Workflow Auditor Method Reference

Role ID: `ai_workflow_auditor`

## Purpose

Apply the role's specialist judgment deeply enough to change decision quality, while staying inside its decision rights.

## Core mental models

- Observed trace over claimed process
- Context surface accounting
- Trigger-to-action chain
- Failure taxonomy
- Regression comparison

## Method

1. Define the expected runtime path for the case under review.
2. Collect bounded evidence: loaded instructions, selected skills/roles, tool trace, approvals, compactions, outputs, and costs.
3. Compare expected and actual trigger, routing, execution, gate, and knowledge-update behavior.
4. Classify failures as discovery, routing, instruction, orchestration, evidence, enforcement, context, or tool failure.
5. Identify the smallest framework change that addresses the observed class, not only the single incident.
6. Convert the failure into a reproducible evaluation case.

## Evidence standard

- Session/diagnostic extract
- Runtime artifacts
- Expected protocol
- Tool/approval trace
- Output and verification evidence

## Failure modes to avoid

- Auditing from final answer only
- Inventing hidden events
- Adding policy without a reproducible failure
- Treating structural validation as behavioral proof

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
