# tool_catalog.py - one set of tool-type and first-choice rules for tool_center (tool wizard, selector, generator).
# First choice = the catalog rates the tool 2 (primary) for the ISO group of the material. A tool rated 1 (suitable) is used only when
# no rated-2 tool exists near the requested size, and it is then marked NOT FIRST CHOICE.
import re
import tool_builder as tb
import tool_lookup as tl
import hole_tools as ht

MM = 25.4
DIA_TOL_IN = 0.003                         # same size when within this many inches (solid tools)
INSERTED_TOL_IN = 0.01                     # inserted cutters and boring
FIRST_OFF = tl.FIRST_CHOICE_DIA_OFF        # a first-choice tool may be up to this fraction off the requested diameter (solid mills)
NOT_FIRST = "NOT FIRST CHOICE: catalog rates it suitable (1), not primary (2), for ISO %s"

# performance levels (Walter tier names behind each level); Kennametal catalogs have one level
LEVELS = [("Performance", {"Supreme", "High performance"}), ("Standard", {"Advance", "", "General purpose"}), ("Low cost", {"Perform"}), ("PCD", {"PCD"})]
LEVEL_MFS = ("Walter", "GARR")             # manufacturers whose catalogs carry performance levels (Walter tiers, GARR sections)
LEVEL_KINDS = ("endmill", "drill", "reamer", "tap", "threadmill")

TECSETS = [("HEM", "Rough-HEM - usage 1"),
           ("Traditional roughing", "Rough - usage 1"),
           ("Slotting", "Slotting - usage 1"),
           ("Wall finishing", "Finish-2D-Radial - usage 1"),
           ("Floor finishing", "Finish-2D-Axial - usage 1"),
           ("Semi-finishing", tb.PURPOSE_SEMI),
           ("3D profiling", tb.PURPOSE_3D)]
DEFAULT_TECSETS = ("Rough-HEM - usage 1", "Rough - usage 1", "Finish-2D-Radial - usage 1")

def _f(x, d=0.0):
    try:
        return float(x)
    except Exception:
        return d

def _endmill(code, shape):
    return lambda r: r.get("type_code") == code and r.get("shape") == shape and r.get("quality") != "unverified" and r.get("flute_len_mm")
def _spot(angle):
    return lambda r: bool(r.get("point_angle")) and int(_f(r["point_angle"])) == angle
def _slot(kind):
    return lambda r: r.get("kind") == kind
def _mc501(r):
    return r.get("type_code") == "13" and bool(re.match(r"^MC501-(\d+\.\d)A\d", r.get("designation", ""))) and bool(r.get("tier"))
def _mc501_row(r):
    """MC501 90 degree chamfer mill: the size is the large diameter Da (from the designation); the table diameter is the tip Dc."""
    rr = dict(r)
    da = float(re.match(r"^MC501-(\d+\.\d)A", r["designation"]).group(1))
    rr["tip_mm"] = r["dia_mm"]; rr["dia_mm"] = str(da); rr["dia_in"] = str(da / MM); rr["half_angle"] = "45"
    return rr

# group = catalog key (tool_lookup.MANUFACTURERS, hole_tools.HOLE_FILES, or 'reamers'); kind = tool_builder kind;
# size = 'dia' | 'thread' | 'bore'; opts = optional limits asked on the size screen; tol = size tolerance (in)
TYPES = [
    ("Flat end mill",                   dict(group="endmills",   kind="endmill",     size="dia",    test=_endmill("10", "Square"),   opts=("loc", "reach", "flutes"), tol=DIA_TOL_IN, solid=True)),
    ("Radius end mill",                 dict(group="endmills",   kind="endmill",     size="dia",    test=_endmill("11", "Radiused"), opts=("loc", "reach", "flutes", "radius"), tol=DIA_TOL_IN, solid=True)),
    ("Ball end mill",                   dict(group="endmills",   kind="endmill",     size="dia",    test=_endmill("12", "Ball"),     opts=("loc", "reach", "flutes"), tol=DIA_TOL_IN, solid=True)),
    ("Chamfer mill (90 degree)",        dict(group="endmills",   kind="chamfer",     size="dia",    test=_mc501, fix=_mc501_row, opts=(), tol=DIA_TOL_IN)),
    ("Drill",                           dict(group="drills",     kind="drill",       size="dia",    test=lambda r: r.get("type") == "Carbide drill" and not r.get("thread"), opts=("depth", "through"), tol=0.002)),
    ("NC spot drill (90 degree)",       dict(group="spotdrills", kind="spotdrill",   size="dia",    test=_spot(90),  opts=(), tol=0.002)),
    ("NC spot drill (120 degree)",      dict(group="spotdrills", kind="spotdrill",   size="dia",    test=_spot(120), opts=(), tol=0.002)),
    ("Centre drill (60 degree)",        dict(group="spotdrills", kind="spotdrill",   size="dia",    test=_spot(60),  opts=(), tol=0.002)),
    ("Exchangeable-tip / insert drill", dict(group="xdrills",    kind="xdrill",      size="dia",    test=lambda r: True, opts=("depth",), tol=0.002)),
    ("Reamer",                          dict(group="reamers",    kind="reamer",      size="dia",    test=lambda r: True, opts=("hole",), tol=0.0015)),
    ("Tap",                             dict(group="taps",       kind="tap",         size="thread", test=lambda r: True, opts=("threadlen", "form"), tol=0)),
    ("Thread mill",                     dict(group="threadmills", kind="threadmill", size="thread", test=lambda r: r.get("type") == "thread mill" and r.get("cutter_dia_in") and r.get("thread_len_mm"), opts=("threadlen", "maxcutter"), tol=0)),
    ("Face mill (inserted)",            dict(group="facemills",  kind="facemill",    size="dia",    test=lambda r: True, opts=("ap", "mount"), tol=INSERTED_TOL_IN)),
    ("Shoulder mill (inserted)",        dict(group="shoulder",   kind="facemill",    size="dia",    test=lambda r: True, opts=("ap", "mount"), tol=INSERTED_TOL_IN)),
    ("High-feed mill (inserted)",       dict(group="hfcopy",     kind="facemill",    size="dia",    test=lambda r: r.get("shape") == "HighFeed" and r.get("l4_mm"), opts=("ap", "mount"), tol=INSERTED_TOL_IN)),
    ("Round insert copy mill (inserted)", dict(group="hfcopy",   kind="facemill",    size="dia",    test=lambda r: r.get("shape") == "Copy" and r.get("l4_mm"), opts=("ap", "mount"), tol=INSERTED_TOL_IN)),
    ("Ball end mill (inserted)",        dict(group="profile",    kind="profilemill", size="dia",    test=lambda r: True, opts=("reachl4",), tol=INSERTED_TOL_IN)),
    ("Inserted chamfer mill (90 degree)", dict(group="chamfer_ins", kind="chamfer",  size="dia",    test=lambda r: abs(_f(r.get("half_angle"), 45) - 45) < 0.5, opts=(), tol=INSERTED_TOL_IN)),
    ("Inserted chamfer mill (60 degree)", dict(group="chamfer_ins", kind="chamfer",  size="dia",    test=lambda r: abs(_f(r.get("half_angle"), 45) - 30) < 0.5, opts=(), tol=INSERTED_TOL_IN)),
    ("Inserted chamfer mill (120 degree)", dict(group="chamfer_ins", kind="chamfer", size="dia",    test=lambda r: abs(_f(r.get("half_angle"), 45) - 60) < 0.5, opts=(), tol=INSERTED_TOL_IN)),
    ("Slot cutter (disc head)",         dict(group="slot",       kind="slot",        size="dia",    test=_slot("slot"),    opts=("width",), tol=INSERTED_TOL_IN)),
    ("Circlip groove cutter (disc head)", dict(group="slot",     kind="slot",        size="dia",    test=_slot("circlip"), opts=("width",), tol=INSERTED_TOL_IN)),
    ("Disc chamfer cutter (45 degree)", dict(group="slot",       kind="slot",        size="dia",    test=_slot("chamfer"), opts=(), tol=INSERTED_TOL_IN)),
    ("T-slot cutter (inserted)",        dict(group="slot",       kind="slot",        size="dia",    test=_slot("tslot"),   opts=("width",), tol=INSERTED_TOL_IN)),
    ("Slotting / side-and-face cutter (shell mount)", dict(group="slot", kind="slot", size="dia",  test=_slot("disc"),    opts=("width",), tol=INSERTED_TOL_IN)),
    ("Boring tool",                     dict(group="boring",     kind="boring",      size="bore",   test=lambda r: True, opts=("boredepth",), tol=0)),
]
TYPE = dict(TYPES)
REAMER_FILES = ht.REAMER_FILES

def table(mf, tname):
    import os
    g = TYPE[tname]["group"]
    if g == "reamers":
        fn = REAMER_FILES.get(mf)
    elif g in ("taps", "threadmills"):
        fn = ht.HOLE_FILES.get(mf, {}).get(g)
    else:
        fn = tl.MANUFACTURERS.get(mf, {}).get(g)
    return fn if fn and os.path.exists(os.path.join(tb.HERE, fn)) else None

def available_types(mf):
    """Tool types the manufacturer has tools for (a table and at least one tool that passes the type's test)."""
    return [n for n, _ in TYPES if table(mf, n) and rows_for(mf, n)]

def rating(r, letter):
    v = int(_f(r.get("iso_" + letter)))
    if v == 0 and tl.GRADE_FALLBACK.get(r.get("grade")) == letter:
        v = 1
    return v

def rows_for(mf, tname, level_tiers=None):
    spec = TYPE[tname]
    fn = table(mf, tname)
    if not fn:
        return []
    key = "cutter_dia_in" if spec["kind"] == "threadmill" else ("dc_min_mm" if spec["size"] == "bore" else "dia_in")
    rows = [r for r in tb.load_rows(fn) if r.get(key) and spec["test"](r)]
    if spec.get("fix"):
        rows = [spec["fix"](r) for r in rows]
    if mf in LEVEL_MFS and level_tiers is not None and spec["kind"] in LEVEL_KINDS:
        rows = [r for r in rows if (r.get("tier") or "") in level_tiers]
    return rows

def levels_with_tools(mf, tname):
    return [n for n, t in LEVELS if rows_for(mf, tname, t)]

# ---------------- optional limits ----------------
def passes(r, prm):
    if prm.get("loc") and _f(r.get("flute_len_mm")) / MM < prm["loc"] - 1e-6:
        return False
    if prm.get("reach") and (_f(r.get("reach_mm")) or _f(r.get("flute_len_mm"))) / MM < prm["reach"] - 1e-6:
        return False
    if prm.get("reachl4") and _f(r.get("l4_mm")) / MM < prm["reachl4"] - 1e-6:
        return False
    if prm.get("flutes") and int(_f(r.get("flutes"))) != prm["flutes"]:
        return False
    if prm.get("radius_set") and abs(_f(r.get("corner_r_mm")) / MM - prm.get("radius", 0)) > 0.0025:
        return False
    if prm.get("depth"):
        d = _f(r.get("depth_max_mm")) / MM or _f(r.get("flute_len_in"))
        if d < prm["depth"] - 1e-6:
            return False
    if prm.get("through") and (r.get("coolant") or "") != "through":
        return False
    if prm.get("hole") not in (None, "", "any") and (r.get("hole_type") or "") != prm["hole"]:
        return False
    if prm.get("ap") and _f(r.get("lc_mm")) / MM < prm["ap"] - 1e-6:
        return False
    if prm.get("mount") == "shell" and not (r.get("interface") or "").startswith("B"):
        return False
    if prm.get("mount") == "shank" and (r.get("interface") or "")[:1] not in ("A", "T", "W", "Z"):
        return False
    if prm.get("width"):
        w = prm["width"] * MM
        lo, hi = _f(r.get("sb_mm")), _f(r.get("sbmax_mm")) or _f(r.get("sb_mm"))
        if not (lo - 0.1 <= w <= hi + 0.1):
            return False
    if prm.get("threadlen") and _f(r.get("thread_len_mm")) / MM < prm["threadlen"] - 1e-6:
        return False
    if prm.get("form") not in (None, "", "any") and (r.get("form") or "") != prm["form"]:
        return False
    if prm.get("maxcutter") and _f(r.get("cutter_dia_in")) > prm["maxcutter"] + 1e-6:
        return False
    if prm.get("boredepth"):
        reach = (_f(r.get("lc_mm")) or _f(r.get("l4_mm")) * 0.6) / MM
        if reach < prm["boredepth"] - 1e-6:
            return False
    return True

# ---------------- size match ----------------
def dia_of(r, kind=None):
    if kind == "threadmill":
        return _f(r.get("cutter_dia_in"))
    return _f(r.get("dia_in"))

def _match_dia(pool, dia, tol, max_off, larger=False):
    exact = [r for r in pool if abs(dia_of(r) - dia) <= tol]
    if exact:
        return exact, ""
    if not pool:
        return [], ""
    if larger:                                   # spot and insert drills: the nearest larger size, else the largest
        big = [r for r in pool if dia_of(r) >= dia]
        near = min(big, key=lambda r: dia_of(r)) if big else max(pool, key=lambda r: dia_of(r))
    else:
        near = min(pool, key=lambda r: abs(dia_of(r) - dia))
    if max_off is not None and abs(dia_of(near) - dia) > max_off:
        return [], ""
    same = [r for r in pool if abs(dia_of(r) - dia_of(near)) < 1e-6]
    return same, "No tool at %.4f in. Nearest is %.4f in." % (dia, dia_of(near))

def _match_thread(pool, th, kind):
    if kind == "tap":
        want = ht._norm_key(th["key"])
        exact = [r for r in pool if ht._norm_key(ht._row_key(r)) == want]
        if exact:
            return exact, ""
        near = [r for r in pool if ht.same_standard(r, th) and r.get("dia_in") and abs(_f(r["dia_in"]) - th["dia_in"]) < 0.004 and
                abs((1.0 / _f(r["tpi"], 1e9) if r.get("tpi") else _f(r.get("pitch_mm")) / MM) - th["pitch_in"]) < 0.002]
        return near, ("Nearest tap size." if near else "")
    inch = th["std"] != "M"
    out = []
    for r in pool:
        rng = (r.get("thread_range") or "").upper()
        if inch and not any(x in rng for x in ("UNC", "UNF")):
            continue
        if not inch and "M" not in rng:
            continue
        lo, hi = _f(r.get("min_thread_dia_mm")) / MM, _f(r.get("max_thread_dia_mm")) / MM
        if not (lo - 0.003 <= th["dia_in"] <= (hi or lo) + 0.003):
            continue
        pm = _f(r.get("pitch_mm")) / MM
        if pm and abs(pm - th["pitch_in"]) > 0.0015:
            continue
        out.append(r)
    return out, ""

def _match_bore(pool, dia):
    D = dia * MM
    return [r for r in pool if _f(r["dc_min_mm"]) - 1e-6 <= D <= _f(r["dc_max_mm"]) + 1e-6], ""

def match(pool, tname, size, first_pool):
    spec = TYPE[tname]
    if spec["size"] == "thread":
        return _match_thread(pool, size, spec["kind"])
    if spec["size"] == "bore":
        return _match_bore(pool, size)
    larger = spec["kind"] in ("spotdrill", "xdrill", "chamfer")
    if spec["kind"] == "reamer":
        off = spec["tol"]                            # reamers: the exact size only
    elif not first_pool:
        off = None                                   # suitable tools: nearest size, the screen says so
    elif spec.get("solid"):
        off = FIRST_OFF * size + spec["tol"]         # solid end mills: a first-choice tool within 8 percent
    elif spec["kind"] in ("drill", "xdrill", "reamer", "spotdrill"):
        off = spec["tol"]                            # hole tools: a first-choice tool only at the exact size
    else:
        off = max(spec["tol"], 0.08 * size)          # inserted cutters
    if larger and not first_pool:
        off = None
    elif larger:
        off = spec["tol"]
    return _match_dia(pool, size, spec["tol"], off, larger)

def prepare(row, tname, size):
    """Copy of the row with the fields the tool builder expects for this type (thread, bore size, cutter diameter)."""
    spec = TYPE[tname]
    r = dict(row)
    if spec["kind"] == "tap":
        r["dia_in"] = "%.4f" % (_f(r.get("dia_in")) or size["dia_in"]); r["_thread"] = size
    elif spec["kind"] == "threadmill":
        r["dia_in"] = r["cutter_dia_in"]; r["dia_mm"] = r.get("cutter_dia_mm"); r["_thread"] = size
    elif spec["kind"] == "boring":
        D = size * MM
        r["bore_dia_mm"] = D; r["dia_in"] = size; r["dia_mm"] = D
    return r

def is_highfeed(r):
    t = " ".join(str(r.get(k, "")) for k in ("family", "series", "title", "description", "shape")).lower()
    return "high feed" in t or "highfeed" in t or "high-feed" in t

def candidates(mf, tname, material, level_tiers, size, prm, unit_pref="inch", include_highfeed=False):
    """All first-choice tools of the type at the size, after the optional limits.
    Returns dict(rows, note, first, why): rows rated 2 when any fit; else rows rated 1 with first=False; why explains an empty result.
    include_highfeed (primary usage high-feed roughing): high-feed tools rated at least 1 for the material are added even when they
    are not first choice; they carry _nfc = True and are listed as NOT FIRST CHOICE."""
    letter = str(material)[:1].upper()
    rows = rows_for(mf, tname, level_tiers)
    if not rows:
        return dict(rows=[], note="", first=True, why="%s has no %s at this performance level." % (mf, tname))
    rated = [r for r in rows if rating(r, letter) >= 1]
    for r in rated:
        r["_rating"] = rating(r, letter)
    lim = [r for r in rated if passes(r, prm)]
    if not rated:
        return dict(rows=[], note="", first=True, why="No %s %s is rated for ISO %s." % (mf, tname, letter))
    if not lim:
        return dict(rows=[], note="", first=True, why="Rated tools exist, but none meets the limits you entered.")
    top = [r for r in lim if r["_rating"] >= 2]
    got, note = match(top, tname, size, True) if top else ([], "")
    first = bool(got)
    if not got:
        got, note = match(lim, tname, size, False)
        best = [r for r in got if r["_rating"] >= 2]
        if best:
            got, first = best, True                  # first-choice tools, but only at a size further from the request
        elif got:
            note = (note + " " if note else "") + (NOT_FIRST % letter)
    if not got:
        return dict(rows=[], note="", first=True, why="No %s %s at this size meets the limits." % (mf, tname))
    # Kennametal prints the same tool in an inch and a metric catalog: keep the session's system when both exist
    seen = {}
    for r in got:
        k = (r.get("family"), r["designation"], r.get("grade"))
        if k not in seen or (r.get("unit_system") == unit_pref and seen[k].get("unit_system") != unit_pref):
            seen[k] = r
    out = [prepare(r, tname, size) for r in seen.values()]
    if include_highfeed:
        have = set(r["designation"] for r in out)
        hf = [r for r in lim if is_highfeed(r) and r["designation"] not in have]
        hits, _ = match(hf, tname, size, False) if hf else ([], "")
        for r in hits:
            x = prepare(r, tname, size)
            x["_nfc"] = r["_rating"] < 2
            out.append(x)
    return dict(rows=out, note=note, first=first, why="")

def all_candidates(mf, tname, material, size, prm, unit_pref="inch"):
    """Tool generator: every tool of the type at the size (all performance levels, any rating for the material), after the
    optional limits. Each row carries _rating (2 primary, 1 suitable, 0 not rated for the material's ISO class).
    Returns dict(rows, note, first, why) like candidates(); rows are ordered by rating, then performance level."""
    letter = str(material)[:1].upper()
    rows = rows_for(mf, tname, None)
    if not rows:
        return dict(rows=[], note="", first=True, why="%s has no %s in the library." % (mf, tname))
    for r in rows:
        r["_rating"] = rating(r, letter)
    lim = [r for r in rows if passes(r, prm)]
    if not lim:
        return dict(rows=[], note="", first=True, why="No %s %s meets the limits you entered." % (mf, tname))
    spec = TYPE[tname]
    got, note = [], ""
    if spec.get("solid") and spec["size"] not in ("thread", "bore"):
        # solid end mills: every size the selector would accept (within FIRST_OFF of the request), so nothing it shows is missing
        win = FIRST_OFF * size + spec["tol"]
        got = [r for r in lim if abs(dia_of(r) - size) <= win]
        if got and not any(abs(dia_of(r) - size) <= spec["tol"] for r in got):
            note = "No tool at %.4f in. Sizes within %.0f%%: %s in." % (size, FIRST_OFF * 100, ", ".join("%.4f" % d for d in sorted(set(dia_of(r) for r in got))))
    if not got:
        got, note = match(lim, tname, size, False)
    if not got:
        return dict(rows=[], note="", first=True, why="No %s %s at this size meets the limits." % (mf, tname))
    seen = {}
    for r in got:
        k = (r.get("family"), r["designation"], r.get("grade"))
        if k not in seen or (r.get("unit_system") == unit_pref and seen[k].get("unit_system") != unit_pref):
            seen[k] = r
    out = []
    for r in seen.values():
        x = prepare(r, tname, size)
        x["_rating"] = r["_rating"]
        x["_nfc"] = r["_rating"] < 2
        out.append(x)
    out.sort(key=lambda r: (-r["_rating"], abs(dia_of(r, spec["kind"]) - (size if not isinstance(size, dict) else 0)), -int(_f(r.get("tier_rank"))), r.get("family") or "", r["designation"]))
    return dict(rows=out, note=note, first=any(r["_rating"] >= 2 for r in out), why="")

RATING_TEXT = {2: "primary", 1: "suitable", 0: "not rated"}

def rating_label(r, material):
    return "ISO %s %s" % (str(material)[:1].upper(), RATING_TEXT.get(int(r.get("_rating", 0)), "not rated"))

# ---------------- display ----------------
def describe_family(rs):
    r = rs[0]
    desc = (r.get("title") or r.get("series") or r.get("type") or r.get("description") or r.get("insert_type") or "").split("|")[0].strip()
    fl = sorted(set(int(_f(x.get("flutes") or x.get("z"))) for x in rs if _f(x.get("flutes") or x.get("z"))))
    s = (r.get("family") or r["designation"]) + (" (NOT FIRST CHOICE)" if any(x.get("_nfc") for x in rs) else "")
    if desc and desc != s:
        s += " - " + desc[:46]
    if fl:
        s += " - %s fl" % "/".join(str(x) for x in fl[:3])
    return s + " - %d tool%s" % (len(rs), "" if len(rs) == 1 else "s")

def _mmin(r, *cols):
    for c in cols:
        v = _f(r.get(c))
        if v:
            return v / MM
    return 0.0

def describe_tool(r, kind, inch=True):
    parts = [r["designation"]]
    d = dia_of(r, kind)
    if kind == "tap":
        parts.append("thread len %.3f" % _mmin(r, "thread_len_mm"))
        parts.append(r.get("form") or "")
        if r.get("chamfer_form"):
            parts.append("chamfer " + r["chamfer_form"])
    elif kind == "threadmill":
        parts.append("cutter %.4f" % d)
        parts.append("thread len %.3f" % _mmin(r, "thread_len_mm"))
        l4 = _mmin(r, "l4_mm", "neck_len_mm")
        if l4:
            parts.append("reach %.3f" % l4)
    elif kind in ("facemill", "profilemill", "chamfer", "slot", "boring"):
        if kind == "chamfer" and _f(r.get("tip_mm")):
            parts.append("Da %.4f tip %.4f" % (d, _f(r["tip_mm"]) / MM))
        if kind == "boring":
            parts.append("bore %.3f-%.3f" % (_f(r.get("dc_min_mm")) / MM, _f(r.get("dc_max_mm")) / MM))
        if _f(r.get("lc_mm")):
            parts.append("ap %.3f" % (_f(r["lc_mm"]) / MM))
        if _f(r.get("sb_mm")):
            parts.append("width %.3f" % (_f(r["sb_mm"]) / MM))
        if _f(r.get("l4_mm")):
            parts.append("reach %.3f" % (_f(r["l4_mm"]) / MM))
        if r.get("interface"):
            parts.append(r["interface"])
        if r.get("insert_type"):
            parts.append(r["insert_type"][:20])
    else:
        fl = _mmin(r, "flute_len_mm", "depth_max_mm") or _f(r.get("flute_len_in"))
        if fl:
            parts.append("cut %.3f (%.1fxD)" % (fl, fl / d if d else 0))
        rc = _mmin(r, "reach_mm")
        if rc:
            parts.append("reach %.3f" % rc)
        cr = _mmin(r, "corner_r_mm")
        if cr:
            parts.append("rad %.3f" % cr)
    oal = _mmin(r, "oal_mm", "l1_mm") or _f(r.get("oal_in"))
    if oal:
        parts.append("OAL %.3f" % oal)
    sh = _mmin(r, "shank_dia_mm", "d1_mm") or _f(r.get("shank_dia_in"))
    if sh and kind not in ("facemill", "slot", "boring", "chamfer", "profilemill"):
        parts.append("shank %.3f" % sh)
    z = r.get("flutes") or r.get("z")
    if z:
        parts.append("%s fl" % z)
    if r.get("coolant"):
        parts.append(r["coolant"])
    if r.get("grade") and r.get("manufacturer") == "Kennametal":
        parts.append(r["grade"])
    if r.get("unit_system") and inch != (r["unit_system"] == "inch"):
        parts.append("(%s catalog)" % r["unit_system"])
    return " | ".join(p for p in parts if p)

def cut_text(r, kind, material):
    """Short cutting data text for one tool, or 'no catalog cutting data'. Borrowed or standard numbers say so (never shown as
    the tool's own), and Walter data carries the material's limit note."""
    t, c = _cut_text(r, kind, material)
    if c is None:
        return t
    notes = [tb.cut_source(c)]
    if r.get("manufacturer", "Walter") == "Walter":
        notes.append(tb.material_note(material))
    return " | ".join([t] + [n for n in notes if n])

def cut_data(r, kind, material):
    """The cutting data cut_text shows: one set, or purpose -> set for end mills; None without data."""
    return _cut_text(r, kind, material)[1]

def source_note(r, kind, material, purposes=None):
    """'' when the cutting data written to the tool is the tool's own catalog data, else plain words on where it comes from
    (borrowed from another family, standard values, a neighbouring material group). purposes: the end mill sets written."""
    c = cut_data(r, kind, material)
    if c and kind in ("endmill", "profilemill") and purposes:
        c = {k: v for k, v in c.items() if k in purposes} or c
    return tb.cut_source(c) if c else ""

def _cut_text(r, kind, material):
    try:
        if kind in ("endmill", "profilemill"):
            c = tb.endmill_cut(r, material)
            if c:
                x = c.get("Rough - usage 1") or c.get("Rough-HEM - usage 1") or list(c.values())[0]
                return "%d rpm, %.1f ipm, fz %.4f" % (x["rpm"], x["ipm"], x["fz"]), c
        elif kind in ("drill", "spotdrill", "xdrill"):
            c = tb.drill_cut(r, material)
            if c:
                return "%d rpm, %.1f ipm, %.4f ipr" % (c["rpm"], c["ipm"], c["ipr"]), c
        elif kind in ("tap", "threadmill", "reamer"):
            c = ht.cut_for(r, kind, material)
            if c:
                return "%d rpm, %.1f ipm" % (c["rpm"], c["ipm"]), c
    except Exception:
        pass
    return "no catalog cutting data", None

# ---------------- machines (sets the spindle speed limit for all cutting data) ----------------
def machines():
    return tb.load_rows("machines.csv")

def machine_models():
    out = []
    for r in machines():
        if r["model"] not in out:
            out.append(r["model"])
    return out

def spindles(model):
    return [r for r in machines() if r["model"] == model]

def spindle_label(r):
    return "%s - %s rpm, %s kW, %s Nm%s" % (r["spindle"], r["rpm"], r["kw"], r["torque_nm"], (" - " + r["best_for"]) if r.get("best_for") else "")
