# Codex Product Operating System 4.0 Alpha 6

## Audit report: Deterministic Runtime Enforcement

**Version:** `4.0.0-alpha.6`  
**Phase:** Deterministic Runtime Enforcement  
**Verdict:** **PASS for the Alpha 6 phase scope, with explicit platform and enforcement limitations**

## 1. Scope of this phase

Alpha 6 adds an optional deterministic guardrail layer on top of the file-only Runtime Kernel, Product Knowledge lifecycle, canonical skills, logical roles, quality gates, and distribution split delivered in Alpha 1–5.

Implemented concerns:

- lifecycle hooks for session start, tool use, permission requests, compaction, workers, and stop;
- lease-aware policy checks for supported writes and verification commands;
- globally forbidden destructive command classes;
- pre-compaction checkpoints and post-compaction state verification;
- targeted Product Knowledge freshness propagation after detected project writes;
- local audit events with rotation and secret redaction;
- subagent lifecycle records;
- optional command rules;
- optional permission-profile examples;
- CLI fallback when hooks are disabled or untrusted.

Not in scope:

- full security-boundary enforcement;
- complete interception of all Codex tools;
- worker archetype orchestration, cancellation, quorum, or worktrees;
- live Codex model certification;
- external observability or remote audit storage;
- SQLite/MCP/external adapters.

## 2. Architectural decisions

### 2.1 Enforcement modes

`.cpt/enforcement.yaml` supports:

- `off`: no hook behavior or audit events;
- `audit`: record and surface supported violations without blocking;
- `enforce`: deny or stop supported violations when the corresponding hook event permits it.

The dedicated enforcement config is installed as mutable runtime state and survives updates.

### 2.2 Native Codex controls remain authoritative

CPT authorization leases and hooks are workflow guardrails. They do **not** replace:

- Codex sandboxing;
- permission profiles;
- approval policy;
- command rules;
- project trust;
- enterprise-managed requirements.

This follows the current Codex hook model, which explicitly describes `PreToolUse` as an incomplete guardrail rather than a comprehensive enforcement boundary.

### 2.3 Hook trust is explicit

Plugin hooks are bundled but are not assumed trusted. The runtime stores only an operator annotation (`unknown`, `trusted`, `untrusted`, or `disabled`). The actual Codex hook trust decision remains external to CPT.

### 2.4 Fallback remains functional

The runtime and Product Knowledge lifecycle continue to work with hooks disabled. Operators can explicitly run:

- `validate`;
- `policy-check`;
- `checkpoint`;
- `recover --verify-only`;
- `knowledge-stale-scan`;
- `audit-validate`.

## 3. Implemented hook events

The CPT Core plugin bundles handlers for:

1. `SessionStart`
2. `PreToolUse`
3. `PermissionRequest`
4. `PostToolUse`
5. `PreCompact`
6. `PostCompact`
7. `SubagentStart`
8. `SubagentStop`
9. `Stop`

Hook commands use `${PLUGIN_ROOT}` and delegate to the canonical project-local runtime CLI when a `.cpt/runtime.yaml` can be found from the event working directory.

## 4. Enforcement behavior

### 4.1 Write and verification policy

Supported `Bash` and `apply_patch` operations are classified for:

- project writes;
- broad reads;
- verification commands;
- dependency changes;
- network access;
- migrations;
- destructive Git operations;
- filesystem-root deletion.

In `enforce` mode:

- project writes require an active lease unless they are limited to exempt runtime paths;
- detected write targets must fall within the lease write scope;
- expensive verification commands must exactly match the approved verification scope;
- globally forbidden operations remain blocked even with a lease;
- unknown write targets fail closed unless an explicitly broad write lease was approved.

### 4.2 Compaction safety

`PreCompact`:

- validates runtime state;
- blocks enforce-mode compaction when workers are still active;
- creates a SHA-256 checkpoint;
- records it in current runtime state;
- prunes old automatic checkpoints according to retention policy.

`PostCompact`:

- resolves the latest checkpoint;
- verifies checkpoint integrity;
- compares the persisted snapshot with current runtime state;
- validates runtime pointers;
- blocks continuation in enforce mode on mismatch.

### 4.3 Knowledge freshness

After a classified project write, `PostToolUse` passes only relevant detected paths to the Product Knowledge stale scanner. Read-only commands do not mark pre-existing working-tree changes stale.

### 4.4 Audit records

Audit events include:

- event and decision;
- timestamp, session, and turn;
- tool name;
- command SHA-256;
- redacted command preview;
- detected paths;
- violations;
- bounded metadata.

The audit stream rotates by configured byte size and retention count. It does not store raw tool output.

### 4.5 Worker records

Subagent start/stop hooks create local worker records containing:

- agent id and type;
- lifecycle state;
- task and lease pointers;
- permission mode;
- timestamps;
- transcript path, when supplied;
- hash of the final assistant message rather than its raw content.

These records are observability state only. Alpha 6 does not yet orchestrate workers.

## 5. Optional rules and permission profiles

Two optional rules profiles are provided:

- `conservative`;
- `strict`.

Rules installation is explicit through `--rules-profile`; CPT does not silently change command rules.

Permission-profile files are examples only and are never installed automatically. They demonstrate read-only, workspace, and narrowly allowlisted network configurations.

## 6. Distribution behavior

- Local ignored mode keeps CPT runtime state out of Git when a Git repository is present.
- Team mode keeps the base framework footprint at **20 files or fewer**, including `.cpt/enforcement.yaml`.
- An optional rules profile adds one project-local policy file.
- Existing tracked `AGENTS.md` is not modified in local mode without explicit permission.
- Update preserves mutable runtime state, Product Knowledge, enforcement config, audit logs, and worker records.
- Uninstall does not remove application files and backs up runtime state by default.

## 7. Validation and evaluation results

### Behavioral tests

- Distribution: **17 / 17**
- Skills: **5 / 5**
- Roles: **4 / 4**
- Product Knowledge: **13 / 13**
- Enforcement: **19 / 19**
- **Total: 58 / 58**

### Static and proxy validation

- Distribution static validation: PASS
- Skill validation: PASS
- Role validation: PASS
- Knowledge asset validation: PASS
- Knowledge runtime validation: PASS
- Enforcement asset validation: PASS
- Enforcement policy eval: **5 / 5**
- Enforcement integration: **13 / 13**
- Knowledge lifecycle eval: **11 / 11**
- Skill trigger proxy eval: **135 / 135**
- Role routing proxy eval: **164 / 164**
- Python compilation: PASS
- Node syntax validation: PASS
- Manifest integrity: PASS
- ZIP integrity: PASS

### Integration coverage

The deterministic integration fixture verifies:

- installation and Git cleanliness;
- doctor;
- Standard Task and lease creation;
- allowed and denied writes;
- destructive Git denial;
- knowledge freshness marking;
- pre/post-compaction checkpoint flow;
- worker lifecycle recording;
- audit validation;
- final runtime validation.

This is a deterministic runtime integration test, **not** a live Codex behavioral certification.

## 8. Known limitations

1. `PreToolUse` and `PostToolUse` do not intercept every possible tool path.
2. Hook trust must be reviewed in Codex; the package cannot establish it.
3. Managed configuration may disable non-managed hooks.
4. Command classification is conservative and cannot fully parse arbitrary shell programs.
5. Native rules syntax was statically reviewed but not executed with `codex execpolicy check` in the build environment because a Codex binary was unavailable.
6. Audit redaction is defense in depth, not a dedicated secret-scanning product.
7. A failed write may conservatively mark affected knowledge as needing review.
8. Worker records do not implement timeout, cancellation, quorum, or worktree isolation.
9. Audit JSONL is local and not a tamper-evident remote log.
10. Permission profiles require a sufficiently recent Codex client and must not be mixed with legacy sandbox settings.

## 9. Release recommendation

Alpha 6 is accepted as the baseline for the Deterministic Runtime Enforcement phase.

Recommended operating sequence:

1. install with enforcement `off` or `audit`;
2. inspect and trust hooks in Codex;
3. review audit output and tune leases;
4. optionally install a rules profile;
5. switch to `enforce` only after representative tasks pass;
6. continue to rely on native sandbox, permissions, approvals, and managed requirements.

## 10. Next phase

**Phase 7: Worker Orchestration** should add:

- 8–12 executable worker archetypes rather than 50 role-agents;
- bounded role-lens injection;
- max threads and depth;
- timeout and cancellation;
- required/optional quorum;
- worktree isolation for parallel writes;
- disjoint write scopes;
- disk-backed orchestration state;
- recovery after compaction or reconnect;
- executable failure and concurrency evals.

## 11. References reviewed

- Codex Hooks: https://developers.openai.com/codex/hooks
- Codex Rules: https://developers.openai.com/codex/rules
- Codex Permissions: https://developers.openai.com/codex/permissions
- Codex Config Reference: https://developers.openai.com/codex/config-reference
- Codex Agent Approvals & Security: https://developers.openai.com/codex/agent-approvals-security
- Codex Build Plugins: https://developers.openai.com/codex/plugins/build
