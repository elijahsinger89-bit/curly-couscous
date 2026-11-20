#!/usr/bin/env python3
"""Builds tool_library/templates/NC_MASTER_SETUP.docx (the template job_docs fills) from your NC_MASTER_SETUP_blank_v2.docx:
  - "MILLING TOOL LIST" -> "TOOL LIST" (turning tools are on it too)
  - "HYPERMILL SIM DATE:" in the empty top-right cell, above VERICUT DATE / VERICUT BY (filled by job_docs; Vericut by hand)
  - a property notice at the bottom of every page (FOOTER_NOTE)
  - the HELLER logo in the top-left cell, above "NC SETUP" (docs/heller_logo.png, made from the official heller_logo.svg)
Run on the PC that builds the package: python3 docs/make_setup_template.py"""
import os
import re
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TPL = os.path.join(os.path.dirname(HERE), "copy_to_python_folder", "tool_library", "templates")
sys.path.insert(0, os.path.dirname(TPL))
import office_fill as of   # noqa: E402

LOGO = os.path.join(HERE, "heller_logo.png")
LOGO_WIDTH_IN = 1.5
LOGO_RID = "rIdHellerLogo"

FOOTER_NOTE = ("PROPRIETARY - This document and the information in it belong to Heller and are given only for the work "
               "it was issued for. Do not copy it, show it or pass it on without written permission.")


def retitle(s):
    """'MILLING TOOL LIST' paragraphs -> 'TOOL LIST' (first run keeps its formatting, the other runs' text is removed)."""
    edits = []
    for a, b in of.innermost(s):
        p = s[a:b]
        if of.plain(p).upper() != "MILLING TOOL LIST":
            continue
        rs = of.spans(p, "w:r")
        new, done = p, False
        for ra, rb in reversed(rs):
            r = p[ra:rb]
            if "<w:t" not in r:
                continue
            r2 = re.sub(r"(<w:t(?:\s[^>]*)?>)[^<]*(</w:t>)", r"\g<1>\g<2>", r)
            new = new[:ra] + r2 + new[rb:]
        ra, rb = next((x for x in of.spans(new, "w:r") if "<w:t" in new[x[0]:x[1]]), (None, None))
        if ra is not None:
            r = new[ra:rb]
            r = re.sub(r"<w:t(?:\s[^>]*)?></w:t>", '<w:t xml:space="preserve">TOOL LIST</w:t>', r, count=1)
            new = new[:ra] + r + new[rb:]
            done = True
        if done:
            edits.append((a, b, new))
    for a, b, new in reversed(edits):
        s = s[:a] + new + s[b:]
    return s, len(edits)


def logo_run(cx, cy):
    """Inline picture run (wp / r are declared on the document root; a / pic declared here)."""
    a = "http://schemas.openxmlformats.org/drawingml/2006/main"
    return ('<w:r><w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0"><wp:extent cx="%d" cy="%d"/>'
            '<wp:effectExtent l="0" t="0" r="0" b="0"/><wp:docPr id="7001" name="HELLER logo" descr="HELLER"/>'
            '<wp:cNvGraphicFramePr><a:graphicFrameLocks xmlns:a="%s" noChangeAspect="1"/></wp:cNvGraphicFramePr>'
            '<a:graphic xmlns:a="%s"><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
            '<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"><pic:nvPicPr>'
            '<pic:cNvPr id="0" name="heller_logo.png"/><pic:cNvPicPr/></pic:nvPicPr><pic:blipFill><a:blip r:embed="%s"/>'
            '<a:stretch><a:fillRect/></a:stretch></pic:blipFill><pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="%d" cy="%d"/>'
            '</a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic></a:graphicData></a:graphic>'
            '</wp:inline></w:drawing></w:r>' % (cx, cy, a, a, LOGO_RID, cx, cy))


def add_logo(parts, tc):
    """Top-left cell: its first empty paragraph becomes the logo (centred), the spacer paragraph goes, "NC SETUP" is centred
    under it. Adds the picture, its relationship and the png content type. Returns the new cell XML."""
    data = open(LOGO, "rb").read()
    w, h = struct.unpack(">II", data[16:24])
    cx = int(LOGO_WIDTH_IN * 914400)
    cy = int(round(cx * h / float(w)))
    parts["word/media/heller_logo.png"] = data
    rels = of.get(parts, "word/_rels/document.xml.rels")
    if LOGO_RID not in rels:
        rels = rels.replace("</Relationships>", '<Relationship Id="%s" Type="http://schemas.openxmlformats.org/officeDocument/2006/'
                            'relationships/image" Target="media/heller_logo.png"/></Relationships>' % LOGO_RID)
        of.put(parts, "word/_rels/document.xml.rels", rels)
    ct = of.get(parts, "[Content_Types].xml")
    if 'Extension="png"' not in ct:
        ct = ct.replace('<Default Extension="xml"', '<Default Extension="png" ContentType="image/png"/><Default Extension="xml"', 1)
        of.put(parts, "[Content_Types].xml", ct)
    ps = of.spans(tc, "w:p")
    k = next(i for i, (a, b) in enumerate(ps) if "NC" in of.plain(tc[a:b]).upper())
    if k < 1 or any(of.plain(tc[a:b]) for a, b in ps[:k]):
        raise SystemExit("top-left cell has no empty paragraph above NC SETUP")
    pa, pb = ps[k]
    nc = re.sub(r'<w:ind w:left="\d+"/>', '<w:jc w:val="center"/>', tc[pa:pb], count=1)
    logo_p = ('<w:p><w:pPr><w:pStyle w:val="TableParagraph"/><w:spacing w:before="90" w:after="50"/><w:jc w:val="center"/></w:pPr>'
              + logo_run(cx, cy) + '</w:p>')
    return tc[:ps[0][0]] + logo_p + nc + tc[pb:]


def main():
    src = os.path.join(TPL, "NC_MASTER_SETUP_blank_v2.docx")
    out = os.path.join(TPL, "NC_MASTER_SETUP.docx")
    parts = of.read_zip(src)
    n_title = 0
    for name in [n for n in parts if re.match(r"word/header\d*\.xml$", n)]:
        s, k = retitle(of.get(parts, name))
        of.put(parts, name, s)
        n_title += k
    doc = of.get(parts, "word/document.xml")
    ta, tb = of.tables(doc)[0]
    tbl = doc[ta:tb]
    rs = of.rows(tbl)
    r0a, r0b = rs[0]
    cs = of.cells(tbl[r0a:r0b])
    ca, cb = cs[-1]
    tc = tbl[r0a:r0b][ca:cb]
    if of.plain(tc):
        raise SystemExit("top-right cell is not empty: %r" % of.plain(tc))
    vp = next(tbl[a:b] for a, b in of.innermost(tbl) if of.plain(tbl[a:b]).upper().startswith("VERICUT DATE"))
    rpr = re.search(r"<w:rPr>.*?</w:rPr>", vp, re.S).group(0)
    tc2 = of.set_cell(tc, "HYPERMILL SIM DATE:", rpr=rpr)
    row0 = tbl[r0a:r0b]
    row0 = row0[:ca] + tc2 + row0[cb:]
    la, lb = of.cells(row0)[0]
    row0 = row0[:la] + add_logo(parts, row0[la:lb]) + row0[lb:]
    tbl =tbl[:r0a] + row0 + tbl[r0b:]
    doc = doc[:ta] + tbl + doc[tb:]
    of.put(parts, "word/document.xml", doc)
    n_foot = 0
    for name in [n for n in parts if re.match(r"word/footer\d*\.xml$", n)]:
        of.put(parts, name, of.add_footer_note(of.get(parts, name), FOOTER_NOTE))
        n_foot += 1
    of.write_zip(parts, out)
    print("wrote %s (title fixed in %d header paragraphs, notice in %d footers)" % (out, n_title, n_foot))


if __name__ == "__main__":
    main()
