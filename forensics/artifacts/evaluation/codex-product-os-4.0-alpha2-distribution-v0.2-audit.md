# Codex Product Operating System 4.0 Alpha 2 — Distribution Split Audit

Date: 2026-07-10  
Version: `4.0.0-alpha.2`  
Phase: **Phase 2 — Distribution Split**

## Verdict

**PASS for Phase 2 / Alpha 2 Distribution Split, with explicitly documented boundaries.**

The package converts the Alpha 1 Runtime Kernel into a safe, independently distributable architecture. It does not yet claim the full Alpha 2 Expertise acceptance criteria: role migration and skill consolidation remain later workstreams.

## Implemented

- minimal repo scaffold;
- native Codex `cpt-core` plugin;
- personal and repo marketplace exposure;
- local-ignored mode;
- team-shared mode;
- managed `AGENTS.md` block;
- safe handling of existing tracked `AGENTS.md`;
- installation receipt;
- conflict-aware update;
- state-preserving uninstall backup;
- independent domain-pack add/remove boundary;
- domain pack template and contract;
- plugin metadata-budget measurement;
- static distribution validator;
- behavioral distribution tests;
- preserved Alpha 1 runtime task/micro/lease/checkpoint behavior.

## Metrics

| Metric | Result |
|---|---:|
| Repo files after local install | 10 |
| Repo files after team install with repo plugin | 15 |
| Required maximum | `< 20` |
| Root managed `AGENTS.md` block | 2,156 bytes / 46 lines |
| Core plugins | 1 |
| Core skills | 1 |
| Estimated core skill discovery metadata | 375 characters |
| Distribution behavioral tests | 12 |
| External services required | 0 |
| Application source files touched by install | 0 |

## Phase 2 exit criteria

| Criterion | Status | Evidence |
|---|---|---|
| New project receives fewer than 20 repo-local framework files | PASS | local: 10; team + repo plugin: 15 |
| Core works without domain packs | PASS | runtime integration with `--plugin-scope none` |
| Packs can be exposed/removed independently | PASS | synthetic domain pack test; core preserved |
| Uninstall does not damage the project | PASS | application source survived uninstall unchanged |

## Static validation

```text
DISTRIBUTION STATIC VALIDATION PASSED
core metadata estimate: 375 chars
Python syntax validation: PASS
```

Validated:

- plugin manifest and path rules;
- skill frontmatter;
- `agents/openai.yaml` parseability;
- marketplace relative path;
- managed AGENTS markers;
- root loader guidance size;
- absence of private product or design-system names;
- domain pack contract shape.

## Behavioral tests

Passed individually:

1. local install remains Git-clean and below file budget;
2. team install with repo plugin remains below file budget;
3. existing tracked `AGENTS.md` is not modified in local mode;
4. update preserves mutable runtime state;
5. update refuses modified managed tooling without `--force`;
6. uninstall preserves application files;
7. personal marketplace preserves unrelated plugin entries;
8. domain pack removal preserves core;
9. team-mode managed block uninstall preserves existing AGENTS content;
10. personal core plugin survives project uninstall by default;
11. core metadata stays within the test budget;
12. doctor passes after local install.

## Runtime integration

The installed scaffold successfully completed:

```text
create Standard Task
create scoped lease
create checkpoint
verify checkpoint
validate runtime
complete task
start Micro Change
complete Micro Change
validate runtime
```

Result:

```text
ALPHA2-RUNTIME-INTEGRATION-PASSED
```

## Safety behavior

- installer never runs `git add`, commit, branch, reset, or clean;
- existing tracked AGENTS stays untouched in local mode by default;
- AGENTS ownership is limited to an explicit marked block;
- updates replace only receipt-owned tooling files;
- mutable runtime records are preserved;
- uninstall backs up state outside the project unless explicitly discarded;
- personal plugin removal requires an explicit flag;
- plugin does not own canonical runtime state;
- no optional service is required.

## Honest limitations

- Marketplace exposure does not enable the plugin automatically.
- Codex restart or plugin UI installation may be required.
- Existing manually copied Alpha 1 installs are not adopted automatically.
- YAML remains the exact registry; SQLite is not implemented yet.
- Domain packs contain only a packaging contract/template.
- The 50-role and 95-skill expertise library is not migrated.
- Hooks, rules, permission profiles, Product Knowledge, workers, and external adapters are absent.
- Full cross-platform execution is not yet CI-verified.
- The authorization lease remains a runtime contract, not a native security boundary.

## Official compatibility basis

The package follows current Codex documentation for:

- `.codex-plugin/plugin.json` plugin manifests;
- `skills/` packaging;
- personal and repo marketplaces;
- relative `./` plugin source paths;
- `agents/openai.yaml` skill metadata;
- independent plugin enable/disable behavior;
- project trust boundaries.

## Recommendation

Freeze this package as **Alpha 2 Distribution baseline** and proceed to Phase 3: Skills Consolidation. Do not add Product Knowledge or role content to the always-on repo scaffold.
