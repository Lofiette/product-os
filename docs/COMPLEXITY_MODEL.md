# COMPLEXITY_MODEL.md — Minimum Sufficient Ceremony

The goal is not to maximize process. The goal is to apply the smallest amount of specialist thinking that prevents expensive mistakes.

## Complexity tiers

| Tier | Use when | Question budget | Role budget | Planning depth | Chronicle | Approval |
|---|---|---:|---:|---|---|---|
| Tiny | typo, copy tweak, trivial file change | 0–2 | 0–2 | inline | optional | user intent may be enough |
| Fast Lane | small low-risk task | 1–3 | 1–3 | short plan | compact if files change | required if files change |
| Standard | normal feature/fix/review | 3–7 | 4–7 | planning brief | required | required |
| Complex | multi-area product/tech task | 5–9 | 8–12 | specialist findings + consolidated plan | required | required |
| High-risk | auth, privacy, payments, AI tools, migrations, release, incident | 5–9 + targeted follow-up | 10–15 | risk-gated plan | required | required at each gate |
| Exception | 16+ roles or cross-program work | explicit user approval | explicit user approval | program plan | required | required |

## Anti-bureaucracy rules

- Do not ask every question in `QUESTION_TREE.md`; ask only questions that affect routing, risk, scope, or acceptance criteria.
- Do not activate a role whose output cannot change the next decision.
- Do not produce long artifacts for Tiny/Fast Lane tasks.
- Do not run research roles if the task has no research uncertainty.
- Do not run engineering specialists if the task is strategy-only.
- Do not run visual/design roles if there is no user-facing interface.
- Do not run risk specialists “just in case”; run them when a trigger in `RISK_POLICY.md` or `ROLE_ROUTING_MATRIX.md` is met.

## Optimal complexity heuristic

Use the lightest tier that can answer these questions confidently:

1. What are we trying to achieve?
2. What must not happen?
3. Who owns each important decision?
4. What evidence supports the plan?
5. How will we verify done?
6. What gate requires user approval?

If the answer is unclear, move up one tier. If the answer is clear and risk is low, move down one tier.
