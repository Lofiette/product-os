---
name: anticipation-radar
description: Identify likely future expectations, hidden quality risks, and proactive improvement proposals that require explicit approval before scope changes.
---


# anticipation-radar

## Purpose

Anticipate what the user, stakeholder, end user, developer, or reviewer may expect next, then propose bounded improvements without silently changing scope.

## Use when

- planning a design/product/production task;
- a new signal or idea appears during work;
- there is likely hidden expectation or handoff risk;
- the solution may be technically correct but strategically incomplete;
- user asks for proactive suggestions.

## Procedure

1. Load `docs/ANTICIPATION_BRANCH.md` and `docs/PROACTIVE_PROPOSALS.md`.
2. Identify signals: user wording, task context, DS mode, risk gates, quality gaps, support/research/analytics hints.
3. Generate 3–5 anticipated expectations maximum.
4. Classify each as A-0..A-4.
5. Convert relevant items into explicit proposals.
6. Ask for approval before changing scope, roles, skills, architecture, DS contract, or acceptance criteria.

## Output schema

```markdown
## Anticipation Radar

### Signals observed

### Anticipated expectations
| Expectation | Evidence level | Level | Proposed action |
|---|---|---|---|

### Proactive proposals requiring approval
| Proposal | Benefit | Cost | Scope impact | Recommendation | Approval question |
|---|---|---:|---|---|---|

### Backlog ideas
```

## BLOCKED conditions

- A-4 blocker found.
- A proactive idea was implemented without approval.

