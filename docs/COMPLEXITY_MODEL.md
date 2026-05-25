# COMPLEXITY_MODEL.md — Minimum Sufficient Ceremony

The goal is not to maximize process. The goal is to apply the smallest amount of specialist thinking that prevents expensive mistakes.

## Complexity tiers

| Tier | Use when | Question budget | Active role budget | Planning depth | Chronicle | Approval | Review |
|---|---|---:|---:|---|---|---|---|
| Tiny | typo, copy tweak, trivial reversible file change | 0–2 | 0–2 | inline | optional service | explicit user request may be enough | Review 0 |
| Fast Lane | small low-risk bounded task | 1–3 | 1–3 | short plan | compact service if files/decisions change | explicit user request may be enough if reversible | Review 0–1 |
| Standard | normal feature/fix/review | 3–7 | 4–7 | planning brief | compact or active depending on duration | required | Review 1–2 |
| Complex | multi-area product/tech task | 5–9 | 8–12 | specialist findings + consolidated plan | active or compact depending on duration | required | Review 2–3 |
| High-risk | auth, privacy, payments, AI tools, migrations, release, incident | 5–9 + targeted follow-up | 10–15 | risk-gated plan | active | required at each gate | Review 3 |
| Exception | 16+ active roles or cross-program work | explicit user approval | explicit user approval | program plan | active | required | Review 3 |

System services and consulted role cards do not count against the active role budget. See `docs/ROLE_SERVICE_BUDGET.md`.

## Anti-bureaucracy rules

- Do not ask every question in `QUESTION_TREE.md`; ask only questions that affect routing, risk, scope, or acceptance criteria.
- Do not activate a role whose output cannot change the next decision.
- Do not produce long artifacts for Tiny/Fast Lane tasks.
- Do not run research roles if the task has no research uncertainty.
- Do not run engineering specialists if the task is strategy-only.
- Do not run visual/design roles if there is no user-facing interface.
- Do not run risk specialists “just in case”; run them when a trigger in `RISK_POLICY.md` or `ROLE_ROUTING_MATRIX.md` is met.
- Do not run creative methods unless they can improve a decision, reduce risk, or produce better candidates for a known problem.

## Optimal complexity heuristic

Use the lightest tier that can answer these questions confidently:

1. What are we trying to achieve?
2. What must not happen?
3. Who owns each important decision?
4. What evidence supports the plan?
5. How will we verify done?
6. What gate requires user approval?

If the answer is unclear, move up one tier. If the answer is clear and risk is low, move down one tier.

## Context-budget heuristics

- Start with bootstrap docs, then load routing docs, then role cards, then full playbooks only for selected roles.
- Loading a large document is justified only when it can change the next decision or required artifact.
- Prefer compact artifacts over long explanations.
- Use creative methods as a focused improvement loop, not as additional bureaucracy.
- For existing repositories, run Repo Recon before loading large source files.

## Output-length budgets

| Tier | Default output style |
|---|---|
| Tiny | 3–8 bullets or compact patch summary |
| Fast Lane | short plan + verification summary |
| Standard | concise planning brief + role contract |
| Complex | specialist findings summarized by decision |
| High-risk | risk tables, gates, and required evidence only; no essays |
