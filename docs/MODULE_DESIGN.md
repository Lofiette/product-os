# MODULE_DESIGN.md

Use when designing an entire product module, not just one screen.

## Required output: Module Design Package

```markdown
# Module Design Package

## 1. Module purpose
## 2. Users and jobs
## 3. Scope and non-goals
## 4. Object model
## 5. Navigation / IA model
## 6. Main flows
## 7. Screen inventory
| Screen | Purpose | Primary action | States | DS patterns |
## 8. Cross-screen state matrix
| Object/state | Where shown | UI behavior | Empty/error/loading |
## 9. Component matrix
| Need | DS component/pattern | Variant | Notes | Deviation? |
## 10. Content matrix
| Screen/state | Message | Owner | Localization notes |
## 11. Accessibility requirements
## 12. Responsive behavior
## 13. Analytics and instrumentation notes, if relevant
## 14. Developer Rebuild Brief
## 15. Open questions and risks
## 16. Acceptance criteria
```

## Gate

A module design is not complete until the component matrix, state matrix, and developer rebuild brief exist or the omission is explicitly approved.
