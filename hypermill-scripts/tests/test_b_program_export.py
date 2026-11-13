#!/usr/bin/env python3
"""Headless test of b_program_export.py and the export side of b_programs.py (fake om in tests/fake_om).
Run: python3 tests/test_b_program_export.py [copy-sample-to.json]"""
import os
import sys
import json
import shutil
import tempfile
import importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(HERE, "fake_om"))
import om                      # noqa: E402  (fake)
import om.cad.gui as gui       # noqa: E402  (fake)

LIB = os.path.join(ROOT, "copy_to_python_folder", "tool_library")
SCRIPT = os.path.join(ROOT, "copy_to_python_folder", "b_program_export", "b_program_export.py")
fails = []


def flat(t):
    return " ".join(str(t).split())


def check(cond, label):
    print(("ok   " if cond else "FAIL ") + label)
    if not cond:
        fails.append(label)


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


bp = load(os.path.join(LIB, "b_programs.py"), "bp_under_test")

# ---------------- rules ----------------
rules = [
    dict(tool_type="drilTool", dia_min="", dia_max="0.125", units="INCH", brk_check="0", brk_tol="", measure="1",
         measure_always="0", max_brk="2", life="1", setpiece="1", note="small drills: no break check"),
    dict(tool_type="drilTool", dia_min="", dia_max="", units="INCH", brk_check="1", brk_tol="0.01", measure="1",
         measure_always="1", max_brk="3", life="1", setpiece="1", note="drills"),
    dict(tool_type="*", dia_min="", dia_max="", units="METRIC", brk_check="1", brk_tol="0.3", measure="1",
         measure_always="0", max_brk="2", life="2", setpiece="1", note="anything else"),
]
r = bp.match_rule(rules, "drilTool", 0.1, True)
check(r is rules[0], "small drill matches the first drill row")
r = bp.match_rule(rules, "DRILTOOL", 0.75, True)
check(r is rules[1], "0.75 drill matches the general drill row (type case-insensitive)")
p = bp.presets(rules[1], True)
check(p["brk_tol"] == "0.0100" and p["meas_always"] and p["max_brk"] == 3, "drill presets: tol 0.0100 in, always, max 3")
p = bp.presets(bp.match_rule(rules, "endMill", 0.5, True), True)
check(p["brk_tol"] == "0.0118" and p["life"] == 2, "metric 0.3 mm row in an inch document -> 0.0118")
p = bp.presets(bp.match_rule(rules, "drilTool", 20.0, False), False)
check(p["brk_tol"] == "0.254", "inch 0.01 row in a metric document -> 0.254 mm")
r = bp.match_rule(rules, "drilTool", 3.0, False)
check(r is rules[0], "3 mm drill in a metric document = 0.118 in < 0.125: small drill row")
shipped = bp.load_rules(os.path.join(LIB, "brk_rules.csv"))
check(len(shipped) == 4, "shipped brk_rules.csv: 4 rows (drills, rough, finish, rest)")
tol = lambda t, purpose, d=0.5: bp.presets(bp.match_rule(shipped, t, d, True, purpose), True)["brk_tol"]
check(tol("drilTool", "") == "0.0020" and tol("drilTool", "rough") == "0.0020", "standard: drills 0.002 whatever the stock")
check(tol("faceMill", "rough", 2.0) == "0.0040" and tol("endMill", "rough") == "0.0040", "standard: roughing 0.004")
check(tol("endMill", "finish") == "", "standard: finishing range .00005-.0005 left blank until set")
check(tol("tapTool", "") == "", "no stock to leave (tap): blank")
check(bp.presets(bp.match_rule(shipped, "drilTool", 20.0, False, ""), False)["brk_tol"] == "0.051", "metric document: drill 0.002 in -> 0.051 mm")
J = om.Job
check(bp.job_purpose(J("r", None, {"*AUFMASS": "0.019685", "*AUFMASS_HORI": "0"})) == "rough", "stock to leave 0.0197 = rough")
check(bp.job_purpose(J("f", None, {"*AUFMASS": "0", "*AUFMASS_Z": "0"})) == "finish", "zero stock to leave = finish")
check(bp.job_purpose(J("d", None, {"*CHECK_TOL": "0.0039"})) == "", "no allowance key (drilling) = no purpose")
check(bp.compound_purpose(["rough", "finish", ""]) == "finish", "rough + finish in one compound job = finish")
check(bp.step_of("B_00948602_025_0010_HF5", "00948602_025", "HF5") == 10, "step parsed from a 4-digit name")
check(bp.step_of("B_00948602_025_010", "00948602_025", "") == 10, "step parsed without machine")
check(bp.step_of("B_00948602_025_010_HF5", "00948602_025", "") is None, "machine suffix not expected: not a match")
check(bp.step_of("00948602_025_B_OP205_01", "00948602_025", "HF5") is None, "old naming is not a B program name")


# ---------------- document ----------------
def build(doc_path, dup=False):
    T = om.Tool
    fm = T("905083900", "2in Ceramic Facemill", "faceMill", 2.0)
    dr = T("475080900", "19mm Drill", "drilTool", 19.0, "mm")
    tap = T("416580900", "1/4-20 Tap", "tapTool", 0.25)
    spot = T("850080900", "Spot", "spotDrill", 0.5)
    rough, finish = {"*AUFMASS": "0.019685", "*AUFMASS_HORI": "0"}, {"*AUFMASS": "0", "*AUFMASS_Z": "0"}
    em = T("350080900", "1/2 End mill", "endMill", 0.5)
    cs = [om.CompoundJob("------ notes ------"),
          om.CompoundJob("B_00948602_025_010_HF5", [om.Job("a", fm, rough), om.Job("b", fm, rough)]),
          om.CompoundJob("B_00948602_025_020_HF5", [om.Job("c", dr)]),
          om.CompoundJob("B_00948602_025_%s_HF5" % ("020" if dup else "030"), [om.Job("d", tap)]),
          om.CompoundJob("B_00948602_025_040_HF5", [om.Job("h", em, rough), om.Job("i", em, finish)]),
          om.CompoundJob("B_00948602_025_111_HF5", [om.Job("e", tap), om.Job("f", spot)]),
          om.CompoundJob("00948602_025_B_OP299_01", [om.Job("g", fm)])]
    om._App.CurrentDocument = om.Document(doc_path, om.Model([om.JobList("00948602-025_B_OP200_02", cs)], inch=True))


def run(answers):
    gui.SCRIPT[:] = answers
    gui.BOXES.clear()
    m = load(SCRIPT, "bpe_under_test")
    m.run()
    gui.SCRIPT.clear()


def ans(**kv):
    def f(dlg):
        d = dlg.defaults()
        d.update({k.replace("_", " "): v for k, v in kv.items()})
        return True, d
    return f


tmp = tempfile.mkdtemp(prefix="bpe_")
tempfile.tempdir = tmp
docdir = os.path.join(tmp, "job")
os.makedirs(docdir)
doc = os.path.join(docdir, "00948602_025_A_OP200_03.hmc")
build(doc)
with open(os.path.join(tmp, "b_program_rename_last.json"), "w") as f:
    json.dump({"part": "00948602_025", "machine": "HF5"}, f)
run([ans()])
pj = os.path.join(docdir, "00948602_025_A_OP200_03_B_PROGRAMS.json")
check(os.path.exists(pj) and os.path.exists(pj.replace(".json", ".csv")), "json and csv written next to the document")
data = json.load(open(pj))
check(data["format"] == "SINUMERIK_B_PROGRAM_LIST" and data["version"] == 1 and data["units"] == "INCH", "format, version, units")
check(data["part"] == "00948602_025" and data["machine"] == "HF5", "part and machine from the last rename")
check([s["step"] for s in data["steps"]] == [10, 20, 30, 40], "steps 10, 20, 30, 40 in tree order")
check([s["tool"] for s in data["steps"]] == ["905083900", "475080900", "416580900", "350080900"], "tool = tool ID")
check(data["steps"][1]["tool_type"] == "drilTool" and abs(data["steps"][1]["diameter"] - 0.748) < 0.001,
      "19 mm drill exported as drilTool D0.748 in")
check(data["steps"][0]["jobs"] == 2, "job count per compound job")
check([s["brk_tol"] for s in data["steps"]] == ["0.0040", "0.0020", "", ""], "presets: face mill rough 0.004, drill 0.002, tap blank, rough+finish blank")
check([s["purpose"] for s in data["steps"]] == ["rough", "", "", "finish"], "purpose per B program")
reasons = {r["name"]: r["reason"] for r in data["refused"]}
check(set(reasons) == {"B_00948602_025_111_HF5", "00948602_025_B_OP299_01"}, "refused: mixed tools and old naming")
check("more than one tool" in reasons["B_00948602_025_111_HF5"], "refused reason: more than one tool")
check(not any("notes" in r["name"] for r in data["refused"]), "notes are not listed")
check("4 B programs written" in flat(gui.BOXES[-1]) and "2 steps with break check on and no tolerance" in flat(gui.BOXES[-1]),
      "final message: 4 written, 2 blank tolerances")
shutil.copy(pj, os.path.join(tmp, "sample.json"))

# duplicate step -> nothing written
os.remove(pj)
build(doc, dup=True)
run([ans()])
check(not os.path.exists(pj) and "used twice" in flat(gui.BOXES[-1]), "duplicate step: nothing written, message names it")

# wrong machine -> nothing matches
build(doc)
run([ans(Machine="F5000")])
check("Nothing written" in flat(gui.BOXES[-1]), "names for another machine: nothing written")

# unwritable / Windows-style document path -> falls back to the OPEN MIND (here: temp) folder
build(r"C:\jobs\OTHER_DOC.hmc")
run([ans()])
check(os.path.exists(os.path.join(tmp, "OTHER_DOC_B_PROGRAMS.json")), "document folder not writable: written to the fallback folder")

if len(sys.argv) > 1:
    shutil.copy(os.path.join(tmp, "sample.json"), sys.argv[1])
    print("sample written to", sys.argv[1])
print()
print("FAILURES: %d" % len(fails) if fails else "ALL EXPORT CHECKS PASSED")
sys.exit(1 if fails else 0)
