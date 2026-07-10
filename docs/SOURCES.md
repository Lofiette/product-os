# Sources and Platform Assumptions

Official guidance used by the 4.0 Alpha series:

- https://developers.openai.com/codex/skills
- https://developers.openai.com/codex/plugins/build
- https://developers.openai.com/codex/hooks
- https://developers.openai.com/codex/config-reference
- https://json-schema.org/draft/2020-12

Platform assumptions:

- Skills use progressive disclosure; concise metadata and task-specific pack activation matter.
- `agents/openai.yaml` controls interface metadata and implicit invocation policy.
- Plugins are the reusable boundary for skills and later hooks/MCP configuration.
- Project hooks require separate trust and are deliberately deferred from Alpha 5.
- JSON Schema Draft 2020-12 is the machine-validation contract for Product Knowledge artifacts.

These assumptions must be revalidated against current official documentation before a release candidate.
