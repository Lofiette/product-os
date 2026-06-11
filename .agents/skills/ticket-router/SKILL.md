---
name: ticket-router
description: Route new user instructions to the active ticket, a new ticket, a follow-up, or archive based on deliverable and approval boundaries.
---

# ticket-router

Use at intake and when the user adds new instructions.

## Decision rules
Create a new ticket if the new work has an independent deliverable, acceptance criteria, approval gate, evidence packet, or can be done separately.
Update the active ticket if the instruction only clarifies scope, constraints, examples, or acceptance criteria.
Park as follow-up if it is useful but out of current scope.

## Output
- Route: active ticket / new ticket / follow-up / archive.
- Reason.
- Required ticket updates.
- Whether user approval is needed.
