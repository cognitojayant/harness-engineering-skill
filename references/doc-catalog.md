# Harness Doc Catalog

Every file the harness can contain. In **init**, include a file only if its
**Include when** condition holds. In **update**, refresh a file when its
**Update triggers** fire. The **key** column is what you pass to
`scaffold_tree.py --manifest`.

## Table of contents
- Root files (AGENTS.md, ARCHITECTURE.md)
- docs/ top-level (DESIGN, FRONTEND, PLANS, PRODUCT_SENSE, QUALITY_SCORE, RELIABILITY, SECURITY)
- docs/ subtrees (design-docs, exec-plans, generated, product-specs, research, references)

---

## Root files

### `agents` → `AGENTS.md`
- **Purpose**: Canonical entry / contract. The landing page for any agent. Also
  the root of the DOX contract hierarchy.
- **Include when**: Always (root). Child `AGENTS.md` files are added per durable
  sub-boundary — see `references/dox.md`.
- **Fill from**: Everything in Step 1. Overview, quick-start, verification
  commands, ≤15 hard constraints, linked index of the docs/ tree, and a Child
  DOX Index when the repo has subtree contracts.
- **Update triggers**: any structural change, new/removed doc, dep/build change,
  constraint change, new/removed durable sub-boundary (→ child AGENTS.md + index).

### `architecture` → `ARCHITECTURE.md`
- **Purpose**: Big-picture system shape — services, boundaries, data flow, the
  "why" you'd only get by reading many files.
- **Include when**: Any non-trivial codebase (more than a single script).
- **Fill from**: top-level dirs, entry points, service boundaries, how
  components talk, deployment shape.
- **Update triggers**: new service/module, changed routes, restructured dirs,
  changed cross-component communication.

---

## docs/ top-level files

### `design` → `docs/DESIGN.md`
- **Purpose**: Visual/UX design system, tokens, component patterns.
- **Include when**: Project has a UI / frontend.
- **Fill from**: design tokens, CSS/Tailwind config, component library, existing
  design-system reference.
- **Update triggers**: style system, theme, or component-pattern changes.

### `frontend` → `docs/FRONTEND.md`
- **Purpose**: Frontend architecture — framework, state mgmt, routing, build,
  component conventions.
- **Include when**: A frontend app/package exists.
- **Fill from**: frontend framework + version, state lib, router, bundler,
  directory conventions.
- **Update triggers**: framework/state/router changes, new page/component patterns.

### `plans` → `docs/PLANS.md`
- **Purpose**: Planning hub — how work is planned, links into exec-plans.
- **Include when**: Always (it's the index for exec-plans).
- **Fill from**: existing roadmap/issues if present; otherwise a short
  convention note + pointers to `exec-plans/active|completed`.
- **Update triggers**: planning process changes; new active plan.

### `product_sense` → `docs/PRODUCT_SENSE.md`
- **Purpose**: Product judgment — who the users are, what good looks like, the
  bar for UX decisions.
- **Include when**: User-facing product (not a pure library/tool).
- **Fill from**: README/product copy, onboarding flows, existing specs. Heavy on
  human judgment → expect TODO stubs with pointed questions.
- **Update triggers**: rarely from code; mostly human-driven.

### `quality_score` → `docs/QUALITY_SCORE.md`
- **Purpose**: Living scorecard grading each module/area A–C so sessions fix the
  weakest area first. Core of the "leave a clean state" discipline.
- **Include when**: Always.
- **Fill from**: test coverage signals, lint health, complexity hotspots, areas
  with frequent churn. Seed grades conservatively.
- **Update triggers**: after features ship, after refactors, weekly maintenance.

### `reliability` → `docs/RELIABILITY.md`
- **Purpose**: Failure modes, error handling, retries, timeouts, jobs, health
  checks, observability.
- **Include when**: Backend/services/long-running or job-based code.
- **Fill from**: error-handling patterns, retry/circuit-breaker code, background
  jobs, health endpoints, logging/tracing setup.
- **Update triggers**: changes to error handling, retries, jobs, health checks.

### `security` → `docs/SECURITY.md`
- **Purpose**: Auth model, permissions, input handling, secrets, data exposure
  surface, threat notes.
- **Include when**: Auth, user input, public endpoints, or sensitive data exist.
- **Fill from**: auth middleware, permission checks, input validation, secret
  handling, public API surface.
- **Update triggers**: auth/permission/input-handling/endpoint changes.

---

## docs/ subtrees

### `design_docs` → `docs/design-docs/{index.md, core-beliefs.md}`
- **Purpose**: Long-form design rationale + the project's core engineering
  beliefs/principles.
- **Include when**: Team wants durable design rationale (most non-trivial projects).
- **Fill from**: existing ADRs/design notes; `core-beliefs.md` is largely
  human-authored → TODO stub with prompts.
- **Update triggers**: new architectural decision recorded.

### `exec_plans` → `docs/exec-plans/{active/, completed/, tech-debt-tracker.md}`
- **Purpose**: Execution plans in flight vs done, plus a tech-debt ledger.
- **Include when**: Always (dirs; start empty).
- **Fill from**: open issues/PRs for active; `tech-debt-tracker.md` seeded from
  TODO/FIXME scan + known rough areas.
- **Update triggers**: feature ships → move active→completed; new debt found.

### `generated` → `docs/generated/db-schema.md`
- **Purpose**: Human/agent-readable snapshot of the DB schema.
- **Include when**: A database exists (migrations/models/schema file present).
- **Fill from**: migrations, ORM models, `schema.sql`/`schema.rb`/Prisma. Mark
  the file as generated — regenerate, don't hand-edit.
- **Update triggers**: any migration / model / schema change.

### `product_specs` → `docs/product-specs/{index.md, new-user-onboarding.md}`
- **Purpose**: Feature specs; onboarding flow as the canonical example spec.
- **Include when**: User-facing product with discrete features.
- **Fill from**: existing specs, onboarding flow in code. Stub where vision is
  needed.
- **Update triggers**: new feature spec'd or onboarding flow changes.

### `research` → `docs/research/Research.md`
- **Purpose**: Durable log of research that informed the project — external best
  practices, prior art, library/tool comparisons, spikes, and the conclusions
  drawn. Stops the same investigation being redone every session (an agent that
  can't see past research repeats it and burns context).
- **Include when**: The project involved (or will involve) non-trivial
  investigation — tech selection, design spikes, competitor/prior-art review,
  performance studies. Skip for throwaway/trivial repos.
- **Fill from**: existing research notes, ADR rationale, README "why we chose X"
  sections, comparison tables in comments/docs. Each entry records the question,
  what was found, sources, and the decision — never invent findings; stub the
  question if no research exists yet.
- **Update triggers**: a new investigation/spike is done; a tech decision is
  revisited; a dependency is swapped after evaluation.

### `references` → `docs/references/*-llms.txt`
- **Purpose**: Condensed LLM-friendly docs for key dependencies.
- **Include when**: Project has major deps that publish an `llms.txt`
  (e.g. `uv`, `nixpacks`, a design system).
- **Fill from**: fetch the dep's `llms.txt` when available; one file per major
  dep. Don't pad with irrelevant ones.
- **Update triggers**: major dep added/removed/upgraded across a major version.
