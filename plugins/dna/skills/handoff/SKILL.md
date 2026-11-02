---
name: handoff
description: Write or consume a handoff inside the project's agent context layer (.agents/handoffs/): a self-contained note between sessions or between a parent domain and a child project, so the receiver can act with none of the sender's context. Use when the user says "write a handoff", "hand this off to the engine/backend/child session", "leave a note for the other session", "to-<project> note", "tell the parent/child session", "update the handoff for this epic", "read the handoffs the parent created", "check my handoffs", "process the handoff", "/rc independent agent", "pasale esto a la otra sesión", "leé los handoffs". Enforces one writer per file and archives a handoff once the receiver has acted on it. For saving the whole session state use save-state instead.
---

# handoff

A handoff is a file one session leaves so another session can act without the first one's chat. It is part of the layer contract ([../../references/layer-contract.md](../../references/layer-contract.md), optional reading). Two kinds, one skill, three modes.

| Kind | Path | Lifecycle |
|---|---|---|
| **Living** | `.agents/handoffs/<epic>.md` in the node doing the work | ONE file per epic, overwritten each session, ≤3 KB |
| **Directional** | `.agents/handoffs/<to\|from>-<node>-<yyyy-mm-dd>-<topic>.md` in the **receiver's** node | written once by the sender, read by the receiver, then archived by the receiver, ≤4 KB |

## Why the rules exist

Two sessions editing the same file overwrite each other, and a note that assumes shared context makes the receiver guess and invent. So: the sender writes only files it owns or the file addressed to the receiver, never edits the receiver's other files, and the note must stand alone.

## Mode 1: write a living handoff (resume myself later)

1. Resolve the node and the epic (the one the session worked on; ask once if unclear). Read the existing handoff before overwriting it; keep what is still true.
2. Overwrite `.agents/handoffs/<epic>.md` using [references/templates.md](references/templates.md). Cover only: where things stand, the exact next command or step, gotchas that cost time, what is running or locked. Link the epic and task files instead of copying them.
3. If `save-state` is also requested, it calls this; do not write the handoff twice.

## Mode 2: write a directional handoff (tell another node)

1. Identify the receiver (child, parent, sibling) and find its directory; `<receiver>` in the filename is that directory's name. If the receiver has no `.agents/` yet, create `.agents/handoffs/` only and tell the user the node still lacks the layer's `status.md`. Create the file in **its** `.agents/handoffs/`, named `to-<receiver>-<date>-<topic>.md` (or `from-<sender>-…` when the receiver is the parent being told). Date: `date +%F`.
2. Make it self-contained with the directional template: why you are writing, evidence (commands, paths, hashes, absolute dates), what the receiver should do, what you did NOT do, how you will know it worked. Write it as if the receiver has never seen this conversation.
3. Ground every claim in a file, command output or commit. Label anything unverified as such. No secret values.
4. Stay in your lane: do not edit anything else in the receiver's layer. Optionally add one pointer line under "Blocked" (or "In flight") in your own `status.md`: "waiting on <receiver>: <file>".
5. If the receiver is an executor launched by a brief (not a standing node), put the same content in a task card `.agents/tasks/TASK-<epic>-<nn>.md` instead.

## Mode 3: read and consume handoffs addressed to me

1. List `.agents/handoffs/` in my node; open only `to-*`/`from-*` files not yet archived, newest first, reading each one's `when:` line first.
2. Verify the claims that matter (run the check, read the commit) before relying on them; a handoff is a claim. If the evidence lives somewhere you cannot reach, say so and treat the claim as unverified.
3. Act on it, or record what blocks. Then move the file to `.agents/archive/` (`git mv` in a repo, plain `mv` otherwise; the receiver archives, the sender never deletes). If you cannot act, still archive it after recording the blocker in a reply. And, if the sender needs an answer, write a directional handoff back in the sender's `.agents/handoffs/`.
4. Reflect new work in the epic or `status.md`; if unsure how, use `save-state`.

## Never

Edit the sender's or receiver's other files; leave a handoff unindexed outside `.agents/handoffs/`; write relative dates; paste secrets (refer to the file by path); let a living handoff grow into a log.
