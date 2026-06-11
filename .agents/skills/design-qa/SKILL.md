---
name: design-qa
description: Validate a screen/module design or implementation against specs, states, DS rules, accessibility, copy, responsive behavior, and handoff requirements.
---


# design-qa

## Purpose

Provide a final design-quality gate before handoff or completion.

## Procedure

1. Load the relevant design artifact: Screen Design Spec, Module Design Package, or Prototype UI Kit Contract.
2. Load DS Compliance Report if DS exists.
3. Run or reference UI Heuristic Audit.
4. Check state matrix coverage.
5. Check content/copy completeness.
6. Check accessibility basics.
7. Check responsive assumptions.
8. Return a gate verdict.

## Output schema

```markdown
## Design QA Report

### Artifact checked
### Verdict
PASS / PASS WITH WARNINGS / BLOCKED
### Missing states
### DS compliance issues
### Copy/content issues
### Accessibility issues
### Responsive issues
### Required fixes before done
### Approved exceptions
```

## BLOCKED conditions

- Implementation/handoff cannot be evaluated because required design artifact is missing.
- A blocker from UI/DS/a11y/state checks remains unresolved.

## Stop conditions

- Required evidence is missing and the next step would require guessing.
- The skill would change approved scope.
- A risk gate requires user approval.
- Another role owns the decision and has not been consulted.



## Culture and taste gate

Design QA must include team culture and taste checks when applicable:
- user stewardship;
- craft discipline;
- system fidelity;
- content clarity;
- approved proactive suggestions only.
