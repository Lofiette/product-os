# ANTICIPATION_BRANCH.md

## Purpose

The Anticipation Branch generates proactive, perspective-building suggestions that may improve the result before the user asks. It must not silently expand scope.

Think of it as a lightweight product foresight mechanism:

```text
observe signal → anticipate expectation → propose option → ask confirmation → update plan only if approved
```

## What counts as anticipation

- A user expectation likely implied by the task but not explicitly stated.
- A quality risk that will become visible later.
- A missing state, flow, or constraint that users will likely encounter.
- A design-system or implementation issue that will create rework.
- A small product improvement with high likely value and low scope impact.
- A creative alternative surfaced by methods like focal objects, synectics, SCAMPER, pre-mortem, or Opportunity Solution Tree.

## What is not allowed

- Do not implement proactive ideas without approval.
- Do not treat generated ideas as evidence.
- Do not expand scope because the idea is interesting.
- Do not run continuous ideation loops during implementation.
- Do not use anticipation to bypass acceptance criteria.

## Anticipation levels

| Level | Meaning | Action |
|---|---|---|
| A-0 | No impact | Ignore or log only |
| A-1 | Small quality improvement, no scope change | Suggest inline or include if user confirms |
| A-2 | Changes acceptance criteria or deliverable | Ask approval before changing plan |
| A-3 | Changes team, risk, architecture, DS contract, or research need | Re-route and ask approval |
| A-4 | Reveals blocker | Stop and escalate |

## Required proposal format

```markdown
## Anticipation Proposal

### Signal
What triggered the suggestion.

### Anticipated expectation
What the user/stakeholder/end user may expect later.

### Proposed improvement

### Why now

### Evidence level
Evidence / assumption / hypothesis / taste judgment / generated idea

### Impact
Scope, roles, skills, DS, implementation, verification

### Recommendation
Approve now / backlog / reject / needs clarification
```

## Rule

Anticipation improves quality only when it is explicit, bounded, and approved. Otherwise it is scope creep wearing a nice hat.
