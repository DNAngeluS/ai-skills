#!/usr/bin/env python3
"""Validate a directory against the dna layer contract (plugins/dna/references/layer-contract.md).

Read-only, stdlib only.
Usage: python3 -I validate_layer.py <dir> [--json] [--legacy]
Exit 0 = clean or warnings only, 1 = at least one fail.
"""
import json
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

KB = 1024
BUDGET = {  # bytes, per contract
    "AGENTS.md": 8 * KB, "CLAUDE.md": int(1.5 * KB), ".agents/status.md": 4 * KB,
    ".memory/INDEX.md": 6 * KB,
}
DIR_BUDGET = {  # (dir, glob) -> bytes
    ".agents/epics": 6 * KB, ".agents/tasks": 4 * KB, ".agents/handoffs": 4 * KB,
    ".agents/plans": 8 * KB, ".agents/workflows": 8 * KB,
    ".memory/cards": 3 * KB, ".memory/decisions": 3 * KB, ".memory/projects": 2 * KB,
}
LIVING_HANDOFF = 3 * KB
TINY_AGENTS = 6 * KB
SESSION_START = 12 * KB
EXEMPT = {"runs", "archive", ".cache", "scripts", "skills", "templates", "tools", "instructions"}
NAMING = {
    ".agents/epics": re.compile(r"^EPIC-[a-z0-9][a-z0-9-]*\.md$"),
    ".agents/tasks": re.compile(r"^TASK-[a-z0-9][a-z0-9-]*-\d{2,}\.md$"),
    ".memory/decisions": re.compile(r"^DEC-\d{2,}-[a-z0-9][a-z0-9-]*\.md$"),
}
DIRECTIONAL = re.compile(r"^(to|from)-.*?(\d{4}-\d{2}-\d{2})")
STATUS_OK = {"todo", "in-progress", "blocked", "done"}
WHEN = re.compile(r"^\s*<!--\s*when:", re.I)


class Report:
    def __init__(self, legacy):
        self.legacy, self.items = legacy, []

    def fail(self, path, msg):
        self.items.append(("warn" if self.legacy else "fail", str(path), msg))

    def warn(self, path, msg):
        self.items.append(("warn", str(path), msg))

    @property
    def failed(self):
        return any(k == "fail" for k, _, _ in self.items)


def size(p):
    return p.stat().st_size


def md_files(root):
    if not root.is_dir():
        return []
    return [p for p in sorted(root.rglob("*.md"))
            if not (set(p.relative_to(root).parts[:-1]) & EXEMPT)]


def check(root, r):
    agents = root / "AGENTS.md"
    status = root / ".agents/status.md"
    if not agents.is_file():
        r.fail("AGENTS.md", "missing")
    if not status.is_file():
        r.fail(".agents/status.md", "missing")

    for rel, limit in BUDGET.items():
        p = root / rel
        if p.is_file() and size(p) > limit:
            r.fail(rel, f"{size(p)} bytes, budget {limit}")

    has_memory = (root / ".memory").is_dir()
    if agents.is_file() and not has_memory and size(agents) > TINY_AGENTS:
        r.warn("AGENTS.md", f"{size(agents)} bytes without .memory/: outgrown tiny stage (budget {TINY_AGENTS})")

    for rel, limit in DIR_BUDGET.items():
        for p in md_files(root / rel):
            lim = LIVING_HANDOFF if rel.endswith("handoffs") and not p.name.startswith(("to-", "from-")) else limit
            if size(p) > lim:
                r.fail(p.relative_to(root), f"{size(p)} bytes, budget {lim}")

    for rel, rx in NAMING.items():
        for p in md_files(root / rel):
            if p.name != "index.md" and not rx.match(p.name):
                r.fail(p.relative_to(root), f"name does not match {rx.pattern}")

    for sub in (".agents", ".memory"):
        for p in md_files(root / sub):
            with p.open(encoding="utf-8", errors="replace") as f:
                first = f.readline()
            if not WHEN.match(first):
                r.fail(p.relative_to(root), "first line must be <!-- when: ... -->")

    for rel in (".agents/epics", ".agents/tasks"):
        for p in md_files(root / rel):
            m = re.search(r"\*\*Status:\*\*\s*([A-Za-z-]+)", p.read_text(encoding="utf-8", errors="replace"))
            if m and m.group(1).lower() not in STATUS_OK:
                r.fail(p.relative_to(root), f"status '{m.group(1)}' not in {sorted(STATUS_OK)}")

    index = root / ".memory/INDEX.md"
    if has_memory and not index.is_file():
        r.fail(".memory/INDEX.md", "missing while .memory/ exists")
    if index.is_file():
        text = index.read_text(encoding="utf-8", errors="replace")
        for p in md_files(root / ".memory"):
            rel = p.relative_to(root / ".memory")
            if rel.name != "INDEX.md" and rel.name not in text and str(rel) not in text:
                r.fail(Path(".memory") / rel, "not listed in .memory/INDEX.md")

    cutoff = datetime.now() - timedelta(days=14)
    for p in md_files(root / ".agents/handoffs"):
        m = DIRECTIONAL.match(p.name)
        if m:
            try:
                if datetime.strptime(m.group(2), "%Y-%m-%d") < cutoff:
                    r.warn(p.relative_to(root), "directional handoff older than 14 days: consume and archive")
            except ValueError:
                pass

    start = [p for p in (agents, index, status) if p.is_file()]
    total = sum(size(p) for p in start)
    if total > SESSION_START:
        r.fail("session-start set", f"{total} bytes (AGENTS.md + INDEX.md + status.md), budget {SESSION_START}")

    children = [d for d in sorted(root.iterdir())
                if d.is_dir() and not d.name.startswith(".") and (d / "AGENTS.md").is_file()]
    if len(children) >= 2 and not (root / ".memory/projects").is_dir():
        r.warn("layout", f"{len(children)} child nodes with AGENTS.md but no .memory/projects/: domain stage reached")
    for d in children:
        if not (d / ".agents").is_dir():
            r.warn(d.relative_to(root), "child has AGENTS.md but no .agents/")
    return stage(root, has_memory, len(children))


def stage(root, has_memory, n_children):
    if n_children >= 2:
        return "domain"
    if has_memory:
        return "mature"
    if any((root / ".agents" / d).is_dir() for d in ("epics", "tasks", "handoffs")):
        return "standard"
    return "tiny"


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    if len(args) != 1 or not Path(args[0]).is_dir():
        print(__doc__)
        return 2
    r = Report("--legacy" in argv)
    st = check(Path(args[0]).resolve(), r)
    if "--json" in argv:
        print(json.dumps({"stage": st, "items": [dict(level=k, path=p, msg=m) for k, p, m in r.items]}, indent=1))
    else:
        print(f"stage: {st}")
        for k, p, m in r.items:
            print(f"{k.upper():5} {p}: {m}")
        print("FAIL" if r.failed else "OK")
    return 1 if r.failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
