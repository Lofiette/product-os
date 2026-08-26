# product-os-chat-export

Technical forensic export for the dialogue package named `product-os-development-to-4.0`.

- Visible dialogue date range: 2026-05-20 through 2026-08-21.
- Export prepared: 2026-08-21.
- Included artifact files: 194.
- Missing or inaccessible artifact records: 58.
- Total included artifact size before outer ZIP: 27298721 bytes.

## Structure

- `uploaded/`: actual bytes of user-uploaded image attachments available in the active sandbox.
- `generated/`: actual bytes of assistant-generated files and archives available in the active sandbox.
- `manifest.json`: included and missing artifact registry.
- `conversation-file-map.json`: factual mapping between visible stages and artifact IDs.
- `missing-assets.json`: mentioned assets whose bytes were unavailable.
- `checksums.sha256`: SHA-256 values for every file included in the package except the checksum file itself.
- `visible-transcript.md`: auxiliary partial transcript with explicit gap markers; it is not a canonical account export.

## Integrity verification

From the directory containing the unpacked `product-os-chat-export/` folder:

```bash
cd product-os-chat-export
sha256sum -c checksums.sha256
```

On macOS without GNU `sha256sum`, individual files can be checked with:

```bash
shasum -a 256 <path>
```

The final outer ZIP SHA-256 is reported separately after packaging.
