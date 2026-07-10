# Localization Readiness Gate

Gate ID: `gate-localization-readiness`

## Apply when

For multilingual products or changes that affect locale-sensitive content/layout.

## Owners

- `localization_specialist`
- `ux_writer`

## PASS criteria

- Strings are externalizable and context-rich.
- Plural, date, number, expansion, directionality, and cultural risks are covered as relevant.
- Pseudo-localization or representative locales have been considered.

## BLOCK criteria

- Concatenated strings prevent correct grammar.
- Layout assumes one language length or direction.
- Locale-sensitive values are formatted manually.

## Required evidence

- String inventory
- Locale-risk checklist
- Pseudo-localization result

## Verdict contract

- `PASS`: required evidence supports the acceptance claim.
- `PASS_WITH_WARNINGS`: acceptance is supportable, with explicit non-blocking residual risk.
- `BLOCKED`: one or more blocking conditions are present.
- `INSUFFICIENT_EVIDENCE`: the gate cannot responsibly decide.

A warning must never hide a blocker. Missing evidence must never be converted into a clean pass.
