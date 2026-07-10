---
name: cpt-implementation-review
description: Use to review implementation against approved scope, contracts, tests, quality gates, risk, and handoff; not as a replacement for domain-specific review.
---

# CPT Implementation Review

## Use when

- Meaningful code changes are ready for review or completion.

## Do not use when

- No implementation exists.
- The request is solely visual acceptance or security threat modeling.

## Required inputs

- Task/Impact Map/lease, diff, relevant code, tests, build/lint results, product/design/API contracts, gates, and known risks.

## Method

1. Confirm the diff matches approved outcome and scope; identify unrelated changes.
2. Trace changed behavior through callers, state/data flow, errors, permissions, and lifecycle.
3. Review correctness, maintainability, duplication, naming, types, boundaries, and failure handling.
4. Check tests for behavior, regression, edge cases, and false confidence.
5. Invoke relevant domain gates for UI, API, data, security, privacy, performance, or migration.
6. Classify findings by blocker/major/minor and distinguish evidence gaps.
7. Prepare concise reviewer/handoff summary, release notes, limitations, and knowledge updates.

## Output contract

Produce a compact artifact containing:

- `Scope/diff summary.`
- `Findings with severity, evidence, impact, and fix.`
- `Verification and gate results.`
- `PASS/WARN/BLOCKED verdict plus handoff/release summary.`

## Evidence standard

- A passing build does not prove behavior or product quality.

## Stop and escalate

- Diff exceeds approved lease or contains unknown generated changes.
- Critical verification is missing.

## Failure modes to avoid

- Nitpicking style while missing behavior.
- Approving because tests passed without assessing test coverage.
