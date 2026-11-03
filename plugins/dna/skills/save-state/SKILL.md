---
name: save-state
description: Close out or checkpoint a working session by landing what happened into the project's agent context layer (.agents/status.md, the active epic and task rows, the living handoff, memory cards or decisions) so the next session can resume from files instead of chat. Use whenever the user says "save state", "save everything to continue later", "update status and memory", "wrap up", "checkpoint", "I'm clearing the session", "before /clear", "update the handoff", "commit and update status", "guardá todo para seguir después", "cerremos la sesión", or when context is about to be compacted. Writes directly in the fixed layout; commits only if the user asked for a commit.
---

# save-state

Turn the session's results into durable files, in the places the layer contract defines, so a cold session (after `/clear` or compaction) loses nothing. This is the write half of [../../references/layer-contract.md](../../references/layer-contract.md); the `status` skill is the read half. The contract is about 9 KB: read it only for a standard-or-larger node or when a budget or ownership question comes up. A tiny node needs only the quick path below.

## Principles

- **Write directly, in one consistent form.** No propose-then-apply step. Safety comes from the fixed layout and from git: the diff you show at the end is the undo path.
- **State is overwritten, history is not duplicated.** `status.md` and living handoffs are rewritten whole. What happened goes to git, the epic, or a dated decision, never into an ever-growing status file.
- **Only write what you can ground.** Use the conversation, `git status`, `git diff --stat` and `git log` since the status file's date. Do not invent progress. If something is unclear (did that experiment pass? is that decision final?), ask once, batched, before writing.
- **Stay in your node.** Write only to this node's `AGENTS.md`, `.agents/` and `.memory/`. Never into a child's or sibling's layer. A domain session updates its one row for a child; the child's own session updates the child's files.
- **Edit what the session touched, flag the rest.** Dated facts in sections you did not work on may be stale; leave them and mention it. Rewrite only text the session directly contradicts. Leave links to files that do not exist alone.

## Quick path (tiny node: only `AGENTS.md` + `.agents/status.md`, or `status.md` missing)

1. If `.agents/status.md` is missing, create it from [references/status-template.md](references/status-template.md).
2. Write it from the session facts. One "next step" does not justify an epic. Create `.agents/epics/EPIC-<slug>.md` only when there are two or more planned tasks, or a multi-step plan that clearly outlives this session; then follow the full steps.
3. Validate, show the result, commit only if asked (steps 8-10).

## Full steps

1. **Resolve the node** (nearest ancestor with `AGENTS.md`, or the one the user names) and its stage: tiny, standard, mature, domain.
2. **Read before writing:** `.agents/status.md`, the active epic and its living handoff if they exist. Date: use `date +%F`, unless the user stated a date, which wins.
3. **Run the validator first** to see headroom and pre-existing problems: `python3 -I ../../scripts/validate_layer.py <node>` (path relative to this skill's directory; skip if not reachable).
4. **Collect the facts of the session:** what was done (with commit hashes), what is in progress and its exact next step, what is blocked and by what, decisions made and why, open questions for the user, anything learned that will stay true.
5. **Route each fact** with [references/routing.md](references/routing.md). Short version: current state → `status.md`; progress on planned work → the epic's Now/Next/Blocked and task-table rows (use `todo|in-progress|blocked|done`, and normalise a free-text status word such as "drafted" in any header you rewrite); how to resume → the epic's living handoff (overwrite); a message to another node → a directional handoff in the *receiver's* `.agents/handoffs/`; a decision → `DEC-<nn>-<slug>.md`, or in a node without `.memory/` a dated line under a `## Decisions` section of the epic; a durable fact → a card (mature+ only); a new durable file → one line in the nearest index.
   - Update an epic's task-table row even if its `TASK-*.md` card does not exist; create a card only when a task is being briefed for delegation.
   - A task may be `done` on evidence: a commit, a passing check, or the user's own statement (cite which). Otherwise `in-progress` with what remains.
   - If the epic's prose and its table disagree on ids, follow the table and mention the mismatch in your report.
6. **Grow the layer only when a signal fires**, never speculatively (epic threshold in the quick path). Do not create `.memory/` for a node that does not have it.
7. **Respect budgets** ([layer-contract](../../references/layer-contract.md) has them). Write `status.md` from the template, under 4 KB. If `status.md` will not fit, move overflow into the epic it belongs to and leave a one-line pointer. If the file you are editing is itself over budget (an epic, say), move the least current material to `.agents/archive/` (or split a new epic) rather than trimming hand-written text away; never raise the limit. Read every file before overwriting it, and never drop human content outright.
   - **Oversized `status.md`** (a domain's especially): copy the old file verbatim to `.agents/archive/status-before-trim-<date>.md`, then rewrite the status from the template. In the copy, replace the `when:` header with `<!-- when: you need the full pre-trim status; may be stale -->` so it is never preloaded as current. Say in the summary that the trim happened, so the user can review what you judged current.
   - **Epic table rows:** past about 25 rows, move `done` rows older than the last session to `.agents/archive/` (same verbatim-copy rule) and leave one line in the epic with the count and the archive link.
   - **Legacy status words** (drafted, planned, open, fixed, ...) in rows you do not otherwise rewrite are left alone and reported. Never drop or reinterpret them in a status-only pass; normalise only the rows the session touched.
   - **Session-start budget:** the preloaded set is the router, the INDEX head and `status.md` (12 KB together). If the router or the INDEX alone overflows it, trimming `status.md` cannot fix that: report the byte counts and name which rules or rows are candidates to leave the preloaded files. Do not cut them yourself; that is the user's decision.
8. **Validate again.** Fix any FAIL you caused (missing `when:` header, over budget, unindexed file). Fix pre-existing FAILs only when your own edit has to touch that same text; otherwise report them.
9. **Show the result:** `git status --short` (new files are untracked, so a diff stat alone shows nothing for them) and a two-line summary of what went where. In the status head, write branch and cleanliness as they will be after the save: "layer files saved, uncommitted" or the post-commit state.
10. **Commit only if the user asked** (for example "save and commit", or a plain "commit"). Stage only the layer files you wrote, never unrelated code changes, and say what you left out. Write a detailed message: what state was captured and why, listing the files. Never push, never amend.

## Never

- Write secret values, tokens, or machine paths taken from `.env` files; refer to the file by path.
- Leave a stray file anywhere outside a layer location, or an unindexed durable file.
- Use relative dates ("yesterday", "last week").
