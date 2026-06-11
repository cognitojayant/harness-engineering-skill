# Doc Templates

Skeletons for each harness file. These are *starting shapes*, not rigid forms —
adapt headings to the project. Fill every section with verified content from
repo analysis; use `<!-- TODO: question -->` only where a fact genuinely needs
human judgment. Keep each file lean.

---

## AGENTS.md (canonical entry — keep ≤200 lines)

```markdown
# <Project Name>

<One sentence: what this project is.>

## Quick start
\`\`\`bash
<install>
<run dev>
\`\`\`

## Verify
\`\`\`bash
<test>        # how to run the full suite
<test-one>    # how to run a single test
<lint>
<typecheck>
<build>
\`\`\`

## Hard constraints (max 15 — the rules an agent must never break)
- <constraint>
- ...

## Architecture (one paragraph + pointer)
<2–3 sentences.> See ARCHITECTURE.md for detail.

## Docs index
- ARCHITECTURE.md — system shape
- docs/SECURITY.md — auth, permissions, data surface
- docs/RELIABILITY.md — failure modes & error handling
- docs/QUALITY_SCORE.md — module health grades
- docs/exec-plans/ — active & completed work, tech-debt-tracker.md
- docs/generated/db-schema.md — DB schema snapshot
- <only list files that exist>
```

> Put the most critical constraints at the **top or bottom** — middle content
> gets under-used by models ("lost in the middle").

---

## ARCHITECTURE.md

```markdown
# Architecture

## Stack
<languages, frameworks, runtimes — with detected versions>

## Services / modules
<each top-level unit: what it does, where it lives>

## Data flow
<how a request / job moves through the system>

## External dependencies
<datastores, queues, third-party APIs>

## Deployment shape
<how it builds & runs in prod, from Dockerfile/nixpacks/CI>
```

---

## docs/SECURITY.md

```markdown
# Security

## Authentication
<mechanism, where enforced — cite the middleware/path>

## Authorization
<permission model, roles, checks>

## Input handling
<validation/sanitization boundaries>

## Secrets
<how secrets are loaded; never commit them>

## Exposure surface
<public endpoints, data that leaves the system>
```

---

## docs/RELIABILITY.md

```markdown
# Reliability

## Failure modes
<what breaks, where>

## Error handling
<patterns, where errors are caught/propagated>

## Retries & timeouts
<policies, cite code>

## Background jobs / async
<queues, workers, idempotency>

## Health & observability
<health checks, logging, tracing>
```

---

## docs/FRONTEND.md

```markdown
# Frontend

## Framework & build
<framework + version, bundler, entry>

## State management
<lib + patterns>

## Routing
<router + structure>

## Component conventions
<where components live, naming, patterns>
```

---

## docs/DESIGN.md

```markdown
# Design

## Design tokens
<colors, spacing, type scale — from config>

## Components
<library / patterns>

## Interaction & motion
<conventions>

<!-- TODO: any brand/visual principles not encoded in config -->
```

---

## docs/QUALITY_SCORE.md

```markdown
# Quality Score

Grades each area A (solid) · B (okay) · C (weak — fix first). Update after
shipping and during maintenance.

| Area | Grade | Notes / weakest points |
|------|-------|------------------------|
| <module> | B | <why> |

## Fix-first queue
1. <lowest-graded area + why>
```

---

## docs/PLANS.md

```markdown
# Plans

How work is planned here. Active and completed execution plans live in
docs/exec-plans/. Tech debt is tracked in docs/exec-plans/tech-debt-tracker.md.

## Active
<links into exec-plans/active/>

## Conventions
<how a plan is written / promoted to completed>
```

---

## docs/PRODUCT_SENSE.md  &  docs/product-specs/

```markdown
# Product Sense

## Who uses this
<!-- TODO: describe the primary users -->

## What "good" looks like
<!-- TODO: the UX/quality bar for product decisions -->

## Non-goals
<!-- TODO: what we deliberately don't do -->
```

`product-specs/index.md`: list of specs. `new-user-onboarding.md`: the
onboarding flow as the canonical example spec (fill from the real flow in code;
stub the intent).

---

## docs/design-docs/

`index.md`: list of design docs / ADRs.
`core-beliefs.md`:

```markdown
# Core Beliefs

Engineering principles this project holds (and why).

<!-- TODO: capture the team's actual beliefs — e.g. "boring tech",
     "tests gate merges", "optimize for deletion". -->
```

---

## docs/exec-plans/

- `active/` — one file per in-flight plan (start empty).
- `completed/` — finished plans (start empty).
- `tech-debt-tracker.md`:

```markdown
# Tech Debt Tracker

| Item | Location | Severity | Notes |
|------|----------|----------|-------|
| <debt> | <path> | high/med/low | <context> |
```

(Seed from a TODO/FIXME scan + known rough areas.)

---

## docs/research/Research.md

```markdown
# Research Log

Investigations that shaped this project. Newest first. Each entry: the question,
what was found, sources, and the decision it drove. This exists so a fresh agent
session inherits prior research instead of repeating it.

## <YYYY-MM-DD> — <question / topic>
**Question:** <what was being decided>
**Findings:** <key facts, options compared, tradeoffs>
**Sources:** <links / files / docs consulted>
**Decision:** <what was chosen and why> (→ see DESIGN.md / ADR if applicable)

<!-- TODO: seed from existing research notes, "why we chose X" sections, and
     comparison tables. If none exist yet, leave this header as the template
     for the first entry — do not fabricate findings. -->
```

---

## docs/generated/db-schema.md

```markdown
# DB Schema (generated — do not hand-edit)

Source: <migrations dir / schema file>. Regenerate after schema changes.

## <table>
| Column | Type | Constraints |
|--------|------|-------------|
| ... | ... | ... |

Relationships: <FKs, joins>
```
