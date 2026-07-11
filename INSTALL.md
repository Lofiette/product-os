# Installation

## Requirements

- Python 3.10+
- Git is recommended for local ignored mode
- Runtime dependencies: `PyYAML` and `jsonschema`

```bash
python -m pip install -r requirements.txt
```

## Local ignored mode

```bash
python tools/cpt_dist.py install \
  --project /path/to/repo \
  --mode local \
  --enforcement-mode off
```

`--enforcement-mode` accepts `off`, `audit`, or `enforce`. Start with `off` or `audit`; `enforce` should only be enabled after reviewing and trusting the hooks.

Defaults:

- `.cpt/` is added to the repository-local `.git/info/exclude`;
- `cpt-core` is copied to the personal Codex plugin directory;
- a personal marketplace entry is added;
- a missing `AGENTS.md` is created and ignored;
- a tracked existing `AGENTS.md` is not modified automatically.

If a tracked `AGENTS.md` already exists, the installer creates `.cpt/AGENTS_SNIPPET.md` and reports that automatic kernel guidance is inactive. Merge only after reviewing it.

## Team shared mode

```bash
python tools/cpt_dist.py install \
  --project /path/to/repo \
  --mode team \
  --enforcement-mode audit \
  --rules-profile conservative
```

Rules profiles are optional. Project-scoped hooks and rules require a trusted project, and plugin hooks require explicit hook review/trust.

Defaults:

- runtime files are shareable and not ignored;
- the managed kernel block is appended to an existing `AGENTS.md`;
- `cpt-core` is exposed through the personal marketplace by default; use `--plugin-scope repo` only when the team intentionally vendors the plugin;
- the default team-shared repo footprint is currently 11 framework files and remains below the 20-file target; an explicitly installed rules profile or repo-vendored plugin adds project-local files.

The installer never runs `git add`, creates a branch, or commits.

## Optional worker pack

Worker archetypes are installed separately and never appear implicitly:

```bash
python tools/cpt_dist.py workers-install --scope personal
```

Use repo scope only when a team intentionally vendors the ten custom-agent TOML files:

```bash
python tools/cpt_dist.py workers-install --scope repo --project /path/to/repo
```

Review `WORKER_PACK.md` and the recommended `[agents]` limits before use.

## Existing tracked AGENTS.md in local mode

Default behavior is safe skip. To explicitly merge the managed block:

```bash
python tools/cpt_dist.py install \
  --project /path/to/repo \
  --mode local \
  --agents-policy merge \
  --allow-tracked-agents-change
```

This intentionally creates a tracked change.

## No plugin mode

```bash
python tools/cpt_dist.py install --project . --mode local --plugin-scope none
```

The repo kernel continues to work without plugins. The plugin is a distribution and discoverability layer, not canonical state.
