
# Hook trust and fallback

Non-managed project and plugin hooks must be reviewed and trusted in Codex. Installing or enabling CPT Core does not automatically trust the current hook definition.

CPT stores `hooks.trust_state` as an operator record only. It cannot verify Codex's internal trust registry. Marking it `trusted` is a human assertion after review.

If project config is untrusted, project-local config, rules, and hooks can be skipped. Personal plugin behavior remains subject to the active Codex host and plugin enablement.

The file-only runtime and CLI remain the fallback contract when hooks do not run.
