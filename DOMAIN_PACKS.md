# Domain Packs

Alpha 9 ships five implemented, optional domain plugins. Core operates without them. Each pack now declares its primary logical roles in addition to canonical skills.

## Bundled catalog

```bash
python tools/cpt_dist.py pack-catalog
```

Bundled packs:

- `cpt-product-research`
- `cpt-design-ui`
- `cpt-engineering`
- `cpt-risk-operations`
- `cpt-ai-agentic`

## Install a bundled pack

Personal scope:

```bash
python tools/cpt_dist.py pack-add   --name cpt-design-ui   --scope personal
```

Repository scope:

```bash
python tools/cpt_dist.py pack-add   --name cpt-engineering   --scope repo   --project /path/to/repo
```

## Install a third-party pack

```bash
python tools/cpt_dist.py pack-add   --path /path/to/plugin   --scope personal
```

## Remove independently

```bash
python tools/cpt_dist.py pack-remove   --name cpt-design-ui   --scope personal
```

Removing one pack does not remove core or another pack. Plugin exposure is not the same as enablement; Codex plugin controls remain authoritative.

## Loading rule

Enable only packs relevant to the work. Typical profiles are measured in `tools/measure_all_skill_metadata.py`. Activating every optional pack simultaneously is supported as a diagnostic condition, not recommended as the default discovery surface.
