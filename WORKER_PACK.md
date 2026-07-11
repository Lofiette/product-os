# Optional CPT Worker Pack

The worker pack installs ten custom Codex agents. It is optional and is not installed with the repo scaffold or core plugin by default.

## Install

Personal scope:

```bash
python tools/cpt_dist.py workers-install --scope personal
```

Repository scope:

```bash
python tools/cpt_dist.py workers-install --scope repo --project /path/to/repo
```

Inspect:

```bash
python tools/cpt_dist.py workers-status --scope personal
```

Remove:

```bash
python tools/cpt_dist.py workers-remove --scope personal
```

## Recommended Codex limits

The pack includes `payload/worker-pack/config/agents.example.toml`:

```toml
[agents]
max_threads = 4
max_depth = 1
job_max_runtime_seconds = 900
interrupt_message = true
```

Merge limits deliberately. CPT does not silently change the user's global Codex configuration.

## Security and permissions

Custom agents inherit the parent session's sandbox and approval policy. Their TOML profiles narrow expected behavior but do not create a stronger operating-system security boundary.

Read-heavy archetypes use `read-only`. `cpt_implementer` and `cpt_test_runner` use `workspace-write` and are expected to receive managed worktree contracts for parallel writes.

## Receipt safety

Installation writes a receipt containing only known worker TOML filenames and hashes. Removal validates that every path remains inside the expected agents directory and matches a known archetype. Modified files require explicit `--force`; unrelated custom agents are not removed.
