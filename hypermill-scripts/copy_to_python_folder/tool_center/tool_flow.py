# tool_flow.py - the screens of the three tool_center paths. Run from tool_center.py.
# Every path shows the same screens up to the size screen:
#   machine model | spindle (its max rpm caps every speed and feed) | manufacturer | tool type and material (starts on the
#   joblist material) | size, every limit for the tool type, primary usage (milling tools)
# Then:
#   wizard     one tool per performance level (the best first-choice tool of each level) -> pick one
#   selector   performance level -> first-choice families (list) -> family -> tools in the family (list) -> tool
#   generator  every family of the type at the size, grouped by the material's rating (primary, suitable, not rated)
#              -> family -> tools in the family (list) -> tool
#   search     the tool type drop-down on screen 4 is a search box (family, series, product name or catalog number:
#              md133, harvi 4, kor 5, X5, H1TE4RA0500...). Several matches -> pick one. Then the same size screen
#              (that tool type's limits) -> every tool of that family at the size, any rating (list) -> tool
# All three end the same way: cutting-data sets (end mills) -> generate -> next.
# First choice = the catalog rates the tool 2 (primary) for the material's ISO class; rated-1 tools are used only when no rated-2
# tool exists at the size and are marked NOT FIRST CHOICE (rules in tool_library/tool_catalog.py). The wizard picks from the same
# tools the selector lists for that level, so the two always agree.
# Every screen after the first has a Back choice; Cancel ends. The last machine, spindle, manufacturer, tool type, material,
# level, size and usage are remembered.
# Logs: C:\Users\Public\Documents\OPEN MIND\tool_wizard_log.txt, tool_selector_log.txt, tool_generator_log.txt
import os, json, tempfile, traceback

# ---------------- SETTINGS ----------------
PY_DIR   = r"C:\Users\Public\Documents\OPEN MIND\python"
LIB_DIR  = os.path.join(PY_DIR, "tool_library")
MAX_SPINDLE_RPM = 12000.0     # used only until a spindle is picked: the spindle's max rpm then caps the cutting data
MAX_BOX_LINES = 30            # screen lines a message box may use (wrapped lines counted), so its OK button stays on screen;
                              # the rest of the list is in the output window and on the next drop-down
BOX_WRAP = 90                 # characters per message box line before it wraps
DROP_MAX = 130                # characters of an option shown in a drop-down (the full text goes to the output window)
LAST_FILE = r"C:\Users\Public\Documents\OPEN MIND\tool_center_last.json"
# ------------------------------------------

MM = 25.4
BACK = "<< Back"
MODES = {"wizard": ("Tool wizard", "tool_wizard_log.txt"),
         "selector": ("Tool selector", "tool_selector_log.txt"),
         "generator": ("Tool generator", "tool_generator_log.txt"),
         "search": ("Tool search", "tool_search_log.txt")}
T = "Tool selector"
LOG_NAME = "tool_selector_log.txt"
lines = []

def log(*a):
    lines.append(" ".join(str(x) for x in a))

def _write_log():
    for p in [os.path.join(r"C:\Users\Public\Documents\OPEN MIND", LOG_NAME),
              os.path.join(os.path.expanduser("~"), "Documents", LOG_NAME),
              os.path.join(tempfile.gettempdir(), LOG_NAME)]:
        try:
            with open(p, "w", encoding="utf-8") as f:
                f.write("\n".join(lines))
            return p
        except Exception:
            continue
    return ""

def load_last():
    for p in (LAST_FILE, os.path.join(tempfile.gettempdir(), "tool_center_last.json")):
        try:
            with open(p, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            continue
    return {}

def save_last(d):
    for p in (LAST_FILE, os.path.join(tempfile.gettempdir(), "tool_center_last.json")):
        try:
            with open(p, "w", encoding="utf-8") as f:
                json.dump(d, f)
            return
        except Exception:
            continue

def _gui():
    import om.cad.gui as g
    return g

def _dialog(title):
    return _gui().InputDialog(title)

def load_lib(folder):
    import sys, importlib
    if folder not in sys.path:
        sys.path.insert(0, folder)
    out = {}
    for n in ("tool_builder", "tool_lookup", "hole_tools", "tool_catalog", "tool_usage"):
        m = importlib.import_module(n)
        importlib.reload(m)       # hyperMILL keeps imported modules between runs
        out[n] = m
    return out

def info(title, text):
    g = _gui()
    g.ShowMessageBox(g.MessageBoxType.INFORMATION, title, text)

def to_output(text):
    try:
        g = _gui()
        try:
            g.CleanOutput(g.UIOutputWindow.ALL)
        except Exception:
            pass
        g.WriteToOutput(text, g.UIOutputWindow.ALL)
    except Exception:
        pass

def _index(v, options, default=0):
    if isinstance(v, int) and not isinstance(v, bool):
        return v if 0 <= v < len(options) else default
    options = list(options)
    return options.index(v) if v in options else default

def pick(title, label, options, default=0, back=True):
    """One drop-down showing the option text (cut at DROP_MAX characters). Returns the index, 'back' or None when cancelled."""
    opts = [str(o) for o in options] + ([BACK] if back else [])
    shown = []
    for o in opts:
        t = o if len(o) <= DROP_MAX else o[:DROP_MAX - 3] + "..."
        while t in shown:                          # identical labels would collapse into one entry
            t += " "
        shown.append(t)
    dlg = _dialog(title)
    dlg.AddDropDown(label, shown, defaultIndex=max(0, min(default, len(shown) - 1)))
    ok, vals = dlg.Show()
    if not ok:
        return None
    i = _index(vals[label], shown)
    return "back" if (back and i == len(shown) - 1) else i

def show_list(title, header, rows):
    """List screen: output window (stays visible) and a message box cut to MAX_BOX_LINES so its OK button stays on screen."""
    def height(t):
        return sum(max(1, -(-len(x) // BOX_WRAP)) for x in str(t).split("\n"))
    used = height(header) + 3
    shown = []
    for r in rows:
        h = height(r)
        if shown and used + h > MAX_BOX_LINES:
            break
        shown.append(r); used += h
    more = len(rows) - len(shown)
    text = header + "\n\n" + "\n".join(shown) + (("\n... and %d more: full list in the output window, all of them on the next drop-down" % more) if more > 0 else "")
    to_output(header + "\n" + "\n".join(rows))
    info(title, text)

def parse_len(text, inch):
    """'0.5', '1/2', '1 1/2' -> inches (entered in session units). Blank -> 0.0. None if unreadable."""
    t = (text or "").strip()
    if not t:
        return 0.0
    try:
        total = 0.0
        for part in t.split():
            if "/" in part:
                a, b = part.split("/"); total += float(a) / float(b)
            else:
                total += float(part)
    except Exception:
        return None
    return total if inch else total / MM

def parse_len_xd(text, inch, base_in):
    """Length as '1.5' (session units) or '3x' / '3xD' (times the diameter). Blank -> 0.0. None if unreadable."""
    t = (text or "").strip().lower().replace(",", ".")
    if not t:
        return 0.0
    try:
        if t.endswith("xd"):
            t = t[:-2]
        if t.endswith("x"):
            return float(t[:-1]) * base_in
    except Exception:
        return None
    return parse_len(t, inch)

# limits per tool type (tool_catalog.TYPES opts): key -> (label, kind); kind 'len' (session units), 'lenx' (units or x diameter),
# 'int', 'bool', list (drop-down)
LIMITS = {               # blank = any; lengths in session units, or times the diameter (3x) where the kind is 'lenx'
    "loc":       ("Min cutting length", "lenx"),
    "reach":     ("Min reach below shank", "len"),
    "radius":    ("Corner radius", "len"),
    "flutes":    ("Flutes", "int"),
    "depth":     ("Min hole depth", "lenx"),
    "through":   ("Through-coolant only", "bool"),
    "hole":      ("Hole type", ["any", "through", "blind"]),
    "threadlen": ("Min thread length", "lenx"),
    "form":      ("Tap form", ["any", "cutting", "forming"]),
    "maxcutter": ("Max cutter diameter", "len"),
    "ap":        ("Min depth of cut ap", "len"),
    "mount":     ("Mount", ["any", "shell", "shank"]),
    "reachl4":   ("Min reach", "len"),
    "width":     ("Slot width", "len"),
    "boredepth": ("Min bore depth", "len"),
}
LENGTH_LIMITS = ("loc", "reach", "reachl4", "depth", "threadlen", "ap", "boredepth")

# ---------------- wizard: the best tool of a level ----------------
SPOT_FAMILIES = ("A1174", "A1174C", "A1114", "A1115", "K1161XPL", "K1161")
XDRILL_ORDER = {"D5150": 0, "D4140": 1, "D5142": 2, "D4240": 3, "D4120": 4, "D3120": 5, "D4170": 6, "B3212": 7, "B3213": 7, "B3214": 7}
BORING_MOUNT_ORDER = {"N": 0, "C": 1, "T": 2}      # cylindrical shank, Capto, ScrewFit

def _boring_mount(r):
    d = r["designation"]
    ch = d.split("-")[-2][:1] if "-" in d else ""
    if "." in d and "-" not in d[:6]:
        ch = d.split(".")[1][:1]
    return BORING_MOUNT_ORDER.get(ch, 3)

def tool_length_mm(r):
    """The length a length limit checks: cutting / thread / hole depth / depth of cut / reach (mm)."""
    f = lambda k: _num(r.get(k))
    return max(f("flute_len_mm"), f("reach_mm"), f("depth_max_mm"), f("thread_len_mm"), f("lc_mm"), f("l4_mm"), f("flute_len_in") * MM)

def _num(x, d=0.0):
    try:
        return float(x)
    except Exception:
        return d

def wizard_key(tc, tl, r, kind, size, mat):
    """Order of the tools a level offers (best first): first choice, nearest size, higher tier, has catalog cutting data,
    the session's unit system, then the type's own preference (the rules the wizard used before)."""
    dist = abs(tc.dia_of(r, kind) - size) if isinstance(size, float) else 0.0
    base = (bool(r.get("_nfc")), round(dist / 0.0005), -int(_num(r.get("tier_rank"))),
            0 if tc.cut_data(r, kind, mat) is not None else 1, tl._unit_rank(r))
    if kind == "endmill":
        tail = (_num(r.get("flute_len_mm")),)
    elif kind == "drill":
        tail = (0 if r.get("coolant") == "through" else 1, _num(r.get("depth_max_mm")))
    elif kind == "spotdrill":
        tail = (0 if r.get("family") in SPOT_FAMILIES else 1, _num(r.get("oal_mm")))
    elif kind == "xdrill":
        tail = (_num(r.get("flute_len_in")), XDRILL_ORDER.get(r.get("family"), 9))
    elif kind == "facemill":
        want = ("B",) if isinstance(size, float) and size >= 2.0 else ("A", "T", "W", "Z")
        tail = (0 if (r.get("interface") or "")[:1] in want else 1, -int(_num(r.get("flutes"))), _num(r.get("lc_mm")))
    elif kind == "profilemill":
        tail = (_num(r.get("l4_mm")), (r.get("interface") or "")[:1] not in ("A", "T", "W"))
    elif kind == "chamfer":
        tail = ((r.get("interface") or "")[:1] not in ("A", "T"), _num(r.get("oal_mm")))
    elif kind == "slot":
        tail = (-int(_num(r.get("z"))),)
    elif kind == "boring":
        tail = (_boring_mount(r), _num(r.get("dc_max_mm")) - _num(r.get("dc_min_mm")),
                _num(r.get("lc_mm")) or _num(r.get("l4_mm")) * 0.6)
    else:                                            # tap, thread mill, reamer
        tail = (_num(r.get("thread_len_mm")) or _num(r.get("flute_len_mm")), _num(r.get("oal_mm")))
    return base + tail + (r["designation"],)

def wizard_best(tc, tl, tu, mf, rows, kind, size, mat, usage):
    """(row, usage reason): the tool the wizard offers for one level, picked from the selector's tools for that level."""
    if usage and kind in tu.MILL_KINDS:
        fams = {}
        for r in rows:
            fams.setdefault(r.get("family") or r["designation"], []).append(r)
        base_key = lambda f: (-max(int(tc._f(x.get("tier_rank"))) for x in fams[f]), f)
        names, why = tu.order_families(mf, fams, usage, mat, base_key)
        best = tu.order_tools(fams[names[0]], usage)[0]
        return best, why.get(names[0]) or "catalog order"
    return min(rows, key=lambda r: wizard_key(tc, tl, r, kind, size, mat)), ""

# ---------------- search: family, series, product name or catalog number ----------------
NAME_FILES = {"Kennametal": "kennametal_names.csv"}      # product names printed in the catalog (HARVI IV = HA4R ...)
ROMAN = {"i": "1", "ii": "2", "iii": "3", "iv": "4", "v": "5", "vi": "6", "vii": "7", "viii": "8", "ix": "9", "x": "10"}
MAX_MATCHES = 60          # families shown on the match list
MAX_DIRECT = 40           # a catalog-number search with this many matching tools or fewer lists them without the size screen
SIZE_KINDS = ("tap", "threadmill", "boring")      # tools that need the thread or bore size to be built: never skip the size screen
END_MILLS = ("Flat end mill", "Radius end mill", "Ball end mill")   # one search match per family; the corner radius picks the shape
SEARCH_END_MILL = "End mill"                 # a family's flat, radius and ball end mills; the size screen has a Tool type drop-down
RADIUS_TOL_IN = 0.0025

def tokens(text):
    import re, unicodedata
    t = str(text or "")
    for ch in ("\u2122", "\u00ae", "\u00b7", "\u2219"):          # trade mark, registered, the dots in X\u00b7pert and Thread\u2219tec
        t = t.replace(ch, "")
    t = unicodedata.normalize("NFKC", t).lower()                # the fi ligature in the Kennametal tables -> fi
    return re.findall(r"[a-z0-9]+", t)

def norm(text):
    """Search form of a text: lower case, letters and digits only (spaces, dashes, dots, slashes dropped), and a roman numeral
    I to X that follows a word of two or more letters becomes its number: 'HARVI IV', 'harvi 4' and 'Harvi-4' all give 'harvi4';
    'X 5' stays 'x5' (no word before the X)."""
    out, prev = [], ""
    for t in tokens(text):
        out.append(ROMAN[t] if (t in ROMAN and prev.isalpha() and len(prev) >= 2) else t)
        prev = t
    return "".join(out)

def product_names(tb, mf):
    fn = NAME_FILES.get(mf)
    if not fn or not os.path.exists(os.path.join(tb.HERE, fn)):
        return {}
    return {r["family"]: r["name"] for r in tb.load_rows(fn)}

def _unique(rows):
    seen, out = set(), []
    for r in rows:
        k = (r["designation"], r.get("grade"))
        if k not in seen:
            seen.add(k); out.append(r)
    return out

def _mf_files(tl, ht, tc, mf):
    files = list(tl.MANUFACTURERS.get(mf, {}).values()) + list(ht.HOLE_FILES.get(mf, {}).values())
    if tc.REAMER_FILES.get(mf):
        files.append(tc.REAMER_FILES[mf])
    return [f for i, f in enumerate(files) if f and f not in files[:i]]

def _score_family(q, fam, name, series_values):
    """4: family code or product name starts with the search; 3: family code, series or product name contains it; 0 else."""
    code, nm = norm(fam), norm(name)
    if code.startswith(q) or (nm and nm.startswith(q)):
        return 4
    if q in code or (nm and q in nm) or any(q in norm(v) for v in series_values):
        return 3
    return 0

def search(tb, tl, ht, tc, mf, query, other_mfs=True):
    """Families of one manufacturer matching the search, best first.
    Returns dict(matches, total, unbuildable, elsewhere):
      matches     [dict(score, tname, family, name, rows, hits)] at the best score found, at most MAX_MATCHES;
                  hits = the matching catalog numbers when the search matched catalog numbers (score 2), else []
      total       how many families matched at that score (more than MAX_MATCHES means the list was cut)
      unbuildable families in the tables that match but belong to no tool type yet: [(family, what it is, file)]
      elsewhere   when nothing matches here: [(manufacturer, [family / product name, ...])] that do match
    Scores: 4 family code or product name starts with it, 3 family code / series / product name contains it,
            2 catalog number (designation or EDP) contains it, 1 description / title / type contains it."""
    q = norm(query)
    out = dict(matches=[], total=0, unbuildable=[], elsewhere=[])
    if not q:
        return out
    names = product_names(tb, mf)
    groups = {}
    for tname in tc.available_types(mf):
        gt = SEARCH_END_MILL if tname in END_MILLS else tname
        for r in tc.rows_for(mf, tname):
            r["_tname"] = tname
            fam = r.get("family") or r["designation"]
            g = groups.setdefault((gt, fam), dict(rows=[], series=set(), text=set(), hits=[]))
            g["rows"].append(r)
            g["series"].add(r.get("series") or "")
            for k in ("description", "title", "type", "insert_type", "kind"):
                if r.get(k):
                    g["text"].add(r[k])
            if q in norm(r["designation"]) or (r.get("edp") and q == norm(r["edp"])):
                g["hits"].append(r["designation"])
    scored = []
    for (gt, fam), g in groups.items():
        sc = _score_family(q, fam, names.get(fam, ""), g["series"])
        if not sc and g["hits"]:
            sc = 2
        if not sc and any(q in norm(t) for t in g["text"]):
            sc = 1
        if sc:
            scored.append(dict(score=sc, tname=gt, family=fam, name=names.get(fam, ""), rows=g["rows"],
                               hits=sorted(set(g["hits"])) if sc == 2 else []))
    reach = set(f for _, f in groups)
    # families that match but no tool type takes them (routers, barrel mills, HSS drills ...): say so instead of "nothing"
    for fn in _mf_files(tl, ht, tc, mf):
        if not os.path.exists(os.path.join(tb.HERE, fn)):
            continue
        seen = {}
        for r in tb.load_rows(fn):
            fam = r.get("family") or r.get("designation") or ""
            if not fam or fam in reach or fam in seen:
                continue
            if _score_family(q, fam, names.get(fam, ""), [r.get("series") or ""]) or q in norm(r.get("designation")):
                what = r.get("shape") or r.get("type") or r.get("kind") or ""
                if r.get("thread") and "drill" in what.lower():
                    what += " (step drill for thread %s)" % r["thread"]
                seen[fam] = what
        out["unbuildable"] += [(f, w, fn) for f, w in seen.items()]
    if scored:
        top = max(m["score"] for m in scored)
        order = [SEARCH_END_MILL] + [n for n, _ in tc.TYPES]
        best = sorted([m for m in scored if m["score"] == top], key=lambda m: (m["name"] or m["family"], order.index(m["tname"]), m["family"]))
        out["total"] = len(best)
        out["matches"] = best[:MAX_MATCHES]
    elif other_mfs:
        for mf2 in tl.MANUFACTURERS:
            if mf2 == mf:
                continue
            r2 = search(tb, tl, ht, tc, mf2, query, other_mfs=False)
            labels = []
            for m in r2["matches"]:
                lab = (m["name"] + " " if m["name"] else "") + m["family"]
                if lab not in labels:
                    labels.append(lab)
            if labels:
                out["elsewhere"].append((mf2, labels))
    return out

def match_shapes(m):
    """Tool types in a search match: the end mill shapes the family has (Flat / Radius / Ball end mill), else its one type."""
    if m["tname"] != SEARCH_END_MILL:
        return [m["tname"]]
    have = set(r.get("_tname") for r in m["rows"])
    return [t for t in END_MILLS if t in have]

def match_label(tc, m):
    rows = _unique(m["rows"])
    kind_txt = m["tname"] if m["tname"] != SEARCH_END_MILL else "End mill: " + " / ".join(t.split()[0].lower() for t in match_shapes(m))
    lab = "%s | %s%s" % (kind_txt, (m["name"] + " - ") if m["name"] else "", tc.describe_family(rows))
    if m["hits"]:
        lab += " - %d match%s the catalog number" % (len(m["hits"]), "es" if len(m["hits"]) != 1 else "")
    return lab

def search_spec(tc, tname):
    """Tool type rules for a search match (the three end mill shapes are one match: corner radius first on the size screen)."""
    if tname == SEARCH_END_MILL:
        return dict(tc.TYPE["Radius end mill"], opts=("radius", "loc", "reach", "flutes"))
    return tc.TYPE[tname]

def direct_tools(tc, m, material):
    """Catalog-number search: the matching tools themselves (no size screen). Kinds that need a thread or bore size are not
    listed this way."""
    letter = str(material)[:1].upper()
    tname = "Radius end mill" if m["tname"] == SEARCH_END_MILL else m["tname"]
    want = set(m["hits"])
    out = []
    for r in _unique([r for r in m["rows"] if r["designation"] in want]):
        x = tc.prepare(r, tname, tc.dia_of(r))
        x["_rating"] = tc.rating(r, letter)
        x["_nfc"] = x["_rating"] < 2
        out.append(x)
    out.sort(key=lambda r: (-r["_rating"], tc.dia_of(r), tc._f(r.get("corner_r_mm")), tc._f(r.get("flute_len_mm") or r.get("depth_max_mm") or r.get("lc_mm")), r["designation"]))
    return out

def family_tools(tc, mf, m, material, size, prm, unit_pref, shape="Any"):
    """Every tool of one search match at the size (any rating for the material), after the limits.
    Solid end mills and chamfer mills: every size within tool_catalog.FIRST_OFF (8 percent) of the request, like the generator;
    else the exact size, else the family's nearest size. Corner radius (search end mills): checked after the size, so a
    ball end mill whose radius is half of its own diameter counts when the radius entered is half the requested diameter.
    A catalog-number search keeps only the matching catalog numbers. Returns dict(rows, note, why)."""
    letter = str(material)[:1].upper()
    merged = m["tname"] == SEARCH_END_MILL
    tname = "Radius end mill" if merged else m["tname"]
    spec = tc.TYPE[tname]
    rows = [r for r in m["rows"]]
    if merged and shape in END_MILLS:            # Tool type picked on the size screen
        rows = [r for r in rows if r.get("_tname") == shape]
    if m["hits"]:
        want = set(m["hits"])
        rows = [r for r in rows if r["designation"] in want]
    for r in rows:
        r["_rating"] = tc.rating(r, letter)
    want_r = prm.get("radius") if (merged and prm.get("radius_set")) else None
    lim = [r for r in rows if tc.passes(r, dict(prm, radius_set=False) if merged else prm)]
    if not lim:
        return dict(rows=[], note="", why="No %s tool meets the limits you entered." % m["family"])
    def radius_ok(r):
        if want_r is None:
            return True
        if r.get("shape") == "Ball":
            return abs(want_r - size / 2) <= RADIUS_TOL_IN or abs(want_r - tc.dia_of(r) / 2) <= RADIUS_TOL_IN
        return abs(tc._f(r.get("corner_r_mm")) / tc.MM - want_r) <= RADIUS_TOL_IN
    note = ""
    got = []
    if spec["size"] == "dia" and (spec.get("solid") or spec["kind"] == "chamfer"):
        win = tc.FIRST_OFF * size + spec["tol"]
        got = [r for r in lim if abs(tc.dia_of(r) - size) <= win and radius_ok(r)]
        if got and not any(abs(tc.dia_of(r) - size) <= spec["tol"] for r in got):
            note = "No tool at %.4f in. Sizes within %.0f%%: %s in." % (size, tc.FIRST_OFF * 100, ", ".join("%.4f" % d for d in sorted(set(tc.dia_of(r) for r in got))))
    if not got:
        pool = [r for r in lim if radius_ok(r)]
        if not pool:
            radii = sorted(set(round((tc.dia_of(r) / 2) if r.get("shape") == "Ball" else tc._f(r.get("corner_r_mm")) / tc.MM, 4) for r in lim))
            return dict(rows=[], note="", why="No %s tool has a %.4f in corner radius. Radii in this family: %s in." % (
                m["family"], want_r, ", ".join("%.4f" % x for x in radii[:12])))
        got, note = tc.match(pool, tname, size, False)
    if not got:
        return dict(rows=[], note="", why="No %s tool at this size." % m["family"])
    seen = {}
    for r in got:
        k = (r["designation"], r.get("grade"))
        if k not in seen or (r.get("unit_system") == unit_pref and seen[k].get("unit_system") != unit_pref):
            seen[k] = r
    out = []
    for r in seen.values():
        x = tc.prepare(r, tname, size)
        x["_rating"] = r["_rating"]
        x["_nfc"] = r["_rating"] < 2
        out.append(x)
    out.sort(key=lambda r: (-r["_rating"], abs(tc.dia_of(r, spec["kind"]) - (size if not isinstance(size, dict) else 0)),
                            tc._f(r.get("corner_r_mm")), tc._f(r.get("flute_len_mm") or r.get("thread_len_mm") or r.get("depth_max_mm") or r.get("lc_mm")),
                            tc._f(r.get("oal_mm") or r.get("l1_mm")), r["designation"], r.get("grade", "")))
    return dict(rows=out, note=note, why="")

def no_match_text(mf, query, res):
    """Message when the search finds nothing that can be built."""
    t = ["Nothing in the %s tables that can be built matches '%s'." % (mf, query)]
    if res["unbuildable"]:
        t.append("In the %s tables but no tool type for it yet:" % mf)
        t += ["  %s - %s (%s)" % (f, w or "other tool", fn) for f, w, fn in res["unbuildable"][:12]]
    for mf2, labels in res["elsewhere"]:
        t.append("Found under %s: %s%s. Pick %s on the manufacturer screen." % (mf2, ", ".join(labels[:8]), " ..." if len(labels) > 8 else "", mf2))
    if not res["unbuildable"] and not res["elsewhere"]:
        t.append("Search by family (MD133, H1TE, X5, TD117), product name (HARVI IV, KOR 5), series or catalog number.")
    return "\n".join(t)

def run(model=None, default_mat=None, mode="selector"):
    """mode: 'wizard', 'selector' or 'generator'. default_mat: material picked first on the material drop-down (tool_center
    reads it from the document's joblists)."""
    global T, LOG_NAME
    T, LOG_NAME = MODES.get(mode, MODES["selector"])
    wiz, gen, srch = mode == "wizard", mode == "generator", mode == "search"
    lines.clear()
    log("mode:", mode, "| material from the joblists:", default_mat or "none")
    try:
        lib = load_lib(LIB_DIR)
        tb, tl, ht, tc, tu = lib["tool_builder"], lib["tool_lookup"], lib["hole_tools"], lib["tool_catalog"], lib["tool_usage"]
        tb.MAX_RPM = MAX_SPINDLE_RPM
        if model is None:
            import om
            model = om.Application().CurrentDocument.CamModel
        inch = bool(model.IsInchMode() if callable(model.IsInchMode) else model.IsInchMode)
        u = "in" if inch else "mm"
        tl.UNIT_PREF = "inch" if inch else "metric"
        jt = tb.JobTools()
        materials = [r["hypermill_material"] for r in tb.load_rows("material_map.csv")]
        last = load_last()
        step = "machine"
        machine = spindle = None
        mf = tname = mat = None
        spec = kind = None
        size = None; size_text = ""; prm = {}; thread_tool = False
        usage = ""                 # primary usage key ('' = any): orders families and tools, pre-ticks the matching cutting-data set
        level_name, level_tiers = "", None
        res = None; fams = {}; fam_names = []; fam = None; sizes = []; row = None
        row_note = ""; row_first = True; level_screen = False
        query = last.get("search", ""); matches = []; found = None; m_sel = None; direct = False
        shape = "Any"              # search end mills: the tool type picked on the size screen
        while True:
            # ================= shared screens =================
            if step == "machine":
                models = tc.machine_models()
                i = pick(T, "Machine model", models, default=models.index(last["machine"]) if last.get("machine") in models else 0, back=False)
                if i is None:
                    break
                machine = models[i]; step = "spindle"
            elif step == "spindle":        # its maximum speed limits every speed and feed below
                sps = tc.spindles(machine)
                names = [r["spindle"] for r in sps]
                i = pick("%s | %s" % (T, machine), "Spindle", [tc.spindle_label(r) for r in sps], default=names.index(last["spindle"]) if last.get("spindle") in names else 0)
                if i is None:
                    break
                if i == "back":
                    step = "machine"; continue
                spindle = sps[i]
                tb.MAX_RPM = float(spindle["rpm"])
                last.update(machine=machine, spindle=spindle["spindle"]); save_last(last)
                log("machine:", machine, "| spindle:", spindle["spindle"], "| max rpm", spindle["rpm"])
                step = "mf"
            elif step == "mf":
                mfs = list(tl.MANUFACTURERS)
                i = pick("%s | %s %s %s rpm" % (T, machine, spindle["spindle"], spindle["rpm"]), "Manufacturer", mfs, default=mfs.index(last["mf"]) if last.get("mf") in mfs else 0)
                if i is None:
                    break
                if i == "back":
                    step = "spindle"; continue
                mf = mfs[i]; step = "type"
            elif step == "type":           # tool type and material
                types = tc.available_types(mf)
                if not types:
                    info(T, "%s has no tool catalogs loaded." % mf)
                    step = "mf"; continue
                dlg = _dialog("%s | %s" % (T, mf))
                if srch:
                    dlg.AddText("Search", defaultValue=query)
                else:
                    dlg.AddDropDown("Tool type", types, defaultIndex=types.index(tname or last.get("tname")) if (tname or last.get("tname")) in types else 0)
                dm = mat if mat in materials else (default_mat if default_mat in materials else
                     (last.get("mat") if last.get("mat") in materials else ("N - Aluminum" if "N - Aluminum" in materials else materials[0])))
                dlg.AddDropDown("Material", materials, defaultIndex=materials.index(dm))
                dlg.AddBool("Back to previous screen", defaultValue=False)
                ok, vals = dlg.Show()
                if not ok:
                    break
                def val_of(prefix, vals=vals):
                    for k, v in vals.items():
                        if str(k).startswith(prefix):
                            return v
                    return None
                if val_of("Back"):
                    step = "mf"; continue
                mat = materials[_index(val_of("Material"), materials)]
                if srch:
                    query = str(val_of("Search") or "").strip()
                    if not norm(query):
                        info(T, "Type a family (MD133, H1TE, X5, TD117), product name (HARVI IV, KOR 5), series or catalog number.")
                        continue
                    found = search(tb, tl, ht, tc, mf, query)
                    matches = found["matches"]
                    last.update(mf=mf, mat=mat, search=query); save_last(last)
                    log("search:", mf, repr(query), "| normalized", norm(query), "|", found["total"], "match(es):",
                        [(m_["family"], m_["tname"], m_["score"], len(m_["hits"])) for m_ in matches][:20],
                        "| no tool type yet:", [f for f, _, _ in found["unbuildable"]], "| elsewhere:", found["elsewhere"])
                    if not matches:
                        info(T, no_match_text(mf, query, found))
                        continue
                    step = "match"; continue
                new_t = types[_index(val_of("Tool type"), types)]
                if new_t != tname:
                    size_text = ""
                tname = new_t
                mat = materials[_index(val_of("Material"), materials)]
                spec = tc.TYPE[tname]; kind = spec["kind"]
                step = "size"
            elif step == "match":          # search: pick one of the matching families
                if len(matches) == 1:
                    k = 0
                else:
                    head = "%s | '%s' | %d matching famil%s%s" % (mf, query, found["total"], "y" if found["total"] == 1 else "ies",
                           (" | first %d shown, type more to narrow it" % MAX_MATCHES) if found["total"] > MAX_MATCHES else "")
                    if found["unbuildable"]:
                        head += "\nAlso in the tables, no tool type for it yet: " + ", ".join("%s (%s)" % (f, w or "other") for f, w, _ in found["unbuildable"][:8])
                    show_list(T + " - matches", head, ["%d. %s" % (n + 1, match_label(tc, m_)) for n, m_ in enumerate(matches)])
                    k = pick(T, "Match", [match_label(tc, m_) for m_ in matches])
                    if k is None:
                        break
                    if k == "back":
                        step = "type"; continue
                m_sel = matches[k]
                if m_sel["tname"] != tname or m_sel["family"] != fam:
                    size_text = ""; prm = {}; shape = "Any"
                tname, fam = m_sel["tname"], m_sel["family"]
                spec = search_spec(tc, tname)
                kind = spec["kind"]
                direct = bool(m_sel["hits"]) and len(m_sel["hits"]) <= MAX_DIRECT and kind not in SIZE_KINDS
                if direct:                 # catalog number: the matching tools themselves, no size screen
                    usage = ""; size_text = ""
                    step = "direct"
                else:
                    step = "size"
            elif step == "direct":
                sizes = direct_tools(tc, m_sel, mat)
                res = dict(rows=sizes, note="", first=True, why="")
                nm_ = m_sel["name"]
                level_name = "search '%s': %s%s" % (query, (nm_ + " ") if nm_ else "", fam)
                show_list(T + " - " + fam, "%s%s | %s | catalog numbers matching '%s' | %d tool%s | cutting data for %s, %s %s max %s rpm" % (
                              (nm_ + " - ") if nm_ else "", fam, tname, query, len(sizes), "" if len(sizes) == 1 else "s", mat, machine,
                              spindle["spindle"], spindle["rpm"]),
                          ["%d. [%s] %s\n      %s" % (n + 1, tc.rating_label(r, mat), tc.describe_tool(r, kind, inch), tc.cut_text(r, kind, mat)) for n, r in enumerate(sizes)])
                step = "tool"
            elif step == "size":           # size, every limit for the type, primary usage
                thread_tool = spec["size"] == "thread"
                dlg = _dialog("%s | %s | %s | %s" % (T, mf, (fam + " | " + tname) if srch else tname, mat))
                if srch:                       # the search remembers its own last size, per manufacturer, family and type
                    remembered = last.get("search_size") if last.get("search_key") == [mf, fam, tname] else ""
                else:
                    remembered = last.get("size_text") if last.get("tname") == tname else ""
                st_ = size_text or remembered or ("1/4-20 UNC" if thread_tool else "0.5")
                shapes = match_shapes(m_sel) if (srch and tname == SEARCH_END_MILL) else []
                if len(shapes) > 1:
                    if shape not in shapes and last.get("search_key") == [mf, fam, tname]:
                        shape = last.get("search_shape", "Any")
                    opts_ = ["Any"] + shapes
                    dlg.AddDropDown("Tool type", opts_, defaultIndex=opts_.index(shape) if shape in opts_ else 0)
                if thread_tool:
                    dlg.AddText("Thread", defaultValue=st_)
                else:
                    size_label = "Bore diameter" if spec["size"] == "bore" else ("Large diameter Da" if kind == "chamfer" else "Diameter")
                    dlg.AddText(size_label, defaultValue=st_)
                for key in spec["opts"]:
                    label, lk = LIMITS[key]
                    if lk == "bool":
                        dlg.AddBool(label, defaultValue=bool(prm.get(key)))
                    elif isinstance(lk, list):
                        dlg.AddDropDown(label, lk, defaultIndex=lk.index(prm[key]) if prm.get(key) in lk else 0)
                    else:
                        dlg.AddText(label, defaultValue="")
                milling = kind in tu.MILL_KINDS
                if milling:
                    du = [l for k_, l, _ in tu.USAGES if k_ == usage][0] if usage else (last.get("usage") if last.get("usage") in tu.USAGE_LABELS else tu.USAGE_LABELS[0])
                    dlg.AddDropDown("Primary usage", tu.USAGE_LABELS, defaultIndex=tu.USAGE_LABELS.index(du))
                dlg.AddBool("Back to previous screen", defaultValue=False)
                ok, vals = dlg.Show()
                if not ok:
                    break
                def val_of(prefix, vals=vals):
                    for k, v in vals.items():
                        if str(k).startswith(prefix):
                            return v
                    return None
                if val_of("Back"):
                    step = "match" if (srch and len(matches) > 1) else "type"; continue
                if len(shapes) > 1:
                    shape = (["Any"] + shapes)[_index(val_of("Tool type"), ["Any"] + shapes)]
                else:
                    shape = shapes[0] if shapes else "Any"
                if thread_tool:
                    size_text = str(val_of("Thread") or "").strip()
                    size = ht.parse_thread(size_text)
                    if size is None:
                        info(T, "Thread could not be read. Use 1/4-20 UNC, #10-32 UNF, M6 or M8x1.")
                        continue
                    base = size["dia_in"]
                else:
                    size_text = str(val_of(size_label) or "").strip()
                    size = parse_len(size_text, inch)
                    if not size:
                        info(T, "Diameter could not be read. Use numbers like 0.5 or 1/2.")
                        continue
                    base = size
                usage = tu.usage_key(tu.USAGE_LABELS[_index(val_of("Primary usage"), tu.USAGE_LABELS)]) if milling else ""
                prm, bad = {}, False
                for key in spec["opts"]:
                    label, lk = LIMITS[key]
                    raw = val_of(label.split(" (")[0].split("%")[0].strip())
                    if lk == "bool":
                        prm[key] = bool(raw)
                    elif isinstance(lk, list):
                        prm[key] = lk[_index(raw, lk)]
                    elif lk == "int":
                        try:
                            prm[key] = int(str(raw or "").strip() or 0)
                        except Exception:
                            bad = True
                    else:
                        v = parse_len_xd(str(raw or ""), inch, base) if lk == "lenx" else parse_len(str(raw or ""), inch)
                        if v is None:
                            bad = True
                        else:
                            prm[key] = v
                            if key == "radius":
                                prm["radius_set"] = bool(str(raw or "").strip())
                if bad:
                    info(T, "A limit could not be read. Use numbers like 1.5, 1/2 or 3x.")
                    continue
                last.update(mf=mf, mat=mat)
                if srch:
                    last.update(search_size=size_text, search_key=[mf, fam, tname], search_shape=shape)
                else:
                    last.update(tname=tname, size_text=size_text)
                if milling:
                    last["usage"] = [l for k_, l, _ in tu.USAGES if k_ == usage][0]
                save_last(last)
                log("request:", mf, tname, ("| tool type " + shape) if srch else "", "| material", mat, "| size", size_text, "| limits", prm, "| usage", usage or "any")
                step = "wizard" if wiz else ("found" if srch else ("families" if gen else "level"))
            # ================= wizard: one tool per performance level =================
            elif step == "wizard":
                levels = tc.LEVELS if (mf in tc.LEVEL_MFS and kind in tc.LEVEL_KINDS) else [("All levels" if mf in tc.LEVEL_MFS else "Standard", None)]
                options = []          # (level, row, note, first, length_short)
                whys = []
                for gname, tset in levels:
                    c = tc.candidates(mf, tname, mat, tset, size, prm, tl.UNIT_PREF, include_highfeed=(usage == "rough"))
                    short = False
                    if not c["rows"] and any(prm.get(k) for k in LENGTH_LIMITS):
                        loose = {k: v for k, v in prm.items() if k not in LENGTH_LIMITS}
                        c2 = tc.candidates(mf, tname, mat, tset, size, loose, tl.UNIT_PREF, include_highfeed=(usage == "rough"))
                        if c2["rows"]:
                            pool = [r for r in c2["rows"] if not r.get("_nfc")] or c2["rows"]
                            far = max(tool_length_mm(r) for r in pool)
                            pool = [r for r in pool if tool_length_mm(r) >= far - 1e-6]
                            r_ = min(pool, key=lambda r: wizard_key(tc, tl, r, kind, size, mat))
                            note = "REQUESTED LENGTH NOT AVAILABLE at this level; closest is " + tc.describe_tool(r_, kind, inch)
                            if c2["note"]:
                                note = c2["note"] + " | " + note
                            options.append((gname, r_, note, c2["first"] and not r_.get("_nfc"), True))
                            short = True
                    if not c["rows"]:
                        if not short:
                            whys.append("%s: %s" % (gname, c["why"]))
                        continue
                    r_, why = wizard_best(tc, tl, tu, mf, c["rows"], kind, size, mat, usage)
                    notes = [c["note"]]
                    if why:
                        notes.append("best fit for %s: %s" % ([l for k_, l, _ in tu.USAGES if k_ == usage][0], why))
                    if r_.get("_nfc") and c["first"]:
                        notes.append("NOT FIRST CHOICE for this material (high-feed tool, catalog rates it suitable)")
                    notes.append(tc.source_note(r_, kind, mat))
                    if mf != "Walter" and r_.get("unit_system"):
                        notes.append("%s catalog%s" % (r_["unit_system"], " (not your session unit)" if (r_["unit_system"] == "inch") != inch else ""))
                    options.append((gname, r_, " | ".join(n for n in notes if n), c["first"] and not r_.get("_nfc"), False))
                if not options:
                    log("no tool:", whys)
                    info(T, "No tool found.\n" + "\n".join(whys) + "\nChange the size or limits, or go back.")
                    step = "size"; continue
                def short_label(t, r_, n_, first_, short_):
                    """Level | designation | size and lengths | flags (the full note goes to the output window)."""
                    try:
                        desc = tc.describe_tool(r_, kind, inch).split(" | ", 1)
                    except Exception:
                        desc = [r_["designation"]]
                    d_ = tc.dia_of(r_, kind)
                    flags = []
                    if not first_:
                        flags.append("NOT 1ST CHOICE")
                    if short_:
                        flags.append("LENGTH SHORT")
                    low = (n_ or "").lower()
                    if "nearest" in low:
                        flags.append("nearest size")
                    if "borrowed" in low:
                        flags.append("borrowed data")
                    if "standard reaming" in low or "reamer data used" in low:
                        flags.append("standard data")
                    if "data used (catalog prints no" in low:
                        flags.append("other group data")
                    return " | ".join(x for x in [t] + flags + [r_["designation"], ("dia %.4f" % d_) if d_ and not thread_tool else "",
                                                           desc[1] if len(desc) > 1 else ""] if x)
                to_output("%s | %s | %s | %s | %s\n" % (machine + " " + spindle["spindle"], mf, tname, mat, size_text) +
                          "\n".join("%s | %s%s" % (t, r_["designation"], (" | " + n_) if n_ else "") for t, r_, n_, _, _ in options))
                k = pick(T, "Performance level", [short_label(*o) for o in options])
                if k is None:
                    break
                if k == "back":
                    step = "size"; continue
                level_name, row, row_note, row_first, _ = options[k]
                log("offered:", [(o[0], o[1]["designation"], o[4]) for o in options])
                step = "tecsets"
            # ================= selector: performance level =================
            elif step == "level":
                level_screen = mf in tc.LEVEL_MFS and kind in tc.LEVEL_KINDS
                if level_screen:
                    found, missing = [], []
                    for gname, tset in tc.LEVELS:
                        c = tc.candidates(mf, tname, mat, tset, size, prm, tl.UNIT_PREF, include_highfeed=(usage == "rough"))
                        if c["rows"]:
                            found.append((gname, tset, c))
                        else:
                            missing.append(gname)
                    if not found:
                        have = tc.levels_with_tools(mf, tname)
                        info(T, "No tool found at any performance level.\n" + ("Levels with this tool type: %s.\n" % ", ".join(have) if have else "") +
                             "Change the size or limits, or go back.")
                        step = "size"; continue
                    def lv_label(gname, c):
                        nf = len(set(r.get("family") or r["designation"] for r in c["rows"]))
                        return "%s - %d famil%s, %d tool%s%s" % (gname, nf, "y" if nf == 1 else "ies", len(c["rows"]), "" if len(c["rows"]) == 1 else "s",
                                                            "" if c["first"] else " - NOT FIRST CHOICE")
                    names = [f[0] for f in found]
                    k = pick(T + (" | none at this size: %s" % ", ".join(missing) if missing else ""), "Performance level",
                             [lv_label(g_, c_) for g_, _, c_ in found], default=names.index(last["level"]) if last.get("level") in names else 0)
                    if k is None:
                        break
                    if k == "back":
                        step = "size"; continue
                    level_name, level_tiers, res = found[k]
                    last["level"] = level_name; save_last(last)
                else:
                    level_name = "all levels (no performance levels for this tool type)" if mf in tc.LEVEL_MFS else "one level (single catalog tier)"
                    level_tiers = None
                    res = tc.candidates(mf, tname, mat, None, size, prm, tl.UNIT_PREF, include_highfeed=(usage == "rough"))
                    if not res["rows"]:
                        log("no tool:", res["why"])
                        info(T, "No tool found.\n" + res["why"] + "\nChange the size or limits, or go back.")
                        step = "size"; continue
                step = "families"
            # ================= search: the family's tools at the size =================
            elif step == "found":
                res = family_tools(tc, mf, m_sel, mat, size, prm, tl.UNIT_PREF, shape)
                if not res["rows"]:
                    log("no tool:", res["why"])
                    info(T, "No tool found.\n" + res["why"] + "\nChange the size or limits, or go back.")
                    step = "size"; continue
                sizes = res["rows"]
                if usage:
                    sizes = tu.order_tools(sizes, usage)
                nm_ = m_sel["name"]
                level_name = "search '%s': %s%s" % (query, (nm_ + " ") if nm_ else "", fam)
                show_list(T + " - " + fam, "%s%s | %s | %s | %d option%s | cutting data for %s, %s %s max %s rpm%s" % (
                              (nm_ + " - ") if nm_ else "", fam, (("end mill, any shape" if shape == "Any" else shape) if tname == SEARCH_END_MILL else tname), size_text, len(sizes), "" if len(sizes) == 1 else "s", mat, machine,
                              spindle["spindle"], spindle["rpm"], ("\n" + res["note"]) if res["note"] else ""),
                          ["%d. [%s] %s\n      %s" % (n + 1, tc.rating_label(r, mat), tc.describe_tool(r, kind, inch), tc.cut_text(r, kind, mat)) for n, r in enumerate(sizes)])
                step = "tool"
            # ================= selector and generator: families =================
            elif step == "families":
                if gen:
                    level_name = "all levels, every rating"
                    res = tc.all_candidates(mf, tname, mat, size, prm, tl.UNIT_PREF)
                    if not res["rows"]:
                        log("no tool:", res["why"])
                        info(T, "No tool found.\n" + res["why"] + "\nChange the size or limits, or go back.")
                        step = "size"; continue
                fams = {}
                for r in res["rows"]:
                    fams.setdefault(r.get("family") or r["designation"], []).append(r)
                base_key = lambda f: (-max(int(tc._f(x.get("tier_rank"))) for x in fams[f]), f)
                fam_names = sorted(fams, key=base_key)
                why_fam = {}
                if gen:
                    # every family, grouped by the material's rating (primary, suitable, not rated); the primary usage orders inside a group
                    frate = lambda f: max(int(x.get("_rating", 0)) for x in fams[f])
                    fam_names = []
                    for rt in (2, 1, 0):
                        grp = {f: fams[f] for f in fams if frate(f) == rt}
                        if not grp:
                            continue
                        if usage:
                            names_, why_ = tu.order_families(mf, grp, usage, mat, base_key)
                            fam_names += names_; why_fam.update(why_)
                        else:
                            fam_names += sorted(grp, key=base_key)
                elif usage:
                    fam_names, why_fam = tu.order_families(mf, fams, usage, mat, base_key)
                letter = str(mat)[:1].upper()
                shown = ("thread %s" % size["name"]) if thread_tool else ("bore %.4f in" % size) if spec["size"] == "bore" else \
                        ("dia %.4f in asked" % size) if gen else ("dia %.4f in" % tc.dia_of(res["rows"][0], kind))
                rating_txt = ("all %d tools, ordered by ISO %s rating (primary, suitable, not rated)" % (len(res["rows"]), letter)) if gen else \
                             (("ISO %s first choice" % letter) if res["first"] else ("ISO %s suitable (NOT FIRST CHOICE)" % letter))
                header = "%s %s (%s rpm max) | %s | %s | %s | %s | %s | %s%s%s" % (machine, spindle["spindle"], spindle["rpm"], mf, tname, mat, rating_txt,
                                                            level_name, shown, ("\nOrdered for: %s" % [l for k_, l, _ in tu.USAGES if k_ == usage][0]) if usage else "",
                                                            ("\n" + res["note"]) if res["note"] else "")
                def fam_label(f):
                    if not gen:
                        return tc.describe_family(fams[f])
                    best = max(fams[f], key=lambda x: int(x.get("_rating", 0)))
                    return "[%s] %s" % (tc.rating_label(best, mat), tc.describe_family([dict(x, _nfc=False) for x in fams[f]]))
                show_list(T + " - families", header, ["%d. %s%s" % (k + 1, fam_label(f), ("\n      fit: " + why_fam[f]) if why_fam.get(f) else "")
                                                      for k, f in enumerate(fam_names)])
                step = "family"
            elif step == "family":
                k = pick(T, "Tool family", ["%s - %d%s" % (f, len(fams[f]), (" " + tc.RATING_TEXT.get(max(int(x.get("_rating", 0)) for x in fams[f]), "")) if gen else "")
                                            for f in fam_names])
                if k is None:
                    break
                if k == "back":
                    step = "size" if (gen or not level_screen) else "level"; continue
                fam = fam_names[k]
                sizes = sorted(fams[fam], key=lambda r: (tc._f(r.get("flute_len_mm") or r.get("thread_len_mm") or r.get("depth_max_mm") or r.get("lc_mm")),
                                                          tc._f(r.get("oal_mm") or r.get("l1_mm")), r["designation"], r.get("grade", "")))
                if usage:
                    sizes = tu.order_tools(sizes, usage)
                show_list(T + " - " + fam, "%s | %s | %d option%s | cutting data for %s, %s %s max %s rpm" % (fam, tname, len(sizes), "" if len(sizes) == 1 else "s", mat, machine, spindle["spindle"], spindle["rpm"]),
                          ["%d. %s%s\n      %s" % (n + 1, ("[%s] " % tc.rating_label(r, mat)) if gen else "", tc.describe_tool(r, kind, inch), tc.cut_text(r, kind, mat)) for n, r in enumerate(sizes)])
                step = "tool"
            elif step == "tool":
                k = pick(T, "Tool", ["%d. %s%s" % (n + 1, r["designation"], (" " + r["grade"]) if r.get("manufacturer") == "Kennametal" and r.get("grade") else "") for n, r in enumerate(sizes)])
                if k is None:
                    break
                if k == "back":
                    if srch:
                        step = "size" if not direct else ("match" if len(matches) > 1 else "type")
                    else:
                        step = "family"
                    continue
                row = sizes[k]
                if gen or srch:
                    row_first = int(row.get("_rating", 0)) >= 2
                else:
                    row_first = res["first"] and not row.get("_nfc")
                row_note = res["note"]
                step = "tecsets"
            # ================= all three: cutting-data sets, generate =================
            elif step == "tecsets":
                dlg = _dialog("%s | %s" % (T, row["designation"]))
                if kind == "endmill":
                    want = tu.purpose_of(usage)
                    for label, purpose in tc.TECSETS:
                        dlg.AddBool(label, defaultValue=(purpose == want) if want else (purpose in tc.DEFAULT_TECSETS))
                dlg.AddBool("Generate tool", defaultValue=True)
                dlg.AddBool("Back to previous screen", defaultValue=False)
                ok, vals = dlg.Show()
                if not ok:
                    break
                if any(str(kk).startswith("Back") and vv for kk, vv in vals.items()):
                    step = "wizard" if wiz else "tool"; continue
                purposes = None
                if kind == "endmill":
                    purposes = [p for (label, p) in tc.TECSETS if vals.get(label)]
                    if not purposes:
                        info(T, "Pick at least one cutting-data type.")
                        continue
                if not any(str(kk).startswith("Generate") and vv for kk, vv in vals.items()):
                    step = "wizard" if wiz else "tool"; continue
                tool, msg = tl.build(model, jt, row, kind, mat, purposes=purposes, force_new=True)
                log("selected:", level_name, "|", row["designation"], row.get("tier", ""), row.get("grade", ""), "|", msg, "| tecsets", purposes,
                    "| first choice", row_first, "|", row_note)
                if tool is None:
                    info(T, "Selected %s but the import failed: %s" % (row["designation"], msg))
                else:
                    extra = ""
                    if tc.cut_text(row, kind, mat) == "no catalog cutting data":
                        extra = "\nThe catalog publishes no cutting data for this tool. Set speeds and feeds in the Tools tab."
                    else:
                        src = tc.source_note(row, kind, mat, purposes)
                        if src:
                            extra = "\nCUTTING DATA: " + src + "."
                    if kind == "xdrill":
                        extra += "\nThis is the holder/body only; the tip or insert is not modeled."
                    if (gen or srch) and int(row.get("_rating", 0)) == 0:
                        nfc = "\nNOT RATED by the catalog for ISO %s." % str(mat)[:1].upper()
                    else:
                        nfc = "" if row_first else "\nNOT FIRST CHOICE for this material."
                    info(T, "%s %s\n%s%s%s%s" % (row["designation"], row.get("tier", ""), msg, ("\n" + row_note) if ((wiz or srch) and row_note) else "", nfc, extra))
                nxt = pick(T, "Next", [("Another tool, same family and material" if srch else "Another tool, same type and material"),
                                       ("New search" if srch else "Start over (manufacturer)"), "Change machine or spindle", "End"], back=False)
                if nxt == 0:
                    step = "direct" if (srch and direct) else "size"
                elif nxt == 1:
                    step = "type" if srch else "mf"
                elif nxt == 2:
                    step = "machine"
                else:
                    break
    except Exception:
        log("FAILED:", traceback.format_exc())
        try:
            info(T, "Failed. See %s." % LOG_NAME)
        except Exception:
            pass
    finally:
        _write_log()

if __name__ == "__main__":
    run()
