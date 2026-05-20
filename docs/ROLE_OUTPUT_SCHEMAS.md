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
