---
name: harness-engineering
description: >-
  Scaffold and maintain a documentation harness for AI-agent codebases (Claude
  Code, Codex, Cursor) — generates AGENTS.md plus a docs/ tree (ARCHITECTURE,
  SECURITY, RELIABILITY, DESIGN, QUALITY_SCORE, exec-plans, product-specs,
  generated db-schema, etc.) filled from real repo analysis, then keeps it in
  sync as the repo changes. Use this skill whenever the user wants to set up,
  bootstrap, initialize, or "harness" a repo for coding agents; asks for an
  AGENTS.md / CLAUDE.md / agent docs / project memory; mentions making a repo
  agent-ready, agent-friendly, or a "single source of truth" for agents; or
  asks to refresh/update/sync agent docs after code changes — even if they
  don't say the words "harness engineering."
---

# Harness Engineering

## What this does and why

AI coding agents fail less from weak models than from a weak **harness** — the
docs, conventions, and verification context that live in the repo. An agent
can't see Slack, Confluence, or a teammate's head: *if it isn't in the repo, it
doesn't exist for the agent.* This skill builds that harness as a documentation
tree, and keeps it from rotting.

It has **two modes**:

- **init** — scaffold the harness for a repo that doesn't have one
- **update** — refresh existing harness docs after code changed

Detect which mode you're in: if `AGENTS.md` plus a `docs/` harness already
exist, default to **update**. Otherwise **init**. When ambiguous, ask.

## Core principles (apply throughout)

These come from the harness-engineering discipline — internalize them; don't
just cite them:

1. **Repo is the single source of truth.** Every doc must be answerable from
   the repo. Don't invent facts — if you can't verify it, mark it a TODO.
2. **Co-locate and keep lean.** Each doc earns its place. A backend repo gets no
   `FRONTEND.md`. Empty/irrelevant files are dead weight that bury real signal.
3. **Self-contained + cited.** A fresh agent session must understand the project
   from these docs alone. Note where each fact came from (a path, a file).
4. **Verification beats prose.** Wherever possible, docs name the *command* that
   proves a claim (`pytest`, `npm run typecheck`), not just describe behavior.
5. **Don't let docs drift.** Stale docs are worse than missing ones. Update mode
   exists because entropy is the default.
6. **Layer the harness as a DOX contract hierarchy.** The root `AGENTS.md` is the
   project rail; each durable sub-boundary (a service, package, or major dir with
   its own purpose and rules) gets its own child `AGENTS.md` that acts as the
   local contract. A doc closer to the code is more specific; parents hold
   repo-wide rules. Every `AGENTS.md` that has children carries a **Child DOX
   Index** linking them. This keeps each part of the repo understandable from its
   nearest `AGENTS.md` plus the parents above it — see `references/dox.md`.

---

## Mode: init

### Step 1 — Analyze the repo (before writing anything)

You cannot write real docs without reading the repo. Gather:

- **Stack & tooling**: dependency manifests (`package.json`, `pyproject.toml`,
  `Cargo.toml`, `go.mod`, `Gemfile`), lockfiles, runtime version files,
  `Dockerfile`/`nixpacks`, CI config. Note exact versions.
- **Structure**: top-level dirs, where services/apps/packages live, entry points.
- **Data layer**: migrations, ORM models, `schema.sql`, `schema.rb`, Prisma —
  anything that defines a DB.
- **Surfaces**: HTTP routes, CLI commands, frontend pages/components, public API.
- **Verification**: how tests/lint/typecheck/build run (read scripts + CI).
- **Conventions**: existing patterns, `.cursorrules`, `.github/copilot-instructions.md`,
  any existing `CLAUDE.md`/`README.md` — fold their important parts in.
- **History**: recent git log for active areas and pace.

Run cheap parallel reads. If the repo is large, dispatch subagents to map
subsystems (see `dispatching-parallel-agents` if available).

### Step 2 — Decide the doc set (adaptive)

Pick only the docs the project warrants. Use `references/doc-catalog.md` — it
lists every harness file, its purpose, the **include-when** rule, and **what to
read** to fill it. Skip files whose include-when condition is false.

Tell the user the chosen set and why a few were skipped, before generating.

### Step 3 — Scaffold the tree

Create directories and empty files deterministically with the helper, then fill
them:

```bash
python3 ~/.claude/skills/harness-engineering/scripts/scaffold_tree.py \
  --root <repo-root> --manifest <comma-separated doc keys from catalog>
```

The script creates only the **directories** the chosen docs need (idempotent),
then prints the list of files to author. It does **not** create empty doc files —
you write each file's content directly with the Write tool in Step 4 (this avoids
a wasted Read-before-Write round-trip on pre-created empty files). Filling content
is your job, in Step 4.

### Step 4 — Fill each doc from analysis

Use `references/templates.md` for the skeleton of each doc. For every file:

- Write **real, verified content** from Step 1. Detected stack, actual services,
  the real db schema, the real verification commands.
- Where a fact needs human judgment you can't infer (product vision, design
  beliefs), leave a clearly-marked `<!-- TODO: ... -->` stub with a pointed
  question — never a fabricated answer.
- `AGENTS.md` is the canonical entry: ≤200 lines, one-sentence overview,
  quick-start, verification commands, ≤15 hard constraints, and a linked index
  of the docs/ tree. Critical rules go at top or bottom (middle gets ignored).

### Step 4b — Build the DOX contract hierarchy

Decide which directories are **durable boundaries** — a service, package, app, or
major module with its own purpose, conventions, or verification. Each gets a
child `AGENTS.md` (the local contract). Don't create one for every folder — only
where a real boundary exists; spurious child docs are dead weight.

For each child, use the DOX child shape in `references/dox.md`: Purpose,
Ownership, Local Contracts, Work Guidance, Verification, Child DOX Index. Fill
each from the code in that subtree, with verification commands specific to it.

Then give the **root `AGENTS.md` a Child DOX Index** listing each child and what
it covers. A child that has its own children repeats the pattern. Read
`references/dox.md` for the exact rails before writing these.

### Step 5 — Thin pointers for other tools

`AGENTS.md` is the single source of truth. Generate tiny redirects so every tool
lands there (only create ones that fit the project / user's tools):

- `CLAUDE.md` → one line: `See AGENTS.md for all project guidance.`
- `.cursor/rules/agents.mdc` (or `.cursorrules`) → same pointer.

If a real `CLAUDE.md` already exists with content, fold it into `AGENTS.md` and
replace it with the pointer (confirm with user first).

### Step 6 — Report

Summarize: files created, what each is seeded with, and the open TODOs the user
must answer (the judgment-heavy ones). Suggest committing the harness as one
atomic commit.

---

## Mode: update

The repo changed; refresh only what's affected — surgical, not a full rewrite.

### Step 1 — Get the diff

Find what changed since the harness was last touched. Prefer git:

```bash
git diff --stat <since>..HEAD      # <since> = last harness commit or a ref the user gives
git diff <since>..HEAD -- <paths>  # detail for mapping
```

If no clean ref exists, ask the user for the range or compare against the most
recent commit that touched `docs/`.

### Step 2 — Map changed code → affected docs

Use the mapping in `references/doc-catalog.md` (the "update triggers" column).
Typical mappings:

| Changed | Refresh |
|---|---|
| migrations / models / schema | `docs/generated/db-schema.md` |
| routes / controllers / new service | `ARCHITECTURE.md`, `AGENTS.md` index |
| auth / permissions / input handling | `docs/SECURITY.md` |
| error handling / retries / jobs | `docs/RELIABILITY.md` |
| components / pages / styles | `docs/FRONTEND.md`, `docs/DESIGN.md` |
| deps / runtime / build config | `AGENTS.md` quick-start + verification |
| new feature shipped | move plan `exec-plans/active→completed`, update `QUALITY_SCORE.md` |

Only touch docs whose triggers fired.

### Step 3 — Update surgically, then reconcile

Follow the DOX rails (`references/dox.md`): before editing, read the chain from
root to the changed path so you edit the *nearest owning* `AGENTS.md`, not just
the root. For each affected doc: read it, read the changed code, update the
specific stale sections. Don't rewrite untouched parts. Then:

- Update the **nearest owning child `AGENTS.md`** when the change alters that
  subtree's purpose, contracts, or verification.
- If a new durable boundary appeared (new service/package/major dir), create its
  child `AGENTS.md` and add it to the parent's Child DOX Index. If one was
  removed, delete it and its index entry.
- Re-verify the verification commands still exist/pass-able.
- Update the relevant `AGENTS.md` docs index / Child DOX Index if files were
  added or removed.
- If the change invalidates a hard constraint or adds one, edit the constraint
  list (keep ≤15).

### Step 4 — Report what changed and what you left alone

State which docs you updated, and explicitly which you checked but left
unchanged and why (per the harness "report unchanged docs" discipline).

---

## Reference files

- `references/doc-catalog.md` — every harness file: purpose, include-when rule,
  what-to-read-to-fill, and update triggers. **Read this in both modes.**
- `references/templates.md` — skeleton content for each doc. Read when filling.
- `references/dox.md` — the DOX contract-hierarchy rails: when to create a child
  `AGENTS.md`, the child shape, the Child DOX Index, and the read/update
  discipline. **Read this before creating or editing any `AGENTS.md`.**

## Notes

- The `docs/references/*-llms.txt` files are condensed LLM-friendly docs for key
  dependencies (e.g. `uv`, `nixpacks`, a design system). In init, fetch them only
  for the project's *major* detected deps when an `llms.txt` is available; don't
  pad with irrelevant ones.
- Never fabricate. A precise TODO beats a confident wrong answer — wrong docs
  actively mislead the agent and cost more than missing ones.
