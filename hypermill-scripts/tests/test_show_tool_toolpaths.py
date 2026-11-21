#!/usr/bin/env python3
"""Headless test of show_tool_toolpaths.py (fake om in tests/fake_om).
v3 default (SWITCH = False): the bulb finder reads only and lists what changed between two runs.
v2 switching (SWITCH = True, kept for when the bulb is found): one toolpath switched first and checked.
Run: python3 tests/test_show_tool_toolpaths.py"""
import os
import sys
import enum
import uuid
import tempfile
import importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(HERE, "fake_om"))
import om                      # noqa: E402  (fake)
import om.cad.gui as gui       # noqa: E402  (fake)

SCRIPT = os.path.join(ROOT, "copy_to_python_folder", "show_tool_toolpaths", "show_tool_toolpaths.py")
tmp = tempfile.mkdtemp(prefix="stt_")
tempfile.tempdir = tmp
LOG = os.path.join(tmp, "show_tool_toolpaths_log.txt")
DOCDIR = os.path.join(tmp, "job")
POFDIR = os.path.join(DOCDIR, "POF")
os.makedirs(POFDIR)
fails = []


def check(cond, label):
    print(("ok   " if cond else "FAIL ") + label)
    if not cond:
        fails.append(label)


class PS(enum.Enum):
    UP_TO_DATE = 0
    NEEDS_CALCULATION = 3


class JS(enum.Enum):
    UP_TO_DATE = 1


BEHAVIOUR = {"mode": "display"}     # display: only the bulb changes | change: counted as a change | ccrpt: deletes the result | ignore


class CJob(om.Job):
    """Toolpath with *SHOW_NCPATH, a POF file with a toolpath id and a Simulation Center result."""
    def __init__(self, name, tool, on=False, simulated=True):
        om.Job.__init__(self, name, tool, {"*SHOW_NCPATH": "1" if on else "0", "*AUFMASS": "0"})
        self.UUID = str(uuid.uuid4())
        self.ucid = str(uuid.uuid4())
        self.PofFileName = os.path.join(POFDIR, self.UUID + ".pof")
        with open(self.PofFileName, "wb") as f:
            f.write(b"POF\r\n0: ucid(" + self.ucid.encode() + b")\r\n" + b"G1 X0\r\n" * 20)
        if simulated:
            with open(os.path.join(POFDIR, self.ucid + ".ccrpt"), "w") as f:
                f.write("CC_RESULT 1\r\n")
        self.Status, self.POFStatus = JS.UP_TO_DATE, PS.UP_TO_DATE
        self.sets = 0

    def SetCfgParameters(self, d):
        self.sets += 1
        b = BEHAVIOUR["mode"]
        if b == "ignore":
            return
        self._cfg.update(d)
        if b == "change":
            self.POFStatus = PS.NEEDS_CALCULATION
        if b == "ccrpt":
            p = os.path.join(POFDIR, self.ucid + ".ccrpt")
            if os.path.exists(p):
                os.remove(p)


class PJob(om.Job):
    """Toolpath with only the ShowNCPaths property (no *SHOW_NCPATH setting)."""
    def __init__(self, name, tool, on=False):
        om.Job.__init__(self, name, tool, {"*AUFMASS": "0"})
        self.UUID = str(uuid.uuid4())
        self.PofFileName = ""
        self.Status, self.POFStatus = JS.UP_TO_DATE, PS.UP_TO_DATE
        self._p = {"ShowNCPaths": "1" if on else "0"}

    def GetProperty(self, n):
        return self._p.get(n, "")

    def SetProperty(self, n, v):
        self._p[n] = v


class CComp(om.CompoundJob):
    def __init__(self, name, jobs, with_key=True):
        om.CompoundJob.__init__(self, name, jobs)
        self.cfg = {"*CPJOBNAME": name}
        if with_key:
            self.cfg["*SHOW_NCPATH"] = "0"

    def GetCfgParameters(self):
        return dict(self.cfg)

    def SetCfgParameters(self, d):
        self.cfg.update(d)


T = om.Tool
t1, t2 = T("905080900", "Ceramic"), T("903080900", "Turn")


def build(job_cls=CJob, hand_on=1, comp_key=True, simulated=True):
    for n in os.listdir(POFDIR):
        os.remove(os.path.join(POFDIR, n))
    mk = (lambda n, t, on: CJob(n, t, on, simulated)) if job_cls is CJob else job_cls
    j = [mk("1: Rough", t1, False), mk("2: Turn OD", t2, hand_on == 1), mk("3: Turn ID", t2, False),
         mk("4: Finish", t1, False), mk("5: Loose", t1, False)]
    cs = [CComp("B_X_010_HF5", j[0:2], comp_key), CComp("B_X_020_HF5", j[2:3], comp_key), CComp("B_X_030_HF5", j[3:4], comp_key)]
    jl = om.JobList("Op1", cs)
    jl.GetJobs = lambda: [x for c in cs for x in c.GetJobs()] + [j[4]]
    om._App.CurrentDocument = om.Document(os.path.join(DOCDIR, "doc.hmc"), om.Model([jl]))
    return j, cs


def run(tool_index, show, switch=True):
    gui.SCRIPT[:] = [lambda d: (True, dict(d.defaults(), Tool=tool_index, Show=show))] if switch else []
    gui.BOXES.clear(); gui.SHOWN.clear(); gui.OUTPUT.clear()
    spec = importlib.util.spec_from_file_location("stt_under_test", SCRIPT)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    m.SWITCH = switch
    m.run()
    with open(LOG, encoding="utf-8") as f:
        return f.read()


on = lambda x: x._cfg.get("*SHOW_NCPATH")
T1 = 1          # tools sorted by ID: 0 = T903080900, 1 = T905080900

# ---- v3 default: bulb finder, reads only ----
SNAP = os.path.join(tmp, "show_tool_toolpaths_snapshot.json")
j, cs = build()
for x in j:
    x.ShowInTree = False                     # stands in for the unknown light bulb field
lg = run(0, "", switch=False)
check(not gui.SHOWN and os.path.exists(SNAP) and gui.BOXES[0].startswith("Bulb finder (changes nothing): 5 toolpaths read and saved"),
      "first run: no screens, snapshot saved, asks to switch ONE bulb and run again")
check(sum(x.sets for x in j) == 0 and [on(x) for x in j] == ["0", "1", "0", "0", "0"], "finder writes nothing")
check("v3" in lg and "bulb finder (reads only)" in lg, "log says v3, reads only")
j[3].ShowInTree = True                       # the user turns one bulb on
lg = run(0, "", switch=False)
check(gui.BOXES[0].startswith("Changed since the run at") and "toolpath 4: Finish | m.ShowInTree: False -> True" in gui.BOXES[0]
      and ": 1 value." in gui.BOXES[0], "second run: exactly the one field that changed, on that toolpath")
check("toolpath 4: Finish | m.ShowInTree: False -> True" in lg and "changed since" in "\n".join(gui.OUTPUT), "change in the log and the output window")
lg = run(0, "", switch=False)
check(gui.BOXES[0].startswith("Nothing changed since the run at"), "third run, nothing switched: says nothing changed")
check(sum(x.sets for x in j) == 0, "three finder runs: still nothing written")
os.remove(SNAP)

# ---- v2 switching (SWITCH = True) ----

# ---- the hand-turned bulb confirms *SHOW_NCPATH; this tool only
j, cs = build()
lg = run(T1, "This tool only")
outp = "\n".join(gui.OUTPUT)
check("*SHOW_NCPATH: 2: Turn OD" in outp and "ShowNCPaths: none" in outp, "before anything changes: the bulb turned on by hand is listed (2: Turn OD)")
check("light bulb: cfg | *SHOW_NCPATH reads on for: 2: Turn OD" in lg, "route chosen from the setting that reads on")
check([on(x) for x in j] == ["1", "0", "0", "1", "1"], "this tool only: T905080900 on, the others (incl. the hand one) off")
check([c.cfg["*SHOW_NCPATH"] for c in cs] == ["1", "0", "1"], "compound jobs with the tool on, the other off")
check("safety test on '1: Rough'" in lg and "safety test passed" in lg, "first toolpath switched alone and checked")
check(gui.BOXES[0].startswith("T905080900  Ceramic: 3 toolpaths on, 2 off.") and "Light bulb: *SHOW_NCPATH reads on for: 2: Turn OD" in gui.BOXES[0],
      "message: counts and which setting is the bulb")

# ---- add this tool: the others stay
j, cs = build()
run(T1, "Add this tool")
check([on(x) for x in j] == ["1", "1", "0", "1", "1"], "add this tool: the hand-on toolpath stays on")

# ---- everything on; no bulb on before: ROUTE used and said so
j, cs = build(hand_on=0)
lg = run(0, "Everything on")
check(all(on(x) == "1" for x in j) and "no toolpath reads on before the change: used *SHOW_NCPATH (ROUTE)" in gui.BOXES[0],
      "nothing on before: ROUTE (*SHOW_NCPATH) used and the message says so")

# ---- safety: hyperMILL counts the switch as a change -> stop after one, switched back, nothing else touched
BEHAVIOUR["mode"] = "change"
j, cs = build()
run(T1, "This tool only")
check("Stopped after one toolpath" in gui.BOXES[0] and "calculation status UP_TO_DATE -> NEEDS_CALCULATION" in gui.BOXES[0],
      "counted as a change: stops after one, says what changed")
check([on(x) for x in j] == ["0", "1", "0", "0", "0"] and sum(x.sets for x in j) == 2 and [c.cfg["*SHOW_NCPATH"] for c in cs] == ["0", "0", "0"],
      "the test toolpath switched back; no other toolpath or compound job touched")

# ---- safety: the switch deletes the Simulation Center result
BEHAVIOUR["mode"] = "ccrpt"
j, cs = build()
run(T1, "This tool only")
check("Simulation Center result (.ccrpt) deleted" in gui.BOXES[0] and "Re-simulate that B program" in gui.BOXES[0],
      "result deleted: stops and says to re-simulate")
check(sum(1 for x in j if not os.path.exists(os.path.join(POFDIR, x.ucid + ".ccrpt"))) == 1,
      "the test used a toolpath WITH a result, so only that one result is lost")
j, cs = build(simulated=False)
run(T1, "This tool only")
check("Stopped" not in gui.BOXES[0] and [on(x) for x in j] == ["1", "0", "0", "1", "1"],
      "nothing simulated: no result to lose, every toolpath switched")

# ---- the setting does not change: not the bulb
BEHAVIOUR["mode"] = "ignore"
j, cs = build()
run(T1, "This tool only")
check("did not change" in gui.BOXES[0] and "not the light bulb" in gui.BOXES[0], "setting ignored by hyperMILL: stops, not the bulb")
BEHAVIOUR["mode"] = "display"

# ---- property route (no *SHOW_NCPATH, ShowNCPaths reads on)
j, cs = build(job_cls=PJob, comp_key=False)
lg = run(T1, "This tool only")
check("light bulb: prop | ShowNCPaths reads on for: 2: Turn OD" in lg and [x._p["ShowNCPaths"] for x in j] == ["1", "0", "0", "1", "1"],
      "ShowNCPaths route when only it reads on")

# ---- nothing to switch
j, cs = build(hand_on=0)
run(T1, "Add this tool")
run(T1, "Add this tool")
check(gui.BOXES[0].startswith("Nothing to switch"), "second run: nothing to switch")

print("\n%d failed" % len(fails) if fails else "\nall passed")
sys.exit(1 if fails else 0)
