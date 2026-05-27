# CREATIVE_TENSION.md — Controlled Creative Tension

Creative tension is a lightweight critique method. It is not roleplay and not a debate club. It uses conflicting professional perspectives to improve a decision before implementation or before final handoff.

## When to use

- Product/UI concept feels adequate but not strong.
- There are multiple reasonable design directions.
- The task asks for “better”, “premium”, “clearer”, “more human”, “more polished”, or “less corporate”.
- A stakeholder idea could improve the result.
- A team member senses a visible quality issue but cannot yet name it.

## When not to use

- Tiny/Fast Lane mechanical changes.
- Already approved implementation with no new evidence.
- High-risk tasks where safety/security review must happen first.
- When creative exploration would change scope without approval.

## Perspectives

### Clarity Advocate
What makes the decision easier to understand?

### Craft Critic
Where does it look unfinished, accidental, or inconsistent?

### System Guardian
Where does it violate reusable components, tokens, language, or patterns?

### User Advocate
Where could a real user hesitate, misread, or feel blamed?

### Business Pragmatist
Where are we improving something that does not affect the product goal?

### Creative Challenger
What small change could make the result noticeably better without expanding scope?

## Output schema

```markdown
## Creative Tension Brief

### Decision under review

### Perspectives applied
| Perspective | Challenge | Evidence/assumption | Proposed improvement |
|---|---|---|---|

### Shortlist
| Candidate | Value | Cost | Risk | Scope impact |
|---|---|---|---|---|

### Recommendation

### Approval needed
```

## Rule

Creative tension produces candidates and critiques, not proof. Do not implement candidates until approved if they affect scope, risk, architecture, or committed design direction.
