<!-- when: start of any session in ai-skills; the current state, overwritten each save -->
# Status — 2026-11-02

**Goal now:** Maintain the `dnangelus` marketplace and its `dna` plugin (agent context layer: skills, hooks, contract). The roadmap build order is complete; the work now is real use and fixing what use reveals.
**Stage:** tiny · **Branch/head:** main @ c2285d4, clean after the next commit

## Open questions (need the user)
1. `ship` triggers on only 2 of 5 pull-request phrasings; check in a live session whether it needs a stronger description.
2. The `crew` advisor fallback (fresh worker as reviewer when no advisor tool exists) is untested.
3. Add `<!-- dna:layer v1 -->` to the `AGENTS.md` of Crytek, AI and other layers so the hooks act there (done for this repo). Nothing has been run against the real Crytek layers yet.

## Last session (2026-11-02)
- Built and pushed all skills: status, save-state, handoff (454fa78, 727e495), agentize (2290a28), domain-init (f83c264), opt-in hooks (00443b0), crew (dce2fb7, 2225c3f), ship/plan/export-context/review-board (c2285d4).
- Each skill had at least one independent run on scratch copies; the CONTEXT.md index marks them `tested`. None is `stable` yet (needs real use).
- First real use: `/dna:status` and `/dna:save-state` run on this repo from the installed marketplace copy.
- Added the hook marker to this repo's AGENTS.md and trimmed CLAUDE.md to clear the validator.
