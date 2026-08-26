# RC trials and release gates

Beta 1 is certified for the deterministic, self-contained offline scope. It is not an RC and does not claim live Codex certification.

Eleven release gates separate evidence that can be proven locally from evidence that requires native platforms or a live Codex client. The provider-neutral Manager/adoption gate is deterministic and beta-required; real isolated Codex switching plus a fresh-session lifecycle receipt is a separate RC gate. A gate marked `PENDING` is not silently converted into `PASS`.

The release tool reads the package's reviewed registries and reports. It does not replace the underlying validators or executable evaluation harness.

## Offline Beta gate

Beta requires package integrity, offline regression, migration safety, install/update/rollback, universality, and documentation. Native platform and live-model gates may remain pending.

## RC gate

RC additionally requires native Linux/macOS/Windows/WSL evidence, a real isolated Codex adoption with new-session evidence, live Codex tasks with real worker threads and compaction/reconnect, token and latency measurements, and an independent mega-audit.
