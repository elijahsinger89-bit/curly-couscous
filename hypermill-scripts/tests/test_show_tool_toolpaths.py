#!/usr/bin/env python3
"""Headless test of show_tool_toolpaths.py (fake om in tests/fake_om). Run: python3 tests/test_show_tool_toolpaths.py"""
import os
import sys
import tempfile
import importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(HERE, "fake_om"))
import om                      # noqa: E402  (fake)
import om.cad as cad           # noqa: E402  (fake)
import om.cad.gui as gui       # noqa: E402  (fake)

SCRIPT = os.path.join(ROOT, "copy_to_python_folder", "show_tool_toolpaths", "show_tool_toolpaths.py")
fails = []
tmp = tempfile.mkdtemp(prefix="stt_")
tempfile.tempdir = tmp
LOG = os.path.join(tmp, "show_tool_toolpaths_log.txt")


def check(cond, label):
    print(("ok   " if cond else "FAIL ") + label)
    if not cond:
        fails.append(label)


T = om.Tool
t1, t2 = T("905080900", "Ceramic"), T("903080900", "Turn")
_n = [0]


def uid(p):
    _n[0] += 1
    return "{%s-%04d}" % (p, _n[0])


class Plain(om.Job):
    """A toolpath with no display member (as in the real dump)."""
    def __init__(self, name, tool):
        om.Job.__init__(self, name, tool)
        self.UUID = uid("J")


class PJob(Plain):
    """Light bulb as a property."""
    def __init__(self, name, tool, on=True):
        Plain.__init__(self, name, tool)
        self.ToolpathVisible = on


class PComp(om.CompoundJob):
    """Compound job with a light bulb; cascade=True also switches its toolpaths (like a tree parent might)."""
    def __init__(self, name, jobs, on=True, cascade=False):
        om.CompoundJob.__init__(self, name, jobs)
        self._on, self._cascade = on, cascade

    @property
    def ToolpathVisible(self):
        return self._on

    @ToolpathVisible.setter
    def ToolpathVisible(self, v):
        self._on = bool(v)
        if self._cascade:
            for j in self._jobs:
                j.ToolpathVisible = bool(v)


class Bag:
    def __init__(self, d):
        self._d = d

    def __iter__(self):
        return iter(list(self._d))


class BJob(Plain):
    """Light bulb only in the property set (values come back as text)."""
    def __init__(self, name, tool):
        Plain.__init__(self, name, tool)
        self._p = {"Color": "3", "ToolPathVisibility": "true"}
        self.PropertySet = Bag(self._p)

    def GetProperty(self, n):
        return self._p[n]

    def SetProperty(self, n, v):
        if n not in self._p:
            raise KeyError(n)
        self._p[n] = "true" if v is True else "false" if v is False else v


class Node:
    def __init__(self, obj, kids=()):
        self.UUID, self.Name, self.IsVisible = obj.UUID, obj.Name, True
        self._k = list(kids)

    def GetChildren(self):
        return self._k


class LJobList(om.JobList):
    """Joblist with toolpaths outside compound jobs and (optional) job tree nodes."""
    def __init__(self, name, compounds, loose=(), nodes=None):
        om.JobList.__init__(self, name, compounds)
        self._loose, self._nodes = list(loose), nodes

    def GetJobs(self):
        return om.JobList.GetJobs(self) + self._loose

    def GetJobTreeNodes(self):
        if self._nodes is None:
            raise RuntimeError("not available")
        return self._nodes


def build(job_cls=PJob, comp_cls=PComp, nodes=False, on=True, cascade=False, two_lists=False):
    mk = (lambda n, t: job_cls(n, t, on)) if job_cls is PJob else job_cls
    j = [mk("1: Rough", t1), mk("2: Turn OD", t2), mk("3: Turn ID", t2), mk("4: Finish", t1), mk("5: Loose", t1)]
    if comp_cls is PComp:
        cs = [PComp("B_X_010_HF5", j[0:2], on, cascade), PComp("B_X_020_HF5", j[2:3], on, cascade),
              PComp("B_X_030_HF5", j[3:4], on, cascade)]
    else:
        cs = [om.CompoundJob("B_X_010_HF5", j[0:2]), om.CompoundJob("B_X_020_HF5", j[2:3]),
              om.CompoundJob("B_X_030_HF5", j[3:4])]
    nd = None
    if nodes:
        nd = [Node(cs[0], [Node(j[0]), Node(j[1])]), Node(cs[1], [Node(j[2])]), Node(cs[2], [Node(j[3])]), Node(j[4])]
    lists = [LJobList("Op1", cs, [j[4]], nd)]
    if two_lists:
        lists.append(LJobList("Op2", [om.CompoundJob("B_Y_010_HF5", [Plain("1: Other", t2)])]))
    om._App.CurrentDocument = om.Document(os.path.join(tmp, "doc.hmc"), om.Model(lists))
    return j, cs, nd


def run(answer):
    gui.SCRIPT[:] = [answer]
    gui.BOXES.clear(); gui.SHOWN.clear()
    spec = importlib.util.spec_from_file_location("stt_under_test", SCRIPT)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    m.run()
    with open(LOG, encoding="utf-8") as f:
        return m, f.read()


def ans(tool_index, show, joblist=None):
    def a(d):
        v = d.defaults()
        v["Tool"], v["Show"] = tool_index, show
        if joblist is not None:
            v["Joblist"] = joblist
        return True, v
    return a


T1 = 1      # tools sorted by ID: 0 = T903080900, 1 = T905080900

# ---- dialog
j, cs, _ = build()
m, lg = run(ans(T1, "This tool only"))
fields = gui.SHOWN[0][1]
check([f[1] for f in fields] == ["Joblist", "Tool", "Show"], "dialog: Joblist, Tool, Show")
tl = fields[1][2][0]
check(tl == ["T903080900  Turn  - 2 toolpaths", "T905080900  Ceramic  - 3 toolpaths"], "tool list sorted by ID with counts: %s" % tl)
check(fields[2][2] == (["This tool only", "Add this tool", "Everything on"], 0), "Show options, This tool only first")

# ---- 1. property: This tool only
check([x.ToolpathVisible for x in j] == [True, False, False, True, True], "prop / only: T905080900 on, the others off")
check([c.ToolpathVisible for c in cs] == [True, False, True], "prop / only: compound jobs with the tool on, the other off")
check("light bulb: ('prop', 'ToolpathVisible')" in lg, "log names the member used")
check(gui.BOXES and gui.BOXES[0].startswith("T905080900  Ceramic: 3 toolpaths on, 2 off."), "message: %s" % gui.BOXES[:1])

# ---- 1. property: Add this tool (others as they were, also when a compound job switch cascades)
j, cs, _ = build(on=False, cascade=True)
j[1].ToolpathVisible = False
j[2].ToolpathVisible = True
run(ans(T1, "Add this tool"))
check([x.ToolpathVisible for x in j] == [True, False, True, True, True], "prop / add: tool on, others as they were (cascade put back)")
check(gui.BOXES[0].startswith("T905080900  Ceramic: 3 toolpaths on."), "message add: %s" % gui.BOXES[:1])

# ---- 1. property: Everything on
j, cs, _ = build(on=False)
run(ans(0, "Everything on"))
check(all(x.ToolpathVisible for x in j) and all(c.ToolpathVisible for c in cs), "prop / everything: all on")
check(gui.BOXES[0].startswith("Every toolpath: 5 toolpaths on."), "message everything: %s" % gui.BOXES[:1])

# ---- 2. property set
j, cs, _ = build(job_cls=BJob, comp_cls=None)
m, lg = run(ans(0, "This tool only"))
check([x._p["ToolPathVisibility"] for x in j] == ["false", "true", "true", "false", "false"], "bag / only: T903080900 on")
check(all(x._p["Color"] == "3" for x in j), "bag: other properties untouched")
check("light bulb: ('bag', 'ToolPathVisibility')" in lg, "log: bag route")

# ---- 3. job tree nodes
j, cs, nd = build(job_cls=Plain, comp_cls=None, nodes=True)
m, lg = run(ans(T1, "This tool only"))
flat = [nd[0]._k[0], nd[0]._k[1], nd[1]._k[0], nd[2]._k[0], nd[3]]
check([x.IsVisible for x in flat] == [True, False, False, True, True], "node / only: T905080900 nodes on")
check([nd[0].IsVisible, nd[1].IsVisible, nd[2].IsVisible] == [True, False, True], "node / only: compound job nodes")
check("('node', ('prop', 'IsVisible'))" in lg, "log: node route")
check("job tree nodes: 8, matched to a job: 8" in lg, "log: tree nodes counted")

# ---- 4. om.cad Unhide / Hide
shown = set()
cad.UnhideEntity = lambda e: shown.add(e.UUID)
cad.HideEntity = lambda e: shown.discard(e.UUID)
j, cs, _ = build(job_cls=Plain, comp_cls=None)
m, lg = run(ans(T1, "This tool only"))
check(shown == {j[0].UUID, j[3].UUID, j[4].UUID, cs[0].UUID, cs[2].UUID}, "cad / only: tool's toolpaths and their compound jobs unhidden")
check("light bulb: ('cad', False)" in lg, "log: cad route")
check("If the light bulbs did not change" in gui.BOXES[0], "cad: message asks for the log if nothing changed")
del cad.UnhideEntity, cad.HideEntity

# ---- nothing found
j, cs, _ = build(job_cls=Plain, comp_cls=None)
m, lg = run(ans(T1, "This tool only"))
check("was not found, so nothing was changed" in gui.BOXES[0], "not found: message")
check("light bulb: NOT FOUND" in lg and "toolpath  Plain (" in lg and "compound job  CompoundJob (" in lg,
      "not found: log lists toolpath and compound job members")
check("GetJobTreeNodes()" in lg and "-> error not available" in lg, "not found: tree node try logged")

# ---- tool not in the chosen joblist, cancel
build(two_lists=True)
run(ans(T1, "This tool only", joblist="Op2"))
check(gui.BOXES and "has no toolpaths in Op2" in gui.BOXES[0], "tool not in joblist: message")
build()
gui.SCRIPT[:] = [lambda d: (False, {})]
gui.BOXES.clear()
spec = importlib.util.spec_from_file_location("stt_cancel", SCRIPT)
mm = importlib.util.module_from_spec(spec); spec.loader.exec_module(mm); mm.run()
check(not gui.BOXES, "cancel: no message")

print("\n%d failed" % len(fails) if fails else "\nall passed")
sys.exit(1 if fails else 0)
