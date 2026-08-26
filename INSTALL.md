# Installation

Product OS has two separate installation targets:

1. the **source repository**, which should live in Git;
2. the **project runtime**, installed into each working repository through `tools/cpt_dist.py`.

A Codex plugin marketplace is an optional delivery adapter on top of the source repository. It does not replace project runtime state.

## Requirements

- Python 3.10+
- Git, strongly recommended
- Runtime dependencies: `PyYAML` and `jsonschema`

```bash
python -m pip install -r requirements.txt
```

Windows:

```powershell
py -3 -m pip install -r requirements.txt
```

## Source repository

Keep one stable checkout rather than a folder per release:

```powershell
git clone <REPOSITORY_URL> "Product OS"
Set-Location "Product OS"
git fetch --tags
git switch --detach v4.1.0
py -3 -m pip install -r requirements.txt
```

See `docs/VERSIONING_AND_GIT.md`.

## Local ignored project mode

```bash
python tools/cpt_dist.py install \
  --project /path/to/repo \
  --mode local \
  --enforcement-mode audit
```

`--enforcement-mode` accepts `off`, `audit`, or `enforce`. Start with `off` or `audit`; enable `enforce` only after reviewing and trusting hooks.

Defaults:

- `.cpt/` is added to repository-local `.git/info/exclude`;
- `cpt-core` is copied to the personal Codex plugin directory;
- a personal marketplace entry is added;
- a missing `AGENTS.md` is created and ignored;
- a tracked existing `AGENTS.md` is not modified automatically.

If a tracked `AGENTS.md` already exists, the installer creates `.cpt/AGENTS_SNIPPET.md` and reports that automatic kernel guidance is inactive. Merge only after reviewing it.

## Team-shared project mode

```bash
python tools/cpt_dist.py install \
  --project /path/to/repo \
  --mode team \
  --enforcement-mode audit \
  --rules-profile conservative
```

Rules profiles are optional. Project-scoped hooks and rules require a trusted project, and plugin hooks require explicit hook review and trust.

Defaults:

- runtime files are shareable and not ignored;
- the managed kernel block is appended to an existing `AGENTS.md`;
- `cpt-core` is exposed through the personal marketplace by default;
- `--plugin-scope repo` vendors the plugin only when the team deliberately chooses that model;
- the installer never runs `git add`, creates a branch, or commits.

## Add domain packs

Product Designer and the UI knowledge plane live in `cpt-design-ui`:

```bash
python tools/cpt_dist.py pack-add \
  --name cpt-design-ui \
  --scope personal \
  --project /path/to/repo
```

Available bundled packs:

```bash
python tools/cpt_dist.py pack-catalog
```

## Windows helper

The release includes a convenience wrapper:

```powershell
.\scripts\product-os.ps1 \
  -Action install \
  -Project "C:\path\to\project" \
  -Mode local \
  -PluginScope personal \
  -EnforcementMode audit \
  -Packs cpt-design-ui
```

The Python CLI remains canonical; the PowerShell wrapper only assembles and verifies commands.

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

## No-plugin mode

```bash
python tools/cpt_dist.py install --project . --mode local --plugin-scope none
```

The repo kernel continues to work without plugins. This is the portable mode for agents that do not support Codex plugin packaging.

## Codex marketplace from this repository

Local development:

```bash
codex plugin marketplace add .
codex plugin add cpt-core@product-os
codex plugin add cpt-design-ui@product-os
```

Remote Git repository:

```bash
codex plugin marketplace add <GIT_URL_OR_OWNER/REPO>
codex plugin add cpt-core@product-os
codex plugin add cpt-design-ui@product-os
```

Windows helper:

```powershell
.\scripts\register-codex-marketplace.ps1 \
  -Source "owner/product-os" \
  -Plugins cpt-core,cpt-design-ui
```

Start a new Codex thread after installation.

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

## Evaluation Plane

The deterministic suite needs no Codex CLI or external service:

```bash
python tools/validate_evaluation.py
python tools/cpt_eval.py run --suite offline-core --backend reference --report-dir .cpt-eval-runs/offline
```

Live suites are optional. They require a Codex CLI session or trusted CI integration and must not be confused with the deterministic baseline. See `EVALUATION.md`.
