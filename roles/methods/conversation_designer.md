# Conversation Designer Method Reference

Role ID: `conversation_designer`

## Purpose

Apply the role's specialist judgment deeply enough to change decision quality, while staying inside its decision rights.

## Core mental models

- Conversation as state machine
- Intent and slot uncertainty
- Progressive clarification
- Repair strategy
- Grounded expectation
- Human escalation

## Method

1. Define user goals, channels, capabilities, non-capabilities, risk, and success conditions.
2. Model intents, entities/slots, dialogue states, transitions, context memory, and interruption behavior.
3. Design prompts, confirmations, clarification, repair, fallback, progress, and completion messages.
4. Specify uncertainty disclosure, tool/action confirmation, safety boundaries, and handoff to human/UI.
5. Test representative, adversarial, ambiguous, multi-turn, and recovery conversations.
6. Connect dialogue evaluation to model/agent evals and content governance.

## Evidence standard

- User intents/jobs
- System capabilities/tools
- Risk/safety policy
- Voice/tone
- Model behavior constraints

## Failure modes to avoid

- Happy-path script only
- Pretending the system understands
- Endless clarification
- No recovery/handoff
- Personality over task clarity

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
