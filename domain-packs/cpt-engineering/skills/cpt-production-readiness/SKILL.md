---
name: cpt-production-readiness
description: Use to plan or review production service/release readiness across architecture, security, privacy, performance, rollout, rollback, support, and verification.
---

# CPT Production Readiness

## Use when

- A meaningful feature/service is approaching production, rollout, or launch.

## Do not use when

- A prototype is explicitly disposable and will not be released.

## Required inputs

- Product scope, architecture, dependencies, quality gates, test results, risk reviews, deployment environment, SLOs, flags, rollback, ownership, and support plan.

## Method

1. Partition review into product, architecture, data/API, UI/DS, security/privacy, performance, reliability, operations, and support.
2. Confirm acceptance, test evidence, monitoring, capacity, failure modes, and dependency readiness.
3. Define environment/config/secrets, CI/CD, feature flags, rollout rings, migrations, and compatibility.
4. Verify backup, rollback/forward-fix, incident ownership, runbooks, and customer/support communication.
5. Classify blockers, accepted risks, waivers, and post-launch measurements.
6. Produce go/no-go decision with explicit owner and evidence.

## Output contract

Produce a compact artifact containing:

- `Readiness matrix by domain.`
- `Blockers, waivers, owners, and due dates.`
- `Rollout/rollback/monitoring/support plan.`
- `GO / CONDITIONAL GO / NO-GO verdict.`

## Evidence standard

- A checklist item is complete only with evidence, owner, or explicit waiver.

## Stop and escalate

- Rollback or critical monitoring is absent.
- Unaccepted high-severity risk remains.

## Failure modes to avoid

- Treating deployment success as product readiness.
- Reviewing every domain shallowly without expert gates.
