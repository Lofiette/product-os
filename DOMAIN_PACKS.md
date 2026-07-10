# Domain Packs

Alpha 2 defines the packaging boundary but does not migrate the 3.0 expertise library yet.

A CPT domain pack is a native Codex plugin plus `cpt-pack.json`.

```text
my-domain-pack/
  .codex-plugin/plugin.json
  cpt-pack.json
  skills/
```

Validate and expose a pack:

```bash
python tools/cpt_dist.py pack-add \
  --path /path/to/pack \
  --scope personal
```

Or repo scope:

```bash
python tools/cpt_dist.py pack-add \
  --path /path/to/pack \
  --scope repo \
  --project /path/to/repo
```

Remove one pack without affecting core or other packs:

```bash
python tools/cpt_dist.py pack-remove --name cpt-example --scope personal
```

The Codex plugin UI remains the authority for enabling and disabling exposed plugins.
