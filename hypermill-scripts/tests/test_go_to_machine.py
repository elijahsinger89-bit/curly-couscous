#!/usr/bin/env python3
"""Headless test of go_to_machine.py and tool_library/release_check.py (fake om in tests/fake_om).
Documents mirror release_probe v5: POF header "0: ucid(<id>)", POF\\<id>.ccrpt "CC_RESULT 1" / "CC_RESULT 0".
Run: python3 tests/test_go_to_machine.py"""
import os
import sys
import enum
import json
import shutil
import tempfile
import importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(HERE, "fake_om"))
import om                      # noqa: E402  (fake)
import om.cad.gui as gui       # noqa: E402  (fake)
import csv                     # noqa: E402

SCRIPT = os.path.join(ROOT, "copy_to_python_folder", "go_to_machine", "go_to_machine.py")
LIB = os.path.join(ROOT, "copy_to_python_folder", "tool_library")
TOL = os.path.join(HERE, "fake_tool_order_list", "tool_order_list.py")
TOL_FILES = [TOL]
TLM = os.path.join(ROOT, "copy_to_python_folder", "tool_load_mda", "tool_load_mda.py")
TLM_FILES = [TLM]
fails = []


def check(cond, label):
    print(("ok   " if cond else "FAIL ") + label)
    if not cond:
        fails.append(label)


def flat(t):
    return " ".join(str(t).split())


class PS(enum.Enum):
    UP_TO_DATE = 0
    NEEDS_CALCULATION = 3


class JS(enum.Enum):
    UP_TO_DATE = 1
    ERRORS = 2
    WARNINGS = 3


class PJob(om.Job):
    def __init__(self, name, tool, pof, status=JS.UP_TO_DATE, pofs=PS.UP_TO_DATE):
        om.Job.__init__(self, name, tool, {"*AUFMASS": "0"})
        self.PofFileName, self.Status, self.POFStatus = pof, status, pofs


class PostSet(om.JobListSet):
    """CalculateNC writes NC\\<compound job name>.mpf for each compound job UUID (or nothing / raises)."""
    calls = []
    mode = "write"

    def CalculateNC(self, uuids):
        PostSet.calls.append(list(uuids))
        if PostSet.mode == "raise":
            raise RuntimeError("post processor not found")
        if PostSet.mode == "write":
            os.makedirs(os.path.join(DOCDIR, "NC"), exist_ok=True)
            for jl in self.GetJobLists():
                for c in jl.GetCompoundJobs():
                    if c.UUID in uuids:
                        with open(os.path.join(DOCDIR, "NC", c.Name + ".mpf"), "w") as f:
                            f.write("; " + c.Name)
        return True


tmp = tempfile.mkdtemp(prefix="gtm_")
tempfile.tempdir = tmp
DOCDIR = os.path.join(tmp, "job")
POFDIR = os.path.join(DOCDIR, "POF")
os.makedirs(POFDIR)
DOC = os.path.join(DOCDIR, "G17_SLIDE_OP10.hmc")
open(DOC, "w").close()
with open(os.path.join(tmp, "b_program_rename_last.json"), "w") as f:
    json.dump({"part": "G17_SLIDE", "machine": "HF5"}, f)

UC = {"a": "010cbcb0-e345-4f88-b7ff-2aa5765902c7", "b": "ba0ff6bd-42b7-430d-bda4-1e4f0aab9059",
      "c": "3989928e-cd22-400c-a14d-dcfb554232ba", "d": "a581eab5-2482-482b-9257-dbcc5cb984d5",
      "e": "bfbab6ae-0137-454a-a2fe-4d14274f09f7", "f": "f36764a2-81b9-4b51-ad7f-522e0e1ce34d"}


def pof(n, ucid, upper=False):
    p = os.path.join(POFDIR, "Op10_%d.pof" % n)
    u = ucid.upper() if upper else ucid
    with open(p, "wb") as f:
        f.write(b"POF\r\n0: technology(milling)\r\n0: platform(x64)\r\n0: ucid(" + u.encode() + b")\r\n0: jobname(x)\r\n" + b"G1 X0\r\n" * 50)
    return p


def ccrpt(ucid, res):
    with open(os.path.join(POFDIR, ucid + ".ccrpt"), "w", newline="") as f:
        f.write("CC_RESULT %d\r\n" % res)


def build(all_pass=False, dup=False):
    for n in os.listdir(POFDIR):
        os.remove(os.path.join(POFDIR, n))
    shutil.rmtree(os.path.join(DOCDIR, "NC"), ignore_errors=True)
    for n in os.listdir(DOCDIR):
        if n.endswith((".json", ".csv", ".MPF")):  # B lists, tool sheets, tool load programs
            os.remove(os.path.join(DOCDIR, n))
    T = om.Tool
    em, dr, fm = T("10047210", "End mill", "endMill", 0.4724), T("11039410", "Drill", "drilTool", 0.25), T("905083900", "Face", "faceMill", 2.0)
    j1 = PJob("1: Contour", em, pof(1, UC["a"]))
    j2 = PJob("2: Contour finish", em, pof(2, UC["b"], upper=True))            # ucid upper case in the header
    ccrpt(UC["a"], 1)
    ccrpt(UC["b"], 1)
    j3 = PJob("3: Drill", dr, pof(3, UC["c"]))
    ccrpt(UC["c"], 1 if all_pass else 0)                                         # collision run
    j4 = PJob("4: Face", fm, pof(4, UC["d"]))                                    # never simulated
    if all_pass:
        ccrpt(UC["d"], 1)
    j5 = PJob("5: Face finish", fm, pof(5, UC["e"]), pofs=PS.UP_TO_DATE if all_pass else PS.NEEDS_CALCULATION)
    j6 = PJob("6: Face errors", fm, pof(6, UC["f"]), status=JS.UP_TO_DATE if all_pass else JS.ERRORS)
    ccrpt(UC["e"], 1)
    ccrpt(UC["f"], 1)
    cs = [om.CompoundJob("------ notes ------"),
          om.CompoundJob("B_G17_SLIDE_010_HF5", [j1, j2]),
          om.CompoundJob("B_G17_SLIDE_%s_HF5" % ("010" if dup else "020"), [j3]),
          om.CompoundJob("B_G17_SLIDE_030_HF5", [j4]),
          om.CompoundJob("B_G17_SLIDE_040_HF5", [j5, j6]),
          om.CompoundJob("B_G17_SLIDE_111_HF5", [PJob("m1", em, pof(7, UC["a"])), PJob("m2", dr, pof(8, UC["a"]))]),
          om.CompoundJob("G17 old name", [PJob("o1", fm, pof(9, UC["a"]))])]
    model = om.Model([om.JobList("Op10", cs)], inch=True)
    model.JobListSet = PostSet(model.JobListSet.GetJobLists())
    om._App.CurrentDocument = om.Document(DOC, model)
    PostSet.calls = []
    return cs


def ans(**kv):
    def f(dlg):
        d = dlg.defaults()
        d.update({k.replace("_", " "): v for k, v in kv.items()})
        return True, d
    return f


def post_pick(i):
    return lambda dlg: (True, {"Post": i})


def include_pick(i):
    return lambda dlg: (True, {"Include": i})


def run(answers):
    gui.SCRIPT[:] = answers
    gui.BOXES.clear()
    gui.SHOWN.clear()
    spec = importlib.util.spec_from_file_location("gtm_under_test", SCRIPT)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    m.TOL_FILES = tuple(TOL_FILES)
    m.TLM_FILES = tuple(TLM_FILES)
    m.run()
    left = len(gui.SCRIPT)
    gui.SCRIPT.clear()
    return m, left


def nc_files():
    d = os.path.join(DOCDIR, "NC")
    return sorted(os.listdir(d)) if os.path.isdir(d) else []


LOGP = os.path.join(tmp, "go_to_machine_log.txt")
BLIST = os.path.join(DOCDIR, "G17_SLIDE_OP10_B_PROGRAMS.json")
SHEET = os.path.join(DOCDIR, "G17_SLIDE_OP10_Op10_tool_order.csv")
MPF = os.path.join(DOCDIR, "G17_SLIDE_OP10_TOOL_LOAD.MPF")


def counts(**by_id):
    """Answer the tool load MDA screen: by_id = {tool id: (sisters, life)} as text."""
    def f(dlg):
        d = dlg.defaults()
        for label in list(d):
            for tid, (sv, lv) in by_id.items():
                if label.startswith(tid + " "):
                    d[label] = sv if label.endswith("sisters") else lv
        return True, d
    return f


def sheet():
    with open(SHEET, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

# ---------------- release_check on its own ----------------
spec = importlib.util.spec_from_file_location("rc_under_test", os.path.join(LIB, "release_check.py"))
rc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rc)
cs = build()
cache = rc.Ccrpt()
r = [rc.check_compound(c, DOCDIR, cache) for c in cs[1:5]]
check([x["ok"] for x in r] == [True, False, False, False], "release_check: 010 passes; 020, 030, 040 fail")
check(r[0]["jobs"][1]["ucid"] == UC["b"], "upper-case ucid in the POF header read (lower-cased)")
check(r[1]["failed"][0]["reason"] == rc.R_COLLISION, "CC_RESULT 0: collision reason")
check(r[2]["failed"][0]["reason"] == rc.R_NOT_SIM, "no .ccrpt: not simulated or changed since")
check([j["reason"] for j in r[3]["failed"]] == ["not calculated (NEEDS_CALCULATION)", rc.R_ERRORS], "not calculated and errors reasons")
os.remove(os.path.join(POFDIR, "Op10_1.pof"))
check(rc.check_job(cs[1].GetJobs()[0], DOCDIR, rc.Ccrpt())["reason"] == rc.R_NO_POF, "POF file missing: reason")
with open(os.path.join(POFDIR, "Op10_2.pof"), "wb") as f:
    f.write(b"POF without an id")
check(rc.check_job(cs[1].GetJobs()[1], DOCDIR, rc.Ccrpt())["reason"] == rc.R_NO_ID, "POF without a toolpath id: reason")
with open(os.path.join(POFDIR, UC["e"] + ".ccrpt"), "w") as f:
    f.write("CC_RESULT 7\r\n")
j5ok = PJob("x", None, os.path.join(POFDIR, "Op10_5.pof"))
check("unknown Simulation Center result 'CC_RESULT 7'" in rc.check_job(j5ok, DOCDIR, rc.Ccrpt())["reason"], "unknown result text shown")

# ---------------- check only ----------------
build()
m, left = run([ans(Action="Check only")])
box = flat(gui.BOXES[-1])
rep = "\n".join(gui.OUTPUT)
check(left == 0 and PostSet.calls == [] and nc_files() == [] and not os.path.exists(BLIST), "check only: nothing posted, nothing written")
check("4 B programs: 1 pass, 3 fail." in box and "Check only: nothing posted" in box, "check only: counts in the message")
check("OK   B_G17_SLIDE_010_HF5" in rep and "FAIL B_G17_SLIDE_020_HF5" in rep, "report: OK / FAIL per B program")
check("3: Drill: " + rc.R_COLLISION in rep and "4: Face: " + rc.R_NOT_SIM in rep, "report: reason per failing job")
check("5: Face finish: not calculated (NEEDS_CALCULATION)" in rep and "6: Face errors: has errors" in rep, "report: not calculated, errors")
check("B_G17_SLIDE_111_HF5  (more than one tool)" in rep and "G17 old name  (not a B program name" in rep and "notes" not in rep,
      "report: mixed and old-name compound jobs listed as not posted; notes skipped")
check(os.path.exists(LOGP) and "FAIL B_G17_SLIDE_030_HF5" in open(LOGP).read(), "log written")

# ---------------- check and post, failures: post nothing ----------------
build()
m, left = run([ans(Action="Check and post", Tool_load_MDA=False), post_pick(0)])
check(left == 0 and PostSet.calls == [] and "Nothing posted." in gui.BOXES[-1], "warning answered No: nothing posted")
check(any("WARNING: 3 of 4 B programs fail the check." in b for b in gui.BOXES), "warning box before the choice")
opts = gui.SHOWN[-1][1][0][2][0]
check(opts == ["No - post nothing", "Post all 4 (3 fail the check)", "Post only the 1 that pass"], "warning choices: %s" % opts)
check(gui.SHOWN[-1][0].endswith("WARNING: 3 fail the check"), "warning dialog title")

# ---------------- post only the ones that pass, list: only the posted ----------------
cs = build()
m, left = run([ans(Action="Check and post", Tool_load_MDA=False), post_pick(2), include_pick(0)])
box = flat(gui.BOXES[-1])
check(left == 0 and PostSet.calls == [[cs[1].UUID]], "post only passing: CalculateNC with the one passing compound job UUID")
check(nc_files() == ["B_G17_SLIDE_010_HF5.mpf"] and "NC files written or updated: 1" in box and "NC/B_G17_SLIDE_010_HF5.mpf" in box.replace("\\", "/"),
      "post: written NC file found and listed")
check("No NC file found" not in box and "Posted 1 B program (CalculateNC returned True)." in box, "post: message")
inc = gui.SHOWN[-1]
check(inc[0].endswith("B program list and tool sheet") and inc[1][0][2][0] == ["Only the 1 posted", "All 4 B programs"],
      "only some posted: asks what the list and tool sheet hold (only posted first)")
data = json.load(open(BLIST))
check([s["step"] for s in data["steps"]] == [10] and "B program list for the generator (Import B list): 1 B program" in box,
      "list: only the posted B program")
nposted = [r["name"] for r in data["refused"] if r["reason"].startswith("not posted")]
check(nposted == ["B_G17_SLIDE_020_HF5", "B_G17_SLIDE_030_HF5", "B_G17_SLIDE_040_HF5"], "list: the 3 not posted listed as refused 'not posted'")
rows = sheet()
check(len(rows) == 1 and rows[0]["Designation"] == "End mill" and rows[0]["Manufacturer"] == "Walter" and
      rows[0]["Toolpath names"] == "B_G17_SLIDE_010_HF5: 1: Contour ; B_G17_SLIDE_010_HF5: 2: Contour finish" and rows[0]["Toolpaths using it"] == "2",
      "tool sheet: the posted B program's one tool, its toolpaths named by B program")
check("Tool sheet: 1 tool" in box and "G17_SLIDE_OP10_Op10_tool_order.csv" in box, "message: tool sheet path")

# ---------------- post only the ones that pass, list: all ----------------
cs = build()
m, left = run([ans(Action="Check and post", Tool_load_MDA=False), post_pick(2), include_pick(1)])
data = json.load(open(BLIST))
check(left == 0 and PostSet.calls == [[cs[1].UUID]] and [s["step"] for s in data["steps"]] == [10, 20, 30, 40],
      "list: all B programs when chosen (only 010 posted)")
check(not any(r["reason"].startswith("not posted") for r in data["refused"]), "list: nothing marked not posted")
rows = sheet()
check(sorted(r["Designation"] for r in rows) == ["Drill", "End mill", "Face"] and "not in tool_library: " in flat(gui.BOXES[-1]),
      "tool sheet: every tool of the 4 B programs; tools not in tool_library named")

# ---------------- post all ----------------
cs = build()
m, left = run([ans(Action="Check and post", Tool_load_MDA=False), post_pick(1)])
check(PostSet.calls == [[c.UUID for c in cs[1:5]]] and len(nc_files()) == 4, "post all: 4 UUIDs, 4 NC files")
check("Posted although 3 fail the check." in flat(gui.BOXES[-1]), "post all: message says posted with failures")
check("POSTED WITH FAILURES" in open(LOGP).read(), "post all: log records the override")
check(len(gui.SHOWN) == 2 and len(sheet()) == 3, "post all: no list question; tool sheet with all 3 tools")

# ---------------- everything passes: confirm ----------------
cs = build(all_pass=True)
m, left = run([ans(Action="Check and post", Tool_load_MDA=False), post_pick(1)])
check(gui.SHOWN[-1][0].endswith("confirm") and gui.SHOWN[-1][1][0][2][0] == ["No - do not post", "Yes - post 4 B programs"],
      "all pass: plain confirm, No first")
check(PostSet.calls == [[c.UUID for c in cs[1:5]]] and not any(b.startswith("WARNING") for b in gui.BOXES), "all pass: posted, no warning")
build(all_pass=True)
m, left = run([ans(Action="Check and post", Tool_load_MDA=False), post_pick(0)])
check(PostSet.calls == [] and "Nothing posted." in gui.BOXES[-1], "all pass, confirm No: nothing posted")

# ---------------- duplicate step: stop ----------------
build(dup=True)
m, left = run([ans(Action="Check and post", Tool_load_MDA=False)])
check(left == 0 and PostSet.calls == [] and "Nothing posted. Fix these first" in flat(gui.BOXES[-1]) and "used twice" in gui.BOXES[-1],
      "step used twice: stops before posting")

# ---------------- CalculateNC fails / writes nothing ----------------
build(all_pass=True)
PostSet.mode = "raise"
m, left = run([ans(Action="Check and post", Tool_load_MDA=False), post_pick(1)])
check("Posting failed: RuntimeError: post processor not found" in flat(gui.BOXES[-1]), "CalculateNC error reported")
build(all_pass=True)
PostSet.mode = "nothing"
m, left = run([ans(Action="Check and post", Tool_load_MDA=False), post_pick(1)])
check("No NC file found for:" in gui.BOXES[-1] and "B_G17_SLIDE_040_HF5" in gui.BOXES[-1], "CalculateNC wrote nothing: B programs without an NC file listed")
PostSet.mode = "write"

# ---------------- tool load MDA ----------------
for f in ("tool_load_mda_last.json",):
    if os.path.exists(os.path.join(tmp, f)):
        os.remove(os.path.join(tmp, f))
cs = build(all_pass=True)
m, left = run([ans(Action="Check and post"), post_pick(1), counts(**{"10047210": ("2", "50"), "905083900": ("0", "")})])
box = flat(gui.BOXES[-1])
labels = [f[1] for f in gui.SHOWN[-1][1]]
check(left == 0 and gui.SHOWN[0][1][-1][:2] == ("bool", "Tool load MDA") and gui.SHOWN[0][1][-1][2] is True,
      "first screen: Tool load MDA, ticked by default")
check(gui.SHOWN[-1][0].startswith("Tool load MDA | tools 1-3 of 3") and "10047210  D0.4724  tool life (SETPIECE)" in labels,
      "MDA screen after posting: the 3 tools of the B programs, SETPIECE tools marked")
txt = open(MPF).read()
check(txt.count('NEWT("10047210",') == 2 and 'NEWT("11039410",1)' in txt and "905083900" not in txt,
      "MDA: 2 sisters of the end mill, 1 drill, face mill left out (0 sisters)")
check(txt.count("$TC_MOP13[R999,1]=50") == 2 and "go_to_machine Op10" in txt, "MDA: tool life 50 on the end mill; source in the header")
check("Tool load MDA: 3 tool entries (2 tools)" in box and "G17_SLIDE_OP10_TOOL_LOAD.MPF" in box, "message: MDA path and counts")
check("left out (0 sisters): 905083900" in box and "WARNING - SETPIECE counts these tools but no tool life was entered" in box
      and "11039410" in box.split("WARNING - SETPIECE")[1], "message: left out and SETPIECE-without-tool-life warning")
check(json.load(open(os.path.join(tmp, "tool_load_mda_last.json"))).get("10047210") == [2, 50], "MDA values remembered")

build(all_pass=True)
m, left = run([ans(Action="Check and post"), post_pick(1), lambda dlg: (True, dlg.defaults())])
fields = {f[1]: f[2] for f in gui.SHOWN[-1][1]}
check(fields.get("10047210  D0.4724  sisters") == "2" and fields.get("10047210  D0.4724  tool life (SETPIECE)") == "50",
      "second run: remembered sisters and tool life offered")

build(all_pass=True)
m, left = run([ans(Action="Check and post"), post_pick(1), lambda dlg: (False, {})])
check(left == 0 and "Tool load MDA cancelled: not written." in flat(gui.BOXES[-1]) and not os.path.exists(MPF) and os.path.exists(BLIST),
      "MDA screen cancelled: posted, list and sheet written, no MDA")

build(all_pass=True)
m, left = run([ans(Action="Check and post", Tool_load_MDA=False), post_pick(1)])
check(left == 0 and not os.path.exists(MPF) and "Tool load MDA" not in gui.BOXES[-1], "MDA unticked: no screen, no program")

build(all_pass=True)
TLM_FILES[:] = [os.path.join(tmp, "nowhere", "tool_load_mda.py")]
m, left = run([ans(Action="Check and post"), post_pick(1)])
check(left == 0 and "Tool load MDA not written: tool_load_mda.py not found" in flat(gui.BOXES[-1]), "tool_load_mda missing: says so")
TLM_FILES[:] = [TLM]

build()
m, left = run([ans(Action="Check only")])
check(left == 0 and not os.path.exists(MPF), "check only: no MDA screen")

# ---------------- tool_order_list not installed ----------------
build(all_pass=True)
TOL_FILES[:] = [os.path.join(tmp, "nowhere", "tool_order_list.py")]
m, left = run([ans(Action="Check and post", Tool_load_MDA=False), post_pick(1)])
check("Tool sheet not written: tool_order_list.py not found" in flat(gui.BOXES[-1]) and not os.path.exists(SHEET) and os.path.exists(BLIST),
      "tool_order_list missing: B list still written, tool sheet skipped with the reason")
TOL_FILES[:] = [TOL]

# ---------------- input errors and no B programs ----------------
build()
m, left = run([ans(Part_number="G17-SLIDE")])
check("Fix these first" in gui.BOXES[-1] and PostSet.calls == [], "part number with - refused")
build()
m, left = run([ans(Machine="F5000")])
check("Run b_program_rename first" in gui.BOXES[-1], "no B programs for that machine: says so")

shutil.rmtree(tmp, ignore_errors=True)
print()
print("FAILURES: %d" % len(fails) if fails else "ALL GO TO MACHINE CHECKS PASSED")
sys.exit(1 if fails else 0)
