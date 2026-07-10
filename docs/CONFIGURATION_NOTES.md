# Codex Configuration Notes

- Codex loads project `AGENTS.md` instructions when a session starts. Restart or start a new session after changing stable instructions.
- Project instruction discovery has a combined byte budget, so the root loader is intentionally small.
- Native sandbox and approval policies remain independent of CPT authorization leases.
- Project hooks require trust review. Alpha 1 ships a checkpoint contract, not active hooks.
- Optional integrations are not required for startup, validation, checkpointing, or recovery.

See `docs/REFERENCES.md` for primary documentation.
