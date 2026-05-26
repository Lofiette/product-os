# ROLE_SKILL_ARCHITECTURE.md

## Model

Role = accountability, expert judgment, owned artifact, boundaries, and handoff.
Skill = reusable workflow, method, checklist, script, or procedure.
Custom agent = technical spawnable role definition in `.codex/agents`.
Spawned subagent = real delegated Codex thread.

Do not replace roles with skills. A skill does not own a product decision. A role chooses or requests skills and owns the artifact quality.

## Skill loading rule

Load a skill only if it can change:
- scope;
- risk posture;
- acceptance criteria;
- implementation approach;
- verification;
- design-system compliance;
- handoff quality.

Default: 1–4 skills per operation. More than 4 skills requires explicit justification.

## Role playbooks

Every role must define:
- mission;
- activation triggers;
- non-responsibilities;
- owned artifacts;
- default skills;
- optional skills;
- handoffs;
- escalation triggers;
- strict output schema.
