# Plugin And Marketplace Model

`cpt-core` is a native Codex plugin with a required `.codex-plugin/plugin.json` and one focused runtime skill.

Plugin source can be exposed through:

- personal marketplace: `~/.agents/plugins/marketplace.json` + `~/.codex/plugins/cpt-core`;
- repo marketplace: `.agents/plugins/marketplace.json` + `plugins/cpt-core`.

Marketplace exposure makes a plugin discoverable. Installation and enabled state remain user-controlled in Codex.

The plugin does not own `.cpt/` canonical state. It provides runtime instructions and discoverability only.
