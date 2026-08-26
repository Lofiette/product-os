
# Lease enforcement

A scoped authorization lease describes approved reads, writes, verification commands, delegation budget, forbidden operation classes, and expiration.

Beta 1 enforces only operations that can be classified from supported hook inputs. Unknown or ambiguous tool paths are never presented as fully secured. In enforce mode, obvious project writes without an active matching lease are denied. `.cpt/**` runtime writes remain exempt when configured.

A lease never expands native Codex permissions and never overrides the sandbox.
