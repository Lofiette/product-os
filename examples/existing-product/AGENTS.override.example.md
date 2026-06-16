# AGENTS.override.md

Local-only Codex runtime override for this workspace.

This file defines how Codex should work in this local environment without changing project code or tracked project files.

## Safety rules

- Do not modify application code unless the user explicitly asks.
- Do not modify repository runtime files such as `AGENTS.md`, `TASK.md`, or `CHRONICLE.md` unless the user explicitly asks.
- Do not create branches, commits, or staged changes.
- Do not run destructive Git commands.
- Before making file changes, explain what will change and ask for approval.

## Local runtime memory

Use local runtime memory only if it exists:

- `.codex-runtime/CURRENT.md`
- `.codex-runtime/TASK_INDEX.md`
- `.codex-runtime/CHRONICLE.md`
- `.codex-runtime/tasks/*`
- `.codex-runtime/context/packets/*`

If local runtime memory does not exist yet, ask the user before creating it.

Do not use root `TASK.md` or root `CHRONICLE.md` as active working memory by default.

## Context economy

Keep context small.

- Load only files needed for the next decision.
- Do not load old logs, archives, diagnostics, generated files, or broad external modules by default.
- Prefer targeted file reads over broad scans.
- Prefer `git diff --stat` before full diffs.
- Avoid large command outputs unless debugging a specific failure.

## Execution transparency

Before acting, report:

- files loaded;
- current task or ticket;
- whether roles are simulated or real subagents are spawned;
- skills or workflows used;
- blockers;
- next proposed operation.

If real subagents are needed, propose the lineup and ask for approval before spawning.

## UI and design work

For UI/design work:

- Build success is not design success.
- If a visual reference is provided, compare against it explicitly.
- If design-system compliance is claimed, cite the actual component/token/source or approved deviation.
- If evidence is missing, say so instead of returning a clean PASS.

## Language

Answer the user in Russian.
Keep internal artifacts concise.

## Bounded discovery mode

After the user gives a concrete product/UI task, Codex may perform bounded read-only discovery without requiring the user to list exact files.

Allowed by default for bounded discovery:
- targeted search in `src/`, `app/`, `components/`, `lib/`, `styles/`;
- reading small relevant files found by targeted search;
- `git diff --stat`;
- reporting an Impact Map.

Not allowed without approval:
- editing files;
- broad repository scans;
- reading root `TASK.md` or root `CHRONICLE.md`;
- broad external module reads, including local design-system/reference modules, except specific approved entrypoints;
- running build/test/lint;
- spawning real subagents.

Before implementation, Codex must provide:
- Impact Map;
- proposed files to edit;
- reason for each edit;
- risks;
- verification plan;
- approval request.

## Framework loading policy

This local override is a startup gate, not a replacement for the product-team framework.

Do not load the whole framework by default.

When a concrete task is given:

1. Start from local runtime memory.
2. Use `PRODUCT_MAP` and `KNOWLEDGE_INDEX` to choose the relevant product area.
3. Select the smallest useful set of roles and skills.
4. Load only relevant role cards, skills, playbooks, and gates.
5. Do not load all roles, all skills, all docs, or root `AGENTS.md`.

For product/UI discovery, planning, or review tasks, consider:
- product_designer
- ux_writer
- design_system_guardian
- design_engineer
- qa_engineer

For product/UI implementation tasks, also consider:
- frontend_architect or frontend_engineer
- code_reviewer
- qa_engineer

For UI work involving data, API behavior, persistence, or server/client contracts, also consider:
- api_contract_guardian
- backend_architect, if backend/API behavior may change
- data_architect, if data model or entities may change

For architecture/API/data tasks, choose corresponding architecture and engineering roles instead of design-only roles.

Before using real subagents, propose the lineup and ask for approval.

If the required role/skill path is unknown, ask for permission to run a bounded framework-index discovery, not a broad project scan.