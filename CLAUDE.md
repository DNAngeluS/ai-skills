# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Read these first

- **[AGENTS.md](AGENTS.md)** — the canonical, provider-neutral rules for this repo (layout,
  skill-authoring rules, what to update when skills change). All of it applies to you.
- **[CONTEXT.md](CONTEXT.md)** — project context, decisions, and the index of skills.

One rule from AGENTS.md is worth naming here because it applies to every task you finish in
this repo: **write the `CHANGELOG.md` entry as part of the change.** Your work is done when
the entry exists.

This file only holds what is specific to Claude Code; the rest lives in AGENTS.md.

## Claude Code specifics

- **Installing a skill for testing:** symlink it, don't copy, so edits are live —
  `ln -s "$PWD/skills/<name>" ~/.claude/skills/<name>` (user scope) or into
  `.claude/skills/<name>` of the target project. Remove the symlink when done.
- **Invoke** an installed skill with the `Skill` tool or `/<skill-name>`; a skill's real test
  is whether it *triggers* from a natural request, which depends entirely on its
  `description:` frontmatter.
- The `skill-creator` skill (already installed at user scope) is the right tool for creating,
  refining, and evaluating skills here — prefer it over hand-writing scaffolding.
- Some skills in this collection originated as user-scope skills under `~/.claude/skills/`.
  When importing one, move it into `skills/` here and symlink back, so there is one source of
  truth.

## Do not

- Run `npm test` expecting signal — it is a placeholder that exits 1 by design.
- Add build tooling, linters, or CI to this repo without being asked; it is Markdown by intent.
