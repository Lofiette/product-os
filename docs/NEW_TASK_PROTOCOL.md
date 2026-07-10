# New Task Protocol

Use for work that is not eligible for the Micro Change Protocol.

## Flow

1. Capture the user intent.
2. Create a runtime task record automatically; runtime bookkeeping does not require a separate approval.
3. Classify task type and complexity.
4. Load only relevant product knowledge and expertise when available.
5. Perform bounded read-only discovery.
6. Produce an Impact Map or compact equivalent:
   - affected areas and files;
   - assumptions and unknowns;
   - product/engineering risks;
   - proposed writes;
   - verification plan;
   - required expertise/delegation.
7. Request one scoped authorization lease covering approved reads, writes, verification, and delegation.
8. Implement within the lease.
9. Renew the lease if scope changes.
10. Verify, update affected durable knowledge, complete the task, and compact runtime state.

## No ceremony for its own sake

Do not create separate artifacts when the active task record can represent the needed information compactly. Create a context packet only when it reduces repeated reads or supports delegation/recovery.
