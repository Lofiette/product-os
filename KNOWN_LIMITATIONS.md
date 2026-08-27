# Product OS 4.1 known limitations

Product OS 4.1 is offline-certified for its deterministic scope. Its deterministic fixtures, runtime contracts, migration safety, package integrity and evaluation harness have been exercised without external services.

It does not yet certify:

- live Codex model quality outside the explicitly recorded release-trial cases and configurations;
- real subagent event ordering and cancellation delivery;
- native reconnect behavior across Codex clients;
- real Codex plugin install/switch/cache behavior on macOS or WSL; Windows has
  one owner-confirmed Product OS 4.1 adoption, rollback rehearsal, and fresh-session check;
- cross-client delivery of the new-session lifecycle receipt; one actual Windows
  Codex session is recorded in the reviewed release evidence;
- token, latency and cost behavior outside the recorded live release trials;
- screenshot-based visual fidelity grading;
- organization-managed permission and plugin policies.

The production adoption provider is intentionally local-Git-only in 4.1: it
does not fetch a remote or run repository hooks. Codex legacy selector
retirement is also intentionally deferred; rollback remains available and the
old selectors are retained until registry-wide reference completeness can be
proven. These two boundaries are acceptance risks, not simulated capabilities.
For lifecycle evidence with a non-default Manager root, the new Codex process
must inherit the exact `PRODUCT_OS_HOME`; the CLI fails closed when a
lifecycle-required doctor run does not match it.

External services remain optional. The core continues to work with local files, Git and Python only.
