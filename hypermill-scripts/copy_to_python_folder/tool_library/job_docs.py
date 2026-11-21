# job_docs.py - the job-end documents, filled from the tools of the posted B programs (tool_info.read dicts, in the order
# the tools are first used). Used by go_to_machine (Validation / Production).
#   setup_sheet()        NC master setup, Word: templates\NC_MASTER_SETUP.docx (built by docs\make_setup_template.py)
#   order_sheet()        what to buy, Excel: one line per cutter, holder and collet / extension, same order no. merged
#   sister_sheet()       sister tool sheet, Excel: templates\Sister_Tool_Sheet.xlsx, tools filled, Sisters / Tool Life
#                        left for you (validation), read back by read_sister_sheet() (production)
# Sisters = extra tools everywhere: QTY = 1 + sisters.
import os, re, datetime
import office_fill as of
import tool_info as ti

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATES = os.path.join(HERE, "templates")
SETUP_TPL = "NC_MASTER_SETUP.docx"
SISTER_TPL = "Sister_Tool_Sheet.xlsx"
SETUP_FONT_HALFPTS = 20          # 10 pt in the tool rows
SISTER_FIRST_ROW = 12            # first tool row of the sister sheet template (A = T No. ... J = Notes)
SISTER_LAST_TEMPLATE_ROW = 60    # the template's formulas reach this row; more tools get their own formulas


def inch(v, places=3):
    if v is None:
        return ""
    s = ("%." + str(places) + "f") % float(v)
    return s[1:] if s.startswith("0.") else s


def rad_angle(i):
    """RAD/ANGLE column: corner radius, point / chamfer / insert angle."""
    out = []
    if i.get("corner_r"):
        out.append("R" + inch(i["corner_r"], 3))
    if i.get("angle") and i.get("angle_kind") in ("point", "chamfer", "insert"):
        out.append("%g°" % round(float(i["angle"]), 1))
    return " / ".join(out)


def qty_of(i, counts):
    return 1 + int((counts or {}).get(i["id"], (0, 0))[0] or 0)


def life_of(i, counts):
    life = int((counts or {}).get(i["id"], (0, 0))[1] or 0)
    return str(life) if life else ""


# ---------------- NC master setup (Word) ----------------
def setup_sheet(path, infos, header, counts=None, template=None):
    """header keys: part, rev, mtl, material_type, part_name, date, programmer, machine, sim_date (blank = left blank).
    Returns path."""
    parts = of.read_zip(template or os.path.join(TEMPLATES, SETUP_TPL))
    band = {"MATERIAL TYPE:": header.get("material_type", ""), "MACHINE:": header.get("machine", "")}
    for n in [n for n in parts if re.match(r"word/header\d*\.xml$", n)]:
        s, _ = of.fill_labels(of.get(parts, n), band)
        of.put(parts, n, s)
    doc = of.get(parts, "word/document.xml")
    doc, _ = of.fill_labels(doc, {
        "P/N:": header.get("part", ""), "REV:": header.get("rev", ""), "MTL:": header.get("mtl", ""),
        "PART NAME:": header.get("part_name", ""), "DATE:": header.get("date", ""),
        "PROGRAMMER:": header.get("programmer", ""), "HYPERMILL SIM DATE:": header.get("sim_date", "")})
    rows = []
    for i in infos:
        turning = i.get("turning")
        rows.append([i.get("id", ""), ti.description(i), "" if turning else inch(i.get("dia")), rad_angle(i),
                     "" if turning else inch(i.get("flute_len"), 2), inch(i.get("reach")), str(qty_of(i, counts)),
                     life_of(i, counts), ti.assembly(i)])
    doc = of.fill_table(doc, 1, rows, rpr=of.row_rpr(doc, 1, 0, size_halfpts=SETUP_FONT_HALFPTS))
    of.put(parts, "word/document.xml", doc)
    of.write_zip(parts, path)
    return path


# ---------------- order sheet (Excel) ----------------
ORDER_HEAD = ["Item", "Manufacturer", "Order #", "Description", "Catalog no. / grade", "Qty", "For tool", "Check"]
ORDER_WIDTHS = [10, 16, 22, 44, 44, 6, 26, 34]


def order_lines(infos, counts=None):
    """[(item, manufacturer, order no., description, catalog, qty, tools, check)] cutters, then holders, then collets /
    extensions. Same item and order no. = one line, quantities added."""
    lines, index = [], {}

    def add(item, mfr, order, desc, cat, qty, tid, check):
        key = (item, order.strip().upper()) if order.strip() else (item, "#" + tid + desc)
        if key in index:
            ln = index[key]
            ln[5] += qty
            if tid not in ln[6]:
                ln[6].append(tid)
            if check and check not in ln[7]:
                ln[7].append(check)
            return
        ln = [item, mfr, order, desc, cat, qty, [tid], [check] if check else []]
        index[key] = ln
        lines.append(ln)

    for i in infos:
        q = qty_of(i, counts)
        chk = ""
        if not i.get("order_code"):
            chk = "no order no."
        elif i.get("order_from") == "Tool name":
            chk = "order no. is the tool name: check"
        add("Cutter", i.get("manufacturer", ""), i.get("order_code", ""), i.get("tool_name", ""), i.get("tool_comment", ""),
            q, i.get("id", ""), chk)
    for i in infos:
        q = qty_of(i, counts)
        for h in i.get("holders", []):
            nm = (h.get("name") or "").strip()
            chk = "holder name is not an order no.: check" if nm.lower() in ("", "holder", "toolholder") else ""
            add("Holder", "", nm, h.get("comment", ""), "", q, i.get("id", ""), chk)
    for i in infos:
        q = qty_of(i, counts)
        for e in i.get("extensions", []):
            nm = (e.get("name") or "").strip()
            chk = "extension name is not an order no.: check" if nm.lower() in ("", "extension") else ""
            add("Collet / ext.", "", nm, e.get("comment", ""), "", q, i.get("id", ""), chk)
    return [(a, b, c, d, e, f, ", ".join(g), "; ".join(h)) for a, b, c, d, e, f, g, h in lines]


def order_sheet(path, infos, counts=None, title=""):
    lines = order_lines(infos, counts)
    marked = {k for k, ln in enumerate(lines) if ln[7]}
    note = "Qty = tools to buy (1 + sisters per tool). Yellow = check the order no. before ordering."
    of.new_xlsx(path, "Order", ORDER_HEAD, [list(ln) for ln in lines], ORDER_WIDTHS, marked,
                title_rows=[t for t in (title, note) if t])
    return path, len(lines), len(marked)


# ---------------- sister tool sheet (Excel) ----------------
def sister_sheet(path, infos, header, counts=None, template=None):
    """header keys: job, part, program, machine, programmer, date. counts (optional) pre-fills Sisters / Tool Life.
    Returns path."""
    parts = of.read_zip(template or os.path.join(TEMPLATES, SISTER_TPL))
    sh = of.get(parts, "xl/worksheets/sheet1.xml")
    for r, k in zip(range(3, 9), ("job", "part", "program", "machine", "programmer", "date")):
        if header.get(k):
            sh = of.xlsx_set(sh, "B%d" % r, str(header[k]))
    styles = of.row_styles(sh, SISTER_LAST_TEMPLATE_ROW)
    for n, i in enumerate(infos):
        r = SISTER_FIRST_ROW + n
        if r > SISTER_LAST_TEMPLATE_ROW:                    # beyond the template: empty cells styled like its last row
            for col in "ABCDEGIJ":
                sh = of.xlsx_set(sh, "%s%d" % (col, r), None, styles.get(col))
        sh = of.xlsx_set(sh, "A%d" % r, i.get("id", ""))
        sh = of.xlsx_set(sh, "B%d" % r, i.get("order_code", ""))
        sh = of.xlsx_set(sh, "C%d" % r, ti.description(i))
        if i.get("dia") is not None and not i.get("turning"):
            sh = of.xlsx_set(sh, "D%d" % r, round(float(i["dia"]), 4))
        if i.get("gage") is not None:
            sh = of.xlsx_set(sh, "E%d" % r, round(float(i["gage"]), 4))
        if counts and i.get("id") in counts:
            s, life = counts[i["id"]]
            sh = of.xlsx_set(sh, "G%d" % r, int(s))
            if life:
                sh = of.xlsx_set(sh, "I%d" % r, int(life))
        notes = [m for m in i.get("missing", []) if m in ("order no.", "diameter")]
        if i.get("order_from") == "Tool name":
            notes.append("EDP = tool name: check")
        if notes:
            sh = of.xlsx_set(sh, "J%d" % r, "; ".join(notes))
        if r > SISTER_LAST_TEMPLATE_ROW:                    # beyond the template's formulas: write them
            sh = of.xlsx_formula(sh, "F%d" % r, 'IF(D%d="","",IF(D%d<4,4,D%d))' % (r, r, r), styles.get("F"))
            sh = of.xlsx_formula(sh, "H%d" % r, 'IF(AND(A%d="",B%d=""),"",1+N(G%d))' % (r, r, r), styles.get("H"))
    last = SISTER_FIRST_ROW + max(len(infos), 1) - 1
    if last > SISTER_LAST_TEMPLATE_ROW:
        sh = sh.replace("SUM(G12:G60)", "SUM(G12:G%d)" % last).replace("SUM(H12:H60)", "SUM(H12:H%d)" % last)
        sh = sh.replace("COUNTIF(B12:B60,", "COUNTIF(B12:B%d," % last)
        sh = re.sub(r'<dimension ref="A1:J\d+"/>', '<dimension ref="A1:J%d"/>' % last, sh)
    of.put(parts, "xl/worksheets/sheet1.xml", sh)
    of.put(parts, "xl/workbook.xml", of.recalc_on_open(of.get(parts, "xl/workbook.xml")))
    if "xl/calcChain.xml" in parts:                          # Excel rebuilds it; a stale one is reported as damaged
        parts = drop_calc_chain(parts)
    of.write_zip(parts, path)
    return path


def drop_calc_chain(parts):
    parts = dict(parts)
    parts.pop("xl/calcChain.xml", None)
    ct = of.get(parts, "[Content_Types].xml")
    of.put(parts, "[Content_Types].xml", re.sub(r'<Override PartName="/xl/calcChain.xml"[^>]*/>', "", ct))
    rel = of.get(parts, "xl/_rels/workbook.xml.rels")
    of.put(parts, "xl/_rels/workbook.xml.rels", re.sub(r'<Relationship [^>]*Target="calcChain.xml"[^>]*/>', "", rel))
    return parts


def read_sister_sheet(path):
    """({tool id: (sisters, life)}, problems) from a filled sister sheet. Blank = 0; a value that is not a whole number
    >= 0 is listed in problems and read as 0."""
    v = of.xlsx_values(path)
    out, problems = {}, []
    r = SISTER_FIRST_ROW
    blank_run = 0
    while blank_run < 5 and r < 2000:
        tid = str(v.get("A%d" % r, "") or "").strip()
        if not tid:
            blank_run += 1; r += 1; continue
        blank_run = 0

        def whole(ref, what):
            x = v.get(ref, "")
            if x in ("", None):
                return 0
            try:
                f = float(x)
                if f >= 0 and abs(f - round(f)) < 1e-9:
                    return int(round(f))
            except (TypeError, ValueError):
                pass
            problems.append("%s row %d: %s %r is not a whole number (read as 0)" % (tid, r, what, x))
            return 0
        out[tid] = (whole("G%d" % r, "sisters"), whole("I%d" % r, "tool life"))
        r += 1
    return out, problems


def today():
    return datetime.date.today().strftime("%Y-%m-%d")
