#!/usr/bin/env python3
"""job_docs.py: NC master setup, order sheet, sister sheet and reading it back. Run: python3 tests/test_job_docs.py [outdir]
Reopens the files with python-docx / openpyxl and prints the setup sheet with LibreOffice when present."""
import os
import sys
import shutil
import tempfile
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
LIB = os.path.join(os.path.dirname(HERE), "copy_to_python_folder", "tool_library")
sys.path.insert(0, LIB)
import job_docs as jd   # noqa: E402
OUT = sys.argv[1] if len(sys.argv) > 1 else tempfile.mkdtemp(prefix="jd_")
os.makedirs(OUT, exist_ok=True)
fails = []


def check(cond, label):
    print(("ok   " if cond else "FAIL ") + label)
    if not cond:
        fails.append(label)


def tool(tid, desc, **kw):
    i = {"id": tid, "nc_name": desc, "tool_name": kw.pop("name", desc), "tool_comment": kw.pop("comment", ""),
         "manufacturer": kw.pop("mfr", ""), "order_code": kw.pop("order", ""), "order_from": kw.pop("order_from", "Ordering code"),
         "dia": kw.pop("dia", None), "corner_r": kw.pop("r", None), "angle": kw.pop("angle", None),
         "angle_kind": kw.pop("akind", ""), "flute_len": kw.pop("loc", None), "reach": kw.pop("reach", None),
         "gage": kw.pop("gage", None), "turning": kw.pop("turning", False), "holders": kw.pop("holders", []),
         "extensions": kw.pop("ext", []), "nc_comment": "", "missing": kw.pop("missing", [])}
    assert not kw, kw
    return i


INFOS = [
    tool("M_11075010", ".750 BR R.03 6FL L1.50", name="Kennametal HARVI III 6FL radius .750", comment="HA3R6RA0750R150 | KCSM15A",
         mfr="Kennametal", order="7077716", dia=0.75, r=0.03, loc=1.5, reach=2.25, gage=6.188,
         holders=[{"name": "A63.140.19", "comment": "HSK100 SHR .750 x 140"}]),
    tool("M_11075020", ".750 BR R.06 6FL L1.50", name="Kennametal HARVI III .060R", mfr="Kennametal", order="7077716",
         dia=0.75, r=0.06, loc=1.5, reach=3.0, gage=6.9, holders=[{"name": "A63.140.19", "comment": "HSK100 SHR .750 x 140"}]),
    tool("M_50016510", ".165 DR L.80", name="DC170-05-04.200A1-WJ30EJ", mfr="Walter", order="DC170-05-04.200A1-WJ30EJ",
         dia=0.1654, angle=140, akind="point", loc=0.8, reach=1.9, gage=4.7,
         holders=[{"name": "Holder", "comment": ""}], ext=[{"name": "ER16 .165", "comment": "collet"}]),
    tool("943580900", "Semi & Finish Inner Tube ID", name="Semi & Finish Inner Tube ID", comment="DCGT 11 T3 08 - UM S205",
         order="Semi & Finish Inner Tube ID", order_from="Tool name", r=0.0312, angle=55, akind="insert", gage=7.671,
         turning=True, holders=[{"name": "T35", "comment": "DCGT 11 T3 08 - UM S205"}]),
    tool("M_10037510", ".375 EM", name="old hand-made tool", order="", order_from="", dia=0.375, missing=["order no."]),
]
COUNTS = {"M_11075010": (2, 120), "M_50016510": (1, 0)}
HEAD = {"part": "00948602-025", "material_type": "S - Nickel Based", "machine": "HF5500", "date": "2026-11-21",
        "programmer": "ES", "sim_date": "2026-11-18", "job": "00948602-025 OP200", "program": "A_P1"}

# ---- setup sheet
p = jd.setup_sheet(os.path.join(OUT, "SETUP.docx"), INFOS, HEAD, COUNTS)
import docx  # noqa: E402
t = docx.Document(p).tables[1]
r1 = [c.text.strip() for c in t.rows[1].cells]
check(r1 == ["M_11075010", ".750 BR R.03 6FL L1.50", ".750", "R.030", "1.50", "2.250", "3", "120", "A63.140.19 (HSK100 SHR .750 x 140)"],
      "setup row: no., description, dia, radius, flute, stick-out = reach, QTY = 1 + 2 sisters, life, holder: %s" % r1)
r3 = [c.text.strip() for c in t.rows[3].cells]
check(r3[3] == "140°" and r3[6] == "2" and r3[8] == "Holder | ER16 .165 (collet)", "drill: point angle, QTY 2, holder | collet: %s" % r3)
r4 = [c.text for c in t.rows[4].cells]
check(r4[2] == "" and r4[3] == "R.031 / 55°" and r4[4] == "" and r4[6] == "1", "turning tool: no dia / flute, nose radius / insert angle: %s" % r4)
check(len(t.rows) == 1 + 11, "short job: one page of rows (11)")
if shutil.which("soffice"):
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", OUT, p], capture_output=True, timeout=180)
    check(os.path.exists(os.path.join(OUT, "SETUP.pdf")), "setup sheet prints (LibreOffice)")

# ---- order sheet
lines = jd.order_lines(INFOS, COUNTS)
cut = [ln for ln in lines if ln[0] == "Cutter"]
check(cut[0][2] == "7077716" and cut[0][5] == 4 and cut[0][6] == "M_11075010, M_11075020",
      "same EDP on two tools = one line, qty 3 + 1 = 4, both T nos.")
hold = [ln for ln in lines if ln[0] == "Holder"]
check(hold[0][2] == "A63.140.19" and hold[0][5] == 4 and "not an order no." in [h for h in hold if h[2] == "Holder"][0][7],
      "holders merged by order no.; holder named 'Holder' flagged")
ext = [ln for ln in lines if ln[0] == "Collet / ext."]
check(ext == [("Collet / ext.", "", "ER16 .165", "collet", "", 2, "M_50016510", "")], "collet: own line, qty 1 + 1 sister")
check([ln for ln in cut if ln[6] == "943580900"][0][7] == "order no. is the tool name: check" and
      [ln for ln in cut if ln[6] == "M_10037510"][0][7] == "no order no.", "order no. from the tool name / missing: flagged")
p, n, marked = jd.order_sheet(os.path.join(OUT, "ORDER.xlsx"), INFOS, COUNTS, "TOOL ORDER - 00948602-025 - PRODUCTION - 2026-11-21")
import openpyxl  # noqa: E402
ws = openpyxl.load_workbook(p).active
check(ws["A1"].value.startswith("TOOL ORDER") and ws["A4"].value == "Item" and ws["C5"].value == "7077716" and ws["F5"].value == 4,
      "order workbook: title, header row 4, first line")
check(marked == 3 and ws.cell(row=5 + [k for k, ln in enumerate(lines) if ln[7]][0], column=1).fill.fgColor.rgb == "FFFFF2CC",
      "lines to check are yellow (%d)" % marked)

# ---- sister sheet: written, then filled in Excel (openpyxl stands in), read back
p = jd.sister_sheet(os.path.join(OUT, "SISTERS.xlsx"), INFOS, HEAD)
wb = openpyxl.load_workbook(p)
ws = wb.active
check(ws["B3"].value == "00948602-025 OP200" and ws["A12"].value == "M_11075010" and ws["B12"].value == "7077716"
      and ws["D12"].value == 0.75 and ws["E12"].value == 6.188 and ws["G12"].value is None, "sister sheet: header, tool rows; Sisters left blank")
check(ws["F12"].value.startswith("=IF(") and ws["J15"].value == "EDP = tool name: check" and ws["J16"].value == "order no.",
      "formulas kept; notes for tools to check")
ws["G12"] = 2; ws["I12"] = 120; ws["G14"] = 1; ws["I13"] = "lots"
filled = os.path.join(OUT, "SISTERS_filled.xlsx")
wb.save(filled)
got, problems = jd.read_sister_sheet(filled)
check(got["M_11075010"] == (2, 120) and got["M_50016510"] == (1, 0) and got["943580900"] == (0, 0) and len(got) == 5,
      "read back after Excel saved it (shared strings): sisters / life per tool")
check(problems and "M_11075020" in problems[0] and "lots" in problems[0], "a tool life that is not a number is listed")

# ---- more tools than the template has rows (49)
many = [dict(INFOS[0], id="M_500%02d010" % k, order="ED%d" % k) for k in range(55)]
p = jd.sister_sheet(os.path.join(OUT, "SISTERS_55.xlsx"), many, HEAD)
ws = openpyxl.load_workbook(p).active
check(ws["A66"].value == "M_50054010" and ws["F66"].value.startswith("=IF(D66") and ws["H66"].value.startswith("=IF(AND(A66")
      and ws["G66"].fill.fgColor.rgb == ws["G60"].fill.fgColor.rgb, "55 tools: rows past 60 get the formulas and the input colour")
check(ws["F4"].value == "=SUM(G12:G66)" and "B12:B66" in ws["F3"].value, "totals cover every row")
got, _ = jd.read_sister_sheet(p)
check(len(got) == 55, "all 55 read back")
p = jd.setup_sheet(os.path.join(OUT, "SETUP_55.docx"), many, HEAD)
check(len(docx.Document(p).tables[1].rows) == 1 + 57, "setup sheet: 55 rows + 2 blank")

print("\noutput in", OUT)
print("%d failed" % len(fails) if fails else "ALL JOB DOCS CHECKS PASSED")
sys.exit(1 if fails else 0)
