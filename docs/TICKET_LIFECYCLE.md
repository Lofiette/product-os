# TICKET_LIFECYCLE.md

## Statuses

- `Backlog` — captured but not ready.
- `Ready` — scoped and ready.
- `Intake` — being briefed.
- `In Progress` — active work.
- `Blocked` — waiting for decision/evidence.
- `Review` — implementation or artifact under review.
- `Done` — complete and summarized.
- `Archived` — inactive; do not load by default.

## Lifecycle rules

- Only one primary active ticket by default.
- Do not move a ticket to `Done` without acceptance criteria, gate status, and next-action summary.
- Move detailed history to `chronicle/` before closing long tickets.
- Archive closed tickets when they are no longer needed for current decisions.
