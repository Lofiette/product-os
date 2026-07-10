# Official Sources

Checked: 2026-07-10.

- Plugin structure, marketplaces, installation, path rules, hooks: https://developers.openai.com/codex/plugins/build
- Skills distribution and `agents/openai.yaml`: https://developers.openai.com/codex/skills
- Project-scoped configuration and trust: https://developers.openai.com/codex/config-reference
- AGENTS.md loading: https://developers.openai.com/codex/guides/agents-md

Design consequences:

- reusable distribution uses plugins;
- repo and personal marketplaces are both supported;
- plugin enable/disable remains native Codex behavior;
- skill metadata is kept small;
- no plugin owns canonical runtime state;
- hooks remain unbundled until the enforcement phase.
