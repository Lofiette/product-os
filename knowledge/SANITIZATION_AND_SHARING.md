# Knowledge Sanitization and Sharing

Canonical Product Knowledge may contain internal product structure, user decisions, source paths, contract details, or sensitive operational evidence. It must remain useful without becoming a secret store.

## Classification

- `public`: safe for deliberate public distribution.
- `internal`: ordinary project knowledge; external sharing is prohibited by default.
- `confidential`: material whose disclosure could harm users, the organization, or product security.
- `restricted`: credentials, regulated data, private keys, production secrets, or similarly high-risk material. Restricted values must not be stored in canonical Product Knowledge.

## Sharing policy

Each artifact records `external_sharing` and `sanitization_status`. External sharing is never inferred from file location.

- `allowed`: only for public or explicitly reviewed material.
- `after_sanitization`: allowed only after status becomes `sanitized`.
- `prohibited`: local/team use only.

## Sanitization rules

1. Reference secret locations; never copy secret values.
2. Replace personal, customer, credential, and environment-specific values with typed placeholders.
3. Preserve the decision-relevant meaning after redaction.
4. Record redactions and limitations in `sharing.redactions` and `sharing.notes`.
5. Run `knowledge-sanitize-check --external` before exporting or attaching Product Knowledge outside its approved scope.
6. Vector or semantic recall layers may return candidates, but exported evidence must be traced to sanitized canonical sources.

The runtime scans for common high-risk token patterns. This is defense in depth, not a guarantee that all sensitive information is detected.
