# CONTEXT_BUDGET_POLICY.md — Context Economy

Context quality beats context volume. Load the smallest packet that can change the next decision.

## Canonical loading tiers

### Tier 0 — startup, always load

- `AGENTS.md`
- `CURRENT.md`
- `TASK_INDEX.md`
- `CHRONICLE.md`
- `docs/BOOTSTRAP_INDEX.md`
- `docs/LANGUAGE_POLICY.md`


### Tiny/Micro exception

For obvious reversible `Tiny/Micro` work, do not load role/skill indexes by default. Use Tier 0, the active ticket or a compact inline note, and the smallest relevant self-check. Load indexes only when the route is ambiguous or a gate may be triggered.

### Tier 1 — intake / active operation

Load only when the current decision needs it:

- active ticket from `CURRENT.md`;
- `docs/QUESTION_TREE.md`, only for structured intake;
- `docs/SKILL_ROUTER_INDEX.json`, for ambiguous domain routing before heavier indexes;
- `docs/ROLE_TINY_INDEX.json`, for `Standard+` routing or ambiguous Fast Lane only;
- `docs/SKILL_TINY_INDEX.json`, for `Standard+` routing or ambiguous Fast Lane only;
- relevant role cards.

### Tier 2 — selected workflow

Load only selected docs/skills/gates:

- selected `SKILL.md` files;
- relevant quality/risk/design gates;
- relevant evidence packet under `context/packets/`;
- selected full playbooks only when role-card guidance is insufficient.

### Tier 3 — reference-only / build-time

Do not load by default:

- all tickets;
- closed tickets;
- detailed chronicle logs;
- archive;
- old snapshots;
- release notes;
- self-audit reports;
- full role method libraries;
- all playbooks or all skills.

## Large load rule

If Codex wants to load an archive, all tickets, full playbooks, full method libraries, or many docs, it must state:

1. what decision the load can change;
2. why a smaller packet is insufficient;
3. what will be loaded;
4. when the information will be summarized, unloaded, or archived.

## Context budget log

Record large loads in the active ticket context budget log.

## Compression response

If context compression happens frequently, propose `context-snapshot` and `context-prune` before continuing.
