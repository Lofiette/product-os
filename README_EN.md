# Product OS 4.1

[Русская версия](README.md) · [Release v4.1.0](https://github.com/Lofiette/product-os/releases/tag/v4.1.0)

Product OS is a model- and client-neutral operating environment for sustained product work with AI agents. It combines a file-based runtime, Product Knowledge, professional role lenses, skills, quality gates, deterministic enforcement, bounded worker orchestration, an Evaluation Plane, migration tooling, and release evidence.

The current stable version is **4.1.0**. The GitHub marketplace release is public; listing in an official OpenAI plugin directory is a separate review process.

## Product Designer 4.1

Version 4.1 adds Interaction Intelligence, form and long-process design, professional data interfaces, a provider-neutral Design Execution Plane, and optional compatibility with OpenAI Product Design when its capabilities are actually present.

OpenAI Product Design is an adapter, not a dependency. Product OS remains usable by agents without Codex plugin support.

See [docs/PRODUCT_DESIGNER_4.1.md](docs/PRODUCT_DESIGNER_4.1.md).

## Codex quick start

Product Designer needs two plugins: `cpt-core` and `cpt-design-ui`. Pin the marketplace to the immutable release tag, install both plugins, then start a new Codex task:

```bash
codex plugin marketplace add Lofiette/product-os --ref v4.1.0
codex plugin add cpt-core@product-os
codex plugin add cpt-design-ui@product-os
```

These commands add Product Designer capabilities to Codex. They do not create the per-project `.cpt` runtime.

## Repository versus project installation

These are different layers:

1. **Product OS repository**: canonical source, version history, tests, plugins, and releases.
2. **Codex plugins**: capability discovery and workflow guidance for the agent.
3. **Project installation**: an `AGENTS.md` kernel, `.cpt/` runtime state, and selected domain packs.

Plugins do not own the project's canonical runtime or Product Knowledge state. This keeps Product OS portable across agents and clients.

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

See [INSTALL.md](INSTALL.md) for complete installation options.

## Update

For a marketplace registered directly from Git:

```bash
codex plugin marketplace upgrade product-os
codex plugin add cpt-core@product-os
codex plugin add cpt-design-ui@product-os
```

Start a new Codex task after plugin installation or reinstall. A Manager-owned installation is pinned to an immutable commit root and must use a confirmed `plan-local-git -> prepare -> switch` transaction instead of manual retargeting.

Update a project runtime separately from the new Product OS source checkout:

```bash
python tools/cpt_dist.py status --project /path/to/project
python tools/cpt_dist.py update --project /path/to/project
python tools/cpt_dist.py doctor --project /path/to/project
```

## Release status and boundaries

Product OS 4.1.0 reached **RC_READY** with all 11 required release gates passing. Deterministic and migration suites ran across Windows, macOS, Linux, and ephemeral WSL. Isolated live Codex trials and independent release audits are recorded in the reviewed release evidence.

The boundaries remain explicit: native Codex plugin switching and cache behavior on macOS or WSL are not certified, and the live evidence does not generalize to every model or client. See [KNOWN_LIMITATIONS.md](KNOWN_LIMITATIONS.md).

## Documentation

- [README.md](README.md) — canonical Russian overview;
- [INSTALL.md](INSTALL.md) — installation guide in Russian;
- [docs/PRODUCT_DESIGNER_4.1.md](docs/PRODUCT_DESIGNER_4.1.md);
- [docs/PRODUCT_OS_MANAGER.md](docs/PRODUCT_OS_MANAGER.md);
- [docs/MIGRATION_4.0_TO_4.1.md](docs/MIGRATION_4.0_TO_4.1.md);
- [docs/PLUGIN_AND_MARKETPLACE.md](docs/PLUGIN_AND_MARKETPLACE.md);
- [UPDATE_AND_ROLLBACK.md](UPDATE_AND_ROLLBACK.md);
- [KNOWN_LIMITATIONS.md](KNOWN_LIMITATIONS.md).

## Verification

```bash
python tools/build_manifest.py
python tools/validate_distribution.py
python tools/validate_release.py
python tools/validate_evaluation.py
python scripts/validate_migration_assets.py
python tests/run_all.py
```
