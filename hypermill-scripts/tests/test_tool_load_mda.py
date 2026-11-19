#!/usr/bin/env python3
"""Headless test of tool_load_mda.py (fake om in tests/fake_om): NEWT per sister, tool life lines, remembered values.
Run: python3 tests/test_tool_load_mda.py"""
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

SCRIPT = os.path.join(ROOT, "copy_to_python_folder", "tool_load_mda", "tool_load_mda.py")
fails = []


def check(cond, label):
    print(("ok   " if cond else "FAIL ") + label)
    if not cond:
        fails.append(label)


tmp = tempfile.mkdtemp(prefix="tlm_")
tempfile.tempdir = tmp
docdir = os.path.join(tmp, "job")
os.makedirs(docdir)
DOC = os.path.join(docdir, "G17 Slide OP10.hmc")
open(DOC, "w").close()
MPF = os.path.join(docdir, "G17_SLIDE_OP10_TOOL_LOAD.MPF")
T = om.Tool
em = T("M_10047210", "MD128-12.0A6LJ-WJ30RA", "endMill", 0.4724, gage=3.6614)
dr = T("M_50016110", "DC180", "drilTool", 0.1614, gage=2.5984)
fm = T("M_90508390", "Face mill", "faceMill", 25.0, unit="mm", gage=120.0)     # metric tool file: converted to inch
ng = T("M_NOGAGE", "No gage", "endMill", 0.25, gage=None)
cs = [om.CompoundJob("B_010", [om.Job("1: Contour", em), om.Job("2: Finish", em)]),
      om.CompoundJob("B_020", [om.Job("3: Drill", dr)]),
      om.CompoundJob("B_030", [om.Job("4: Face", fm), om.Job("5: No gage", ng)])]
om._App.CurrentDocument = om.Document(DOC, om.Model([om.JobList("Op10", cs)]))


def counts(**by_id):
    """Answer the sisters / tool life screen: by_id = {tool id: (sisters, life)} as text."""
    def f(dlg):
        d = dlg.defaults()
        for label in list(d):
            for tid, (s, l) in by_id.items():
                if label.startswith(tid + " "):
                    d[label] = s if label.endswith("sisters") else l
        return True, d
    return f


def run(answers):
    gui.SCRIPT[:] = answers
    gui.BOXES.clear()
    gui.SHOWN.clear()
    spec = importlib.util.spec_from_file_location("tlm_under_test", SCRIPT)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    m.OPEN_FILE = False
    m.run()
    left = len(gui.SCRIPT)
    gui.SCRIPT.clear()
    return m, left


m, left = run([lambda dlg: (True, {"Tools from": 0}), counts(M_10047210=("2", "50"), M_90508390=("1", ""))])
check(left == 0 and os.path.exists(MPF), "program written next to the document")
txt = open(MPF).read()
check(txt.count('NEWT("M_10047210",') == 2 and 'R999=NEWT("M_10047210",2)' in txt and 'R999=NEWT("M_50016110",1)' in txt,
      "NEWT per sister: 2 for the end mill, 1 (default) for the drill")
check(txt.count("$TC_MOP13[R999,1]=50") == 2 and txt.count("$TC_TP9[R999]=2") == 2, "tool life 50 on both end mill sisters")
check("$TC_DP1[R999,1]=120" in txt and "$TC_DP1[R999,1]=200" in txt and "$TC_DP1[R999,1]=140" in txt, "Siemens types 120 / 200 / 140")
check("$TC_DP3[R999,1]=4.7244" in txt and "$TC_TPC4[R999]=4.0000" in txt, "metric face mill: gage 120 mm -> 4.7244 in, HD 4.0 below 4 in")
check("M_NOGAGE" not in txt and txt.rstrip().endswith("M30"), "tool without a gage length left out; ends with M30")
check(txt.count('R999=GETT("M_10047210",2)') == 1 and txt.count("IF (R999<=0)") == txt.count("ENDIF") == txt.count("=NEWT(") == 4,
      "every tool and sister: GETT first, NEWT only inside IF (R999<=0) ... ENDIF (already on the control = left as it is)")
i = txt.index('R999=GETT("M_50016110",1)')
check(txt[i:].split("\n")[1] == "IF (R999<=0)" and txt[i:].split("\n")[2] == '  R999=NEWT("M_50016110",1)', "GETT, IF, NEWT in that order")
check("written to" in gui.BOXES[-1] and "Paste it into MDA" in gui.BOXES[-1], "final message")
last = json.load(open(os.path.join(tmp, "tool_load_mda_last.json")))
check(last.get("M_10047210") == [2, 50] and last.get("M_50016110") == [1, 0], "sisters and tool life remembered per tool ID")

# second run: the remembered values are the defaults
m, left = run([lambda dlg: (True, {"Tools from": 0}), lambda dlg: (True, dlg.defaults())])
fields = {f[1]: f[2] for f in gui.SHOWN[-1][1]}
check(fields.get("M_10047210  D0.4724  sisters") == "2" and fields.get("M_10047210  D0.4724  tool life") == "50",
      "second run: remembered sisters 2 and tool life 50 offered")
check(fields.get("M_50016110  D0.1614  tool life") == "", "tool without tool life: blank")

# need_life marks the SETPIECE tools (used by go_to_machine)
spec = importlib.util.spec_from_file_location("tlm2", SCRIPT)
m2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m2)
gui.SCRIPT[:] = [lambda dlg: (True, dlg.defaults())]
gui.SHOWN.clear()
tools = [m2.tool_data(em), m2.tool_data(dr)]
c = m2.ask_counts(tools, {}, {"M_50016110"})
labels = [f[1] for f in gui.SHOWN[-1][1]]
check("M_50016110  D0.1614  tool life (SETPIECE)" in labels and "M_10047210  D0.4724  tool life" in labels, "SETPIECE tools labelled")
check(c == {"M_10047210": (1, 0), "M_50016110": (1, 0)}, "defaults: 1 sister, no tool life")

# all tools in the document; 0 sisters everywhere -> nothing written
os.remove(MPF)
m, left = run([lambda dlg: (True, {"Tools from": 2}), counts(M_10047210=("0", ""), M_50016110=("0", ""), M_90508390=("0", ""))])
check(not os.path.exists(MPF) and "0 sisters" in gui.BOXES[-1], "every tool 0 sisters: no program")

# turning tools: real hyperMILL export of 943580900 (trimmed), a milling-only export as the control case
XML = open(os.path.join(HERE, "fixtures", "turning_943580900.omtdx"), encoding="utf-8").read()
tt = T("943580900", "Semi & Finish Inner Tube ID", xml=XML)
rough = T("956770900", "Rough OD", xml=XML.replace('"topLeft"', '"bottomLeft"', 1).replace('value="55"', 'value="80"'))
groove = T("926480900", "Groove", xml=XML.replace('type="rhombic"', 'type="grooving"', 1))
spec = importlib.util.spec_from_file_location("tlm3", SCRIPT)
m3 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m3)
d = m3.tool_data(tt)
check(d["turning"] and d["stype"] == 510 and d["id"] == "943580900", "turning tool found from the turning cutting profile; 55 deg rhombic -> 510")
check(abs(d["l1"] + 1.3826) < 1e-4 and abs(d["l2"] - 7.8585) < 1e-4 and d["l_from"] == "tool",
      "L1 = setting length Z -1.3826 (radial), L2 = setting length X 7.8585 (axial); NC tool zeros skipped")
check(d["hm_pos"] == ["topLeft", "bottomLeft"] and d["tip"] == 2 and d["cut"] == 3, "first cutting point topLeft -> tip 2, cut 3 preset")
check(m3.tool_data(rough)["stype"] == 500 and m3.tool_data(rough)["tip"] == 3 and m3.tool_data(rough)["cut"] == 3,
      "80 deg rhombic -> 500 roughing; bottomLeft -> tip 3, cut 3")
gd = m3.tool_data(groove)
check(gd["stype"] == 520 and gd["cut"] is None, "grooving insert -> 520, no cut direction")
gtxt, _ = m3.program([gd], {gd["id"]: (1, 0)}, "doc", "test")
check("$TC_DP2[R999,1]=2" in gtxt and "$TC_DP11" not in gtxt, "grooving tool: tip direction written, no DP11")
# the four cases from the control: (tip, cut) 2+up, 3+left, 2+left OK; 1+down = warning triangle; 4+down OK
check([m3.cut_ok(a, b) for a, b in ((2, 2), (3, 3), (2, 3), (1, 1), (4, 1))] == [True, True, True, False, True],
      "allowed pairs: 2 up, 3 left, 2 left, 4 down; 1 down refused")
check([m3.cut_preset(i) for i in (1, 2, 3, 4)] == [2, 3, 3, 1], "cut preset per tip: 1 up, 2 left, 3 left, 4 down")
check(not m3.tool_data(em)["turning"] and m3.tool_data(em)["stype"] == 120, "end mill is not a turning tool")
check([m3.tip_of(x) for x in ("topRight", "topLeft", "bottomLeft", "bottomRight", "right", "top", "left", "bottom", "center", "?")]
      == [1, 2, 3, 4, 5, 6, 7, 8, 9, None], "hyperMILL cutting point -> tip direction table")

# whole run with a turning tool: screen 3 asks tip / cut; 1 (down) with tip 2 is refused and asked again; then 2 (up)
cs2 = [om.CompoundJob("B_040", [om.Job("6: Turn", tt), om.Job("7: Contour", em)])]
om._App.CurrentDocument = om.Document(DOC, om.Model([om.JobList("Op20", cs2)]))
if os.path.exists(MPF):
    os.remove(MPF)


def turn_screen(dlg):
    d = dlg.defaults()
    check(d.get("943580900  tip direction (hyperMILL topLeft)") == "2" and d.get("943580900  cut direction") == "3 \u2190",
          "screen 3 preset: tip 2, cut 3 (left arrow)")
    check(not any(k.startswith("M_10047210") for k in d), "screen 3 lists turning tools only")
    check("1 \u2191\u2192  2 \u2191\u2190  3 \u2193\u2190  4 \u2193\u2192" in dlg.title, "screen 3 title lists the allowed arrows")
    d["943580900  cut direction"] = "1 \u2193"
    return True, d


def turn_again(dlg):
    d = dlg.defaults()
    check("tip 2 takes cut 2 \u2191 or 3 \u2190" in gui.BOXES[-1], "bad pair: message names the allowed arrows")
    check(d.get("943580900  cut direction") == "1 \u2193", "same screen again, entry kept")
    d["943580900  cut direction"] = "2 \u2191"
    return True, d


m, left = run([lambda dlg: (True, {"Tools from": 0}), counts(M_10047210=("1", ""), **{"943580900": ("1", "")}), turn_screen, turn_again])
txt = open(MPF).read()
blk = txt[txt.index('R999=GETT("943580900",1)'):]
blk = blk[:blk.index("ENDIF")]
check(left == 0 and "$TC_DP1[R999,1]=510" in blk and "$TC_DP2[R999,1]=2" in blk and "$TC_DP3[R999,1]=-1.3826" in blk
      and "$TC_DP4[R999,1]=7.8585" in blk and "$TC_DP11[R999,1]=2" in blk, "turning tool: DP1 510, DP2 2, DP3 -1.3826, DP4 7.8585, DP11 2")
check("$TC_TPC5[R999]=7.6710" in blk and "$TC_TPC4[R999]=4.0000" in blk, "turning tool: HL = gage length, HD = minimum")
mill = txt[txt.index('R999=GETT("M_10047210",1)'):]
mill = mill[:mill.index("ENDIF")]
check("$TC_DP2" not in mill and "$TC_DP4" not in mill and "$TC_DP11" not in mill and "$TC_DP3[R999,1]=3.6614" in mill,
      "milling tool unchanged: DP3 = gage length only")
check("; turning tools: L1 = setting length Z (radial)" in txt, "header names the turning lengths")
check(json.load(open(os.path.join(tmp, "tool_load_mda_turning.json"))).get("943580900") == [2, 2], "tip / cut remembered per tool ID")

# next run offers the remembered cut direction; cancel on screen 3 = nothing written
os.remove(MPF)


def turn_cancel(dlg):
    check(dlg.defaults().get("943580900  cut direction") == "2 \u2191", "second run: remembered cut direction 2 (up) offered")
    return False, {}


m, left = run([lambda dlg: (True, {"Tools from": 0}), lambda dlg: (True, dlg.defaults()), turn_cancel])
check(not os.path.exists(MPF), "cancel on the turning screen: no program")

# 0 sisters on the turning tool: no turning screen
m, left = run([lambda dlg: (True, {"Tools from": 0}), counts(**{"943580900": ("0", "")})])
check(left == 0 and os.path.exists(MPF) and "943580900" not in open(MPF).read().split("\n", 4)[-1], "turning tool with 0 sisters: no screen 3, left out")

shutil.rmtree(tmp, ignore_errors=True)
print()
print("FAILURES: %d" % len(fails) if fails else "ALL TOOL LOAD MDA CHECKS PASSED")
sys.exit(1 if fails else 0)
