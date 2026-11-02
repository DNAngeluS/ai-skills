# CLAUDE.md

Claude Code specifics only. The rules for this repo live in **[AGENTS.md](AGENTS.md)** and
apply to you in full; project context, decisions and the skill index are in
**[CONTEXT.md](CONTEXT.md)**.

One rule worth repeating: **write the `CHANGELOG.md` entry as part of the change.** Your work
is done when the entry exists.

## Claude Code specifics

- **Testing a skill:** run `claude --plugin-dir plugins/dna` so edits are live, or install via
  `/plugin marketplace add DNAngeluS/ai-skills`. Invoke with the `Skill` tool or `/dna:<skill>`.
- A skill's real test is whether it *triggers* from a natural request, which depends entirely
  on its `description:` frontmatter.
- Use the `skill-creator` skill to create, refine and evaluate skills here.

## Do not

- Run `npm test` expecting signal: it is a placeholder that exits 1 by design.
- Add build tooling, linters or CI without being asked; this repo is Markdown by intent.
