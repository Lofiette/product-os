# Reconstruction method

## Sources

The reconstruction uses three evidence classes:

1. Canonical ChatGPT account export for the conversations `Продуктовая команда в Codex` and `Миграция на среду 4.0`.
2. Byte-preserved generated artifacts from `product-os-development-to-4.0.zip`.
3. The previously corrected 4.0 release tree used only for the explicit retrospective normalization from internal `4.0.0-beta.1` to public `4.0.0`.

## Actual artifact vs reconstructed history

A source snapshot commit is created only when a corresponding ZIP artifact is present and its SHA-256 matches the forensic manifest. Missing snapshots are never recreated from conversational descriptions.

The Git commits themselves are reconstructed metadata. Commit dates correspond to the message timestamps where the artifacts were delivered, but these are not claimed to be original historical Git commits.

## Source-history normalization

For source commits, the single distribution wrapper directory is stripped. Generated Python bytecode caches (`__pycache__`, `*.pyc`) are omitted from source-history trees. The original ZIP files are preserved byte-for-byte on this `forensic/history` branch under `forensics/artifacts/release_archive/`, so normalization never destroys the historical evidence.

## Training

Artifacts categorized as `training` are deliberately excluded from the product repository. Their existence and hashes remain visible in the source forensic manifest.

## Privacy

Raw ChatGPT conversation exports and user-uploaded screenshots are not committed. The repository keeps artifact provenance and message identifiers, not the user's full account history.
