# FIRST_PROMPT.md — Codex Product Team 3.0 Ultra

Paste this into a fresh Codex thread when starting a project with this kit.

```text
Start from Codex Product Team 3.0 Ultra.

Load only these Tier 0 files first:
- AGENTS.md
- CURRENT.md
- TASK_INDEX.md
- CHRONICLE.md
- docs/BOOTSTRAP_INDEX.md
- docs/LANGUAGE_POLICY.md

Do not load all tickets, old logs, archives, diagnostics, generated files, external modules, all roles, all skills, or root legacy task memory by default.
TASK.md is only a deprecated compatibility pointer.

If a local ignored runtime overlay exists, such as AGENTS.override.md or .codex-runtime/*, treat it as current workspace runtime and still use staged loading.

Tiny/Micro obvious reversible work: no role/skill indexes by default. Do not load role/skill indexes by default for obvious Tiny/Micro work.
Fast Lane: use docs/SKILL_ROUTER_INDEX.json only if the route is unclear.
Standard+: use docs/SKILL_ROUTER_INDEX.json, docs/ROLE_TINY_INDEX.json, and docs/SKILL_TINY_INDEX.json before larger indexes.
Follow docs/SKILL_DISCOVERY_POLICY.md for critical workflows.

For UI/page review use UI Review Packet when review evidence matters. If real subagents fail or stall, use SUBAGENT_FAILURE_POLICY and report Subagent Completion Status.

For visual reference work: Reference Fidelity is required. Generated artifacts cannot validate themselves. Looks similar is not evidence.

Report:
1. Files loaded.
2. Active ticket or no active ticket.
3. Product knowledge files available.
4. Complexity tier.
5. Whether this is Tiny/Micro, Fast Lane, or Standard+.
6. Proposed next safe operation.
7. Whether approval is needed.

Do not edit files until I approve the next operation.
```

For a product/UI task, add:

```text
Task:
[describe task in natural language]

Use New Task Protocol:
- propose/create local ticket if needed;
- read PRODUCT_MAP and KNOWLEDGE_INDEX if present;
- select relevant area maps;
- propose bounded discovery;
- produce Impact Map;
- ask approval before implementation.
```
