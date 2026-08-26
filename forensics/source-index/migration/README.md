# product-os-migration forensic chat export

Archived chat: current Product OS migration conversation available in this ChatGPT thread.

Preparation date: 2026-08-21.

Included historical source artifacts: 0.

Missing or inaccessible referenced artifacts: 118.

Included historical source-artifact bytes: 0.

Directory layout:
- `uploaded/` — user-uploaded source attachments whose actual bytes were accessible.
- `generated/` — assistant-created historical artifacts whose actual bytes were accessible.
- `manifest.json` — manifest of uploaded/generated chat artifacts.
- `conversation-file-map.json` — message/stage-to-file-reference map.
- `missing-assets.json` — referenced files whose bytes were unavailable.
- `checksums.sha256` — SHA-256 hashes of packaged files except `checksums.sha256` itself.
- `visible-transcript.md` — auxiliary transcript of the chat text available to the exporter; explicit gap markers identify portions not available as a byte-exact transcript.

Integrity verification:
1. Extract the ZIP.
2. From `product-os-chat-export/`, run `sha256sum -c checksums.sha256`.
3. The final ZIP SHA-256 is reported with the delivered ZIP.

The historical Product OS ZIP was not unpacked, repacked, or reconstructed. Its bytes were unavailable to the exporter and it is recorded as inaccessible.
