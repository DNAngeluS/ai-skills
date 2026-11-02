# CONTEXT.md

Project context for **ai-skills**. Everything an agent or a human needs to know that is not
derivable from the files themselves. Rules live in [AGENTS.md](AGENTS.md); this is the *why*
and the *what's here*.

## Purpose

A personal, curated collection of AI skills used day to day — some written from scratch, some
gathered and adapted. The repo exists so these skills have one source of truth instead of
living only inside a single agent's config directory, and so they can be shared across
providers and machines.

Owner: DNAngeluS (dev@khemlabs.com). License: MIT. Repo:
https://github.com/DNAngeluS/ai-skills

## Decisions

*(dated; append, don't rewrite history)*

- **2026-08-18 — Multi-agent by default.** Rules go in `AGENTS.md`, not `CLAUDE.md`. Any
  provider-specific file is a thin pointer to it. Reason: the same skills are used from more
  than one agent/provider, and forking rules per provider guarantees drift.
- **2026-08-18 — Four root docs, distinct audiences.** `AGENTS.md` = rules for LLMs.
  `CLAUDE.md` = Claude Code pointer + Claude-only mechanics. `CONTEXT.md` = project context +
  skill index. `README.md` = humans using or browsing the repo.
- **2026-08-18 — `package.json` is metadata only.** No build, no test runner, no deps. `main`
  points at `AGENTS.md` because the rules are the entry point of this package.
- **2026-08-18 — Changelog upkeep is mandatory, and split from this file.** `CHANGELOG.md`
  records *what* changed and *when*; the decisions log below records *why*. Reason: agents
  work here across sessions and providers with no shared memory, and a dated timeline is the
  cheapest way for the next one to see what state the repo is in. Making it a hard rule rather
  than a habit is deliberate — an optional changelog decays into a stale one.
- **2026-08-18 — Skills are directories, not single files.** `skills/<name>/SKILL.md` plus
  optional `references/`, `scripts/`, `evals/`, matching the convention the installed skills
  already use, so a skill can be symlinked into an agent's skills path unmodified.

- **2026-11-01 — Repo becomes the DNAngeluS skills marketplace.** Lives at `~/Code/dna/ai-skills`
  (moved from `~/Code/dnangelus/`, which is gone; `dna/` is the brand domain). Repo name stays
  `ai-skills` for now. Prefix = domain = Claude plugin (`dna`, later `pla`), invoked `/dna:<skill>`.
- **2026-11-01 — Public, generic only.** No third-party code or licenses, no client data, no
  CRYENGINE data. `pla` skills are tooling-shaped and engine-data-free.
- **2026-11-01 — Khem stays out.** It has its own marketplace (`khemlabs/khem-marketplace`).
  `dna` skills may be lighter re-derivations of khem's domain-init/agentize for POC/research work.
- **2026-11-01 — Third-party skills via `source: github`, not vendoring.** Same mechanism khem
  uses for `mattpocock-skills`; updates come with the plugin update, no second remote needed.
  The local `.agents/skills/` copies + `skills-lock.json` are the owner's installed set, not the
  marketplace content.
- **2026-11-01 — Skills are built one per session**, long-thought, from `ROADMAP.md`.

- **2026-11-01 — Roadmap ranking confirmed.** Ten candidates in `ROADMAP.md` accepted as the queue,
  including the additions `status`, `handoff`, `ship`.
- **2026-11-01 — `.agents/status.md` is the single status file** for every domain and project.
  All dna skills read and write it; none invents another.
- **2026-11-01 — Skills write directly, in one consistent form.** No propose-then-apply step.
  Safety comes from the fixed layout contract and from git (commits are the undo), not from
  confirmation prompts.
- **2026-11-01 — Hooks are in scope**, alongside skills (e.g. SessionStart reads the index,
  PreCompact/Stop triggers save-state). Goal: one consistent, token-efficient system that scales
  from a tiny POC to a complex multi-project domain as it evolves. Plugins can ship hooks, so
  they live in `plugins/dna/hooks/`.

- **2026-11-01 — Layer contract defined** (`plugins/dna/references/layer-contract.md`). Every
  node (project or domain) has its own `AGENTS.md` + `.agents/`; `.memory/` only from the
  mature stage. Budgets in bytes (a "one line per epic" status was 24 KB), session-start set
  capped at 12 KB. `status.md` is overwrite-only; history goes to git/changelog/epics.
  Handoffs: one living file per epic; directional `to-`/`from-` files archived by the receiver.
  Hooks: SessionStart read-only; PreCompact/Stop only remind, never write unattended. Contract
  overrides workspace §2 for per-node `.agents/`. Growth is signalled by the validator, never
  automatic. JSON shards optional at domain stage.

- **2026-11-02 — save-state commits only on request.** ROADMAP listed "commits" as part of
  save-state; that conflicted with the standing no-unrequested-commits rule. Resolved: it writes
  and shows the diff, and commits (layer files only) when the prompt says so. `status` is strictly
  read-only and reports staleness instead of fixing it.

## Skill index

Skills live in `skills/<name>/`. Keep this table in sync — adding a skill without indexing it
here counts as an incomplete change.

| Skill | Status | Purpose | Requires |
|---|---|---|---|
| `dna:status` | draft | Read-only recall of a project/domain state from the layer (`plugins/dna/skills/status`) | layer contract |
| `dna:save-state` | draft | Lands session results into status/epic/handoff/memory; commits only on request (`plugins/dna/skills/save-state`) | layer contract |
| `dna:handoff` | draft | Write/consume living and directional handoffs in `.agents/handoffs/`; single writer, receiver archives (`plugins/dna/skills/handoff`) | layer contract |
| `dna:agentize` | draft | Add the tiny layer to an existing project: router AGENTS.md (original archived), CLAUDE.md pointer, seeded status (`plugins/dna/skills/agentize`) | layer contract |
| `dna:domain-init` | draft | Domain layer for a folder of projects: status table, child cards, index; read-only on children (`plugins/dna/skills/domain-init`) | layer contract, agentize |

Build order for the rest: [ROADMAP.md](ROADMAP.md). Plugins: `dna`, ext `mattpocock-skills`.

**Status values:** `active` (in daily use), `draft` (works, still being shaped),
`archived` (kept for reference, not installed).

## Candidates to migrate

Skills currently living only at user scope (`~/.claude/skills/`) that belong here:

- `khem-project-docs` — generates Khem Labs ProjectContext / MarketingContext docs from a
  codebase. Has `references/` templates. **Contains client-facing framing — scrub any client
  names before committing** (see the no-secrets rule in AGENTS.md).
- `plan-to-board` — turns a project's plan/task docs into an Epics→Stories board in
  Jira/Linear/Asana. Has `references/jira.md` and `evals/evals.json`.

`plan-to-board-workspace/` at user scope is eval scratch output, not a skill — do not migrate.

## Open questions

- Repo rename (`ai-skills` → something marketplace-shaped) — deferred; renaming changes the
  install URL.
- Whether an install script (`bin/install <skill>`) is worth adding once there are enough
  skills to make manual symlinking tedious.
