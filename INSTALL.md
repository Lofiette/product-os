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
  --mode local
```

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
  --mode team
```

Defaults:

- runtime files are shareable and not ignored;
- the managed kernel block is appended to an existing `AGENTS.md`;
- `cpt-core` is exposed through a repo marketplace;
- the complete repo-local footprint remains below 20 framework files.

The installer never runs `git add`, creates a branch, or commits.

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
