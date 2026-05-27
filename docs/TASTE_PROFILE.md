# TASTE_PROFILE.md — Taste Profile and Examples

Taste is an operational quality layer. It is not “I like it / I dislike it”. It is a set of preferences that shapes design decisions, implementation fidelity, copy, and review.

## Default product taste

- Clear over clever.
- Useful over impressive.
- Calm over noisy.
- Systemic over decorative.
- Specific over generic.
- Human over corporate.
- Fast to understand over rich to admire.
- Design-system fidelity over local prettiness.

## Default UI taste

- One obvious primary action per decision moment.
- Strong information hierarchy.
- Consistent spacing, density, radius, and component rhythm.
- Empty states that explain context and next action.
- Error states that explain recovery.
- Loading states that protect perceived progress.
- No raw UI if a DS component or token exists.
- No decorative novelty without product reason.

## Default content taste

- Short, concrete, action-oriented.
- No fake friendliness.
- No blame.
- No generic “Something went wrong” when recovery can be described.
- Labels should describe user intent, not implementation internals.
- CTA text should include the object when ambiguity is possible.

## Good / bad examples

### Primary action
Good:
- One visually dominant CTA aligned with the user’s next step.
- Secondary actions are quieter and placed after the primary path.

Bad:
- Three visually equal buttons compete in one block.
- Primary action is hidden in a menu while decorative metrics are emphasized.

### Empty state
Good:
- “No interviews yet. Add the first interview to start collecting insights.”
- Includes one relevant action.

Bad:
- “Nothing here.”
- Decorative illustration with no explanation or next step.

### Error state
Good:
- “Could not save the interview. Check the required fields and try again.”
- Error appears near the field or action it affects.

Bad:
- “Oops!”
- Red toast with no recovery instruction.

### Design-system fidelity
Good:
- Uses existing `Button`, `Card`, `Input`, `Dialog`, `Tabs`, and DS tokens.
- Records approved deviations when a DS component cannot cover the need.

Bad:
- Custom `div` styled as a button when DS `Button` exists.
- Hardcoded colors, shadows, spacing, and one-off card layouts.

### Prototype without DS
Good:
- A small Prototype UI Kit Contract defines typography, spacing, roles, buttons, cards, forms, states, and density.
- Every screen uses the same local rules.

Bad:
- Each screen invents its own button size, card density, field style, and accent color.

### Data display
Good:
- The chart answers one explicit question.
- Scale, aggregation, and comparison are clear.

Bad:
- Dashboard shows many metrics but no decision hierarchy.
- Decorative charts obscure the user’s next action.

### Copy tone
Good:
- “Create request” when the object is a request.
- “Approve invoice” when the action is specific.

Bad:
- “Submit”, “Proceed”, “Continue” used everywhere regardless of context.
- Corporate fog: “Leverage operational capabilities to facilitate workflows.”

## Anti-taste

- Pretty but unclear.
- Clever but inconsistent.
- Dense without hierarchy.
- Friendly but imprecise.
- Minimalist but hiding required context.
- Custom UI that only looks similar to DS components.
- Metrics without a decision.
- Redesign that improves aesthetics but worsens task completion.

## Project taste fields

A task may override the default taste profile with:
- desired feel;
- product adjectives;
- good references;
- bad references;
- UI density;
- visual expressiveness;
- content tone;
- DS strictness;
- examples supplied by user;
- forbidden patterns.

## Evidence rule

Taste can guide decisions, but taste is not evidence. Taste judgments must be framed as:
- observed issue;
- taste principle affected;
- likely user/product impact;
- proposed fix;
- whether user approval is needed.
