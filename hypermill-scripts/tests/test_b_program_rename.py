#!/usr/bin/env python3
"""Headless test of b_program_rename.py against the fake om module (tests/fake_om).
Run: python3 tests/test_b_program_rename.py"""
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

SCRIPT = os.path.join(ROOT, "copy_to_python_folder", "b_program_rename", "b_program_rename.py")
DOC = r"C:\jobs\00948602_025_A_OP200_03.hmc"
fails = []


def check(cond, label):
    print(("ok   " if cond else "FAIL ") + label)
    if not cond:
        fails.append(label)


def load_script():
    spec = importlib.util.spec_from_file_location("b_program_rename_under_test", SCRIPT)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def fresh_tmp():
    d = tempfile.mkdtemp(prefix="bpr_")
    tempfile.tempdir = d
    return d


# ---------------- document builders ----------------
def build(mode="name", n_one=5, second=False, doc=DOC):
    om.WRITES.clear()
    T = om.Tool
    fm, dr, spot = T("905083900", "2in Ceramic Facemill"), T("416580900"), T("850080900")
    cs = [om.CompoundJob("------ Rough Top Down, 2inch Ceramic ------", mode=mode)]
    for i in range(n_one):
        cs.append(om.CompoundJob("00948602_025_B_OP%03d_01" % (205 + i), [om.Job("%d: T905083900 Rough" % i, fm)], mode=mode))
    cs.insert(3, om.CompoundJob("------ divider ------", mode=mode))
    cs.append(om.CompoundJob("B_00948602_025_111_HF5", [om.Job("a", dr), om.Job("b", spot)], mode=mode))
    cs.append(om.CompoundJob("no tool here", [om.Job("c", None)], mode=mode))
    lists = [om.JobList("00948602-025_B_OP200_02", cs)]
    if second:
        lists.append(om.JobList("OP300", [om.CompoundJob("B_00948602_025_030_HF5", [om.Job("d", fm)], mode=mode)]))
    om._App.CurrentDocument = om.Document(doc, om.Model(lists))
    return lists


def names(lists):
    return [c.Name for jl in lists for c in jl.GetCompoundJobs()]


# ---------------- scripted answers ----------------
def ans(**by_label):
    """OK with the dialog defaults, overridden by label (underscores in keys = spaces)."""
    def f(dlg):
        d = dlg.defaults()
        for k, v in by_label.items():
            d[k.replace("_", " ")] = v
        return True, d
    return f


def inputs(part="00948602_025", machine="HF5", start="10", advance="10", which=0):
    return ans(Part_number=part, Machine=machine, Starting_step=start, Advance=advance, **{"Compound jobs": which})


def confirm(yes):
    return lambda dlg: (True, {dlg.fields[0][1]: 1 if yes else 0})


def cancel(dlg):
    return False, {}


def run(answers, action=0, scope=0):
    gui.SCRIPT[:] = [ans(Action=action, Joblist=scope)] + answers
    gui.BOXES.clear()
    gui.SHOWN.clear()
    m = load_script()
    m.run()
    left = len(gui.SCRIPT)
    gui.SCRIPT.clear()
    return m, left


# ---------------- scenarios ----------------
fresh_tmp()
L = build()
m, left = run([inputs(), confirm(True)])
want = ["------ Rough Top Down, 2inch Ceramic ------", "B_00948602_025_010_HF5", "B_00948602_025_020_HF5",
        "------ divider ------", "B_00948602_025_030_HF5", "B_00948602_025_040_HF5", "B_00948602_025_050_HF5",
        "B_00948602_025_111_HF5", "no tool here"]
check(names(L) == want, "rename all: tree order 010..050, notes kept, mixed and no-tool untouched")
check(left == 0, "rename all: every scripted screen used")
check("Renamed 5 compound jobs" in gui.BOXES[-1], "rename all: final message")
u = json.load(open(os.path.join(tempfile.gettempdir(), "b_program_rename_undo.json")))
check(len(u["items"]) == 5 and u["items"][0]["old"] == "00948602_025_B_OP205_01", "rename all: undo file holds the 5 old names")
review = gui.BOXES[-2]
check("Not renamed" in review and "B_00948602_025_111_HF5" in review and "no tool here" in review,
      "review lists the mixed and no-tool compound jobs")
check(any("<- 00948602_025_B_OP205_01" in o for o in gui.OUTPUT), "output window holds the old -> new list")
dlg_title = gui.SHOWN[1][0]
check("5 to rename, 2 notes, 2 not renamable" in dlg_title, "input screen title counts: " + dlg_title)

# undo
m, left = run([confirm(True)], action=1)
check(names(L)[1] == "00948602_025_B_OP205_01" and names(L)[6] == "00948602_025_B_OP209_01", "undo puts the old names back")
check(os.path.exists(os.path.join(tempfile.gettempdir(), "b_program_rename_undo_used.json")), "undo file moved to _used")
m, left = run([], action=1)
check("No rename to undo" in gui.BOXES[-1], "second undo: nothing to undo")

# review only
fresh_tmp()
L = build()
before = names(L)
m, left = run([inputs(), confirm(False)])
check(names(L) == before and not om.WRITES, "answer No: nothing written")
check("Nothing renamed" in gui.BOXES[-1], "answer No: message")

# cancel at inputs
fresh_tmp()
L = build()
m, left = run([cancel])
check(names(L) == before and not om.WRITES, "cancel at inputs: nothing written")

# bad inputs, then fixed
fresh_tmp()
L = build()
m, left = run([inputs(part="00948602-025"), inputs(start="1"), inputs(machine="HAAS_EC500"), inputs(), confirm(True)])
check(any("letters, digits and _" in b for b in gui.BOXES), "part number with - refused")
check(any("probe program" in b for b in gui.BOXES), "starting step 1 refused (probe step)")
check(any("machine can be at most 5" in b for b in gui.BOXES), "machine too long: shows the 5-character room (3-digit steps)")
check(names(L)[1] == "B_00948602_025_010_HF5", "after fixing the inputs the rename runs")

# pick mode: untick the second one
fresh_tmp()
L = build()

def untick_second(dlg):
    d = dlg.defaults()
    d[dlg.fields[1][1]] = False
    return True, d

m, left = run([inputs(which=1), untick_second, confirm(True)])
check(names(L)[1:3] == ["B_00948602_025_010_HF5", "00948602_025_B_OP206_01"] and names(L)[4] == "B_00948602_025_020_HF5",
      "pick: unticked job keeps its name and takes no number")
check(gui.SHOWN[2][0].endswith("pick 1 of 1") and sum(1 for f in gui.SHOWN[2][1] if f[0] == "bool") == 5, "pick screen shows the 5 candidates")

# 4-digit steps
fresh_tmp()
L = build(n_one=120)
m, left = run([inputs(), confirm(True)])
nn = [n for n in names(L) if n.startswith("B_") and n != "B_00948602_025_111_HF5"]
check(nn[0] == "B_00948602_025_0010_HF5" and nn[-1] == "B_00948602_025_1200_HF5" and len(nn) == 120,
      "120 jobs by 10: every name 4-digit, last 1200")
check(max(len(n) for n in nn) == 23, "4-digit names are 23 characters")

# pick screens page by 10
fresh_tmp()
L = build(n_one=23)
m, left = run([inputs(which=1), ans(), ans(), ans(), confirm(True)])
check(left == 0 and gui.SHOWN[4][0].endswith("pick 3 of 3"), "23 candidates = 3 pick screens")

# collision with a compound job in another joblist that is not renamed
fresh_tmp()
L = build(second=True)
m, left = run([inputs(), cancel], scope=0)
check(any("already belong" in b and "B_00948602_025_030_HF5" in b for b in gui.BOXES), "collision with another joblist refused")
check(not om.WRITES, "collision: nothing written")

# all joblists: numbering continues into the second joblist
fresh_tmp()
L = build(second=True)
m, left = run([inputs(), confirm(True)], scope=2)
check(names(L)[-1] == "B_00948602_025_060_HF5", "all joblists: numbering continues across joblists")

# Name read-only: falls back to *CPJOBNAME
fresh_tmp()
L = build(mode="cfg")
m, left = run([inputs(), confirm(True)])
check(names(L)[1] == "B_00948602_025_010_HF5", "Name read-only: *CPJOBNAME fallback renames")
check(any(w[0] == "cfg" for w in om.WRITES), "fallback used SetCfgParameters")

# nothing sticks: stops after the first
fresh_tmp()
L = build(mode="stuck")
m, left = run([inputs(), confirm(True)])
check("Renamed 0 of 5, then stopped" in gui.BOXES[-1], "name will not change: stops at the first and says so")
check(names(L)[1] == "00948602_025_B_OP205_01", "stuck: names unchanged")

# undo refuses another document
fresh_tmp()
L = build()
run([inputs(), confirm(True)])
build(doc=r"C:\jobs\OTHER.hmc")
run([], action=1)
check("another document" in gui.BOXES[-1], "undo refuses a different document")

# undo skips a compound job renamed by hand since
fresh_tmp()
L = build()
run([inputs(), confirm(True)])
L[0].GetCompoundJobs()[2].Name = "HAND EDIT"
run([confirm(True)], action=1)
check("renamed since: HAND EDIT" in gui.BOXES[-1] and names(L)[1] == "00948602_025_B_OP205_01", "undo skips a hand-edited name, restores the rest")

# rerun on already-named jobs: nothing to rename
fresh_tmp()
L = build()
run([inputs(), confirm(True)])
run([inputs()])
check("0 compound jobs to rename, 5 already named" in gui.BOXES[-1], "second run: all already named, no confirm screen")

# log written
check(os.path.exists(os.path.join(tempfile.gettempdir(), "b_program_rename_log.txt")), "log written")

print()
print("FAILURES: %d" % len(fails) if fails else "ALL RENAME CHECKS PASSED")
sys.exit(1 if fails else 0)
