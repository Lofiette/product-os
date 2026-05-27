---
name: current-page-ui-review
description: Use when reviewing a rendered page or interface prototype for product clarity, DS fidelity, taste, obvious UI issues, and implementation fidelity.
---

Follow `docs/UI_REVIEW_RUNBOOK.md`.

Default execution:
- Build a UI Review Packet first.
- Use main-thread multi-lens review for Fast/Standard unless the user approves real subagents.
- If spawning reviewers, use at most two by default and apply subagent failure recovery.

Required gates:
- Product clarity
- Primary action clarity
- State coverage
- Design-system fidelity
- Taste profile alignment, if active
- Obvious UI errors
- Accessibility basics
- Responsive risks

Output: PASS / PASS WITH WARNINGS / BLOCKED with evidence and required fixes.
