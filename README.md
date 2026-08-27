# Product OS 4.1

Product OS is a model- and client-neutral operating system for product work. It combines a file-based runtime, Product Knowledge, professional role lenses, skills, quality gates, deterministic enforcement, bounded worker orchestration, an Evaluation Plane, migration tooling, and release evidence.

## Product Designer 4.1

Version 4.1 adds:

- Interaction Intelligence and contextual pattern selection;
- form and long-process design;
- professional data and expert-workflow interfaces;
- a provider-neutral Design Execution Plane;
- optional compatibility with OpenAI Product Design when its capabilities are actually present.

OpenAI Product Design is an adapter, not a dependency. Product OS remains usable by agents without Codex plugin support.

See `docs/PRODUCT_DESIGNER_4.1.md`.

## Repository versus project installation

These are different layers:

1. **Product OS repository**: canonical source, version history, tests, plugins, and releases.
2. **Project installation**: a small `AGENTS.md` and `.cpt/` runtime scaffold plus selected plugin packs.

Plugins provide discovery and workflow capabilities. They do not own the project's canonical runtime or Product Knowledge state.

## Install into a project

```bash
python -m pip install -r requirements.txt
python tools/cpt_dist.py install \
  --project /path/to/project \
  --mode local \
  --enforcement-mode audit
python tools/cpt_dist.py pack-add \
  --name cpt-design-ui \
  --scope personal \
  --project /path/to/project
```

## Update a project

Run from the **new Product OS source checkout**:

```bash
python tools/cpt_dist.py status --project /path/to/project
python tools/cpt_dist.py update --project /path/to/project
python tools/cpt_dist.py doctor --project /path/to/project
```

Product OS 4.1 preserves mutable runtime state and refreshes the core plus every bundled pack recorded in `.cpt/install.json`.

## Codex Git marketplace

The repository contains `.agents/plugins/marketplace.json` with all six plugins:

```bash
codex plugin marketplace add <GIT_URL_OR_OWNER/REPO>
codex plugin add cpt-core@product-os
codex plugin add cpt-design-ui@product-os
```

Update:

```bash
codex plugin marketplace upgrade product-os
```

This command is for a marketplace that Codex registered directly from Git. A
Product OS Manager installation is pinned to an immutable local commit root;
publishing to GitHub does not silently update it. Use a new Manager
`plan-local-git` -> `prepare` -> `switch` transaction for that case.

Start a new thread after plugin installation or reinstall. Update project `.cpt/` state separately with `cpt_dist.py update` for a legacy local-distribution installation.

For a transactional 4.0 local-installation to Git-marketplace adoption, use
`tools/product_os_manager.py plan-local-git`, then separately confirm `prepare`
and `switch`. Trusted commands require explicit project, user, Codex, and
Product OS roots; source-dependent phases additionally require a repository
root. They reject the process-active `CODEX_HOME` by default. See
`docs/PRODUCT_OS_MANAGER.md`; real Codex switching remains separately evidenced
from the deterministic offline certification.

## Verification

```bash
python tools/build_manifest.py
python tools/validate_distribution.py
python tools/validate_release.py
python tools/validate_evaluation.py
python scripts/validate_migration_assets.py
python tests/run_all.py
```

## Documentation

- `INSTALL.md`
- `UPDATE_AND_ROLLBACK.md`
- `docs/MIGRATION_4.0_TO_4.1.md`
- `docs/VERSIONING_AND_GIT.md`
- `docs/PLUGIN_AND_MARKETPLACE.md`
- `docs/PRODUCT_DESIGNER_4.1.md`
- `docs/PRODUCT_OS_MANAGER.md`
- `KNOWN_LIMITATIONS.md`
