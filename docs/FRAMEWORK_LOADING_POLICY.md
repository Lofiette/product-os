# Framework Loading Policy

The runtime kernel must not disable the expert framework. It must stage-load it.

## Always

- Start with runtime kernel and active task.
- Use product knowledge to choose area.
- Use task type to choose roles/skills/gates.
- Load only relevant role cards, skills, playbooks, and gates.

## Never by default

- all roles;
- all skills;
- all playbooks;
- all docs;
- root legacy task memory.

## If framework paths are unknown

Ask for bounded framework-index discovery. Do not broad scan the repository.

## UI/product implementation minimum

Design-only routing is not enough for implementation.

Include frontend engineering accountability for code UI changes. Use design engineering for UI fidelity and frontend engineering for integration, state, routing, and maintainability.
