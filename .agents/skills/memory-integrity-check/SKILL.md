---
name: memory-integrity-check
description: Verify ticketed memory consistency: active ticket, TASK_INDEX.md, TASK.md shim, compact CHRONICLE.md, packets, snapshots, and archive rules.
---

# memory-integrity-check

Use before release, after context-prune, after ticket moves, or when memory seems inconsistent.

## Checks
1. `CURRENT.md` active ticket exists.
2. Active ticket is listed in `TASK_INDEX.md`.
3. Only one primary current ticket exists.
4. `TASK.md` is only a compatibility pointer.
5. `CHRONICLE.md` is compact and does not contain detailed logs.
6. Referenced evidence packets and snapshots exist.
7. Closed tickets are not marked current.

## Output
Use the memory-integrity-report template with PASS/WARN/BLOCKED.
