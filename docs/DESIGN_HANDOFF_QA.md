# DESIGN_HANDOFF_QA.md

Use when Codex designs a UI/module that a human developer will later rebuild or implement.

## Design handoff QA checklist

- Module/screen purpose is clear.
- Design-system mode is identified.
- Component matrix references real DS components or approved placeholders.
- State matrix covers empty, loading, success, error, disabled, permission, overflow, and responsive states as relevant.
- Content matrix covers primary CTAs, helper text, validation, empty states, errors, confirmations, and destructive actions.
- Accessibility notes cover labels, focus, keyboard, headings, dialogs, tables, and announcements as relevant.
- Developer rebuild brief lists files/patterns to inspect, implementation constraints, and non-goals.
- Deviations are explicit and approved.

## Handoff verdict

Return one of:
- PASS
- PASS WITH WARNINGS
- BLOCKED

BLOCKED if the module/screen cannot be implemented from the package without guessing core layout, state behavior, components, or copy.
