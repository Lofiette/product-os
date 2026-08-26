# Versioning policy for reconstructed Product OS history

## Public releases

- `v4.0.0`: Product OS immediately before the Product Designer redesign. This is the former internal Beta 1 baseline, retrospectively normalized as the public 4.0.0 release by explicit project decision on 2026-08-21.
- `v4.1.0`: reserved for the next release containing the redesigned Product Designer and the adoption/migration work. It is intentionally not present in this history yet.

## Historical checkpoints

All refs under `snapshot/*` are forensic checkpoints. They preserve development progress but are not promoted to public SemVer releases. This prevents internal alpha/beta iterations from being confused with the official product version line.
