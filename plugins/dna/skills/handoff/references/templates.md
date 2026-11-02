<!-- when: handoff is writing a living or directional handoff file -->
# Handoff templates

## Living (`.agents/handoffs/<epic>.md`, overwritten, ≤3 KB)
```markdown
<!-- when: resuming EPIC-<slug>; overwritten at the end of each session -->
# Handoff: <epic> (state at <YYYY-MM-DD>)
Read first: [epic](../epics/EPIC-<slug>.md)
- **State:** <what is done / in progress, with commit hashes>
- **Next:** <exact command or step>
- **Gotchas:** <what cost time; what not to touch>
- **Running/locked:** <processes, ports, branches, shared resources, or "nothing">
```

## Directional (`<receiver>/.agents/handoffs/to-<receiver>-<date>-<topic>.md`, ≤4 KB)
```markdown
<!-- when: <receiver> starts or resumes and needs to know <topic>; written <date> by <sender> -->
# To <receiver>: <topic> (<YYYY-MM-DD>)
**From:** <sender node + path>. **Why you are reading this:** <one sentence>.
## Facts (verified)
1. <claim> — evidence: <command / path / commit>
## Unverified
- <claim and why it is unverified>
## Please do
1. <action>, done when <observable check>
## I did not do
- <what is left alone and why>
## Reply
<where to answer: a `from-` note in my `.agents/handoffs/`, or "none needed">
```
Receiver: after acting, `git mv` this file to `.agents/archive/`.
