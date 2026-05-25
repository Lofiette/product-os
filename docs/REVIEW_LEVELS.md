# REVIEW_LEVELS.md — Right-Sized Review

Review is mandatory in spirit, not always as a full Code Reviewer role. Choose the lightest review level that protects correctness, scope, and risk.

| Level | Use when | Who performs it | Required artifact |
|---|---|---|---|
| Review 0: Self-check | Tiny reversible changes, no risk gates | Implementing agent | 3-line summary: changed file, check performed, risk none/low |
| Review 1: Lightweight checklist | Fast Lane file changes or small fixes | Relevant role or compact Code Reviewer service | Checklist: scope, obvious regression, minimal verification |
| Review 2: Code Reviewer role | Standard production change, bugfix, refactor, meaningful diff | Agrias / Code Reviewer | Review verdict with blockers/non-blockers/tests |
| Review 3: Multi-role review | High-risk, AI, auth, privacy, migrations, public API, release | Code Reviewer + triggered risk roles + Consistency Auditor | Risk-gated review report |

## Read-only rule

Review/audit mode is read-only by default. A reviewer may recommend changes, but must not edit files until the user explicitly switches to implementation or the task was already approved for implementation.

## Minimum checks

- Scope check: does the diff match approved or explicit user scope?
- Verification check: what command/manual check was run or why not?
- Risk check: did any gate trigger?
- Chronicle check: was a compact update needed?

## Tiny/Fast exception

A full Code Reviewer role is not required for Tiny/Fast Lane when Review 0 or Review 1 is sufficient. This preserves quality without wasting role budget.
