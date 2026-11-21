# hole_tools.py - taps, thread mills and reamers from the Walter CSVs: selection, cutting data, tool XML.
# Selection returns a row copy that tool_builder.get_or_create can build (dia_in / dia_mm / oal_mm filled in).
import os, re, math, copy
import xml.etree.ElementTree as ET
import tool_builder as tb

MM = 25.4
TYPE_CODE = {"tap": 60, "reamer": 61, "threadmill": 62}
METRIC_COARSE = {"M1": 0.25, "M1.6": 0.35, "M2": 0.4, "M2.5": 0.45, "M3": 0.5, "M4": 0.7, "M5": 0.8, "M6": 1.0, "M8": 1.25, "M10": 1.5,
                 "M12": 1.75, "M14": 2.0, "M16": 2.0, "M18": 2.5, "M20": 2.5, "M22": 2.5, "M24": 3.0, "M27": 3.0, "M30": 3.5}

TIER_FILTER = None      # set to a set of tier names to limit selection to that grade

def _f(x, d=0.0):
    return tb._f(x, d)

def _load(name):
    rows = tb.load_rows(name)
    if TIER_FILTER:
        rows = [r for r in rows if (r.get("tier") or "") in TIER_FILTER]
    return rows

def iso_letter(material):
    return (material or "N").strip()[:1].upper()

def _grp(material):
    """Walter group for tap and thread mill data. N1 (aluminum, not hardenable) runs far slower than hardenable wrought
    aluminum (6061, 7075, 2024), which is what the Aluminum group holds here, so N1 is read as N2."""
    g = tb.material_group(material)
    return "N2" if g == "N1" else g

def _rate(row, material):
    return int(_f(row.get("iso_" + iso_letter(material)), 0))

def parse_thread(desig):
    """hyperMILL thread designation -> dict(std 'M'/'UNC'/'UNF', key, dia_in, pitch_in, name). None if unreadable.
    Examples: '1/4-20 UNC', '#4-40 UNC', '1/4-28 UNF', 'M6', 'M6x1'."""
    s = (desig or "").strip().upper().replace(" ", "")
    if not s:
        return None
    m = re.match(r"^MJ(\d+(?:\.\d+)?)(?:X(\d+(?:\.\d+)?))?$", s)
    if m:                                          # MJ (aerospace metric, controlled root radius): same sizes and pitches as M
        d = float(m.group(1)); p = float(m.group(2)) if m.group(2) else METRIC_COARSE.get("M" + m.group(1).rstrip("0").rstrip(".") if "." in m.group(1) else "M" + m.group(1))
        if not p:
            return None
        key = "MJ%g" % d + ("" if not m.group(2) else "X%g" % p)
        return dict(std="MJ", key=key, dia_in=d / MM, pitch_in=p / MM, name="MJ%g" % d + ("x%g" % p if m.group(2) else ""), coarse=not m.group(2))
    m = re.match(r"^M(\d+(?:\.\d+)?)(?:X(\d+(?:\.\d+)?))?$", s)
    if m:
        d = float(m.group(1)); p = float(m.group(2)) if m.group(2) else METRIC_COARSE.get("M" + m.group(1).rstrip("0").rstrip(".") if "." in m.group(1) else "M" + m.group(1))
        if not p:
            return None
        key = "M%g" % d + ("" if not m.group(2) else "X%g" % p)
        return dict(std="M", key=key, dia_in=d / MM, pitch_in=p / MM, name="M%g" % d + ("x%g" % p if m.group(2) else ""), coarse=not m.group(2))
    m = re.match(r"^(#\d+|\d+(?:\.\d+)?/\d+|\d+\.\d+/\d+|\d+)-(\d+)(UNC|UNF|UNEF|UN|UNJC|UNJF)?$", s)
    if m:
        size, tpi, std = m.group(1), int(m.group(2)), (m.group(3) or "UNC")
        if size.startswith("#"):
            n = int(size[1:]); dia = 0.060 + 0.013 * n
        elif "/" in size:
            if "." in size:
                w, fr = size.split("."); a, b = fr.split("/"); dia = int(w) + int(a) / int(b)
            else:
                a, b = size.split("/"); dia = int(a) / int(b)
        else:
            dia = float(size)
        return dict(std=std, key="%s%s-%d" % (std, size, tpi), dia_in=dia, pitch_in=1.0 / tpi, name="%s-%d %s" % (size, tpi, std), coarse=False)
    return None

def _row_key(row):
    t = row.get("thread", "").upper().replace(" ", "")
    m = re.match(r"^(UNC|UNF|UNEF|UN|UNJC|UNJF)(.*)$", t)
    return (m.group(1) + m.group(2)) if m else t.replace("X", "X")

def _norm_key(k):
    return k.upper().replace(" ", "")

def same_standard(row, th):
    """Nearest-size fallback only within the same thread family: UN... rows for UNC/UNF requests, M rows for metric, MJ and UNJ
    rows only for MJ and UNJ requests.
    Pipe (NPT, NPTF, NPS, G), Whitworth and other standards never stand in for UN or M threads."""
    k = _row_key(row).upper()
    if th["std"] == "MJ":                          # J forms (controlled root radius) never mix with M or UN taps
        return k.startswith("MJ")
    if th["std"] == "M":
        return k.startswith("M") and not k.startswith("MJ")
    if th["std"].startswith("UNJ"):
        return k.startswith("UNJ")
    return k.startswith("UN") and not k.startswith("UNJ")

HOLE_FILES = {"Walter": {"taps": "walter_taps.csv", "threadmills": "walter_threadmills.csv"},
              "Kennametal": {"taps": "kennametal_taps.csv", "threadmills": "kennametal_threadmills.csv"}}

# ---------------- taps ----------------
def _first(rows, material):
    """First choice = rated 2 (primary) for the material's ISO group; falls back to the rated-1 rows with a note."""
    top = [r for r in rows if _rate(r, material) >= 2]
    if top:
        return top, ""
    return rows, "NOT FIRST CHOICE: catalog rates it suitable (1), not primary (2), for ISO %s" % iso_letter(material)

def _join(note, extra):
    return (note + " | " + extra) if (note and extra) else (note or extra)

def select_tap(designation, thread_len_in, material, manufacturer="Walter"):
    th = parse_thread(designation)
    if th is None:
        return None, "thread designation not readable: %r" % designation
    files = HOLE_FILES.get(manufacturer, {})
    if "taps" not in files:
        return None, "%s has no tap catalog loaded yet" % manufacturer
    rows = _load(files["taps"])
    want = _norm_key(th["key"])
    exact = [r for r in rows if _norm_key(_row_key(r)) == want]
    note = ""
    if not exact:
        near = [r for r in rows if same_standard(r, th) and r["dia_in"] and abs(_f(r["dia_in"]) - th["dia_in"]) < 0.004 and abs((1.0 / _f(r["tpi"], 1e9) if r["tpi"] else _f(r["pitch_mm"]) / MM) - th["pitch_in"]) < 0.002]
        if not near:
            return None, "no %s tap for %s" % (manufacturer, designation)
        exact = near; note = "nearest tap size"
    cut = tb.load_rows("walter_tap_cutting.csv")
    grp = _grp(material)
    fam_vc = {}
    for c in cut:
        if c["group"] == grp:
            fam_vc.setdefault(c["family"], []).append(_f(c["vc_mpm"]))
    ok = [r for r in exact if r["family"] in fam_vc and _rate(r, material) >= 1] or [r for r in exact if _rate(r, material) >= 1]
    if not ok:
        return None, "no %s tap rated for %s" % (manufacturer, material)
    long_enough = [r for r in ok if _f(r["thread_len_mm"]) / MM >= thread_len_in] or ok
    long_enough, fb = _first(long_enough, material)
    note = _join(note, fb)
    def key(r):
        return (-_rate(r, material), -int(r["tier_rank"] or 0), 0 if r["form"] == "cutting" else 1, abs(_f(r["thread_len_mm"]) / MM - thread_len_in))
    long_enough.sort(key=key)
    r = copy.deepcopy(long_enough[0])
    r["dia_in"] = "%.4f" % (_f(r["dia_in"]) or th["dia_in"]); r["_thread"] = th
    return r, note

def _kenn_tap_cut(row, material):
    """Kennametal tap application data (Master Catalog M180, M182): SFM start value per ISO letter and tap style. The table's group numbers
    are not reliably aligned in the text extraction, so rows of the ISO letter are ranked by speed and the material's group number picks
    the position (harder group = slower row)."""
    grp = tb.KENN_GROUP.get(material)
    if not grp:
        return None
    fam = row["family"]
    if fam == "KHSST":                             # general purpose HSS taps: the printed style is in the title
        t = row.get("title", "")
        fam = next((st for st in ("KHSST Spiral Point", "KHSST Spiral Flute", "KHSST Hand") if t.startswith(st)), "")
        if not fam:
            return None                            # pipe and left hand KHSST taps: no printed data
    coolant_of = {"T621": "T620", "T623": "T622", "T625": "T624", "T627": "T626", "T631": "T630", "T633": "T632", "T641": "T640", "T643": "T642", "T651": "T650", "T822": "T820", "T834": "T830"}
    boost = 1.25 if fam in coolant_of and fam not in ("T822", "T834") else 1.0     # catalog note: up to 25% faster with coolant taps
    fam = coolant_of.get(fam, fam)
    rows = [r for r in tb.load_rows("kennametal_tap_cutting.csv") if r["group"][0] == grp[0] and fam in r["styles"].split(",")]
    col = "sfm_start"
    if not rows:
        rows = [r for r in tb.load_rows("kennametal_tap_cutting.csv") if r["group"][0] == grp[0] and fam in r["blind_styles"].split(",")]
        col = "blind_start"
    if not rows:
        return None
    rows.sort(key=lambda r: -_f(r[col]))
    n = max(int(grp[1:]), 1); k = 6 if grp[0] in "PN" else 3      # tap tables start at P1: low carbon steel (P0) reads the P1 position
    pos = int(round((min(n, k) - 1) / float(max(k - 1, 1)) * (len(rows) - 1)))
    vc = _f(rows[pos][col]) * boost
    dia = _f(row["dia_in"])
    rpm = vc * 12 / (math.pi * dia)
    if rpm > tb.MAX_RPM:
        vc *= tb.MAX_RPM / rpm; rpm = tb.MAX_RPM
    pitch = 1.0 / _f(row["tpi"]) if row.get("tpi") else _f(row.get("pitch_mm")) / MM
    return dict(vc=vc, rpm=rpm, ipr=pitch, ipm=rpm * pitch)

def tap_cut(row, material):
    if row.get("manufacturer", "Walter") == "Kennametal":
        return _kenn_tap_cut(row, material)
    grp = _grp(material)
    th = row.get("_thread") or parse_thread(row.get("thread", "")) or {}
    c = [x for x in tb.load_rows("walter_tap_cutting.csv") if x["family"] == row["family"] and x["group"] == grp]
    if not c:
        return None
    c = [x for x in c if x.get("grade") == row.get("grade")] or c      # the row for the tap's own grade or coating first
    vc = _f(c[0]["vc_mpm"]) * 3.28084
    dia = _f(row["dia_in"])
    rpm = vc * 12 / (math.pi * dia)
    if rpm > tb.MAX_RPM:
        vc *= tb.MAX_RPM / rpm; rpm = tb.MAX_RPM
    pitch = 1.0 / _f(row["tpi"]) if row.get("tpi") else _f(row.get("pitch_mm")) / MM
    return dict(vc=vc, rpm=rpm, ipr=pitch, ipm=rpm * pitch)

# ---------------- thread mills ----------------
def select_threadmill(designation, thread_len_in, hole_dia_in, material, manufacturer="Walter"):
    th = parse_thread(designation)
    if th is None:
        return None, "thread designation not readable: %r" % designation
    files = HOLE_FILES.get(manufacturer, {})
    if "threadmills" not in files:
        return None, "%s has no thread mill catalog loaded yet" % manufacturer
    rows = [r for r in _load(files["threadmills"]) if r["type"] == "thread mill" and r["cutter_dia_in"] and r.get("thread_len_mm")]   # no printed thread length: the tool cannot be built correctly
    inch = th["std"] not in ("M", "MJ")
    jform = th["std"] in ("MJ", "UNJC", "UNJF")
    fit = []
    for r in rows:
        rng = r["thread_range"].upper()
        if jform and not ("MJ" in rng if th["std"] == "MJ" else "UNJ" in rng):
            continue                               # J threads need a J profile thread mill
        if inch and not any(x in rng for x in ("UNC", "UNF", "UNJ")):
            continue
        if not inch and "M" not in rng:
            continue
        lo, hi = _f(r["min_thread_dia_mm"]) / MM, _f(r["max_thread_dia_mm"]) / MM
        if not (lo - 0.003 <= th["dia_in"] <= (hi or lo) + 0.003):
            continue
        pm = _f(r["pitch_mm"]) / MM
        if pm and abs(pm - th["pitch_in"]) > 0.0015:
            continue
        if _f(r["cutter_dia_in"]) > hole_dia_in * 0.95:
            continue
        if _rate(r, material) < 1:
            continue
        fit.append(r)
    if not fit:
        return None, "no %s thread mill for %s in a %.3f in hole" % (manufacturer, designation, hole_dia_in)
    fit, fb = _first(fit, material)
    def key(r):
        return (-_rate(r, material), -int(r["tier_rank"] or 0), 0 if _f(r["thread_len_mm"]) / MM >= thread_len_in else 1, -_f(r["cutter_dia_in"]))
    fit.sort(key=key)
    r = copy.deepcopy(fit[0]); r["dia_in"] = r["cutter_dia_in"]; r["dia_mm"] = r["cutter_dia_mm"]; r["_thread"] = th
    return r, fb

def _kenn_group_rows(rows, material):
    grp = tb.KENN_GROUP.get(material)
    if not grp:
        return None
    same = [r for r in rows if r["group"][0] == grp[0]]
    if not same:
        return None
    return min(same, key=lambda r: abs(int(r["group"][1:]) - int(grp[1:])))

def _kenn_threadmill_cut(row, material):
    fam = row["family"].split()[0]
    best = _kenn_group_rows([r for r in tb.load_rows("kennametal_threadmill_cutting.csv") if r["family"] == fam], material)
    if not best:
        return None
    dc = _f(row["cutter_dia_in"])
    vc = _f(best["sfm_start"])
    rpm = vc * 12 / (math.pi * dc)
    if rpm > tb.MAX_RPM:
        vc *= tb.MAX_RPM / rpm; rpm = tb.MAX_RPM
    z = int(_f(row.get("flutes"), 3))
    fz = _f(best["fz_small"] if dc < 0.375 else best["fz_large"])
    if best.get("fz_bands"):                       # printed cutter size bands "0.250:0.002;0.375:0.003;0.625:0.004" (upper limit: IPT)
        bands = sorted((_f(a), _f(b)) for a, b in (x.split(":") for x in best["fz_bands"].split(";") if ":" in x))
        fz = next((f for lim, f in bands if dc <= lim + 1e-6), bands[-1][1])
    return dict(vc=vc, rpm=rpm, fz=fz, ipm=rpm * fz * z, group=best["group"], wanted=tb.KENN_GROUP.get(material))

def threadmill_cut(row, material):
    if row.get("manufacturer", "Walter") == "Kennametal":
        return _kenn_threadmill_cut(row, material)
    grp = _grp(material)
    fam = row["family"].split()[0]
    rows = [c for c in tb.load_rows("walter_threadmill_cutting.csv") if c["group"] == grp]
    c = [x for x in rows if x["family"] == fam]
    by = ""
    if not c and fam != "TME":                     # no printed data for this family and group: TME data, labelled as borrowed
        c = [x for x in rows if x["family"] == "TME"]
        by = "TME" if c else ""
    dc = _f(row["cutter_dia_mm"])
    pick = None
    for x in c:
        t = x["thread_range"].replace(" ", "")
        m = re.match(r"^Dc<=([\d.]+)$", t)
        if m and dc <= float(m.group(1)): pick = x; break
        m = re.match(r"^Dc>([\d.]+)-([\d.]+)$", t)
        if m and float(m.group(1)) < dc <= float(m.group(2)): pick = x; break
        m = re.match(r"^Dc>([\d.]+)$", t)
        if m and dc > float(m.group(1)): pick = x; break
    if pick is None:
        return None
    vc = _f(pick["vc_mpm"]) * 3.28084
    rpm = vc * 12 / (math.pi * _f(row["cutter_dia_in"]))
    if rpm > tb.MAX_RPM:
        vc *= tb.MAX_RPM / rpm; rpm = tb.MAX_RPM
    z = int(_f(row.get("flutes"), 3))
    fz = _f(pick["fz_mm"]) / MM
    return dict(vc=vc, rpm=rpm, fz=fz, ipm=rpm * fz * z, borrowed=by)

# ---------------- reamers ----------------
# Walter reamers: Holemaking compendium data (walter_reamer_cutting.csv, walter_reamer_vrr.csv). Where a family prints
# nothing for the material group, the standard values below are used for solid carbide and HSS machine reamers by ISO
# group, in m/min, with feed per revolution as a fraction of the diameter. They are starting values, and say so on screen,
# in the part wizard 2 check list and in the tool comment.
REAM_VC = {"P": (60, 25), "M": (30, 12), "K": (80, 30), "N": (150, 60), "S": (15, 6), "H": (25, 10)}   # (carbide, HSS) m/min
REAM_FN_PER_D = 0.025                                                                             # mm/rev per mm of diameter, bounded below
def _reamer_feed_mm(vrr, dia_mm):
    """Feed per rev (mm) from Walter's reamer feed chart (walter_reamer_vrr.csv): straight line between printed diameters."""
    pts = sorted((_f(r["dia_mm"]), _f(r["f_mm"])) for r in tb.load_rows("walter_reamer_vrr.csv") if r["vrr"] == str(vrr))
    if not pts:
        return None
    d = min(max(dia_mm, pts[0][0]), pts[-1][0])
    for (d0, f0), (d1, f1) in zip(pts, pts[1:]):
        if d0 <= d <= d1:
            return f0 + (f1 - f0) * (d - d0) / (d1 - d0) if d1 > d0 else f0
    return pts[-1][1]

def _walter_reamer_cut(row, material):
    """Walter Holemaking compendium reaming data (walter_reamer_cutting.csv: vc and feed chart VRR per family, coating and
    material group; feed per rev from walter_reamer_vrr.csv). None when the family prints nothing for the group."""
    grp = tb.material_group(material)
    c = [x for x in tb.load_rows("walter_reamer_cutting.csv") if x["family"] == row["family"] and x["group"] == grp and _f(x["vc_mpm"])]
    if not c:
        return None
    own = [x for x in c if x["coating"] == row.get("grade")]
    x = (own or c)[0]
    dia_mm = _f(row["dia_mm"]) or _f(row["dia_in"]) * MM
    fn = _reamer_feed_mm(x["vrr"], dia_mm)
    if not fn:
        return None
    vc = _f(x["vc_mpm"]) * 3.28084
    rpm = vc * 12 / (math.pi * dia_mm / MM)
    if rpm > tb.MAX_RPM:
        vc *= tb.MAX_RPM / rpm; rpm = tb.MAX_RPM
    out = dict(vc=vc, rpm=rpm, ipr=fn / MM, ipm=rpm * fn / MM, grp=grp)
    if not own:
        out["standard"] = "%s reamer data used (no %s data printed for %s)" % (x["coating"], row.get("grade"), grp)
    return out

def reamer_cut(row, material):
    if row.get("manufacturer", "Walter") == "Walter":
        c = _walter_reamer_cut(row, material)
        if c:
            return c
    if row.get("manufacturer") == "GARR":
        import garr_cut
        c = garr_cut.drill_cut(row, material, table="garr_reamer_cutting.csv")
        if c:
            return c
    carbide = row["family"].startswith("F2") or row.get("manufacturer") == "GARR"     # GARR makes solid carbide tools only
    vc = REAM_VC.get(iso_letter(material), (60, 25))[0 if carbide else 1] * 3.28084
    dia = _f(row["dia_in"])
    rpm = vc * 12 / (math.pi * dia)
    if rpm > tb.MAX_RPM:
        vc *= tb.MAX_RPM / rpm; rpm = tb.MAX_RPM
    fn_mm = max(0.05, min(0.5, REAM_FN_PER_D * dia * MM * 2.0))
    return dict(vc=vc, rpm=rpm, ipr=fn_mm / MM, ipm=rpm * fn_mm / MM,
                standard="standard reaming values, not catalog data for this reamer, check before running")

REAMER_FILES = {"Walter": "walter_reamers.csv", "GARR": "garr_reamers.csv"}

def select_reamer(dia_in, depth_in, material, manufacturer="Walter"):
    fn = REAMER_FILES.get(manufacturer)
    if not fn or not os.path.exists(os.path.join(tb.HERE, fn)):
        return None, "%s has no reamer catalog loaded" % manufacturer
    rows = [r for r in _load(fn) if r["dia_in"] and _rate(r, material) >= 1]
    if not rows:
        return None, "no %s reamer rated for %s" % (manufacturer, material)
    near = min(rows, key=lambda r: abs(_f(r["dia_in"]) - dia_in))
    best = abs(_f(near["dia_in"]) - dia_in)
    if best > 0.0015:
        return None, "no %s reamer within 0.0015 in of %.4f (nearest %.4f)" % (manufacturer, dia_in, _f(near["dia_in"]))
    same = [r for r in rows if abs(_f(r["dia_in"]) - _f(near["dia_in"])) < 1e-6]
    note = "" if best <= 0.0003 else "nearest reamer %.4f in" % _f(near["dia_in"])
    same, fb = _first(same, material)
    note = _join(note, fb)
    def key(r):
        carbide = r["family"].startswith("F2")
        return (-_rate(r, material), -int(r["tier_rank"] or 0), 0 if carbide else 1, 0 if _f(r["flute_len_mm"]) / MM >= depth_in else 1, _f(r["oal_mm"]))
    same.sort(key=key)
    return copy.deepcopy(same[0]), note

# ---------------- XML ----------------
def _tecset(tool, material, purpose, cut, drilling_feed):
    ts = tool.find("tecsets/tecset")
    if ts is None or cut is None:
        return
    tb._setp(ts, "material", iso_letter(material)); tb._setp(ts, "purpose", purpose)
    tb._setp(ts, "cuttingSpeed", cut["vc"]); tb._setp(ts, "spindleSpeed", cut["rpm"])
    for k in ("planeFeedrate", "zFeedrate", "reducedFeedrate"):
        tb._setp(ts, k, cut["ipm"])
    if drilling_feed is not None:
        tb._setp(ts, "drillingFeedrate", drilling_feed)
    if "fz" in cut:
        tb._setp(ts, "feedratePerEdge", cut["fz"])

def build_xml(kind, row, ncnum, outpath, material=None):
    tpl = {"tap": "template_tap.xml", "reamer": "template_reamer.xml", "threadmill": "template_threadmill.xml"}[kind]
    tree = ET.parse(os.path.join(tb.HERE, tpl)); root = tree.getroot(); cont = root.find("container")
    cont.set("main-obj-name", str(ncnum))
    for k in ("srcURL", "srcGuid", "masterGuid", "files"):
        root.attrib.pop(k, None)
    tool = cont.find("tools/tool"); tool.set("name", row["designation"])
    tb._setp(tool, "comment", ("%s %s %s | grade %s" % (row["manufacturer"], row.get("family", ""), row.get("unit_system", ""), row.get("grade", ""))) if row.get("manufacturer", "Walter") != "Walter" else "%s %s" % (row.get("manufacturer", "Walter"), row.get("tier", "")))
    tb._setp(tool, "manufacturer", row.get("manufacturer", "Walter"))
    oal = _f(row.get("oal_mm")) / MM
    tb._setp(tool, "toolTotalLength", oal)
    z = int(_f(row.get("flutes"), 3)); tb._setp(tool, "cuttingEdges", z)
    if kind == "tap":
        dia = _f(row["dia_in"]); pitch = 1.0 / _f(row["tpi"]) if row.get("tpi") else _f(row.get("pitch_mm")) / MM
        tl = _f(row.get("thread_len_mm")) / MM
        tb._setp(tool, "toolDiameter", dia); tb._setp(tool, "toolShaftDiameter", _f(row.get("shank_dia_mm")) / MM or dia)
        tb._setp(tool, "cuttingLength", tl); tb._setp(tool, "taperHeight", tl); tb._setp(tool, "toolShaftChamferAbsPos", tl)
        tb._setp(tool, "pitch", pitch); tb._setp(tool, "minorThreadDiameter", dia - 1.0825 * pitch); tb._setp(tool, "tipDiameter", dia - 1.0825 * pitch)
        tt = "formTap" if row.get("form") == "forming" else ("spiralFlute" if "spiral" in row.get("title", "").lower() else "straightFlute")
        tb._setp(tool, "tapTipType", tt)
        cut = tap_cut(row, material) if material else None
        _tecset(tool, material, "Tapping", cut, pitch)
    elif kind == "reamer":
        dia = _f(row["dia_in"]); fl = _f(row.get("flute_len_mm")) / MM
        tb._setp(tool, "toolDiameter", dia); tb._setp(tool, "cuttingLength", fl); tb._setp(tool, "taperHeight", fl)
        cut = reamer_cut(row, material) if material else None
        _tecset(tool, material, "Reaming", cut, cut["ipr"] if cut else None)
    else:
        dc = _f(row["cutter_dia_in"]); tl = _f(row.get("thread_len_mm")) / MM
        th = row.get("_thread") or {}
        pitch = _f(row.get("pitch_mm")) / MM or th.get("pitch_in", 0.05)
        tb._setp(tool, "toolDiameter", dc); tb._setp(tool, "toolShaftDiameter", _f(row.get("shank_dia_mm")) / MM or dc)
        tb._setp(tool, "cuttingLength", tl); tb._setp(tool, "taperHeight", tl); tb._setp(tool, "toolShaftChamferAbsPos", tl)
        tb._setp(tool, "minorThreadDiameter", _f(row.get("min_thread_dia_mm")) / MM)
        tb._setp(tool, "minPitch", pitch); tb._setp(tool, "maxPitch", pitch)
        tb._setp(tool, "noOfThreadProfiles", max(1, int(tl / pitch)) if pitch else 1)
        cut = threadmill_cut(row, material) if material else None
        _tecset(tool, material, "Thread milling", cut, None)
    note = tb.cut_source(cut) if material else ""
    if note:                                       # borrowed or standard values: said in the tool comment as well
        tb._setp(tool, "comment", (tool.find("param[@name='comment']").get("value") or "") + " | " + note)
    shared = None
    for cp in tool.findall("coupling"):
        g = cp.find("param[@name='objGuid']")
        if g is not None:
            shared = g.get("value")
    for p in cont.iter("param"):
        if p.get("name") == "objGuid" and p.get("value") != shared:
            p.set("value", tb._guid())
    nct = cont.find("ncTools/ncTool")
    nct.set("ncNumber", str(ncnum)); nct.set("id", "M_%s" % ncnum); nct.set("name", "M_%s" % ncnum)
    tb._setp(nct, "comment", row["designation"]); tb._setp(nct, "gageLength", oal)
    if kind == "threadmill":
        # clearance length = catalog l4 (usable length below the shank) when printed, else the neck length, else the thread length
        l4 = _f(row.get("l4_mm")) / MM
        neck = _f(row.get("neck_len_mm")) / MM
        clr = l4 if l4 > tl else (neck if neck > tl else tl)
        if clr:
            tb._setp(nct, "clearanceLength", clr)
    for comp in nct.findall("components/component"):
        comp.set("name", row["designation"])
    for d in cont.findall("docObject"):
        cont.remove(d)
    tree.write(outpath, encoding="utf-8", xml_declaration=True)
    return outpath

def cut_for(row, kind, material):
    c = {"tap": tap_cut, "reamer": reamer_cut, "threadmill": threadmill_cut}[kind](row, material)
    if not c:
        return None
    return dict(rpm=c["rpm"], ipm=c["ipm"], sfm=c["vc"], ipr=c.get("ipr"), fz=c.get("fz"),
                **{k: c[k] for k in ("borrowed", "standard", "group", "wanted") if c.get(k)})
