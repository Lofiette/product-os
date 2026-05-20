# QUESTION_TREE.md — Adaptive Briefing Tree

Ask from broad to specific. Do not ask every question. Select branches based on the task. Keep the first question batch to 5–9 questions unless the task is high-risk or the user asks for exhaustive briefing.

## Level 0 — Always consider

1. What are we trying to achieve?
2. What type of work is this: research, prototype, PoC, MVP, production change, bugfix, refactor, review, audit, data/analytics, incident, or documentation?
3. Is this a new product, an existing product, or a change inside an existing repository?
4. What does “done” mean for this task?
5. Who is the target user, customer, operator, or reviewer?
6. What is explicitly out of scope?
7. Are there constraints around time, stack, design system, security, privacy, compliance, performance, or deployment?
8. What must not be changed?
9. What evidence already exists: user research, analytics, market data, designs, code, tickets, logs, docs?

## Research branch

Use if uncertainty exists around market, users, CX, domain, or product value.

### Market research

- What market/category are we exploring?
- Who are known competitors or substitutes?
- What positioning or adoption question are we trying to answer?
- Do we need external research, or only a framework/template for research?
- What regions, segments, pricing tiers, or channels matter?

### UX research

- What user behavior or usability question are we trying to answer?
- Do we need interviews, usability testing, surveys, diary study, heuristic review, or synthesis?
- Who should participate?
- What hypotheses should be tested?
- What decisions will the research inform?

### CX research

- What customer journey or service experience is involved?
- Which touchpoints matter before, during, and after product use?
- Where do support, sales, onboarding, billing, or retention enter the journey?
- What emotions, failures, expectations, and handoffs must be mapped?

## Product branch

- What is the user problem?
- What is the business or learning goal?
- What is the smallest valuable slice?
- What are non-goals?
- What trade-offs are acceptable?
- What success metrics or signals matter?
- What risks would make this not worth building?

## UI / UX branch

- What primary flow should the user complete?
- Which screens or surfaces are required?
- What empty, loading, error, disabled, success, and permission states are needed?
- Is there an existing design system in code or design files?
- What visual style should it follow?
- Does it need branding, logo, illustration, iconography, motion, or responsive behavior?
- What tone should UX copy use?
- What accessibility requirements are critical?

## Technical branch

- What platforms are targeted: web, backend, mobile, desktop, CLI, API, data pipeline?
- What stack exists or is preferred?
- What are the current architecture boundaries?
- What integrations are involved?
- What tests/checks exist?
- What performance, scale, offline, reliability, or compatibility constraints matter?

## Data / security / privacy branch

- What data is collected, stored, processed, exported, or deleted?
- Is any personal, sensitive, regulated, or customer-confidential data involved?
- Is authentication, authorization, tenant isolation, payment, billing, or file upload involved?
- Are retention, consent, deletion, audit, or compliance requirements relevant?
- What threat or abuse scenarios should be considered?

## Release / operations branch

- Is this going to production?
- Is a rollout or feature flag needed?
- What rollback path exists?
- What monitoring, logs, metrics, dashboards, or alerts are needed?
- What CI/CD or environment constraints apply?

## Bugfix branch

- What is expected behavior?
- What is actual behavior?
- How can we reproduce it?
- What changed recently?
- What logs, screenshots, stack traces, or failing tests exist?
- What is the blast radius?

## Refactor branch

- What pain is the refactor solving?
- What behavior must remain unchanged?
- What tests protect current behavior?
- Can the refactor be staged?
- What should not be refactored?

## Review branch

- What artifact should be reviewed: branch, diff, design, spec, architecture, copy, research plan, release plan?
- What review dimensions matter?
- Should findings be blocking/non-blocking or severity-ranked?
- Should the reviewer suggest fixes or only report issues?

## Documentation branch

- Who is the audience?
- What should the reader be able to do after reading?
- What source of truth should be used?
- Should this be README, PR description, changelog, runbook, decision record, or handoff summary?
