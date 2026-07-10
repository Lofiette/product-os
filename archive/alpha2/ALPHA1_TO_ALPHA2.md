# Alpha 1 To Alpha 2

Alpha 2 preserves the Runtime Kernel behavior but changes distribution:

- runtime CLI and schemas move into `.cpt/`;
- seven schema files become one bundle;
- project docs are reduced to one operations reference;
- `cpt-core` becomes a separate native plugin;
- installation is receipt-driven;
- update preserves mutable state;
- local and team modes become explicit.

A manually copied Alpha 1 directory has no install receipt and is not automatically adopted in this phase. Migration tooling belongs to the RC migration phase.
