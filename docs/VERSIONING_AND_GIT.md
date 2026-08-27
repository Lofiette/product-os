# Versioning and Git model

## Source of truth

The Product OS Git repository is the canonical source for:

- roles, skills, gates, adapters, and knowledge policy;
- runtime scaffold and installer;
- plugin manifests and marketplace catalogs;
- tests, evals, migrations, and release evidence;
- documentation and changelog.

An installed project's `.cpt/` directory is runtime state, not a fork of Product OS source. Installed plugin copies are deployment artifacts, not canonical source.

## Semantic versioning

Product OS uses strict SemVer:

- **MAJOR**: incompatible runtime, receipt, policy, or project-migration contract;
- **MINOR**: backward-compatible roles, skills, adapters, gates, pack capabilities, and evals;
- **PATCH**: backward-compatible bug fixes, documentation corrections, and deterministic validation fixes.

Current lineage:

- `v4.0.0`: complete pre-redesign Product OS baseline;
- `v4.1.0`: the first complete Product Designer redesign, including UI craft, Interaction Intelligence, form and professional-interface expertise, and the portable Design Execution Plane.

Internal Preview 1 and Preview 2 checkpoints are ordinary development commits, not release versions or tags.

Plugin manifests, pack manifests, `VERSION`, `pyproject.toml`, package manifest, and release tag must use the same version.

## Branching

Use a deliberately small branching model:

- `main`: always releasable;
- `feat/<topic>`: short-lived feature work;
- `fix/<topic>`: short-lived corrective work;
- optional `release/<version>` only when a stabilization window is genuinely needed.

Avoid a permanent `develop` branch. Product OS already has a large validation plane; long-lived divergence would create more merge archaeology than value.

## Commit and release discipline

A release commit should include:

1. version bump across canonical metadata;
2. changelog entry;
3. migration note when behavior or installation changes;
4. regenerated `MANIFEST.json`;
5. passing validators and tests;
6. signed or annotated Git tag.

Example:

```bash
git switch main
git pull --ff-only
python tools/build_manifest.py
python tools/validate_distribution.py
python tests/run_all.py
git add -A
git commit -m "release: Product OS 4.1.0"
git tag -a v4.1.0 -m "Product OS 4.1.0"
git push origin main --tags
```

## Repository location

A private GitHub repository named `product-os` is the practical default while the environment contains internal operating knowledge. The repository can later be split into:

- an open core;
- private organization packs;
- private project knowledge.

Do not put secrets, personal Product Knowledge, live project receipts, or generated `.cpt/` state in the source repository.

## Distribution surfaces

The same source repository can produce several adapters:

1. source checkout for any agent or local tooling;
2. Codex marketplace through `.agents/plugins/marketplace.json`;
3. project bootstrap through `tools/cpt_dist.py`;
4. future Claude Code, Cursor, or other agent adapters generated from the same canonical skill corpus.

This preserves universality. Codex is a supported runtime, not the owner of Product OS.

## Pinning and rollout

For normal work, pin Product OS to a release tag rather than following `main` blindly:

```bash
git fetch --tags
git switch --detach v4.1.0
```

For active development, work on a branch. For production projects, upgrade one pilot project first, run `doctor`, then roll the same tag out to the rest.

## Folder naming

Use a stable local folder name:

```text
Product OS/
```

Do not create `Product OS 4.0`, `Product OS 4.1`, and `Product OS 4.2` as permanent parallel roots. Git tags and release artifacts already carry version identity. Side-by-side folders are useful only for temporary migration or forensic comparison.
