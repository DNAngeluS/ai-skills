---
name: review-board
description: Critical review of a plan, design or proposal by a small board: the advisor plus two or three fresh-context cheap reviewers, each with a different lens (correctness and gaps, risk and failure modes, simplicity and cost), merged into one ranked verdict. Use whenever the user says "review this plan", "board of experts", "stress-test this design", "poke holes in this", "second opinions on this proposal", "audit this plan before we build", "revisá este plan", "qué le ves de malo a esto". Reviews documents and designs, not code diffs (use code-review for those). Writes nothing unless asked.
---

# review-board

A plan reviewed only by its author misses what a cold reader would catch. The board gives the work cold readers with different questions, then the operator merges them. It builds on the rules of [../crew/SKILL.md](../crew/SKILL.md): reports are claims, workers read and report but do not edit.

## Rules

- **Review the artifact, not the author.** Reviewers get the document and its context, not your opinion of it, so they are not anchored.
- **Different lenses, not three copies.** Default board: (1) correctness and gaps: does it do what it claims, what is missing or contradictory; (2) risk: what fails, what is irreversible or costly to undo, hidden dependencies; (3) simplicity and cost: what can be cut or done cheaper. Add a lens only when the artifact calls for it (security, migration, UX).
- **Small and cheap.** Name the cheapest capable model (and lower effort) in each Agent call; run reviewers in the background in the same turn. Default two reviewers when the user asked one targeted question (the question is lens one, an orthogonal lens is lens two), three for an open-ended review. Skip the board only when the document is both short and low-stakes (roughly under 50 lines and nothing outward-facing or irreversible depends on it), and say so and review it yourself; an explicit "board" request from the user overrides the skip.
- **Findings must be checkable.** Each cites the part of the document it concerns and says what would fix it. "Could be better" is not a finding. Ask for up to 8, fewer is better; padding is worse than silence.

## Steps

1. Identify the artifact (file path or text) and its stakes. Copy sensitive material to a scratch location if reviewers will read it; never give them write access.
2. Brief each reviewer self-contained: the artifact's path, its goal, their lens, "read only, do not edit", and the report shape: up to 8 findings (fewer if that is all there are), each as `severity (blocker | should | nit) · where · problem · fix`, then a 3-line overall view.
3. When they return, check every blocker against the document yourself. Drop findings you cannot ground; merge duplicates. If reviewers disagree on severity, your grounded severity wins, not the majority; note the split. Verify nothing was edited (modification time or `git diff`): read-only is enforced by the brief, so check it.
4. Write the merged list in your message first (the advisor only sees the transcript), then call the advisor and ask what is missing or wrongly ranked.
5. Deliver one verdict: ship as is / fix the blockers first / rethink, then the ranked findings (blockers first), noting where reviewers disagreed and what you decided. Apply fixes or record them only if the user asks.

## Never

- Pass a reviewer's severity along unverified.
- Let reviewers edit the artifact.
