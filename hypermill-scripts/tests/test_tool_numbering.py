#!/usr/bin/env python3
"""Headless test of tool_numbering.py (fake om in tests/fake_om). Run: python3 tests/test_tool_numbering.py"""
import os
import sys
import tempfile
import importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(HERE, "fake_om"))
import om                      # noqa: E402  (fake)
import om.cad.gui as gui       # noqa: E402  (fake)

SCRIPT = os.path.join(ROOT, "copy_to_python_folder", "tool_numbering", "tool_numbering.py")
tmp = tempfile.mkdtemp(prefix="tnum_")
tempfile.tempdir = tmp
fails = []


def check(cond, label):
    print(("ok   " if cond else "FAIL ") + label)
    if not cond:
        fails.append(label)


def xml(tid, name, ttype, dia, cr=None, cone=None, comment=""):
    extra = "".join('<param name="%s" value="%s"/>' % kv for kv in (("cornerRadius", cr), ("coneAngle", cone)) if kv[1] is not None)
    return ('<root><container><tools><tool type="%s" name="%s"><param name="lengthOfUnit" value="inch"/>'
            '<param name="toolDiameter" value="%s"/><param name="comment" value="%s"/>%s</tool></tools>'
            '<ncTools><ncTool ncNumber="1" id="%s" name="%s"><param name="lengthOfUnit" value="inch"/>'
            '<param name="gageLength" value="5"/></ncTool></ncTools></container></root>' % (ttype, name, dia, comment, extra, tid, name))


def T(tid, name, ttype, dia, **kw):
    return om.Tool(tid, name, xml=xml(tid, name, ttype, dia, **kw))


TURN = open(os.path.join(HERE, "fixtures", "turning_943580900.omtdx"), encoding="utf-8").read()


def build():
    tools = [T("M_11050010", ".500 BR", "radiusMill", 0.5, cr=0.03),          # follows: kept
             T("337580600", "3/8 ball", "ballMill", 0.375),                    # 9-digit -> M_12037510
             T("905080900", "2 in hi-feed", "radiusMill", 2.0, cr=0.06),       # big radius mill: asked
             T("M_10050010", "flat", "radiusMill", 0.75, cr=0),                # old M_ type 10, wrong diameter -> M_10075010
             T("416580600", "4.2mm drill", "drilTool", 0.1654, cone=140),      # -> M_50016510
             T("TAP1", "1/4-20 tap", "tapTool", 0.25),                         # asked: cut / form
             T("123", "second .500 bullnose", "radiusMill", 0.5, cr=0.03),     # same type and size as the first: variant 2
             om.Tool("943580900", "Semi & Finish Inner Tube ID", xml=TURN)]    # turning: asked
    jobs = [om.Job("%d: job" % k, t) for k, t in enumerate(tools)]
    model = om.Model([om.JobList("Op10", [om.CompoundJob("B_X_010_HF5", jobs)])])
    om._App.CurrentDocument = om.Document(os.path.join(tmp, "doc.hmc"), model)
    return tools


def answer_screen1(std=0, src=None, apply=False):
    def f(dlg):
        d = dlg.defaults()
        d["Standard"] = std
        if src is not None:
            d["Tools from"] = src
        d["Apply (unticked = list only)"] = apply
        return True, d
    return f


def answer_asked(dlg):
    d = dlg.defaults()
    for k in list(d):
        if k.startswith("905080900") and k.endswith("type"):
            d[k] = "42 Hi-feed mill"
        if k.startswith("TAP1") and k.endswith("type"):
            d[k] = "71 Form tap"
        if k.startswith("943580900") and k.endswith("turning type"):
            d[k] = "21 Boring finish"
        if k.startswith("943580900") and k.endswith("hand"):
            d[k] = "L"
    return True, d


def run(answers, method=None):
    gui.SCRIPT[:] = answers
    gui.BOXES.clear(); gui.SHOWN.clear(); gui.OUTPUT.clear()
    spec = importlib.util.spec_from_file_location("tnum_under_test", SCRIPT)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    if method is not None:
        m.APPLY_METHOD = method
    m.run()
    left = len(gui.SCRIPT)
    gui.SCRIPT.clear()
    return m, left


tools = build()
m, left = run([answer_screen1(), answer_asked])
rep = "\n".join(gui.OUTPUT)
asked = [f[1] for f in gui.SHOWN[1][1]]
check(left == 0 and any(a.startswith("905080900") for a in asked) and any(a.startswith("TAP1") for a in asked)
      and any(a.startswith("943580900") and "insert ISO" in a for a in asked) and not any(a.startswith("337580600") for a in asked),
      "asked: the 2 in radius mill, the tap, the turning tool; not the ball mill")
iso = [f for f in gui.SHOWN[1][1] if f[1].startswith("943580900") and "insert ISO" in f[1]][0][2]
check(iso == "DC", "turning insert ISO guessed from 'DCGT 11 T3 08': %r" % iso)


def new_of(old):
    for ln in rep.split("\n"):
        if ln.startswith(old + " "):
            return ln.split()[1]
    return None


check(new_of("M_11050010") == "(kept)", "M_11050010 follows and matches: kept")
check(new_of("337580600") == "M_12037510", "9-digit ball mill .375 -> M_12037510")
check(new_of("905080900") == "M_42200010", "big radius mill answered hi-feed -> M_42200010")
check(new_of("M_10050010") == "M_10075010", "old M_ type 10, diameter fixed -> M_10075010")
check(new_of("416580600") == "M_50016510", "4.2 mm drill, 140 deg point -> M_50016510")
check(new_of("TAP1") == "M_71025010", "tap answered form tap -> M_71025010")
check(new_of("123") == "M_11050020", "second .500 bullnose: variant 2 (variant 1 stays with M_11050010)")
check(new_of("943580900") == "T_21DCL10", "turning: T_21DCL10")
check("List only: nothing changed" in gui.BOXES[-1] and tools[1].ID == "337580600", "list only: nothing changed")
check("8 tools: 7 to renumber, 1 kept." in gui.BOXES[-1], "message counts")

# Apply before the probe: refused, nothing changed
tools = build()
m, left = run([answer_screen1(apply=True), answer_asked])
check("Apply is not set up yet" in gui.BOXES[-1] and tools[1].ID == "337580600", "Apply before APPLY_METHOD is set: says so, nothing changed")

# Apply with the fields method (what the probe should confirm)
tools = build()
m, left = run([answer_screen1(apply=True), answer_asked], method="fields")
check(tools[1].ID == "M_12037510" and tools[1].Number == 12037510 and tools[7].ID == "T_21DCL10" and tools[7].Number == 210403210,
      "Apply: ID and NC-Number written (T_ number %s)" % tools[7].Number)
check(tools[0].ID == "M_11050010" and "Post the B programs again" in gui.BOXES[-1], "kept tool untouched; message says to post again")

# Company X: not ready
build()
m, left = run([answer_screen1(std=1)])
check("rule is not set up yet" in gui.BOXES[-1], "Company X: rule not set yet")

print("\n%d failed" % len(fails) if fails else "\nALL TOOL NUMBERING CHECKS PASSED")
sys.exit(1 if fails else 0)
