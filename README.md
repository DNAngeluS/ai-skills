# ai-skills

A collection of AI skills I use day to day — portable instruction packages that agents like
Claude Code, Codex, and Gemini CLI load on demand to do a specific job well.

A **skill** is just a folder with a Markdown file. No install step, no runtime, no
dependencies. The agent reads it when the task matches, and ignores it otherwise.

## What's in here

| Path | For |
|---|---|
| [AGENTS.md](AGENTS.md) | The rules agents follow in this repo: layout, authoring standards |
| [CONTEXT.md](CONTEXT.md) | Project context, decisions, and the index of every skill |
| [CLAUDE.md](CLAUDE.md) | Claude Code-specific notes (points at AGENTS.md for the rest) |
| [CHANGELOG.md](CHANGELOG.md) | Dated timeline of everything that has changed here |
| [ROADMAP.md](ROADMAP.md) | What is built and what is queued |
| `.claude-plugin/marketplace.json` | The `dnangelus` marketplace manifest |
| `plugins/dna/` | The `dna` plugin: `skills/`, `hooks/`, `references/layer-contract.md`, `scripts/validate_layer.py` |

The current list of skills, with status and purpose, is the index table in
**[CONTEXT.md](CONTEXT.md#skill-index)**.

## The dna layer

`dna` gives a project or a folder of projects a small, predictable agent context layer
(`AGENTS.md` router, `.agents/status.md`, optional epics, handoffs and `.memory/`) so a new
session resumes from files, not chat. Skills: `/dna:status`, `/dna:save-state`, `/dna:handoff`,
`/dna:agentize`, `/dna:domain-init`. Hooks are opt-in: they act only where `AGENTS.md` carries
`<!-- dna:layer v1 -->`. The rules are in [the layer contract](plugins/dna/references/layer-contract.md).

## Using it

```bash
# in Claude Code
/plugin marketplace add DNAngeluS/ai-skills
/plugin install dna@dnangelus

# or try the plugin straight from a checkout
claude --plugin-dir plugins/dna
```

Then describe your task normally: a well-written skill triggers on its own, or call it as
`/dna:<skill>`. Other agents: the `SKILL.md` files are plain Markdown with YAML frontmatter,
so copy or symlink a skill directory into whatever path that tool reads.

## Adding a skill

1. Create `plugins/dna/skills/<kebab-case-name>/SKILL.md` with `name` and `description` frontmatter.
2. Put templates and long reference material in `plugins/dna/skills/<name>/references/` so the main file
   stays short.
3. Add a row to the index table in `CONTEXT.md`.
4. Add an entry under `## [Unreleased]` in `CHANGELOG.md` — required for every change, not
   just new skills.
5. Try it on a real task with `claude --plugin-dir plugins/dna`: that's the only test that matters.

Full authoring rules: [AGENTS.md](AGENTS.md).

## License

MIT. Some skills were adapted from work by others; see `CONTEXT.md` for attribution notes.
