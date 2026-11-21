#!/usr/bin/env python3
"""Sandvik Coromant Rotating Tools 2020 -> holder tables (CSV) for tool_library/holders.

Reads word positions from the PDF (pdftotext -bbox-layout, poppler) so every value lands in its column by x position:
merged group cells (printed once per group) are filled down, values that plain text extraction stacks stay in their
row, order codes may contain spaces, and the unlabeled icon columns (coolant bar / torque Nm / weight kg) are left out.

Run (on the PC that builds the package, not in hyperMILL):
  python3 docs/catalog_extract/sandvik_2020.py <pdf> [<pdf> ...] --first-page <catalog page of the first PDF page> ...
  python3 docs/catalog_extract/sandvik_2020.py "Rotating Tools 2020 353-400.pdf" 353 "Rotating Tools 2020 400-463.pdf" 400
Writes copy_to_python_folder/tool_library/holders/sandvik_hsk.csv and sandvik_capto.csv and prints a report.
Only machine side HSK and Coromant Capto tables are kept."""
import os
import re
import sys
import csv
import html
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(os.path.dirname(HERE)), "copy_to_python_folder", "tool_library", "holders")

# columns kept, in CSV order (ISO 13399 names as printed in the catalog)
GEOM = ["DCONMS", "DBC", "DCONWS", "LSC", "LF", "LB1", "LB2", "LB3", "LB4", "LB5", "BD1", "BD2", "BD3", "BD4", "BD5",
        "BHTA1", "BHTA2", "BHTA3", "CRNT", "RPMX"]
LEFT = ["CZCMS", "CZCWS", "TRMAX", "CNSC", "CXSC", "DSGN"]      # printed left of the order code
CSV_COLS = ["maker", "interface", "machine_side", "family", "design", "note", "page", "table", "ordering_code"] + LEFT + GEOM
WORD_RE = re.compile(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</word>')
PAGE_RE = re.compile(r'<page width="[\d.]+" height="([\d.]+)">(.*?)</page>', re.S)


def words_by_page(pdf):
    out = subprocess.run(["pdftotext", "-bbox-layout", pdf, "-"], capture_output=True, text=True, check=True).stdout
    pages = []
    for m in PAGE_RE.finditer(out):
        ws = [dict(x0=float(a), y0=float(b), x1=float(c), y1=float(d), t=html.unescape(e))
              for a, b, c, d, e in WORD_RE.findall(m.group(2))]
        pages.append(ws)
    return pages


def header_tokens(ws, hy):
    """Header words on the line at hy (with their subscripts), merged into tokens: [(name, x0, x1)]."""
    line = sorted([w for w in ws if -1.0 <= w["y0"] - hy <= 3.5], key=lambda w: w["x0"])
    toks = []
    for w in line:
        if toks and w["x0"] - toks[-1][2] < 0.6 and w["t"] != "code":      # subscript glued to its letters
            toks[-1] = (toks[-1][0] + w["t"], toks[-1][1], w["x1"])
        else:
            toks.append((w["t"], w["x0"], w["x1"]))
    out = []
    for t in toks:
        if t[0] == "code" and out and out[-1][0] == "Ordering":
            out[-1] = ("Ordering code", out[-1][1], t[2])
        else:
            out.append(t)
    return out


def rows_below(ws, hy, stop_y):
    """Words between the header and stop_y grouped into rows by their vertical centre."""
    body = sorted([w for w in ws if hy + 5 < (w["y0"] + w["y1"]) / 2 < stop_y], key=lambda w: ((w["y0"] + w["y1"]) / 2, w["x0"]))
    rows = []
    for w in body:
        yc = (w["y0"] + w["y1"]) / 2
        if rows and abs(rows[-1][0] - yc) < 2.2:
            rows[-1][1].append(w)
        else:
            rows.append([yc, [w]])
    return rows


def title_above(ws, hy, prev_y):
    """Family / design / note lines between the previous table (or page top) and this header."""
    lines = {}
    for w in ws:
        if prev_y < w["y0"] < hy - 2 and w["x0"] < 330:
            lines.setdefault(round(w["y0"]), []).append(w)
    out = []
    for y in sorted(lines):
        ws_ = sorted(lines[y], key=lambda w: w["x0"])
        h = max(w["y1"] - w["y0"] for w in ws_)
        txt = " ".join(w["t"] for w in ws_).strip()
        if txt and not re.fullmatch(r"[A-Z]|Dimensions, mm|[\d\s.,°-]+", txt):
            out.append((h, txt))
    return out


def parse_pdf(pdf, first_page):
    tables = []
    for pi, ws in enumerate(words_by_page(pdf)):
        ws = [w for w in ws if not (re.fullmatch(r"[A-Z]", w["t"]) and (w["x0"] < 33 or w["x0"] > 555))]   # edge tabs
        heads = sorted(set(round(w["y0"], 1) for w in ws if w["t"] == "Ordering"))
        page_text = " ".join(w["t"] for w in ws)
        interface = "HSK" if "Machine side interface HSK" in page_text else (
            "CAPTO" if re.search(r"Machine side interface Coromant Capto", page_text) else "")
        foot = min([w["y0"] for w in ws if w["t"] == "spare"] + [10000])
        prev = 0.0
        for k, hy in enumerate(heads):
            toks = header_tokens(ws, hy)
            cols = [t for t in toks if t[0] in LEFT + GEOM or t[0] == "Ordering code"]
            names = [c[0] for c in cols]
            titles = title_above(ws, hy, prev)
            if "Ordering code" not in names:
                continue
            code_x0 = dict((c[0], c) for c in cols)["Ordering code"][1]
            geo = sorted([c for c in cols if c[0] in GEOM], key=lambda c: c[1])
            first_num = geo[0][1]
            # icon columns (coolant bar / Nm / kg) carry no text header: they sit just before RPMX, or after the last
            # column when a table has no RPMX. Values there belong to no column.
            gap = (geo[-2][2], geo[-1][1]) if len(geo) > 1 and geo[-1][0] == "RPMX" else (geo[-1][2] + 1, 1e9)
            stop = min(foot, heads[k + 1] if k + 1 < len(heads) else 10000)
            rows, fill, last_y = [], {}, hy
            for yc, rws in rows_below(ws, hy, stop):
                code_words = [w for w in rws if code_x0 - 3 <= w["x0"] < first_num - 4]
                code = " ".join(w["t"] for w in sorted(code_words, key=lambda w: w["x0"])).strip()
                vals, stray = {}, []
                for w in rws:
                    if w in code_words:
                        continue
                    cx = (w["x0"] + w["x1"]) / 2
                    best = None
                    for name, x0, x1 in cols:
                        if name == "Ordering code":
                            continue
                        hx = (x0 + x1) / 2
                        tol = max((x1 - x0) / 2, (w["x1"] - w["x0"]) / 2) + 2.5
                        if abs(cx - hx) <= tol and (best is None or abs(cx - hx) < best[1]):
                            best = (name, abs(cx - hx))
                    if best:
                        vals[best[0]] = (vals.get(best[0], "") + " " + w["t"]).strip()
                    elif not (gap[0] < cx < gap[1]):
                        stray.append(w["t"])
                n_geo = sum(1 for c in vals if c in GEOM and num(vals[c]) is not None)
                if not code or n_geo < 2:                            # end of the table (title of the next one ...)
                    break
                for c in LEFT:                                       # merged group cells: fill down
                    if c in names:
                        if vals.get(c):
                            fill[c] = vals[c]
                            for later in LEFT[LEFT.index(c) + 1:]:
                                fill.pop(later, None)
                        elif c in fill:
                            vals[c] = fill[c]
                rows.append(dict(code=code, vals=vals, y=yc, stray=stray))
                last_y = yc
            prev = last_y + 4
            tables.append(dict(page=first_page + pi, pdf_page=pi + 1, interface=interface, titles=titles, columns=names, rows=rows))
    return tables


def num(s):
    s = (s or "").replace("°", "").strip()
    try:
        return float(s)
    except ValueError:
        return None


def check_row(t, r):
    """Problems with one row (empty list = fine). Blank cells are normal: a design without that dimension."""
    p = []
    for c in ("DCONMS", "LF"):
        if c in t["columns"] and num(r["vals"].get(c)) is None:
            p.append("%s missing or not a number: %r" % (c, r["vals"].get(c)))
    for c, v in r["vals"].items():
        if c in GEOM and c != "DCONWS" and num(v) is None:
            p.append("%s not a number: %r" % (c, v))
    if r["stray"]:
        p.append("values in no column: %s" % " ".join(r["stray"]))
    return p


FAMILY_RE = re.compile(r"^(HSK|Coromant Capto®)\s.*(adaptor|adapter|chuck|930|970)", re.I)
SKIP_PAGES = range(459, 463)        # Silent Tools damped adaptors


def label(t, carry):
    """family (e.g. 'HSK to CoroChuck™ 930'), design ('Slender design'), machine side ('HSK A/C') and note lines for a
    table; family / machine side carry over from the table before when this one has none."""
    fam = design = side = ""
    notes = []
    for h, s_ in t["titles"]:
        if s_.startswith("DSGN") or "ROTATING TOOL" in s_:
            continue
        m = re.search(r"Machine side interface\s+(.*)$", s_)
        if m:
            side = m.group(1).strip()
        elif FAMILY_RE.search(s_) and h >= 9:
            fam, design, notes = s_, "", []
        elif re.search(r"design\b", s_, re.I) and len(s_) < 60:
            design = s_
        else:
            notes.append(s_)
    if not fam and carry.get("page") == t["page"]:
        fam = carry["family"]
    if not side and carry.get("page") == t["page"]:
        side = carry["side"]
    fam = fam or carry.get("family", "")
    if not design and carry.get("page") == t["page"] and carry.get("family") == fam:
        design = carry.get("design", "")              # second drawing of the same design on the page
    return fam, design, side, "; ".join(notes)[:160]


def crosscheck(pairs, keep):
    """Independent check: every row's values must appear, in order, after its order code in the plain-text extraction
    of the same page (pdftotext -layout). Rows whose values the plain text stacks on other lines cannot be checked."""
    text = {}
    for pdf, first in pairs:
        out = subprocess.run(["pdftotext", "-layout", pdf, "-"], capture_output=True, text=True, check=True).stdout
        for i, pg in enumerate(out.split("\f")):
            text.setdefault(first + i, pg)
    ok = stacked = 0
    wrong = []
    for t in keep:
        for r in t["rows"]:
            line = next((l for l in text.get(t["page"], "").split("\n") if re.search(re.escape(r["code"]) + r"(\s|$)", l)), None)
            vals = [r["vals"][c].replace("°", "") for c in GEOM if r["vals"].get(c)]
            after = line.split(r["code"], 1)[1].replace("°", "").split() if line else []
            if len(after) < len(vals):
                stacked += 1
                continue
            it = iter(after)
            if all(any(v == a for a in it) for v in vals):
                ok += 1
            else:
                wrong.append(r["code"])
    return ok, stacked, wrong


def main(args):
    pairs = list(zip(args[0::2], [int(x) for x in args[1::2]]))
    tables = []
    for pdf, first in pairs:
        tables += parse_pdf(pdf, first)
    keep = [t for t in tables if t["interface"] in ("HSK", "CAPTO") and t["page"] not in SKIP_PAGES]
    carry = {}
    for t in keep:
        t["family"], t["design"], t["side"], t["note"] = label(t, carry)
        carry = dict(page=t["page"], family=t["family"], side=t["side"], design=t["design"])
    # HSK tables that are not for HSK A (F with pins for Makino ...) are left out: the machines are HSK-A
    dropped = [t for t in keep if t["interface"] == "HSK" and t["side"] and not re.search(r"\bA\b|A/", t["side"])]
    keep = [t for t in keep if t not in dropped]
    os.makedirs(OUT, exist_ok=True)
    report, bad_total = [], 0
    for iface, fname in (("HSK", "sandvik_hsk.csv"), ("CAPTO", "sandvik_capto.csv")):
        with open(os.path.join(OUT, fname), "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(CSV_COLS)
            n = 0
            for ti, t in enumerate([t for t in keep if t["interface"] == iface], 1):
                bad = []
                for r in t["rows"]:
                    pr = check_row(t, r)
                    if pr:
                        bad.append((r["code"] or "?", pr))
                        continue
                    w.writerow(["Sandvik", iface, t["side"], t["family"], t["design"], t["note"], t["page"], ti, r["code"]] +
                               [r["vals"].get(c, "") for c in LEFT + GEOM])
                    n += 1
                bad_total += len(bad)
                report.append("%-5s p%d t%-2d %-12s %-46s %-20s %3d rows%s" % (iface, t["page"], ti, t["side"][:12], t["family"][:46], t["design"][:20],
                                                                     len(t["rows"]) - len(bad), (", %d flagged" % len(bad)) if bad else ""))
                for code, pr in bad:
                    report.append("        FLAGGED %s: %s" % (code, "; ".join(pr)))
            report.append("%s: %d rows -> %s" % (iface, n, fname))
    for t in dropped:
        report.append("left out (not HSK A): p%d %s | %s | %d rows" % (t["page"], t["family"], t["side"], len(t["rows"])))
    print("\n".join(report))
    print("flagged rows (left out): %d" % bad_total)
    ok, stacked, wrong = crosscheck(pairs, keep)
    print("plain-text cross-check: %d rows confirmed, %d not checkable (values stacked in the plain text: check those by eye), "
          "%d MISMATCH%s" % (ok, stacked, len(wrong), (": " + ", ".join(wrong[:10])) if wrong else ""))


if __name__ == "__main__":
    main(sys.argv[1:])
