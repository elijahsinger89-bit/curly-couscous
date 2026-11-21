# tool_lookup.py - picks the best library tool for a request and builds it in the document.
# Rule: first choice only (the catalog rates the tool 2 for the material's ISO group; rated-1 tools are offered only when no rated-2 tool
# exists at the size, and the note says NOT FIRST CHOICE), then highest tier (Supreme, Advance, Perform), then a tool with cutting data
# for the job material, then the shortest tool that is long enough.
import tool_builder as tb

MANUFACTURERS = {"Walter": {"drills": "walter_drills.csv", "endmills": "walter_endmills.csv", "facemills": "walter_facemills.csv", "spotdrills": "walter_spotdrills.csv", "boring": "walter_boring.csv", "xdrills": "walter_xdrills.csv", "shoulder": "walter_shoulder.csv", "hfcopy": "walter_hfcopy.csv", "chamfer_ins": "walter_chamfer_ins.csv", "profile": "walter_profile.csv", "slot": "walter_slot.csv"},
                 "Kennametal": {"spotdrills": "kennametal_spotdrills.csv", "drills": "kennametal_drills.csv", "endmills": "kennametal_endmills.csv", "xdrills": "kennametal_xdrills.csv"},
                 "GARR": {"drills": "garr_drills.csv", "spotdrills": "garr_spotdrills.csv", "endmills": "garr_endmills.csv"}}
MM = 25.4

UNIT_PREF = "inch"       # Kennametal publishes separate inch and metric catalogs (column unit_system). Tools from the preferred system sort first.
GRADE_FALLBACK = {"K600": "N", "KD1410": "N"}   # Kennametal families with no ISO rating table: aluminium grades only

def unit_of(row):
    return row.get("unit_system") or "metric"

def _unit_rank(r):
    return 0 if unit_of(r) == UNIT_PREF else 1

TIER_FILTER = None      # set to a set of tier names (for example {"Supreme"}) to limit every selection to that grade

def _rows(manufacturer, group):
    rows = tb.load_rows(MANUFACTURERS[manufacturer][group])
    if TIER_FILTER:
        rows = [r for r in rows if (r.get("tier") or "") in TIER_FILTER]
    return rows


# Walter GPS recommended families for roughing/finishing solid carbide cutters, per ISO group (in Walter's order).
# P, M, S, K from GPS exports (ISO-STEEL, IS0_Stainless, iso_s, iso_K). N and H from GPS screenshots (partial lists).
FAMILIES = {
    "P": "MD133 MD177 MD173 MC326 MC726 MC230 MC233 MC111 MC122 MC213 MC324 MC716 ME232 MC341 MD344 MD340 MC377 MC388 MA230 MA373 MA375 MA377 MC331 MC333 F1678 F1675 F1682",
    "M": "MD133 MD177 MD173 MC326 MC726 MC230 MC233 MC111 MC122 MC213 MC324 MC716 MC341 ME232 MD344 MD340 MC251 MD377 MC377 MA230 MA373 MA375 MA377 MC331 MC333",
    "S": "MD133 MD177 MD173 MC326 MC726 MC230 MC233 MC122 MC213 MC716 ME232 MD344 MD340 MC251 MD377 MC377 MA230 MA373 MA375 MA377 MC331 MC333",
    "K": "MD133 MC326 MC726 MC230 MC233 MC122 MC213 MC324 MC716 MD344 ME232 MD340 MA230 MC331 MC333 F1678 F1675 F1682",
    "N": "ME232 MD266 MC267 MB266 MA263 MA267 MC331 MC333 MC166 MC268 MD265 MC467 MP170 MP160 MP470 MP270 MP271 MP260",
    "H": "MC388 MC281",
}
FAMILIES = {k: v.split() for k, v in FAMILIES.items()}

def _fit_rated(rows, material):
    """Manufacturers without a Walter-style family list (Kennametal): rank by the catalog's own ISO rating (2 = first choice, 1 = suitable)."""
    letter = str(material)[:1].upper()
    col = "iso_" + letter
    def rt(r):
        try: v = int(r.get(col) or 0)
        except Exception: v = 0
        if v == 0 and GRADE_FALLBACK.get(r.get("grade")) == letter: v = 1
        return v
    rows = [r for r in rows if rt(r) >= 1]
    for r in rows: r["_rating"] = rt(r)
    return rows

def _material_fit(rows, material):
    """Only Walter-recommended families for the material's ISO group. Aluminium (N) is narrowed further to cutters rated ISO N 2,
    else rated N with 3 or fewer flutes. Returns [] when Walter lists no family for the group that has this diameter."""
    letter = str(material)[:1].upper()
    fam = FAMILIES.get(letter)
    if fam:
        rows = [r for r in rows if r["designation"][:5] in fam]
    if letter != "N":
        order = {f: i for i, f in enumerate(fam or [])}
        return sorted(rows, key=lambda r: order.get(r["designation"][:5], 99)) if rows else rows
    def n(r):
        try: return int(r.get("iso_N") or 0)
        except Exception: return 0
    def fl(r):
        try: return int(r.get("flutes") or 0)
        except Exception: return 0
    a = [r for r in rows if n(r) >= 2]
    if a: return a
    b = [r for r in rows if n(r) >= 1 and 0 < fl(r) <= 3]
    if b: return b
    return [r for r in rows if 0 < fl(r) <= 3]

def _prefer_first(rows, col):
    """First choice = the catalog rates the tool 2 (primary) for the material's ISO group. Returns (rows, note): the rating-2 rows when any exist,
    else all rows with a note saying the tool is only rated suitable (1)."""
    if not col or not rows:
        return rows, ""
    top = [r for r in rows if int(r.get(col) or 0) >= 2]
    if top:
        return top, ""
    return rows, "NOT FIRST CHOICE: catalog rates it suitable (1), not primary (2), for ISO %s" % col[-1]

def _letter_col(material):
    return "iso_" + str(material)[:1].upper() if str(material)[:1].upper() in "PMKNSH" and str(material) else None

def _add(note, extra):
    return (note + " | " + extra) if (note and extra) else (note or extra)

def select_drill(dia_in, min_depth_in, material, manufacturer="Walter", tol_in=0.002, through=True):
    """Returns (row, note). note is '' for an exact diameter or a short text for an approximate match."""
    rows = [r for r in _rows(manufacturer, "drills") if r["type"] == "Carbide drill" and not r["thread"] and r["dia_in"]]
    rows = [r for r in rows if int(r.get(_letter_col(material) or "", 0) or 0) >= 1] if _letter_col(material) else rows
    if not rows:
        return None, "%s lists no carbide drill rated for %s at this level" % (manufacturer, material)
    def d(r): return float(r["dia_in"])
    exact = [r for r in rows if abs(d(r) - dia_in) <= tol_in]
    note = ""
    if not exact:
        near = min(rows, key=lambda r: abs(d(r) - dia_in))
        exact = [r for r in rows if abs(d(r) - d(near)) < 1e-6]
        note = "no %.4f in drill; nearest is %.4f in" % (dia_in, d(near))
    long_enough = [r for r in exact if tb._f(r["depth_max_mm"]) / MM >= min_depth_in]
    if not long_enough:
        return None, "no %.4f in drill reaches %.3f in" % (dia_in, min_depth_in)
    long_enough, fb = _prefer_first(long_enough, _letter_col(material))
    note = _add(note, fb)
    def key(r):
        has = tb.drill_cut(r, material) is not None
        cool = (r["coolant"] == "through") == through
        return (-int(r["tier_rank"] or 0), 0 if has else 1, 0 if cool else 1, tb._f(r["depth_max_mm"]))
    if manufacturer != "Walter":
        letter = "iso_" + str(material)[:1].upper()
        def kk(r):
            try: v = int(r.get(letter) or 0)
            except Exception: v = 0
            return (round(abs(float(r["dia_in"]) - dia_in) / 0.0005), _unit_rank(r), -v, 0 if (r["coolant"] == "through") == through else 1, tb._f(r["depth_max_mm"]))
        long_enough.sort(key=kk)
    else:
        long_enough.sort(key=key)
    return long_enough[0], note

KIND = {"flat": ("10", "Square"), "radius": ("11", "Radiused"), "ball": ("12", "Ball")}

FIRST_CHOICE_DIA_OFF = 0.08    # a first-choice end mill may differ from the requested diameter by up to 8 percent before a rated-1 tool of the exact size is used

def select_endmill(dia_in, min_flute_in, kind, material, manufacturer="Walter", tol_in=0.003, min_reach_in=0.0):
    """First choice only: searches the tools rated 2 for the material first (nearest diameter, flute, reach); only when none of them
    fits does it search the tools rated 1, and then the note says NOT FIRST CHOICE. Returns (row, note)."""
    code, shape = KIND[kind]
    rows = [r for r in _rows(manufacturer, "endmills") if r["type_code"] == code and r["shape"] == shape and r["quality"] != "unverified" and r["flute_len_mm"] and r["dia_in"]]
    rows = _fit_rated(rows, material)      # catalog ISO rating for the material (2 = first choice, 1 = suitable), same rule for every manufacturer
    if not rows:
        return None, "%s lists no recommended %s end mill for %s" % (manufacturer, kind, material)
    def d(r): return float(r["dia_in"])
    def search(pool, max_off=None):
        exact = [r for r in pool if abs(d(r) - dia_in) <= tol_in]
        note = ""
        if not exact:
            near = min(pool, key=lambda r: abs(d(r) - dia_in))
            if max_off is not None and abs(d(near) - dia_in) > max_off:
                return None, "no first-choice size near %.4f in" % dia_in
            exact = [r for r in pool if abs(d(r) - d(near)) < 1e-6]
            note = "no %.4f in %s end mill; nearest is %.4f in" % (dia_in, kind, d(near))
        ok = [r for r in exact if tb._f(r["flute_len_mm"]) / MM >= min_flute_in]
        if not ok:
            return None, "no %.4f in %s end mill has %.3f in of flute" % (dia_in, kind, min_flute_in)
        if min_reach_in:
            ok2 = [r for r in ok if (tb._f(r.get("reach_mm")) or tb._f(r["flute_len_mm"])) / MM >= min_reach_in]
            if not ok2:
                return None, "no %.4f in %s end mill reaches %.3f in" % (dia_in, kind, min_reach_in)
            ok = ok2
        def key(r):
            has = tb.endmill_cut(r, material) is not None
            return (-int(r["tier_rank"] or 0), 0 if has else 1, tb._f(r["flute_len_mm"]))
        if manufacturer != "Walter":
            ok.sort(key=lambda r: (_unit_rank(r), tb._f(r["flute_len_mm"])))
        else:
            ok.sort(key=key)
        return ok[0], note
    top = [r for r in rows if r["_rating"] >= 2]
    if top:
        r, note = search(top, FIRST_CHOICE_DIA_OFF * dia_in + tol_in)
        if r is not None:
            return r, note
    r, note = search(rows)
    if r is not None and r["_rating"] < 2:
        note = _add(note, "NOT FIRST CHOICE: catalog rates it suitable (1), not primary (2), for ISO %s" % str(material)[:1].upper())
    return r, note


def closest_endmill(dia_in, want_flute_in, kind, material, manufacturer="Walter", tol_in=0.003, min_reach_in=0.0):
    """Used when select_endmill finds nothing: the closest tool of the right diameter with the longest flute (and reach) that does exist.
    Returns (row, note) or (None, msg)."""
    code, shape = KIND[kind]
    rows = [r for r in _rows(manufacturer, "endmills") if r["type_code"] == code and r["shape"] == shape and r["quality"] != "unverified" and r["flute_len_mm"] and r["dia_in"] and abs(float(r["dia_in"]) - dia_in) <= tol_in]
    rows = _fit_rated(rows, material) if rows else rows
    if not rows:
        return None, "no %.4f in %s end mill in this grade" % (dia_in, kind)
    def fl(r): return tb._f(r["flute_len_mm"]) / MM
    def rc(r): return (tb._f(r.get("reach_mm")) or tb._f(r["flute_len_mm"])) / MM
    def key(r):
        return (-fl(r) if fl(r) < want_flute_in else (fl(r) - want_flute_in), -(min(rc(r), min_reach_in) if min_reach_in else 0), 0 if tb.endmill_cut(r, material) is not None else 1)
    rows.sort(key=key)
    return rows[0], ""

def describe_endmill(row, dia_in):
    fl = tb._f(row["flute_len_mm"]) / MM
    s = "flute %.3f in (%.1fxD)" % (fl, fl / dia_in)
    oal = tb._f(row.get("oal_mm"))
    if oal:
        s += ", overall %.3f in" % (oal / MM)
    rc = tb._f(row.get("reach_mm"))
    if rc:
        s += ", reach below shank %.3f in (%.1fxD)" % (rc / MM, rc / MM / dia_in)
    return s

ISO_COL = {"P": "iso_P", "M": "iso_M", "K": "iso_K", "N": "iso_N", "S": "iso_S", "H": "iso_H"}

def select_facemill(dia_in, ap_in, material, manufacturer="Walter", tol_in=0.2, mount="shell", group="facemills"):
    """Inserted face mill from Walter's face milling cutter tables. Needs Walter's rating for the material's ISO group (CC or C),
    a diameter at least dia_in (within tol_in smaller is accepted), and an insert depth of cut of at least ap_in.
    Picks the best rated series, then the smallest sufficient diameter, then the most cutting edges. mount = 'shell' or 'shank'."""
    col = ISO_COL.get(str(material)[:1].upper())
    rows = [r for r in tb.load_rows(MANUFACTURERS[manufacturer][group]) if r["dia_in"]]
    if col:
        rows = [r for r in rows if int(r[col] or 0) >= 1]
    if not rows:
        return None, "Walter lists no face mill for %s" % material
    want = ("B",) if mount == "shell" else ("A", "T", "W", "Z")
    m = [r for r in rows if r["interface"][:1] in want] or rows
    big = [r for r in m if float(r["dia_in"]) >= dia_in - tol_in]
    if not big:
        r = max(m, key=lambda r: float(r["dia_in"]))
        return r, "largest Walter face mill is %.3f in" % float(r["dia_in"])
    deep = [r for r in big if float(r["lc_mm"] or 0) / MM >= ap_in - 1e-6]
    note = ""
    if not deep:
        deep = big; note = "no cutter reaches %.3f in depth of cut; deepest offered" % ap_in
    deep, fb = _prefer_first(deep, col)
    note = _add(note, fb)
    def key(r):
        return (-int(r[col] or 0) if col else 0, r.get("tier") == "PCD", round(abs(float(r["dia_in"]) - dia_in), 2), -int(r["flutes"] or 0), float(r["lc_mm"] or 0))
    deep.sort(key=key)
    r = deep[0]
    if abs(float(r["dia_in"]) - dia_in) > 1e-3 and float(r["dia_in"]) < dia_in:
        note = (note + " | " if note else "") + "nearest smaller diameter %.3f in" % float(r["dia_in"])
    return r, note

def select_spotdrill(dia_in, angle, material, manufacturer="Walter"):
    """Walter NC spot drill (A1174 carbide, A1114 / A1115 HSS) with the requested point angle (90 or 120), rated for the material's
    ISO group. Exact diameter first, else the nearest larger, else the largest. Returns (row, note)."""
    col = ISO_COL.get(str(material)[:1].upper())
    rows = [r for r in _rows(manufacturer, "spotdrills") if int(float(r["point_angle"])) == int(angle)]
    if col:
        rows = [r for r in rows if int(r[col] or 0) >= 1]
    if not rows:
        return None, "no %s %d degree NC spot drill is rated for %s" % (manufacturer, angle, material)
    def d(r): return float(r["dia_in"])
    best = min(rows, key=lambda r: (abs(d(r) - dia_in) > 0.002, d(r) < dia_in, abs(d(r) - dia_in)))
    if manufacturer != "Walter":
        near = [r for r in rows if abs(d(r) - d(best)) < 0.002]
        pref = [r for r in near if unit_of(r) == UNIT_PREF]
        rows = (pref or near)
    if abs(d(best) - dia_in) <= 0.002:
        near = [r for r in rows if abs(d(r) - dia_in) <= 0.002]
    else:
        near = [r for r in rows if abs(d(r) - d(best)) < 1e-6]
    near, fb = _prefer_first(near, col)
    same = [r for r in near if r["family"] in ("A1174", "A1174C", "A1114", "A1115", "K1161XPL", "K1161")] or near
    same.sort(key=lambda r: (-int(r["tier_rank"] or 0), -int(r[col] or 0) if col else 0, float(r["oal_mm"])))
    r = same[0]
    note = "" if abs(d(r) - dia_in) <= 0.002 else "no %.4f in spot drill; nearest is %.4f in" % (dia_in, d(r))
    return r, _add(note, fb)

BORING_MOUNT_ORDER = {"N": 0, "C": 1, "T": 2}      # cylindrical shank, Capto, ScrewFit

def select_boring(bore_in, depth_in, material, manufacturer="Walter"):
    """Walter complete boring tool whose bore range contains bore_in, rated for the material's ISO group.
    Prefers the best rating, then a cylindrical shank, then the tightest range, then the shortest tool that reaches depth_in.
    Usable depth is the catalog Lc where listed, else 60 percent of the projection l4 (approximation). Returns (row, note)."""
    col = ISO_COL.get(str(material)[:1].upper())
    rows = [r for r in _rows(manufacturer, "boring")]
    if col:
        rows = [r for r in rows if int(r[col] or 0) >= 1]
    if not rows:
        return None, "Walter lists no boring tool for %s" % material
    D = bore_in * MM
    fit = [r for r in rows if float(r["dc_min_mm"]) - 1e-6 <= D <= float(r["dc_max_mm"]) + 1e-6]
    if not fit:
        near = min(rows, key=lambda r: min(abs(float(r["dc_min_mm"]) - D), abs(float(r["dc_max_mm"]) - D)))
        return None, "no Walter boring tool covers %.2f mm; nearest range is %.0f-%.0f mm" % (D, float(near["dc_min_mm"]), float(near["dc_max_mm"]))
    def reach(r):
        return (float(r["lc_mm"]) if r["lc_mm"] else float(r["l4_mm"]) * 0.6) / MM
    note = ""
    deep = [r for r in fit if reach(r) >= depth_in - 1e-6]
    if not deep:
        deep = fit; note = "no boring tool reaches %.3f in; deepest offered" % depth_in
    deep, fb = _prefer_first(deep, col)
    note = _add(note, fb)
    def mount(r):
        ch = r["designation"].split("-")[-2][:1] if "-" in r["designation"] else ""
        if "." in r["designation"] and "-" not in r["designation"][:6]:
            ch = r["designation"].split(".")[1][:1]
        return BORING_MOUNT_ORDER.get(ch, 3)
    deep.sort(key=lambda r: (-(int(r[col] or 0) if col else 0), mount(r), float(r["dc_max_mm"]) - float(r["dc_min_mm"]), reach(r)))
    r = dict(deep[0])
    r["bore_dia_mm"] = D
    r["dia_in"] = bore_in; r["dia_mm"] = D
    if not r["lc_mm"]:
        note = (note + " | " if note else "") + "bore depth capability is estimated"
    return r, note

def select_chamfer(hole_dia_in, width_in, material, manufacturer="Walter"):
    """Walter 90 degree solid carbide chamfer mill (MC501, DIN 6535 HA shank) for chamfering a hole edge.
    Large diameter Da must reach hole + 2 x width; tip diameter Dc must be smaller than the hole. Smallest Da that fits.
    Returns (row, note); row has dia_mm = Da, tip_mm = Dc, half_angle = 45."""
    import re
    rows = []
    for r in _rows(manufacturer, "endmills"):
        m = re.match(r"^MC501-(\d+\.\d)A\d", r["designation"])
        if r["type_code"] == "13" and m and r["tier"]:
            rr = dict(r); da = float(m.group(1))
            rr["tip_mm"] = r["dia_mm"]; rr["dia_mm"] = str(da); rr["dia_in"] = str(da / MM); rr["half_angle"] = "45"
            rows.append(rr)
    if TIER_FILTER is not None:
        rows = [r for r in rows if r.get("tier", "") in TIER_FILTER]
    col = ISO_COL.get(str(material)[:1].upper())
    rated = [r for r in rows if col and int(float(r.get(col) or 0)) >= 1]
    note = ""
    if col and rows and not rated:
        note = "no MC501 is rated for %s; used unrated" % material
    rows = rated or rows
    if not rows:
        return None, "no MC501 chamfer mill at this performance level"
    need = hole_dia_in + 2 * width_in
    fit = [r for r in rows if float(r["dia_mm"]) / MM >= need and float(r["tip_mm"]) / MM < hole_dia_in * 0.9]
    if not fit:
        fit = [r for r in rows if float(r["tip_mm"]) / MM < hole_dia_in * 0.9] or rows
        fit.sort(key=lambda r: -float(r["dia_mm"]))
        return fit[0], _add(note, "no MC501 reaches %.3f in across the chamfer; largest that fits the hole" % need)
    fit.sort(key=lambda r: float(r["dia_mm"]))
    return fit[0], note

def get_tool(model, jt, request, material, manufacturer="Walter"):
    """request = dict(kind='drill'|'flat'|'radius'|'ball', dia_in=..., depth_in=...). Returns (tool, message)."""
    k = request["kind"]
    if k == "drill":
        row, note = select_drill(request["dia_in"], request.get("depth_in", 0), material, manufacturer)
        kind, code = "drill", 50
    else:
        row, note = select_endmill(request["dia_in"], request.get("depth_in", 0), k, material, manufacturer)
        kind, code = "endmill", int(row["type_code"]) if row else 11
    if row is None:
        return None, note
    tool, msg = tb.get_or_create(model, kind, row, code, jt, material=material)
    return tool, (row["designation"] + " " + row.get("tier", "") + " | " + msg + (" | " + note if note else ""))

def cut_for(row, kind, material):
    """Cutting data for a selected row: dict(rpm, ipm, ipr or fz) or None."""
    if kind == "drill":
        c = tb.drill_cut(row, material)
        return None if not c else dict(_src(c), rpm=c["rpm"], ipm=c["ipm"], ipr=c["ipr"], sfm=c["vc"])
    c = tb.endmill_cut(row, material)
    if not c:
        return None
    r = c.get("Rough - usage 1") or list(c.values())[0]
    return dict(_src(r), rpm=r["rpm"], ipm=r["ipm"], fz=r["fz"], sfm=r["vc"])

def _src(c):
    """Where the numbers come from (tool_builder.cut_source reads these keys)."""
    return {k: c[k] for k in ("borrowed", "standard", "group", "wanted") if c.get(k)}

def build(model, jt, row, kind, material, purposes=None, force_new=False):
    """Builds (or finds) the tool for a selected row. Returns (tool, message)."""
    if kind in ("tap", "reamer", "threadmill"):
        import hole_tools
        code = hole_tools.TYPE_CODE[kind]
    else:
        code = 50 if kind == "drill" else int(row["type_code"])
    return tb.get_or_create(model, kind, row, code, jt, material=material, purposes=purposes, force_new=force_new)

def select_chamfer_by_da(da_in, material, manufacturer="Walter"):
    """MC501 90 degree chamfer mill with the large diameter Da nearest to da_in. Returns (row, note)."""
    import re
    rows = []
    for r in _rows(manufacturer, "endmills"):
        m = re.match(r"^MC501-(\d+\.\d)A\d", r["designation"])
        if r["type_code"] == "13" and m and r["tier"]:
            rr = dict(r); da = float(m.group(1))
            rr["tip_mm"] = r["dia_mm"]; rr["dia_mm"] = str(da); rr["dia_in"] = str(da / MM); rr["half_angle"] = "45"
            rows.append(rr)
    rows = _fit_rated(rows, material) if rows else rows
    if not rows:
        return None, "no MC501 chamfer mill rated for %s" % material
    near = min(rows, key=lambda r: abs(float(r["dia_in"]) - da_in))
    same = [r for r in rows if r["dia_mm"] == near["dia_mm"]]
    same, fb = _prefer_first(same, _letter_col(material))
    same.sort(key=lambda r: -int(r["tier_rank"] or 0))
    note = "" if abs(float(near["dia_in"]) - da_in) <= 0.003 else "nearest chamfer mill is %.4f in" % float(near["dia_in"])
    return same[0], _add(note, fb)


XDRILL_ORDER = {"D5150": 0, "D4140": 1, "D5142": 2, "D4240": 3, "D4120": 4, "D3120": 5, "D4170": 6, "B3212": 7, "B3213": 7, "B3214": 7}

def select_xdrill(dia_in, depth_in, material, manufacturer="Walter"):
    """Walter exchangeable-head / exchangeable-tip / insert drill rated for the material's ISO group, nominal diameter matched
    (else the nearest larger), shortest body whose flute length reaches depth_in. Returns (row, note)."""
    col = ISO_COL.get(str(material)[:1].upper())
    rows = list(_rows(manufacturer, "xdrills"))
    if col:
        rows = [r for r in rows if int(r[col] or 0) >= 1]
    if not rows:
        return None, "%s lists no exchangeable-tip or insert drill for %s" % (manufacturer, material)
    def d(r): return float(r["dia_in"])
    best = min(rows, key=lambda r: (abs(d(r) - dia_in) > 0.002, d(r) < dia_in, abs(d(r) - dia_in)))
    same = [r for r in rows if abs(d(r) - d(best)) < 0.002]
    ok = [r for r in same if float(r["flute_len_in"]) >= depth_in - 1e-6]
    note = "" if abs(d(best) - dia_in) <= 0.002 else "no %.4f in drill; nearest is %.4f in" % (dia_in, d(best))
    if not ok:
        ok = same; note = (note + " | " if note else "") + "no body reaches %.3f in; deepest offered" % depth_in
    ok, fb = _prefer_first(ok, col)
    note = _add(note, fb)
    if manufacturer != "Walter":
        ok.sort(key=lambda r: (-int(r[col] or 0) if col else 0, 0 if unit_of(r) == UNIT_PREF else 1, float(r["flute_len_in"])))
        return ok[0], note
    ok.sort(key=lambda r: (-int(r[col] or 0) if col else 0, float(r["flute_len_in"]) if ok is not same else -float(r["flute_len_in"]), XDRILL_ORDER.get(r["family"], 9)))
    return ok[0], note


def select_shoulder(dia_in, ap_in, material, manufacturer="Walter"):
    """Inserted 90 degree shoulder mill (Walter M5130, M5137, M4132, F4041, F4042, F5041, F5141, F5241). Shell mount from 2 in diameter up,
    shank mount (cylindrical, Weldon, ScrewFit) below. Needs the ISO rating for the material, nearest diameter, depth of cut >= ap_in."""
    return select_facemill(dia_in, ap_in, material, manufacturer, tol_in=0.02, mount="shell" if dia_in >= 2.0 else "shank", group="shoulder")


def select_highfeed(dia_in, ap_in, material, manufacturer="Walter"):
    """Inserted high-feed mill (Walter M6420, M5008, M4002, F2330, F4030). ap_in is the insert depth of cut."""
    return _select_from(dia_in, ap_in, material, manufacturer, "HighFeed", 0.03)

def select_copy(dia_in, ap_in, material, manufacturer="Walter"):
    """Inserted round-insert copy / profile mill (Walter M5468, M2471-M2473, F2334R, F2339, F2239). Diameter is the cutter diameter Da."""
    return _select_from(dia_in, ap_in, material, manufacturer, "Copy", 0.03)

def _select_from(dia_in, ap_in, material, manufacturer, shape, tol):
    col = ISO_COL.get(str(material)[:1].upper())
    rows = [r for r in tb.load_rows(MANUFACTURERS[manufacturer]["hfcopy"]) if r["shape"] == shape and r["dia_in"] and r["l4_mm"]]
    if col:
        rows = [r for r in rows if int(r[col] or 0) >= 1]
    if not rows:
        return None, "Walter lists no inserted %s cutter for %s" % (shape, material)
    want = ("B",) if dia_in >= 2.0 else ("A", "T", "W", "Z")
    m = [r for r in rows if r["interface"][:1] in want] or rows
    big = [r for r in m if float(r["dia_in"]) >= dia_in - tol]
    if not big:
        r = max(m, key=lambda r: float(r["dia_in"]))
        return r, "largest Walter cutter is %.3f in" % float(r["dia_in"])
    note = ""
    deep = [r for r in big if float(r["lc_mm"] or 0) / MM >= ap_in - 1e-6]
    if not deep:
        deep = big; note = "no cutter reaches %.3f in depth of cut; deepest offered" % ap_in
    deep, fb = _prefer_first(deep, col)
    note = _add(note, fb)
    deep.sort(key=lambda r: (-int(r[col] or 0) if col else 0, round(abs(float(r["dia_in"]) - dia_in), 2), -int(r["flutes"] or 0), float(r["lc_mm"] or 0)))
    r = deep[0]
    if float(r["dia_in"]) < dia_in - 1e-3:
        note = (note + " | " if note else "") + "nearest smaller diameter %.3f in" % float(r["dia_in"])
    return r, note


def select_chamfer_inserted(da_in, material, manufacturer="Walter", angle=90):
    """Inserted chamfer mill (Walter M4574) with the included angle 60, 90 or 120 degrees (half angle 30, 45, 60).
    Matches the large diameter Da, shell/shank by size, rated for the ISO group."""
    col = ISO_COL.get(str(material)[:1].upper())
    rows = [r for r in tb.load_rows(MANUFACTURERS[manufacturer]["chamfer_ins"]) if abs(float(r.get("half_angle") or 45) * 2 - angle) < 0.5]
    if col:
        rows = [r for r in rows if int(r[col] or 0) >= 1]
    if not rows:
        return None, "Walter lists no inserted chamfer mill for %s" % material
    def d(r): return float(r["dia_in"])
    best = min(rows, key=lambda r: (abs(d(r) - da_in) > 0.01, d(r) < da_in, abs(d(r) - da_in)))
    same = [r for r in rows if abs(d(r) - d(best)) < 1e-6]
    same, fb = _prefer_first(same, col)
    same.sort(key=lambda r: (r["interface"][:1] not in ("A", "T"), float(r["oal_mm"])))
    r = same[0]
    note = "" if abs(d(r) - da_in) <= 0.01 else "no %.3f in large diameter; nearest is %.3f in" % (da_in, d(r))
    return r, _add(note, fb)


def select_profile(dia_in, reach_in, material, manufacturer="Walter"):
    """Inserted ball (profile) mill M5460: nearest diameter rated for the material, shortest projection l4 that reaches reach_in,
    shank or ScrewFit mounts. Returns (row, note)."""
    col = ISO_COL.get(str(material)[:1].upper())
    rows = list(tb.load_rows(MANUFACTURERS[manufacturer]["profile"]))
    if col:
        rows = [r for r in rows if int(r[col] or 0) >= 1]
    if not rows:
        return None, "Walter lists no inserted profile mill for %s" % material
    def d(r): return float(r["dia_in"])
    best = min(rows, key=lambda r: (abs(d(r) - dia_in) > 0.01, d(r) < dia_in, abs(d(r) - dia_in)))
    same = [r for r in rows if abs(d(r) - d(best)) < 0.01]
    note = "" if abs(d(best) - dia_in) <= 0.01 else "no %.3f in diameter; nearest is %.3f in" % (dia_in, d(best))
    same, fb = _prefer_first(same, col)
    note = _add(note, fb)
    ok = [r for r in same if float(r["l4_mm"] or 0) / MM >= reach_in - 1e-6]
    if not ok:
        ok = same; note = (note + " | " if note else "") + "no profile mill reaches %.3f in; longest offered" % reach_in
        ok.sort(key=lambda r: -float(r["l4_mm"] or 0))
    else:
        ok.sort(key=lambda r: (-int(r[col] or 0) if col else 0, float(r["l4_mm"] or 0), r["interface"][:1] not in ("A", "T", "W")))
    return ok[0], note


SLOT_KINDS = {"Slot cutter (disc head)": ("slot",), "Circlip groove cutter (disc head)": ("circlip",), "Disc chamfer cutter (45 degree)": ("chamfer",), "T-slot cutter (inserted)": ("tslot",), "Slotting / side-and-face cutter (shell mount)": ("disc",)}

def select_slot(dia_in, width_in, material, kind, manufacturer="Walter"):
    """Disc / T-slot cutter of the given kind (slot, circlip, chamfer, tslot): nearest cutter diameter, then the slot width closest to width_in
    (the next wider if none matches), rated for the material's ISO group. Returns (row, note)."""
    col = ISO_COL.get(str(material)[:1].upper())
    rows = [r for r in tb.load_rows(MANUFACTURERS[manufacturer]["slot"]) if r["kind"] == kind]
    if col:
        rows = [r for r in rows if int(r[col] or 0) >= 1]
    if not rows:
        return None, "Walter lists no %s cutter for %s" % (kind, material)
    def d(r): return float(r["dia_in"])
    best = min(rows, key=lambda r: (abs(d(r) - dia_in) > 0.01, d(r) < dia_in, abs(d(r) - dia_in)))
    same = [r for r in rows if abs(d(r) - d(best)) < 0.003]
    same, fb = _prefer_first(same, col)
    note = _add("" if abs(d(best) - dia_in) <= 0.01 else "no %.3f in cutter diameter; nearest is %.3f in" % (dia_in, d(best)), fb)
    if kind == "disc" and width_in:
        w = width_in * MM
        inr = [r for r in same if float(r["sb_mm"]) - 1e-6 <= w <= float(r["sbmax_mm"] or r["sb_mm"]) + 1e-6]
        if inr:
            r = dict(sorted(inr, key=lambda r: float(r["z"]), reverse=True)[0]); r["sb_mm"] = round(w, 3)
            return r, note
    if kind != "chamfer" and width_in:
        w = lambda r: float(r["sb_mm"]) / MM
        r = min(same, key=lambda r: (abs(w(r) - width_in) > 0.004, w(r) < width_in, abs(w(r) - width_in)))
        if abs(w(r) - width_in) > 0.004:
            note = (note + " | " if note else "") + "no %.3f in slot width at this diameter; nearest is %.3f in" % (width_in, w(r))
    else:
        r = same[0]
    return r, note
