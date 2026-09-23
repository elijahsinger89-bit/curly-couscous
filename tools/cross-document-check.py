#!/usr/bin/env python3
"""
G-56 CHECK. THE CROSS-DOCUMENT DEPENDENCY GRAPH.

G-50 makes every section state what must be true before it and what is true
after it. Every document's own check reads only its own blocks, so a cycle
whose arcs lie in two documents passes both checks. This builds ONE graph
from ALL of them and runs the same test against the union.

IT FINDS: cycles, and preconditions no postcondition anywhere produces.
IT DOES NOT FIND: a fact two documents jointly imply and neither states.
That is a different defect and this check is blind to it.

Reads the files. Writes nothing. Exit 1 if it finds anything.
"""
import re, sys, os, itertools

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# (file, node prefix, section-heading regex, pre-block marker, post-block marker)
DOCS = [
    ("build-book.md",            "D1", r"^## (\d+)\.\s+(.*)$",
     r"MUST BE TRUE BEFORE THIS SECTION STARTS", r"TRUE AFTER IT ENDS"),
    ("commissioning-checklist.md","D8", r"^## (\d+)\.\s+(.*)$",
     r"MUST BE TRUE BEFORE THIS STAGE STARTS",   r"TRUE AFTER THIS STAGE ENDS"),
    ("wiring-instructions.md",   "D4", r"^## PAGE (\d+)[.:]?\s*(.*)$",
     r"MUST BE TRUE BEFORE",                     r"TRUE AFTER"),
]

def bullets(lines, i):
    """Collect the bullet list that follows a marker line.

    A bullet may wrap onto indented continuation lines. Joining them matters:
    BB-09 lives on the wrap of BB-08's bullet, and a parser that stops at the
    first non-bullet line silently loses it - which is this check's own version
    of the defect it exists to find."""
    out, j = [], i + 1
    while j < len(lines):
        raw = lines[j]
        s = raw.strip()
        if not s:
            j += 1
            if out: break
            continue
        if s.startswith(('-', '*')):
            out.append(s.lstrip('-* ').strip()); j += 1; continue
        if out and raw[:1] in ' \t':
            out[-1] += ' ' + s; j += 1; continue
        break
    return out

def parse(path, prefix, head_re, pre_re, post_re):
    if not os.path.exists(path): return {}
    lines = open(path, encoding='utf-8').read().split('\n')
    head = re.compile(head_re)
    secs, cur = {}, None
    for i, ln in enumerate(lines):
        m = head.match(ln)
        if m:
            cur = f"{prefix}§{m.group(1)}"
            secs[cur] = {"title": m.group(2).strip(), "pre": [], "post": [], "line": i + 1}
            continue
        if cur is None: continue
        if re.search(pre_re, ln):  secs[cur]["pre"]  += bullets(lines, i)
        if re.search(post_re, ln): secs[cur]["post"] += bullets(lines, i)
    return secs

secs = {}
for f, p, h, a, b in DOCS:
    secs.update(parse(os.path.join(ROOT, f), p, h, a, b))

# --- where each id is PRODUCED -------------------------------------------
produced = {}                       # id -> node that makes it true
for node, s in secs.items():
    for t in s["post"]:
        for bb in re.findall(r'\bBB-\d+\b', t):
            produced.setdefault(bb, node)

# a D8 stage produces every C- row it contains
raw8 = open(os.path.join(ROOT, "commissioning-checklist.md"), encoding='utf-8').read()
stage_of_c = {}
cur = None
for ln in raw8.split('\n'):
    m = re.match(r'^## (\d+)\.\s', ln)
    if m: cur = f"D8§{m.group(1)}"
    elif cur:
        for c in re.findall(r'\bC-\d\d\b', ln):
            stage_of_c.setdefault(c, cur)

# a D8 stage number is not its section number: stage N is section N+1
stage_node = {}
for ln in raw8.split('\n'):
    m = re.match(r'^## (\d+)\.\s+STAGE (\d+)\b', ln)
    if m: stage_node[m.group(2)] = f"D8\u00a7{m.group(1)}"

# --- edges ----------------------------------------------------------------
edges, unmatched = [], []
for node, s in secs.items():
    doc = node.split('§')[0]
    for t in s["pre"]:
        hits = []
        for bb in re.findall(r'\bBB-\d+\b', t):
            if bb in produced and produced[bb] != node:
                hits.append((produced[bb], bb))
        for dn, sn in re.findall(r'\bD1 section (\d+)|\bD1 §(\d+)', t):
            n = f"D1§{dn or sn}"
            if n in secs and n != node: hits.append((n, f"D1 section {dn or sn}"))
        for c in re.findall(r'\bC-\d\d\b', t):
            if c in stage_of_c and stage_of_c[c] != node:
                hits.append((stage_of_c[c], c))
        for g in re.findall(r'[Ss]tage (\d+) closed|GATE (\d+) passed', t):
            k = g[0] or g[1]
            n = stage_node.get(k)
            if n and n != node: hits.append((n, f"stage {k}"))
        if hits:
            for src, via in hits:
                edges.append((src, node, via, t[:110]))
        else:
            unmatched.append((node, t[:130]))

# --- cycles ---------------------------------------------------------------
adj = {}
for src, dst, via, _ in edges: adj.setdefault(src, []).append((dst, via))
cycles, seen = [], set()
def walk(start, node, path, vias):
    for nxt, via in adj.get(node, []):
        if nxt == start:
            key = tuple(sorted(path + [node]))
            if key not in seen:
                seen.add(key); cycles.append((path + [node], vias + [via]))
        elif nxt not in path and len(path) < 12:
            walk(start, nxt, path + [node], vias + [via])
for n in list(adj): walk(n, n, [], [])

# --- report ---------------------------------------------------------------
print(f"NODES {len(secs)}   EDGES {len(edges)}   CROSS-DOCUMENT EDGES "
      f"{sum(1 for s,d,_,_ in edges if s.split(chr(0xa7))[0] != d.split(chr(0xa7))[0])}")
print()
if unmatched:
    print("=" * 78)
    print("THE GRAPH IS INCOMPLETE. THE CYCLE RESULT BELOW IS NOT A CLEAN BILL.")
    print(f"{len(unmatched)} preconditions name a state in prose and no postcondition")
    print("anywhere claims to produce it. Each is a MISSING ARC. A cycle whose arcs")
    print("are missing cannot be found, and the detector prints 0 either way.")
    print("ZERO HERE MEANS NOT YET LOOKED, NOT NONE.")
    print("=" * 78)
    print()
print(f"CYCLES: {len(cycles)}" + ("   <- ON AN INCOMPLETE GRAPH" if unmatched else ""))
for path, vias in cycles:
    docs = {p.split('§')[0] for p in path}
    print(f"  {'CROSS-DOCUMENT' if len(docs) > 1 else 'within ' + list(docs)[0]:>16}  "
          + " -> ".join(path) + f" -> {path[0]}")
    for v in vias: print(f"                      via {v}")
print()
print(f"PRECONDITIONS NO POSTCONDITION ANYWHERE PRODUCES: {len(unmatched)}")
for node, t in unmatched: print(f"  {node:<8} {t}")
sys.exit(1 if (cycles or unmatched) else 0)
