# RUNTIME_LOAD_POLICY.md — Runtime vs Reference Files

Not every file in the kit is runtime context. Use staged loading and prefer operation packets over full project memory.

## Tier 0 runtime docs

Load at startup:

- `AGENTS.md`
- `CURRENT.md`
- `TASK_INDEX.md`
- `CHRONICLE.md`
- `docs/BOOTSTRAP_INDEX.md`
- `docs/LANGUAGE_POLICY.md`

## Load by operation

Load only when relevant:

- active ticket from `CURRENT.md`;
- `docs/QUESTION_TREE.md` for structured intake;
- for `Tiny/Micro`, no role/skill indexes by default; for `Fast Lane`, tiny indexes only if routing is unclear; for `Standard+`, optional `docs/SKILL_ROUTER_INDEX.json` before tiny indexes; tiny indexes before mini/full indexes;
- relevant role cards;
- selected skill docs;
- selected gate docs;
- evidence packets under `context/packets/`.

## Reference-only docs

Do not load by default:

- `docs/ROLE_METHOD_LIBRARY.md`;
- `docs/ROLE_OUTPUT_SCHEMAS.md`;
- `TEAM.md`;
- release notes;
- self-audit reports;
- closed tickets;
- archive logs;
- old snapshots.

## Build-time docs

Do not load during normal work unless auditing the kit:

- `docs/SELF_AUDIT_REPORT.md`;
- `docs/VALIDATOR_RULES.md`;
- audit reports.

## Operation packet rule

Subagents should receive an operation packet, not the whole repo memory. A run contract should state exactly which ticket, packet, docs, and files they may inspect.


## Diagnostic docs

`docs/CODEX_DIAGNOSTIC_EXPORT_WSL.md` is reference-only. Load it only when the user asks to export Codex logs, debug repeated compaction, or analyze Codex session behavior.

`docs/SKILL_DISCOVERY_POLICY.md` is load-on-demand. Load it when critical skills are being missed, the skill route is unclear, or a previous run used a generic workflow instead of the required skill.
