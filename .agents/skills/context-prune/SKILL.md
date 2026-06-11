---
name: context-prune
description: Compact project memory after major phases or context bloat by archiving detailed logs and preserving only current decisions, blockers, evidence links, and next action.
---

# context-prune

Use when context is bloated, after a major phase, before a new operation, or when context compression is frequent.

## Process
1. Identify the active ticket from `CURRENT.md`.
2. Move detailed history from `CHRONICLE.md` into `chronicle/`.
3. Keep `CHRONICLE.md` as a compact rescue summary.
4. Keep active details inside `tasks/<active-ticket>.md`.
5. Archive closed ticket details when they do not affect current work.
6. Preserve decisions, blockers, approvals, evidence links, and next action.
7. Report what was pruned and what remains loaded.

## Output
- Files updated.
- Information preserved.
- Information archived.
- Current next action.
- Risks of lost context, if any.
