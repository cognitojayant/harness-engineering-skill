# harness-engineering

A Claude Code [skill](https://docs.claude.com/en/docs/claude-code/skills) that
**scaffolds and maintains a documentation harness** for AI-agent codebases
(Claude Code, Codex, Cursor).

It turns a repo into a single source of truth that coding agents can actually
work from — generating an `AGENTS.md` plus an adaptive `docs/` tree, all filled
from real repo analysis, and keeping it in sync as the code changes.

## Why

Coding agents fail less from weak models than from a weak *harness* — the docs,
conventions, and verification context that live in the repo. An agent can't see
Slack, a wiki, or a teammate's head: **if it isn't in the repo, it doesn't exist
for the agent.** This skill builds that harness and stops it from rotting.

## What it produces

```
AGENTS.md                      # canonical entry + DOX rail (≤200 lines)
ARCHITECTURE.md
CLAUDE.md / .cursor/rules/…     # thin pointers → AGENTS.md (one source of truth)
docs/
├── SECURITY.md  RELIABILITY.md  QUALITY_SCORE.md  PLANS.md
├── DESIGN.md  FRONTEND.md  PRODUCT_SENSE.md        # frontend/product only
├── design-docs/{index,core-beliefs}.md
├── exec-plans/{active,completed}/  tech-debt-tracker.md
├── generated/db-schema.md                          # if a DB exists
├── product-specs/{index,new-user-onboarding}.md
├── research/Research.md                            # if research-driven
└── references/*-llms.txt                           # condensed dep docs
<service>/AGENTS.md            # DOX child contracts per durable boundary
```

The doc set is **adaptive** — a backend repo gets no `FRONTEND.md`; a repo with
no DB gets no `db-schema.md`; a flat repo gets no child `AGENTS.md`. Empty,
irrelevant files are dead weight that bury real signal, so the skill doesn't
create them.

## Two modes

- **init** — analyze a repo with no harness and scaffold the full tree, filled
  with verified content (detected stack, real schema, real verification commands).
- **update** — read the git diff since the harness was last touched, map changed
  files to affected docs, and refresh only those — surgically.

## Design principles

1. **Repo is the single source of truth.** Never invent facts; unverifiable
   things become explicit `TODO`s, not confident guesses.
2. **Adaptive & lean.** Each doc earns its place.
3. **Verification beats prose.** Docs name the command that proves a claim.
4. **DOX contract hierarchy.** Root `AGENTS.md` is the rail; durable
   sub-boundaries get their own child contract with a Child DOX Index. A doc
   closer to the code is more specific; parents hold repo-wide rules.
5. **Don't let docs drift.** Update mode exists because entropy is the default.

## Layout

| Path | Purpose |
|------|---------|
| `SKILL.md` | The skill: init + update workflows, principles |
| `references/doc-catalog.md` | Every doc: purpose, include-when, fill-from, update-triggers |
| `references/templates.md` | Skeleton content for each doc |
| `references/dox.md` | The DOX contract-hierarchy rails |
| `scripts/scaffold_tree.py` | Creates the directory structure (dirs only; agent writes the files) |
| `evals/evals.json` | The test prompts the skill was benchmarked against |

## Install

Clone into your Claude Code skills directory:

```bash
git clone <this-repo> ~/.claude/skills/harness-engineering
```

Then in Claude Code, ask it to make a repo agent-ready, or set up `AGENTS.md` /
agent docs — the skill triggers automatically.

## Status

Benchmarked against init (backend / frontend / monorepo) and update scenarios:
with-skill runs passed 100% of assertions vs ~53% for an unaided baseline, with
the largest gap on monorepos (DOX hierarchy + research log).
