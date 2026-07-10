
# Codex Product Operating System 4.0 Alpha 6

Alpha 6 adds optional deterministic runtime enforcement to the self-contained file-only Runtime Kernel, Product Knowledge, canonical skills, and logical role lenses.

## Install

```bash
python tools/cpt_dist.py install --project /path/to/repo --mode local --enforcement-mode audit
```

Enable CPT Core, restart Codex, review and trust the bundled plugin hooks, then observe audit mode before considering enforcement mode.

```bash
python .cpt/bin/cpt_runtime.py enforcement-status
python .cpt/bin/cpt_runtime.py enforcement-set --mode enforce --trust-state trusted
```

CPT hooks are guardrails, not replacements for native Codex sandboxing, permission profiles, approvals, rules, project trust, or enterprise requirements.

See `ENFORCEMENT.md`, `KNOWLEDGE.md`, `ROLES.md`, `SKILLS.md`, and `INSTALL.md`.
