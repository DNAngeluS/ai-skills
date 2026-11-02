# Changelog

Timeline of what changed in this repo. Newest first. Every change lands here in the same
commit that makes it — see the changelog rule in [AGENTS.md](AGENTS.md#changing-this-repo).

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Dates are `YYYY-MM-DD`.
Entries record **what changed**; the reasoning behind a decision goes in
[CONTEXT.md](CONTEXT.md#decisions), linked from the entry when it matters.

## [Unreleased]

### Added

- `.gitignore`: excludes the owner's installed third-party skills (`.agents/skills/`, `.claude/`,
  `skills-lock.json`) per the no-vendoring decision; first commit of the repo.
- Skills `dna:status` (read-only recall) and `dna:save-state` (write half, with `references/routing.md`
  and `references/status-template.md`), draft. Tested by three independent subagents on scratch
  copies (Crytek layer for status; a tiny POC and a standard project with a real commit for
  save-state); their feedback was folded into both SKILL.md files (tiny quick path, epic
  threshold, domain handling, validator summary, budget-overflow rule). Description trigger loops
  (3 iterations each) gave NO signal: every positive query scored 0/3 triggers in all iterations,
  so the original descriptions are kept and the proposed rewrites were not applied. Not done:
  a working trigger measurement, hooks. Decision on commits in CONTEXT.md. Removed
  `plugins/dna/skills/.gitkeep`.

### Added

- `plugins/dna/references/layer-contract.md`: the dna layer contract (file set, ownership,
  byte budgets, growth stages tiny/standard/mature/domain, read/write rules, hook limits,
  token-cost rationale). Every project carries its own `AGENTS.md` and `.agents/`; `.memory/`
  appears when it grows. Decisions in CONTEXT.md. Not done: no skill or hook written; the
  workspace `~/Code/AGENTS.md` §2 amendment is outside this repo.
- `plugins/dna/scripts/validate_layer.py`: stdlib-only, read-only validator (budgets, `when:`
  headers, naming, index coverage, stage detection, `--legacy`, `--json`). Run against Crytek
  (fails on its 24 KB status file, as intended), AI/prompt-spine and a tiny fixture.

### Changed

- Repo moved from `~/Code/dnangelus/ai-skills` to `~/Code/dna/ai-skills`; `dnangelus/` removed.
  Layout is now `plugins/<prefix>/skills/<skill>/` (was top-level `skills/`). `AGENTS.md` and
  `CONTEXT.md` updated; decisions in CONTEXT.md. Workspace `CLAUDE.md` and `.memory/INDEX.md`
  paths fixed. README still describes the old layout (not updated yet).

### Added

- `ROADMAP.md`: resolved decisions, build order (layer contract first) and the Session 0 brief.
- Marketplace scaffold: `.claude-plugin/marketplace.json` (plugins `dna` and third-party
  `mattpocock-skills` via `source: github`) and `plugins/dna/.claude-plugin/plugin.json`. No
  skills written yet; `plugins/dna/skills/` is empty. `pla` plugin deliberately not created yet.
- `ROADMAP.md` — ten candidate skills ranked from mining 1,432 prompts of past sessions, plus
  working-style notes and open questions. Draft, not yet confirmed by owner.
- `CHANGELOG.md` — this file, backfilled with the repo's history to date.
- Changelog upkeep is now a repo rule in `AGENTS.md`: a change is incomplete until its entry
  is written.

## [0.0.1] — 2026-08-18

Repo initialized as a blank sheet: a place to collect the AI skills in daily use, with one
source of truth across agents and machines.

### Added

- `package.json` — metadata only (name `ai-skills`, MIT, repo `DNAngeluS/ai-skills`,
  `main: AGENTS.md`). No build, no dependencies; the `test` script is a placeholder that
  exits 1 by design.
- `AGENTS.md` — canonical provider-neutral rules: the `skills/<name>/SKILL.md` +
  `references/` / `scripts/` / `evals/` layout, mandatory frontmatter, keep `SKILL.md` short
  and lazy-load the rest, stay provider-neutral, ground skills in a project's own files, no
  client-confidential material, and index every skill you add.
- `CONTEXT.md` — purpose, dated decisions log, the skill index table (empty at creation), the
  list of user-scope skills that are candidates to migrate in, and open questions.
- `CLAUDE.md` — thin Claude Code pointer to `AGENTS.md`, plus Claude-only mechanics:
  symlink-don't-copy for live testing, `/<skill-name>` invocation, `skill-creator` for
  scaffolding.
- `README.md` — human-facing entry point: what a skill is, install-by-symlink commands, how to
  add one, license.
- `skills/` — empty directory awaiting the first migrated skill.

### Decided

- Multi-agent by default: rules live in `AGENTS.md`, provider files are thin pointers.
- Four root docs with distinct audiences (agents / Claude / project context / humans).
- Skills are directories, not single files, so they symlink into an agent's skills path
  unmodified.

Full reasoning: [CONTEXT.md § Decisions](CONTEXT.md#decisions).

### Not done

- No git repository initialized yet, despite `package.json` naming a GitHub remote.
- `khem-project-docs` and `plan-to-board` still live only at user scope under
  `~/.claude/skills/`; migration is pending a scrub of client-facing material.
