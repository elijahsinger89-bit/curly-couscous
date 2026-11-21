# tool_builder.py - builds a hyperMILL tool from a library CSV row and attaches it to the document.
# Method: take an exported tool file (template), change its geometry, drop the docObject block, import it.
import os, re, uuid, csv, tempfile, math
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
MM = 25.4
PURPOSE_HEM = "Rough-HEM - usage 1"   # tecset purpose name used for high efficiency milling data (rename here if your tool database uses another name)
PURPOSE_SEMI = "Finish-Semi - usage 1"     # semi-finishing cutting data (rename to match your tool database)
PURPOSE_3D = "Finish-3D - usage 1"         # 3D profiling cutting data (rename to match your tool database)
ROUGH_AE_D = 0.75     # traditional roughing ("Rough - usage 1"), high-feed style: radial engagement ae = 0.75 x D
ROUGH_AP_D = 0.10     # and axial depth ap = 0.10 x D for square tools
ROUGH_AP_R = 0.30     # corner radius tools: ap = 0.30 x corner radius (GARR high-feed rule), chip load raised by axial chip thinning
ROUGH_MIN_R_IN = 0.015  # corner radius below this counts as square
ROUGH_ACTF_MAX = 2.5  # cap on the axial chip-thinning factor
ROUGH_FZ_FACTOR = 1.0 # extra multiplier on the high-feed roughing chip load (1.0 = standards only)
USE_EXTENSION = True   # head/tip drills are built as head + Extension (neck and flange); set False for a single-body tool
MAX_RPM = 12000.0     # spindle speed limit; speeds above it are cut back and the feed follows (set by part_wizard_step1 and batch_apply_strategy)
ORDERING_PARAM = ""    # name of the tool's Ordering code field in a tool export (from the tool_field_probe log); "" = not written yet
COMMON_NAME = True     # Common > Name = short description (".750 BR R.03 6FL L1.50"); False = "M_<number>" as before

import sys
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import tool_numbers    # numbering standard (M_ / T_ type codes); the scripts reload it with the other tool_library modules

def _guid():
    return str(uuid.uuid4())

def load_rows(name):
    with open(os.path.join(HERE, name), newline="", encoding="utf-8-sig") as fh:   # every table is UTF-8; Windows would read cp1252
        return list(csv.DictReader(fh))

def _f(x, d=0.0):
    try:
        return float(x)
    except Exception:
        return d

def _setp(el, name, value):
    for p in el.findall("param"):
        if p.get("name") == name:
            p.set("value", str(value))
            return
    ET.SubElement(el, "param", {"name": name, "value": str(value)})

def nc_code(type_code, dia_in, variant=1, copy=0):
    """M_ + 2-digit type + 4-digit diameter in thousandths of an inch + variant + copy (digits only, tool_numbers.mill_id)."""
    return tool_numbers.mill_id(type_code, dia_in, variant, copy)[2:]

def material_group(material):
    for r in load_rows("material_map.csv"):
        if r["hypermill_material"] == material:
            return r["walter_group"]
    return None

def material_note(material):
    """Limit printed with Walter cutting data for this material (material_map.csv, column note), or ''."""
    for r in load_rows("material_map.csv"):
        if r["hypermill_material"] == material:
            return (r.get("note") or "").strip()
    return ""

def vrr_feed_mm(vrr, dia_mm):
    """Feed per rev (mm) for feed chart number vrr at diameter dia_mm. Charts are linear in the chart number."""
    rows = load_rows("walter_vrr.csv")
    r30 = [r for r in rows if r["vrr"] == "30"][0]
    pts = sorted((float(k.split("_")[-1]), float(v)) for k, v in r30.items() if k.startswith("f_mm"))
    d = min(max(dia_mm, pts[0][0]), pts[-1][0])
    for (d0, f0), (d1, f1) in zip(pts, pts[1:]):
        if d0 <= d <= d1:
            f30 = f0 + (f1 - f0) * (d - d0) / (d1 - d0)
            break
    return f30 * vrr / 30.0

# hyperMILL material -> Kennametal workpiece group (Master Catalog 2018 Vol. 2, workpiece materials overview)
KENN_GROUP = {"P - Low Carbon Steel": "P0", "P - Medium Carbon Steel": "P2", "P - Alloy Steel": "P3", "P - Tool Steel": "P4", "P - Cast Steel": "P2",
              "M - Austenitic": "M1", "M - Martensitic": "P5", "M - Duplex": "M3", "M - PH": "P5",
              "S - Nickel Based": "S3", "S - Iron Based": "S1", "S - Cobalt Based": "S2", "S - Titanium": "S4",
              "K - Gray Cast Iron": "K1", "K - Ductile Iron": "K2", "K - Compacted Graphite Iron": "K2",
              "N - Aluminum": "N1", "N - Copper": "N4", "N - Brass": "N4", "N - Bronze": "N4",
              "H - Hardened Steel 45-55 HRC": "H2", "H - Chilled Cast Iron": "H2"}

def _kenn_series_match(series, designation):
    for tok in re.split(r"[,/]", series or ""):
        tok = tok.strip()
        if not tok:
            continue
        m = re.match(r"B\d+", tok)
        if not m:
            import fnmatch
            if fnmatch.fnmatch(designation, tok + "*"):
                return True
            continue
        pre = m.group(0)
        if not designation.startswith(pre):
            continue
        if len(pre) >= 4 or "_" not in tok:
            return True
        if designation[len(pre):len(pre) + 1].isdigit():
            return True
    return False

def kenn_drill_cut(row, material):
    grp = KENN_GROUP.get(material)
    if not grp:
        return None
    rows = [r for r in load_rows("kennametal_drill_cutting.csv") if r["grade"] == row.get("grade") and _kenn_series_match(r["series"], row["designation"])]
    if not rows:
        return None
    letter = grp[0]
    same = [r for r in rows if r["group"][0] == letter]
    if not same:
        return None
    n = int(grp[1:])
    best = min(same, key=lambda r: abs(int(r["group"][1:]) - n))
    dias = [float(x) for x in best["dia_in"].split(";")]
    lo = [float(x) for x in best["ipr_lo"].split(";")]; hi = [float(x) for x in best["ipr_hi"].split(";")]
    mid = [(a + b) / 2.0 for a, b in zip(lo, hi)]
    d = _f(row["dia_mm"]) / MM
    if d <= dias[0]:
        ipr = mid[0]
    elif d >= dias[-1]:
        ipr = mid[-1]
    else:
        ipr = mid[-1]
        for k in range(len(dias) - 1):
            if dias[k] <= d <= dias[k + 1]:
                t = (d - dias[k]) / (dias[k + 1] - dias[k]); ipr = mid[k] + t * (mid[k + 1] - mid[k]); break
    vc = _f(best["sfm_start"])
    rpm = vc * 12 / (3.14159265 * d)
    if rpm > MAX_RPM:
        vc *= MAX_RPM / rpm; rpm = MAX_RPM
    return dict(vc=vc, rpm=rpm, ipr=ipr, ipm=rpm * ipr, grp=best["group"], vrr="", group=best["group"], wanted=grp)

def drill_cut(row, material):
    """Returns dict(vc_sfm, rpm, ipr, ipm) or None. Walter: compendium data for this drill family, depth class and material. Kennametal: Master Catalog application data (SFM start value, mid of the IPR range)."""
    if row.get("manufacturer", "Walter") == "Kennametal":
        return kenn_drill_cut(row, material)
    if row.get("manufacturer") == "GARR":
        import garr_cut
        return garr_cut.drill_cut(row, material)
    grp = material_group(material)
    if not grp or row.get("manufacturer", "Walter") != "Walter":
        return None
    fam = row["family"].split()[0]
    depth = int(re.sub(r"\D", "", row["length_class"]) or 3)
    coolant = "internal" if row.get("coolant") == "through" else "external"
    c = [r for r in load_rows("walter_drill_cutting.csv") if r["family"] == fam and r["group"] == grp and r["coolant_supply"] == coolant]
    if not c:
        c = [r for r in load_rows("walter_drill_cutting.csv") if r["family"] == fam and r["group"] == grp]
    if not c:
        return None
    c.sort(key=lambda r: abs(int(r["depth_xD"]) - depth))
    c = c[0]
    dia_mm = _f(row["dia_mm"])
    vc = _f(c["vc_mpm"]) * 3.28084           # m/min -> SFM
    rpm = vc * 12 / (3.14159265 * dia_mm / MM)
    if rpm > MAX_RPM:
        vc *= MAX_RPM / rpm
        rpm = MAX_RPM
    ipr = vrr_feed_mm(_f(c["vrr"]), dia_mm) / MM
    return dict(vc=vc, rpm=rpm, ipr=ipr, ipm=rpm * ipr, grp=grp, vrr=c["vrr"])

def mill_feed_mm(cls, dia_mm, ae_mm):
    """Feed per tooth (mm) from the Walter feed table for class A, B or C: nearest tabulated diameter and radial depth."""
    t = [r for r in load_rows("walter_mill_feed.csv") if r["feed_class"] == cls]
    if not t:
        return None
    dias = sorted(set(float(r["dia_mm"]) for r in t))
    d = min(dias, key=lambda x: abs(x - dia_mm))
    ae_l = sorted(set(float(r["ae_mm"]) for r in t if float(r["dia_mm"]) == d))
    if not ae_l:
        return None
    ae = min(ae_l, key=lambda x: abs(x - ae_mm))
    return float([r for r in t if float(r["dia_mm"]) == d and float(r["ae_mm"]) == ae][0]["fz_mm"])

# family (or family:grade) -> application data page of the Solid End Milling catalog (inch; 1000 + page = Fall 2026 Innovations,
# 2000 + page = metric catalog, converted to SFM / IPT), or (page, title keyword) when the page prints several tables
EM_TABLE_PAGE = {"H1TE": 30, "H2TE": 43, "UCDE": 72, "UDDE": 2068, "HA3R": 75, "HA3A": 75, "HA4R": 79, "HA2L": 81,
                 "KOR5": 94, "KOR5:K600": 97, "HPRS": 105, "HPRS:KCPM15": (104, "HPRSS"), "MDRH": 104, "ABDE": 126, "ABDF": 126, "AADE": 128, "AADF": 128,
                 "GOPR": 172, "UEDE": 155, "UEBD": 155, "KOR6": 94, "KOR5:KCSM15A": 1169, "AMVM": 1188, "KHDA": (146, "KHDA"), "KMDA": (146, "KMDA"),
                 "ALCB": (130, "ALCB"), "ALCC": (130, "ALCC"), "ALSB": (131, "ALSB"), "EADE": (136, "EADE"),
                 "ALCR": (130, "ALCR"), "ALSR": (131, "ALSR"), "F1AA": 2127, "F2AA": 2128, "F3AA": 2128, "F3BA": 2129, "F3BS": 2099,
                 "F2AU": 2148, "F3AU": 2148, "UEBC": 2159, "UEBE": 2159}

def kenn_endmill_cut(row, material):
    """Kennametal Solid End Milling catalog application data (side milling table of the tool's family): SFM min/max and IPT by diameter."""
    grp = KENN_GROUP.get(material)
    page = EM_TABLE_PAGE.get("%s:%s" % (row["family"], row.get("grade", ""))) or EM_TABLE_PAGE.get(row["family"])
    if not grp or not page:
        return None
    kw = ""
    if isinstance(page, tuple):
        page, kw = page
    rows = [r for r in load_rows("kennametal_em_cutting.csv") if int(r["page"]) == page and kw in r["title"]]
    if not rows:
        return None
    toks = lambda r: set(g for g in re.split(r"[\s,/]+", r.get("grade") or "") if g)
    mine = [r for r in rows if row.get("grade") and row["grade"] in toks(r)]
    rows = mine or rows                            # a page printing one speed column per grade: the tool's own grade first
    first = rows[0]["title"]
    rows = [r for r in rows if r["title"] == first]
    # the table is printed for other grades only (e.g. KOR6 in KCSM15, table printed for KC643M): label it as borrowed
    printed = set(g for r in rows for g in toks(r))
    by = ("%s %s" % (row["family"], "/".join(sorted(printed)))) if printed and row.get("grade") and row["grade"] not in printed else ""
    same = [r for r in rows if r["group"][0] == grp[0]]
    if not same:
        return None
    n = int(grp[1:])
    best = min(same, key=lambda r: abs(int(r["group"][1:]) - n))
    dias = [float(x) for x in best["dia_in"].split(";")]; fzs = [float(x) for x in best["fz"].split(";")]
    d = _f(row["dia_mm"]) / MM
    if d <= dias[0]:
        fz = fzs[0]
    elif d >= dias[-1]:
        fz = fzs[-1]
    else:
        fz = fzs[-1]
        for k in range(len(dias) - 1):
            if dias[k] <= d <= dias[k + 1]:
                t = (d - dias[k]) / (dias[k + 1] - dias[k]); fz = fzs[k] + t * (fzs[k + 1] - fzs[k]); break
    vmin = _f(best["vmin"]); vmax = _f(best["vmax"]); mid = (vmin + vmax) / 2.0
    z = max(int(_f(row.get("flutes"), 3)), 1)
    flute_in = _f(row.get("flute_len_mm")) / MM
    def mk(sfm, f, ae, ap):
        rpm = sfm * 12 / (3.14159265 * d)
        if rpm > MAX_RPM:
            sfm *= MAX_RPM / rpm; rpm = MAX_RPM
        return dict(vc=sfm, rpm=rpm, fz=f, ipm=rpm * f * z, ae=ae, ap=ap, group=best["group"], wanted=grp, borrowed=by)
    ap_r = min(1.5 * d, flute_in) if flute_in else 1.5 * d
    res = {"Rough - usage 1": mk(mid, fz, 0.5 * d, ap_r),
           "Slotting - usage 1": mk(vmin, fz * 0.8, d, min(1.0 * d, flute_in) if flute_in else d),
           "Finish-2D-Radial - usage 1": mk(vmax, fz * 0.5, 0.1 * d, ap_r),
           "Finish-2D-Axial - usage 1": mk(vmax, fz * 0.5, 0.1 * d, 0.1 * d),
           PURPOSE_HEM: mk(mid * 1.4, fz * 1.67, 0.1 * d, min(2.0 * d, flute_in) if flute_in else 2.0 * d)}
    return res

# general purpose Walter families whose printed data is used, and labelled as borrowed, when a family prints none for the group
ALT_FAMILIES = ("MD340", "MC230", "MD177", "MC326", "ME232", "MD838", "MC500", "MC183", "MC187", "MC388", "MC268", "MD265")
# a family that prints a neighbouring group but not the material's own group uses its own neighbouring data first
# (General compendium cutting force table: N1 wrought Al not hardened, N2 hardened, N3 cast Al < 12% Si; N7, N8, N9 copper alloys)
NO_BORROW_GRADES = ("WIS10", "WDN20", "WP40", "WKM")      # ceramic, PCD, brazed carbide tips
OWN_NEAR_GROUP = {"N1": ("N2", "N3"), "N7": ("N8", "N9"), "N8": ("N9", "N7")}

def _misprint(r, allr):
    """A printed dynamic chip load more than 4 x both neighbouring material groups of the same table is taken as a misprint and
    not used (the compendium prints 0,90 for P7 at Lc = 5 x Dc in several tables, between 0,11 and 0,12)."""
    if not r.get("fz_mm"):
        return False
    same = {x["group"]: _f(x["fz_mm"]) for x in allr if x["page"] == r["page"] and x["families"] == r["families"]
            and x["grade"] == r["grade"] and x["ae_dc"] == r["ae_dc"] and x.get("fz_mm")}
    g = r["group"]; n = int(g[1:])
    nb = [same[k] for k in ("%s%d" % (g[0], n - 1), "%s%d" % (g[0], n + 1)) if same.get(k)]
    return bool(nb) and _f(r["fz_mm"]) > 4 * max(nb)

def endmill_cut(row, material):
    """Returns dict of purpose -> dict(vc, rpm, fz_in, ipm, ae_in, ap_in) for rough, slotting and finish. Walter compendium or Kennametal application data."""
    if row.get("manufacturer", "Walter") == "Kennametal":
        return kenn_endmill_cut(row, material)
    if row.get("manufacturer") == "GARR":
        import garr_cut
        return garr_cut.endmill_cut(row, material)
    grp = material_group(material)
    if not grp or row.get("manufacturer", "Walter") != "Walter":
        return None
    fam = row["family"].split()[0]
    # PCD, brazed, ceramic and inserted cutters use only their own printed data: solid carbide data is never borrowed for them
    own_only = fam.startswith(("MP", "F1", "M5460")) or (row.get("grade") or "") in NO_BORROW_GRADES
    allr = load_rows("walter_mill_cutting.csv")
    want = grp
    rows = [r for r in allr if grp == r["group"] and fam in r["families"].split()]
    src = ""                                       # family the numbers come from when they are not the tool's own
    if not rows and grp in OWN_NEAR_GROUP:         # the family prints the neighbouring group only (e.g. N3 but not N1): its own data first
        for g2 in OWN_NEAR_GROUP[grp]:
            rows = [r for r in allr if g2 == r["group"] and fam in r["families"].split()]
            if rows:
                grp = g2
                break
    if not rows and own_only:
        return None
    if not rows:                                   # family has no data for this material: use a general purpose Walter family that does
        if grp in ("N1", "N2", "N5", "N6", "N7"):  # milling data lists wrought and cast aluminum under N3 / N4; copper alloys under N8
            grp = "N3" if grp in ("N1", "N2", "N5", "N6") else "N8"
        for alt in ALT_FAMILIES:
            rows = [r for r in allr if grp == r["group"] and alt in r["families"].split()]
            if rows:
                src = alt
                break
    if not rows:
        return None
    dia_mm = _f(row["dia_mm"]); z = max(int(_f(row.get("flutes"), 3)), 1)
    def pick(label):
        c = [r for r in rows if r["ae_dc"] == label]
        return (c[0], src) if c else None
    dyn = [r for r in rows if r["ae_dc"].startswith("dyn") and not _misprint(r, allr)]
    res = {}
    spec = (("Rough - usage 1", "1/2", 0.5, 1.5), ("Slotting - usage 1", "1/1", 1.0, 1.0),
            ("Finish-2D-Radial - usage 1", "1/10", 0.1, 1.5), ("Finish-2D-Axial - usage 1", "1/10", 0.1, 0.1))
    def pick_alt(label):
        # the family prints no data for this engagement (for example dynamic-milling-only families): use the same engagement
        # from a general purpose Walter family for the material group. Dynamic chip loads are never used for full or half
        # engagement, they are only valid at the small engagement angle they are printed for.
        if own_only:
            return None
        for alt in ALT_FAMILIES:
            if alt == fam:
                continue
            c = [r for r in allr if grp == r["group"] and alt in r["families"].split() and r["ae_dc"] == label]
            if c:
                return (c[0], alt)
        return None
    for purpose, lab, aedc, apdc in spec:
        hit = pick(lab) or pick_alt(lab)
        r, by = hit if hit else (None, "")
        if r:
            vc = _f(r["vc_mpm"])
            fz = mill_feed_mm(r["feed_class"], dia_mm, aedc * dia_mm) if r["feed_class"] else None
        else:
            continue
        if not fz:
            continue
        sfm = vc * 3.28084
        rpm = sfm * 12 / (3.14159265 * dia_mm / MM)
        if rpm > MAX_RPM:
            sfm *= MAX_RPM / rpm
            rpm = MAX_RPM
        fz_in = fz / MM
        res[purpose] = dict(vc=sfm, rpm=rpm, fz=fz_in, ipm=rpm * fz_in * z, ae=aedc * dia_mm / MM, ap=apdc * dia_mm / MM,
                            borrowed=by, group=grp, wanted=want)
    # high efficiency milling: Walter dynamic data (engagement angle phis, feed fz) for the Lc/Dc class the tool can use
    flute_d = _f(row.get("flute_len_mm")) / dia_mm if dia_mm else 0
    best = None
    for r in dyn:
        m = re.search(r"([\d,.]+)\s*×", r["ae_dc"].replace("Lc=", ""))
        k = _f(m.group(1).replace(",", ".").split("–")[-1]) if m else 0
        if k and k <= flute_d + 0.01 and (best is None or k > best[0]):
            best = (k, r)
    if best is None and dyn:
        best = (1.0, dyn[0])
    if best:
        k, r = best
        phis = _f(r.get("phis"), 40.0); fz = _f(r["fz_mm"]); vc = _f(r["vc_mpm"])
        if fz and vc:
            sfm = vc * 3.28084
            rpm = sfm * 12 / (3.14159265 * dia_mm / MM)
            if rpm > MAX_RPM:
                sfm *= MAX_RPM / rpm; rpm = MAX_RPM
            ae = dia_mm / 2 * (1 - math.cos(math.radians(phis)))
            ap = min(k * dia_mm, _f(row.get("flute_len_mm")) or k * dia_mm)
            res[PURPOSE_HEM] = dict(vc=sfm, rpm=rpm, fz=fz / MM, ipm=rpm * fz / MM * z, ae=ae / MM, ap=ap / MM, borrowed=src, group=grp, wanted=want)
    elif "Finish-2D-Radial - usage 1" in res:
        # Walter prints no dynamic (HEM) data for this material group: use its radial finishing speed and feed at 0.1 x Dc
        # engagement and up to 2 x Dc depth, limited to the flute length
        f = res["Finish-2D-Radial - usage 1"]
        ap = min(2 * dia_mm, _f(row.get("flute_len_mm")) or 2 * dia_mm)
        res[PURPOSE_HEM] = dict(vc=f["vc"], rpm=f["rpm"], fz=f["fz"], ipm=f["ipm"], ae=0.1 * dia_mm / MM, ap=ap / MM, borrowed=f.get("borrowed", ""),
                                group=f.get("group", grp), wanted=want)
    return res or None

def build_chamfer_xml(row, ncnum, outpath, material=None):
    """Chamfer mill (hyperMILL type chamferedcutter). row: dia_mm = large diameter Da, tip_mm = tip diameter Dc, half_angle."""
    tree = ET.parse(os.path.join(HERE, "template_chamfer.xml"))
    root = tree.getroot(); cont = root.find("container")
    cont.set("main-obj-name", str(ncnum))
    for k in ("srcURL", "srcGuid", "masterGuid", "files"):
        root.attrib.pop(k, None)
    da = _f(row["dia_mm"]) / MM; dc = _f(row["tip_mm"]) / MM
    half = float(row.get("half_angle") or 45)
    oal = _f(row["oal_mm"]) / MM
    lc = (da - dc) / 2 / math.tan(math.radians(half))
    tool = cont.find("tools/tool")
    tool.set("name", row["designation"])
    if row.get("manufacturer", "Walter") != "Walter":
        _setp(tool, "comment", "%s %s | grade %s | EDP %s | %s catalog" % (row["manufacturer"], row.get("family", ""), row.get("grade", ""), row.get("edp", ""), row.get("unit_system", "")))
    else:
        _setp(tool, "comment", "%s %s" % (row["manufacturer"], row.get("tier", "")))
    _setp(tool, "manufacturer", row.get("manufacturer", "Walter"))
    _setp(tool, "toolDiameter", da); _setp(tool, "tipDiameter", dc)
    _setp(tool, "chamferAngle", half); _setp(tool, "nominalDiameter", (da + dc) / 2)
    _setp(tool, "toolTotalLength", oal); _setp(tool, "taperHeight", oal)
    _setp(tool, "cuttingLength", lc)
    _setp(tool, "cuttingEdges", int(_f(row.get("flutes"), 4)))
    _setp(tool, "toolShaftDiameter", _f(row["shank_dia_mm"]) / MM or da)
    # cutting data: Walter finishing data for the job material, taken as for an end mill of the large diameter
    em = dict(row); em["dia_mm"] = row["dia_mm"]; em["family"] = row.get("family", "MC501 Advance")
    cut = endmill_cut(em, material) if material else None
    c = (cut or {}).get("Finish-2D-Radial - usage 1")
    base = tool.find("tecsets/tecset")
    if c and base is not None:
        _setp(base, "cuttingSpeed", c["vc"]); _setp(base, "spindleSpeed", c["rpm"]); _setp(base, "feedratePerEdge", c["fz"])
        _setp(base, "planeFeedrate", c["ipm"]); _setp(base, "reducedFeedrate", c["ipm"] * 0.7); _setp(base, "zFeedrate", c["ipm"] * 0.5)
        note = cut_source(c)
        if note:
            _setp(tool, "comment", (tool.find("param[@name='comment']").get("value") or "") + " | " + note)
    shared = None
    for cp in tool.findall("coupling"):
        shared = cp.find("param[@name='objGuid']").get("value")
    for p in cont.iter("param"):
        if p.get("name") == "objGuid" and p.get("value") != shared:
            p.set("value", _guid())
    nct = cont.find("ncTools/ncTool")
    nct.set("ncNumber", str(ncnum)); nct.set("id", "M_%s" % ncnum); nct.set("name", "M_%s" % ncnum)
    _setp(nct, "comment", row["designation"]); _setp(nct, "gageLength", oal); _setp(nct, "clearanceLength", oal)
    for comp in nct.findall("components/component"):
        comp.set("name", row["designation"])
    for d in cont.findall("docObject"):
        cont.remove(d)
    tree.write(outpath, encoding="utf-8", xml_declaration=True)
    return outpath

def build_facemill_xml(row, ncnum, outpath, material=None):
    """Inserted face mill / shell mill as a radiusMill (same structure as hyperMILL shell mills): outer diameter, insert depth of cut,
    collar and body diameter. Walter publishes no cutting data for inserted cutters, so only the base cutting data is written."""
    import math as _m
    tree = ET.parse(os.path.join(HERE, "template_endmill.xml"))
    root = tree.getroot(); cont = root.find("container")
    cont.set("main-obj-name", str(ncnum))
    for k in ("srcURL", "srcGuid", "masterGuid", "files"):
        if k in root.attrib:
            del root.attrib[k]
    dia = _f(row["dia_mm"]) / MM
    lc = _f(row["lc_mm"]) / MM
    oal = _f(row["oal_mm"]) / MM
    head = _f(row.get("head_mm")) / MM or oal
    d1 = _f(row["d1_mm"]) / MM
    iface = (row.get("interface") or "B")[:1]
    body = d1 if iface in ("A", "T", "W", "Z") and d1 else dia * 0.84     # shank or body diameter below the head
    tipd = min(dia * 0.965, dia - 0.02)
    if body >= tipd:
        tipd = body
    taper = head * 0.56                                                       # same proportion as the hyperMILL shell mill sample
    chl = 0.1
    tool = cont.find("tools/tool")
    tool.set("name", row["designation"])
    _setp(tool, "objGuid", _guid())
    _setp(tool, "comment", "Walter %s%s" % (row.get("family", ""), (" | insert %s | grades %s" % (row.get("insert_type", ""), row["insert_grades"])) if row.get("insert_grades") else ""))
    _setp(tool, "manufacturer", "Walter")
    _setp(tool, "toolDiameter", dia); _setp(tool, "toolTotalLength", oal)
    _setp(tool, "cuttingLength", lc); _setp(tool, "cuttingEdges", int(_f(row.get("z"), 4)))
    _setp(tool, "toolShaftDiameter", body)
    _setp(tool, "toolShaftChamferLength", chl)
    _setp(tool, "taperHeight", taper); _setp(tool, "toolShaftChamferAbsPos", taper + chl)
    _setp(tool, "collar", 1); _setp(tool, "tipDiameter", tipd)
    if tipd > body:
        _setp(tool, "toolShaftChamferAngle", _m.degrees(_m.atan(((tipd - body) / 2.0) / chl)))
    _setp(tool, "cornerRadius", _f(row.get("corner_r_mm"), 0.8) / MM)
    ts = tool.find("tecsets")
    for t in list(ts):
        if t.find("param[@name='material']") is not None:
            ts.remove(t)
    shared = None
    for c in tool.findall("coupling"):
        shared = c.find("param[@name='objGuid']").get("value")
    for p in cont.iter("param"):
        if p.get("name") == "objGuid" and p.get("value") != shared:
            p.set("value", _guid())
    nct = cont.find("ncTools/ncTool")
    nct.set("ncNumber", str(ncnum)); nct.set("id", "M_%s" % ncnum); nct.set("name", "M_%s" % ncnum)
    _setp(nct, "comment", row["designation"]); _setp(nct, "gageLength", oal)
    _setp(nct, "clearanceLength", taper + chl)
    for comp in nct.findall("components/component"):
        comp.set("name", row["designation"])
    cp = nct.find("cuttingProfiles")
    for c in list(cp):
        if c.get("material"):
            cp.remove(c)
    for d in cont.findall("docObject"):
        cont.remove(d)
    mats = cont.find("materials")
    if mats is not None:
        for m in list(mats):
            mats.remove(m)
    tree.write(outpath, encoding="utf-8", xml_declaration=True)
    return outpath

def build_boring_xml(row, ncnum, outpath):
    """Boring tool as a hyperMILL boringBar (structure from an exported hyperMILL boring bar): bore range as min/max diameter,
    body diameter d1 as the shaft, projection l4 as total length. Walter publishes no cutting data for boring tools."""
    import math as _m
    tree = ET.parse(os.path.join(HERE, "template_boringbar.xml"))
    root = tree.getroot(); cont = root.find("container")
    cont.set("main-obj-name", str(ncnum))
    for k in ("srcURL", "srcGuid", "masterGuid", "files"):
        if k in root.attrib:
            del root.attrib[k]
    dmin = _f(row["dc_min_mm"]) / MM; dmax = _f(row["dc_max_mm"]) / MM
    bore = _f(row.get("bore_dia_mm")) / MM or dmin
    shaft = _f(row["d1_mm"]) / MM
    total = _f(row["l4_mm"]) / MM
    lc = _f(row.get("lc_mm")) / MM
    neck = lc if lc and lc < total else total * 0.6
    chl = min(0.1875, max(total - neck - 0.01, 0.02))
    tool = cont.find("tools/tool")
    tool.set("name", row["designation"])
    _setp(tool, "objGuid", _guid())
    _setp(tool, "comment", "Walter %s" % row.get("family", ""))
    _setp(tool, "manufacturer", "Walter")
    _setp(tool, "toolDiameter", bore); _setp(tool, "toolTotalLength", total)
    _setp(tool, "cuttingEdges", 2 if (row.get("family") in ("B5460", "B5560") or ".Z2" in row["designation"]) else 1)
    _setp(tool, "toolShaftDiameter", shaft)
    _setp(tool, "taperHeight", neck)
    _setp(tool, "toolShaftChamferLength", chl); _setp(tool, "toolShaftChamferAbsPos", neck + chl)
    if shaft != bore:
        _setp(tool, "toolShaftChamferAngle", _m.degrees(_m.atan((abs(shaft - bore) / 2.0) / chl)))
    _setp(tool, "noTipLength", total)
    _setp(tool, "minDrillDiameter", dmin); _setp(tool, "maxDrillDiameter", dmax)
    shared = None
    for c in tool.findall("coupling"):
        shared = c.find("param[@name='objGuid']").get("value")
    for p in cont.iter("param"):
        if p.get("name") == "objGuid" and p.get("value") != shared:
            p.set("value", _guid())
    nct = cont.find("ncTools/ncTool")
    nct.set("ncNumber", str(ncnum)); nct.set("id", "M_%s" % ncnum); nct.set("name", "M_%s" % ncnum)
    _setp(nct, "comment", row["designation"]); _setp(nct, "gageLength", total)
    _setp(nct, "clearanceLength", neck); _setp(nct, "presetDiameter", bore)
    for comp in nct.findall("components/component"):
        comp.set("name", row["designation"])
    for d in cont.findall("docObject"):
        cont.remove(d)
    tree.write(outpath, encoding="utf-8", xml_declaration=True)
    return outpath

def build_xdrill_ext_xml(row, ncnum, outpath):
    """Head or tip drill as a hyperMILL drilTool (the replaceable head only) plus an Extension holding the neck and flange
    (structure from a user-built D5150 tool). Returns None when the geometry does not fit, so the caller falls back to the single-body tool."""
    import math as _m
    dmax = _f(row.get("dia_max_in")) or _f(row["dia_in"]); dmin = _f(row.get("dia_min_in")) or dmax
    nom = _f(row["dia_in"]); lc = _f(row["flute_len_in"]); total = _f(row["oal_in"])
    d4 = _f(row.get("d4_in")) or _f(row.get("shank_dia_in"))
    cone = _f(row.get("point_angle")) or 140
    head = round(0.565 * nom, 4)
    neck_r = dmin / 2.0 - 0.0005
    y1 = lc - 0.006
    y2 = y1 + (d4 / 2.0 - neck_r)
    ytop = total - head
    if d4 <= dmin or y2 > ytop - 0.01 or y1 <= 0:
        return None
    tree = ET.parse(os.path.join(HERE, "template_xdrill_ext.xml"))
    root = tree.getroot(); cont = root.find("container")
    cont.set("main-obj-name", str(ncnum))
    for k in ("srcURL", "srcGuid", "masterGuid", "files"):
        if k in root.attrib:
            del root.attrib[k]
    ext = cont.find("extensions/extension")
    pts = [(neck_r, 0.0), (neck_r, y1), (d4 / 2.0, y2), (d4 / 2.0, ytop), (0.0, ytop)]
    cont2d = ext.find("geometry/cont2D")
    for e in list(cont2d):
        cont2d.remove(e)
    ET.SubElement(cont2d, "elem2D", {"type": "line", "sx": "0", "sy": "0", "ex": repr(pts[0][0]), "ey": "0"})
    for x, y in pts[1:]:
        ET.SubElement(cont2d, "elem2D", {"type": "line", "ex": repr(x), "ey": repr(y)})
    for mp in ext.findall("geometry/mountingPosition"):
        if mp.get("location") == "machineSide":
            _setp(mp, "origin", "0,%r,0" % ytop)
    tool = cont.find("tools/tool")
    tool.set("name", row["designation"])
    _setp(tool, "objGuid", _guid()); _setp(tool, "comment", "Walter %s" % row.get("family", "")); _setp(tool, "manufacturer", "Walter")
    _setp(tool, "toolDiameter", dmax); _setp(tool, "toolTotalLength", head); _setp(tool, "taperHeight", head)
    _setp(tool, "coneAngle", cone)
    tip = (dmax / 2.0) / _m.tan(_m.radians(cone / 2.0)) if cone < 179 else 0.0
    _setp(tool, "noTipLength", max(head - tip, 0))
    shared = None
    for c in tool.findall("coupling"):
        shared = c.find("param[@name='objGuid']").get("value")
    for p in cont.iter("param"):
        if p.get("name") == "objGuid" and p.get("value") != shared:
            p.set("value", _guid())
    nct = cont.find("ncTools/ncTool")
    nct.set("ncNumber", str(ncnum)); nct.set("id", "M_%s" % ncnum); nct.set("name", "M_%s" % ncnum)
    _setp(nct, "comment", row["designation"]); _setp(nct, "gageLength", total); _setp(nct, "clearanceLength", round(y1 + head + 0.004, 4))
    for comp in nct.findall("components/component"):
        if comp.get("type") == "tool":
            comp.set("name", row["designation"]); comp.set("reach", repr(head))
    for d in cont.findall("docObject"):
        cont.remove(d)
    tree.write(outpath, encoding="utf-8", xml_declaration=True)
    return outpath

def build_xdrill_xml(row, ncnum, outpath, material=None):
    """Exchangeable-head / exchangeable-tip / insert drill as one hyperMILL drilTool (structure from a user-built D5150 tool, no extension):
    toolDiameter = Dc max, taperHeight = Lc, total length = l4, shaft diameter = flange d4 (else d1) with a collar chamfer after Lc.
    cuttingLength = estimated head length (0.565 x Dc, from the D5150-03-11.50 example). Walter publishes no cutting data."""
    import math as _m
    tree = ET.parse(os.path.join(HERE, "template_xdrill.xml"))
    root = tree.getroot(); cont = root.find("container")
    cont.set("main-obj-name", str(ncnum))
    for k in ("srcURL", "srcGuid", "masterGuid", "files"):
        if k in root.attrib:
            del root.attrib[k]
    dia = (_f(row.get("dia_max_in")) if row.get("manufacturer", "Walter") == "Walter" else 0) or _f(row["dia_in"])
    nom = _f(row["dia_in"])
    lc = _f(row["flute_len_in"]); total = _f(row["oal_in"])
    d4 = _f(row.get("d4_in")) or _f(row.get("shank_dia_in")) or dia
    cone = _f(row.get("point_angle")) or 140
    chl = max(min(0.476 * d4, total - lc - 0.01), 0.02)
    tool = cont.find("tools/tool")
    tool.set("name", row["designation"])
    _setp(tool, "objGuid", _guid())
    _setp(tool, "comment", ("%s %s" % (row.get("manufacturer", "Walter"), row.get("family", ""))) + ((" | grade %s | EDP %s" % (row.get("grade", ""), row.get("edp", ""))) if row.get("edp") else ""))
    _setp(tool, "manufacturer", row.get("manufacturer", "Walter"))
    _setp(tool, "toolDiameter", dia); _setp(tool, "toolTotalLength", total)
    _setp(tool, "cuttingEdges", 1 if row.get("family") in ("D4120", "D3120", "D4170", "B3212", "B3213", "B3214") else 2)
    _setp(tool, "cuttingLength", round(0.565 * nom, 4))
    _setp(tool, "taperHeight", lc)
    _setp(tool, "toolShaftDiameter", d4)
    _setp(tool, "toolShaftChamferLength", chl); _setp(tool, "toolShaftChamferAbsPos", lc + chl)
    if d4 > dia:
        _setp(tool, "toolShaftChamferAngle", _m.degrees(_m.atan(((d4 - dia) / 2.0) / chl)))
    _setp(tool, "coneAngle", cone)
    tip = (dia / 2.0) / _m.tan(_m.radians(cone / 2.0)) if cone < 179 else 0.0
    _setp(tool, "noTipLength", max(total - tip, 0))
    cut = drill_cut(row, material) if (material and row.get("manufacturer", "Walter") == "Kennametal") else None
    ts0 = tool.find("tecsets/tecset")
    if cut and ts0 is not None:
        _setp(ts0, "cuttingSpeed", cut["vc"]); _setp(ts0, "spindleSpeed", cut["rpm"]); _setp(ts0, "drillingFeedrate", cut["ipr"])
        for k in ("planeFeedrate", "zFeedrate", "reducedFeedrate"):
            _setp(ts0, k, cut["ipm"])
        _setp(tool, "comment", "%s | cutting data for %s (group %s)" % (tool.find("param[@name='comment']").get("value"), material, cut["grp"]))
    shared = None
    for c in tool.findall("coupling"):
        shared = c.find("param[@name='objGuid']").get("value")
    for p in cont.iter("param"):
        if p.get("name") == "objGuid" and p.get("value") != shared:
            p.set("value", _guid())
    nct = cont.find("ncTools/ncTool")
    nct.set("ncNumber", str(ncnum)); nct.set("id", "M_%s" % ncnum); nct.set("name", "M_%s" % ncnum)
    l4 = _f(row.get("l4_mm")) / MM            # catalog l4 (usable length) when printed; else the flute length
    _setp(nct, "comment", row["designation"]); _setp(nct, "gageLength", total); _setp(nct, "clearanceLength", l4 if lc < l4 <= total + 1e-6 else lc)
    for comp in nct.findall("components/component"):
        comp.set("name", row["designation"])
    for d in cont.findall("docObject"):
        cont.remove(d)
    tree.write(outpath, encoding="utf-8", xml_declaration=True)
    return outpath

def build_slot_xml(row, ncnum, outpath):
    """Disc / T-slot cutter as a hyperMILL Tslotcutter (structure from user-built T-slot cutters with sharp, chamfer and radius corners).
    Modular MG heads: head only (total length l1, stem d1). Indexable M4575 T-slot cutters: shank d1, neck d2, reach l4, overall l1."""
    import math as _m
    tree = ET.parse(os.path.join(HERE, "template_tslot.xml"))
    root = tree.getroot(); cont = root.find("container")
    cont.set("main-obj-name", str(ncnum))
    for k in ("srcURL", "srcGuid", "masterGuid", "files"):
        if k in root.attrib:
            del root.attrib[k]
    dc = _f(row["dia_mm"]) / MM; sb = _f(row["sb_mm"]) / MM
    kind = row.get("kind")
    if kind == "tslot":
        shaft = _f(row["d1_mm"]) / MM; neck = _f(row["d2_mm"]) / MM or shaft
        total = _f(row["l1_mm"]) / MM; reach = _f(row["l4_mm"]) / MM
        if neck >= shaft:
            neck = shaft * 0.95
        chl = max(3.0 * (shaft - neck) / 2.0, 0.04)
    else:
        shaft = neck = _f(row["d1_mm"]) / MM
        total = _f(row["l1_mm"]) / MM; reach = total; chl = 0.04
    tool = cont.find("tools/tool")
    tool.set("name", row["designation"])
    _setp(tool, "objGuid", _guid()); _setp(tool, "comment", "Walter %s" % row.get("family", "")); _setp(tool, "manufacturer", "Walter")
    _setp(tool, "toolTotalLength", total); _setp(tool, "cuttingEdges", int(_f(row.get("z"), 3)))
    _setp(tool, "cuttingLength", sb); _setp(tool, "discHeight", sb)
    _setp(tool, "toolShaftDiameter", shaft); _setp(tool, "toolDiameter", dc); _setp(tool, "tipDiameter", neck)
    _setp(tool, "taperHeight", reach); _setp(tool, "toolShaftChamferLength", chl); _setp(tool, "toolShaftChamferAbsPos", reach + chl)
    if shaft > neck:
        _setp(tool, "toolShaftChamferAngle", _m.degrees(_m.atan(((shaft - neck) / 2.0) / chl)))
    r = _f(row.get("r_mm")) / MM
    if kind == "chamfer":
        h = _f(row.get("tmax_mm")) / MM or sb / 2.0
        for side in ("upper", "lower"):
            _setp(tool, side + "CornerType", "chamfer"); _setp(tool, side + "ChamferAngle", 45); _setp(tool, side + "ChamferHeight", h)
    elif r > 0:
        for side in ("upper", "lower"):
            _setp(tool, side + "CornerType", "radius"); _setp(tool, side + "CornerRadius", r)
    shared = None
    for c in tool.findall("coupling"):
        shared = c.find("param[@name='objGuid']").get("value")
    for p in cont.iter("param"):
        if p.get("name") == "objGuid" and p.get("value") != shared:
            p.set("value", _guid())
    nct = cont.find("ncTools/ncTool")
    nct.set("ncNumber", str(ncnum)); nct.set("id", "M_%s" % ncnum); nct.set("name", "M_%s" % ncnum)
    _setp(nct, "comment", row["designation"]); _setp(nct, "gageLength", total); _setp(nct, "clearanceLength", total)
    for rp in nct.findall("referencePoints/referencePoint"):
        rp.set("diameter", repr(dc))
        if rp.get("type") == "discTop":
            rp.set("offset", repr(sb))
    for comp in nct.findall("components/component"):
        comp.set("name", row["designation"])
    for d in cont.findall("docObject"):
        cont.remove(d)
    tree.write(outpath, encoding="utf-8", xml_declaration=True)
    return outpath

def build_xml(kind, row, ncnum, outpath, material=None, purposes=None):
    """kind = 'drill', 'endmill' or 'chamfer'. Writes an import file, returns its path."""
    if kind == "chamfer":
        return build_chamfer_xml(row, ncnum, outpath, material)
    if kind == "facemill":
        return build_facemill_xml(row, ncnum, outpath, material)
    if kind == "boring":
        return build_boring_xml(row, ncnum, outpath)
    if kind == "slot":
        return build_slot_xml(row, ncnum, outpath)
    if kind == "xdrill":
        if USE_EXTENSION and row.get("family") in ("D5150", "D4140", "D5142", "D4240"):
            p = build_xdrill_ext_xml(row, ncnum, outpath)
            if p:
                return p
        return build_xdrill_xml(row, ncnum, outpath, material)
    if kind in ("tap", "reamer", "threadmill"):
        import hole_tools
        return hole_tools.build_xml(kind, row, ncnum, outpath, material)
    if kind == "profilemill":
        kind = "endmill"
    spot = kind == "spotdrill"
    if spot:
        kind = "drill"                 # spot drills use the drill tool structure with their own point angle and no cutting data
    tpl = os.path.join(HERE, "template_%s.xml" % kind)
    tree = ET.parse(tpl)
    root = tree.getroot()
    cont = root.find("container")
    cont.set("main-obj-name", str(ncnum))
    for k in ("srcURL", "srcGuid", "masterGuid", "files"):
        if k in root.attrib:
            del root.attrib[k]
    dia = _f(row["dia_in"]) or _f(row["dia_mm"]) / MM
    oal = _f(row["oal_mm"]) / MM
    shank = _f(row["shank_dia_mm"]) / MM or dia
    flute = _f(row["flute_len_mm"]) / MM
    tool = cont.find("tools/tool")
    tool.set("name", row["designation"])
    _setp(tool, "objGuid", _guid())
    _setp(tool, "comment", "%s %s" % (row["manufacturer"], row.get("tier", "")))
    _setp(tool, "toolDiameter", dia)
    _setp(tool, "manufacturer", row.get("manufacturer", "Walter"))
    _setp(tool, "toolTotalLength", oal)
    _setp(tool, "toolShaftDiameter", shank)
    if kind == "drill":
        lc = _f(row["depth_max_mm"]) / MM or flute
        _setp(tool, "cuttingLength", lc)
        _setp(tool, "taperHeight", flute or lc)
        _setp(tool, "toolShaftChamferAbsPos", (flute or lc) + 0.04)
        _setp(tool, "noTipLength", max(oal - dia * 0.1, 0))
        _setp(tool, "coneAngle", _f(row.get("point_angle")) or 140)
        _setp(tool, "cuttingEdges", 2)
    else:
        _setp(tool, "cuttingLength", flute)
        # reduced neck: catalog reach l3 (length below the shank) and neck diameter d2
        reach = _f(row.get("reach_mm")) / MM
        neck = _f(row.get("neck_dia_mm")) / MM
        necked = bool(reach and neck and reach > flute + 1e-6 and neck < shank)
        low = reach if necked else flute
        tip_d = neck if necked else dia
        _setp(tool, "taperHeight", low)
        _setp(tool, "toolShaftChamferAbsPos", low + 0.04)
        _setp(tool, "tipDiameter", tip_d)
        if necked:
            _setp(tool, "collar", 1)   # shank collar must be on for the neck to apply
        if shank > tip_d and (necked or row.get("shape") not in ("Ball", "Square")):
            import math as _m
            _setp(tool, "toolShaftChamferAngle", _m.degrees(_m.atan(((shank - tip_d) / 2.0) / 0.04)))
        shape = row.get("shape")
        if shape in ("Ball", "Square"):
            # real ball and flat end mill types: no corner radius parameter (types copied from tools built in hyperMILL)
            tool.set("type", "ballMill" if shape == "Ball" else "endMill")
            for p in list(tool.findall("param")):
                if p.get("name") in ("cornerRadius", "coreDiameter", "coreHeight"):
                    tool.remove(p)
            if necked:
                _setp(tool, "collar", 1); _setp(tool, "tipDiameter", tip_d)
            else:
                _setp(tool, "collar", 0); _setp(tool, "tipDiameter", 0)
            if shape == "Square":
                _setp(tool, "chamfered", 0); _setp(tool, "chamferHeight", 0)
        else:
            _setp(tool, "cornerRadius", _f(row.get("corner_r_mm")) / MM)
        _setp(tool, "cuttingEdges", int(_f(row.get("flutes"), 3)))
    # keep only the base (no material) cutting data
    ts = tool.find("tecsets")
    skeleton = None
    for t in list(ts):
        if t.find("param[@name='material']") is not None:
            if skeleton is None:
                import copy as _c
                skeleton = _c.deepcopy(t)
            ts.remove(t)
    matguid = None
    em_cut = endmill_cut(row, material) if (material and kind == "endmill") else None
    if em_cut and purposes:
        em_cut = {k: v for k, v in em_cut.items() if k in purposes} or em_cut
    elif em_cut:                       # callers that pick no sets (part wizards, hole jobs) keep the original five catalog sets
        em_cut = {k: v for k, v in em_cut.items() if k not in (PURPOSE_SEMI, PURPOSE_3D)}
    if em_cut and skeleton is not None:
        import copy as _c
        first_mat = skeleton.find("param[@name='material']").get("value")
        for t in list(tool.find("tecsets")):
            pass
        for purpose, c in em_cut.items():
            e = _c.deepcopy(skeleton)
            _setp(e, "material", material); _setp(e, "purpose", purpose)
            _setp(e, "cuttingSpeed", c["vc"]); _setp(e, "spindleSpeed", c["rpm"])
            _setp(e, "feedratePerEdge", c["fz"])
            for k in ("planeFeedrate",):
                _setp(e, k, c["ipm"])
            _setp(e, "reducedFeedrate", c["ipm"] * 0.7)
            _setp(e, "zFeedrate", c["ipm"] * 0.5)
            _setp(e, "cuttingWidth", c["ae"]); _setp(e, "cuttingLength", c["ap"])
            ts.append(e)
        matguid = True
    note = cut_source(em_cut) if em_cut else ""
    if note:                                       # borrowed numbers are said in the tool comment as well
        _setp(tool, "comment", "%s %s | %s" % (row["manufacturer"], row.get("tier", ""), note))
    if material and skeleton is not None and kind == "drill" and not spot:
        cut = drill_cut(row, material)
        if cut:
            _setp(skeleton, "material", material)
            _setp(skeleton, "purpose", "Drill")
            _setp(skeleton, "cuttingSpeed", cut["vc"])
            _setp(skeleton, "spindleSpeed", cut["rpm"])
            _setp(skeleton, "drillingFeedrate", cut["ipr"])
            for k in ("planeFeedrate", "zFeedrate", "reducedFeedrate"):
                _setp(skeleton, k, cut["ipm"])
            ts.append(skeleton)
            matguid = True
    shared = None
    for c in tool.findall("coupling"):
        shared = c.find("param[@name='objGuid']").get("value")
    for p in cont.iter("param"):
        if p.get("name") == "objGuid" and p.get("value") != shared:
            p.set("value", _guid())
    nct = cont.find("ncTools/ncTool")
    nct.set("ncNumber", str(ncnum)); nct.set("id", "M_%s" % ncnum); nct.set("name", "M_%s" % ncnum)
    _setp(nct, "comment", row["designation"])
    _setp(nct, "gageLength", oal)
    _r = _f(row.get("reach_mm")) / MM
    _nk = _f(row.get("neck_dia_mm")) / MM
    if kind != "drill" and _r and _r > flute + 1e-6 and (not _nk or _nk < shank):
        # clearance = reach + shaft chamfer (matches hyperMILL exports for ball, flat and bullnose); Walter l4 effective length when no neck diameter is listed
        _setp(nct, "clearanceLength", _r + 0.04)
    else:
        _setp(nct, "clearanceLength", flute or oal)
    for comp in nct.findall("components/component"):
        comp.set("name", row["designation"])
    cp = nct.find("cuttingProfiles")
    keep = None
    for c in list(cp):
        if c.get("material"):
            if keep is None:
                import copy as _c
                keep = _c.deepcopy(c)
            cp.remove(c)
    if matguid and keep is not None:
        import copy as _c
        purposes = list(em_cut.keys()) if em_cut else ["Drill"]
        for pu in purposes:
            k2 = _c.deepcopy(keep); k2.set("material", material); k2.set("purpose", pu)
            cp.append(k2)
    for d in cont.findall("docObject"):
        cont.remove(d)
    # remove material list and unused entries are harmless; clear to keep file small
    mats = cont.find("materials")
    if mats is not None:
        first = None
        for m in list(mats):
            if first is None:
                import copy as _c
                first = _c.deepcopy(m)
            mats.remove(m)
        if matguid and first is not None:
            first.set("name", material)
            mats.append(first)
    tree.write(outpath, encoding="utf-8", xml_declaration=True)
    return outpath

def tool_by_name(ts, name):
    for t in ts.GetTools():
        if t.Name == name:
            return t
    return None

def order_code(row):
    """What is ordered: the EDP / Material Number (Kennametal, GARR), else the designation (Walter tables have no EDP)."""
    return str(row.get("edp") or "").strip() or str(row.get("designation") or "").strip()

def finish_fields(path, type_code, dia_in, row):
    """Tool page fields the standard asks for, on a built tool file: Common > Name = short description (COMMON_NAME),
    Tool > Ordering code = order_code(row) (once ORDERING_PARAM is known). Returns the description written, or ''."""
    try:
        tree = ET.parse(path)
    except Exception:
        return ""
    root = tree.getroot()
    desc = ""
    nct = root.find(".//ncTools/ncTool")
    if COMMON_NAME and nct is not None:
        mm = lambda k: _f(row.get(k)) / MM if _f(row.get(k)) else 0.0
        cr = _f(row.get("corner_r_in")) or mm("corner_r_mm")
        loc = _f(row.get("flute_len_in")) or mm("flute_len_mm")
        try:
            desc = tool_numbers.describe(type_code, dia_in, corner_r=cr, flutes=row.get("flutes"), loc=loc, thread=row.get("thread"))
            nct.set("name", desc)
        except Exception:
            desc = ""
    tool = root.find(".//tools/tool")
    if ORDERING_PARAM and tool is not None and order_code(row):
        _setp(tool, ORDERING_PARAM, order_code(row))
    tree.write(path, encoding="utf-8", xml_declaration=True)
    return desc

class JobTools:
    """Hands out M_ numbers for this job only. Nothing is read from earlier jobs."""
    def __init__(self):
        self.seen = {}      # (type, dia thousandths) -> list of designations
    def number(self, type_code, dia_in, designation):
        key = (type_code, int(round(dia_in * 1000)))
        lst = self.seen.setdefault(key, [])
        if designation not in lst:
            lst.append(designation)
        return int(nc_code(type_code, dia_in, variant=lst.index(designation) + 1, copy=0))

# ---------------- user cutting-data sets ----------------
# hyperMILL's Python API cannot add a cutting-data set to a tool already in the document (probe_tecset 1-4: the document tool
# never changes; om.tdb has no constructor for a technology). So every tool built here comes in with these extra sets, for the
# job material, as copies of the tool's own catalog set (or its invariant base set, with the material added, when there is no
# catalog data). Every set carries the material: a set without one is the invariant set, and a tool has only one. Without a
# job material no user sets are added. Edit their values in hyperMILL's tool dialog. Empty tuple = none.
USER_SETS = ("User - 1", "User - 2", "User - 3")

def add_user_sets(path, material):
    """Adds USER_SETS (tecset + NC tool cutting profile) to a built tool file. Returns the number added."""
    if not USER_SETS:
        return 0
    try:
        tree = ET.parse(path)
    except Exception:
        return 0
    root = tree.getroot()
    tool = root.find(".//tools/tool")
    ts = tool.find("tecsets") if tool is not None else None
    if ts is None or not list(ts):
        return 0
    sets = list(ts)
    def mat(e):
        q = e.find("param[@name='material']")
        return q.get("value") if q is not None else None
    src = ([e for e in sets if material and mat(e) == material] or [e for e in sets if mat(e)] or sets)[0]
    use_mat = material or mat(src) or ""
    if not use_mat:
        return 0                                   # a set without a material is the invariant set, and a tool has only one
    have = set((mat(e), (e.find("param[@name='purpose']").get("value") if e.find("param[@name='purpose']") is not None else None)) for e in sets)
    import copy as _c
    added = []
    for name in USER_SETS:
        if (use_mat, name) in have:
            continue
        e = _c.deepcopy(src)
        _setp(e, "material", use_mat)
        _setp(e, "purpose", name)
        for g in e.iter("param"):
            if g.get("name") == "objGuid":
                g.set("value", _guid())
        ts.append(e)
        added.append(name)
    if not added:
        return 0
    nct = root.find(".//ncTools/ncTool")
    cp = nct.find("cuttingProfiles") if nct is not None else None
    if cp is not None:
        typ = src.get("type", "milling")
        for name in added:
            c = ET.SubElement(cp, "cuttingProfile", {"type": typ, "material": use_mat, "purpose": name})
            ET.SubElement(c, "param", {"name": "enabled", "value": "1"})
    if True:
        mats = root.find(".//materials")
        if mats is None:
            cont = root.find("container")
            mats = ET.Element("materials")
            if cont is not None:                   # same place as in the end mill template: after <formulas>, else first
                kids = list(cont)
                pos = next((i + 1 for i, k in enumerate(kids) if k.tag == "formulas"), 0)
                cont.insert(pos, mats)
        if not any(m.get("name") == use_mat for m in mats.findall("material")):
            m = ET.SubElement(mats, "material", {"type": "legacy", "name": use_mat})
            ET.SubElement(m, "param", {"name": "objGuid", "value": _guid()})
            ET.SubElement(m, "param", {"name": "chippingClass", "value": "unknown"})
    tree.write(path, encoding="utf-8", xml_declaration=True)
    return len(added)

def get_or_create(model, kind, row, type_code, jt, outdir=None, material=None, purposes=None, force_new=False):
    ts = model.ToolSet
    existing = None if force_new else tool_by_name(ts, row["designation"])
    if existing is not None:
        return existing, "existing"
    type_code = tool_numbers.workbook_code(kind, type_code, row)    # catalog type_code -> the standard's code
    dia = _f(row["dia_in"]) or _f(row["dia_mm"]) / MM
    try:
        num = jt.number(type_code, dia, row["designation"])
    except ValueError as e:                  # more than 9 tools of one type and diameter, or a size the code cannot hold
        return None, "no tool number: %s" % e
    used = set(int(t.Number) for t in ts.GetTools())
    while num in used:                       # number already taken by another tool in this document: next variant
        jt.seen[(type_code, int(round(dia * 1000)))].append(row["designation"] + "#")
        num += 10
        if (num // 10) % 10 == 0:            # variant went past 9 (it would run into the diameter digits)
            return None, "no free tool number for type %02d, diameter %.4f in (variants 1-9 all used)" % (type_code, dia)
    outdir = outdir or os.path.join(tempfile.gettempdir(), "tool_builder")
    os.makedirs(outdir, exist_ok=True)
    p = build_xml(kind, row, num, os.path.join(outdir, "%s.omtdx" % row["designation"].replace("/", "_")), material, purposes)
    finish_fields(p, type_code, dia, row)
    add_user_sets(p, material)
    t = ts.ImportTool(p)
    if t is None:
        return None, "import returned None"
    if t.Name != row["designation"]:
        ts.Rename(t.UUID, row["designation"])
    return t, "created M_%s" % num


# ---------------- semi-finishing and 3D profiling sets ----------------
# The catalogs print roughing / slotting / finishing data only. These two sets are derived from the tool's own printed data
# (semi-finishing from the catalog's roughing data, before traditional roughing is set to large ae / small ap below):
#   semi-finishing: roughing speed, 80 percent of the roughing chip load, ae 0.10 x D, roughing ap
#   3D profiling:   finishing speed and chip load, ae (stepover) and ap 0.05 x D
_endmill_cut_catalog = endmill_cut

def _src(c):
    """Where a derived set's numbers come from (same as the set it is derived from)."""
    return {k: c[k] for k in ("borrowed", "group", "wanted", "standard") if k in c}

def endmill_cut(row, material):
    res = _endmill_cut_catalog(row, material)
    if not res:
        return res
    d = _f(row.get("dia_in")) or _f(row.get("dia_mm")) / MM
    z = max(int(_f(row.get("flutes"), 3) or 3), 1)
    rough = res.get("Rough - usage 1") or res.get(PURPOSE_HEM)
    fin = res.get("Finish-2D-Radial - usage 1") or rough
    if rough and PURPOSE_SEMI not in res:
        fz = rough["fz"] * 0.8
        res[PURPOSE_SEMI] = dict(_src(rough), vc=rough["vc"], rpm=rough["rpm"], fz=fz, ipm=rough["rpm"] * fz * z, ae=0.10 * d, ap=rough["ap"])
    if fin and PURPOSE_3D not in res:
        res[PURPOSE_3D] = dict(_src(fin), vc=fin["vc"], rpm=fin["rpm"], fz=fin["fz"], ipm=fin["rpm"] * fin["fz"] * z, ae=0.05 * d, ap=0.05 * d)
    # traditional roughing = high-feed style: large ae, small ap. Speed and chip load from the catalog's full-engagement
    # (slotting) data, which is printed for heavy radial engagement. High-feed tools keep their own printed data.
    text = " ".join(str(row.get(k, "")) for k in ("family", "series", "title", "description", "shape")).lower()
    full = res.get("Slotting - usage 1") or res.get("Rough - usage 1")
    if full and "high feed" not in text and "highfeed" not in text and "high-feed" not in text:
        flute = _f(row.get("flute_len_mm")) / MM
        cr = _f(row.get("corner_r_mm")) / MM if row.get("shape") == "Radiused" else 0.0
        if cr >= ROUGH_MIN_R_IN:
            # corner radius tool: axial depth ROUGH_AP_R x corner radius (GARR high-feed rule), chip load raised by the axial chip
            # thinning of the radius: Fz = hex / sqrt(2 ap/r - (ap/r)^2)  (round insert / corner radius, ap < r)
            ap = ROUGH_AP_R * cr
            q = ap / cr
            actf = min(ROUGH_ACTF_MAX, 1.0 / math.sqrt(max(1e-6, 2 * q - q * q)))
        else:
            ap = ROUGH_AP_D * d                      # square / small corner: no axial thinning, ap 0.10 x D
            actf = 1.0
        if flute:
            ap = min(ap, flute)
        fz = full["fz"] * actf * ROUGH_FZ_FACTOR
        res["Rough - usage 1"] = dict(_src(full), vc=full["vc"], rpm=full["rpm"], fz=fz, ipm=full["rpm"] * fz * z, ae=ROUGH_AE_D * d, ap=ap)
    return res


# ---------------- where the numbers come from ----------------
SET_NAMES = {"Rough - usage 1": "roughing", "Slotting - usage 1": "slotting", "Finish-2D-Radial - usage 1": "finishing",
             "Finish-2D-Axial - usage 1": "floor finishing", "Rough-HEM - usage 1": "HEM", "Finish-Semi - usage 1": "semi-finishing",
             "Finish-3D - usage 1": "3D finishing"}

def cut_source(cut):
    """Plain words on where cutting data comes from when it is not the tool's own printed data, else ''.
    cut is one set (dict with rpm/ipm) or a purpose -> set dict (end mills)."""
    if not cut:
        return ""
    sets = [cut] if "rpm" in cut else [c for c in cut.values() if isinstance(c, dict)]
    out = []
    by = sorted(set(c.get("borrowed") for c in sets if c.get("borrowed")))
    if by:
        if all(c.get("borrowed") for c in sets):
            what = "cutting data"
        else:                                      # name the sets that are borrowed
            names = []
            for k, c in cut.items():
                if isinstance(c, dict) and c.get("borrowed"):
                    nm = SET_NAMES.get(k, k)
                    if nm not in names:
                        names.append(nm)
            what = ", ".join(names) + " data"
        out.append("%s borrowed from %s, check before running" % (what, "/".join(by)))
    std = sorted(set(c.get("standard") for c in sets if c.get("standard")))
    for t in std:
        out.append(t)
    g = sorted(set((c.get("wanted"), c.get("group")) for c in sets if c.get("wanted") and c.get("group") and c["wanted"] != c["group"] and not c.get("borrowed")))
    for w, h in g:
        out.append("group %s data used (catalog prints no %s for this family)" % (h, w))
    return "; ".join(out)
