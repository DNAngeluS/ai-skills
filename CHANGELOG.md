# Changelog

Timeline of what changed in this repo. Newest first. Every change lands here in the same
commit that makes it — see the changelog rule in [AGENTS.md](AGENTS.md#changing-this-repo).

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Dates are `YYYY-MM-DD`.
Entries record **what changed**; the reasoning behind a decision goes in
[CONTEXT.md](CONTEXT.md#decisions), linked from the entry when it matters.

## [Unreleased]

### Added

- `dna` plugin version 0.1.1 -> 0.1.2 (save-state gaps), in both `plugin.json` and `marketplace.json`.

- `save-state` step 7 gains four rules found when the Crytek domain status (25 KB) was trimmed in real use: oversized status goes verbatim to `.agents/archive/status-before-trim-<date>.md` with a "may be stale" `when:` header and the trim is reported for review; epic tables past about 25 rows archive older `done` rows; legacy status words are never dropped in a status-only pass; and when the router or INDEX alone overflows the 12 KB session-start set, report byte counts and candidates instead of cutting them.

- `dna` plugin version 0.1.0 -> 0.1.1 (adopt mode, validator status fix), in both `plugin.json` and `marketplace.json`.

- Adopt mode for `agentize` and `domain-init` (`agentize/references/adopt.md`): a node that already has `.agents/status.md` gets the `dna:layer` marker, a missing `.memory/INDEX.md` (generator-owned shards listed, never edited) and a CLAUDE.md pointer; no content is rewritten and oversized status is left to `save-state`. Previously both skills stopped at step 1. Found by running domain-init on Crytek (25 KB status). Independent adopt runs on scratch copies of FirstPersonShooter and the Crytek domain level (originals read-only): only the marker line and the index/pointer files differed, the index named the real generator (`crytek_index.py`), and findings were folded in (every `.md` file needs its own index row, never replace an existing INDEX, partial generator ownership, case-collision with `index.json`, pointer test, no-child-table and symlink/worktree reporting, session-start budget effect).
- Validator status check reads only the `**Status:**` value, ignores prose, treats known legacy words (drafted, planned, open, fixed, superseded, ...) as WARN instead of FAIL, and accepts a trailing date. Crytek FAILs 57 -> 41 with 9 WARNs, all remaining FAILs genuine size or header problems.

- `dna` plugin version 0.0.1 -> 0.1.0: ten skills (status, save-state, handoff, agentize, domain-init, crew, ship, plan, export-context, review-board) plus opt-in hooks. Installed plugins only update when this number changes, so bump it on each release. Bumped in both `plugin.json` and the `marketplace.json` entry; keep them equal.

- `AGENTS.md` carries the `<!-- dna:layer v1 -->` marker so the hooks act in this repo; `CLAUDE.md` trimmed under the tiny budget and its stale install instructions (old top-level `skills/` symlinks) replaced with `--plugin-dir` / marketplace install.

- `.agents/status.md` for this repo, written by `/dna:save-state` as the first real use of `status` and `save-state` (both run from a stale `dna@synced` copy with only those two skills; `dna@dnangelus` was installed afterwards). Goal, open questions and last-session summary; no epic.

- Skills `dna:plan` (draft-first POC plans: epic file + task table + cards only for delegated work, `references/epic-template.md`), `dna:export-context` (portable briefing for an external chat; secrets stripped always, sensitive nodes get an outline approval first; print, save only on request to `.agents/exports/`), `dna:review-board` (advisor plus 2-3 fresh-context cheap reviewers with distinct lenses, merged into one ranked verdict; builds on crew). Independent run of plan: epic with 6 tasks and 5 cards, validator OK, single-step request correctly stayed in status; findings folded in for plan (check existing work first, assumptions that change the task list count as blocking, Open questions section, Wave and Card columns, card fields aligned with the layer contract, status-update and extend-vs-create rules, English prose in non-English nodes). Independent run of export-context on two sensitive scratch copies (personal tax data; Crytek project): both treated as sensitive, outline step applied, leak scans clean; findings folded in (when-in-doubt tie-break, outline format and approval scope, no reading upward in sensitive trees, individuals' identifiers left out, stale-marking convention, cut order, save-path and gitignore advice). Independent run of review-board, which reviewed the `ship` skill with three cheap reviewers plus the advisor (about 10 tool calls, nothing edited). The board's own ship findings were applied: a PR word no longer implies a push, tags and releases need their own word, merge forbids `--auto`/`--admin` and names `--delete-branch` only on request, failing or pending checks stop the merge, merge state comes from `gh pr view`, cleanup requires a clean tree and no unpushed commits before any `-D`, shorter description. review-board itself: skip only when short and low-stakes (explicit request overrides), two reviewers for a targeted question, fewer findings preferred, grounded severity beats majority, merged list written before calling the advisor, read-only verified after.

- Skill `dna:ship`: commit (stage by name, detailed message, repo-required changelog), then push / PR / merge / post-merge cleanup each only on the user's explicit word. Direct commit on the default branch only where the repo's `AGENTS.md` says so; local cleanup uses `branch -d`, remote deletion only if asked. Trigger check: 3 of 3 commit/cleanup phrasings and 2 of 5 PR phrasings triggered ("create the PR" and "push this branch and open a PR" did; "open a pull request from this branch" did not, intermittent); description widened once. One independent run on a scratch repo with a bare remote (commit-only, branch-on-main rule, push, `--no-ff` cleanup, failing hook) found no safety slips; findings folded in: changelog drafted into the same commit, branch carries uncommitted edits, non-fast-forward push stops and asks, hook-failure handling, test-command discovery, fetch before cleanup and squash-merge `-d` refusal, attribution only when prescribed.

- Skill-index status values redefined as draft / tested / stable / archived; the six `dna` skills with an independent run are marked `tested`.

- Skill `dna:crew`: operator/advisor/workers operating mode (roles table, verification and single-writer rules, advisor points, worker brief shape, cost guidance without hard caps). Invocation counts as the user's opt-in to subagents; it does not widen commit/push permission. Writes nothing. Trigger check 3/3. One independent run (a small read-only lookup) found the mode too heavy for it; folded in: a "when not to use" section with a 5-call/200-line test, a two-line invocation answer, advisor skipped for small tasks, and which rules apply to read-only work. The advisor-fallback path is untested.

- Trigger check for `dna:agentize` and `dna:domain-init` with `claude -p --plugin-dir`: 4/4 natural prompts triggered the right skill; 2 near-miss prompts (add a README, explain the repo) triggered none.

- README rewritten for the marketplace layout (`plugins/dna/`, install commands, the dna layer, hooks opt-in); the old top-level `skills/` text is gone.

- Hooks `plugins/dna/hooks/` (`hooks.json` + stdlib `layer_hook.py`), opt-in: they act only where the nearest `AGENTS.md` carries `<!-- dna:layer v1 -->` (first 2 KB) and `.agents/status.md` exists; an unmarked nearer `AGENTS.md` means silence, so no tokens are spent in non-dna projects. SessionStart preloads `.memory/INDEX.md` head and `status.md`, capped at 8 KB. PreCompact shows a `systemMessage` reminder to run `/dna:save-state` when non-layer work is newer than `status.md`. No Stop hook (fires every turn). Never writes or blocks, always exits 0. `agentize` and `domain-init` now write the marker; the layer contract documents it. Verified by piping hook JSON, `claude plugin validate`, and a live `claude -p --plugin-dir` run where the model answered from the preloaded status. Existing layers (Crytek, AI, etc.) need the marker line added to opt in.

- Skill `dna:domain-init`: domain layer for a folder of projects (router `AGENTS.md`, status table with one row per child, `.memory/INDEX.md` and one card per child). Reads children, never writes into them; reuses agentize's no-loss rules. One independent run on a scratch copy of a six-child folder (children untouched by checksum, validator FAIL to OK); findings folded in (child and grouping detection, dormancy vs one-row-per-child, layer classes, card header and unknown-purpose rule, existing INDEX handling).

- Skill `dna:agentize` (+ `references/agents-template.md`): gives an existing project the tiny layer (router `AGENTS.md`, thin `CLAUDE.md` pointer, `.agents/status.md` seeded from README and git, inferred facts listed as open questions). Restructures a long `AGENTS.md` into a router after archiving the original verbatim to `.agents/archive/`. One independent run on a scratch copy of a real project (existing stub AGENTS.md/CLAUDE.md) passed validator 1 FAIL to 0; its findings were folded in (keep-branch appends routes and commands, strays left alone, language rule, CLAUDE.md pointer wording). A second run on a bloated 8.6 KB AGENTS.md (Crytek SandboxLLM copy) lost no text; its findings added a rule definition, a make-room order, the standard-stage target, an 8 KB budget for standard nodes and fixed archive wording.

- Skill `dna:handoff` (living + directional handoffs; write and consume modes; `references/templates.md`),
  draft; one independent subagent run (write to a child node, consume, archive, reply) passed and its
  ambiguities were fixed; trigger check 3/4 on natural prompts (the 4th is the intended throwaway-doc case). Distinct from the third-party `handoff` skill, which writes a throwaway doc to temp.

- `.gitignore`: excludes the owner's installed third-party skills (`.agents/skills/`, `.claude/`,
  `skills-lock.json`) per the no-vendoring decision; first commit of the repo.
- Skills `dna:status` (read-only recall) and `dna:save-state` (write half, with `references/routing.md`
  and `references/status-template.md`), draft. Tested by three independent subagents on scratch
  copies (Crytek layer for status; a tiny POC and a standard project with a real commit for
  save-state); their feedback was folded into both SKILL.md files (tiny quick path, epic
  threshold, domain handling, validator summary, budget-overflow rule). Description trigger loops
  (3 iterations each) gave NO signal: every positive query scored 0/3 triggers in all iterations,
  so the original descriptions are kept and the proposed rewrites were not applied. A real check
  afterwards (`claude -p --plugin-dir plugins/dna`, 5 prompts) triggered the right skill 4/4 on
  natural requests and nothing on a git-status near-miss, so the loop harness was the problem,
  not the descriptions. Not done: broader trigger set, hooks. Decision on commits in CONTEXT.md. Removed
  `plugins/dna/skills/.gitkeep`.

### Added

- `plugins/dna/references/layer-contract.md`: the dna layer contract (file set, ownership,
  byte budgets, growth stages tiny/standard/mature/domain, read/write rules, hook limits,
  token-cost rationale). Every project carries its own `AGENTS.md` and `.agents/`; `.memory/`
  appears when it grows. Decisions in CONTEXT.md. Not done: no skill or hook written; the
  workspace `~/Code/AGENTS.md` §2 amendment is outside this repo.
- `plugins/dna/scripts/validate_layer.py`: stdlib-only, read-only validator (budgets, `when:`
  headers, naming, index coverage, stage detection, `--legacy`, `--json`). Run against Crytek
  (fails on its 24 KB status file, as intended), AI/prompt-spine and a tiny fixture.

### Changed

- Repo moved from `~/Code/dnangelus/ai-skills` to `~/Code/dna/ai-skills`; `dnangelus/` removed.
  Layout is now `plugins/<prefix>/skills/<skill>/` (was top-level `skills/`). `AGENTS.md` and
  `CONTEXT.md` updated; decisions in CONTEXT.md. Workspace `CLAUDE.md` and `.memory/INDEX.md`
  paths fixed. README still describes the old layout (not updated yet).

### Added

- `ROADMAP.md`: resolved decisions, build order (layer contract first) and the Session 0 brief.
- Marketplace scaffold: `.claude-plugin/marketplace.json` (plugins `dna` and third-party
  `mattpocock-skills` via `source: github`) and `plugins/dna/.claude-plugin/plugin.json`. No
  skills written yet; `plugins/dna/skills/` is empty. `pla` plugin deliberately not created yet.
- `ROADMAP.md` — ten candidate skills ranked from mining 1,432 prompts of past sessions, plus
  working-style notes and open questions. Draft, not yet confirmed by owner.
- `CHANGELOG.md` — this file, backfilled with the repo's history to date.
- Changelog upkeep is now a repo rule in `AGENTS.md`: a change is incomplete until its entry
  is written.

## [0.0.1] — 2026-08-18

Repo initialized as a blank sheet: a place to collect the AI skills in daily use, with one
source of truth across agents and machines.

### Added

- `package.json` — metadata only (name `ai-skills`, MIT, repo `DNAngeluS/ai-skills`,
  `main: AGENTS.md`). No build, no dependencies; the `test` script is a placeholder that
  exits 1 by design.
- `AGENTS.md` — canonical provider-neutral rules: the `skills/<name>/SKILL.md` +
  `references/` / `scripts/` / `evals/` layout, mandatory frontmatter, keep `SKILL.md` short
  and lazy-load the rest, stay provider-neutral, ground skills in a project's own files, no
  client-confidential material, and index every skill you add.
- `CONTEXT.md` — purpose, dated decisions log, the skill index table (empty at creation), the
  list of user-scope skills that are candidates to migrate in, and open questions.
- `CLAUDE.md` — thin Claude Code pointer to `AGENTS.md`, plus Claude-only mechanics:
  symlink-don't-copy for live testing, `/<skill-name>` invocation, `skill-creator` for
  scaffolding.
- `README.md` — human-facing entry point: what a skill is, install-by-symlink commands, how to
  add one, license.
- `skills/` — empty directory awaiting the first migrated skill.

### Decided

- Multi-agent by default: rules live in `AGENTS.md`, provider files are thin pointers.
- Four root docs with distinct audiences (agents / Claude / project context / humans).
- Skills are directories, not single files, so they symlink into an agent's skills path
  unmodified.

Full reasoning: [CONTEXT.md § Decisions](CONTEXT.md#decisions).

### Not done

- No git repository initialized yet, despite `package.json` naming a GitHub remote.
- `khem-project-docs` and `plan-to-board` still live only at user scope under
  `~/.claude/skills/`; migration is pending a scrub of client-facing material.
