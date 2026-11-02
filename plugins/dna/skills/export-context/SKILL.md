---
name: export-context
description: Build a portable briefing from a project's current state to paste into an external chat (Grok, ChatGPT, Gemini web, a colleague): what the project is, where it stands, the question being asked, and the few facts the other side needs. Strips secrets always and, for sensitive nodes, shows an outline and waits for approval before producing text. Prints it in chat; saves only when asked. Use whenever the user says "create a context md to throw into a conversation", "export the context", "brief another model", "I want to ask Grok/ChatGPT about this", "summarize this project for an external chat", "contexto para pegar en otro chat", "armá un resumen para pasarle a otro modelo".
---

# export-context

The text leaves the machine, so two things matter more than completeness: **it must not leak**, and **it must let a reader with no access answer the user's question**. Short beats exhaustive.

## Rules

- **Strip secrets always:** values from `.env`, tokens, keys, passwords, private URLs, internal hostnames, machine paths under a home directory. Refer to a config by its role, never its value.
- **Sensitive node check first.** Treat a node as sensitive if it holds client or audit data, personal data (names, tax or ID numbers, finances), NDA or "private" markers, or sits in a client tree; when in doubt, it is sensitive, and a user's own personal project counts if it contains other people's or their own financial data. Do not produce the briefing yet: print an outline in chat (it is not an export) listing what you will include, what you leave out, and the estimated size, and wait for the user's OK. Approval covers that outline: trimming or shortening is fine, adding anything not in the outline needs a new OK, and "OK but also X" is a revised outline you restate briefly.
- **Never read upward or sideways in a sensitive tree.** Domain-level `AGENTS.md`, handoffs addressed to a client, relays and `.private/` stay out unless the user names them. Names, ID numbers and institution names of individuals are left out by default; use roles ("the taxpayer").
- **Facts from files, not memory:** `AGENTS.md`, `.agents/status.md`, the relevant epic, `README.md`, and `.memory/INDEX.md` if present. Mark what is older than the node's last commit, or contradicted by another source, inline as "(as of <date>, unverified)".
- **Print, don't scatter.** Output is one Markdown block the user can copy. Save only if asked, to `.agents/exports/<yyyy-mm-dd>-<topic>.md` with a `when:` header, one line in `.memory/INDEX.md` or, without one, the `AGENTS.md` routes; for a sensitive node confirm first and suggest (do not make) a `.gitignore` entry for `.agents/exports/`. Never send anything anywhere.
- **Ask for the question.** If the user did not say what they want the other model to do, ask once, in the same message as the outline when one is needed. If the question is ambiguous and the sources do not settle it, say what is unknown in the briefing instead of guessing.

## Steps

1. Resolve the node; read the sources above (read-only). Run the sensitive-node check.
2. Compose, in this order, within about 3 KB unless the user asks for more; when over, cut excerpts first, then background, and keep the Ask and the measured facts the question depends on: **Ask** (the question, first, so it is not buried) → **What this is** (2-3 lines) → **Where it stands** (state, decisions that constrain answers, what was tried and failed) → **Constraints** (stack, rules the answer must respect) → **Useful excerpts** (only the code or text the question needs, trimmed).
3. Scan the result for secrets and private paths once more, then print it. Tell the user what you left out and why.
4. Save only on request.

## Never

- Include raw logs, whole files or the layer's file tree "for context".
- Paste content from a sensitive node without the outline approval.
