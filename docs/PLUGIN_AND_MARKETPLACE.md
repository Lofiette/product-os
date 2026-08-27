# Plugin and marketplace model

## Architectural boundary

Product OS separates three concerns:

```text
Git repository
  canonical roles, skills, gates, adapters, tests, releases
        |
        +--> Codex marketplace and plugins
        |      discovery, workflow instructions, optional tools
        |
        +--> project bootstrap
               AGENTS.md + .cpt runtime and Product Knowledge state
```

A plugin is a delivery adapter. It does not own the project's canonical `.cpt/` state. This keeps Product OS usable by agents that do not support Codex plugins and prevents plugin cache updates from silently mutating project memory.

## Repository marketplace

The repository root contains:

```text
.agents/plugins/marketplace.json
```

It exposes six plugins:

- `cpt-core`;
- `cpt-product-research`;
- `cpt-design-ui`;
- `cpt-engineering`;
- `cpt-risk-operations`;
- `cpt-ai-agentic`.

Each plugin has its own `.codex-plugin/plugin.json` and semantic version.

## Remote Git marketplace

After the repository is pushed to GitHub or another Git server:

```bash
codex plugin marketplace add <HTTPS_OR_SSH_GIT_URL_OR_OWNER/REPO> --ref v4.1.0
codex plugin add cpt-core@product-os
codex plugin add cpt-design-ui@product-os
codex plugin list
```

Release helpers use `Lofiette/product-os@v4.1.0` by default:

```powershell
.\scripts\register-codex-marketplace.ps1
```

```bash
./scripts/register-codex-marketplace.sh
```

To refresh a Git-backed marketplace:

```bash
codex plugin marketplace upgrade product-os
codex plugin add cpt-core@product-os
codex plugin add cpt-design-ui@product-os
```

Start a new Codex thread after installation or reinstall so new skills and tool declarations are loaded at a clean session boundary.

The helpers fail closed when `product-os` already exists. Direct Git-backed
marketplaces may use the explicit upgrade option. A Manager-owned root under
`~/.product-os/sources/` must use the transactional Manager update path so the
receipt, rollback source, and plugin selectors remain consistent.

## Local marketplace for development

From the repository root:

```bash
codex plugin marketplace add .
codex plugin add cpt-core@product-os
codex plugin add cpt-design-ui@product-os
```

Local mode is useful while editing skills before pushing a release. Remote Git mode is better for stable cross-device installation and team rollout.

## Project bootstrap still matters

Installing plugins alone does not create:

- `.cpt/install.json`;
- task, checkpoint, lease, orchestration, or enforcement state;
- project Product Knowledge;
- the managed `AGENTS.md` kernel block;
- project-specific trust and rules configuration.

Use the installer for projects that need the complete Product OS runtime:

```bash
python tools/cpt_dist.py install --project /path/to/project --mode local --enforcement-mode audit
```

Use `--plugin-scope none` when another adapter supplies skills but the project still needs the runtime scaffold.

## Optional OpenAI Product Design integration

OpenAI Product Design is treated as a capability adapter. When detected, Product Designer may delegate bounded execution such as visual directions, source inspection, image-to-code, or visual QA. It never becomes a hard dependency and never self-certifies its output. Product OS gates remain authoritative.

## Agent-neutral rule

Canonical knowledge must not depend on:

- a Codex-only command;
- a proprietary plugin name;
- an assumed connector;
- an undocumented tool behavior.

Provider-specific adapters translate portable capabilities into available tools. When an adapter is absent, the role uses a generic fallback or reports insufficient evidence.
