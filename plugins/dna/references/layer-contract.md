<!-- when: designing, building or checking anything that reads or writes the agent context layer (AGENTS.md, .agents/, .memory/); every dna skill and hook obeys this -->
# dna layer contract

One layout that scales from a 50-line POC to a multi-project domain, and keeps every agent's
session-start cost small and predictable. Skills (`status`, `save-state`, `handoff`, `domain-init`,
`agentize`) and hooks implement this; none of them invents files outside it.
Check a tree with `python3 -I plugins/dna/scripts/validate_layer.py <dir>`.

## Principles

1. **Router, not encyclopedia.** `AGENTS.md` says where things are. Content lives one hop away.
2. **Index before content.** An agent reads a map, then exactly one detail file.
3. **Every node is self-sufficient.** A project has its own `AGENTS.md` and `.agents/` from day one,
   whether or not it sits inside a domain. A domain adds routing and cross-project facts on top; it
   never replaces a project's own layer.
4. **`.agents/` = how work happens (changes often). `.memory/` = what is known (changes rarely).**
   `.memory/` appears only when a node has stable knowledge worth indexing.
5. **Overwrite what is state; append only what is history.** Status and living handoffs are
   overwritten. History lives in git, `CHANGELOG.md` and dated decisions.
6. **Budgets are bytes** (about 4 bytes per token). Line counts lie: a "one line per epic" status
   file was 84 lines and 24 KB.
7. **English, absolute dates, no secrets.** Public-safe naming in anything shipped from this repo.

## File set

`●` required, `○` appears when its trigger fires.

| Path | Stage | Holds | Writer | Budget |
|---|---|---|---|---|
| `AGENTS.md` | ● all | Router: one-paragraph identity, routes table, working rules, before-you-finish | human; skills edit only the routes table | 6 KB tiny, 8 KB otherwise |
| `CLAUDE.md` | ○ | Provider-specific pointer to `AGENTS.md`, nothing restated | human | 1.5 KB |
| `.agents/status.md` | ● all | Current state: now, next, blocked, open questions. Overwritten whole | `save-state`, human | 4 KB |
| `.agents/epics/EPIC-<slug>.md` | ○ first multi-step work | Goal, now/next/blocked, task table | owner node | 6 KB |
| `.agents/tasks/TASK-<epic>-<nn>.md` | ○ delegable unit | Self-contained brief: goal, needs, touches, gate, done-when | owner node | 4 KB |
| `.agents/handoffs/<epic>.md` | ○ first session split | ONE living file per epic, overwritten each session | `handoff`, `save-state` | 3 KB |
| `.agents/handoffs/<to\|from>-<node>-<date>-<topic>.md` | ○ cross-node message | Directional note, consumed once, then archived | sender writes, receiver archives | 4 KB |
| `.agents/plans/`, `workflows/`, `scripts/`, `runs/`, `archive/` | ○ | Plans, procedures, helpers, run evidence, closed material | any | file-level 8 KB; `runs/` and `archive/` exempt, never read whole |
| `.memory/INDEX.md` | ○ standard | One line per memory file and durable asset | whoever adds the file | 6 KB |
| `.memory/cards/<id>.md` | ○ | Stable facts about a component | owner node | 3 KB |
| `.memory/decisions/DEC-<nn>-<slug>.md` | ○ | Dated decision with why and what was rejected | owner node | 3 KB |
| `.memory/projects/<domain>-<project>.md` | ○ domain | Identity card of a child: path, kind, status, git head, epic pointer | domain | 2 KB |
| `.memory/*.json` | ○ domain, optional | Machine shards queried with `jq`; never read whole | generator | exempt |

Rules for the table:
- Names: `EPIC-<slug>`, `TASK-<epic>-<nn>` (two digits, then more if needed), `DEC-<nn>-<slug>`,
  `RUN-<yyyymmdd>-<nn>-<tool>` (workspace rule, `~/Code/AGENTS.md` §8). Status values:
  `todo`, `in-progress`, `blocked`, `done`.
- Every file in `.agents/` and `.memory/` starts with `<!-- when: <situation that makes you read this> -->`.
  This is what lets an agent skip a file without opening it.
- Every durable file is one line in the nearest `.memory/INDEX.md`; if the node has no `.memory/`,
  it is listed in the routes table of `AGENTS.md`. An unindexed file does not exist.
- Close an epic by marking it `done`, moving it to `.agents/archive/`, and removing its row from
  status.

## Growth stages

Signals, never commands. The validator reports "outgrown" and the human or a skill acts.

| Stage | Shape | Typical | Move to next when |
|---|---|---|---|
| **tiny** | `AGENTS.md` + `.agents/status.md` | POC, spike, research folder | first piece of work spans more than one session, or a plan is needed |
| **standard** | + `.agents/epics/`, `tasks/`, `handoffs/` as used | project with real work in flight | stable knowledge accumulates (stack facts, decisions, gotchas) or `AGENTS.md` nears its budget |
| **mature** | + `.memory/` (INDEX, cards, DEC) | a project that grew or needs durable knowledge | a second child directory gets its own `AGENTS.md` |
| **domain** | + `.memory/projects/` cards, domain routes, one status row per child | folder holding several projects | n/a |

A project may reach `mature` on its own. A node is a domain when it routes to children that each
carry their own layer; the domain itself still follows the same table.

## Ownership (single writer)

- A node writes only to its own `AGENTS.md`, `.agents/` and `.memory/`. Never into a sibling or
  child.
- **Project owns:** its epics, tasks, handoffs, plans, decisions about itself.
- **Domain owns:** child identity cards, cross-project decisions, one status row per child, the
  domain routes. It does not copy a child's plans or progress; it links.
- Crossing a boundary is a directional handoff file placed in the **receiver's**
  `.agents/handoffs/`, written by the sender, archived by the receiver after acting. The receiver
  never edits the sender's files.
- Dual-use docs (ADRs, README) stay where humans own them; the layer holds a route, not a copy.
- This contract overrides workspace rule §2 ("plans never go inside a project") for per-node
  `.agents/`. The workspace `AGENTS.md` should be amended to match.

## Read rules

- **Session start, in order, stop when the task is clear:** `AGENTS.md` → `.memory/INDEX.md` (if
  any) → `.agents/status.md` → ONE epic → its living handoff.
- **Session-start budget: 12 KB (about 3k tokens) for the first three files combined.** Needing
  more means a route is missing. Fix the route; do not read around it.
- Read a file's `when:` line before opening the rest. Query JSON with `jq`.
- Facts are dated. Check a volatile fact (count, path, version) against disk before relying on it;
  where they disagree the disk wins and the file is the bug.
- Never read `runs/`, `archive/` or logs whole.

## Write rules

- **Write directly, in the fixed form.** Safety comes from the layout and git, not confirmation
  prompts.
- Read a file before overwriting it. Never delete human-written content without moving it to
  `archive/`.
- `status.md` is overwritten, kept under budget. When it overflows, content moves to the epic it
  belongs to, never into a bigger status file.
- Update the state file in the same change that alters the state.
- Never write secret values or machine-specific paths from `.env` into the layer.
- Commit only when asked.
- Adopting a messy tree (`agentize`): show the plan grouped by action, move with `git mv` on a
  clean tree, write an undo script. Existing human content outranks generated content.

## Hooks

| Event | Allowed | Forbidden |
|---|---|---|
| SessionStart | Read-only. Print `.memory/INDEX.md` head and `status.md`, byte-capped to the session-start budget. | Any write; unbounded output |
| PreCompact, Stop | Remind or prompt the agent to run `save-state`. May run the validator read-only. | Writing, committing, or running `save-state` unattended |

Reason: skills run with a person present who can undo; a hook can fire unattended. Revisit once the
skills are stable. Hooks live in `plugins/dna/hooks/`.

## Token-cost rationale

- A tier-0 file is paid on every turn. 8 KB is about 2k tokens; a 900-line instruction file is
  a recurring tax that grows with the project's value.
- The measured failure: documented session start "about 3k tokens" actually read about 38 KB
  (`AGENTS.md` 8 KB + index 6 KB + status 24 KB), roughly 10k tokens, before any task detail.
- Therefore: small router, `when:` headers to skip files cheaply, an index before content, one
  epic per session, overwrite-only state, bytes not lines.

## Validator

`plugins/dna/scripts/validate_layer.py <dir> [--json] [--legacy]` is stdlib-only and read-only.
- **fail:** over a byte budget (tier-0 and state files), missing `AGENTS.md` or `.agents/status.md`,
  missing `when:` header, bad id naming, stray status value, unindexed `.memory/` file, session-start
  set over 12 KB.
- **warn:** stage outgrown (per the table), consumed `to-`/`from-` handoffs older than 14 days,
  `archive/` or `runs/` referenced by routes.
- `--legacy` downgrades fails to warns for trees that predate the contract.
Exit code: 0 clean or warnings only, 1 on any fail.

## Open items

- Domain-level amendment of `~/Code/AGENTS.md` §2 (outside this repo).
- Whether `agentize` converts `AI/` (flat dated files) is decided in that skill's session.
