# Form Knowledge Policy

Policy ID: `cpt-form-knowledge-policy-v1`
Primary source: Adam Silver, *Form Design Patterns* (2018).
Supporting source: Tidwell et al., *Designing Interfaces*, third edition.
Status: transformed operational summary; source books and code are not bundled.

## Purpose

Treat forms as task and service design, not a pile of fields. Reuse conventions and native semantics because familiarity, resilience, and accessibility reduce effort, but allow evidence-based exceptions. Preserve the source books' problem-oriented framing and explicit trade-offs without freezing 2018 browser code or platform behavior into current rules.

## Source authority

1. Current legal, security, privacy, payment, identity, and domain rules.
2. Verified user research, operational evidence, and product outcomes.
3. Current platform, accessibility, and design-system authority.
4. This transformed form canon.
5. Historical implementations and source examples.

## Durable principles

- Question the process before styling the form.
- Ask for the minimum information at the moment it becomes necessary and understandable.
- Use clear labels, persistent guidance, familiar controls, and plain action language.
- Prefer native semantics and progressive enhancement; custom behavior inherits the complete accessibility and failure contract.
- Give users control, choice, comparable ways to complete tasks, and a robust fallback.
- Prevent trivial errors, accept harmless input variation, preserve entered data, and make correction easy.
- Design validation, errors, focus, announcements, loading, partial success, and recovery as one system.
- Match flow structure to frequency, expertise, branching, duration, risk, and number of actors.
- Support review before consequential commitment and explain what happens next afterward.
- Optimize the second-time experience without making dangerous assumptions.

## Contextual, not universal

- One thing per page is a candidate for complex or infrequent flows, not a literal one-field law.
- Live validation can help in bounded cases but can also interrupt; choose timing from the task and evidence.
- Labels above controls are a robust default, but project layout and professional density may justify tested alternatives.
- Error summary plus inline errors is useful for long/reloaded forms; short local interactions may need a smaller feedback model.
- Default choices must reflect common safe circumstances, remain visible, and never manufacture consent.
- Exact dimensions, browser workarounds, code examples, ARIA patterns, password advice, and conversion figures require current verification.
