# garr_cut.py - GARR TOOL cutting data from the TECHNICAL catalog tables (garr_mill_cutting.csv, garr_drill_cutting.csv,
# garr_reamer_cutting.csv), with the hyperMILL material mapped to a GARR material row by garr_material_map.csv.
# Values: SFM = middle of the printed range; chip load = middle of the printed range at the tool diameter (straight-line
# between the printed diameter columns). ae/ap from the guide's profile/trochoidal and slotting boxes where printed.
# HEM feed gets the radial chip thinning correction (the X/G, V and VRX guides state the data does not include it).
import math, re
import tool_builder as tb

MM = 25.4
_cache = {}

def _rows(name):
    if name not in _cache:
        _cache[name] = tb.load_rows(name)
    return _cache[name]

def _f(x, d=None):
    try:
        return float(str(x).replace('"', "").strip())
    except Exception:
        return d

def _map(material):
    for r in _rows("garr_material_map.csv"):
        if r["hypermill_material"] == material:
            return r
    return None

def _norm(s):
    return re.sub(r"\s+", " ", str(s).replace("’", "'")).strip().lower()

HRC_TARGET = {"H - Hardened Steel 45-55 HRC": (45.0, 55.0), "H - Chilled Cast Iron": (45.0, 55.0)}   # other materials: below 40 HRC
STRATEGY_PREF = ("", "conventional", "Roughing", "high feed", "high speed machining", "Semi-Finishing and Finishing")

def _band(text):
    """'<40' -> (0, 40), '>40' -> (40, 70), '45-50' -> (45, 50), '' -> None (any hardness)."""
    t = str(text or "").replace(" ", "").replace("HRC", "")
    if not t:
        return None
    nums = [float(x) for x in re.findall(r"\d+(?:\.\d+)?", t)]
    if not nums:
        return None
    if t.startswith("<"):
        return (0.0, nums[0])
    if t.startswith(">"):
        return (nums[0], 70.0)
    return (min(nums), max(nums))

def _overlap(a, b):
    return max(0.0, min(a[1], b[1]) - max(a[0], b[0]))

def _pick(table, row, material, col):
    """The printed rows of ONE guide, ONE material row, ONE hardness band and ONE strategy for the tool's series and the mapped
    GARR material. Guides with printed SFM come first (a series can appear in several guides, e.g. A3 in three aluminium ranges)."""
    m = _map(material)
    if not m:
        return []
    fam = row.get("family", "")
    cand = [r for r in _rows(table) if fam in r["series"].split()]
    if not cand:
        return []
    target = HRC_TARGET.get(material, (0.0, 39.9))
    same = [r for r in cand if r["iso"] == m["iso"]]
    for name in [x for x in m[col].split("|") if x.strip()]:
        hit = [r for r in same if _norm(r["material"]) == _norm(name)]
        if not hit:                     # some guides print hardened tool steel under P with a hardness band: match by name
            hit = [r for r in cand if _norm(r["material"]) == _norm(name)]
        if not hit:
            continue
        groups = {}
        for r in hit:
            groups.setdefault((r.get("guide", ""), r.get("hrc", ""), r.get("strategy", "")), []).append(r)
        def score(k):
            g, h, st = k
            rows = groups[k]
            band = _band(h)
            ov = 1.0 if band is None else _overlap(band, target)
            if band is not None and ov <= 0 and not (band[1] <= 40 and target[1] <= 40):
                ov = -1.0
            has_sfm = sum(1 for r in rows if _f(r.get("sfm_min")) or _f(r.get("sfm_max")))
            pref = STRATEGY_PREF.index(st) if st in STRATEGY_PREF else 9
            return (ov >= 0, ov, has_sfm > 0, -pref, len(rows))
        best = max(groups, key=score)
        if score(best)[0]:
            return groups[best]
    return []

def _at_dia(rows, d, lo, hi):
    """Value (mid of lo/hi columns) at diameter d: straight line between printed columns, end values outside."""
    pts = []
    for r in rows:
        a, b = _f(r[lo]), _f(r[hi])
        x = _f(r["dia_in"])
        if x is None or (a is None and b is None):
            continue
        dmin, dmax = _f(r.get("dia_min_in")), _f(r.get("dia_max_in"))
        if dmin is not None and dmax is not None and dmin <= d <= dmax and dmax > dmin:
            return ((a or b) + (b or a)) / 2.0, r
        pts.append((x, ((a or b) + (b or a)) / 2.0, r))
    if not pts:
        return None, None
    pts.sort(key=lambda p: p[0])
    if d <= pts[0][0]:
        return pts[0][1], pts[0][2]
    if d >= pts[-1][0]:
        return pts[-1][1], pts[-1][2]
    for k in range(len(pts) - 1):
        if pts[k][0] <= d <= pts[k + 1][0]:
            t = (d - pts[k][0]) / (pts[k + 1][0] - pts[k][0])
            return pts[k][1] + t * (pts[k + 1][1] - pts[k][1]), pts[k][2]
    return pts[-1][1], pts[-1][2]

def _sfm(r, d):
    a, b = _f(r.get("sfm_min")), _f(r.get("sfm_max"))
    if a is not None or b is not None:
        return ((a or b) + (b or a)) / 2.0
    rpm = _f(r.get("rpm_max")) or _f(r.get("rpm_min"))
    x = _f(r.get("dia_in")) or d
    return rpm * math.pi * x / 12.0 if rpm else None

def _len(text, d, flute, upper=True):
    """'up to 2xD', 'MAX', '5% - 25% of Dia.', '0.5 to 1xD', '0.2xD', '0.3 x Radius' -> inches (None if not printed)."""
    t = str(text or "").lower()
    if not t.strip():
        return None
    if "max" in t:
        return flute or 1.5 * d
    t = t.split(";")[0]
    nums = [float(x) for x in re.findall(r"\d*\.?\d+", t)]
    if not nums:
        return None
    v = max(nums) if upper else min(nums)
    if "%" in t:
        return v / 100.0 * d
    if "radius" in t:
        return v * d / 2.0
    return v * d

def _rpm(sfm, d):
    rpm = sfm * 12 / (math.pi * d)
    if rpm > tb.MAX_RPM:
        sfm *= tb.MAX_RPM / rpm; rpm = tb.MAX_RPM
    return sfm, rpm

def endmill_cut(row, material):
    """dict purpose -> dict(vc, rpm, fz, ipm, ae, ap) like the Walter and Kennametal functions; None without printed data."""
    d = _f(row.get("dia_in")) or (_f(row.get("dia_mm"), 0) / MM)
    if not d:
        return None
    rows = _pick("garr_mill_cutting.csv", row, material, "mill_material")
    if not rows:
        return None
    prof = [r for r in rows if r["op"] in ("profile", "both", "finish")] or rows
    slot = [r for r in rows if r["op"] in ("slot", "both")] or prof
    fz_p, rp = _at_dia(prof, d, "fz_min_in", "fz_max_in")
    fz_s, rs = _at_dia(slot, d, "fz_min_in", "fz_max_in")
    if fz_p is None:
        return None
    if fz_s is None:
        fz_s, rs = fz_p * 0.8, rp
    z = max(int(_f(row.get("flutes"), 3) or 3), 1)
    flute = (_f(row.get("flute_len_mm"), 0) or 0) / MM
    sfm = _sfm(rp, d)
    if not sfm:
        return None
    sfm_s = _sfm(rs, d) or sfm
    ae_r = _len(rp.get("ae_profile"), d, flute) or 0.5 * d
    ap_r = _len(rp.get("ap_profile"), d, flute) or (min(1.5 * d, flute) if flute else 1.5 * d)
    if flute:
        ap_r = min(ap_r, flute)
    ae_s = _len(rs.get("ae_slot"), d, flute) or d
    ap_s = _len(rs.get("ap_slot"), d, flute) or (min(d, flute) if flute else d)
    if flute:
        ap_s = min(ap_s, flute)
    def mk(v, fz, ae, ap):
        v, rpm = _rpm(v, d)
        return dict(vc=v, rpm=rpm, fz=fz, ipm=rpm * fz * z, ae=ae, ap=ap)
    if any(r.get("strategy") == "high feed" for r in rows):
        # GARR high-feed guide (H-45, TECHNICAL p320): full radial width (1 x D) and axial depth 0.3 x the CORNER radius per pass
        # ("when D = 1/2 with .060 corner radius = .018 per pass"); RPM and IPM as printed, chip load already includes the thinning
        cr = _f(row.get("corner_r_mm"), 0) / MM or 0.06 * d
        ap_hf = 0.3 * cr
        hf = mk(sfm, fz_p, d, ap_hf)
        return {"Rough - usage 1": hf, "Slotting - usage 1": dict(hf), tb.PURPOSE_HEM: dict(hf),
                "Finish-2D-Radial - usage 1": mk(sfm, fz_p * 0.6, 0.05 * d, min(d, flute) if flute else d),
                "Finish-2D-Axial - usage 1": mk(sfm, fz_p * 0.6, 0.5 * d, min(0.3 * cr, 0.01))}
    # radial chip thinning for light radial engagement (HEM): fz x 1 / sqrt(1 - (1 - 2 ae/D)^2), capped at 2x
    ae_h = min(ae_r, 0.25 * d)
    k = 1.0 / math.sqrt(max(1e-6, 1 - (1 - 2 * ae_h / d) ** 2)) if ae_h < 0.5 * d else 1.0
    return {"Rough - usage 1": mk(sfm, fz_p, ae_r, ap_r),
            "Slotting - usage 1": mk(sfm_s, fz_s, ae_s, ap_s),
            "Finish-2D-Radial - usage 1": mk(sfm * 1.1, fz_p * 0.6, min(0.05 * d, ae_r), ap_r),
            "Finish-2D-Axial - usage 1": mk(sfm * 1.1, fz_p * 0.6, min(0.5 * d, ae_r * 2), min(0.05 * d, ap_r)),
            tb.PURPOSE_HEM: mk(sfm, fz_p * min(k, 2.0), ae_h, ap_r)}

def drill_cut(row, material, table="garr_drill_cutting.csv"):
    """dict(vc, rpm, ipr, ipm, grp, vrr) like the Walter and Kennametal functions; None without printed data."""
    d = _f(row.get("dia_in")) or (_f(row.get("dia_mm"), 0) / MM)
    if not d:
        return None
    rows = _pick(table, row, material, "drill_material")
    if not rows:
        return None
    # GARR prints feed per tooth; ipr = fz x the tool's own flute count (the printed ipr columns assume one flute count per column)
    fz, r = _at_dia(rows, d, "fz_min_in", "fz_max_in")
    z = int(_f(row.get("flutes"), 0) or 0)
    if fz is not None and z:
        ipr = fz * z
    else:
        ipr, r = _at_dia(rows, d, "ipr_min", "ipr_max")
        if ipr is None:
            return None
    sfm = _sfm(r, d)
    if not sfm:
        return None
    sfm, rpm = _rpm(sfm, d)
    return dict(vc=sfm, rpm=rpm, ipr=ipr, ipm=rpm * ipr, grp=r["iso"] + " " + r["material"][:30], vrr="")
