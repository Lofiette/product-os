---
name: impact-map
description: Create an implementation-preflight map of product area, affected files, risks, unknowns, verification, and approval request.
---

# impact-map

Use before non-trivial implementation, UI changes, API-dependent changes, product behavior changes, or systemic edits.

## Required sections

1. User intent.
2. Relevant product area(s) and knowledge artifacts loaded.
3. Confirmed evidence vs inferred assumptions.
4. Files already read.
5. Proposed files to inspect next.
6. Proposed files to edit, if known.
7. Systemic impact: related screens/modes/components/states.
8. Roles/skills/gates selected.
9. Risks and unknowns.
10. Verification plan.
11. Approval request.

## Rules

- Do not use an Impact Map as permission to edit.
- Do not hide unknowns.
- If the task mentions a mode/state/component/pattern, search for related usages before proposing a one-screen edit.
- For UI work, include design-system and frontend-integration considerations.
- For API/data-dependent UI, include API/data contract considerations.
