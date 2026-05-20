# LANGUAGE_POLICY.md — Language, token discipline, and artifact rules

This kit is designed for users who may prefer one conversational language while the project artifacts remain compact and stable.

## Default language policy

- User-facing assistant replies: **Russian**, unless the user asks otherwise.
- Project control artifacts: **compact English** by default.
  - Examples: `TASK.md`, `CHRONICLE.md`, role outputs, planning briefs, risk tables, review reports.
- Product UI copy: use the **product/user language** defined in `TASK.md`.
- Code identifiers: follow the existing project convention; do not translate identifiers just because the user speaks Russian.
- Code comments: follow the existing codebase convention. If none exists, prefer concise English.
- Research/source notes: preserve original terms when translating would reduce precision.

## Why this policy exists

Russian conversation is comfortable for the user, but long Russian artifacts can use more tokens than compact English. The team should therefore keep large reusable control artifacts in compact English, while preserving Russian for user-facing communication.

## What not to do

- Do not write long bilingual duplicates by default.
- Do not mix Russian and English inside the same user-facing paragraph unless quoting code, filenames, product terms, or user-provided wording.
- Do not translate product UI copy without checking the product language.
- Do not expose or fabricate internal chain-of-thought. Use concise summaries, decision logs, and evidence tables instead.
- Do not use “think in English” as an instruction. Instead: keep internal notes concise and keep durable artifacts in compact English.

## Required `TASK.md` fields

Every non-trivial task should define:

```markdown
## Language policy
- User communication language: Russian
- Control artifacts language: compact English
- Product UI language: TBD
- UX copy language: same as product UI language unless specified
- Code/comment language: existing project convention, otherwise compact English
```

## Role-specific implications

- UX Writer must write product copy in the product UI language, not necessarily the user communication language.
- Localization Specialist is required when product language, locale, cultural expectations, or translation quality affects the task.
- Technical Writer should produce PR/release docs in the repository language unless the user asks otherwise.
- Chronicle Keeper should maintain compact English chronicle entries plus a short Russian summary when useful for the user.
