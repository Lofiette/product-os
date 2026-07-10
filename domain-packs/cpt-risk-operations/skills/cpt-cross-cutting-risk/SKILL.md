---
name: cpt-cross-cutting-risk
description: Use to integrate security, privacy, reliability, safety, compliance, migration, and operational risks into one decision verdict.
---

# CPT Cross Cutting Risk

## Use when

- A task has multiple risk domains or needs a single gate decision.

## Do not use when

- One specialist review fully covers the risk.

## Required inputs

- Task/Impact Map, domain risk reviews, severity model, acceptance policy, mitigations, owners, verification, and rollout.

## Method

1. Identify triggered risk domains and avoid reviewing untriggered domains ceremonially.
2. Normalize findings by severity, likelihood, impact, confidence, and reversibility.
3. Detect interacting risks and mitigation conflicts.
4. Separate must-fix blockers, pre-release conditions, monitored residual risk, and out-of-scope issues.
5. Verify owners, dates, tests, rollback, and waiver authority.
6. Produce consolidated PASS/WARN/BLOCKED or GO/NO-GO decision without overriding specialist evidence.

## Output contract

Produce a compact artifact containing:

- `Risk register and triggered-domain coverage.`
- `Consolidated blockers/conditions/residual risk.`
- `Owners, verification, waivers, and decision verdict.`

## Evidence standard

- Missing specialist evidence stays missing; do not average it away.

## Stop and escalate

- Required domain review is unavailable.
- Risk acceptance owner is absent.

## Failure modes to avoid

- Making every task high risk.
- Collapsing incomparable risks into one numeric score.
