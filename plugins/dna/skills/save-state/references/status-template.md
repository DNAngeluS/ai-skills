<!-- when: save-state is writing or rewriting .agents/status.md -->
# status.md template

Overwrite the whole file every time. Hard cap 4 KB (about 1,000 tokens): one screen. Bullets are one line each; detail belongs in the epic they point to.

```markdown
<!-- when: start of any session in <node>; the current state, overwritten each save -->
# Status — <YYYY-MM-DD>

**Goal now:** <one sentence>
**Stage:** <tiny | standard | mature | domain> · **Branch/head:** <branch @ short-hash>, <clean | N uncommitted | N unpushed>

## In flight
- [EPIC-<slug>](epics/EPIC-<slug>.md) — <state in one line>; next: <exact next step>

## Blocked
- <item> — waiting on <what/who>

## Open questions (need the user)
1. <question>

## Last session (<YYYY-MM-DD>)
- <what changed, with commit hashes; 3 bullets max>
```

For a **domain**, replace "In flight" with one row per child: `| <child> | <state> | <epic pointer> | <date> |`. Link to the child's own status; never copy its plans.

Omit empty sections rather than writing "none". Do not append a dated log: the previous "Last session" is simply replaced, since git and the epics keep history.
