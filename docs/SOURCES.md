# Sources

Current OpenAI guidance used for Alpha 3:

- https://developers.openai.com/codex/skills
- https://developers.openai.com/codex/plugins/build

Platform assumptions used by the package:

- Skills use progressive disclosure: initial discovery sees name, description, and path; full instructions load after selection.
- Initial skill metadata is bounded, so active-pack selection and concise descriptions matter.
- Skill descriptions influence implicit activation.
- `agents/openai.yaml` may expose interface metadata and set `policy.allow_implicit_invocation`.
- Plugins are the reusable distribution boundary for skills and, in later phases, related hooks or MCP configuration.
- Marketplace exposure and plugin enablement are separate operations.

These assumptions should be revalidated against current official documentation before a release candidate.
