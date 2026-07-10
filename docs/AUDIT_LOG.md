
# Runtime audit log

Audit events are stored as JSON Lines in `.cpt/audit/events.jsonl` and rotated by size.

Events include hashes and redacted previews of commands, paths, decisions, violations, output-size estimates, knowledge artifacts marked for review, and worker lifecycle metadata. Raw tool output and full subagent messages are not persisted.

Audit logs are machine-local by default, including in team-shared installations. Do not treat them as canonical Product Knowledge.
