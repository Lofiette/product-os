# Domain Pack Contract

A domain pack is an optional, independently enabled Codex plugin that groups a coherent set of methods. It must not own canonical CPT runtime state.

## Required files

```text
<pack>/
  .codex-plugin/plugin.json
  cpt-pack.json
  README.md
  skills/<skill>/SKILL.md
  skills/<skill>/agents/openai.yaml
```

## `cpt-pack-v2`

Each pack declares:

- stable kebab-case `name`;
- `kind` and version;
- core compatibility range;
- coherent domain labels;
- `canonical_state_owner: false`;
- optional/required status;
- exact `skill_count`;
- exact `skill_ids` inventory;
- legacy package provenance and source-skill count.

The installed skill folders, plugin manifest, and pack inventory must agree. Validators reject drift.

## Domain boundary

Create a pack only when it represents a stable working domain with a useful independent activation profile. Do not create a pack merely to:

- preserve old folder organization;
- expose aliases;
- reduce file count without improving discovery;
- represent one rare method that belongs in an existing domain.

A pack should be installable and removable without modifying core or another pack.

## Skill requirements

Every active skill must follow `SKILL_AUTHORING_STANDARD.md`, include invocation metadata, and have trigger cases. Pack-level README content is navigation; skill details remain inside the skill.

## Metadata and activation

Pack descriptions and skill metadata contribute to initial discovery. Packs must stay within release budgets and be enabled only when relevant. The package catalog records supported profiles; enabling all optional packs simultaneously is a diagnostic condition rather than the default usage model.

## State and services

A domain pack may provide methods, references, scripts, hooks, or optional MCP configuration in later phases, but canonical task/runtime state remains owned by the repo scaffold. Any external integration must have a local fallback and must not become the sole canonical knowledge store.

## Removal contract

Removal must:

- delete only the named pack and its marketplace entry;
- preserve `cpt-core`, other packs, runtime state, and application files;
- leave user-created task or knowledge artifacts untouched unless the user explicitly requests cleanup.
