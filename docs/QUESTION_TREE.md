# QUESTION_TREE.md

Ask adaptively. Do not ask every question. Start with Intake A, then Intake B after the user answers.

## Decision-impact question rule

Ask a question only if the answer can change scope, risk, role lineup, acceptance criteria, verification, approval gates, product language, repo recon need, creative/opportunity handling, or implementation sequence.

## Intake depth budgets

| Intake depth | Use when | Question budget |
|---|---|---:|
| Micro Intake | Tiny, obvious, reversible, low-risk | 0–2 |
| Fast Lane Intake | Small, low-risk, bounded | 1–3 |
| Standard Intake | Normal feature/fix/review | 3–7 |
| Complex/High-risk Intake | Multi-area, risky, ambiguous, AI/auth/privacy/migration/release | 5–9 + targeted follow-up |

## Micro / Fast Lane question pool

Use only what changes the next action:

1. Which file/screen/component should change, if not obvious?
2. Is this implementation or review-only?
3. What verification should be enough for this small change?
4. Is there any hidden risk: auth, privacy, data, API, migration, dependency, release?

## Standard / Complex first batch

1. What are we trying to achieve, in one sentence?
2. What work mode is closest: research, strategy, prototype, PoC, MVP, production change, bugfix, refactor, audit, incident, AI/ML feature, opportunity event?
3. Who is the target user or audience?
4. What would count as done for this first iteration?
5. Is this a new project or an existing repository/product?
6. What must not be changed or touched?
7. Are there any security, privacy, compliance, data, payment, auth, migration, dependency, AI autonomy, or release risks?
8. Are there design-system, visual style, UX writing, accessibility, localization, or brand constraints?
9. Do you want fast lane, standard planning, or full team planning?

## Branch: existing repository / repo recon

- What repository area, feature, or files are likely involved?
- What commands should be used for test/lint/typecheck/build if known?
- Are there generated files, forbidden areas, or local project conventions?
- Should the task preserve public API, design system contracts, or data schemas?

## Branch: research/discovery

- What decisions should this research support?
- What evidence already exists?
- Are we researching market, users, CX, competitors, pricing, usability, or demand?
- What sources are allowed?
- What confidence level is needed?

## Branch: UX/UI/product design

- What are the primary flows?
- What states matter: empty, loading, error, success, disabled, partial data?
- Is there a design system in code or design files?
- What tone should the product copy use?
- Any accessibility requirements or regulated audiences?

## Branch: engineering

- What platform and stack?
- What architecture exists?
- What tests/checks exist?
- What data/storage/API constraints exist?
- What deployment target exists?

## Branch: AI/ML

- What model-enabled behavior is required?
- What data can the model access?
- What actions or tools can the AI use?
- What errors are unacceptable?
- How will success be evaluated?
- What guardrails, fallbacks, or human review are required?

## Branch: incident/bug

- What is observed?
- Expected vs actual behavior?
- Reproduction steps?
- Impact and severity?
- Recent changes?
- Logs or screenshots?

## Branch: opportunity event / improvement idea

- What is the new idea, signal, or event?
- Who or what is the source: stakeholder, user, support, analytics, market, repo, incident, or design critique?
- What decision could this change: scope, UX, copy, architecture, risk, delivery, or verification?
- Is there evidence, or is it an assumption/hypothesis?
- Should we ignore, defer, clarify, creatively explore, re-route, re-plan, or block?
- What constraint must the idea respect?

## Language policy branch

Ask only when language affects the task or durable artifacts are being created.

1. What language should I use when speaking with you? Default: Russian.
2. What language should durable project artifacts use? Default: compact English for token efficiency.
3. What language is the product UI/copy for end users?
4. Does the task require localization, bilingual UX, locale-specific formats, or cultural adaptation?
5. Should PR/release documentation follow repository language or user language?

## Intake B outputs

- Updated `TASK.md` when useful.
- Updated `CHRONICLE.md` when appropriate.
- Work mode and team-size tier.
- Active roles with rationale.
- System services and consulted role cards.
- Skipped roles with rationale.
- Open questions and assumptions.
