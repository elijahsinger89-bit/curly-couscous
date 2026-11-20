# part_wizard_2.py - puts a library tool and its cutting data in every toolpath (run after part_wizard_1, once the pocket
# features are attached to the milling toolpaths and the stock references are set).
#   1 machine and spindle (the choice from part_wizard_1 is offered first; its max rpm caps every speed, the feed follows)
#   2 tool manufacturer and performance level
#   3 joblists, replace existing tools or not, create or dry run, calculate and check afterwards or not
#   4 per toolpath: the operation (from part_wizard_1's job list, else the job name) sets the tool shape and the primary usage;
#     attached features set the size: holes -> diameter and depth, pockets -> corner radius, diameter limit and height.
#     Toolpaths without features get the operation's default tool size (job_settings.json) with a flute of at least 1 x D.
#   5 optional: calculate, reset floor stock on 'Bottom higher than top', recalculate, flag jobs that made no toolpath
# Log: C:\Users\Public\Documents\OPEN MIND\part_wizard_2_log.txt
import os, re, json, tempfile, traceback

# ---------------- SETTINGS ----------------
PY_DIR          = r"C:\Users\Public\Documents\OPEN MIND\python"
LIB_DIR         = os.path.join(PY_DIR, "tool_library")
JOBS_FILE       = os.path.join(tempfile.gettempdir(), "part_wizard_1_jobs.json")              # written by part_wizard_1
POCKET_RADIUS_FIT     = 1.0     # finishing: end mill diameter = 2 x smallest pocket corner radius x this
POCKET_TOOL_SHARP_IN  = 0.125   # finishing a sharp-cornered pocket with no diameter limit
POCKET_WIDTH_CLEARANCE_IN = 0.05  # end mill is at least this much narrower than the pocket's diameter limit (LD)
POCKET_WIDTH_FRACTION = 0.8       # and at most this fraction of it
FLUTE_EXTRA_IN        = 0.05    # flute length beyond the deepest attached feature
MILL_FLUTE_RATIO      = 1.0     # toolpath without features: flute at least this many diameters
FACE_MILL_DIA_IN      = 2.0     # face mill body diameter asked for (Face Mill toolpaths)
FACE_MILL_AP_IN       = 0.1     # face mill depth of cut asked for
MILL_Z_FEED_RATIO     = 0.5     # milling plunge feed = this x the cutting feed (same as the tool's cutting data)
SET_TECSET_LINK       = False   # True = also try to point the job at the usage's cutting-data set (*JOB_CPNAME); hyperMILL 35 ignored it
POF_EMPTY_BYTES       = 12000   # a calculated job whose .pof file is smaller than this probably has no toolpath
# tool rule, primary usage and default tool per operation: tool_library/job_types.py
TNAME = {"flat": "Flat end mill", "radius": "Radius end mill", "ball": "Ball end mill"}
# ------------------------------------------

lines = []
warnings = []
def log(*a):
    lines.append(" ".join(str(x) for x in a))

def warn(text):
    warnings.append(text)
    log("   CHECK:", text)

def val(x):
    return x() if callable(x) else x

def _gui():
    import om.cad.gui as g
    return g

def _dialog(title):
    return _gui().InputDialog(title)

def choose(title, label, options, default=0):
    dlg = _dialog(title)
    dlg.AddDropDown(label, list(options), defaultIndex=default)
    ok, vals = dlg.Show()
    if not ok:
        return None
    v = vals[label]
    if isinstance(v, int) and not isinstance(v, bool):
        return v if 0 <= v < len(options) else 0
    return list(options).index(v) if v in options else 0

def checks(title, items):
    dlg = _dialog(title)
    for label, default in items:
        dlg.AddBool(label, defaultValue=bool(default))
    ok, vals = dlg.Show()
    if not ok:
        return None
    return [bool(vals[label]) for label, _ in items]

def info(title, text):
    g = _gui()
    g.ShowMessageBox(g.MessageBoxType.INFORMATION, title, text)

class UI:
    choose = staticmethod(choose)
    checks = staticmethod(checks)
    info = staticmethod(info)

LIB = {}
def load_lib(folder):
    import sys, importlib
    if folder not in sys.path:
        sys.path.insert(0, folder)
    for n in ("tool_builder", "tool_lookup", "hole_tools", "tool_catalog", "tool_usage", "hole_jobs", "job_settings", "job_types", "machine_pick"):
        m = importlib.import_module(n)
        importlib.reload(m)
        LIB[n] = m
    return LIB

def _f(x, d=0.0):
    try:
        return float(x)
    except Exception:
        return d

def dia_in(r):
    return _f(r.get("dia_in")) or _f(r.get("dia_mm")) / 25.4

# ---------------- which operation is this job ----------------
def load_jobs_file():
    try:
        with open(JOBS_FILE, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def identify(job, side):
    """(operation, part_wizard_1 entry or None, source)."""
    u = str(job.UUID)
    if u in side:
        return side[u].get("op"), side[u], "part_wizard_1"
    for src, text in (("job name", lambda: job.Name), ("cycle", lambda: job.CycleName), ("cycle", lambda: job.LocCycleName)):
        try:
            t = str(val(text())).lower()
        except Exception:
            continue
        op = LIB["job_types"].op_from_name(t)
        if op:
            return op, None, src
    return None, None, "not recognised"

# ---------------- features ----------------
NUM = r"([0-9]*\.?[0-9]+)"
HEIGHT_KEYS = ("Pocket::Height", "Generic_Pocket::Height", "Pocket::Depth", "Height", "Pocket::Pocket_Height")

def read_pocket(hj, f):
    dn = str(val(f.DisplayName))
    def g(pat):
        m = re.search(pat, dn)
        return float(m.group(1)) if m else None
    height = None
    for k in HEIGHT_KEYS:
        height = hj.num(hj.gp(f, k))
        if height is not None:
            break
    return dict(f=f, id=int(val(f.ID)), dn=dn, radius=g(r"\bR" + NUM), limit=g(r"\bLD" + NUM), height=height,
                bottom_radius=g(r"\bBCR" + NUM))

def read_hole(hj, f):
    dn = str(val(f.DisplayName))
    dia = hj.num(hj.gp(f, "Hole::Diameter"))
    if dia is None:
        m = re.search(r"\bD" + NUM, dn)
        dia = float(m.group(1)) if m else None
    return dict(f=f, id=int(val(f.ID)), dn=dn, dia=dia, depth=hj.num(hj.gp(f, "Hole::Depth")), prop=hj.gp(f, "Hole::Front_Machining_Property"), ops=[], note="")

# ---------------- tool choice ----------------
def mill_size(op, rule, kind, dia, pockets):
    """(diameter asked for, largest diameter allowed or None, flute length, shape, reason)."""
    if not pockets:
        return dia, None, dia * MILL_FLUTE_RATIO, kind, "no features: default tool %.4f in %s, flute %.1f x D" % (dia, kind, MILL_FLUTE_RATIO)
    hs = [p["height"] for p in pockets if p["height"] is not None]
    flute = (max(hs) if hs else dia * MILL_FLUTE_RATIO) + FLUTE_EXTRA_IN
    lims = [p["limit"] for p in pockets if p["limit"] is not None]
    lim = max(0.03, min(min(lims) - POCKET_WIDTH_CLEARANCE_IN, min(lims) * POCKET_WIDTH_FRACTION)) if lims else None
    why = "%d feature(s), %s %.3f" % (len(pockets), "reach" if rule in ("corner", "floor") else "flute", flute) + ("" if hs else " (height unreadable)")
    top = dia if lim is None else min(dia, lim)
    if lim is not None:
        why += ", diameter limit %.4f" % min(lims)
    if rule == "corner":
        radii = [p["radius"] for p in pockets if p["radius"] is not None]
        if radii and min(radii) > 0:
            top = min(top, 2.0 * min(radii) * POCKET_RADIUS_FIT)
            why += ", corner radius %.4f" % min(radii)
        elif lim is None:
            top = min(top, POCKET_TOOL_SHARP_IN)
            why += ", sharp corners"
    if rule == "floor" and kind == "flat" and any((p["bottom_radius"] or 0) > 0 for p in pockets):
        kind = "radius"
        why += ", floor corner radius"
    return top, top, flute, kind, why

def pick_mill(mf, kind, dia, top, flute, usage, mat, reach_only=False):
    """Best first-choice end mill for the usage at dia (or the largest size at or below top). Returns (row, note)."""
    tc, tu, tl = LIB["tool_catalog"], LIB["tool_usage"], LIB["tool_lookup"]
    tname = TNAME[kind]
    letter = str(mat)[:1].upper()
    if top is not None:
        rows = tc.rows_for(mf, tname, tl.TIER_FILTER)
        sizes = sorted(set(round(dia_in(r), 4) for r in rows if 0 < dia_in(r) <= top + 0.0005 and tc.rating(r, letter) >= 1), reverse=True)[:10]
    else:
        sizes = [dia]
    why = "no %s %s at or below %.4f in" % (mf, tname, top) if top is not None else ""
    for s in sizes:
        c = tc.candidates(mf, tname, mat, tl.TIER_FILTER, s, {"reach": flute} if reach_only else {"loc": flute}, tl.UNIT_PREF, include_highfeed=(usage == "rough"))
        rows = c["rows"]
        if top is not None:
            rows = [r for r in rows if dia_in(r) <= top + 0.0005]
        if not rows:
            why = c.get("why") or why
            continue
        fams = {}
        for r in rows:
            fams.setdefault(r.get("family") or r["designation"], []).append(r)
        names, reasons = tu.order_families(mf, fams, usage, mat, lambda f: (-max(int(_f(x.get("tier_rank"))) for x in fams[f]), f))
        pick, skipped = names[0], []
        for nm in names:                    # a toolpath needs speeds and feeds: the best-ranked family that has catalog cutting data
            if mill_cut(tu.order_tools(fams[nm], usage)[0], usage, mat)[0]:
                pick = nm
                break
            skipped.append(nm)
        else:
            skipped = []
        best = tu.order_tools(fams[pick], usage)[0]
        note = reasons.get(pick) or ""
        if skipped:
            note += " | ranked higher but no catalog cutting data: " + ", ".join(skipped[:3])
        if best.get("_nfc"):
            note += " | NOT FIRST CHOICE for this material (high-feed tool, catalog rates it suitable)"
        if c.get("note"):
            note = c["note"] + " | " + note
        return best, note
    # nothing reaches: the longest-reaching first-choice tool at the largest fitting size, marked SHORT so the operator decides
    def reach(r):
        return (_f(r.get("reach_mm")) or _f(r.get("flute_len_mm"))) / 25.4
    for s in sizes:
        c = tc.candidates(mf, tname, mat, tl.TIER_FILTER, s, {}, tl.UNIT_PREF)
        rows = [r for r in c["rows"] if top is None or dia_in(r) <= top + 0.0005]
        rows = [r for r in rows if mill_cut(r, usage, mat)[0]] or rows
        if rows:
            best = max(rows, key=reach)
            return best, "SHORT: reaches %.3f in, needs %.3f in (longest %s %s at this size)" % (reach(best), flute, mf, tname)
    return None, why or "no %s %s fits" % (mf, tname)

def with_level(fn):
    """Runs a tool pick at the chosen performance level, then at any level when that level has nothing."""
    tl, ht = LIB["tool_lookup"], LIB["hole_tools"]
    def safe():
        try:
            return fn()
        except Exception as e:
            log("      tool search FAILED", traceback.format_exc()[-300:])
            return None, "tool search failed: %s" % str(e)[:80]
    tl.TIER_FILTER = ht.TIER_FILTER = LEVEL["tiers"]
    try:
        row, note = safe()
    finally:
        tl.TIER_FILTER = ht.TIER_FILTER = None
    if row is None and LEVEL["tiers"] is not None:
        row, note2 = safe()
        if row is not None:
            note = "no %s tool, used another level | %s" % (LEVEL["name"], note2)
    return row, note

LEVEL = {"name": "Any", "tiers": None}
BUILT = set()

def mill_cut(row, usage, mat):
    """Cutting data of the usage's set (rpm, ipm, ae, ap), else the general roughing data."""
    tb, tu, tl = LIB["tool_builder"], LIB["tool_usage"], LIB["tool_lookup"]
    try:
        res = tb.endmill_cut(row, mat) or {}
    except Exception:
        res = {}
    p = tu.purpose_of(usage) if usage else None
    c = res.get(p) if p else None
    if c:
        return dict({k: c[k] for k in ("borrowed", "standard", "group", "wanted") if c.get(k)},
                    rpm=c["rpm"], ipm=c["ipm"], ae=c.get("ae"), ap=c.get("ap")), p
    c = tl.cut_for(row, "endmill", mat)
    return c, "Rough - usage 1" if c else None

def set_cut(job, cut, milling):
    """Speed and feed on the job. Milling: FeedrateXY is the cutting feed, FeedrateZ the plunge feed. Holes: FeedrateZ."""
    if not cut:
        return
    vals = [("SpindleRPM", cut["rpm"])]
    vals += [("FeedrateXY", cut["ipm"]), ("FeedrateZ", cut["ipm"] * MILL_Z_FEED_RATIO)] if milling else [("FeedrateZ", cut["ipm"])]
    for name, v in vals:
        try:
            job.SetTTProperty(name, float(v), 1)
            log("      SetTTProperty(%s, %.3f, 1) ok" % (name, v))
        except Exception as e:
            log("      SetTTProperty(%s) FAILED %s" % (name, str(e)[:200]))

def link_tecset(job, purpose):
    if not (SET_TECSET_LINK and purpose):
        return
    try:
        r = job.SetCfgParameters({"*JOB_CPNAME": purpose})
        log("      cutting-data set link *JOB_CPNAME = %s -> %s | reads back %s" % (purpose, r, dict(job.GetCfgParameters()).get("*JOB_CPNAME")))
    except Exception as e:
        log("      cutting-data set link FAILED", str(e)[:150])

def build(model, row, kind, mat, label, purposes=None):
    """(tool or None, True when the tool was already in the document)."""
    try:
        tool, msg = LIB["tool_lookup"].build(model, LIB["jt"], row, kind, mat, purposes=purposes)
    except Exception as e:
        log("      tool build FAILED", traceback.format_exc()[-300:])
        warn("%s: tool %s could not be built (%s)" % (label, row.get("designation"), str(e)[:60]))
        return None, False
    log("      tool:", msg)
    if tool is None:
        warn("%s: tool %s could not be built (%s)" % (label, row.get("designation"), msg))
        return None, False
    if "existing" not in str(msg):
        BUILT.add(row.get("designation"))          # built in this run with every cutting-data set
    return tool, "existing" in str(msg) and row.get("designation") not in BUILT

def attach(model, job, row, kind, mat, purposes, label):
    """Builds (or reuses) the tool and puts it in the job. Returns (ok, tool was already in the document)."""
    tool, existing = build(model, row, kind, mat, label, purposes)
    if tool is None:
        return False, existing
    if not LIB["hole_jobs"].attach_tool(job, tool, log):
        warn("%s: tool could not be attached" % label)
        return False, existing
    log("      job tool now:", getattr(job.GetTool(), "Name", "?"))
    return True, existing

def chamfer_job(model, job, row, kind, mat, label):
    """Centering as 'chamfer existing hole' with the chamfer tool; 1 when the tool is in the job afterwards."""
    tool, _ = build(model, row, kind, mat, label)
    if tool is None:
        return 0
    LIB["hole_jobs"].make_chamfer_job(model, job, log, tool)
    try:
        ok = str(job.GetTool().UUID) == str(tool.UUID)
    except Exception:
        ok = False
    if not ok:
        warn("%s: chamfer tool could not be attached" % label)
    return int(ok)

def has(mf, group):
    return group in LIB["tool_lookup"].MANUFACTURERS.get(mf, {})

def chamfer_tool(mf, hole_dia, mat):
    """(row, kind, note): Walter MC501 chamfer mill; manufacturers without chamfer mills in the library get a 90 degree spot drill."""
    hj, tl = LIB["hole_jobs"], LIB["tool_lookup"]
    if mf == "Walter":
        row, note = with_level(lambda: tl.select_chamfer(hole_dia, hj.CHAMFER_WIDTH_IN, mat, mf))
        return row, "chamfer", note
    if has(mf, "spotdrills"):
        row, note = with_level(lambda: tl.select_spotdrill(hole_dia + 2 * hj.CHAMFER_WIDTH_IN, 90, mat, mf))
        return row, "spotdrill", "%s has no chamfer mill in the library: 90 degree spot drill | %s" % (mf, note)
    return None, None, "%s has no chamfer mill or spot drill in the library" % mf

# ---------------- per job ----------------
def do_mill(model, job, op, entry, feats, label, mat, mf, data, apply_now):
    hj, tl = LIB["hole_jobs"], LIB["tool_lookup"]
    spec = LIB["job_types"].OPS[op]
    if spec["rule"] == "chamfer":
        row, kind, note = chamfer_tool(mf, hj.EDGE_CHAMFER_REF_IN, mat)
        if row is None:
            warn("%s: no chamfer tool (%s)" % (label, note)); return 0
        log("   %s: %s %s | %s" % (label, row["designation"], row.get("tier", ""), note))
        if kind == "spotdrill":
            warn("%s: spot drill used for chamfering, check hyperMILL accepts it in this cycle" % label)
        return 1 if not apply_now else int(attach(model, job, row, kind, mat, None, label)[0])
    rule, usage = spec["rule"], spec["usage"]
    rec = None
    if entry and entry.get("settings"):
        found = LIB["job_settings"].find(data, entry.get("group") or mat, entry["settings"].split(" | ")[0], op, entry.get("stepover", ""))
        rec = found[2] if found else None
    kind, dia = (rec["tool_shape"], float(rec["tool_dia_in"])) if rec and rec.get("tool_shape") in TNAME and rec.get("tool_dia_in") else (spec["shape"] or "flat", spec["dia"] or 0.5)
    if rule == "face" and not has(mf, "facemills"):
        log("   %s: %s has no face mills in the library, end mill instead" % (label, mf))
    elif rule == "face":
        row, note = with_level(lambda: tl.select_facemill(FACE_MILL_DIA_IN, FACE_MILL_AP_IN, mat, mf))
        if row is not None:
            log("   %s: face mill %s %s | %s" % (label, row["designation"], row.get("tier", ""), note))
            if apply_now and attach(model, job, row, "facemill", mat, None, label)[0]:
                log("      cutting data: from the tool (face mill)")
                return 1
            return 0 if apply_now else 1
        log("   %s: no %s face mill (%s), end mill instead" % (label, mf, note))
    pockets = [read_pocket(hj, f) for f in feats if str(val(f.Name)) == "Generic Pocket"]
    want, top, flute, kind, why = mill_size(op, rule, kind, dia, pockets)
    # finishing and rest tools only need to reach the depth (a necked tool is fine); roughing tools need the flute length
    row, note = with_level(lambda: pick_mill(mf, kind, want, top, flute, usage, mat, reach_only=rule in ("corner", "floor")))
    if row is None:
        warn("%s: no library %s end mill (%s) | %s" % (label, kind, why, note)); return 0
    cut, purpose = mill_cut(row, usage, mat)
    cut_txt = "" if not cut else " | %s: %.0f rpm, %.1f ipm%s" % (purpose, cut["rpm"], cut["ipm"],
                                                                     (", ae %.3f ap %.3f" % (cut["ae"], cut["ap"])) if cut.get("ae") and cut.get("ap") else "")
    log("   %s: %s | %s %s dia %.4f%s | %s" % (label, why, row["designation"], row.get("tier", ""), dia_in(row), cut_txt, note))
    if note.startswith("SHORT") or " SHORT:" in note:
        warn("%s: %s is too short for the depth: %s" % (label, row["designation"], note.split("SHORT: ")[-1].split(" (")[0]))
    if not cut:
        warn("%s: %s has no catalog cutting data, set speeds and feeds by hand" % (label, row["designation"]))
    elif LIB["tool_builder"].cut_source(cut):
        warn("%s: %s %s" % (label, row["designation"], LIB["tool_builder"].cut_source(cut)))
    if spec["rule"] == "rough" and not usage:
        warn("%s: library end mill picked; check it is rated for plunging" % label)
    if not pockets and rule not in ("default", "face"):
        warn("%s: no features attached, tool length not checked against the part" % label)
    if not apply_now:
        return 1
    purposes = [p for _, p in LIB["tool_catalog"].TECSETS]       # a new tool gets every cutting-data set, so any later usage can link to it
    ok, existing = attach(model, job, row, "endmill", mat, purposes, label)
    if not ok:
        return 0
    if existing:
        log("      tool was already in the document: cutting-data set link skipped (it may not carry the %s set); speed and feed set on the job" % purpose)
    else:
        link_tecset(job, purpose)
    set_cut(job, cut, True)
    return 1

def do_holes(model, job, op, feats, label, mat, mf, apply_now, entry=None):
    hj, tl = LIB["hole_jobs"], LIB["tool_lookup"]
    holes = [read_hole(hj, f) for f in feats if str(val(f.Name)) == "Generic Hole"]
    thru = (entry or {}).get("through") or {}
    for h in holes:
        L = thru.get(str(h["f"].UUID))
        if L:                                      # part_wizard_1 drills it on through the opposite hole: the tool must reach that far
            log("   %s: hole %d drilled through to the opposite hole, depth %.4f (feature %.4f)" % (label, h["id"], L, h["depth"] or 0))
            h["depth"] = L
    holes = [h for h in holes if h["dia"] and h["depth"] is not None]
    if not holes:
        warn("%s: no hole features with diameter and depth attached" % label); return 0
    if op == "Helical Thread Drilling/Milling":
        warn("%s: library thread mill picked; this cycle drills with the tool tip, check the tool has one" % label)
    op = LIB["job_types"].HOLE_OP[op]
    if op in ("Drill", "Peck Drill"):
        r = max(h["depth"] / h["dia"] for h in holes)
        if r >= hj.DEEP_RATIO and op == "Drill":
            warn("%s is %.1fxD deep but is not a pecking cycle: change its cycle to Pecking (tool set anyway)" % (label, r))
    if op == "Centering":
        d = max(h["dia"] for h in holes)
        row, kind, note = chamfer_tool(mf, d, mat)
        ids = ",".join(str(h["id"]) for h in holes)
        if row is None:
            warn("%s: no chamfer tool | features %s | %s" % (label, ids, note)); return 0
        log("   %s: Centering (chamfer existing hole) dia %.4f | features %s | %s %s | %s" % (label, d, ids, row["designation"], row.get("tier", ""), note))
        if not apply_now:
            return 1
        return chamfer_job(model, job, row, kind, mat, label)
    if op == "Boring":
        if not has(mf, "boring"):
            warn("%s: %s has no boring tools in the library" % (label, mf)); return 0
        d = max(h["dia"] for h in holes); depth = max(h["depth"] for h in holes)
        row, note = with_level(lambda: tl.select_boring(d, depth, mat, mf))
        if row is None:
            warn("%s: no boring tool (%s)" % (label, note)); return 0
        log("   %s: boring %.4f x %.4f | %s %s | %s" % (label, d, depth, row["designation"], row.get("tier", ""), note))
        return 1 if not apply_now else int(attach(model, job, row, "boring", mat, None, label)[0])
    for h in holes:
        h["ops"] = [op]
    plan = []
    def p():
        plan[:] = hj.build_plan(holes, tl, mat, mf, log)
        j0 = max(plan, key=lambda j: j["dia"]) if plan else None
        return (j0["row"] if j0 else None), (j0["note"] if j0 else "no plan")
    with_level(p)
    if not plan:
        return 0
    plan.sort(key=lambda j: -j["dia"])
    j = plan[0]
    if len(plan) > 1:
        warn("%s: %d diameters in one toolpath, tool for the largest (%.4f in)" % (label, len(plan), j["dia"]))
    ids = ",".join(str(h["id"]) for h in j["holes"])
    if j["row"] is None:
        warn("%s: no library tool | features %s | %s" % (label, ids, j["note"])); return 0
    cut_txt = "" if not j["cut"] else " | %.0f rpm, %.1f ipm" % (j["cut"]["rpm"], j["cut"]["ipm"])
    src = LIB["tool_builder"].cut_source(j["cut"]) if j["cut"] else ""
    if src:
        warn("%s: %s %s" % (label, j["row"]["designation"], src))
    log("   %s: %s dia %.4f depth %.4f | features %s | %s %s | %s%s" % (label, op, j["dia"], j["depth"], ids, j["row"]["designation"], j["row"].get("tier", ""), j["note"], cut_txt))
    if not apply_now:
        return 1
    if j["kind"] == "chamfer":
        return chamfer_job(model, job, j["row"], "chamfer", mat, label)
    if not attach(model, job, j["row"], j["kind"], mat, None, label)[0]:
        return 0
    set_cut(job, j["cut"], j["kind"] == "endmill")
    return 1

# ---------------- calculate and check ----------------
def msgs(j):
    try:
        return [str(getattr(m, "Message", m)).replace("\n", " ")[:100] for m in j.GetMessages()]
    except Exception:
        return []

def calculate_and_check(model, targets, tooled):
    for jl in targets:
        try:
            log("calculating", jl.Name, "->", model.JobListSet.Run(str(jl.UUID)))
        except Exception as e:
            log("calculate FAILED", str(e)[:150])
    fixed = set()
    for job, label in tooled:
        if any("Bottom higher than top" in m for m in msgs(job)):
            try:
                c = job.GetCfgParameters()
                if str(c.get("*AUFMASS_Z", "0")) not in ("0", "0.0", ""):
                    log("   %s: 'Bottom higher than top', floor stock *AUFMASS_Z %s -> 0 -> %s" % (job.Name, c.get("*AUFMASS_Z"), job.SetCfgParameters({"*AUFMASS_Z": "0"})))
                    fixed.add(str(job.JobList.UUID))
                    warn("%s: floor stock to leave set to 0 (feature too shallow for it)" % job.Name)
            except Exception as e:
                log("   floor stock reset FAILED", str(e)[:100])
    for jl in targets:
        if str(jl.UUID) in fixed:
            try:
                log("recalculating", jl.Name, "->", model.JobListSet.Run(str(jl.UUID)))
            except Exception as e:
                log("recalculate FAILED", str(e)[:150])
    for jl in targets:
        for job in jl.GetJobs():
            try:
                pf = str(job.PofFileName)
                size = os.path.getsize(pf) if os.path.exists(pf) else -1
            except Exception:
                size = -1
            log("   toolpath check: %s | pof %d bytes | status %s | %s" % (job.Name, size, job.Status, msgs(job)))
            if size < POF_EMPTY_BYTES:
                warn("%s probably has NO toolpath (pof %d bytes)" % (job.Name, size))

# ---------------- main ----------------
def run(ui=UI, model=None, write_log=True):
    try:
        if model is None:
            import om
            model = om.Application().CurrentDocument.CamModel
        if not bool(val(model.IsInchMode)):
            ui.info("Part wizard 2", "This session is metric. The tool library selection is set up for inch sessions.")
            log("metric session, stopped"); return
        load_lib(LIB_DIR)
        tb, tl, tc, hj = LIB["tool_builder"], LIB["tool_lookup"], LIB["tool_catalog"], LIB["hole_jobs"]
        sp = LIB["machine_pick"].pick_spindle(_dialog, "Part wizard 2 - machine", log)
        if sp is None:
            log("cancelled at machine"); return
        LIB["jt"] = tb.JobTools()
        BUILT.clear()
        mfs = list(tl.MANUFACTURERS)
        mi = ui.choose("Part wizard 2", "Tool manufacturer", mfs, default=0)
        if mi is None:
            log("cancelled at manufacturer"); return
        mf = mfs[mi]
        if mf in tc.LEVEL_MFS:
            levels = [("Any level (best first-choice tool)", None)] + [(n, t) for n, t in tc.LEVELS]
            li = ui.choose("Part wizard 2", "Performance level", [n for n, _ in levels], default=0)
            if li is None:
                log("cancelled at level"); return
            LEVEL.update(name=levels[li][0], tiers=levels[li][1])
        log("manufacturer:", mf, "| level:", LEVEL["name"])
        lists = list(model.JobListSet.GetJobLists())
        if not lists:
            ui.info("Part wizard 2", "No joblists in this document."); return
        r = ui.checks("Joblists", [("Tool the jobs in " + jl.Name, True) for jl in lists])
        if r is None:
            return
        targets = [jl for jl, on in zip(lists, r) if on]
        go = ui.checks("Part wizard 2", [("Put the tools in the jobs now (leave unticked for a dry run that only writes the log)", False),
                                         ("Replace tools that are already in jobs", False),
                                         ("Calculate the joblists afterwards and check each job for a toolpath", False)])
        if go is None:
            return
        apply_now, replace, calc = go
        log("apply:", apply_now, "| replace:", replace, "| calculate:", calc)
        try:
            data = LIB["job_settings"].load(log)
        except Exception as e:
            data = {}
            log("job_settings.json not read, built-in tool sizes used:", e)
        side = load_jobs_file()
        log("part_wizard_1 job list:", JOBS_FILE, "|", len(side), "jobs")
        before = hj.tool_uuids(model) if apply_now else set()
        tooled, done, skipped = [], 0, 0
        for jl in targets:
            mat = jl.Material
            log("== joblist:", jl.Name, "| material:", mat)
            if mf == "Walter" and tb.material_note(mat):
                warn("%s (%s): %s" % (jl.Name, mat, tb.material_note(mat)))
            for job in jl.GetJobs():
                label = "%s (%s)" % (job.Name, jl.Name)
                try:
                    has_tool = job.GetTool() is not None
                except Exception:
                    has_tool = False
                if has_tool and not replace:
                    log("   has a tool, kept:", label, "|", getattr(job.GetTool(), "Name", "?")); continue
                op, entry, src = identify(job, side)
                if op is None:
                    warn("%s: operation not recognised from its name, tool it by hand" % label); skipped += 1; continue
                try:
                    feats = list(job.GetFeatures())
                except Exception:
                    feats = []
                log("  ", label, "| operation", op, "(from %s)" % src, "|", len(feats), "feature(s)")
                try:
                    spec = LIB["job_types"].OPS.get(op)
                    if spec is None:
                        warn("%s: no rule for operation %s" % (label, op)); n = 0
                    elif spec["rule"] == "hand":
                        warn("%s: %s needs a tool type the library does not have yet, tool it by hand" % (label, op)); n = 0
                    elif spec["rule"] == "hole":
                        n = do_holes(model, job, op, feats, label, mat, mf, apply_now, entry)
                    else:
                        n = do_mill(model, job, op, entry, feats, label, mat, mf, data, apply_now)
                except Exception:
                    log("   FAILED", label, traceback.format_exc()[-600:]); n = 0
                if n:
                    done += 1
                    tooled.append((job, label))
                else:
                    skipped += 1
        log("jobs tooled:", done, "| not tooled:", skipped)
        if apply_now:
            hj.delete_unused_new_tools(model, before, log)
        if apply_now and calc and tooled:
            calculate_and_check(model, targets, tooled)
        msg = "%d toolpath(s) %s, %d not. Details: part_wizard_2_log.txt" % (done, "got a tool" if apply_now else "planned (dry run)", skipped)
        if warnings:
            msg += "\n\nCheck by hand:\n" + "\n".join(warnings[:14])
        ui.info("Part wizard 2", msg)
    except Exception:
        log("FAILED:", traceback.format_exc())
        try:
            ui.info("Part wizard 2", "Failed. See part_wizard_2_log.txt.")
        except Exception:
            pass
    finally:
        if write_log:
            _write_log()

def _write_log():
    for p in [r"C:\Users\Public\Documents\OPEN MIND\part_wizard_2_log.txt",
              os.path.join(os.path.expanduser("~"), "Documents", "part_wizard_2_log.txt"),
              os.path.join(tempfile.gettempdir(), "part_wizard_2_log.txt")]:
        try:
            with open(p, "w", encoding="utf-8") as f:
                f.write("\n".join(lines))
            return p
        except Exception:
            continue

if __name__ == "__main__":
    run()
