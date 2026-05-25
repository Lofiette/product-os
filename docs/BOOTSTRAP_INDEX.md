# BOOTSTRAP_INDEX.md — Lean Startup Map

Read this at startup to avoid loading the whole kit.

## Start here

1. Read `AGENTS.md`, `TASK.md`, `CHRONICLE.md`, `docs/QUESTION_TREE.md`, and `docs/LANGUAGE_POLICY.md`.
2. Classify likely work mode and complexity lightly.
3. Ask only decision-impact questions.
4. After user answers, load `docs/RUNTIME_DECISION_TREE.md`, routing docs, and role cards.
5. Load full playbooks only for active selected roles.

## Complexity quick map

- Tiny: obvious reversible tweak, 0–2 questions, 0–2 active roles, Review 0.
- Fast Lane: small low-risk task, 1–3 questions, 1–3 active roles, Review 0/1.
- Standard: normal feature/fix/review, 3–7 questions, 4–7 active roles, Review 1/2.
- Complex: multi-area task, 5–9 questions, 8–12 active roles, Review 2/3.
- High-risk: AI tools, auth, privacy, payments, migrations, public API, release, incident, 10–15 active roles, Review 3.

System services and consulted role cards do not count as active roles unless they produce full artifacts.

## Hard stops

Ask before public API, DB/schema migration, auth/security/privacy/payment, new production dependency, infra/deploy/CI, deletion, large refactor, irreversible AI/tool actions, or approved-scope changes.

## Existing repo

If implementation/review may touch an existing repo, run the `repo-recon` skill before deep planning or edits.

## Language

Reply to the user in Russian by default. Keep durable artifacts in compact English. Product UI copy uses product language.

## Creativity

Use creative methods only when they can improve a specific decision. One creative loop per planning cycle unless the user asks for an ideation sprint.
