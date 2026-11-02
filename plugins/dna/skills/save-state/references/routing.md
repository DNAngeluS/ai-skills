<!-- when: save-state needs to decide which layer file a fact from the session belongs in -->
# Routing facts to layer files

| Fact from the session | Destination | Form |
|---|---|---|
| Where the node stands right now, next step, blockers, open questions | `.agents/status.md` | overwrite whole, ≤4 KB, dated |
| Progress on a planned body of work | `.agents/epics/EPIC-<slug>.md` | edit Now/Next/Blocked and task-table rows; status values `todo`, `in-progress`, `blocked`, `done` |
| A delegable unit of work was defined or finished | `.agents/tasks/TASK-<epic>-<nn>.md` | create (self-contained brief) or update status; next free two-digit number |
| How a cold session resumes this epic (state, exact next command, gotchas) | `.agents/handoffs/<epic>.md` | ONE living file, overwritten, ≤3 KB |
| Something another node must act on | `.agents/handoffs/to-<node>-<yyyy-mm-dd>-<topic>.md` **in the receiver's directory**; self-contained: symptom, evidence, what is needed | create; the receiver archives it |
| A message received and acted on | move to `.agents/archive/` | `git mv` |
| A decision with consequences, and what was rejected | `.memory/decisions/DEC-<nn>-<slug>.md` (mature+); in a tiny/standard node, a dated line in the epic | create |
| A fact that will stay true (stack gotcha, how to build, a constraint) | `.memory/cards/<id>.md` (mature+); otherwise `AGENTS.md` working rules if it must always be followed | edit |
| Evidence, logs, raw output | `.agents/runs/` | never read whole, referenced by path |
| A new durable file of any kind | one line in `.memory/INDEX.md`, or the `AGENTS.md` routes table if there is no index | edit |
| A child project's changed state (domain session only) | the child's one row in the domain `status.md` | edit the row, nothing else of the child's |

Every file starts with `<!-- when: ... -->`. Headline numbers and dates must be absolute. A fact you cannot ground in the session, git, or a file goes in "open questions", not in state.
