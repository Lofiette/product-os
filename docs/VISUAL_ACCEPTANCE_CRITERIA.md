# VISUAL_ACCEPTANCE_CRITERIA.md

Use this document to prevent technical checks from masquerading as design quality.

## Non-equivalence rules

- Build success is not design success.
- Console-clean route is not visual QA.
- Raw-value scan pass is not DS compliance.
- Component import scan pass is not component correctness.
- Screenshot exists is not reference fidelity.
- “Looks similar” is not evidence.

## Final UI/design verdict requires

1. Source authority report.
2. Reference fidelity report if reference exists.
3. DS/prototype UI contract compliance.
4. Screenshot or explicit limitation.
5. Content realism review when prototype/demo data is used.
6. Debug control classification.
7. Taste Review if taste profile or examples exist.
8. Blockers fixed or explicitly accepted.

## Verdict rules

- `PASS`: all required evidence exists, no blockers, deviations approved.
- `PASS WITH WARNINGS`: non-blocking issues or missing evidence with user-accepted limitation.
- `BLOCKED`: unapproved DS drift, unproven reference fidelity, missing critical visual evidence, visible craft failure, misleading content, or unresolved debug controls.
