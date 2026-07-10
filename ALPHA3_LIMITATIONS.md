# Alpha 3 limitations

- Trigger evaluation is a deterministic metadata proxy, not a live Codex model trace.
- Logical roles, role-to-skill routing, quality-gate registry, and worker archetypes remain Phase 4 work.
- Domain packs are bundled and exposed independently but are not enabled automatically by installation.
- The combined engineering pack is an Alpha 3 consolidation choice; it may be split only if behavioral evidence shows better discovery or distribution ergonomics.
- Hooks, rules, native permission profiles, SQLite, MCP, external services, and behavioral CI remain later phases.
- Legacy aliases are documented and machine-mapped, not installed as active skills.
- Installing every optional pack at once exceeds the intended initial discovery profile; enable only relevant packs.
- Authorization leases remain runtime records rather than native sandbox boundaries.
- Cross-platform behavior has synthetic coverage but not full production CI across every Codex host.
