---
name: plan
description: Turn a goal into a POC-weight plan inside the project's agent context layer: one epic file with a task table and stable ids (EPIC-<slug>, TASK-<epic>-<nn>), task cards only for work that will be delegated, and a status pointer. Drafts first from what the node already says and asks only what blocks. Use whenever the user says "plan this", "make a plan for", "break this into tasks", "create an epic", "phase this work", "what are the steps to", "plan the next phase", "armá un plan", "dividí esto en tareas", or starts a multi-step piece of work that will outlive the session. Not for a single next step; that goes in status.
---

# plan

Write the smallest plan that lets a cold session (or a worker) continue. Plans are state in the layer ([../../references/layer-contract.md](../../references/layer-contract.md): ids, budgets, ownership), not a loose document.

## Rules

- **Draft first.** Read `.agents/status.md`, any related epic, the README and `AGENTS.md`, and check what already exists for the goal (tests, scripts, docs) so the plan builds on it. Ask only what blocks the draft: an unknown goal, or an assumption that would change the task list itself. Everything else goes in the epic's `## Open questions`, each with the default you assumed, so a cold session still sees them.
- **Weight matches the work.** One next step is not an epic: put it in `status.md`. An epic is for two or more separately completable tasks or a plan that outlives the session; one step that touches several files is still one step. Prefer 3-8 tasks; split an epic when it passes about 10. Mark tasks that can run in parallel with the same `Wave` number.
- **Ids are stable.** `EPIC-<kebab-slug>` and `TASK-<epic-slug>-<nn>` (next free two digits). Never renumber; a dropped task is marked `blocked` or removed with a note, not reused.
- **Task cards only when delegating.** The table row is enough for work you will do yourself; the table's `Card` column says which rows have one. A card (`.agents/tasks/TASK-<epic>-<nn>.md`) is a self-contained brief with the contract's fields (goal, needs, touches, gate, done-when) plus steps and report shape, written for a reader with none of this conversation. The epic's table is the source of truth for status; the card's status line is a copy to update with it.
- **Stay in your node and its budgets:** epic under 6 KB, task under 4 KB, every file starts with `<!-- when: ... -->`, absolute dates, status values `todo | in-progress | blocked | done`. Tiny nodes gain `.agents/epics/` and `.agents/tasks/` here, nothing else.
- **No invented facts.** Estimates, owners and dates not given are omitted or marked as a guess. Do not start executing the plan.

## Steps

1. Resolve the node; read as above. If an open epic already has the same goal or the same files, add the new tasks to it (next free numbers, a dated line under Decisions saying why) instead of creating another; a `done` epic is never reopened, start a new one that links it. Write `.agents/` prose in English even if the project is in another language, quoting titles and identifiers verbatim.
2. Draft the epic from [references/epic-template.md](references/epic-template.md): goal, done-criteria (checkable), non-goals, task table, Now/Next/Blocked, a `## Decisions` section if choices were made.
3. For tasks that will be delegated, write the cards. Order tasks by dependency and say what runs in parallel.
4. Update `.agents/status.md`: read it, keep its existing lines, add or replace only the In flight line for this epic (`[EPIC-x](epics/EPIC-x.md) — todo; next: <exact first step>`); a small standalone step goes as one line under In flight. If the session has other state to save, use `save-state`.
5. Validate: `python3 -I ../../scripts/validate_layer.py <node>` (path relative to this skill). Fix FAILs you caused.
6. Report: the epic id, the task table, the open questions with defaults. Commit only if asked.

## Never

- Create `.memory/`, or plans outside `.agents/`.
- Leave a task without an acceptance check.
