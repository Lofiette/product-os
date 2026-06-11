---
name: context-snapshot
description: Create a lightweight recovery checkpoint before major changes, long runs, context pruning, or context-loss recovery.
---

# context-snapshot

Use before major changes, long subagent runs, context pruning, or when resuming after context loss.

## Process
1. Read `CURRENT.md` and the active ticket.
2. Summarize current objective, decisions, blockers, evidence links, files changed, and next operation.
3. Write a snapshot under `context/snapshots/`.
4. Link the snapshot from the active ticket or `CHRONICLE.md` if it affects recovery.

## Output
- Snapshot path.
- Recovery summary.
- Next action.
