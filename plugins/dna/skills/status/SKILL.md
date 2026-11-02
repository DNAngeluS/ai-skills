---
name: status
description: Read-only recall of where a project or domain stands, cheaply. Reads the agent context layer (AGENTS.md routes, .memory/INDEX.md, .agents/status.md, the active epic) and reports state, work in flight, blockers, open questions and the suggested next step. Use whenever the user opens a session with "<project> status", "status", "where were we", "what's the current state", "read the current state, open epics, questions", "what's open", "how is X going", "cómo viene X", "en qué quedamos", or resumes work after /clear or compaction, even if they never say the word status. Never writes anything.
---

# status

Give the user an accurate, short picture of where a node (a project or a domain) stands, so they can decide what to do next. This is the read half of the layer contract ([../../references/layer-contract.md](../../references/layer-contract.md), optional reading: the steps below are self-contained). It is deliberately cheap: state is one hop away, so do not scan the codebase or read around a missing route.

## Rules

- **Read-only.** Never create, edit, move or commit anything, including "obvious" fixes to stale files. Report the problem and name `save-state` as the fix.
- **Stop reading as soon as the picture is clear.** Epics and handoffs are opened one at a time, only when relevant. Read files separately, never dump several into one command.
- **A status file is a claim.** It is dated and may be stale. Check the few volatile facts you will repeat (branch, a path, a count) against disk or git before stating them as current, and say what you could not check.

## Steps

1. **Resolve the node.** If the user named a project or domain, find its directory (a child of the current domain, a card under `.memory/projects/`, or a path they gave). Otherwise use the nearest ancestor of the working directory that has an `AGENTS.md`. If the name is ambiguous, list the candidates and ask once.
2. **Read in contract order:** `AGENTS.md` (routes only, skim) → `.memory/INDEX.md` if present → `.agents/status.md`. Use the `when:` first line of any other file to decide whether to open it. If `status.md` is much larger than 4 KB (the contract's cap), read its head and any tables, trust the newest dated block over older text, and report the oversize as a doubt.
3. **Project nodes:** pick the active thread. If status points at one epic (or the user named one), read that `EPIC-*.md` and its living handoff `.agents/handoffs/<epic>.md`. **Domain nodes:** skip this step.
4. **Cheap checks.** In the node run `git status --short` and `git log -1 --format='%h %ad %s' --date=short`; note uncommitted or unpushed work. Freshness = the newest date written in `status.md` (header or newest block) versus the last commit date: say "fresh" or "N days behind git", and name the discrepancy if the header and a newer block disagree. Run `python3 -I ../../scripts/validate_layer.py <node>` (path relative to this skill's directory; skip if unreachable) and **summarise** it: the FAIL count, the three worst offenders, nothing more.
5. **Domain nodes:** report one line per child from the status rows. To see whether a child moved, run `git -C <child> log -1 --format=%ad --date=short` and compare with the row date; if the child directory is absent, write "not checked". Group dormant or parked children on one line. Do not read the children's layers unless the user picks one.
6. **Stale-looking rows** (for example open questions that a later block seems to have decided): list them under Doubts instead of deciding which is live.
7. **No layer found:** say so plainly, give what you can from `README.md` and git, and suggest the layer be created (the `agentize` and `domain-init` skills, when installed). Do not create it.

## Report format

Lead with the answer, not the process. A project report stays under about 25 lines. A domain report may run longer, one line per child, but must stay scannable.

```
<node> — <stage>, status dated <YYYY-MM-DD> (<fresh | N days behind git>)
In flight:  <epic/task or child, one line each>
Blocked:    <item and what unblocks it, or "nothing">
Open questions: <numbered, the ones needing the user>
Uncommitted/unpushed: <summary or "clean">
Next: <the single most useful next action, from status/epic, not invented>
Doubts: <stale or unverifiable claims, oversize status, validator summary; omit if none>
Open: <domain only: "which child do you want to open?">
```

Use absolute dates. If status and git disagree, say which one you trust and why. Label any guess as a guess. Answer in the user's language.
