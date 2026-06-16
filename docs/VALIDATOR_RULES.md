# VALIDATOR_RULES.md — 3.0 beta 2

Validators must check structural integrity and runtime-semantic coherence.

## Required checks

- all required runtime/kernel/product/framework files exist;
- all role cards, playbooks, and TOML agents exist for indexed roles;
- all indexed skills have `SKILL.md` with YAML front matter;
- scenario JSON and markdown files are synchronized;
- `TASK.md` remains a deprecated compatibility pointer;
- current runtime memory has exactly one intake placeholder or active ticket;
- no stale 2.x version labels outside `archive/`;
- mirrored protocol/template files do not drift silently;
- critical 3.0 skills are present and referenced by routing/scenarios;
- `frontend_engineer` is present and used by UI implementation routing;
- soft artifact-size policy says target ranges are guidance, not hard truncation caps.

## Runtime checks

- root startup remains lightweight;
- Tiny/Micro tasks do not load role/skill indexes by default;
- real subagents require approval;
- broad repository/external reads require approval;
- Impact Map exists before non-trivial implementation.
