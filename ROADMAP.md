# ROADMAP.md

What to build next and why. Evidence comes from mining 1,432 user prompts across 329 Claude Code
sessions (2026-07-16 → 2026-11-01, 51 project dirs). Each skill gets its own deep session; this
file is the queue and the brief seed. Rules: [AGENTS.md](AGENTS.md). Decisions: [CONTEXT.md](CONTEXT.md).

## How the owner works (design inputs for every skill)

- **Domain → project tree.** Work lives in domains (`~/Code/Crytek`, `~/Code/AI`) holding related
  projects. A parent session orchestrates; child project sessions execute. Parent/child state
  flows through **handoff files**, with a single-writer rule per codebase.
- **Many short sessions, one long memory.** Sessions are cleared often (`/clear <topic>`, context
  compaction). Continuity lives in files (`.memory/`, `.agents/status`, epics/tasks), not chat.
  The recurring opening is "<project> status".
- **Operator + advisor + cheap workers.** Typical preamble: Sonnet orchestrates, Opus advises,
  Haiku agents research. Token cost is a first-class concern.
- **POCs and research, not delivery.** Lighter than Khem: no estimates, proposals or Jira chain.
  Plans, epics, phases and open questions yes; ceremony no.
- **Ask first, then run.** "Review the plan and ask me open questions before the run." Wants
  decisions surfaced, detailed commit messages, and no unrequested pushes.
- Mixes English and Spanish; skills should not depend on either.

## Candidate skills (ranked by observed frequency)

| # | Skill | Plugin | Evidence | What it does |
|---|---|---|---|---|
| 1 | `status` | dna | ~120 prompts ("X project status", "read the current state, open epics, questions") | Read-only recall: reads memory index + status, reports state, open items, blockers, open questions. Cheap. |
| 2 | `save-state` | dna | ~65 ("save everything to continue later", "commit, update status/memory") | Closes a session: collects recent work, lands it in the right status/memory/handoff files, commits. |
| 3 | `domain-init` | dna | explicit use in Crytek, mute | Light init/refresh of a domain root: map child projects, index, parent status. Derived from khem's, minus the weight. |
| 4 | `agentize` | dna | explicit use in 4+ projects | Like domain-init for one project, plus reorganizing existing docs/agent files. More rework, same layer. |
| 5 | `handoff` | dna | `to-engine-*` files, "/rc independent agent", "read the handoffs the parent created" | Write/read a self-contained handoff between sessions or parent↔child; enforces single-writer. |
| 6 | `ship` | dna | ~149 commit/push/PR, ~77 merge-then-cleanup | Detailed commit message, push/PR only on request, after merge: delete branch, switch to main, update changelog/status. |
| 7 | `crew` | dna | ~64 ("operator/advisor/Haiku workers") | Role preamble: who orchestrates, who advises, what workers may do, cost rules. Probably a short skill + reference. |
| 8 | `plan` | dna | ~217 plan/epic/phase prompts | POC-weight plan → epics/tasks files with stable ids (`EPIC-<slug>`, `TASK-<epic>-<nn>`). |
| 9 | `export-context` | dna | "create a context md to throw into a conversation" | Portable briefing for an external chat (Grok/ChatGPT) from the project state. |
| 10 | `review-board` | dna | ~99 review/audit, "board of experts", ultrareview | Critical review of a plan/design using advisor + cheap researchers. Lowest priority; may stay a prompt. |

Plugin `pla` (plasmid/CRYENGINE tooling, public, no engine data) is created when its first skill
exists. No candidates mined yet beyond what the Crytek domain already has under `Crytek/.agents/`;
mine that tree in the session that creates `pla`.

Skills 3, 4, 2 and 5 share one **context layer contract** (`AGENTS.md` router, `.agents/`,
`.memory/`, status, handoffs). Define that contract once, in `plugins/dna/references/` or as a
skill all four read, before writing any of them.

## Ground truth to start from (read before drafting)

- Existing heavy versions: `khemlabs/khem-marketplace/plugins/khem/skills/{domain-init,project-agentize}`
  (293 / 378 lines, with scripts). Lighten, don't copy.
- Live examples of the layer: `~/Code/Crytek` (`.memory/INDEX.md`, `.agents/status.md`, naming
  scheme, handoffs) and `~/Code/AI`.
- Workspace rules these skills must respect: `~/Code/AGENTS.md`.

## Not skills (mined, deliberately dropped)

- Pasted error logs and one-off sysadmin questions (Arch tuning, battery, clipman): no repeat shape.
- `15m` / `30m` replies: Jira worklog answers for khem work-on-task; belong to khem.
- Khem delivery chain, Jira work: stays in the khem marketplace.

## Resolved (2026-11-01)

Status file = `.agents/status.md`. Skills write directly, consistently. Hooks are in scope.
Design target: one system that scales from a tiny POC to a multi-project domain as the work grows,
and keeps agents' token use low (small router, lazy-loaded detail, indexes before content).

## Build order

0. **Layer contract** (own session, longest thought). Defines, once: the file set and what each
   file holds (`AGENTS.md` router, `.agents/status.md`, `.agents/` plans/epics/handoffs,
   `.memory/INDEX.md` + cards), id/naming scheme (reuse Crytek's `EPIC-<slug>`/`TASK-<epic>-<nn>`
   unless the study says otherwise), size budgets per file, how a project *grows* (tiny → standard
   → domain: which files appear when), and the read/write rules every skill and hook obeys.
   Output: `plugins/dna/references/layer-contract.md` plus a validator script.
1. `status` + `save-state` (they are the read and write halves of the contract).
2. `handoff`, then `domain-init` and `agentize` (they build the layer from nothing / from a mess).
3. Hooks: SessionStart (load index, show status), PreCompact/Stop (save-state). Built after the
   skills they call, and only once the contract is stable.
4. `ship`, `crew`, `plan`, `export-context`, `review-board`.

## Session 0 brief (copy into a fresh session in `~/Code/dna/ai-skills`)

> Read `ROADMAP.md`, `CONTEXT.md`, `AGENTS.md`. Design the dna layer contract. Study before
> proposing: `~/Code/Crytek` (`.memory/`, `.agents/`, naming, handoffs), `~/Code/AI`, one small
> POC project, and khem's `domain-init` / `project-agentize` with their references. Find what a
> 50-line POC and a 15-project domain have in common and where they must differ. Deliver
> `plugins/dna/references/layer-contract.md` (file set, ownership, size budgets, growth stages,
> read/write rules, token-cost rationale) and a stdlib-only validator script. Ask me the open
> questions before writing. Do not write any skill yet.

## Still open

1. Hook details: which events, and how much a hook may do unattended (read-only vs. write).
2. Whether `.memory/` stays a separate directory from `.agents/` in the contract (workspace
   rule today: `.memory/` = what is known, `.agents/` = how work happens). Session 0 decides.
