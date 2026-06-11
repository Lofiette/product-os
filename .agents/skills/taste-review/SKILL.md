---
name: taste-review
description: Review design/UI/content output against the Taste Profile, good/bad examples, DS fidelity, clarity, and craft quality.
---

# TASTE_REVIEW.md — Taste Review Gate

Use Taste Review when a task affects product design, UI concept, prototype quality, visual direction, UX copy, design-system fidelity, or user-facing experience.

Do not use Taste Review for purely backend, mechanical refactor, dependency-only, or test-only tasks unless the user explicitly asks.

## Inputs

- Active task ticket taste fields.
- docs/TASTE_PROFILE.md.
- User-provided good/bad examples, if any.
- Screen Design Spec / Module Design Package / Prototype UI Kit Contract.
- Design-system mode and DS evidence.
- Rendered UI or screenshots, if implementation exists.

## Review dimensions

1. User clarity.
2. Information hierarchy.
3. Action priority.
4. State usefulness.
5. Copy specificity.
6. Design-system fidelity.
7. Visual rhythm and density.
8. Craft completeness.
9. Consistency with good examples.
10. Avoidance of bad examples / anti-taste.

## Output schema

```markdown
## Taste Review

### Verdict
PASS / PASS WITH WARNINGS / BLOCKED

### Taste profile used

### What feels right

### What feels off
| Issue | Evidence | Impact | Fix | Blocking? |
|---|---|---|---|---|

### Good examples matched

### Bad examples avoided / violated

### Design-system taste

### Top fixes without scope expansion

### Approval needed
```

## BLOCKED conditions

- Primary user action is unclear.
- Design-system component exists but custom lookalike was used without approval.
- The UI contradicts the project’s explicit bad examples.
- Empty/error states are decorative or dead-end in a user-critical flow.
- Visual hierarchy directs attention away from the user’s main job.
- The final artifact claims taste alignment without evidence.
