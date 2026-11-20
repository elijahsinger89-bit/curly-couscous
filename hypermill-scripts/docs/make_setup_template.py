#!/usr/bin/env python3
"""Builds tool_library/templates/NC_MASTER_SETUP.docx (the template job_docs fills) from your NC_MASTER_SETUP_blank_v2.docx:
  - "MILLING TOOL LIST" -> "TOOL LIST" (turning tools are on it too)
  - "HYPERMILL SIM DATE:" in the empty top-right cell, above VERICUT DATE / VERICUT BY (filled by job_docs; Vericut by hand)
  - a property notice at the bottom of every page (FOOTER_NOTE)
  - the logo top left: not yet (send the logo; then it goes in here)
Run on the PC that builds the package: python3 docs/make_setup_template.py"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TPL = os.path.join(os.path.dirname(HERE), "copy_to_python_folder", "tool_library", "templates")
sys.path.insert(0, os.path.dirname(TPL))
import office_fill as of   # noqa: E402

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
    tbl = tbl[:r0a] + row0 + tbl[r0b:]
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
