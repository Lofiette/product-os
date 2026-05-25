# VALIDATOR_RULES.md

The structural validator is intentionally conservative. It must catch packaging mistakes that would make Codex routing unreliable.

## Required checks

- Required root and docs files exist.
- No `.bak`, `.tmp`, or editor backup files are shipped.
- Every playbook has a matching custom agent TOML.
- Every playbook contains required operational sections.
- Every TOML has `name`, `description`, and `developer_instructions`.
- `FIRST_PROMPT.md` lists core docs as separate bullets, not comma-packed pseudo-paths.
- `AGENTS.md` references language, evidence, complexity, role schemas, external evidence, codename policy, and role method library.
- `SCENARIO_TESTS.json` is valid and references only known role IDs.
- Markdown scenario tests are generated from JSON and have matching IDs.
- No role escalates to itself.
- Review/audit mode is read-only by default.

## Validator boundaries

The validator does not prove professional quality of every role. It only prevents structural decay. Content audits should still review role methodology, routing quality, and scenario realism.


## v1.4 Pro checks

- `FIRST_PROMPT.md` Stage 0 must not load heavy assets: `TEAM.md`, `ROLE_METHOD_LIBRARY.md`, `ROLE_OUTPUT_SCHEMAS.md`, or `SCENARIO_TESTS.json`.
- Every role must have a role card in `.agents/role_cards/`.
- `TEAM.md`, playbook headers, playbook codename lines, and TOML descriptions must agree on codename and title.
- Creative/opportunity docs and skill must exist and be referenced.
- `SCENARIO_TESTS.json` remains a validation asset, not normal startup runtime context.
