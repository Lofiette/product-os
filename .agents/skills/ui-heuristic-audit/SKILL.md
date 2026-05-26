---
name: ui-heuristic-audit
description: Run a compact but blocking UI audit for obvious interaction, hierarchy, state, copy, accessibility, responsive, and DS errors.
---


# ui-heuristic-audit

## Purpose

Catch obvious UI problems that code checks miss.

## Checklist

Return PASS/WARN/BLOCKED for each:

1. Primary action clarity.
2. Secondary/destructive action safety.
3. Information hierarchy.
4. Empty/loading/error/success states.
5. Form labels, validation, and helper text.
6. Copy clarity and CTA specificity.
7. Accessibility basics: labels, headings, keyboard/focus, dialogs, tables.
8. Responsive behavior and overflow.
9. Design-system component fidelity.
10. Token/spacing/density consistency.

## Output schema

```markdown
## UI Heuristic Audit

| Check | Verdict | Evidence | Required fix |
|---|---|---|---|

### Overall verdict
PASS / PASS WITH WARNINGS / BLOCKED
```

## BLOCKED conditions

- Any critical user action is unclear.
- A likely state is missing and blocks task completion.
- A governed DS exists and custom UI bypasses it.

## Stop conditions

- Required evidence is missing and the next step would require guessing.
- The skill would change approved scope.
- A risk gate requires user approval.
- Another role owns the decision and has not been consulted.

