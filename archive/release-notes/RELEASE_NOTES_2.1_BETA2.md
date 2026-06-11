# Release Notes — Codex Product Team 2.1 beta 2

## Focus

Beta 2 hardens ticketed memory and context economy after the beta 1 deep audit.

## Changes

- Added YAML front matter to memory runtime skills: `context-prune`, `context-snapshot`, `task-ledger`, `ticket-router`, `memory-integrity-check`.
- Synchronized startup load policy across `AGENTS.md`, `FIRST_PROMPT.md`, `BOOTSTRAP_INDEX.md`, `CONTEXT_BUDGET_POLICY.md`, and `RUNTIME_LOAD_POLICY.md`.
- Cleaned stale bootstrap labels and ambiguous doc references.
- Made `ROLE_TINY_INDEX.json` and `SKILL_TINY_INDEX.json` more compact for routing.
- Strengthened validators for skill front matter, startup policy drift, stale runtime labels, bootstrap references, and scenario behavioral rules.

## Runtime rule

Start with Tier 0 files only. Load the active ticket and tiny indexes after intake. Do not load archives, closed tickets, all skills, all playbooks, release notes, or reference-only docs by default.
