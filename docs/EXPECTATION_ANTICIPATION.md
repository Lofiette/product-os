# EXPECTATION_ANTICIPATION.md — Anticipation Branch

The Anticipation Branch helps the team propose forward-looking improvements that the user did not explicitly request, but may reasonably expect or appreciate. It prevents silent scope creep by requiring explicit human approval.

## Purpose

- Surface high-leverage improvements before implementation becomes expensive.
- Detect hidden expectations from task context, design-system rules, user audience, quality bar, and product conventions.
- Convert promising ideas into clear proposals instead of sneaking them into scope.

## What anticipation is not

- Not automatic scope expansion.
- Not a license to redesign everything.
- Not a replacement for evidence.
- Not a requirement for Tiny/Fast Lane tasks.
- Not a way to bypass approval gates.

## Anticipation levels

- **A0 — No meaningful proposal.** Continue without noise.
- **A1 — Small polish within approved scope.** Can be included if reversible and no gate is triggered.
- **A2 — Quality improvement that affects acceptance criteria.** Ask approval.
- **A3 — Directional improvement that changes scope/team/architecture.** Re-route and ask approval.
- **A4 — Critical hidden expectation or blocker.** Stop and ask.

## Triggers

Use anticipation when:
- task is product/design/UI/prototype/module/service planning;
- user asks for quality, taste, “make it better”, or “think ahead”;
- design-system constraints imply missing states/patterns;
- support/research/analytics signal suggests a better direction;
- implementation reveals a simpler or more robust path;
- current plan meets stated requirements but may disappoint likely user expectations.

Do not use by default for:
- typo fixes;
- dependency bumps;
- mechanical refactors;
- isolated backend bugs;
- tasks under strict scope freeze.

## Proposal budget

Default: max 3 anticipation proposals per planning cycle.
Use more only when the user explicitly asks for an ideation sprint.

## Output schema

```markdown
## Anticipation Proposals

### Summary

| ID | Level | Proposal | Why now | Evidence / assumption | Value | Cost | Risk | Approval needed |
|---|---|---|---|---|---|---|---|---|

### Recommended decision
- Approve now:
- Park for later:
- Reject:

### Scope impact

### Required roles/skills if approved
```

## Approval rule

A2/A3/A4 proposals must not be implemented until the user approves them. If approved, update TASK.md decisions and CHRONICLE.md.
