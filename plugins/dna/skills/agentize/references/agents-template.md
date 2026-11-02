<!-- when: agentize is creating or restructuring a project's AGENTS.md -->
# AGENTS.md router template

Hard cap 6 KB while tiny. A router points; it does not explain. Fill every placeholder from evidence or drop the line.

```markdown
# AGENTS.md
<!-- dna:layer v1 -->

<One or two sentences: what this project is and who it is for.>

## Start here
1. Read [.agents/status.md](.agents/status.md): the current state, overwritten each session.
2. Open other files only through the routes below.

## Commands
- Build: `<cmd>`   Test: `<cmd>`   Run: `<cmd>`

## Working rules
- <Rules that must always be followed, kept verbatim from the old AGENTS.md. Omit the section if there are none.>

## Routes
| Need | Go to |
|---|---|
| Current state, next step | [.agents/status.md](.agents/status.md) |
| Original AGENTS.md text (if restructured) | [.agents/archive/AGENTS-before-agentize-<date>.md](.agents/archive/AGENTS-before-agentize-<date>.md) |
| Project docs | <links, only to files that exist> |
```

Layout reminder: epics, tasks and handoffs appear under `.agents/` and `.memory/` later, through `save-state`, once the work needs them.
