# AGENTS.md

Canonical rules for **any** LLM agent (Claude Code, Codex, Gemini CLI, Cursor, …) working in
this repository. Provider-specific files (`CLAUDE.md`, `GEMINI.md`, `.cursorrules`) must not
restate these rules — they point here.

## What this repo is

A curated collection of **AI skills**: portable, self-contained instruction packages that get
loaded into an agent's context on demand. It is a content repository, not an application.
There is no build, no runtime, no dependency tree. `package.json` exists only for metadata and
publishing; its `test` script is a placeholder — do not treat a failing `npm test` as a
regression.

Read `CONTEXT.md` before doing substantive work; it holds the project's decisions and the
index of what lives here.

## Layout

```
plugins/<prefix>/                 # prefix = domain: dna, pla, ... (khem is NOT here)
  .claude-plugin/plugin.json
  skills/<skill-name>/
    SKILL.md        # required — frontmatter + instructions
    references/     # optional — templates, per-tool guides, long docs
    scripts/        # optional — executable helpers
    evals/          # optional — evals.json + fixtures
.claude-plugin/marketplace.json   # lists every plugin; third-party ones use source: github
```

Skills are invoked as `/<prefix>:<skill-name>`, so skill names carry no prefix themselves.
One skill per directory. Directory name == `name:` in the frontmatter == kebab-case.

## Authoring rules

- **Frontmatter is mandatory** in every `SKILL.md`:
  ```yaml
  ---
  name: kebab-case-name
  description: What it does, then when to use it — include the literal phrases a user
    would say to trigger it. This is the only text an agent sees before loading the skill,
    so it must carry all the triggering signal.
  ---
  ```
- **Write for an agent, not a reader.** Imperative instructions, explicit workflows, stated
  failure modes. No marketing prose, no "as an AI" framing.
- **Keep `SKILL.md` short and load the rest lazily.** Aim under ~500 lines; push templates,
  tool-specific detail, and long examples into `references/` and link to them so they are
  only read when needed.
- **Stay provider-neutral.** Do not hardcode Claude-only tool names, MCP server names, or
  file paths in a skill's instructions unless the skill is inherently about that tool — and
  if so, say which tool it requires up front.
- **Never invent facts.** Skills that inspect a project must be grounded in that project's
  own files, docs, and git history. If information is missing, the skill should instruct the
  agent to ask rather than fill the gap.
- **No secrets, no client-confidential material.** This repo is public. Use placeholders
  (`[ClientName]`, `[ProjectName]`) and, for NDA work, industry descriptors instead of names.

## Changing this repo

Three files carry the record, each with one job. Keep them in their lanes:

| File | Holds |
|---|---|
| `CHANGELOG.md` | **What** changed and **when** — every change, dated, newest first |
| `CONTEXT.md` | **Why** — decisions, trade-offs, what was tried and rejected; plus the skill index |
| `README.md` | How a human uses the repo |
| `ROADMAP.md` | What to build next, with evidence; the queue for per-skill sessions |

- **Every change lands with its `CHANGELOG.md` entry, written in the same change.** This is
  mandatory and applies to all of them — new or edited skills, doc changes, layout changes,
  tooling. Add to `## [Unreleased]` under `Added` / `Changed` / `Removed` / `Fixed`; open a
  dated version section when a version ships. Write the entry from the work you actually did,
  and say plainly what you left undone. **The task is finished when the entry exists** — a
  change without one is incomplete, not merely untidy.
- When you add, rename, or remove a skill, update the index in `CONTEXT.md` in the same
  change. A skill that is not indexed is considered missing.
- Record non-obvious decisions (why a skill is structured a certain way, what was tried and
  rejected) in `CONTEXT.md` — the changelog entry links to them rather than restating them.
- Editing an existing skill: preserve its section structure if other skills or people depend
  on its output shape. Change the content, not the contract.
- Prefer editing a skill in place over forking a near-duplicate. Two skills with overlapping
  `description:` fields degrade triggering accuracy for both.

## Installing / testing a skill

Skills are used by symlinking or copying a skill directory into the agent's skills path
(for Claude Code: `~/.claude/skills/<name>` for user scope, `.claude/skills/<name>` for a
project). Verify a change by installing the skill and invoking it on a real task — there is
no unit-test harness. Skills with an `evals/` directory carry their own eval cases; run them
with whatever eval tooling the skill documents.
