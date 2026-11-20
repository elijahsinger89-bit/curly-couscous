#!/usr/bin/env python3
"""office_fill.py (Word / Excel templates) and tool_info.py (tool reader). Run: python3 tests/test_office_fill.py [outdir]
Checks the files with python-docx / openpyxl and renders them with LibreOffice when present."""
import os
import sys
import shutil
import tempfile
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
LIB = os.path.join(os.path.dirname(HERE), "copy_to_python_folder", "tool_library")
sys.path.insert(0, LIB)
import office_fill as of   # noqa: E402
import tool_info as ti     # noqa: E402
OUT = sys.argv[1] if len(sys.argv) > 1 else tempfile.mkdtemp(prefix="of_")
os.makedirs(OUT, exist_ok=True)
fails = []


def check(cond, label):
    print(("ok   " if cond else "FAIL ") + label)
    if not cond:
        fails.append(label)


# ---- Word: labels in the header and the NC SETUP block, tool rows
parts = of.read_zip(os.path.join(LIB, "templates", "NC_MASTER_SETUP.docx"))
hdr = [n for n in parts if n.startswith("word/header")]
for n in hdr:
    s, done = of.fill_labels(of.get(parts, n), {"MATERIAL TYPE:": "S - Nickel Based", "MACHINE:": "HF5500"})
    of.put(parts, n, s)
doc, done = of.fill_labels(of.get(parts, "word/document.xml"),
                           {"P/N:": "00948602-025", "MTL:": "Inconel 718", "DATE:": "2026-11-21", "PROGRAMMER:": "ES",
                            "HYPERMILL SIM DATE:": "2026-11-18", "VERICUT DATE:": "", "REV:": ""})
check(done["P/N:"] == 1 and done["HYPERMILL SIM DATE:"] == 1 and done["DATE:"] == 1 and done["VERICUT DATE:"] == 0,
      "labels filled once each; DATE: not confused with VERICUT DATE:; blank values left alone %s" % done)
rows = [["M_11075010", ".750 BR R.03 6FL L1.50", ".750", "R.03", "1.50", "2.250", "2", "120", "HSK100 SHR .750 | ER32 1/2"]]
rows += [["M_%02d0%03d10" % (50, 100 + k), "DRILL %d" % k, ".%03d" % (100 + k), "140", ".800", "1.900", "1", "", ""] for k in range(62)]
doc = of.fill_table(doc, 1, rows, rpr=of.row_rpr(doc, 1, 0, size_halfpts=18))
rr = of.row_rpr(doc, 1, 0, size_halfpts=18)
check("<w:b/>" not in rr and "w:spacing" not in rr and 'w:sz w:val="18"' in rr and "Times" not in rr,
      "row font from the header row (style font), not bold, 9 pt: %s" % rr)
of.put(parts, "word/document.xml", doc)
out_doc = os.path.join(OUT, "setup_filled.docx")
of.write_zip(parts, out_doc)
try:
    import docx
    d = docx.Document(out_doc)
    t0, t1 = d.tables[0], d.tables[1]
    check(t0.rows[0].cells[1].text.strip() == "P/N: 00948602-025" and "2026-11-18" in t0.rows[0].cells[-1].text,
          "python-docx reads P/N and the sim date: %r" % t0.rows[0].cells[-1].text)
    check(len(t1.rows) == 1 + 63 + 2 and t1.rows[1].cells[0].text == "M_11075010" and t1.rows[63].cells[1].text == "DRILL 61"
          and t1.rows[64].cells[0].text == "", "63 tool rows (template had 58: rows added) + 2 blank rows")
    hd = " ".join(p.text for s in d.sections for p in s.header.paragraphs)
except ImportError:
    print("     (python-docx not installed: Word file not reopened)")
w = os.path.join(OUT, "setup_filled.pdf")
if shutil.which("soffice"):
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", OUT, out_doc], capture_output=True, timeout=180)
    check(os.path.exists(w) and os.path.getsize(w) > 10000, "LibreOffice opens and prints the filled setup sheet")
    if shutil.which("pdftotext"):
        txt = subprocess.run(["pdftotext", "-layout", w, "-"], capture_output=True, text=True).stdout
        check("MATERIAL TYPE: S - Nickel Based" in txt and "HF5500" in txt and "TOOL LIST" in txt and "MILLING" not in txt,
              "page header: TOOL LIST, material and machine filled")
        check("PROPRIETARY" in txt and "M_11075010" in txt and "HSK100 SHR .750" in txt, "footer notice and the first tool row printed")

# ---- Excel: fill the sister sheet template, read it back
xp = of.read_zip(os.path.join(LIB, "templates", "Sister_Tool_Sheet.xlsx"))
sh = of.get(xp, "xl/worksheets/sheet1.xml")
sh = of.xlsx_set(sh, "B3", "00948602-025 OP200")
sh = of.xlsx_set(sh, "A12", "M_11075010"); sh = of.xlsx_set(sh, "B12", "7077716"); sh = of.xlsx_set(sh, "D12", 0.75)
sh = of.xlsx_set(sh, "E12", 6.25); sh = of.xlsx_set(sh, "G12", 2); sh = of.xlsx_set(sh, "I12", 120)
sh = of.xlsx_set(sh, "F12", 999)                       # formula cell: left alone
sh = of.xlsx_set(sh, "K70", "new cell, new row")       # cell and row that do not exist yet
of.put(xp, "xl/worksheets/sheet1.xml", sh)
of.put(xp, "xl/workbook.xml", of.recalc_on_open(of.get(xp, "xl/workbook.xml")))
out_x = os.path.join(OUT, "sister_filled.xlsx")
of.write_zip(xp, out_x)
v = of.xlsx_values(out_x)
check(v.get("A12") == "M_11075010" and v.get("G12") == 2.0 and v.get("I12") == 120.0 and v.get("B3") == "00948602-025 OP200",
      "values read back (text and numbers)")
check(v.get("A11") == "T No." and v.get("K70") == "new cell, new row", "template labels (shared strings) and a new row read")
try:
    import openpyxl
    wb = openpyxl.load_workbook(out_x)
    ws = wb.active
    check(ws["F12"].value.startswith("=IF(") and ws["H12"].value.startswith("=IF(") and ws["B12"].value == "7077716",
          "openpyxl: formulas kept (F / H), values in place")
    check(wb.calculation.fullCalcOnLoad, "Excel recalculates when the file opens")
except ImportError:
    print("     (openpyxl not installed: Excel file not reopened)")

# ---- new workbook (order sheet)
p = of.new_xlsx(os.path.join(OUT, "order.xlsx"), "Order", ["Manufacturer", "Order #", "Qty"],
                [["Kennametal", "7077716", 3], ["Walter", "", 1]], widths=[16, 18, 6], marked={1}, title_rows=["ORDER SHEET - 00948602"])
v = of.xlsx_values(p)
check(v.get("A1") == "ORDER SHEET - 00948602" and v.get("A3") == "Manufacturer" and v.get("B4") == "7077716" and v.get("C4") == 3.0,
      "new workbook: title, header, rows")
try:
    import openpyxl
    ws = openpyxl.load_workbook(p).active
    check(ws.freeze_panes == "A4" and ws.auto_filter.ref == "A3:C5" and ws["A5"].fill.fgColor.rgb == "FFFFF2CC",
          "frozen header, autofilter, missing row highlighted")
except ImportError:
    pass

# ---- tool_info on real exports
class T:
    def __init__(self, src, **kw):
        self.src = src
        self.__dict__.update(kw)

    def Export(self, path):
        shutil.copy(self.src, path)
        return True


fx = os.path.join(HERE, "fixtures", "turning_943580900.omtdx")
i = ti.read(T(fx, ID="943580900", Number=943580900, Name="Semi & Finish Inner Tube ID", UUID="{A}"))
check(i["turning"] and i["id"] == "943580900" and abs(i["corner_r"] - 0.0312) < 1e-6 and i["angle"] == 55 and i["angle_kind"] == "insert",
      "turning tool: id, insert corner radius .0312, insert angle 55")
check(i["holders"] == [{"name": "T35", "comment": "DCGT 11 T3 08 - UM S205"}] and abs(i["gage"] - 7.671) < 0.001,
      "turning holder and gage length")
check(i["order_code"] == "DCGT 11 T3 08 - UM S205" or i["order_from"] in ("Tool comment", "Tool name"), "order no. fallback noted: %r from %s" % (i["order_code"], i["order_from"]))
check(ti.description(i) == "Semi & Finish Inner Tube ID", "description = Common Name")

em = os.path.join(LIB, "template_endmill.xml")
i = ti.read(T(em, ID="11100011", Number=11100011, Name="x", UUID="{B}"))
check(i["order_code"] == "3866068" and i["order_from"] == "Tool comment" and abs(i["dia"] - 1.0) < 1e-9 and abs(i["corner_r"] - 0.015) < 1e-9,
      "end mill: EDP from the old Tool comment, dia 1.000, corner radius .015")
check("description (Common > Name)" in i["missing"] and "holder" in i["missing"], "M_ Common Name and no holder listed as missing: %s" % i["missing"])
xd = os.path.join(LIB, "template_xdrill_ext.xml")
i = ti.read(T(xd, ID="2", Number=2, Name="Drill Tool_1", UUID="{C}"))
check(i["extensions"] and i["extensions"][0]["name"] == "Extension" and i["angle"] == 158 and i["angle_kind"] == "point",
      "drill with extension: extension listed, point angle 158")
check(ti.assembly({"holders": [{"name": "HSK100 SHR .750", "comment": ""}], "extensions": [{"name": "ER32 1/2", "comment": "collet"}]})
      == "HSK100 SHR .750 | ER32 1/2 (collet)", "assembly text: holder | extension")

print("\noutput in", OUT)
print("%d failed" % len(fails) if fails else "ALL OFFICE FILL AND TOOL INFO CHECKS PASSED")
sys.exit(1 if fails else 0)
