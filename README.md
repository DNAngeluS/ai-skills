# ai-skills

A collection of AI skills I use day to day — portable instruction packages that agents like
Claude Code, Codex, and Gemini CLI load on demand to do a specific job well.

A **skill** is just a folder with a Markdown file. No install step, no runtime, no
dependencies. The agent reads it when the task matches, and ignores it otherwise.

## What's in here

| File | For |
|---|---|
| [AGENTS.md](AGENTS.md) | The rules agents follow in this repo — layout, authoring standards |
| [CONTEXT.md](CONTEXT.md) | Project context, decisions, and the index of every skill |
| [CLAUDE.md](CLAUDE.md) | Claude Code-specific notes (points at AGENTS.md for the rest) |
| [CHANGELOG.md](CHANGELOG.md) | Dated timeline of everything that has changed here |
| `skills/` | The skills themselves, one directory each |

The current list of skills, with status and purpose, is the index table in
**[CONTEXT.md](CONTEXT.md#skill-index)**.

## Using a skill

Point your agent at the skill directory. For Claude Code:

```bash
# user scope — available in every project
ln -s "$PWD/skills/<skill-name>" ~/.claude/skills/<skill-name>

# or project scope — available only in one project
ln -s "$PWD/skills/<skill-name>" /path/to/project/.claude/skills/<skill-name>
```

Then just describe your task normally — a well-written skill triggers on its own. You can also
invoke it explicitly with `/<skill-name>`.

Other agents: copy or symlink the directory into whatever path that tool reads skills from.
The `SKILL.md` format is deliberately plain Markdown with YAML frontmatter, so it travels.

## Adding a skill

1. Create `skills/<kebab-case-name>/SKILL.md` with `name` and `description` frontmatter.
2. Put templates and long reference material in `skills/<name>/references/` so the main file
   stays short.
3. Add a row to the index table in `CONTEXT.md`.
4. Add an entry under `## [Unreleased]` in `CHANGELOG.md` — required for every change, not
   just new skills.
5. Symlink it in and try it on a real task — that's the only test that matters.

Full authoring rules: [AGENTS.md](AGENTS.md).

## License

MIT. Some skills were adapted from work by others; see `CONTEXT.md` for attribution notes.
