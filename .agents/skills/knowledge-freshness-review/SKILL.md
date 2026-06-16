---
name: knowledge-freshness-review
description: Review Product Knowledge freshness after code/product changes without rereading the whole repository.
---

# knowledge-freshness-review

Use after tasks that may make Product Knowledge stale.

## Procedure

1. Start with `git diff --stat` or the task's changed-file list.
2. Match changed files to `review_trigger` fields.
3. Mark affected artifacts `needs-review` when evidence may be stale.
4. Reread only affected files if approved.
5. Do not refresh unrelated maps.
6. Prefer small targeted corrections over full remapping.

## Output

Freshness Review:

- changed files considered;
- affected artifacts;
- freshness changes;
- confidence changes;
- targeted rereads needed;
- approval request.
