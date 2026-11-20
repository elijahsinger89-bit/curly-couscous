# office_fill.py - fills Word (.docx) and Excel (.xlsx) templates with Python's standard library only (hyperMILL's Python
# has no python-docx / openpyxl). The XML is edited as text: Python's XML writer renames namespace prefixes, which Word
# reports as unreadable content. Styles, formulas, headers, footers and pictures of the template stay as they are.
import re, zipfile
from xml.sax.saxutils import escape


# ---------------- zip ----------------
def read_zip(path):
    """{part name: bytes} in the original order."""
    with zipfile.ZipFile(path) as z:
        return {n: z.read(n) for n in z.namelist()}


def write_zip(parts, path):
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for n, b in parts.items():
            z.writestr(n, b)


def get(parts, name):
    return parts[name].decode("utf-8")


def put(parts, name, s):
    parts[name] = s.encode("utf-8")


# ---------------- XML text helpers ----------------
def spans(s, tag, start=0, end=None):
    """Top-level <tag ...>...</tag> (and <tag/>) spans in s[start:end]; nested elements of the same tag stay inside."""
    end = len(s) if end is None else end
    op = re.compile(r"<%s(?=[\s>/])" % re.escape(tag))
    close = "</%s>" % tag
    out, i = [], start
    while True:
        m = op.search(s, i, end)
        if not m:
            return out
        a = m.start()
        gt = s.find(">", a)
        if s[gt - 1] == "/":
            out.append((a, gt + 1)); i = gt + 1; continue
        depth, j = 1, gt + 1
        while depth:
            m2 = op.search(s, j, end)
            c = s.find(close, j, end)
            if c < 0:
                raise ValueError("unbalanced <%s>" % tag)
            if m2 and m2.start() < c:
                g2 = s.find(">", m2.start())
                if s[g2 - 1] != "/":
                    depth += 1
                j = g2 + 1
            else:
                depth -= 1
                j = c + len(close)
        out.append((a, j))
        i = j


def innermost(s, tag="w:p", start=0, end=None):
    """Spans of <tag> elements that hold no <tag> inside (paragraphs inside text boxes included)."""
    out = []
    for a, b in spans(s, tag, start, end):
        gt = s.find(">", a) + 1
        inner = spans(s, tag, gt, b)
        if inner:
            out += innermost(s, tag, gt, b)
        else:
            out.append((a, b))
    return out


def plain(s):
    return re.sub(r"\s+", " ", "".join(re.findall(r"<w:t(?:\s[^>]*)?>([^<]*)</w:t>", s))).strip()


def _rpr(p, bold):
    """Run properties for new text in paragraph p: the last run's, else the paragraph mark's; bold on / off."""
    runs = spans(p, "w:r")
    src = ""
    for a, b in reversed(runs):
        m = re.search(r"<w:rPr>.*?</w:rPr>", p[a:b], re.S)
        if m:
            src = m.group(0); break
    if not src:
        m = re.search(r"<w:pPr>.*?(<w:rPr>.*?</w:rPr>).*?</w:pPr>", p, re.S)
        src = m.group(1) if m else "<w:rPr></w:rPr>"
    return plain_rpr(src, bold)


def plain_rpr(src, bold=False, size_halfpts=None):
    """Run properties without bold, letter spacing, scaling, kerning or raised / lowered text; bold / size when asked."""
    src = re.sub(r"<w:(?:b|bCs|spacing|w|kern|position)(?:\s[^>]*)?/>", "", src)
    src = re.sub(r"<w:(ins|del|rPrChange)\b.*?(?:/>|</w:\1>)", "", src, flags=re.S)
    if size_halfpts:
        src = re.sub(r"<w:szCs?(?:\s[^>]*)?/>", "", src)
        src = src.replace("</w:rPr>", '<w:sz w:val="%d"/><w:szCs w:val="%d"/></w:rPr>' % (size_halfpts, size_halfpts))
    if bold:
        src = src.replace("<w:rPr>", "<w:rPr><w:b/><w:bCs/>", 1)
    return src


def run(text, rpr="<w:rPr></w:rPr>"):
    return '<w:r>%s<w:t xml:space="preserve">%s</w:t></w:r>' % (rpr, escape(text))


def append_text(p, text, bold=False):
    """Paragraph p with a run holding text added at its end (formatting of the paragraph's last run, not bold)."""
    if p.endswith("/>") and not p.endswith("</w:p>"):
        p = p[:-2] + "></w:p>"
    k = p.rfind("</w:p>")
    return p[:k] + run(text, _rpr(p, bold)) + p[k:]


def fill_labels(s, values):
    """Every innermost paragraph whose text is a label ('P/N:', 'MACHINE:' ...) gets ' value' after it.
    values = {label: value}; labels compare upper case with spaces collapsed. Returns (xml, {label: times filled})."""
    want = {re.sub(r"\s+", " ", k).strip().upper(): (k, v) for k, v in values.items()}
    done = {k: 0 for k in values}
    edits = []
    for a, b in innermost(s):
        t = plain(s[a:b]).upper()
        if t in want and str(want[t][1] or "").strip():
            k, v = want[t]
            raw = "".join(re.findall(r"<w:t(?:\s[^>]*)?>([^<]*)</w:t>", s[a:b]))
            sep = "" if raw[-1:].isspace() else " "
            edits.append((a, b, append_text(s[a:b], sep + str(v).strip())))
            done[k] += 1
    for a, b, new in reversed(edits):
        s = s[:a] + new + s[b:]
    return s, done


def set_cell(tc, text, bold=False, rpr=None):
    """Table cell tc with text in its first paragraph (old text in that paragraph removed)."""
    ps = spans(tc, "w:p")
    if not ps:
        return tc
    a, b = ps[0]
    p = tc[a:b]
    keep_pr = re.search(r"<w:pPr>.*?</w:pPr>", p, re.S)
    r = rpr if rpr is not None else _rpr(p, bold)
    head = re.match(r"<w:p(?:\s[^>]*)?>", p).group(0) if not p.endswith("/>") else p[:-2] + ">"
    new = head + (keep_pr.group(0) if keep_pr else "") + (run(text, r) if text != "" else "") + "</w:p>"
    return tc[:a] + new + tc[b:]


def tables(s):
    return spans(s, "w:tbl")


def rows(tbl):
    return spans(tbl, "w:tr")


def cells(tr):
    return spans(tr, "w:tc")


def _no_ids(x):
    return re.sub(r'\sw14:(?:paraId|textId)="[^"]*"', "", x)


def row_rpr(s, index, row=0, size_halfpts=None):
    """Run properties of the first text in row of table index, without bold (the header row's font for the data rows)."""
    ta, tb = tables(s)[index]
    tbl = s[ta:tb]
    ra, rb = rows(tbl)[row]
    m = re.search(r"<w:r(?:\s[^>]*)?>\s*(<w:rPr>.*?</w:rPr>)\s*<w:t", tbl[ra:rb], re.S)
    return plain_rpr(m.group(1) if m else "<w:rPr></w:rPr>", False, size_halfpts)


def fill_table(s, index, data, prototype=1, blank=2, min_rows=11, rpr=None):
    """Table index of s: rows after the header replaced by one row per data row (list of cell texts), cloned from row
    prototype, then blank rows up to max(len(data) + blank, min_rows). rpr = run properties of the new text (default: the
    cell's own). Returns the new xml."""
    ta, tb = tables(s)[index]
    tbl = s[ta:tb]
    rs = rows(tbl)
    proto = _no_ids(tbl[rs[prototype][0]:rs[prototype][1]])
    out = []
    for values in data:
        tr = proto
        cs = cells(tr)
        for (a, b), v in reversed(list(zip(cs, values))):
            tr = tr[:a] + set_cell(tr[a:b], "" if v is None else str(v), rpr=rpr) + tr[b:]
        out.append(tr)
    empty = proto
    for a, b in reversed(cells(proto)):
        empty = empty[:a] + set_cell(empty[a:b], "") + empty[b:]
    while len(out) < max(len(data) + blank, min_rows):
        out.append(empty)
    first, last = rs[prototype][0], rs[-1][1]
    tbl = tbl[:first] + "".join(out) + tbl[last:]
    return s[:ta] + tbl + s[tb:]


def add_footer_note(s, text, size_halfpts=14):
    """Footer part s with a centred small paragraph of text at its end."""
    p = ('<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:before="0" w:after="0"/></w:pPr>%s</w:p>'
         % run(text, '<w:rPr><w:sz w:val="%d"/><w:szCs w:val="%d"/></w:rPr>' % (size_halfpts, size_halfpts)))
    k = s.rfind("</w:ftr>")
    return s[:k] + p + s[k:]


# ---------------- Excel ----------------
def col_row(ref):
    m = re.match(r"^([A-Z]+)(\d+)$", ref)
    return m.group(1), int(m.group(2))


def col_num(col):
    n = 0
    for ch in col:
        n = n * 26 + ord(ch) - 64
    return n


def col_name(n):
    s = ""
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def _cell_xml(ref, value, style):
    st = ' s="%s"' % style if style else ""
    if value is None or value == "":
        return '<c r="%s"%s/>' % (ref, st)
    if isinstance(value, bool):
        value = int(value)
    if isinstance(value, (int, float)):
        return '<c r="%s"%s><v>%s</v></c>' % (ref, st, repr(value) if isinstance(value, float) else value)
    return '<c r="%s"%s t="inlineStr"><is><t xml:space="preserve">%s</t></is></c>' % (ref, st, escape(str(value)))


def xlsx_set(sheet, ref, value, style=None):
    """Sheet xml with cell ref set to value (number or text), keeping the cell's style; the cell and its row are made when
    missing. A formula cell is left alone."""
    col, rn = col_row(ref)
    m = re.search(r'<c r="%s"(?=[\s/>])' % ref, sheet)
    if m:
        a = m.start()
        gt = sheet.find(">", a)
        b = gt + 1 if sheet[gt - 1] == "/" else sheet.find("</c>", gt) + 4
        old = sheet[a:b]
        if "<f" in old:
            return sheet
        sm = re.search(r'\ss="(\d+)"', old[:old.find(">") + 1])
        return sheet[:a] + _cell_xml(ref, value, style if style is not None else (sm.group(1) if sm else None)) + sheet[b:]
    new = _cell_xml(ref, value, style)
    rm = re.search(r'<row r="%d"(?=[\s>/])[^>]*?(/?)>' % rn, sheet)
    if rm:
        if rm.group(1) == "/":
            return sheet[:rm.start()] + rm.group(0)[:-2] + ">" + new + "</row>" + sheet[rm.end():]
        end = sheet.find("</row>", rm.end())
        row = sheet[rm.end():end]
        pos = len(row)
        for cm in re.finditer(r'<c r="([A-Z]+)\d+"', row):
            if col_num(cm.group(1)) > col_num(col):
                pos = cm.start(); break
        return sheet[:rm.end()] + row[:pos] + new + row[pos:] + sheet[end:]
    k = None
    for rm2 in re.finditer(r'<row r="(\d+)"', sheet):
        if int(rm2.group(1)) > rn:
            k = rm2.start(); break
    if k is None:
        k = sheet.find("</sheetData>")
    return sheet[:k] + '<row r="%d">%s</row>' % (rn, new) + sheet[k:]


def recalc_on_open(workbook):
    """workbook.xml that makes Excel recalculate every formula when the file opens."""
    if "fullCalcOnLoad" in workbook:
        return workbook
    if "<calcPr" in workbook:
        return re.sub(r"<calcPr", '<calcPr fullCalcOnLoad="1"', workbook, count=1)
    return workbook.replace("</workbook>", '<calcPr fullCalcOnLoad="1"/></workbook>')


def xlsx_values(path, sheet="xl/worksheets/sheet1.xml"):
    """{ref: value} of one sheet: text as str, numbers as float, formulas as their cached value."""
    parts = read_zip(path)
    shared = []
    if "xl/sharedStrings.xml" in parts:
        ss = get(parts, "xl/sharedStrings.xml")
        for a, b in spans(ss, "si"):
            shared.append("".join(re.findall(r"<t(?:\s[^>]*)?>([^<]*)</t>", ss[a:b])))
    s = get(parts, sheet)
    out = {}
    for a, b in spans(s, "c"):
        c = s[a:b]
        ref = re.search(r'r="([A-Z]+\d+)"', c).group(1)
        t = re.search(r'\st="([^"]+)"', c[:c.find(">") + 1])
        t = t.group(1) if t else "n"
        if t == "inlineStr":
            v = "".join(re.findall(r"<t(?:\s[^>]*)?>([^<]*)</t>", c))
        else:
            m = re.search(r"<v>([^<]*)</v>", c)
            if not m:
                continue
            v = m.group(1)
            if t == "s":
                v = shared[int(v)] if v.isdigit() and int(v) < len(shared) else ""
            elif t in ("n",):
                try:
                    v = float(v)
                except ValueError:
                    pass
        out[ref] = _unescape(v) if isinstance(v, str) else v
    return out


def _unescape(s):
    return s.replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", '"').replace("&apos;", "'").replace("&amp;", "&")


# ---------------- a new workbook (one sheet) ----------------
STYLES = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
          '<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
          '<fonts count="2"><font><sz val="10"/><name val="Arial"/></font><font><b/><sz val="10"/><color rgb="FFFFFFFF"/><name val="Arial"/></font></fonts>'
          '<fills count="4"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill>'
          '<fill><patternFill patternType="solid"><fgColor rgb="FF1F3864"/><bgColor indexed="64"/></patternFill></fill>'
          '<fill><patternFill patternType="solid"><fgColor rgb="FFFFF2CC"/><bgColor indexed="64"/></patternFill></fill></fills>'
          '<borders count="2"><border><left/><right/><top/><bottom/><diagonal/></border>'
          '<border><left style="thin"><color rgb="FFA6A6A6"/></left><right style="thin"><color rgb="FFA6A6A6"/></right>'
          '<top style="thin"><color rgb="FFA6A6A6"/></top><bottom style="thin"><color rgb="FFA6A6A6"/></bottom><diagonal/></border></borders>'
          '<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>'
          '<cellXfs count="4"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>'
          '<xf numFmtId="0" fontId="1" fillId="2" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1">'
          '<alignment horizontal="center" vertical="center" wrapText="1"/></xf>'
          '<xf numFmtId="0" fontId="0" fillId="0" borderId="1" xfId="0" applyBorder="1"><alignment vertical="top" wrapText="1"/></xf>'
          '<xf numFmtId="0" fontId="0" fillId="3" borderId="1" xfId="0" applyFill="1" applyBorder="1"><alignment vertical="top" wrapText="1"/></xf>'
          '</cellXfs><cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles></styleSheet>')
HEAD, BODY, MARK = 1, 2, 3     # cell styles above: header, body, highlighted body


def new_xlsx(path, sheet_name, header, data, widths=None, marked=(), title_rows=()):
    """One-sheet workbook: optional title rows (text), a header row (dark, white bold), data rows (bordered; rows whose
    index is in marked are yellow). Header frozen, autofilter on, fits one page wide (landscape)."""
    ncols = len(header)
    xml_rows, r = [], 1
    for t in title_rows:
        xml_rows.append('<row r="%d">%s</row>' % (r, _cell_xml("A%d" % r, t, None)))
        r += 1
    if title_rows:
        r += 1
    hr = r
    xml_rows.append('<row r="%d" ht="30" customHeight="1">%s</row>' % (r, "".join(_cell_xml("%s%d" % (col_name(i + 1), r), h, HEAD) for i, h in enumerate(header))))
    for k, values in enumerate(data):
        r += 1
        st = MARK if k in marked else BODY
        xml_rows.append('<row r="%d">%s</row>' % (r, "".join(_cell_xml("%s%d" % (col_name(i + 1), r), v, st) for i, v in enumerate(values))))
    cols = "".join('<col min="%d" max="%d" width="%s" customWidth="1"/>' % (i + 1, i + 1, w) for i, w in enumerate(widths or []))
    last = "%s%d" % (col_name(ncols), max(r, hr))
    sheet = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
             '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
             'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
             '<sheetPr><pageSetUpPr fitToPage="1"/></sheetPr><dimension ref="A1:%s"/>'
             '<sheetViews><sheetView workbookViewId="0"><pane ySplit="%d" topLeftCell="A%d" activePane="bottomLeft" state="frozen"/></sheetView></sheetViews>'
             '<sheetFormatPr defaultRowHeight="13.2"/>%s<sheetData>%s</sheetData>'
             '<autoFilter ref="A%d:%s"/>'
             '<pageMargins left="0.4" right="0.4" top="0.5" bottom="0.5" header="0.3" footer="0.3"/>'
             '<pageSetup orientation="landscape" fitToWidth="1" fitToHeight="0"/></worksheet>'
             % (last, hr, hr + 1, ("<cols>%s</cols>" % cols) if cols else "", "".join(xml_rows), hr, last))
    name = escape(sheet_name[:31])
    parts = {
        "[Content_Types].xml": ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
            '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
            '<Default Extension="xml" ContentType="application/xml"/>'
            '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
            '<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
            '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>'
            '</Types>'),
        "_rels/.rels": ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
            '</Relationships>'),
        "xl/workbook.xml": ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
            'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
            '<sheets><sheet name="%s" sheetId="1" r:id="rId1"/></sheets>'
            '<definedNames><definedName name="_xlnm._FilterDatabase" localSheetId="0" hidden="1">\'%s\'!$A$%d:$%s$%d</definedName></definedNames>'
            '</workbook>' % (name, name.replace("'", "''"), hr, col_name(ncols), max(r, hr))),
        "xl/_rels/workbook.xml.rels": ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>'
            '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
            '</Relationships>'),
        "xl/styles.xml": STYLES,
        "xl/worksheets/sheet1.xml": sheet,
    }
    write_zip({k: v.encode("utf-8") for k, v in parts.items()}, path)
    return path
