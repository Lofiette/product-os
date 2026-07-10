---
name: cpt-customer-journey
description: Use to map end-to-end customer journeys, service blueprints, channels, support signals, handoffs, and backstage dependencies.
---

# CPT Customer Journey

## Use when

- The experience crosses screens, teams, channels, support, or operational systems.
- Support data suggests repeated customer pain requiring journey-level analysis.

## Do not use when

- The task is a single local UI interaction with no cross-channel impact.

## Required inputs

- Actor/segment, job, journey boundary, channels, evidence, support signals, systems, policies, and service owners.

## Method

1. Define trigger, desired outcome, journey start/end, and actor.
2. Map stages, actions, touchpoints, expectations, emotions, evidence, and failure/recovery paths.
3. Map frontstage people/UI and backstage teams, systems, policies, data, and dependencies.
4. Aggregate support signals by frequency, severity, segment, and confidence; do not infer prevalence from anecdotes.
5. Identify handoff failures, waiting, duplicate effort, broken ownership, and service-level risks.
6. Prioritize opportunities by user impact, operational leverage, evidence, and feasibility.
7. Assign owners and measurements for redesigned service moments.

## Output contract

Produce a compact artifact containing:

- `Journey map and service blueprint.`
- `Support-signal evidence table.`
- `Moments of truth, failures, handoffs, and opportunities.`
- `Owners, measures, and validation needs.`

## Evidence standard

- Each pain point should cite research, analytics, support data, or be labeled hypothesis.

## Stop and escalate

- Journey boundary or actor is too broad.
- Backstage ownership cannot be established.

## Failure modes to avoid

- Creating an empathy poster without operational dependencies.
- Treating ticket count as unique-user frequency.
