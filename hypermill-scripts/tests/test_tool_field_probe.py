#!/usr/bin/env python3
"""Headless test of tool_field_probe.py (fake om in tests/fake_om). Run: python3 tests/test_tool_field_probe.py"""
import os
import sys
import tempfile
import importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(HERE, "fake_om"))
import om                      # noqa: E402  (fake)
import om.cad.gui as gui       # noqa: E402  (fake)

SCRIPT = os.path.join(ROOT, "copy_to_python_folder", "tool_field_probe", "tool_field_probe.py")
tmp = tempfile.mkdtemp(prefix="tfp_")
tempfile.tempdir = tmp
LOG = os.path.join(tmp, "tool_field_probe_log.txt")
fails = []


def check(cond, label):
    print(("ok   " if cond else "FAIL ") + label)
    if not cond:
        fails.append(label)


XML = ('<root><container><tools><tool type="endMill" name="HA3R6RA0750"><param name="comment" value="Kennametal HARVI"/>'
       '<param name="orderingCode" value="7077716"/><param name="manufacturer" value="Kennametal"/>'
       '<tecsets><tecset/><tecset/><tecset/><tecset/><tecset/></tecsets></tool></tools>'
       '<holders><holder name="Holder"><param name="comment" value="HSK100 SHR"/></holder></holders>'
       '<ncTools><ncTool ncNumber="11075010" id="M_11075010" name="M_11075010"><param name="comment" value="x"/></ncTool></ncTools>'
       '</container></root>')


class PTool(om.Tool):
    """Tool with a settable Comment and a Number hyperMILL refuses to change."""
    def __init__(self, tid, name, xml=None):
        om.Tool.__init__(self, tid, name, xml=xml)
        self._c = "note"

    @property
    def Comment(self):
        return self._c

    @Comment.setter
    def Comment(self, v):
        self._c = v

    def __setattr__(self, k, v):
        if k == "Number" and hasattr(self, "Number"):
            raise RuntimeError("read-only")
        object.__setattr__(self, k, v)


class SJob(om.Job):
    def SetToolByUUID(self, u):
        self._tool = next(t for t in TOOLS if t.UUID == u)
        return True


class TS(om.ToolSet):
    def Rename(self, uuid, name):
        for t in TOOLS:
            if t.UUID == uuid:
                t.Name = name
        return True


t1 = PTool("11075010", "HA3R6RA0750", xml=XML)
t2 = PTool("50016510", "DRILL 4.2")
TOOLS = [t1, t2]
jobs = [SJob("1: Rough", t1), SJob("2: Drill", t2)]
model = om.Model([om.JobList("Op10", [om.CompoundJob("B_X_010_HF5", jobs)])])
model.ToolSet = TS(model)
om._App.CurrentDocument = om.Document(os.path.join(tmp, "doc.hmc"), model)


def run(writes, second=0):
    gui.SCRIPT[:] = [lambda d: (True, {"Tool": 0, "Second tool": second, "Try writes (scratch copy only)": writes})]
    gui.BOXES.clear()
    spec = importlib.util.spec_from_file_location("tfp_under_test", SCRIPT)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    m.run()
    with open(LOG, encoding="utf-8") as f:
        return f.read()


lg = run(False)
check("=== 1. PYTHON ===" in lg and "import openpyxl" in lg, "python facts logged")
check("--- ToolSet" in lg and "def  Rename" in lg, "ToolSet members logged")
check("prop Comment" in lg and "reading Comment" in lg, "tool members logged, each read first")
check("orderingCode = '7077716'" in lg, "export: ordering code param found")
check("holder {'name': 'Holder'}" in lg, "export: holder block logged")
check("repeated blocks (first 3 logged): tecset x5" in lg, "export: repeated blocks capped")
check(os.path.exists(os.path.join(tmp, "tool_field_probe_export.xml")), "export copy saved next to the log")
import re  # noqa: E402
check("jobs using it: 1" in lg and re.search(r"Job\.SetToolByUUID +there", lg) and re.search(r"Job\.SetTool +not there", lg),
      "job tool methods listed")
check("=== 7. TRY WRITES" not in lg and t1.Comment == "note", "read only: nothing written")
check(gui.BOXES and gui.BOXES[0].startswith("Done."), "message: done")

lg = run(True, second=2)
check("field Comment:" in lg and "reads back 'note_P' -> CHANGES" in lg and t1.Comment == "note", "Comment: changes, put back")
check("field Number:" in lg and "write refused: read-only" in lg, "Number: refused logged")
check("ToolSet.Rename(uuid, name_P)" in lg and t1.Name == "HA3R6RA0750", "Rename tried and put back")
check("SetToolByUUID(second)" in lg and "SWAPS" in lg and jobs[0].GetTool() is t1, "job swap tried and put back")
check("SetTool: not there" in lg, "missing SetTool logged")

print("\n%d failed" % len(fails) if fails else "\nALL TOOL FIELD PROBE CHECKS PASSED")
sys.exit(1 if fails else 0)
