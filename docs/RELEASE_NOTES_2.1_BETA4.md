# RELEASE_NOTES_2.1_BETA4.md

## Codex Product Team 2.1 beta 4 — System Coherence & Diagnostics Patch

Focus: practical reliability, not new process weight.

Changes:

- Added `docs/CODEX_DIAGNOSTIC_EXPORT_WSL.md` and `scripts/export-codex-diagnostics-wsl.sh` for VS Code + WSL diagnostic packs.
- Added `docs/SKILL_DISCOVERY_POLICY.md` to reduce reliance on implicit skill activation in a large skill set.
- Updated runtime guidance to explicitly select critical UI/design/runtime skills when triggers are present.
- Kept `SKILL_TINY_INDEX.json` intact: optimize by loading it less often, not by removing useful trigger text.
- Cleaned runtime version labels to 2.1 beta 4 where relevant.

No new roles were added. No major workflow expansion was introduced.
