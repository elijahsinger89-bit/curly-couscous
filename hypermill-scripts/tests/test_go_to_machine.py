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


# posted NC text per B program (G41/G42 and R parameter scan for the generator's CMC checks)
NC_TEXT = {
    "B_G17_SLIDE_010_HF5": "N10 CYCLE800(1,\"H\",200000,54,0,0,0,0,-90,0,0,0,0,1,0,101) ; A=DC(-90)\nG1 G41 D1 X10\n"
                           "R1=5 R12=R1+1 ; R700 in a comment\nMSG(\"R800\")\nG2 X1 Y1 CR=5\nCYCLE800()\n"
                           "CYCLE800(0,\"H\",200000,54,0,0,0,0,-90,0,0,0,0,-1,0,1)\n",
    "B_G17_SLIDE_020_HF5": "G0 X0\nCYCLE81(1,0,1,-5)\nTRAFOOF\nG40\nCYCLE800()\n",
    "B_G17_SLIDE_030_HF5": "CYCLE800(0,\"H\",200000,54,0,0,0,0,-90,0,0,0,0,1,0,101)\nG42 X0\nR[R2]=1\n"
                           "CYCLE800(0,\"H\",200000,54,0,0,0,0,0,0,0,0,0,1,0,101)\n",
    "B_G17_SLIDE_040_HF5": "CYCLE800(0,\"TURN_TRAFO\",210,57,,,,0,0,0,,,,-1,0,102)\nG1 X1\n",
}


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
                            f.write(NC_TEXT.get(c.Name, "; " + c.Name))
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
    shutil.rmtree(OUTDIR, ignore_errors=True)    # B lists, tool sheets, tool load programs
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
    m.TLM_FILES = tuple(TLM_FILES)
    m.run()
    left = len(gui.SCRIPT)
    gui.SCRIPT.clear()
    return m, left


def nc_files():
    d = os.path.join(DOCDIR, "NC")
    return sorted(os.listdir(d)) if os.path.isdir(d) else []


LOGP = os.path.join(tmp, "go_to_machine_log.txt")
OUTDIR = os.path.join(DOCDIR, "go to machine")   # every output except the NC files
BLIST = os.path.join(OUTDIR, "G17_SLIDE_OP10_B_PROGRAMS.json")
ORDER = os.path.join(OUTDIR, "G17_SLIDE_OP10_ORDER.xlsx")
MPF = os.path.join(OUTDIR, "G17_SLIDE_OP10_TOOL_LOAD.MPF")


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


sys.path.insert(0, LIB)
import office_fill as OF   # noqa: E402
F_POST, F_BLIST, F_MDA = "Post the B programs", "B program list (generator)", "Tool load MDA"
F_ORDER, F_SISTER, F_SETUP = "Order sheet", "Sister tool sheet", "NC master setup sheet"
F_PROG, F_SHEET = "Programmer", "Sister sheet (sisters, tool life)"


def funcs(*ticked, **text):
    """Answer screen 2: tick these functions (the rest unticked); text = {label: value} for Programmer / Sister sheet."""
    def f(dlg):
        d = dlg.defaults()
        for k in (F_POST, F_BLIST, F_MDA, F_ORDER, F_SISTER, F_SETUP):
            d[k] = k in ticked
        d.update(text)
        return True, d
    return f


def keep():
    return lambda dlg: (True, dlg.defaults())


PICK = ans(Package="Pick functions")
CHECK_ONLY = [PICK, funcs()]


def order_rows(path=None):
    """Order sheet lines as dicts (header row 4)."""
    v = OF.xlsx_values(path or ORDER)
    head = [v.get("%s4" % c) for c in "ABCDEFGH"]
    out, r = [], 5
    while v.get("A%d" % r):
        out.append({h: v.get("%s%d" % (c, r), "") for h, c in zip(head, "ABCDEFGH")})
        r += 1
    return out

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
m, left = run(CHECK_ONLY)
box = flat(gui.BOXES[-1])
rep = "\n".join(gui.OUTPUT)
check(left == 0 and PostSet.calls == [] and nc_files() == [] and not os.path.exists(BLIST), "pick functions, nothing ticked: check only, nothing written")
check("4 B programs: 1 pass, 3 fail." in box and "Check only: nothing posted" in box, "check only: counts in the message")
check("OK   B_G17_SLIDE_010_HF5" in rep and "FAIL B_G17_SLIDE_020_HF5" in rep, "report: OK / FAIL per B program")
check("3: Drill: " + rc.R_COLLISION in rep and "4: Face: " + rc.R_NOT_SIM in rep, "report: reason per failing job")
check("5: Face finish: not calculated (NEEDS_CALCULATION)" in rep and "6: Face errors: has errors" in rep, "report: not calculated, errors")
check("B_G17_SLIDE_111_HF5  (more than one tool)" in rep and "G17 old name  (not a B program name" in rep and "notes" not in rep,
      "report: mixed and old-name compound jobs listed as not posted; notes skipped")
check(os.path.exists(LOGP) and "FAIL B_G17_SLIDE_030_HF5" in open(LOGP).read(), "log written")
s1 = gui.SHOWN[0][1]
check([f[1] for f in s1] == ["Joblist", "Part number", "Machine", "Package"] and s1[3][2][0] == ["Validation", "Production", "Pick functions"],
      "screen 1: joblist, part, machine, package (Validation / Production / Pick functions)")
s2 = {f[1]: f[2] for f in gui.SHOWN[1][1]}
check(all(s2[k] is False for k in (F_POST, F_BLIST, F_MDA, F_ORDER, F_SISTER, F_SETUP)) and F_SHEET in s2 and F_PROG in s2,
      "screen 2 (pick functions): every function unticked, programmer and sister sheet fields")

# ---------------- one Simulation Center run with a collision marks many B programs: one line in the pop-up ----------------
def build_run(n):
    import uuid as _uuid
    for x in os.listdir(POFDIR):
        os.remove(os.path.join(POFDIR, x))
    em = om.Tool("10047210", "End mill", "endMill", 0.4724)
    cs = []
    for i in range(n):
        u = str(_uuid.uuid4())
        cs.append(om.CompoundJob("B_G17_SLIDE_%03d_HF5" % (10 * (i + 2)), [PJob("%d: Contour" % (i + 1), em, pof(100 + i, u))]))
        ccrpt(u, 0)                                   # the whole run had a collision
    cs.append(om.CompoundJob("B_G17_SLIDE_%03d_HF5" % (10 * (n + 2)), [PJob("%d: Face" % (n + 1), em, pof(200, str(_uuid.uuid4())))]))
    model = om.Model([om.JobList("Op10", cs)], inch=True)
    model.JobListSet = PostSet(model.JobListSet.GetJobLists())
    om._App.CurrentDocument = om.Document(DOC, model)
    PostSet.calls = []


build_run(30)
m, left = run(CHECK_ONLY)
box = gui.BOXES[-1]
check(left == 0 and "had a collision: 30 B programs marked (B_G17_SLIDE_020_HF5 ... B_G17_SLIDE_310_HF5)." in flat(box) and
      "Simulate each B program on its own" in box and box.count("\n") < 16,
      "30 B programs from one collision run: one line, not 30 (%d lines)" % (box.count("\n") + 1))
check("Fail:" in box and "B_G17_SLIDE_320_HF5  " + rc.R_NOT_SIM in box, "other failures still listed per B program")
check(sum(1 for x in gui.OUTPUT[-1].split("\n") if rc.R_COLLISION in x) == 30, "output window keeps the full list (30 collision lines)")

# ---------------- post, failures: post nothing ----------------
build()
m, left = run([PICK, funcs(F_POST, F_BLIST), post_pick(0)])
check(left == 0 and PostSet.calls == [] and "Nothing posted." in gui.BOXES[-1], "warning answered No: nothing posted")
check(any("WARNING: 3 of 4 B programs fail the check." in b for b in gui.BOXES), "warning box before the choice")
opts = gui.SHOWN[-1][1][0][2][0]
check(opts == ["No - post nothing", "Post all 4 (3 fail the check)", "Post only the 1 that pass"], "warning choices: %s" % opts)
check(gui.SHOWN[-1][0].endswith("WARNING: 3 fail the check"), "warning dialog title")

# ---------------- post only the ones that pass, list: only the posted ----------------
cs = build()
m, left = run([PICK, funcs(F_POST, F_BLIST, F_ORDER), post_pick(2), include_pick(0)])
box = flat(gui.BOXES[-1])
check(left == 0 and PostSet.calls == [[cs[1].UUID]], "post only passing: CalculateNC with the one passing compound job UUID")
check(nc_files() == ["B_G17_SLIDE_010_HF5.mpf"] and "NC files written or updated: 1" in box and "NC/B_G17_SLIDE_010_HF5.mpf" in box.replace("\\", "/"),
      "post: written NC file found and listed")
check("No NC file found" not in box and "Posted 1 B program (CalculateNC returned True)." in box, "post: message")
inc = gui.SHOWN[-1]
check(inc[0].endswith("B program list and documents") and inc[1][0][2][0] == ["Only the 1 posted", "All 4 B programs"],
      "only some posted: asks what the list and documents hold (only posted first)")
data = json.load(open(BLIST))
check([s["step"] for s in data["steps"]] == [10] and "B program list for the generator (Import B list): 1 B program" in box,
      "list: only the posted B program")
nposted = [r["name"] for r in data["refused"] if r["reason"].startswith("not posted")]
check(nposted == ["B_G17_SLIDE_020_HF5", "B_G17_SLIDE_030_HF5", "B_G17_SLIDE_040_HF5"], "list: the 3 not posted listed as refused 'not posted'")
rows = order_rows()
check(len(rows) == 1 and rows[0]["Description"] == "End mill" and rows[0]["Qty"] == 1 and rows[0]["For tool"] == "10047210"
      and rows[0]["Check"] == "order no. is the tool name: check", "order sheet: the posted B program's one tool, qty 1, order no. flagged")
check("Order sheet: 1 line, 1 to check (yellow)" in box and "G17_SLIDE_OP10_ORDER.xlsx" in box, "message: order sheet path")

# ---------------- post only the ones that pass, list: all ----------------
cs = build()
m, left = run([PICK, funcs(F_POST, F_BLIST, F_ORDER), post_pick(2), include_pick(1)])
data = json.load(open(BLIST))
check(left == 0 and PostSet.calls == [[cs[1].UUID]] and [s["step"] for s in data["steps"]] == [10, 20, 30, 40],
      "list: all B programs when chosen (only 010 posted)")
check(not any(r["reason"].startswith("not posted") for r in data["refused"]), "list: nothing marked not posted")
rows = order_rows()
check(sorted(r["Description"] for r in rows) == ["Drill", "End mill", "Face"], "order sheet: every tool of the 4 B programs")
box = flat(gui.BOXES[-1])
check("Tool numbers not in the HELLER standard" in box and "No holder in hyperMILL" in box, "message: tool numbers and holders to fix")

# ---------------- post all ----------------
cs = build()
m, left = run([PICK, funcs(F_POST, F_BLIST, F_ORDER), post_pick(1)])
check(PostSet.calls == [[c.UUID for c in cs[1:5]]] and len(nc_files()) == 4, "post all: 4 UUIDs, 4 NC files")
check("Posted although 3 fail the check." in flat(gui.BOXES[-1]), "post all: message says posted with failures")
check("POSTED WITH FAILURES" in open(LOGP).read(), "post all: log records the override")
check(len(gui.SHOWN) == 3 and len(order_rows()) == 3, "post all: no list question; order sheet with all 3 tools")
check(os.path.exists(BLIST) and os.path.exists(ORDER) and
      not [n for n in os.listdir(DOCDIR) if n.endswith((".json", ".csv", ".MPF", ".xlsx"))] and
      ("go to machine" + os.sep + "G17_SLIDE_OP10_B_PROGRAMS.json") in gui.BOXES[-1],
      "pick functions: outputs in <document folder>\\go to machine, none next to the document; NC files stay in NC")
facts = {s["program"]: (s.get("radius_comp"), s.get("r_params")) for s in json.load(open(BLIST))["steps"]}
check(facts == {"B_G17_SLIDE_010_HF5": (True, [1, 12]), "B_G17_SLIDE_020_HF5": (False, []), "B_G17_SLIDE_030_HF5": (True, [2]),
                "B_G17_SLIDE_040_HF5": (False, [])},
      "posted NC read: G41/G42 and R numbers (comments, strings, CR= and G40 ignored) %s" % facts)
box = flat(gui.BOXES[-1])
check("R parameters in posted B programs" in box and "B_G17_SLIDE_010_HF5 (R1, R12)" in box and "R[...] with a computed number" in box and
      "No G41/G42" in box, "message: R parameters, indirect R and missing G41/G42 named")
pl = {s["program"]: (s.get("cycle800"), s.get("cycle800_note")) for s in json.load(open(BLIST))["steps"]}
check(pl == {"B_G17_SLIDE_010_HF5": ('CYCLE800(1,"H",200000,54,0,0,0,0,-90,0,0,0,0,1,0,101)', None),
             "B_G17_SLIDE_020_HF5": ("", None), "B_G17_SLIDE_030_HF5": (None, "SEVERAL"), "B_G17_SLIDE_040_HF5": (None, "TURNING")},
      "CYCLE800 planes: one (retraction / direction ignored), none, several, turning alignment only %s" % pl)
check("Several CYCLE800 planes, none stored" in box and "B_G17_SLIDE_030_HF5" in box and "Only a turning-tool CYCLE800" in box,
      "message: several planes and turning alignment named")
csvrow = [r for r in csv.DictReader(open(BLIST[:-5] + ".csv", encoding="utf-8-sig")) if r["program"] == "B_G17_SLIDE_010_HF5"][0]
check(csvrow["cycle800"].startswith("CYCLE800(1,") , "csv: cycle800 column")
check(csvrow["radius_comp"] == "True" and csvrow["r_params"] == "1 12", "csv: radius_comp and r_params columns")

# ---------------- not posting: list and NC facts from the NC files already there ----------------
build(all_pass=True)
os.makedirs(os.path.join(DOCDIR, "NC"), exist_ok=True)
with open(os.path.join(DOCDIR, "NC", "B_G17_SLIDE_010_HF5.mpf"), "w") as f:
    f.write(NC_TEXT["B_G17_SLIDE_010_HF5"])
m, left = run([PICK, funcs(F_BLIST)])
facts = {s["program"]: s.get("radius_comp") for s in json.load(open(BLIST))["steps"]}
check(left == 0 and PostSet.calls == [] and facts["B_G17_SLIDE_010_HF5"] is True and "Not posted (Post the B programs unticked)" in gui.BOXES[-1],
      "list without posting: NC facts from the NC file already there")

# ---------------- everything passes: confirm ----------------
cs = build(all_pass=True)
m, left = run([PICK, funcs(F_POST, F_BLIST), post_pick(1)])
check(gui.SHOWN[-1][0].endswith("confirm") and gui.SHOWN[-1][1][0][2][0] == ["No - do not post", "Yes - post 4 B programs"],
      "all pass: plain confirm, No first")
check(PostSet.calls == [[c.UUID for c in cs[1:5]]] and not any(b.startswith("WARNING") for b in gui.BOXES), "all pass: posted, no warning")
build(all_pass=True)
m, left = run([PICK, funcs(F_POST, F_BLIST), post_pick(0)])
check(PostSet.calls == [] and "Nothing posted." in gui.BOXES[-1], "all pass, confirm No: nothing posted")

# ---------------- duplicate step: stop ----------------
build(dup=True)
m, left = run([PICK, funcs(F_POST, F_BLIST)])
check(left == 0 and PostSet.calls == [] and "Nothing posted, nothing written. Fix these first" in flat(gui.BOXES[-1]) and "used twice" in gui.BOXES[-1],
      "step used twice: stops before posting")

# ---------------- CalculateNC fails / writes nothing ----------------
build(all_pass=True)
PostSet.mode = "raise"
m, left = run([PICK, funcs(F_POST, F_BLIST), post_pick(1)])
check("Posting failed: RuntimeError: post processor not found" in flat(gui.BOXES[-1]), "CalculateNC error reported")
build(all_pass=True)
PostSet.mode = "nothing"
m, left = run([PICK, funcs(F_POST, F_BLIST), post_pick(1)])
check("No NC file found for:" in gui.BOXES[-1] and "B_G17_SLIDE_040_HF5" in gui.BOXES[-1], "CalculateNC wrote nothing: B programs without an NC file listed")
PostSet.mode = "write"

# ---------------- tool load MDA (pick functions, no sister sheet: screens) ----------------
for f in ("tool_load_mda_last.json",):
    if os.path.exists(os.path.join(tmp, f)):
        os.remove(os.path.join(tmp, f))
cs = build(all_pass=True)
m, left = run([PICK, funcs(F_POST, F_BLIST, F_MDA, **{F_SHEET: ""}), post_pick(1), counts(**{"10047210": ("2", "50"), "905083900": ("0", "")})])
box = flat(gui.BOXES[-1])
labels = [f[1] for f in gui.SHOWN[-1][1]]
check(gui.SHOWN[-1][0].startswith("Tool load MDA | tools 1-3 of 3") and "10047210  D0.4724  tool life (SETPIECE)" in labels,
      "MDA screen after posting: the 3 tools of the B programs, SETPIECE tools marked")
txt = open(MPF).read()
check(txt.count('NEWT("10047210",') == 3 and txt.count('NEWT("11039410",') == 1 and txt.count('NEWT("905083900",') == 1,
      "MDA (sisters = extras): end mill + 2 = 3, drill 1, face mill 0 sisters = 1 (not left out)")
check(txt.count("$TC_MOP13[R999,1]=50") == 3 and "go_to_machine Op10" in txt, "MDA: tool life 50 on the end mills; source in the header")
check("Tool load MDA: 3 tools + 2 extra sisters (5 entries)" in box and "G17_SLIDE_OP10_TOOL_LOAD.MPF" in box, "message: MDA path and counts")
check("left out" not in box and "WARNING - SETPIECE counts these tools but no tool life was entered" in box
      and "11039410" in box.split("WARNING - SETPIECE")[1], "message: nothing left out; SETPIECE-without-tool-life warning")
check(json.load(open(os.path.join(tmp, "tool_load_mda_last.json"))).get("10047210") == [2, 50], "MDA values remembered")

build(all_pass=True)
m, left = run([PICK, funcs(F_POST, F_MDA, **{F_SHEET: ""}), post_pick(1), keep()])
fields = {f[1]: f[2] for f in gui.SHOWN[-1][1]}
check(fields.get("10047210  D0.4724  sisters") == "2" and fields.get("10047210  D0.4724  tool life (SETPIECE)") == "50",
      "second run: remembered sisters and tool life offered")

build(all_pass=True)
m, left = run([PICK, funcs(F_POST, F_BLIST, F_MDA, **{F_SHEET: ""}), post_pick(1), lambda dlg: (False, {})])
check(left == 0 and "Tool load MDA cancelled: not written." in flat(gui.BOXES[-1]) and not os.path.exists(MPF) and os.path.exists(BLIST),
      "MDA screen cancelled: posted, list written, no MDA")

build(all_pass=True)
m, left = run([PICK, funcs(F_POST, F_BLIST), post_pick(1)])
check(left == 0 and not os.path.exists(MPF) and "Tool load MDA" not in gui.BOXES[-1], "MDA unticked: no screen, no program")

build(all_pass=True)
TLM_FILES[:] = [os.path.join(tmp, "nowhere", "tool_load_mda.py")]
m, left = run([PICK, funcs(F_POST, F_MDA), post_pick(1)])
check(left == 0 and "Tool load MDA not written: tool_load_mda.py not found" in flat(gui.BOXES[-1]), "tool_load_mda missing: says so")
TLM_FILES[:] = [TLM]

# ---------------- Validation: post, list, MDA without sisters, order sheet qty 1, sister sheet ----------------
import datetime   # noqa: E402
import openpyxl   # noqa: E402
TODAY = datetime.date.today().strftime("%Y-%m-%d")
VAL = os.path.join(OUTDIR, "VALIDATION_" + TODAY)
PROD = os.path.join(OUTDIR, "PRODUCTION_" + TODAY)
cs = build(all_pass=True)
m, left = run([ans(Package="Validation"), funcs(F_POST, F_BLIST, F_MDA, F_ORDER, F_SISTER, **{F_PROG: "ES"}), post_pick(1)])
s2 = {f[1]: f[2] for f in gui.SHOWN[1][1]}
check([k for k in (F_POST, F_BLIST, F_MDA, F_ORDER, F_SISTER, F_SETUP) if s2[k]] == [F_POST, F_BLIST, F_MDA, F_ORDER, F_SISTER]
      and F_SHEET not in s2, "Validation preset: post, list, MDA, order sheet, sister sheet ticked; no setup sheet; no sister sheet field")
vfiles = sorted(os.listdir(VAL)) if os.path.isdir(VAL) else []
check(left == 0 and vfiles == ["G17_SLIDE_OP10_B_PROGRAMS.csv", "G17_SLIDE_OP10_B_PROGRAMS.json", "G17_SLIDE_OP10_ORDER.xlsx",
                               "G17_SLIDE_OP10_SISTERS.xlsx", "G17_SLIDE_OP10_TOOL_LOAD.MPF"],
      "Validation files in go to machine\\VALIDATION_<date>: %s" % vfiles)
vt = open(os.path.join(VAL, "G17_SLIDE_OP10_TOOL_LOAD.MPF")).read()
check(vt.count("=NEWT(") == 3 and "$TC_MOP13" not in vt and not any(t[0].startswith("Tool load MDA | tools") for t in gui.SHOWN),
      "Validation MDA: one of each tool, no tool life, no sisters screen")
check(all(r["Qty"] == 1 for r in order_rows(os.path.join(VAL, "G17_SLIDE_OP10_ORDER.xlsx"))), "Validation order sheet: qty 1 each")
SIS = os.path.join(VAL, "G17_SLIDE_OP10_SISTERS.xlsx")
ws = openpyxl.load_workbook(SIS).active
check(ws["A12"].value == "10047210" and ws["A13"].value == "11039410" and ws["A14"].value == "905083900" and ws["B7"].value == "ES"
      and ws["G12"].value is None, "sister sheet: tools in first-use order, programmer, Sisters left to fill")
# filled in during prove-out (Excel)
wb = openpyxl.load_workbook(SIS)
wb.active["G12"] = 2; wb.active["I12"] = 50; wb.active["G14"] = 1
wb.save(SIS)

# ---------------- Production: sister sheet read, MDA with sisters, order 1 + sisters, setup sheet ----------------
saved_sheet = open(SIS, "rb").read()
build(all_pass=True)                                  # build() clears "go to machine": put the filled sheet back
os.makedirs(VAL, exist_ok=True)
open(SIS, "wb").write(saved_sheet)
m, left = run([ans(Package="Production"), keep(), post_pick(1)])
s2 = {f[1]: f[2] for f in gui.SHOWN[1][1]}
check(s2.get(F_SHEET) == SIS and s2[F_SETUP] and not s2[F_SISTER] and s2.get(F_PROG) == "ES",
      "Production preset: setup sheet on, sister sheet off, the newest validation sister sheet offered, programmer remembered")
pt = open(os.path.join(PROD, "G17_SLIDE_OP10_TOOL_LOAD.MPF")).read()
check(pt.count('NEWT("10047210",') == 3 and pt.count('NEWT("905083900",') == 2 and pt.count("$TC_MOP13[R999,1]=50") == 3
      and not any(t[0].startswith("Tool load MDA | tools") for t in gui.SHOWN),
      "Production MDA from the sheet: end mill + 2, face mill + 1, tool life 50, no screens")
qty = {r["For tool"]: r["Qty"] for r in order_rows(os.path.join(PROD, "G17_SLIDE_OP10_ORDER.xlsx"))}
check(qty == {"10047210": 3, "11039410": 1, "905083900": 2}, "Production order sheet: 1 + sisters %s" % qty)
import docx   # noqa: E402
sd = docx.Document(os.path.join(PROD, "G17_SLIDE_OP10_SETUP.docx"))
t1 = sd.tables[1]
check([c.text.strip() for c in t1.rows[1].cells][:2] == ["10047210", "End mill"] and t1.rows[1].cells[6].text.strip() == "3"
      and t1.rows[1].cells[7].text.strip() == "50", "setup sheet: end mill QTY 3, tool life 50")

check(("HYPERMILL SIM DATE: " + TODAY) in sd.tables[0].rows[0].cells[-1].text and "P/N: G17_SLIDE" in sd.tables[0].rows[0].cells[1].text,
      "setup sheet header: P/N and the Simulation Center date")

# production without a sister sheet: stops before posting
shutil.rmtree(VAL, ignore_errors=True)
build(all_pass=True)
m, left = run([ans(Package="Production"), keep()])
check(left == 0 and PostSet.calls == [] and "Production needs the sister sheet" in gui.BOXES[-1], "Production without a sister sheet: stops, nothing posted")

# ---------------- input errors and no B programs ----------------
build()
m, left = run([ans(Part_number="G17-SLIDE")])
check("Fix these first" in gui.BOXES[-1] and PostSet.calls == [], "part number with - refused")
build()
m, left = run([ans(Machine="F5000"), funcs()])
check("Run B program rename" in gui.BOXES[-1], "no B programs for that machine: says so")

shutil.rmtree(tmp, ignore_errors=True)
print()
print("FAILURES: %d" % len(fails) if fails else "ALL GO TO MACHINE CHECKS PASSED")
sys.exit(1 if fails else 0)
