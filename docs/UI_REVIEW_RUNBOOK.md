# UI_REVIEW_RUNBOOK.md

Use this runbook when the user asks to review a rendered page or prototype.

## Step 1 — Collect evidence

- Confirm target URL/route.
- Capture or inspect screenshot/rendered page when possible.
- Identify changed files and component sources.
- Run or inspect console/build/lint status if available.
- Determine design-system mode.
- Create a `UI Review Packet`.

## Step 2 — Choose execution mode

- Fast visual sanity check: main-thread multi-lens review.
- Standard UI review: spawn at most one or two reviewers after approval.
- High-stakes UI review: spawned reviewers allowed, but use quorum and failure policy.

## Step 3 — Run gates

Always cover:

- Product clarity
- Primary action clarity
- State coverage
- Design-system fidelity
- Taste profile alignment, if active
- Obvious UI errors
- Accessibility basics
- Responsive risks

## Step 4 — Verdict

Return:

```markdown
Verdict: PASS / PASS WITH WARNINGS / BLOCKED
Subagent completion status:
Top blockers:
Required fixes:
Optional improvements:
Evidence limitations:
```

If review agents hang, do not wait indefinitely. Apply `SUBAGENT_FAILURE_POLICY.md`.
