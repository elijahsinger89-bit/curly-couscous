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
    ("build-book.md",            "D1", r"^## (\d+[a-z]?)\.\s+(.*)$",
     r"MUST BE TRUE BEFORE THIS SECTION STARTS", r"TRUE AFTER IT ENDS"),
    ("commissioning-checklist.md","D8", r"^## (\d+[a-z]?)\.\s+(.*)$",
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
        # A BULLET IS '- ' OR '* ', NEVER '**'. A continuation line that opens with
        # markdown bold reads as a list marker to a naive startswith, and the bullet
        # splits in two. That produced two of this check's own false findings.
        if re.match(r'^[-*]\s', s):
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

# A precondition may carry an explicit PRODUCER tag naming what makes it true, or
# saying that nothing does and why. Untagged preconditions are the ones this check
# cannot reason about at all.
KINDS = ("PRODUCED", "INVARIANT", "LOOKUP", "OPEN ROW", "RULE", "OPERATOR",
         "DECISION", "SOFTWARE STATE", "UNPRODUCED")
def kinds_in(t):
    u = t.upper()
    return [k for k in KINDS if "PRODUCER:" in u and k in u.split("PRODUCER:", 1)[1]]

# --- edges ----------------------------------------------------------------
edges, unmatched, tagged, gaps = [], [], [], []
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
        ks = kinds_in(t)
        for src, via in hits:
            edges.append((src, node, via, t[:110]))
        if ks:
            tagged.append((node, ks, t[:120]))
            if "UNPRODUCED" in ks:
                gaps.append((node, t[:150]))
        elif not hits:
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

# 21 paths round one loop is one defect, not 21. Group the cycles into strongly
# connected components so the headline counts DEFECTS and the paths stay available
# underneath it. A count that inflates with the graph's density is a count nobody
# can act on.
def sccs():
    plain = {k: [d for d, _ in v] for k, v in adj.items()}
    rev = {}
    for k, vs in plain.items():
        for v in vs: rev.setdefault(v, []).append(k)
    order, seen_n = [], set()
    def push(n):
        stack = [(n, iter(plain.get(n, [])))]
        seen_n.add(n)
        while stack:
            v, it = stack[-1]
            for w in it:
                if w not in seen_n:
                    seen_n.add(w); stack.append((w, iter(plain.get(w, [])))); break
            else:
                order.append(stack.pop()[0])
    for n in set(list(plain) + [x for v in plain.values() for x in v]): 
        if n not in seen_n: push(n)
    comp, assigned = [], set()
    for n in reversed(order):
        if n in assigned: continue
        grp, stack = [], [n]; assigned.add(n)
        while stack:
            v = stack.pop(); grp.append(v)
            for w in rev.get(v, []):
                if w not in assigned: assigned.add(w); stack.append(w)
        if len(grp) > 1: comp.append(sorted(grp))
    return comp
clusters = sccs()

# --- report ---------------------------------------------------------------
print(f"NODES {len(secs)}   EDGES {len(edges)}   CROSS-DOCUMENT EDGES "
      f"{sum(1 for s,d,_,_ in edges if s.split(chr(0xa7))[0] != d.split(chr(0xa7))[0])}")
print()
if unmatched:
    print("=" * 78)
    print("THE GRAPH IS INCOMPLETE. THE CYCLE RESULT BELOW IS NOT A CLEAN BILL.")
    print(f"{len(unmatched)} preconditions carry neither a resolved reference nor a")
    print("PRODUCER tag. Each is an arc this check cannot see, and a cycle whose arcs")
    print("are missing cannot be found. ZERO HERE WOULD MEAN NOT YET LOOKED, NOT NONE.")
    print("=" * 78)
    print()
print(f"CYCLIC CLUSTERS: {len(clusters)}   ({len(cycles)} distinct paths round them)"
      + ("   <- ON AN INCOMPLETE GRAPH" if unmatched else ""))
for c in clusters:
    docs = {n.split('\u00a7')[0] for n in c}
    print(f"  {'CROSS-DOCUMENT' if len(docs) > 1 else 'within one document':>20}: "
          + ", ".join(c))
print()
print(f"PATHS: {len(cycles)}")
for path, vias in cycles[:6]:
    docs = {p.split('\u00a7')[0] for p in path}
    print(f"  {'CROSS-DOCUMENT' if len(docs) > 1 else 'within ' + list(docs)[0]:>16}  "
          + " -> ".join(path) + f" -> {path[0]}")
    for v in vias: print(f"                      via {v}")
if len(cycles) > 6: print(f"  ... and {len(cycles)-6} more round the same cluster")
print()
print(f"UNTAGGED AND UNRESOLVED: {len(unmatched)}")
for node, t in unmatched: print(f"  {node:<8} {t}")
print()
print(f"TAGGED WITH A PRODUCER: {len(tagged)}")
from collections import Counter
for k, n in sorted(Counter(k for _, ks, _ in tagged for k in ks).items()):
    print(f"  {n:>3}  {k}")
print()
print(f"GENUINE GAPS - TAGGED UNPRODUCED, NOTHING IN THE BUILD MAKES THEM TRUE: {len(gaps)}")
for node, t in gaps: print(f"  {node:<8} {t}")
print()
print("A GAP IS NOT A MISSING ARC. An arc this check cannot see is its own blindness;")
print("a gap is the build's. The two must never be reported as one number.")
sys.exit(1 if (clusters or unmatched or gaps) else 0)
