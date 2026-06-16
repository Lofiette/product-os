# Codex Product Team 3.0 Ultra

A universal Codex runtime for building digital products with bounded context, product knowledge, expert roles, skills, playbooks, gates, and controlled subagent orchestration.

## What changed in 3.0

3.0 adds a real **Runtime Kernel** and **Product Knowledge System** on top of the 2.x role/skill framework.

2.x was mostly an expert framework. 3.0 is an expert framework inside an operating system:

- lightweight runtime startup;
- local/ignored runtime overlay support;
- ticketed task memory;
- compact `CHRONICLE` rescue summaries;
- Product Knowledge maps and evidence indexes;
- bounded discovery instead of broad repo reading;
- Impact Map before implementation;
- staged role/skill/gate loading;
- greenfield, existing-product, and redesign/migration modes;
- API/Data Shape contract prewarm;
- no hard line caps that cut useful knowledge.

## Quick start

1. Copy the kit into your project.
2. Start a new Codex thread.
3. Ask it to read `AGENTS.md`, `CURRENT.md`, `TASK_INDEX.md`, and `CHRONICLE.md` first.
4. For an existing product, run product onboarding from `product-knowledge/protocols/EXISTING_PRODUCT_ONBOARDING.md`.
5. For a new task, use the New Task Protocol: local ticket → product map → area map → bounded discovery → Impact Map → approval → implementation.

## Core principle

Codex should not know everything. Codex should know where to look, what evidence is current, and when to stop.

## Safety

No code edits, broad scans, real subagents, builds/tests/lints, or external module deep reads without approval unless explicitly allowed by the task and runtime policy.

## Role library

3.0 preserves the complete 2.x role library and adds `frontend_engineer` for implementation responsibility. Roles are loaded by task type and do not imply real subagents.


## 3.0 Ultra beta 2

This build hardens routing, critical skills, role metadata, and runtime coherence after control audit.
