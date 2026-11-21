# tool_usage.py - order first-choice milling tools by the operator's primary usage (HEM, roughing, slotting, semi-finishing,
# wall finishing, floor finishing, 3D profiling). Ordering only: no tool is removed, first-choice ratings are unchanged.
#
# Score per family = manufacturer statement (walter_usage.csv, kennametal_usage.csv, garr_usage.csv) plus a generic geometry
# score 0..5 that fills the gaps where the manufacturer says nothing. The statement always leads:
#   catalog names this use (2)      12 + geometry   (12..17)
#   catalog says suitable (1)        6 + geometry   (6..11)
#   catalog says nothing                 geometry   (0..5)
#   catalog says not for it (0)     -6 + geometry   (-6..-1)
# Generic rules (secondary source, general shop guidance):
#   Redline Tools, 4/5/6 flute end mills: 4 flute = roughing and the only geometry rated for full slots; 5 flute = HEM / dynamic
#     paths with light-to-moderate radial engagement and semi-finishing; 6 flute = finish and semi-finish profiling of walls;
#     chip breakers for roughing only, "not recommended for finishing passes"; 2 flute preferable for aluminium.
#     https://www.redlinetools.com/resources/4-5-and-6-flute-endmills
#   Productivity Inc., selecting the right end mill: roughing/slotting fewer flutes (3-4 in metals), serrated roughers;
#     HEM more flutes (6-13); finishing high flute counts (5-10+); aluminium 2-3 flutes.
#     https://productivity.com/blog/selecting-the-right-end-mill-for-your-machining-set-up/
#   Dapra, 3D finishing: ball nose for 3D finishing of sloped or curved surfaces; bull nose (corner radius) for walls and
#     semi-finishing. https://www.dapra.com/tool-finder/3d-finishing
import os
import tool_builder as tb

PURPOSE_SEMI = tb.PURPOSE_SEMI             # tecset purpose names of the two new cutting-data sets (set in tool_builder.py)
PURPOSE_3D = tb.PURPOSE_3D

# key, label, tecset purpose pre-ticked on the last screen
USAGES = [("", "Any", None),
          ("hem", "HEM / dynamic roughing", "Rough-HEM - usage 1"),
          ("rough", "Traditional roughing", "Rough - usage 1"),
          ("slot", "Slotting", "Slotting - usage 1"),
          ("semi", "Semi-finishing", PURPOSE_SEMI),
          ("finish_wall", "Wall finishing", "Finish-2D-Radial - usage 1"),
          ("finish_floor", "Floor finishing", "Finish-2D-Axial - usage 1"),
          ("profile3d", "3D profiling", PURPOSE_3D)]
USAGE_LABELS = [u[1] for u in USAGES]
USAGE_FILES = {"Walter": "walter_usage.csv", "Kennametal": "kennametal_usage.csv", "GARR": "garr_usage.csv"}
MILL_KINDS = ("endmill", "facemill", "profilemill")

_cache = {}

CATALOG_WEIGHT = 6       # points per catalog usage level; more than the best geometry score (5), so the catalog statement leads
NOT_FOR = -6             # catalog says the family is not for this usage: below every family the catalog says nothing about

def _f(x, d=0.0):
    """Number from a table cell. A blank cell gives d; anything else that is not a number stops with the cell named, so a typo in
    a table is caught instead of turning into 0."""
    if x is None or str(x).strip() == "":
        return d
    try:
        return float(str(x).strip().replace(",", "."))
    except ValueError:
        raise ValueError("tool_usage: unreadable number %r in a tool table" % (x,))

def usage_key(label):
    for k, l, _ in USAGES:
        if l == label:
            return k
    return ""

def purpose_of(key):
    for k, _, p in USAGES:
        if k == key:
            return p
    return None

def mfg_table(mf):
    """{family: {usage: (score, quote)}} from the manufacturer usage table, {} if there is none."""
    if mf in _cache:
        return _cache[mf]
    out = {}
    fn = USAGE_FILES.get(mf)
    if fn and os.path.exists(os.path.join(tb.HERE, fn)):
        for r in tb.load_rows(fn):
            s = int(_f(r.get("score"), -1))
            fam = (r.get("family") or "").strip()
            u = (r.get("usage") or "").strip()
            if fam and u and s >= 0:
                cur = out.setdefault(fam, {}).get(u)
                if cur is None or s > cur[0]:
                    out[fam][u] = (s, (r.get("quote") or "")[:40])
    _cache[mf] = out
    return out

def _text(r):
    return " ".join(str(r.get(k, "")) for k in ("family", "designation", "series", "title", "description", "shape", "kind")).lower()

def generic(r, usage, material):
    """Generic geometry score 0..5 and a short reason (a manufacturer statement weighs 6 per level, so it always leads)."""
    z = int(_f(r.get("flutes") or r.get("z"), 0))
    d = _f(r.get("dia_mm")) or _f(r.get("dia_in")) * 25.4
    loc = _f(r.get("flute_len_mm"))
    shape = r.get("shape", "")
    t = _text(r)
    chip = any(w in t for w in ("chip split", "chip break", "chipbreak", "serrat", "wavy", "knuckle"))   # flute form words only, not "roughing" in a title
    var = "variable" in t or "var" == str(r.get("helix", "")).lower()
    alu = str(material)[:1].upper() == "N"
    lxd = loc / d if d else 0
    s, why = 0, []
    def add(n, w):
        nonlocal s
        s += n; why.append(w)
    if usage == "hem":
        if (alu and z == 3) or (not alu and z >= 5):
            add(2, "%d fl" % z)
        if chip:
            add(1, "chip splitter")
        if var:
            add(1, "variable helix")
        if lxd >= 2.0:
            add(1, "long flute")
    elif usage == "rough":
        # traditional roughing here = high-feed style, large ae and small ap: high-feed geometry first, then a corner radius
        # (protects the corner at small ap), then a strong core (4-6 flutes; 3 in aluminium)
        if "high feed" in t or "highfeed" in t or "high-feed" in t:
            add(3, "high-feed geometry")
        if shape == "Radiused":
            add(1, "corner radius")
        if (alu and 2 <= z <= 3) or (not alu and 4 <= z <= 6):
            add(1, "%d fl" % z)
        if chip:
            add(1, "chip breaker")
    elif usage == "slot":
        if (alu and 2 <= z <= 3) or (not alu and 3 <= z <= 4):
            add(2, "%d fl for slots" % z)
        if z >= 6:
            add(-1, "too many flutes to slot")
        if shape in ("Square", "Radiused"):
            add(1, shape.lower())
    elif usage == "semi":
        if 5 <= z <= 6 or (alu and z == 3):
            add(2, "%d fl" % z)
        if shape == "Radiused":
            add(1, "corner radius")
        if not chip:
            add(1, "plain flute")
    elif usage == "finish_wall":
        if z >= 6 or (alu and z >= 3):
            add(2, "%d fl" % z)
        if not chip:
            add(1, "plain flute")
        if 0 < lxd <= 2.0:
            add(1, "short flute")
    elif usage == "finish_floor":
        if shape == "Square" or (shape == "Radiused" and _f(r.get("corner_r_mm")) <= 0.1 * d):
            add(1, "flat bottom")
        if z >= 4:
            add(1, "%d fl" % z)
        if not chip:
            add(1, "plain flute")
    elif usage == "profile3d":
        if shape == "Ball" or "ball" in t or "profile" in t:
            add(3, "ball nose")
        elif shape == "Radiused":
            add(2, "corner radius")
    return max(0, min(5, s)), ", ".join(why)

def family_score(mf, fam, rows, usage, material):
    """(score, reason): manufacturer statement (see the table at the top) plus the best generic score of the family's tools."""
    if not usage:
        return 0, ""
    m = mfg_table(mf).get(fam, {}).get(usage)
    g, gwhy = max((generic(r, usage, material) for r in rows), key=lambda x: x[0])
    if m is not None:
        return (CATALOG_WEIGHT * m[0] if m[0] > 0 else NOT_FOR) + g, ("%s: %s" % (mf, m[1] or ("recommended" if m[0] == 2 else ("suitable" if m[0] == 1 else "not for this"))) +
                             (" | " + gwhy if gwhy else ""))
    return g, gwhy

def order_families(mf, fams, usage, material, base_key):
    """Family names, best for the usage first (base_key breaks ties = the catalog order), and a reason per family."""
    sc = {f: family_score(mf, f, fams[f], usage, material) for f in fams}
    names = sorted(fams, key=lambda f: (-sc[f][0], base_key(f)))
    return names, {f: sc[f][1] for f in fams}

def order_tools(rows, usage):
    """Tools within a family: HEM prefers 2-3xD flute, finishing the shortest rigid tool, slotting about 1-1.5xD; else unchanged."""
    if not usage:
        return rows
    def lxd(r):
        d = _f(r.get("dia_mm")) or _f(r.get("dia_in")) * 25.4
        return (_f(r.get("flute_len_mm")) / d) if d else 0
    def key(r):
        x = lxd(r)
        reach = _f(r.get("reach_mm")) or _f(r.get("flute_len_mm"))
        if usage in ("hem",):
            return (abs(x - 2.5), reach)
        if usage in ("slot",):
            return (abs(x - 1.25), reach)
        if usage in ("finish_wall", "finish_floor", "semi", "profile3d"):
            return (x, reach)
        return (x, reach)
    return sorted(rows, key=key)
