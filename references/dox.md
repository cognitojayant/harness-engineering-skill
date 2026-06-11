# DOX — the AGENTS.md contract hierarchy

DOX makes the harness a *tree of contracts* instead of one big file. Each
`AGENTS.md` is binding for its subtree. Any file must be understandable from its
nearest `AGENTS.md` plus every parent `AGENTS.md` above it. This is the same
"repo is the single source of truth" principle, applied recursively so large
repos stay legible.

## When to create a child AGENTS.md

Create one when a directory is a **durable boundary** — it has its own purpose,
rules, ownership, workflow, or verification. Typical triggers:

- a service / app / package in a monorepo (`services/api/`, `apps/web/`)
- a major module with distinct conventions (`workers/`, `infra/`, `migrations/`)
- a subtree whose verification differs from the rest (its own test/lint command)

**Do not** create one for every folder. A directory that's just code following
the parent's rules needs no child doc — a spurious child is dead weight that
dilutes signal (Lecture 4). When unsure, leave it to the parent.

## Child AGENTS.md shape

Default section order (drop a section if it has nothing real to say — empty
headings are noise):

```markdown
# <subtree name>

## Purpose
What this subtree is and why it exists.

## Ownership
Who/what owns it; what stays owned by the parent vs decided locally.

## Local Contracts
The binding rules for working here — conventions, invariants, patterns specific
to this subtree. These refine (never weaken) the parent's rules.

## Work Guidance
Current standards / how to do work here. Leave empty if none yet.

## Verification
The exact commands that prove work here is correct. Leave empty if none exist.

## Child DOX Index
- <child-dir>/AGENTS.md — what it covers
(omit if this subtree has no children)
```

## Root AGENTS.md additions

The root stays the canonical harness entry (overview, quick-start, verification,
≤15 hard constraints, docs index). On top of that it carries the top-level
**Child DOX Index**:

```markdown
## Child DOX Index
- services/api/AGENTS.md — HTTP API service, owns request/response contracts
- apps/web/AGENTS.md — Next.js frontend, owns UI conventions
- packages/core/AGENTS.md — shared domain logic
```

The index explains what each direct child covers and what stays owned by the
root. A child with its own children repeats the pattern one level down.

## The rails (apply in both init and update)

**Read before editing.** Walk from the repo root to the path you're about to
touch and read every `AGENTS.md` on the way. The nearest one is the local
contract; parents hold repo-wide rules. If docs conflict, the closer doc controls
local detail — but no child may weaken a root-level rule.

**Update after editing.** After a change, update the **nearest owning**
`AGENTS.md` if the change affected purpose, scope, contracts, workflow,
verification, or structure. Update parent docs when parent-level structure or the
child index changed. Refresh every affected Child DOX Index. Remove stale or
contradictory text immediately — don't leave history behind.

**Closeout.** Re-check changed paths against the DOX chain, update nearest owners
and affected parents/children, refresh indexes, delete stale text, and report any
doc you intentionally left unchanged and why.

## Relationship to the docs/ tree

The `docs/` files (SECURITY, RELIABILITY, ARCHITECTURE, etc.) are repo-wide
concerns owned by the **root** contract. Child `AGENTS.md` files cover
**subtree-local** concerns. A child may link to a docs/ file for a repo-wide rule
rather than restating it — don't duplicate the same rule across many files unless
each scope genuinely needs its own version.
