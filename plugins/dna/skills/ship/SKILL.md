---
name: ship
description: Deliver a git change cleanly: stage only what belongs, write a detailed commit message with the changelog entry the repo requires, and, only when explicitly asked, push, open a pull request, merge, and clean up after the merge. Use for any git delivery step (commit, push, PR, merge, post-merge cleanup) in a repository, e.g. "ship it", "commit this", "commit and push", "open a pull request", "create the PR", "it's merged, clean up", "hacé el commit", "subí los cambios".
---

# ship

Turn a finished change into history, one outward step at a time. The inward step (commit) is easy to undo; the outward ones (push, PR, merge, remote deletion) are not, so each needs the user's explicit word and one approval never covers the next.

## What an invocation authorizes

| User said | You may |
|---|---|
| "ship", "commit" | prepare and make the commit |
| "push", "commit and push" | the above, then push the current branch |
| "open a PR" | create the PR only. If the branch is not on the remote, stop and ask for the push word |
| "merge" | merge that PR, as reviewed (re-check the head commit has not changed since you reported its state) |
| "merged, clean up" | local cleanup (below); delete the remote branch only if named |
| "release", "tag" | create a tag or release only on its own explicit word |

If the user's wording is ambiguous, ask once. Never infer a push from "ship".

## Commit

1. **Look first.** `git status --short`, `git diff --stat`, current branch and default branch. Read the repo's `AGENTS.md`/`CLAUDE.md` for commit, changelog and branching rules.
2. **Branch.** On the default branch, commit directly only if the repo's `AGENTS.md` says that is how it works; otherwise `git switch -c <type>/<short-slug>` (uncommitted edits come along) and tell the user before committing. A later push of that branch needs its own word.
3. **Stage by name, never `git add -A` blindly.** Include only files that belong to the change. Leave out unrelated work, scratch files, and anything secret (`.env`, keys, tokens); say what you left out, ask once if a file's status is unclear, and suggest (do not make) a `.gitignore` entry for secrets. If the repo requires a changelog entry with every change and none is staged, draft it from the diff in the file's own format and place (newest first, under Unreleased), stage it in the same commit, and mention it in your report.
4. **Message.** Imperative subject under about 72 characters; a body saying what changed and why, not a file list restated; mention evidence (tests run, runs done) only if it actually happened. End with the attribution lines the environment or `CLAUDE.md` prescribes; if none are prescribed, add none. Pass it with a heredoc.
5. **Never** amend, force, skip hooks (`--no-verify`) or rewrite history unless the user asks. If a hook fails nothing was committed and the staged state stays as it is: fix the cause if it is in your change, re-stage and commit again. If the cause is outside the change (a broken hook, a missing tool), do not edit the hook; report its output and stop.
6. **Check, then show.** Find the project's test command (`AGENTS.md`, README, manifest) and run it if it is cheap; otherwise say plainly that tests were not run. Show `git log -1 --stat`, what was staged and what was left out.

## Push, PR, merge

- **Push:** set the upstream on first push; never force-push; never push to the default branch unless the repo's rules say that is the workflow and the user asked. Report the pushed range. If the push is rejected as non-fast-forward, stop: `git fetch`, show how the branches diverge, and ask whether to rebase or merge; do neither unasked.
- **PR:** `gh pr create` with a title and a body (what, why, how it was checked, anything the reviewer must know). Target the default branch. Return the URL.
- **Merge:** only on the explicit word, with the repo's usual method (ask if unknown). Check the PR state and required checks first; if any check is failing or pending, stop and ask. Never use `--auto` or `--admin`, and `--delete-branch` only if the user named it.

## Clean up after a merge

Confirm the merge happened with `gh pr view --json state,mergedAt` (use `git branch --merged <default>` only for a purely local merge; it is unreliable after squash). Require a clean working tree first. Then: `git fetch --prune`, switch to the default branch, `git pull --ff-only` (say if local is ahead of origin), and delete the merged local branch with `git branch -d`. After a squash or rebase merge `-d` refuses because the commits differ: report that, and offer `-D` only once you have confirmed the PR is merged and the user says so and `git log <branch> --not --remotes` shows no unpushed commits. The change's own changelog entry already went in with its commit; here only bring status files up to date (run `save-state` when the repo has the dna layer) and do not create a tag or release (that needs its own word). Delete the remote branch only if the user asked.

## Never

- Commit secrets, or unrelated changes that happened to be in the tree.
- Claim tests passed that you did not run, or claim a push or merge that did not happen; verify with `git log`/`git status` before saying done.
