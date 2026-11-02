<!-- when: plan is writing or extending an epic file or a task card -->
# Epic and task templates

```markdown
<!-- when: working on <topic>; the plan, task table and decisions for EPIC-<slug> -->
# EPIC-<slug> — <title>
**Status:** todo | in-progress | blocked | done · **Opened:** <YYYY-MM-DD>

**Goal:** <one sentence>
**Done when:** <checkable criteria, bullets>
**Not in scope:** <bullets>

| Task | Title | Status | Wave | Depends on | Card | Note |
|---|---|---|---|---|---|---|
| TASK-<slug>-01 | <title> | todo | 1 | - | yes/no | <one line> |

## Now / Next / Blocked
- Now: <exact next step>
- Next: <ordered>
- Blocked: <item and what unblocks it>

## Open questions
1. <question> — default assumed: <...>

## Decisions
- <YYYY-MM-DD> <decision and why; what was rejected>
```

Task card (only for delegated work), under 4 KB:

```markdown
<!-- when: executing TASK-<slug>-<nn>; the self-contained brief -->
# TASK-<slug>-<nn> — <title>
**Status:** todo · **Epic:** [EPIC-<slug>](../epics/EPIC-<slug>.md)
**Goal and why:** ...
**Needs:** <inputs, earlier tasks, context the reader lacks>
**Touches:** <files/dirs it may change; everything else is off limits>
**Steps:** 1. ...
**Gate:** <command or check that must pass before reporting done>
**Done when:** <observable result>
**Report shape:** <what to return, how long>
```
