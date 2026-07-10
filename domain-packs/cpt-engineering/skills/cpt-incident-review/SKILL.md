---
name: cpt-incident-review
description: Use to investigate incidents with timeline, impact, contributing factors, root causes, remediation, and prevention; not to assign blame.
---

# CPT Incident Review

## Use when

- A production or operational failure needs structured learning and corrective action.

## Do not use when

- The issue is an unshipped bug with no incident impact.

## Required inputs

- Incident window, telemetry, changes, user/business impact, communications, responders, mitigations, and system context.

## Method

1. Define severity, affected users/systems, duration, detection, and current status.
2. Build evidence-based timeline with uncertainty and source references.
3. Separate trigger, contributing conditions, latent weaknesses, and detection/response gaps.
4. Analyze technical, process, ownership, tooling, capacity, and organizational factors.
5. Evaluate mitigation effectiveness and what slowed diagnosis/recovery.
6. Create corrective actions across immediate, preventive, detective, and resilience layers with owners/dates.
7. Define verification and recurrence indicators; communicate blamelessly.

## Output contract

Produce a compact artifact containing:

- `Impact and timeline.`
- `Root/contributing cause analysis.`
- `Response and detection review.`
- `Prioritized corrective actions, owners, verification, and follow-up.`

## Evidence standard

- Do not declare root cause from correlation alone.

## Stop and escalate

- Evidence is incomplete enough to make conclusions unsafe.

## Failure modes to avoid

- Writing “human error” as root cause.
- Creating actions with no owner or verification.
