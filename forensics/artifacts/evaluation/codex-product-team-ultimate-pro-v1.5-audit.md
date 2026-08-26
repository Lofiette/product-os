# Codex Product Team ULTIMATE Pro v1.5 — Build & Audit Report

## Verdict

PASS.

The v1.5 package applies the Runtime Hardening & Repo Recon Patch. It keeps the ULTIMATE team powerful while making startup, routing, review, and memory updates cheaper and less ceremonial.

## Validator result

```text
VALIDATION PASSED: 42 roles, 14 skills, 11 scenarios.
```

Zip integrity check passed.

## Package counts

- Roles: 42
- Role cards: 42
- Custom Codex agents: 42
- Skills: 14
- Scenario tests: 11

## Startup context budget

Stage 0 now loads only:

- `AGENTS.md`
- `TASK.md`
- `CHRONICLE.md`
- `docs/BOOTSTRAP_INDEX.md`
- `docs/QUESTION_TREE.md`
- `docs/LANGUAGE_POLICY.md`

Approximate Stage 0 size:

```text
21,967 characters
~5,492 rough tokens by chars/4
```

The full runtime decision tree, routing docs, role cards, skills, and full playbooks are loaded only after intake when they can change the next decision.

## Key v1.5 changes

### 1. Runtime decision kernel

Added `docs/RUNTIME_DECISION_TREE.md`.

It defines the operational loop:

1. classify request;
2. choose intake depth;
3. classify contributors;
4. build selected-role contract;
5. load context progressively;
6. plan and gate;
7. verify and review;
8. update chronicle compactly.

### 2. Active roles vs services vs role-card consults

Added `docs/ROLE_SERVICE_BUDGET.md`.

Contributor classes:

- Active specialist role: counts against role budget and owns an artifact.
- System service: does not count when compact.
- Consulted role card: does not count when no artifact is produced.

This fixes the Fast Lane problem where Chronicle Keeper, Code Reviewer, Intake, or Consistency Auditor could accidentally inflate role budget.

### 3. Review levels

Added `docs/REVIEW_LEVELS.md`.

- Review 0: Tiny self-check.
- Review 1: Fast Lane lightweight checklist.
- Review 2: active Code Reviewer role.
- Review 3: Code Reviewer plus triggered risk roles.

This preserves quality without forcing full review ceremony for one-line reversible changes.

### 4. Tiny/Fast implicit approval

Documented in `AGENTS.md`, `FAST_LANE.md`, `QUALITY_GATES.md`, and `RUNTIME_DECISION_TREE.md`.

Rule:

> If the user explicitly asked to implement, no risk gate is triggered, and the change is reversible, the user request counts as implementation approval.

### 5. Repo Recon

Added:

- `docs/REPO_RECON.md`
- `.agents/skills/repo-recon/SKILL.md`

Repo Recon prevents Codex from assuming stack, scripts, architecture, generated-file zones, or project conventions in existing repositories.

### 6. Chronicle compaction

Added `docs/CHRONICLE_POLICY.md`.

Chronicle now has two modes:

- compact chronicle service update;
- full Chronicle Keeper active role.

Tiny/Fast tasks no longer have to activate Aerith as a full role just because a file changed.

### 7. Opportunity event control

Updated `docs/OPPORTUNITY_EVENTS.md`.

Opportunity events now use classes:

- OE-0: no decision impact;
- OE-1: small improvement;
- OE-2: changes acceptance criteria;
- OE-3: changes risk/team/architecture;
- OE-4: blocker.

Added churn control:

- at most one creative loop per planning cycle unless user asks for ideation sprint;
- park useful but out-of-scope ideas;
- creative outputs remain hypotheses until validated.

### 8. Intake budgets

Updated `docs/QUESTION_TREE.md`.

- Micro Intake: 0–2 questions.
- Fast Lane Intake: 1–3 questions.
- Standard Intake: 3–7 questions.
- Complex/High-risk Intake: 5–9 + targeted follow-up.

### 9. Routing improvements

Updated `docs/ROLE_ROUTING_MATRIX.md`.

Added platform/surface routing:

- Web UI;
- Mobile app;
- API/service;
- Data product;
- Design-system component;
- AI summarization;
- AI tool-using agent;
- CLI/developer tooling;
- Existing repository change.

Clarified MVP rule:

- Small MVP: Product Strategist owns scope discipline.
- Delivery Manager required only for multi-phase/cross-area/deadline-heavy MVP.

### 10. Role index

Added `docs/ROLE_INDEX.json` for cheaper routing before loading full `TEAM.md` or full playbooks.

### 11. Scenario tests

Scenario tests increased to 11 and are synced from JSON to markdown.

New scenario:

- `existing_repo_feature_change`, requiring `repo-recon`.

## Remaining known boundary

v1.5 is structurally validated and process-hardened. It still cannot guarantee perfect task outcomes by structure alone. Real quality depends on:

- user-provided context;
- repository evidence;
- correct risk triggers;
- meaningful verification;
- human approval for risky changes.

## Recommended next use

Use v1.5 as the preferred working template. The next improvement cycle should be based on observing real Codex sessions, not adding more roles.
