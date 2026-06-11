# QUALITY_GATES.md

Use PASS / PASS WITH WARNINGS / BLOCKED.

## Universal gates
- Scope matches the approved active task ticket.
- Claims are evidence-labeled.
- Required roles/skills executed or intentionally skipped.
- Tests/checks run or limitations stated.
- Chronicle updated when durable state changed.

## UI gates
- Design recon completed when UI repo/DS involved.
- Screen Design Spec exists for screen creation/redesign.
- DS compliance checked.
- Visual QA attempted or limitation stated.
- UI obvious errors checklist has no blockers.

## Risk gates
- Security/privacy/AI/migration/release gates passed when triggered.

## Review levels
See REVIEW_LEVELS.md.


## Taste Review Gate

Use when task affects product/UI/design/prototype/content quality and a Taste Profile exists or can be inferred.

Report:
- taste profile used;
- good examples matched;
- bad examples avoided or violated;
- visible craft issues;
- DS/taste deviations;
- top fixes without scope expansion.

Verdict: PASS / PASS WITH WARNINGS / BLOCKED.

BLOCKED if avoidable UX confusion, DS drift, visible craft failure, or contradiction with explicit bad examples remains unresolved.
