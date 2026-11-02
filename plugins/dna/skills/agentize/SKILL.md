---
name: agentize
description: Give an existing project (one repo or folder, not a collection of projects) the dna agent context layer: a router AGENTS.md, a thin CLAUDE.md pointer and a seeded .agents/status.md, so every later session can resume from files. Restructures a bloated or missing AGENTS.md into a short router without losing any text. Use whenever the user says "agentize this project", "set up the agent context layer", "add AGENTS.md and .agents", "bootstrap agent context here", "make this repo agent-ready", "init the layer for this project", "este proyecto no tiene AGENTS.md", or opens a project with no layer after a status check found none. For a domain that contains projects use domain-init instead. Writes directly; commits only if asked.
---

# agentize

Create the minimum layer a project needs ([../../references/layer-contract.md](../../references/layer-contract.md): read it only if a budget or ownership question comes up). The target is the stage the node already has (the validator reports it): **tiny** (`AGENTS.md` + `.agents/status.md`) for a bare project, **standard** if epics, tasks or handoffs already exist. Never promote the stage and never create epics, tasks, handoffs or `.memory/`; growth happens later through `save-state` when a signal fires.

## Rules

- **No content is lost.** Anything you remove from an existing `AGENTS.md` is first preserved verbatim (step 3). Git is the undo path, and the final diff is the proof.
- **Seed only from evidence.** Facts come from the README, manifest files, `git log` and `git status`. Whatever you infer is written as a guess under Open questions, never as state.
- **Write in the project, for the project.** Nothing outside this node's `AGENTS.md`, `CLAUDE.md` and `.agents/`. Public repo? Keep secrets, client data and machine paths out.
- English for prose in `.agents/` even if the project is in another language, but quote commit subjects and doc titles verbatim. Absolute dates (`date +%F`); every `.agents/` file starts with `<!-- when: ... -->`.
- **Leave strays alone.** Loose root files, an existing empty `.agents/`, and secret files (`.env`) are never moved, edited or read; list only notable strays in your final message.

## Steps

1. **Resolve the node:** the directory the user names, else the git root of the working directory. If it contains several independent projects it is a domain: say so and suggest `domain-init`. If it already has `.agents/status.md`, the layer exists: switch to **adopt mode** and follow [references/adopt.md](references/adopt.md) instead of the steps below (marker, index and pointer only; no content is rewritten, and an oversized status is left for `save-state`).
2. **Survey, cheaply:** list the top level; read `README.md` (head), the manifest (`package.json`, `pyproject.toml`, etc.) for the build/test commands, any existing `AGENTS.md` and `CLAUDE.md`; run `git status --short`, `git log -5 --format='%h %ad %s' --date=short`, and the current branch. Run the validator for a baseline: `python3 -I ../../scripts/validate_layer.py <node>` (path relative to this skill; skip if unreachable).
3. **Preserve, then restructure `AGENTS.md`:**
   - **Missing:** create it from [references/agents-template.md](references/agents-template.md).
   - **Present and within 6 KB:** keep its text unchanged and append what is missing: the `<!-- dna:layer v1 -->` marker on the line after the title (hooks act only in nodes carrying it; a restructured or created `AGENTS.md` gets it too), a routes table (linking `.agents/status.md`, every doc it or `CLAUDE.md` already references, and `README.md`; if many other docs exist, do not guess which matter, list the question in status) and a Commands line when the manifest or README states them (otherwise an open question). If the real working rules live in a referenced doc, route to it with a label like "rules live here"; do not copy them.
   - **Present but long or unstructured:** copy it unchanged to `.agents/archive/AGENTS-before-agentize-<date>.md` with a `when:` header prepended, then rewrite `AGENTS.md` as a router under its budget (6 KB tiny, 8 KB standard; the budget applies to the final file, additions included): purpose in two lines, commands (partial and marked unverified is fine), the **binding rules** kept verbatim, and a routes table.
   - A binding rule is an imperative constraint or default (must, never, always, default to, read-only, branch/tag conventions). Descriptive passages (where things live, structure, history) are not rules. If unsure, treat it as binding.
   - Make room in this order: move descriptive sections out first (rebuild "where things live" as routes), then, only if still over budget, move rule sections out, leaving in `AGENTS.md` a one-line pointer per moved rule section (its heading plus "see archive, section X") and saying so in your final message so the user can decide.
   - Moved text lives only in the archive. Its `when:` header is `<!-- when: you need the full pre-agentize AGENTS.md; may contain stale rules -->`, and its routes row says the same. Links to files outside the node are kept as plain backticked text, unchecked.
4. **`CLAUDE.md`:** create a thin pointer (`Read [AGENTS.md](AGENTS.md) first. This file only holds Claude Code specifics.`) if missing. If it exists, leave it; if it lacks a pointer to `AGENTS.md`, add `Read [AGENTS.md](AGENTS.md) first.` at the top. Never touch the rest. Report duplicated rules (AGENTS.md vs CLAUDE.md, or either vs a referenced doc) in your final message, not in status.
5. **Seed `.agents/status.md`** from [../save-state/references/status-template.md](../save-state/references/status-template.md), under 4 KB: Goal now from the README, Stage `tiny`, branch/head and cleanliness from git, Last session from the git log (hashes), and Open questions listing every inferred or missing fact ("Goal inferred from README: confirm"). Stage is whatever the node already is. If `.agents/epics/` exists, list each epic under In flight as "state not verified" with a link; otherwise omit In flight unless git or the README shows a plan. Keep Last session to 3 bullets.
6. **Validate again;** fix any FAIL you caused. Report pre-existing ones as a count plus the three worst, and name `save-state` as the fix; do not repair them here.
7. **Show the result:** `git status --short` plus two lines: what was created, what was preserved where. Commit only if the user asked, staging only the files you wrote; never push or amend. If this repo keeps a changelog, add the entry in the same change.

## Never

- Overwrite or delete an existing file's text without the archived copy.
- Invent goals, owners, deadlines or progress.
- Paraphrase a binding rule, or drop one without a pointer to where it went.
