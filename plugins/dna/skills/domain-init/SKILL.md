---
name: domain-init
description: Give a folder that holds several projects (a client, a team or a theme) the dna domain layer: router AGENTS.md, .agents/status.md with one row per child project, and .memory/ with an INDEX and one identity card per child. Reads children, never writes into them. Use whenever the user says "init this domain", "set up the domain layer", "domain-init", "make a status table for the projects in this folder", "index the projects under <client>", "this client folder needs an AGENTS.md and memory", "organizá esta carpeta de proyectos", or a status check on a multi-project folder found no layer. For a single project use agentize. Writes directly; commits only if asked.
---

# domain-init

Create the domain layer ([../../references/layer-contract.md](../../references/layer-contract.md): read the Stages and Domain owns parts only if a budget or ownership question comes up). A domain routes and indexes; it does not copy a child's plans or progress. Its result: `AGENTS.md` (router), `.agents/status.md` (one row per child), `.memory/INDEX.md`, `.memory/projects/<domain>-<project>.md` (one card per child, 2 KB each).

## Rules

- **Read children, never write into them.** Single-writer ownership: a child's layer is only changed by a session in that child. A child with no layer gets a "no layer" row and a suggestion to run `agentize` there.
- **Same safety as `agentize`:** no text lost (archive any `AGENTS.md` you restructure verbatim to `.agents/archive/`, binding rules stay verbatim, same make-room order, budget 8 KB at domain stage), existing `.memory/` files are never overwritten: append missing lines to an existing INDEX.md, add only missing cards. If the domain has no `AGENTS.md`, create it from the agentize template (nothing to restructure). Facts come from disk and git; guesses are listed under Open questions.
- English for prose in `.agents/` and `.memory/`, absolute dates (`date +%F`), `<!-- when: ... -->` on every file there. Public repo content stays generic. Never read `.env` or secrets.

## Steps

1. **Resolve the domain** (the folder named, else the working directory). If it is itself a single project (one manifest or code at the top, no child projects), say so and suggest `agentize`. If `.agents/status.md` exists, stop and point at `status`/`save-state`.
2. **Find children:** immediate subdirectories (or one level down when the folder is a grouping like `Projects/`) that look like projects: contain `.git`, a manifest (`pyproject.toml`, `package.json`, `requirements.txt`, `Cargo.toml`, `go.mod`, `Makefile`, `*.sln`) or an `AGENTS.md`/`CLAUDE.md`. A grouping folder (like `Projects/`) is one with none of those whose subfolders qualify. A folder with none of those and no qualifying subfolders (docs, templates) is not a child: list it as skipped. Skip hidden, build, vendor, `data`, `logs` and `node_modules` folders. Show the candidate and skipped lists; if there are over ten children or a case is unclear, confirm once with the user, and if you cannot ask, index the clear ones and list the rest as open questions.
3. **Survey each child cheaply, read-only:** layer present? (`AGENTS.md`, `.agents/status.md`; if so its `Stage` and status date), `git -C <child> log -1 --format='%h %ad %s' --date=short`, branch, whether clean, one line of purpose from its README head or `AGENTS.md`. Do not open a child's epics.
4. **Write `AGENTS.md`:** follow `agentize` step 3 (create from a template, keep-and-append, or archive and restructure). Content: what the domain is in two lines, domain-level binding rules verbatim, and a routes table: `.agents/status.md`, `.memory/INDEX.md`, and one line saying "each child has its own AGENTS.md; open it when working there". Do not list children here; status and cards do.
5. **Write `.agents/status.md`** from the save-state template's domain form (under 4 KB): `| child | state | epic pointer | date |`, linking each child's own status when it exists. Dormant or parked children (no commit for 60 days) are grouped on one line. A child without a layer reads "no layer, run agentize there". Date column = the child's last commit date (`YYYY-MM-DD`); a child without git has date "no git" and is never dormant by the date rule. Dormancy only moves a child to the grouped line when at least one child is active; if all are dormant, keep one row per child. Classify layers as: none, partial (an `AGENTS.md` or empty `.agents/` but no `.agents/status.md`), or full.
6. **Write `.memory/projects/<domain>-<project>.md`** per child: path, kind (from manifest or README), purpose, layer state, git head and date, pointer to the child's `AGENTS.md`. Under 2 KB, facts only, starting with `<!-- when: you need the identity of <child> without opening it -->`. File name is `<domain>-<project>.md` as the contract says. Purpose comes from the child's README or `AGENTS.md` head; with neither, write "unknown" and an open question, never a guess from commit messages. Leave each child's language as it is. Then `.memory/INDEX.md` with one line per card and a `<!-- when: ... -->` header. Add `.memory/decisions/` only if the user states a domain-wide decision.
7. **Validate** on the domain (`python3 -I ../../scripts/validate_layer.py <domain>`, path relative to this skill) and fix FAILs you caused; report pre-existing ones as a count plus the three worst. Do not validate or repair children.
8. **Show the result:** `git status --short` if the domain is a repo (many domains are plain folders: then list the files written) and two lines of summary: children indexed, children with no layer. Commit only if asked, only the files you wrote; never push or amend. In this repo add the changelog entry in the same change.

## Never

- Write in a child, move or rename a child, or copy a child's plans into the domain.
- Invent a child's purpose or state; use "unknown" and an open question.
- Promote anything to `mature` or create epics at domain level.
