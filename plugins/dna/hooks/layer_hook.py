#!/usr/bin/env python3
"""dna layer hooks. Stdlib only, never writes, never blocks (always exit 0).

  session-start  print INDEX head + status.md of the nearest node, byte-capped
  pre-compact    remind (systemMessage) to run /dna:save-state when status is stale

Only acts in nodes whose nearest AGENTS.md carries the dna:layer marker.

Contract: plugins/dna/references/layer-contract.md (Hooks).
"""
import json, os, subprocess, sys
from pathlib import Path

CAP = 8000        # bytes printed at session start (contract session-start budget is 12 KB incl. AGENTS.md)

MARK = "dna:layer"   # opt-in marker, e.g. <!-- dna:layer v1 --> in the first lines of AGENTS.md

def node_of(cwd):
    """Nearest ancestor with an AGENTS.md decides: marked = our node, unmarked = stay silent."""
    for d in [Path(cwd), *Path(cwd).parents]:
        a = d / "AGENTS.md"
        if a.is_file():
            head = read(a, 2000)
            ok = MARK in head and (d / ".agents" / "status.md").is_file()
            return d if ok else None
        if d == Path.home():
            break
    return None

def read(p, limit):
    try:
        return p.read_bytes()[:limit].decode("utf-8", "replace")
    except OSError:
        return ""

def stale(node):
    """True if tracked/untracked work outside the layer is newer than status.md."""
    st = (node / ".agents" / "status.md").stat().st_mtime
    try:
        out = subprocess.run(["git", "-C", str(node), "status", "--porcelain"],
                             capture_output=True, text=True, timeout=5).stdout
    except Exception:
        return False
    for line in out.splitlines():
        rel = line[3:].split(" -> ")[-1].strip('"')
        if rel.startswith((".agents/", ".memory/")):
            continue
        try:
            if (node / rel).stat().st_mtime > st:
                return True
        except OSError:
            continue
    return False

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    try:
        data = json.load(sys.stdin)
    except Exception:
        data = {}
    node = node_of(data.get("cwd") or os.getcwd())
    if not node:
        return
    if mode == "session-start":
        parts = []
        idx = node / ".memory" / "INDEX.md"
        if idx.is_file():
            parts.append(f"## {idx.relative_to(node)}\n" + read(idx, 2500))
        parts.append("## .agents/status.md\n" + read(node / ".agents" / "status.md", CAP))
        text = f"[dna] layer of {node.name} (read-only preload; /dna:status for more)\n\n" + "\n\n".join(parts)
        b = text.encode()
        if len(b) > CAP:
            text = b[:CAP].decode("utf-8", "ignore") + "\n[truncated by dna hook]"
        print(text)
    elif mode == "pre-compact" and stale(node):
        msg = ("dna: work in " + node.name + " is newer than .agents/status.md. "
               "Run /dna:save-state before clearing or compacting.")
        print(json.dumps({"systemMessage": msg}))

if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
