# Distribution Modes

## Separation of concerns

CPT OS 4.0 distribution has three independent layers:

1. **Repo scaffold** — tiny `AGENTS.md`, `.cpt/` state, runtime CLI, schemas.
2. **Core plugin** — one focused runtime skill, install-surface metadata.
3. **Domain packs** — optional plugins that can be exposed and enabled independently.

## Local ignored mode

Use for personal environments and experimentation.

- `.cpt/` is hidden through `.git/info/exclude` when Git is available.
- Core plugin is normally personal.
- Project source and tracked configuration remain untouched by default.
- An existing tracked `AGENTS.md` requires explicit permission to modify.

## Team shared mode

Use when runtime state and kernel guidance should be visible to the team.

- `.cpt/` is not ignored.
- Kernel guidance is merged as a marked block.
- Repo plugin exposure is available.
- Git staging and commits remain manual human actions.

## Plugin scopes

- `personal`: plugin source under `$CODEX_HOME/plugins/`; personal marketplace.
- `repo`: plugin source under `plugins/`; repo marketplace.
- `none`: scaffold only.

Exposing a plugin is not the same as enabling it. Codex users can install, enable, or disable plugins independently through supported plugin surfaces.

## Domain packs

Domain packs use the same native plugin boundary. Core has no dependency on any domain pack. A domain pack may declare a CPT compatibility range in `cpt-pack.json`, but canonical runtime state remains in the project scaffold.
