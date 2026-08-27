# Official OpenAI plugin-directory submission

The Git marketplace is the canonical self-service distribution path for Product
OS. Listing Product OS in the shared ChatGPT and Codex plugin directory is a
separate OpenAI review process and is not implied by a GitHub release.

Official guidance:

- <https://developers.openai.com/codex/plugins/>
- <https://developers.openai.com/codex/build-plugins>
- <https://developers.openai.com/plugins/deploy/submission>

## Product OS submission boundary

Product OS 4.1 is a skills-first plugin bundle. Its public submission should
include at minimum:

- a verified individual or business publisher identity;
- public website, support, privacy-policy, and terms URLs;
- the final `cpt-core` and `cpt-design-ui` skill bundles;
- clear starter prompts for Product Designer workflows;
- five positive and three negative test cases with expected behavior;
- an accurate explanation that plugin installation does not create project
  `.cpt` state and that Product OS remains provider-neutral;
- no claim that OpenAI Product Design or Codex owns Product Designer decisions.

MCP-specific URLs, OAuth details, tool annotations, and demo credentials are
required only if a future submission adds an MCP server. They are not invented
for the current skills-only release.

## External owner actions

The repository can prepare the technical bundle and test cases, but final
submission requires account-bound actions that cannot be completed by a Git
merge:

1. verify the publisher identity in the OpenAI Platform;
2. provide and approve the public legal/support URLs;
3. submit through the OpenAI plugin publication flow;
4. respond to review feedback;
5. record the accepted public listing URL only after OpenAI approval.

Until those steps finish, user-facing documentation must describe Product OS as
a Git marketplace plugin, not as an officially listed OpenAI plugin.
