# QUESTION_TREE.md

Ask adaptively. Do not ask every question. Start with Intake A, then Intake B after user answers.

## Intake A: universal first batch, 5 to 9 questions

1. What are we trying to achieve, in one sentence?
2. What work mode is closest: research, strategy, prototype, PoC, MVP, production change, bugfix, refactor, audit, incident, AI/ML feature?
3. Who is the target user or audience?
4. What would count as done for this first iteration?
5. Is this a new project or an existing repository/product?
6. What must not be changed or touched?
7. Are there any security, privacy, compliance, data, payment, auth, migration, or release risks?
8. Are there design-system, visual style, UX writing, accessibility, or brand constraints?
9. Do you want fast lane or full team planning?

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
- What errors are unacceptable?
- How will success be evaluated?
- What guardrails or human review are required?

## Branch: incident/bug
- What is observed?
- Expected vs actual behavior?
- Reproduction steps?
- Impact and severity?
- Recent changes?
- Logs or screenshots?

## Intake B outputs
- Updated `TASK.md`.
- Updated `CHRONICLE.md`.
- Work mode and team-size tier.
- Selected roles with rationale.
- Skipped roles with rationale.
- Open questions and assumptions.


## Language policy branch

Ask only when language affects the task or durable artifacts are being created.

1. What language should I use when speaking with you? Default: Russian.
2. What language should durable project artifacts use? Default: compact English for token efficiency.
3. What language is the product UI/copy for end users?
4. Does the task require localization, bilingual UX, locale-specific formats, or cultural adaptation?
5. Should PR/release documentation follow repository language or user language?
