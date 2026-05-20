# ROLE_OUTPUT_SCHEMAS.md

Every selected role must produce a compact artifact, not generic advice. Use the role playbook’s `Strict output schema v1.3`.

## Universal schema

```markdown
## <Codename> / <Role> output

### Artifact
<name of artifact produced>

### Decision supported
<which decision this output enables>

### Evidence level
- Repository evidence:
- User-provided evidence:
- External evidence:
- Assumptions:
- Hypotheses:

### Findings / recommendations
<concise role-specific result>

### Handoffs
<downstream roles or user decisions>

### Blockers / escalations
<what must be resolved before proceeding>
```

## Verdict roles

Consistency Auditor, Code Reviewer, Security Reviewer, Privacy Reviewer, AI Safety Reviewer, and QA Engineer must include one of:

- PASS
- PASS WITH WARNINGS
- BLOCKED
- REQUEST CHANGES

## Review mode is read-only

In Review/Audit mode, reviewers must not edit files. They may propose patches, but implementation requires explicit user approval and a switch to implementation mode.


## ULTIMATE role-specific artifact minimums

- Research roles: include decision supported, method choice, evidence table, confidence level, assumptions, and next data needed.
- UX/design roles: include flow/state/content/accessibility/component implications and handoffs.
- Engineering roles: include files/areas affected, system boundaries, trade-offs, verification approach, and risk gates.
- AI/ML roles: include behavior contract, context/data map, eval matrix, failure taxonomy, fallback/human escalation, and monitoring signals.
- Risk roles: include assets/data/actors, threat or compliance concern, severity, evidence, mitigation, and tests/checks.
- Review roles: include verdict, blocking issues, non-blocking issues, missing evidence/tests, and merge/approval recommendation.

## Required tables for high-risk work

High-risk AI, security, privacy, migration, release, or public API work must include at least one compact table for risks and mitigations. If the role cannot fill the table from evidence, it must mark unknowns instead of guessing.
