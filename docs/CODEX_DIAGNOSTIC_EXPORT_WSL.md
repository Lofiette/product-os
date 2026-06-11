# CODEX_DIAGNOSTIC_EXPORT_WSL.md

Use this guide when Codex behavior needs debugging from VS Code running under WSL.

## Goal

Create a small diagnostic pack that explains what Codex actually did:

- session transcript and history snippets;
- Codex config and runtime logs;
- current ticketed memory state;
- changed files and git diff;
- UI screenshots and reference images if available;
- active framework docs/skills that should have influenced the run.

## Privacy rules

Before sharing a diagnostic pack, remove or redact:

- `.env*`, credentials, tokens, cookies, private keys;
- `~/.codex/auth.json`;
- production/customer data;
- internal URLs that must not be shared;
- `node_modules`, builds, caches, coverage, large binaries.

Use placeholders such as `[REDACTED_TOKEN]`, `[REDACTED_CLIENT]`, `[REDACTED_INTERNAL_URL]`.

## Where Codex stores state in WSL

When Codex runs inside WSL, use the Linux home for that WSL distribution.

Default Codex home:

```bash
~/.codex
```

If `CODEX_HOME` is set, use that instead:

```bash
echo "$CODEX_HOME"
```

Typical files/directories:

```text
~/.codex/config.toml
~/.codex/history.jsonl
~/.codex/sessions/
~/.codex/archived_sessions/
```

## Quick export

From the repository root inside WSL:

```bash
bash scripts/export-codex-diagnostics-wsl.sh
```

The script creates:

```text
./codex-diagnostic-pack-YYYYMMDD-HHMMSS.zip
```

## What to include manually if the script misses it

- reference screenshots;
- actual screenshots;
- Playwright traces/videos;
- browser console output;
- Codex UI screenshots showing subagent status;
- any session transcript that the script did not find.

## What the auditor will inspect

- whether Codex loaded the intended runtime files;
- whether it used the active ticket, not `TASK.md`;
- whether skills were explicitly selected or only assumed;
- whether real subagents were spawned or roles were simulated;
- whether UI quality gates ran before PASS/WARN/BLOCKED;
- whether reference fidelity and DS authority were proven;
- where context compression or long outputs started to distort behavior.
