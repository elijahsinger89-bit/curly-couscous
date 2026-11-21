#!/usr/bin/env python3
"""tool_numbers.py and the builder's numbering. Run: python3 tests/test_tool_numbers.py"""
import os
import sys
import csv
import tempfile
import importlib
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
LIB = os.path.join(os.path.dirname(HERE), "copy_to_python_folder", "tool_library")
sys.path.insert(0, LIB)
import tool_numbers as tn   # noqa: E402
import tool_builder as tb   # noqa: E402
importlib.reload(tn); importlib.reload(tb)
fails = []


def check(cond, label):
    print(("ok   " if cond else "FAIL ") + label)
    if not cond:
        fails.append(label)


def raises(f):
    try:
        f()
    except ValueError:
        return True
    return False


# ---- ids
check(tn.mill_id(11, 0.5, 1, 0) == "M_11050010", "mill_id .500 bullnose = M_11050010")
check(tn.mill_id(10, 0.375) == "M_10037510" and tn.mill_id(40, 2.0) == "M_40200010", "diameter digits 0375, 2000")
check(raises(lambda: tn.mill_id(18, 0.5)) and raises(lambda: tn.mill_id(11, 12.0)) and raises(lambda: tn.mill_id(11, 0.5, 10)),
      "refuses a type not in the standard, a diameter over 9.999 in, variant 10")
check(tn.turn_id(10, "cn", "r") == "T_10CNR10", "turn_id = T_10CNR10")
p = tn.parse("M_11050011")
check(p == {"kind": "M", "type": 11, "dia_in": 0.5, "variant": 1, "copy": 1}, "parse M_")
check(tn.parse("T_21DNL20")["iso"] == "DN" and tn.parse("943580900") is None and tn.parse("M_18050010") is None, "parse T_, refuses 9-digit and unknown type")
check(tn.number_of("M_11050010") == 11050010 and tn.number_of("T_10CNR10") == 100314110, "NC numbers: M_ digits, T_ 9 digits")
check(tn.number_of("T_10CNR10") > 99999999 >= tn.number_of("M_99999999"), "T_ numbers never equal an M_ number")
check(tn.follows("M_11050010")[0] and not tn.follows("943580900")[0] and not tn.follows("m_11050010")[0], "follows HELLER")
check(tn.follows("M_11050010", "COMPANY_X") == (False, tn.NOT_READY), "Company X: rule not set yet")
check(tn.free_variant(lambda v: tn.mill_id(11, 0.5, v), ["M_11050010", "m_11050020"]) == "M_11050030", "free_variant skips used ones")

# ---- catalog codes -> standard
W = tn.workbook_code
check(W("facemill", 14) == 40 and W("facemill", 15) == 43 and W("facemill", 16) == 42 and W("facemill", 17) == 42, "face 40, shoulder 43, hi-feed / copy 42")
check(W("slot", 21, {"kind": "disc"}) == 46 and W("slot", 21, {"kind": "tslot"}) == 30, "slot 46, T-slot 30")
check(W("xdrill", 53) == 52 and W("boring", 52) == 61 and W("spotdrill", 51) == 53 and W("spotdrill", 54) == 54, "insert drill 52, boring 61, spot 53, centre 54")
check(W("tap", 60, {"form": "cutting"}) == 70 and W("tap", 60, {"form": "forming"}) == 71, "cut tap 70, form tap 71")
check(W("reamer", 61) == 60 and W("threadmill", 62) == 72, "reamer 60, thread mill 72")
check(W("endmill", 10) == 10 and W("endmill", 11) == 11 and W("endmill", 12) == 12 and W("chamfer", 18) == 13 and W("profilemill", 19) == 44,
      "end mills unchanged, chamfer 13, inserted ball 44")
check(W("endmill", 14, {"shape": "Corner rounding"}) == 34 and W("endmill", 14, {"shape": "Deburrer"}) == 92, "corner rounding 34, deburrer 92")

# ---- type of an existing tool
check(tn.type_from_hm("radiusMill", 0.5, 0) == (10, True) and tn.type_from_hm("radiusMill", 0.5, 0.03) == (11, True), "radius mill: flat 10, bullnose 11")
check(tn.type_from_hm("radiusMill", 2.0, 0.06) == (11, False), "big bullnose: asked (face / hi-feed built as bullnose)")
check(tn.type_from_hm("radiusMill", 0.5, 0.25)[0] == 12 and tn.type_from_hm("drilTool", 0.25, 0, 90) == (53, True), "ball 12, 90 deg drill = spot 53")
check(tn.type_from_hm("tapTool") == (70, False) and tn.type_from_hm("insertTtool")[1] is False, "tap asked (cut / form), unknown asked")

# ---- description
check(tn.describe(11, 0.75, 0.03, 6, 1.5) == ".750 BR R.03 6FL L1.50", "describe bullnose = .750 BR R.03 6FL L1.50")
check(tn.describe(11, 0.5, 0.015, 4, 1.0) == ".500 BR R.015 4FL L1.00", "corner radius .015 keeps 3 places")
check(tn.describe(70, 0.25, thread="1/4-20 UNC") == "TAP 1/4-20 UNC" and tn.describe(40, 2.0) == "2.000 FM", "tap and face mill")


# ---- builder: real catalog rows, built offline
class FakeTool:
    def __init__(self, p):
        r = ET.parse(p).getroot()
        n = r.find(".//ncTools/ncTool")
        self.Number, self.ID, self.NcName = int(n.get("ncNumber")), n.get("id"), n.get("name")
        self.Name = r.find(".//tools/tool").get("name")
        self.UUID = "{%s}" % self.ID
        self.path = p


class FakeTS:
    def __init__(self):
        self.tools = []

    def GetTools(self):
        return list(self.tools)

    def ImportTool(self, p):
        t = FakeTool(p)
        self.tools.append(t)
        return t

    def Rename(self, u, name):
        for t in self.tools:
            if t.UUID == u:
                t.Name = name


class FakeModel:
    def __init__(self):
        self.ToolSet = FakeTS()


def first(name, test):
    with open(os.path.join(LIB, name), encoding="utf-8-sig") as f:
        return next(r for r in csv.DictReader(f) if test(r))


tmp = tempfile.mkdtemp(prefix="tn_")
model, jt = FakeModel(), tb.JobTools()
cases = [
    ("endmill", first("kennametal_endmills.csv", lambda r: r["type_code"] == "11" and r.get("flutes")), 11, "11"),
    ("facemill", first("walter_facemills.csv", lambda r: True), 14, "40"),
    ("slot", first("walter_slot.csv", lambda r: r.get("kind") == "disc"), 21, "46"),
    ("spotdrill", first("walter_spotdrills.csv", lambda r: r["type_code"] == "51"), 51, "53"),
    ("xdrill", first("walter_xdrills.csv", lambda r: True), 53, "52"),
]
for kind, row, data_code, want in cases:
    t, msg = tb.get_or_create(model, kind, row, data_code, jt, outdir=tmp)
    ok = t is not None and str(t.Number).startswith(want) and t.ID == "M_%d" % t.Number
    check(ok, "%s %s -> M_%s... (%s)" % (kind, row["designation"], want, msg if t is None else t.ID))
em = model.ToolSet.tools[0]
check(em.NcName.startswith(tn.inch(float(cases[0][1]["dia_in"]))) and " BR " in em.NcName, "Common Name = description: %r" % em.NcName)
check(em.Name == cases[0][1]["designation"], "Tool name = catalog designation")

tb.ORDERING_PARAM = "orderingCode"
row = cases[0][1]
t, _ = tb.get_or_create(model, "endmill", row, 11, jt, outdir=tmp, force_new=True)
tool_el = ET.parse(t.path).getroot().find(".//tools/tool")
oc = tool_el.find("param[@name='orderingCode']")
check(oc is not None and oc.get("value") == tb.order_code(row) and t.Number != em.Number, "ordering code written once the field name is set; second copy gets the next variant")
tb.ORDERING_PARAM = ""

# variants 1-9 used -> refused, not rolled into the diameter digits
jt2, m2 = tb.JobTools(), FakeModel()
rows = [r for r in csv.DictReader(open(os.path.join(LIB, "kennametal_endmills.csv"), encoding="utf-8-sig"))
        if r["type_code"] == "10" and abs(float(r["dia_in"] or 0) - 0.5) < 1e-6][:11]
res = [tb.get_or_create(m2, "endmill", r, 10, jt2, outdir=tmp) for r in rows]
built = [t for t, _ in res if t is not None]
check(len(rows) >= 10 and len(built) == 9 and all(str(t.Number).startswith("100500") for t in built) and "no tool number" in res[9][1],
      "10th .500 flat end mill refused, numbers stay 100500v0 (%d built)" % len(built))

print("\n%d failed" % len(fails) if fails else "\nALL TOOL NUMBER CHECKS PASSED")
sys.exit(1 if fails else 0)
