# AGENT_NAMING_POLICY.md

## Purpose

Keep agent execution transparent. Agent names must be exact machine identifiers, not decorative aliases.

## Rules

- Use exact `role_id` / `.codex/agents/<role_id>.toml` `name` values in all orchestration output.
- Do not assign human names, fictional names, philosopher names, codenames, nicknames, or persona labels to agents.
- Do not append any UI-generated thread/display label to a role title.
- Correct format: `product_designer`, `design_engineer`, `design_system_guardian`.
- If the Codex UI/platform auto-labels internal threads, map them back to role IDs in summaries and do not reuse the labels as agent identity.
- Role title may be shown for readability, but role ID remains the source of truth.

## Required orchestration wording

```markdown
Now spawning real subagents:
- `product_designer` — artifact: Screen Design Spec
- `design_engineer` — artifact: UI Implementation Fidelity Report
```

## Forbidden orchestration wording

```markdown
Now spawning real subagents:
- Product Designer <personal-display-label>
- Design Engineer <personal-display-label>
```
