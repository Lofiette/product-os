# SUBAGENT_PROMPT_RECIPES.md

## Planning spawn recipe

Use true subagent workflow.
Spawn these custom agents by exact name:
- `<agent_name>`

Each agent must:
- read TASK.md and only relevant docs/files;
- stay inside its role boundary;
- use only approved skills;
- return the required artifact schema;
- not modify files unless explicitly given write permission;
- label evidence, assumptions, and blockers.

Wait for all agents. Then consolidate.

## UI redesign recipe

Spawn:
- product_designer for Screen Design Spec;
- design_system_guardian for DS constraints;
- ux_writer for Content Matrix, if copy/states matter;
- design_engineer after implementation for UI Fidelity Report.

Do not implement before design-recon and screen spec approval unless user explicitly asks for throwaway exploration.
