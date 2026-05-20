# Adaptive Question Tree for Task Intake

Use this tree to brief the user. Ask only relevant questions. Prefer batches of 5–9 questions. Do not exhaustively ask every question if the task is small.

## Intake principle

Start broad, then branch. Stop asking when there is enough information to choose work mode, roles, scope, acceptance criteria, and verification plan.

## Level 0 — Always ask if missing

1. What are we trying to achieve?
2. Is this a new product, a feature in an existing product, a bugfix, a refactor, a review, or research?
3. What outcome would make you say “done”?
4. Should this be a prototype, PoC, MVP, or production-ready change?
5. Are we working in an existing repository or starting from scratch?
6. Are there hard constraints: time, stack, design system, platform, dependencies, security, performance?
7. What should explicitly not be changed or touched?

## Level 1 — Work mode selection

### If Prototype

Ask:

- What should the prototype demonstrate?
- Who is the prototype for: you, stakeholders, users, investors, internal team?
- Should it be visually polished or functional enough for learning?
- What shortcuts are acceptable?
- What must not be faked?

### If PoC

Ask:

- What technical assumption are we proving?
- What would disprove feasibility?
- What can be mocked?
- What integration or platform constraint matters most?
- What measurable result proves success?

### If MVP

Ask:

- Who is the primary user?
- What is the smallest valuable end-to-end flow?
- What must be included in v1?
- What should be deferred?
- What is the release or demo target?

### If Production Change

Ask:

- What existing behavior must be preserved?
- What regression risks are unacceptable?
- Which tests/checks are required?
- Is there a rollout, feature flag, or rollback expectation?
- Are there compliance, privacy, or security constraints?

### If Bugfix

Ask:

- What is the observed behavior?
- What is the expected behavior?
- How can the issue be reproduced?
- When did it start?
- Is it user-facing, internal, intermittent, or environment-specific?
- Are logs, screenshots, stack traces, or failing tests available?

### If Refactor

Ask:

- What pain are we solving?
- What behavior must remain identical?
- What is the smallest safe refactor?
- Are there tests that protect current behavior?
- Should refactor and behavior change be separated?

### If Review

Ask:

- What should be reviewed: code, PR, architecture, UX, tests, security, performance?
- What standard should the review use?
- Should the output be blocking/non-blocking findings, checklist, or rewrite proposal?

### If Research

Ask:

- What decision should the research support?
- What sources or code areas should be considered authoritative?
- What format should the output take: summary, comparison, recommendation, plan?

## Level 2 — Product and users

Ask if product value or audience is relevant:

- Who is the target audience?
- What user problem are we solving?
- What are the primary and secondary user flows?
- What user context matters: device, environment, frequency, expertise, accessibility needs?
- What user emotions or perceptions should the experience create or avoid?
- What are the top failure states from the user's perspective?

## Level 3 — UX/UI branch

Ask if the task affects interface, interaction, flows, or content:

- Which screens, components, or flows are affected?
- Is there an existing design system?
- Is the design system in code, Figma, documentation, screenshots, or only in memory?
- What visual style should be used?
- Are there brand/logo requirements?
- Are there typography, color, spacing, iconography, or motion constraints?
- Which states are required: empty, loading, error, disabled, success, partial data?
- What accessibility level or constraints matter?
- Should copy be formal, friendly, neutral, playful, enterprise, or domain-specific?

## Level 4 — Technical branch

Ask if implementation is required:

- What platform is targeted: web, mobile, desktop, backend, CLI, embedded, data pipeline?
- What stack is used?
- What files, modules, services, packages, or folders are likely relevant?
- Are there existing patterns to reuse?
- Are new dependencies allowed?
- Are there environment variables, secrets, external services, or local setup requirements?
- What commands run build, tests, typecheck, lint, storybook, or local app?

## Level 5 — Backend/data branch

Ask if APIs, storage, auth, or integrations are involved:

- What data is created, read, updated, or deleted?
- Are there authorization rules or roles?
- Are there privacy or retention constraints?
- Are database migrations allowed?
- Are API contracts public or internal?
- Are integrations real, mocked, or unavailable locally?
- Is idempotency, pagination, caching, or consistency important?

## Level 6 — Quality branch

Ask before implementation plan:

- What tests already exist?
- What should be tested: unit, integration, e2e, visual, accessibility, contract, performance?
- What commands should Codex run?
- What manual verification is expected?
- What risks are acceptable for this work mode?
- What is the rollback or undo path?

## Level 7 — Team selection

After enough answers, select roles:

- Product Strategist: unclear value, scope, MVP, prioritization.
- UX Interaction Reviewer: flows, screens, copy, interaction states.
- Design System Guardian: UI components, visual system, tokens, reusable patterns.
- Frontend Architect: frontend implementation.
- Backend Architect: API, service, data, domain logic.
- QA Engineer: tests and verification.
- Code Reviewer: after diff or for PR/review tasks.

Always record selected and skipped roles in `TASK.md`.
