# hole_jobs.py - reads the mapped holes, assigns each hole group to a joblist, and creates the hole operations with a
# library tool per diameter. Used by part_wizard_1.py and part_wizard_2.py. Nothing here runs by itself.
import math, traceback

LARGE_IN = 1.0              # diameter at or above this: Helical Drilling
DEEP_RATIO = 5.0            # depth/dia at or above this: Peck Drill
GUN_RATIO = 10.0            # depth/dia at or above this: gun drill (by hand)
SHALLOW_RATIO = 0.5         # depth/dia below this: no drilling operation
AUTO_TOL_DEG = 30.0         # a group within this angle of a joblist's approach axis is assigned without asking
THREAD_MILL_MIN_IN = 0.5    # thread diameter at or above this: Thread Milling; below: Tapping
REAM_ALLOWANCE_IN = 0.016   # drill this much under the finished size before reaming
HELICAL_TOOL_RATIO = 0.6    # helical drilling end mill diameter as a fraction of the hole diameter
DEPTH_EXTRA_RATIO = 0.3     # drill must reach hole depth plus this fraction of the diameter (point allowance)
ORDER = ["Drill", "Peck Drill", "Helical Drilling", "Centering", "Reaming", "Thread Milling", "Tapping"]

def val(x):
    return x() if callable(x) else x

def num(x):
    try:
        return float(str(x).strip())
    except Exception:
        return None

def gp(f, n):
    try:
        v = f.GetProperty(n)
        return "" if v is None else str(v).strip()
    except Exception:
        return ""

def operations(h):
    dia, depth, prop = h["dia"], h["depth"], h["prop"]
    if dia is None or depth is None:
        return [], "no diameter or depth"
    r = depth / dia
    if prop == "Thread":
        td = num(gp(h["f"], "Hole::Front_Thread::Diameter")) or dia
        return (["Drill" if r < DEEP_RATIO else "Peck Drill", "Centering", "Thread Milling" if td >= THREAD_MILL_MIN_IN else "Tapping"],
                "thread %s" % gp(h["f"], "Hole::Front_Thread::Designation"))
    if prop == "ISO fit":
        return ["Drill" if r < DEEP_RATIO else "Peck Drill", "Centering", "Reaming"], "ISO fit %s" % gp(h["f"], "Hole::Front_ISO-Fit::ISO-Fit_Value")
    if r >= GUN_RATIO:
        return [], "gun drill, by hand (%.1fxD)" % r
    if r < SHALLOW_RATIO:
        return [], "shallow step, no drilling operation (%.1fxD)" % r
    if dia >= LARGE_IN:
        return ["Helical Drilling"], "large (%.1fxD)" % r
    if r >= DEEP_RATIO:
        return ["Peck Drill", "Centering"], "deep (%.1fxD)" % r
    return ["Drill", "Centering"], "drill (%.1fxD)" % r

def vec3(v):
    try:
        return (float(v.X), float(v.Y), float(v.Z))
    except Exception:
        try:
            return (float(v[0]), float(v[1]), float(v[2]))
        except Exception:
            return None

def frame_axes(fr):
    """Z axis (approach direction) of a frame in world coordinates, from Frame.CoordinateSystem = (origin, x, y, z)."""
    try:
        cs = list(fr.CoordinateSystem)
        vs = [vec3(c) for c in cs]
        if len(cs) == 4:
            return vs[3]
        if len(cs) == 3:
            return vs[2]
    except Exception:
        pass
    return None

def angle(a, b):
    na = math.sqrt(sum(x * x for x in a)); nb = math.sqrt(sum(x * x for x in b))
    if not na or not nb:
        return 999.0
    c = sum(x * y for x, y in zip(a, b)) / (na * nb)
    return math.degrees(math.acos(max(-1.0, min(1.0, c))))

def read_holes(model, log):
    groups = {}
    for fl in list(model.FeatureListSet.GetFeatureLists()):
        name = str(getattr(fl, "Name", "?"))
        try:
            frame = fl.GetFrame().Name
        except Exception:
            frame = "no frame"
        for f in list(fl.GetFeatures()):
            if str(val(f.Name)) != "Generic Hole":
                continue
            try:
                o = val(f.Orientation); ovec = (float(o.X), float(o.Y), float(o.Z))
                ori = "%.2f,%.2f,%.2f" % tuple(round(c, 2) + 0.0 for c in ovec)     # + 0.0 turns -0.00 into 0.00 (one group per direction)
            except Exception:
                ori, ovec = "?", None
            try:
                pos = [vec3(p) for p in list(val(f.Positions))]
            except Exception:
                pos = []
            h = dict(f=f, id=int(val(f.ID)), dn=str(val(f.DisplayName)), dia=num(gp(f, "Hole::Diameter")),
                     depth=num(gp(f, "Hole::Depth")), ovec=ovec, prop=gp(f, "Hole::Front_Machining_Property"), ori=ori, list=name, frame=frame,
                     bottom=gp(f, "Bottom_Type"), pos=[p for p in pos if p])
            h["ops"], h["note"] = operations(h)
            groups.setdefault((name, frame, ori), []).append(h)
    log("hole groups:", len(groups), "| holes:", sum(len(v) for v in groups.values()))
    return groups

# ---------------- opposing holes on one axis ----------------
OPEN_BOTTOMS = ("Through", "Through_Hidden")   # open bottom: the hole breaks out (into the far face or a pocket)
COAX_TOL_IN = 0.005         # two hole positions are on one axis when the side offset is below this
SAME_DIA_IN = 0.0005        # same diameter
BREAK_EXTRA_IN = 0.02       # drill this far past the far end of the opposite hole

def _sub(a, b):
    return tuple(x - y for x, y in zip(a, b))

def _dot(a, b):
    return sum(x * y for x, y in zip(a, b))

def _unit(v):
    n = math.sqrt(_dot(v, v))
    return tuple(x / n for x in v) if n else None

def _through_length(a, b):
    """Length from a's entry to b's entry along a's axis when every position of a has one of b on its axis (one to one), else None."""
    da, db = _unit(a["ovec"]), _unit(b["ovec"])
    if not da or not db or _dot(da, db) > -0.999 or not a["pos"] or len(a["pos"]) != len(b["pos"]):
        return None
    used, lengths = set(), []
    for pa in a["pos"]:
        hit = None
        for k, pb in enumerate(b["pos"]):
            if k in used:
                continue
            v = _sub(pb, pa)
            along = -_dot(v, da)                   # a is drilled against its orientation; b's entry lies further along that way
            side = math.sqrt(max(0.0, _dot(v, v) - along * along))
            if along > 0 and side <= COAX_TOL_IN:
                hit = (k, along); break
        if hit is None:
            return None
        used.add(hit[0]); lengths.append(hit[1])
    return max(lengths)

def merge_opposing(groups, assign, joblist_order, log):
    """Two open-bottom holes of the same diameter and machining property, facing each other on one axis (a through hole broken by a
    pocket, or seen from both sides), are drilled from one side only: the side (direction) with more hole features, then the
    earlier joblist, then the longer hole. The other hole is removed from its group; the kept hole gets through = length from its
    entry to the far entry, and its operations are worked out again for that length. Threaded holes keep both sides.
    Returns the notes for the check list."""
    def jl(key):
        return assign.get("%s | %s" % (key[0], key[2]))
    def assigned(key):
        return jl(key) not in (None, "skip")
    count = {}
    for key, hs in groups.items():
        if assigned(key):
            count[key[2]] = count.get(key[2], 0) + len(hs)
    cand = [(key, h) for key, hs in groups.items() if assigned(key) for h in hs
            if h["bottom"] in OPEN_BOTTOMS and h["dia"] and h["depth"] is not None and h["ovec"] and h["pos"] and h["prop"] in ("", "None", "ISO fit")]
    done, notes = set(), []
    for i, (ka, a) in enumerate(cand):
        for kb, b in cand[i + 1:]:
            if a["id"] in done or b["id"] in done or ka[2] == kb[2]:
                continue
            if abs(a["dia"] - b["dia"]) > SAME_DIA_IN or (a["prop"] or "None") != (b["prop"] or "None"):
                continue
            L = _through_length(a, b)
            if L is None or L < a["depth"] + b["depth"] - 0.01:
                continue
            def rank(k, h):
                o = jl(k)
                return (count.get(k[2], 0), -(joblist_order.index(o) if o in joblist_order else 99), h["depth"], -h["id"])
            (kk, keep), (kd, drop) = sorted([(ka, a), (kb, b)], key=lambda x: rank(*x), reverse=True)
            groups[kd] = [h for h in groups[kd] if h is not drop]
            keep["through"] = L
            keep["merged"] = drop["id"]
            keep["ops"], keep["note"] = operations(dict(keep, depth=L))
            done.update((a["id"], b["id"]))
            msg = ("holes %d and %d are one axis (D%.4f): drilled from %s only (%s, %d holes that side), %.4f in through to the far side"
                   % (keep["id"], drop["id"], keep["dia"], kk[2], jl(kk), count.get(kk[2], 0), L))
            log("   " + msg)
            notes.append(msg)
    for k in [k for k, hs in groups.items() if not hs]:
        del groups[k]
    return notes

def joblist_axes(model, log):
    frames = {}
    try:
        for fr in model.FrameSet.GetFrames():
            frames[str(getattr(fr, "Name", ""))] = fr
    except Exception as e:
        log("FrameSet FAILED", str(e)[:100])
    out = {}
    for jl in model.JobListSet.GetJobLists():
        try:
            jobs = list(jl.GetJobs())
            fname = str(getattr(jobs[0].GetFrame(), "Name", "")) if jobs else ""
            if not fname and jl.Name in frames:
                fname = jl.Name          # empty joblist: use a frame that carries the joblist's name
            ax = frame_axes(frames[fname]) if fname in frames else None
            if not jobs and ax is None:
                log("joblist", jl.Name, "has no jobs yet; frames in file:", ", ".join(sorted(frames)) or "none")
            if ax:
                out[jl.Name] = ax
            log("joblist", jl.Name, "| frame", fname, "| approach axis", ax)
        except Exception as e:
            log("joblist", jl.Name, "axis FAILED", str(e)[:100])
    return out

def assign_groups(model, groups, hole_assign, ask, log):
    """Returns {group key: joblist name or 'skip'}. hole_assign = saved answers. ask(pending) -> {key: joblist or 'skip'} or None."""
    jl_axis = joblist_axes(model, log)
    assign = dict(hole_assign or {})
    pending = []
    for (name, frame, ori), hs in groups.items():
        key = "%s | %s" % (name, ori)
        if key in assign:
            continue
        best = None
        if jl_axis and hs[0]["ovec"]:
            angs = sorted((angle(hs[0]["ovec"], ax), jn) for jn, ax in jl_axis.items())
            log("group", key, "angles to joblist axes:", ", ".join("%s %.1f deg" % (jn, a) for a, jn in angs))
            if angs and angs[0][0] <= AUTO_TOL_DEG + 0.1 and (len(angs) == 1 or angs[1][0] > AUTO_TOL_DEG + 0.1):
                best = angs[0][1]
        if best:
            assign[key] = best
            log("group", key, "auto-assigned to", best)
        else:
            pending.append((key, name, frame, ori, hs))
    if pending:
        answers = ask(pending) if ask else None
        for key, name, frame, ori, hs in pending:
            assign[key] = (answers or {}).get(key, "skip")
    log("HOLE_ASSIGN =", assign)
    return assign

def ask_dialog(joblist_names, log):
    """Returns an ask(pending) function that shows one dropdown per group."""
    def ask(pending):
        import om.cad.gui as g
        overview = []
        for i, (key, name, frame, ori, hs) in enumerate(pending, 1):
            overview.append("GROUP %d   %s   frame %s   direction %s" % (i, name, frame, ori))
            for h in hs:
                overview.append("      %d: D%s x %s  %s" % (h["id"], h["dia"], h["depth"], h["note"]))
            overview.append("")
        g.ShowMessageBox(g.MessageBoxType.INFORMATION, "Hole groups to assign (%d)" % len(pending), "\n".join(overview)[:2500])
        choices = list(joblist_names) + ["Skip"]
        dlg = g.InputDialog("Assign each hole group to a joblist")
        labels = []
        for i, (key, name, frame, ori, hs) in enumerate(pending, 1):
            label = "G%d %s | %s | %d holes" % (i, name, ",".join(str(h["id"]) for h in hs)[:40], len(hs))
            labels.append(label)
            default = 0
            for k, jn in enumerate(joblist_names):
                if jn in frame or jn in name:
                    default = k
            dlg.AddDropDown(label, choices, defaultIndex=default)
        try:
            ok, vals = dlg.Show()
        except Exception:
            log("dialog FAILED", traceback.format_exc()[-300:]); return None
        if not ok:
            return None
        out = {}
        for (key, name, frame, ori, hs), label in zip(pending, labels):
            v = vals.get(label)
            if isinstance(v, int) and not isinstance(v, bool):
                v = choices[v] if 0 <= v < len(choices) else "Skip"
            out[key] = "skip" if str(v) == "Skip" else str(v)
        return out
    return ask

# ---------------- plan and apply ----------------
def build_plan(holes, tl, material, manufacturer, log):
    """holes: list of hole dicts for one joblist. Returns an ordered list of jobs to create:
    dict(op, dia, holes, request or None, row, note, cut)."""
    buckets = {}
    for h in holes:
        for op in h["ops"]:
            if op in ("Thread Milling", "Tapping"):
                key = (op, gp(h["f"], "Hole::Front_Thread::Designation") or ("%.4f" % h["dia"]))
            else:
                key = (op, round(h["dia"], 4))
            buckets.setdefault(key, []).append(h)
    jobs = []
    for (op, dkey), hs in buckets.items():
        dia = max(h["dia"] for h in hs); depth = max(h["depth"] for h in hs)
        j = dict(op=op, dkey=dkey, holes=hs, dia=dia, depth=depth, row=None, kind=None, note="no library tool", cut=None)
        try:
            if op in ("Drill", "Peck Drill"):
                d = dia - (REAM_ALLOWANCE_IN if any(h["prop"] == "ISO fit" for h in hs) else 0.0)
                row, note = tl.select_drill(d, depth + DEPTH_EXTRA_RATIO * dia, material, manufacturer)
                j.update(row=row, kind="drill", note=note or "library drill")
            elif op == "Centering":
                row, note = tl.select_chamfer(dia, CHAMFER_WIDTH_IN, material, manufacturer)
                j.update(row=row, kind="chamfer", note=note or "library chamfer mill")
            elif op == "Tapping":
                import hole_tools as ht
                tlen = num(gp(hs[0]["f"], "Hole::Front_Thread::Length")) or depth
                row, note = ht.select_tap(dkey, tlen, material, manufacturer)
                j.update(row=row, kind="tap", note=note or "library tap")
            elif op == "Thread Milling":
                import hole_tools as ht
                tlen = num(gp(hs[0]["f"], "Hole::Front_Thread::Length")) or depth
                row, note = ht.select_threadmill(dkey, tlen, dia, material, manufacturer)
                j.update(row=row, kind="threadmill", note=note or "library thread mill")
            elif op == "Reaming":
                import hole_tools as ht
                row, note = ht.select_reamer(dia, depth, material, manufacturer)
                j.update(row=row, kind="reamer", note=note or "library reamer")
            elif op == "Helical Drilling":
                row, note = tl.select_endmill(dia * HELICAL_TOOL_RATIO, depth, "flat", material, manufacturer)
                j.update(row=row, kind="endmill", note=note or "library end mill")
            if j["row"] is not None and j["kind"] in ("tap", "reamer", "threadmill"):
                import hole_tools as ht
                j["cut"] = ht.cut_for(j["row"], j["kind"], material)
            elif j["row"] is not None and j["kind"] != "chamfer":
                j["cut"] = tl.cut_for(j["row"], j["kind"], material)
            elif j["kind"]:
                j["note"] = note
        except Exception:
            log("tool selection FAILED for", op, dkey, traceback.format_exc()[-300:])
        jobs.append(j)
    jobs.sort(key=lambda j: (ORDER.index(j["op"]) if j["op"] in ORDER else 99, j["dia"]))
    return jobs

def attach_tool(job, tool, log):
    err = []
    for label, fn in (("SetToolByUUID", lambda: job.SetToolByUUID(str(tool.UUID))), ("SetTool", lambda: job.SetTool(tool))):
        try:
            r = fn()
            log("      %s -> %s" % (label, r))
            if r is None or r is True or str(r).endswith("OK"):
                return True
        except Exception as e:
            err.append("%s: %s" % (label, str(e)[:260]))
    log("      attach tool FAILED:", " | ".join(err))
    return False

def set_cut(job, cut, log):
    if not cut:
        return
    for name, v in (("SpindleRPM", cut["rpm"]), ("FeedrateZ", cut["ipm"])):
        try:
            job.SetTTProperty(name, float(v), 1)
            log("      SetTTProperty(%s, %.3f, 1) ok" % (name, v))
        except Exception as e:
            log("      SetTTProperty(%s) FAILED %s" % (name, str(e)[:200]))

# ---------------- chamfer ----------------
CHAMFER_WIDTH_IN = 0.02
EDGE_CHAMFER_REF_IN = 0.2     # Chamfer on 3D Model uses the same MC501 chamfer mill as a 0.2 in hole centering          # chamfer width on the hole edge (Parameters tab, Chamfer width)

def find_chamfer_tool(model):
    """First chamfered cutter in the tool set (fallback when no library chamfer tool is given)."""
    for t in model.ToolSet.GetTools():
        if "CHAMFER" in str(getattr(t, "Type", "")).upper() or "chamfer" in str(t.Name).lower():
            return t
    return None

def make_chamfer_job(model, job, log, tool=None):
    """Centering job -> chamfer existing hole: chamfered cutter in the tool, Machining mode 'Chamfer existing hole', width."""
    t = tool or find_chamfer_tool(model)
    if t is None:
        log("      chamfer: no chamfered cutter in the tool set"); return
    if attach_tool(job, t, log):
        log("      job tool now:", getattr(job.GetTool(), "Name", "?"))
    for name, v in (("DrillStrategy", 1), ("CenChamferwidth", CHAMFER_WIDTH_IN)):
        try:
            job.SetTTProperty(name, float(v), 1)
            log("      SetTTProperty(%s, %s, 1) ok" % (name, v))
        except Exception as e:
            log("      SetTTProperty(%s) FAILED %s" % (name, str(e)[:200]))

# ---------------- milling tools and cleanup ----------------
HOLE_OPS = ("Centering", "Drill", "Peck Drill", "Helical Drilling", "Thread Milling", "Tapping", "Reaming")
# Centering is applied after drilling and carries the chamfer tool (no centering before carbide drills)

def tool_uuids(model):
    return set(str(t.UUID) for t in model.ToolSet.GetTools())

def delete_unused_new_tools(model, before, log):
    """hyperMILL's Python API has no tool delete. Lists the tools no job uses ("new" = came in during this run) so they can be
    deleted in the Tools tab."""
    log("== unused tools (delete in the Tools tab: select them, right-click, delete)")
    used = set()
    for jl in model.JobListSet.GetJobLists():
        for j in jl.GetJobs():
            try:
                used.add(str(j.GetTool().UUID))
            except Exception:
                pass
    n = 0
    for t in model.ToolSet.GetTools():
        if str(t.UUID) not in used:
            n += 1
            log("   unused (%s): %s | NC %s | dia %s" % ("new" if str(t.UUID) not in before else "older", t.Name, t.Number, t.Diameter))
    log("   %d unused tool(s)" % n)
