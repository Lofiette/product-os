
# Permission profile guidance

CPT authorization leases are workflow records, not sandbox boundaries. Use the narrowest native Codex permission profile that lets a task complete.

- `readonly.example.toml` is suitable for planning and review.
- `workspace.example.toml` is suitable for approved implementation inside the workspace.
- `readonly-net.example.toml` demonstrates a narrowly allowlisted network profile.

Copy these snippets into an appropriate user or managed Codex config only after review. CPT does not install permission profiles automatically.
