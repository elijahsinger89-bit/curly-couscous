# part_wizard_1.py - builds the job structure of a part, no tools, no macros.
#   1 machine and spindle (remembered for part_wizard_2)
#   2 industry, part type, setups, part features
#   3 joblists to fill: each needs its frame (NCS), model and material set; stock is reported
#   4 material and stepover, plan summary
#   5 add toolpaths (optional): any of the 77 milling and drilling types (tool_library\job_types.py) added to a joblist
#     hole and pocket feature mapping (only when the file has no feature lists yet)
#   6 one toolpath per planned operation, made with Joblist.CreateJob and the settings in tool_library\job_settings.json
#     (stock to leave, stepdown, stepover, clearance ... per material and operation; edit that file to change them).
#     Types without saved settings are created with hyperMILL's default settings and listed in the final pop-up.
#   7 hole groups: which joblist (setup) each group belongs to, then one hole toolpath per operation and diameter with the
#     holes attached
#   8 picture pop-ups for the toolpaths that need a boundary
# Then: attach the pocket features to the milling toolpaths, set the stock references, run part_wizard_2 (tools), calculate.
# Log: C:\Users\Public\Documents\OPEN MIND\part_wizard_1_log.txt
import os, json, tempfile, traceback

# ---------------- SETTINGS ----------------
PY_DIR       = r"C:\Users\Public\Documents\OPEN MIND\python"
ICON_DIR     = os.path.join(PY_DIR, "icons")
LIB_DIR      = os.path.join(PY_DIR, "tool_library")      # tool_library folder: strategies.py, job_settings.py/.json, hole_jobs.py ...
BOUNDARY_HINTS = True       # picture pop-up for each toolpath that needs a boundary curve or surface
ASK_HOLES    = True         # ask which joblist each hole group belongs to (groups within 30 degrees of a joblist axis are assigned without asking)
HOLE_ASSIGN  = {}           # saved answers, "feature list | direction": joblist name or "skip" (copy from part_wizard_1_log.txt to skip the dialog)
AUTO_STOCK_CHAIN = False    # True = turn on the automatic stock chain on each filled joblist
NAME_JOBS    = True         # name each job by operation and material ("Pocket Milling HEM Inconel 718"); part_wizard_2 reads the operation from it
JOBS_FILE    = os.path.join(tempfile.gettempdir(), "part_wizard_1_jobs.json")   # job id -> operation, read by part_wizard_2
# ------------------------------------------

lines = []
warnings = []
def log(*a):
    lines.append(" ".join(str(x) for x in a))

def warn(text):
    warnings.append(text)
    log("   CHECK:", text)

def load_strategies(*folders):
    """strategies.py by file path (tool_library first, then the python folder), so an old copy elsewhere is never used."""
    import importlib.util
    path = None
    for folder in folders:
        for cand in (os.path.join(folder, "strategies.py"), os.path.join(folder, "strategies", "strategies.py")):
            if os.path.exists(cand):
                path = cand
                break
        if path:
            break
    if path is None:
        raise RuntimeError("strategies.py not found in " + " or ".join(folders))
    spec = importlib.util.spec_from_file_location("hm_strategies", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.LOADED_FROM = path
    for need in ("setup_for", "operations", "plan", "sequence_text", "VERSION"):
        if not hasattr(mod, need):
            raise RuntimeError("strategies.py at %s is an old version (missing %s)." % (path, need))
    return mod

def load_lib(folder):
    """Imports and reloads the tool_library modules (hyperMILL keeps imported modules between runs)."""
    import sys, importlib
    if folder not in sys.path:
        sys.path.insert(0, folder)
    mods = {}
    for n in ("tool_numbers", "tool_builder", "job_settings", "job_types", "hole_jobs", "machine_pick"):
        m = importlib.import_module(n)
        importlib.reload(m)
        mods[n] = m
    return mods

S = None
try:
    S = load_strategies(LIB_DIR, PY_DIR)
except Exception:
    log("FAILED loading strategies:", traceback.format_exc())

def val(x):
    return x() if callable(x) else x

# ---------------- dialogs (om.cad.gui.InputDialog) ----------------
def _gui():
    import om.cad.gui as g
    return g

def _dialog(title):
    return _gui().InputDialog(title)

def _icon(name):
    p = os.path.join(ICON_DIR, name + ".png")
    return p if os.path.exists(p) else ""

def choose(title, label, options, icons=None, default=0):
    """Dropdown. Returns the chosen index, or None on Cancel."""
    g = _gui()
    for use_icons in ((True, False) if icons else (False,)):
        try:
            dlg = _dialog(title)
            dlg.AddDropDown(label, list(options), defaultIndex=default, icons=icons if use_icons else None)
            ok, vals = dlg.Show()
        except Exception:
            log("dropdown with icons failed" if use_icons else "dropdown failed", traceback.format_exc()[-300:])
            continue
        if not ok:
            return None
        v = vals[label]
        if isinstance(v, bool):
            return 0
        if isinstance(v, int):
            return v if 0 <= v < len(options) else 0
        if v in options:
            return list(options).index(v)
        try:
            n = int(v)
            return n if 0 <= n < len(options) else 0
        except (TypeError, ValueError):
            return 0
    return None

def checks(title, items):
    """Checkbox list [(label, default)]. Returns list of bools, or None on Cancel."""
    g = _gui()
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

# ---------------- wizard flow (no hyperMILL calls; testable) ----------------
NOT_SURE = "Not sure - show me pictures"

def pick_part(ui):
    """Industry -> part, or picture picker when unknown. Returns a part key or None."""
    inds = [n for n, _ in S.INDUSTRIES]
    i = ui.choose("Part wizard", "Industry", inds + ["Not sure"], default=0)
    if i is None:
        return None
    industry = inds[i] if i < len(inds) else None
    if industry:
        keys = S.parts_in_industry(industry)
        names = [S.PARTS[k]["name"] for k in keys]
        j = ui.choose("Part wizard " + industry, "Part type", names + [NOT_SURE], default=0)
        if j is None:
            return None
        if j < len(keys):
            return keys[j]
    # picture picker
    shapes = [s for s in S.SHAPES if not industry or any(S.industry_of(p) == industry for p in s[2])]
    if not shapes:
        shapes = list(S.SHAPES)
    k = ui.choose("Part wizard shape", "Shape",
                  [s[1] for s in shapes], icons=[_icon(s[0]) for s in shapes], default=0)
    if k is None:
        return None
    cands = [p for p in shapes[k][2] if not industry or S.industry_of(p) == industry] or list(shapes[k][2])
    if len(cands) == 1:
        return cands[0]
    names = [S.PARTS[p]["name"] for p in cands]
    m = ui.choose("Part wizard closest match", "Part type", names, default=0)
    return None if m is None else cands[m]

def pick_features(ui, part):
    flags = S.relevant_features(part)
    items = [(S.FEATURE_LABELS[f], f in S.PARTS[part]["features"]) for f in flags]
    r = ui.checks("Part features", items)
    if r is None:
        return None
    return {f for f, on in zip(flags, r) if on}

MAX_POPUP_CHARS = 2500
SMALL_TAB_PARTS = ("core_pin", "dental_abutment")
MOLD_BLOCKS = ("mold_cavity", "die_forging_insert", "molding_surface_block", "punch_die_insert", "mold_slide_lifter", "blow_mold_half", "thrust_chamber_liner")

def recommended_setups(part):
    """(number of setups, reason) for a generic 5-axis machine. Basis: five-sided machining reaches every face except the one
    on the fixture, so a fully machined prismatic part needs two setups (the second takes the clamped face); fewer when the
    blank arrives turned or the clamp area is a tab cut off last; more when stress relief or warpage control needs a re-datum."""
    P = S.PARTS[part]; f = P["features"]
    if "blades" in f:
        return 1, "The turned blank comes from the lathe. Mill the flow path, blades and holes in one 5-axis setup."
    if part in SMALL_TAB_PARTS:
        return 1, "Small part: hold it on a stock tab or dovetail, machine five sides, cut the tab last."
    if part in MOLD_BLOCKS:
        return 1, "One 5-axis setup reaches the cavity or core and its sides. The back is the squared reference face."
    if "warpage" in f:
        return 3, "Rough, stress relieve and re-datum, then finish. Flip as needed to keep the part balanced."
    if "heat treat" in " ".join(str(v) for v in S.SETUP_GUIDE.get(P["family"], {}).values()).lower():
        return 2, "Rough before heat treat; finish the datum faces, bores and holes after heat treat."
    return 2, "Five-sided machining reaches every face except the one on the fixture. The second setup machines the clamped face."

SETUP_CHOICES = ["Part default", "1 setup", "2 setups", "3 setups", "4 setups", "5 setups", "6 setups"]

def build_plan(part, joblists, features):
    """joblists: [(name, material group)]. Returns list of dicts for the summary.
    When setups are merged, a joblist that maps to an already planned setup is left empty."""
    plan = []
    used = set()
    for jl_name, group in joblists:
        setup = S.setup_for(part, jl_name, features=features)
        if setup is None:
            plan.append({"joblist": jl_name, "group": group, "setup": "no matching setup for this part",
                         "ops": [], "manual": [], "notes": [], "guide": "", "sequence": ""})
            continue
        if (setup, group) in used:
            plan.append({"joblist": jl_name, "group": group, "setup": "merged into " + setup,
                         "ops": [], "manual": [], "notes": [], "guide": "", "sequence": ""})
            continue
        used.add((setup, group))
        steps = S.plan(part, group, setup, features)
        plan.append({"joblist": jl_name, "group": group, "setup": setup,
                     "ops": S.operations(part, group, setup, features),
                     "seq_ops": S.operation_sequence(part, group, setup, features),
                     "manual": [s["why"] for s in steps if s["manual"]],
                     "notes": S.notes(part, group, features),
                     "guide": S.setup_guide(part, setup, features),
                     "sequence": S.sequence_text(part, group, setup, features)})
    return plan

def summary_text(part, plan):
    t = ["Part: " + S.PARTS[part]["name"], ""]
    for p in plan:
        t.append("%s  [%s, %s]" % (p["joblist"], p["setup"], p["group"]))
        if p.get("guide"):
            t.append("   " + p["guide"])
        t.extend("   %d. %s" % (i + 1, o) for i, o in enumerate(p["ops"]))
        t.extend("   manual: " + m for m in p["manual"])
        t.append("")
    t.append("Notes:")
    seen = []
    for p in plan:
        for n in p["notes"]:
            if n not in seen:
                seen.append(n)
    t.extend("- " + n for n in seen)
    text = "\n".join(t)
    if len(text) > MAX_POPUP_CHARS:
        text = text[:MAX_POPUP_CHARS].rsplit("\n", 1)[0] + "\n... (cut for length; the full plan is in part_wizard_1_log.txt)"
    return text

PART_PICTURE = {  # part key -> drawing used in the boundary window (icons\bnd_<drawing>_<operation>.png)
    'aero_actuator_housing': 'manifold',
    'aero_gearbox_housing': 'housing',
    'api_flange': 'disc',
    'bearing_housing_flange': 'disc',
    'blisk_hrsa': 'blades',
    'blisk_titanium': 'blades',
    'blow_mold_half': 'mold',
    'bone_plate': 'bone_plate',
    'brake_caliper': 'housing',
    'central_wing_box': 'panel',
    'choke_valve_body': 'manifold',
    'clevis_lug_fitting': 'bracket',
    'cold_plate': 'plate',
    'combustion_casing': 'disc',
    'composite_wing_skin': 'panel',
    'compression_mold_plate': 'plate',
    'compressor_vane_ring': 'disc',
    'control_arm': 'rib_frame',
    'core_pin': 'pin',
    'crank_arm': 'bracket',
    'cylinder_head': 'housing',
    'defense_bracket_armor': 'plate',
    'dental_abutment': 'pin',
    'die_forging_insert': 'mold',
    'downhole_tool_housing': 'shaft',
    'drone_frame_plate': 'box_enclosure',
    'end_cap_cylinder': 'plate',
    'engine_block': 'housing',
    'engine_mount': 'bracket',
    'fan_casing': 'disc',
    'fan_disc': 'disc',
    'fixture_plate': 'plate',
    'flap_track': 'bracket',
    'frac_fluid_end': 'housing',
    'fuselage_bulkhead': 'rib_frame',
    'gas_manifold': 'manifold',
    'gearbox_housing': 'housing',
    'gimbal_mount': 'box_enclosure',
    'gripper_finger': 'bracket',
    'harmonic_drive_housing': 'housing',
    'heat_sink_enclosure': 'box_enclosure',
    'hip_stem': 'stem',
    'hot_runner_manifold': 'manifold',
    'impeller': 'blades',
    'inspection_fixture': 'plate',
    'intake_manifold': 'housing',
    'knee_femoral': 'knee',
    'landing_gear_beam': 'rib_frame',
    'lower_receiver': 'receiver',
    'main_fitting': 'bracket',
    'manifold_block': 'manifold',
    'mold_base_plate': 'plate',
    'mold_cavity': 'mold',
    'mold_ejector_plate': 'plate',
    'mold_slide_lifter': 'mold',
    'molding_surface_block': 'mold',
    'optic_mount': 'bracket',
    'optical_mount': 'bracket',
    'orthopedic_trial': 'plate',
    'piston_forged': 'disc',
    'plate_bracket': 'plate',
    'progressive_die_plate': 'plate',
    'propeller_blade': 'blades',
    'pump_casing': 'housing',
    'punch_die_insert': 'mold',
    'pylon_bracket': 'bracket',
    'rf_waveguide': 'plate',
    'robot_arm_link': 'rib_frame',
    'rocket_injector_plate': 'manifold',
    'rocket_nozzle_extension': 'disc',
    'satellite_housing': 'box_enclosure',
    'satellite_panel_bracket': 'rib_frame',
    'seat_track': 'rail',
    'shaft': 'shaft',
    'showerhead_plate': 'plate',
    'slat_track': 'bracket',
    'soft_jaws': 'plate',
    'spinal_cage': 'cage',
    'spool': 'disc',
    'suppressor_baffle': 'shaft',
    'surgical_instrument': 'shaft',
    'telescope_housing': 'housing',
    'thrust_chamber_liner': 'mold',
    'thrust_fitting': 'bracket',
    'tombstone_fixture': 'plate',
    'transmission_case': 'housing',
    'turbine_blade_dovetail': 'dovetail',
    'turbine_disc': 'disc',
    'turbo_housing': 'housing',
    'turbopump_housing': 'housing',
    'turret_ring_housing': 'housing',
    'unibody_enclosure': 'box_enclosure',
    'upper_receiver': 'receiver',
    'vacuum_chamber': 'housing',
    'valve_body': 'manifold',
    'vertical_tail_frame': 'panel',
    'wafer_chuck': 'plate',
    'weldment_frame': 'weldment',
    'weldment_machine_base': 'weldment',
    'wellhead_body': 'housing',
    'wheel_hub_upright': 'bracket',
    'wing_rib': 'rib_frame',
    'wing_spar': 'rib_frame',
}
OP_PICTURE = {"Face Mill": "face", "Rough HEM": "rough", "Pocket HEM": "pocket", "Automatic Rest Machining": "rest", "Contour Finish": "contour", "Plane Finish": "plane", "Z Level Shape Finish": "zlevel", "3D Profile Finish Ball": "ball", "Swarf Curve": "contour", "Swarf Surface": "contour"}

# Picture hints for operations that need a boundary curve or surface selection.
# op name -> (picture file, what to create)
BOUNDARY_TEXT = {
    "Face Mill":                 ("bnd_face_mill", "Create a boundary curve around the whole top face to be faced (orange area), slightly outside the part edge."),
    "Rough HEM":                 ("bnd_rough_hem", "Create a closed boundary curve around the area to be roughed (orange area), on the outer stock edge."),
    "Pocket HEM":                ("bnd_pocket_hem", "Create a closed boundary curve on the top edge of each pocket to clear (orange area)."),
    "Automatic Rest Machining":  ("bnd_rest", "Create a boundary curve around the corner areas the large tool left (orange corners), or around the whole pocket."),
    "Contour Finish":            ("bnd_contour", "Select the wall edge curves to finish (orange ring) or draw a boundary along the wall top edge."),
    "Plane Finish":              ("bnd_plane", "Select the flat floor faces to finish, or draw a boundary curve around the floor (orange area)."),
    "Swarf Curve":               ("bnd_contour", "Swarf: select the guide curve along the bottom or top edge of the wall to finish (orange ring)."),
    "Swarf Surface":             ("bnd_contour", "Swarf: select the wall surfaces to finish with the side of the tool (orange ring)."),
    "Z Level Shape Finish":      ("bnd_zlevel", "Create a boundary curve around the steep surfaces to finish (orange rings)."),
    "3D Profile Finish Ball":    ("bnd_ball", "Create a boundary curve around the contoured surface to blend (orange area)."),
}


def boundary_window(title, text, png):
    """Small always-on-top window that stays open while hyperMILL remains usable. Returns 'done' or 'skip'.
    The script waits in a loop that keeps processing hyperMILL's events, so you can draw the boundary, then click Done."""
    import time
    import tkinter as tk
    result = {"v": None}
    root = tk.Tk()
    root.title(title)
    root.attributes("-topmost", True)
    try:
        img = tk.PhotoImage(file=png)
        if img.width() < 200:
            img = img.zoom(3, 3)
        tk.Label(root, image=img).pack(padx=8, pady=8)
    except Exception:
        pass
    tk.Label(root, text=text, wraplength=380, justify="left").pack(padx=8, pady=4)
    row = tk.Frame(root); row.pack(pady=8)
    tk.Button(row, text="Done - next operation", width=22, command=lambda: result.update(v="done")).pack(side="left", padx=4)
    tk.Button(row, text="Skip remaining hints", width=22, command=lambda: result.update(v="skip")).pack(side="left", padx=4)
    root.protocol("WM_DELETE_WINDOW", lambda: result.update(v="done"))
    root.geometry("+40+40")
    g = _gui()
    while result["v"] is None:
        root.update()
        try:
            g.ProcessEvents()
        except Exception:
            pass
        time.sleep(0.05)
    root.destroy()
    return result["v"]

def boundary_hint(ui, jl_name, name, state, part=None, job=None):
    """Picture window for one created operation; hyperMILL stays usable until you click Done."""
    if not state.get("on", True):
        return
    try:
        op = name.split(" | ")[-1]
        h = BOUNDARY_TEXT.get(op)
        if not h:
            return
        png = _icon("bnd_%s_%s" % (PART_PICTURE.get(part, ""), OP_PICTURE.get(op, ""))) or _icon(h[0])
        pname = S.PARTS[part]["name"] if part in S.PARTS else ""
        jname = ""
        try:
            jname = str(job.Name) if job is not None else ""
        except Exception:
            pass
        title = "Boundary needed: " + (jname or op) + " (" + jl_name + ")" + (" - " + pname if pname else "")
        try:
            r = boundary_window(title, h[1] + ("\n\nToolpath: " + jname if jname else ""), png)
        except Exception:
            log("   boundary window FAILED, using message box", traceback.format_exc()[-300:])
            url = "file:///" + png.replace("\\", "/")
            ui.info(title, "<b>%s</b> (%s)<br>%s<br><br><img src='%s' width='400' height='400'><br>" % (op, jl_name, h[1], url))
            r = "done"
        if r == "skip":
            state["on"] = False
        log("   boundary hint shown:", op, "->", r)
    except Exception:
        log("   boundary hint FAILED", traceback.format_exc()[-300:])

# ---------------- toolpath creation (no macros) ----------------
LIB = {}

def _num(x):
    try:
        return float(str(x).strip())
    except Exception:
        return None

def _same(a, b):
    if str(a) == str(b):
        return True
    fa, fb = _num(a), _num(b)
    return fa is not None and fb is not None and abs(fa - fb) <= 1e-6 * max(1.0, abs(fa))

def joblist_check(jl, groups):
    """(missing items that stop the run, frame name, model name, stock name)."""
    miss = []
    def name_of(get):
        try:
            o = get()
            return str(getattr(o, "Name", "") or "") if o is not None else ""
        except Exception:
            return ""
    fn = name_of(lambda: jl.NCS)
    mn = name_of(jl.GetModel)
    sn = name_of(jl.GetStock)
    mat = str(jl.Material or "")
    if not fn:
        miss.append("frame (NCS)")
    if not mn:
        miss.append("model")
    if not mat:
        miss.append("material")
    elif mat not in groups:
        miss.append("material group '%s' is not in job_settings.json" % mat)
    return miss, fn, mn, sn

def milling_area(jl):
    """Milling area of the first job already in the joblist, else the joblist model."""
    for j in jl.GetJobs():
        try:
            ma = j.GetMillingArea()
            if ma is not None:
                return ma, "from job " + str(j.Name)
        except Exception:
            pass
    try:
        m = jl.GetModel()
        if m is not None:
            return m, "joblist model " + str(getattr(m, "Name", ""))
    except Exception:
        pass
    return None, "none"

TOOL_DRIVEN = ("FEEDRATE", "SPINDLE", "VORSCHUB", "DREHZAHL", "_ABS")   # feed, speed and absolute stepover follow the tool (part_wizard_2)
MISSED = {}     # setting key -> [operations] that kept another value; listed once in the final pop-up

def apply_settings(job, params):
    """Writes the operation's settings into a new job. A formula (*KEY_F) the new job carries but the settings do not list
    would override the setting's value, so it is set to that value as a constant formula. Returns the keys that
    did not take (formula-driven, feed/speed and keys this job type does not use are logged, not returned)."""
    try:
        cur = dict(job.GetCfgParameters())
    except Exception as e:
        cur = {}
        log("      GetCfgParameters FAILED", str(e)[:100])
    want = dict(params)
    fixed = []
    for k, v in cur.items():
        if k.endswith("_F") and k not in want and str(v or "").strip():
            base = k[:-2]
            if base in want and str(want[base]).strip():
                want[k] = str(want[base])          # constant formula = the saved value
                fixed.append(k)
    new_keys = [k for k in want if cur and k not in cur]
    bad = []
    try:
        r = job.SetCfgParameters(want)
        log("      settings: %d keys (%d formulas set to the saved value, %d keys the new job did not have) -> %s" % (len(want), len(fixed), len(new_keys), r))
    except Exception as e:
        log("      settings in one call FAILED (%s); setting them one at a time" % str(e).replace("\n", " ")[:150])
        for k, v in want.items():
            try:
                job.SetCfgParameters({k: v})
            except Exception:
                bad.append(k)
        if bad:
            log("      keys refused:", bad[:30])
    try:
        after = dict(job.GetCfgParameters())
    except Exception:
        return bad
    unused, by_formula, by_tool, diff = [], [], [], []
    for k, v in want.items():
        if k in bad or _same(after.get(k), v):
            continue
        if k.endswith("_F") and after.get(k) is None and (k[:-2] not in want or _same(after.get(k[:-2]), want[k[:-2]])):
            continue                               # a constant formula is stored as the plain value: the formula is gone, the value is right
        if after.get(k) is None and k not in cur:
            unused.append(k)                       # this job type has no such setting
        elif str(after.get(k + "_F") or "").strip() and not k.endswith("_F"):
            by_formula.append(k)                   # a formula sets it (frame clearance F:Cl, job feed J:F ...)
        elif any(t in k for t in TOOL_DRIVEN):
            by_tool.append(k)
        else:
            diff.append(k)
    if unused:
        log("      not used by this job type:", ", ".join(unused[:12]))
    if by_formula:
        log("      set by formula:", "; ".join("%s=%s (%s)" % (k, after.get(k), after.get(k + "_F")) for k in by_formula[:12]))
    if by_tool:
        log("      follow the tool's cutting data:", ", ".join(by_tool[:12]))
    if diff:
        log("      %d key(s) read back different:" % len(diff), "; ".join("%s=%s (wanted %s)" % (k, after.get(k), want[k]) for k in diff[:12]))
    return bad + diff

def create_job(model, jl, op, found, ma, created, feats=None, frame=None):
    name, cmt, rec = found
    code = rec["code"]
    try:
        job = jl.CreateJob(code)
    except Exception as e:
        warn("%s: CreateJob(%s) failed: %s" % (op, code, str(e)[:100])); return None
    if job is None:
        warn("%s: CreateJob(%s) returned nothing" % (op, code)); return None
    log("   created:", op, "| code", code, "| from", name, "|", cmt or "-")
    if feats:
        try:
            log("      SetFeatures (%d) -> %s" % (len(feats), job.SetFeatures(feats)))
        except Exception as e:
            warn("%s: features not attached: %s" % (op, str(e)[:100]))
    if feats:
        try:
            now = str(getattr(job.GetFrame(), "Name", ""))
            if frame is None:
                log("      frame %s (set by the features; the feature list has no frame)" % now)
            elif now != str(frame.Name):
                log("      frame %s -> %s: %s | now %s" % (now, frame.Name, job.SetFrame(frame), getattr(job.GetFrame(), "Name", "?")))
            else:
                log("      frame %s" % now)
        except Exception as e:
            log("      SetFrame FAILED", str(e)[:100])
    if rec.get("params") is None:
        log("      hyperMILL default settings (no saved settings for this operation)")
    else:
        for k in apply_settings(job, rec["params"]):
            MISSED.setdefault(k, []).append(op)
    if NAME_JOBS and rec.get("jobname"):
        try:
            job.Name = rec["jobname"]
        except Exception as e:
            log("      job name not set:", str(e)[:80])
    if ma is not None:
        try:
            log("      SetMillingArea ->", job.SetMillingArea(ma))
        except Exception as e:
            log("      SetMillingArea FAILED", str(e)[:100])
    created.append((job, op, name, cmt))
    return job

def settings_for(data, group, material, op, stepover, defaults_used):
    """(label, stepover, settings) from job_settings.json; an operation without saved settings gets its CreateJob code and
    hyperMILL's default settings. None when the operation is unknown."""
    found = LIB["job_settings"].find(data, group, material, op, stepover)
    if found:
        return found
    spec = LIB["job_types"].OPS.get(op)
    if spec is None:
        warn("unknown operation %s, not created" % op)
        return None
    defaults_used.add(op)
    return "hyperMILL defaults | " + op, "", dict(code=spec["code"], jobname="%s %s" % (op, material), params=None)

def add_toolpaths(ui, targets):
    """Optional: any milling or drilling toolpath type added to a joblist after the plan. Returns {joblist name: [operations]}."""
    jt = LIB["job_types"]
    labels = jt.picker_labels()
    out = {}
    while True:
        names = [jl.Name for jl in targets]
        k = ui.choose("Add toolpaths", "Add a toolpath to the plan?", ["No - continue"] + ["Add to " + n for n in names], default=0)
        if not k:
            break
        i = ui.choose("Add toolpaths", "Toolpath type for " + names[k - 1], labels, default=0)
        if i is None:
            continue
        op = labels[i].split(" | ", 1)[1]
        out.setdefault(names[k - 1], []).append(op)
        log("added by the operator:", op, "->", names[k - 1])
    return out

HOLE_OPS = ("Centering", "Drill", "Peck Drill", "Chip Break Drill", "Helical Drilling", "Thread Milling", "Tapping", "Reaming")   # made from the mapped holes
THROUGH_OPS = ("Drill", "Peck Drill", "Chip Break Drill", "Reaming")      # go on through to the far end of a merged opposite hole
JOB_THROUGH = {}     # job uuid -> {hole feature uuid: length through to the opposite hole}, for part_wizard_2

def attached_uuids(model):
    s = set()
    for jl in model.JobListSet.GetJobLists():
        for j in jl.GetJobs():
            try:
                for f in j.GetFeatures():
                    s.add(str(f.UUID))
            except Exception:
                pass
    return s

def hole_buckets(hj, holes):
    """One toolpath per operation and diameter (taps and thread mills: per thread), in machining order."""
    b = {}
    for h in holes:
        for op in h["ops"]:
            if op in ("Thread Milling", "Tapping"):
                key = (op, hj.gp(h["f"], "Hole::Front_Thread::Designation") or ("%.4f" % h["dia"]))
            elif op in ("Drill", "Peck Drill") and h["prop"] == "ISO fit":
                key = (op, "%.4f ream" % h["dia"] + (" thru %.4f" % h["through"] if h.get("through") else ""))   # drilled under size for reaming: never shares a toolpath with plain holes
            elif h.get("through"):
                key = (op, "%.4f thru %.4f" % (h["dia"], h["through"]))   # drilled through to the opposite hole: its own break-through length
            else:
                key = (op, round(h["dia"], 4))
            b.setdefault(key, []).append(h)
    return sorted(b.items(), key=lambda kv: (hj.ORDER.index(kv[0][0]) if kv[0][0] in hj.ORDER else 99, max(h["dia"] for h in kv[1])))

def run_holes(model, targets, data, mats, stepover, apply_now, created, frames, chip_break=()):
    hj, js = LIB["hole_jobs"], LIB["job_settings"]
    done = attached_uuids(model)
    groups = {}
    for key, hl in hj.read_holes(model, log).items():
        hl = [h for h in hl if str(h["f"].UUID) not in done]
        if hl:
            groups[key] = hl
    if not groups:
        log("holes: no mapped Generic Hole features without a toolpath")
        return
    names = [jl.Name for jl in model.JobListSet.GetJobLists()]
    ask = hj.ask_dialog(names, log) if ASK_HOLES else None
    assign = hj.assign_groups(model, groups, HOLE_ASSIGN, ask, log)
    for note in hj.merge_opposing(groups, assign, names, log):
        warn(note)
    for jl in targets:
        mat = mats.get(jl.Material, "")
        mine = [(key, hl) for key, hl in groups.items() if assign.get("%s | %s" % (key[0], key[2])) == jl.Name]
        if mine and not mat:
            warn("%s has no material (or no settings for its material group): its hole toolpaths were not created" % jl.Name); continue
        ma, _ = milling_area(jl)
        mine = [(key, hl) for key, hl in groups.items() if assign.get("%s | %s" % (key[0], key[2])) == jl.Name]
        for key, hl in mine:
            log("== holes:", key[0], "| frame", key[1], "| direction", key[2], "->", jl.Name, "|", len(hl), "holes")
            for h in hl:
                if not h["ops"]:
                    warn("hole %d by hand: %s" % (h["id"], h["note"]))
            for (op, dkey), hs in hole_buckets(hj, hl):
                if op == "Drill" and jl.Name in chip_break:
                    op = "Chip Break Drill"          # the plan asks for chip breaking in this material
                label = "%s %s | holes %s" % (op, dkey, ",".join(str(h["id"]) for h in hs))
                found = settings_for(data, jl.Material, mat, op, stepover, set())
                if not found:
                    continue
                if not apply_now:
                    log("   plan:", label, "| settings from", found[0]); continue
                job = create_job(model, jl, op, found, ma, created, feats=[h["f"] for h in hs], frame=frames.get(key[1]))
                thru = [h for h in hs if h.get("through")]
                if job is not None and thru:
                    JOB_THROUGH[str(job.UUID)] = {str(h["f"].UUID): h["through"] for h in thru}
                    if op in THROUGH_OPS:
                        extra = max(h["through"] - h["depth"] for h in thru) + hj.BREAK_EXTRA_IN
                        want = {"*USE_BREAK_THROUGH_LENGTH": "1", "*BREAK_THROUGH_LENGTH": "%.4f" % extra}
                        try:
                            r = job.SetCfgParameters(want)
                            back = dict(job.GetCfgParameters())
                            log("      through to the opposite hole: break-through length %.4f -> %s | reads back %s %s" % (
                                extra, r, back.get("*USE_BREAK_THROUGH_LENGTH"), back.get("*BREAK_THROUGH_LENGTH")))
                            if not _same(back.get("*BREAK_THROUGH_LENGTH"), "%.4f" % extra):
                                warn("%s: break-through length %.4f did not take, set the drill depth through holes %s by hand" % (
                                    op, extra, ",".join(str(h["id"]) for h in thru)))
                        except Exception as e:
                            warn("%s: break-through length not set (%s), set the drill depth by hand" % (op, str(e)[:80]))
                    elif op != "Centering":
                        warn("%s: holes %s go through to the opposite hole; this cycle stops at the first hole's depth, extend it by hand" % (
                            op, ",".join(str(h["id"]) for h in thru)))
                if job is not None and op == "Centering":
                    for nm, v in (("DrillStrategy", 1), ("CenChamferwidth", hj.CHAMFER_WIDTH_IN)):      # chamfer existing hole
                        try:
                            job.SetTTProperty(nm, float(v), 1)
                            log("      SetTTProperty(%s, %s, 1) ok" % (nm, v))
                        except Exception as e:
                            log("      SetTTProperty(%s) not set yet (part_wizard_2 sets it with the tool): %s" % (nm, str(e)[:100]))

def save_jobs(created):
    d = {}
    try:
        with open(JOBS_FILE, encoding="utf-8") as f:
            d = json.load(f)
    except Exception:
        pass
    for job, op, name, cmt in created:
        try:
            d[str(job.UUID)] = dict(op=op, settings=name, stepover=cmt, group=str(job.JobList.Material),
                                    through=JOB_THROUGH.get(str(job.UUID), {}))
        except Exception:
            pass
    try:
        with open(JOBS_FILE, "w", encoding="utf-8") as f:
            json.dump(d, f)
        log("job list for part_wizard_2:", JOBS_FILE, "|", len(d), "jobs")
    except Exception as e:
        log("job list not saved:", e)

def _write_log():
    for p in [r"C:\Users\Public\Documents\OPEN MIND\part_wizard_1_log.txt",
              os.path.join(os.path.expanduser("~"), "Documents", "part_wizard_1_log.txt"),
              os.path.join(tempfile.gettempdir(), "part_wizard_1_log.txt")]:
        try:
            with open(p, "w", encoding="utf-8") as f:
                f.write("\n".join(lines))
            return p
        except Exception:
            continue

def run(ui=UI, model=None, write_log=True):
    MISSED.clear()
    JOB_THROUGH.clear()
    try:
        if model is None:
            import om
            model = om.Application().CurrentDocument.CamModel
        if S is None:
            ui.info("Part wizard 1", "strategies.py could not be loaded. See part_wizard_1_log.txt."); return
        log("strategies:", S.LOADED_FROM, "| version", S.VERSION)
        inch = bool(val(model.IsInchMode))
        LIB.update(load_lib(LIB_DIR))
        js, hj = LIB["job_settings"], LIB["hole_jobs"]
        sp = LIB["machine_pick"].pick_spindle(_dialog, "Part wizard 1 - machine", log)
        if sp is None:
            log("cancelled at machine"); return
        if not inch:
            ui.info("Part wizard 1", "This session is metric. job_settings.json holds inch values."); log("metric session, stopped"); return
        data = js.load(log)
        groups = js.groups(data)
        lists = list(model.JobListSet.GetJobLists())
        if not lists:
            ui.info("Part wizard 1", "No joblists in this document.\nCreate one joblist per setup (frame, model, material, stock), then run again.")
            log("no joblists"); return
        part = pick_part(ui)
        if part is None:
            log("cancelled at part selection"); return
        log("part:", part)
        rec_n, rec_why = recommended_setups(part)
        own = len(S._setups(part))
        log("recommended setups:", rec_n, "|", rec_why, "| part default:", own)
        ui.info("Recommended setups", "%s should have %d setup%s on a generic 5-axis machine.\n%s\nThe part default plans %d." % (S.PARTS[part]["name"], rec_n, "" if rec_n == 1 else "s", rec_why, own))
        n_setups = ui.choose("Setups", "Setups on the 5-axis machine", SETUP_CHOICES, default=min(rec_n, own) if rec_n < own else 0)
        if n_setups is None:
            log("cancelled at setups"); return
        S.MAX_SETUPS = n_setups or None
        log("max setups:", S.MAX_SETUPS)
        features = pick_features(ui, part)
        if features is None:
            log("cancelled at features"); return
        r = ui.checks("Joblists to fill", [("Fill " + jl.Name, True) for jl in lists])
        if r is None:
            log("cancelled at joblists"); return
        targets = [jl for jl, on in zip(lists, r) if on]
        if not targets:
            log("no joblists ticked"); return
        # every joblist needs its frame, model and material before toolpaths go in
        report, stop = [], False
        for jl in targets:
            miss, fn, mn, sn = joblist_check(jl, groups)
            log("joblist", jl.Name, "| frame", fn or "-", "| model", mn or "-", "| material", jl.Material or "-", "| stock", sn or "-", "| missing:", miss)
            report.append("%s: frame %s | model %s | material %s | stock %s%s" % (jl.Name, fn or "MISSING", mn or "MISSING", jl.Material or "MISSING", sn or "none yet",
                                                                                  ("\n   set first: " + ", ".join(miss)) if miss else ""))
            stop = stop or bool(miss)
        if stop:
            ui.info("Joblists not ready", "\n".join(report)[:1500] + "\n\nSet these in the joblist (Edit joblist), then run again.")
            k = ui.choose("Joblists not ready", "Next", ["Stop and fix the joblists", "Continue anyway"], default=0)
            if k != 1:
                log("stopped: joblists not ready"); return
            warn("continued with joblists not ready: " + "; ".join(x.replace("\n   set first:", " | set first:") for x in report if "set first" in x))
        mats = {}
        for g in sorted(set(jl.Material for jl in targets)):
            names = js.materials(data, g)
            if not names:
                log("no job settings for group", g); mats[g] = ""; continue
            i = ui.choose("Material", "Material for " + g, names, default=0)
            if i is None:
                log("cancelled at material"); return
            mats[g] = names[i]
        j = ui.choose("Stepover", "Stepover type", ["Percent stepover", "Distance stepover"], default=0)
        if j is None:
            return
        stepover = ["Percent stepover", "Distance stepover"][j]
        log("materials:", mats, "| stepover:", stepover)
        plan = build_plan(part, [(jl.Name, jl.Material) for jl in targets], features)
        ui.info("Plan", summary_text(part, plan))
        extra = add_toolpaths(ui, targets)
        go = ui.checks("Create", [("Create the toolpaths now (leave unticked for a dry run that only writes the log)", False),
                                  ("Create the hole toolpaths from the mapped holes (asks which joblist each hole group belongs to)", True),
                                  ("Show a picture pop-up for each toolpath that needs a boundary", BOUNDARY_HINTS),
                                  ("Run hole and pocket feature mapping first (only when the file has no feature lists)", True)])
        if go is None:
            log("cancelled at confirm"); return
        apply_now, want_holes, want_hints, want_map = go
        log("create:", apply_now, "| holes:", want_holes, "| pictures:", want_hints, "| mapping:", want_map)
        if want_map and apply_now:
            fls = model.FeatureListSet
            if list(fls.GetFeatureLists()):
                log("feature mapping skipped: feature lists already exist")
            else:
                log("hole feature mapping ->", fls.HoleFeatureMapping())
                log("pocket feature mapping ->", fls.PocketFeatureMapping())
                n = list(fls.GetFeatureLists())
                log("feature lists after mapping:", len(n), "| features:", sum(len(list(fl.GetFeatures())) for fl in n))
        frames = {}
        try:
            for fr in model.FrameSet.GetFrames():
                frames[str(getattr(fr, "Name", ""))] = fr
        except Exception as e:
            log("frames not read:", e)
        created, hint_queue, chip_break, defaults_used = [], [], set(), set()
        for jl, p in zip(targets, plan):
            mat = mats.get(jl.Material, "")
            if not mat:
                warn("%s has no material (or no settings for its material group): nothing created in it" % jl.Name); continue
            full = p.get("seq_ops") or p["ops"]
            ops = []
            for o in full:
                if not (want_holes and o in HOLE_OPS) and o not in ops:
                    ops.append(o)              # an operation planned twice (two reasons in the plan) is made once
            ops += extra.get(jl.Name, [])      # toolpaths added on the Add toolpaths screen, always made
            if "Chip Break Drill" in full:
                chip_break.add(jl.Name)
            log("== joblist:", jl.Name, "| setup:", p["setup"], "| group:", jl.Material, "| material:", mat)
            for line in p["sequence"].split("\n"):
                log("   seq:", line)
            for m in p["manual"]:
                log("   by hand:", m)
            if want_holes and any(o in HOLE_OPS for o in full):
                log("   hole operations come from the mapped holes:", sorted(set(o for o in full if o in HOLE_OPS)))
            ma, ma_src = milling_area(jl)
            log("   milling area for new jobs:", ma_src)
            for o in ops:
                found = settings_for(data, jl.Material, mat, o, stepover, defaults_used)
                if not found:
                    continue
                if not apply_now:
                    log("   plan:", o, "| settings from", found[0], "|", found[1] or "-", "| code", found[2]["code"]); continue
                job = create_job(model, jl, o, found, ma, created)
                if job is not None:
                    hint_queue.append((jl.Name, found[0], job))
            if apply_now and AUTO_STOCK_CHAIN:
                try:
                    jl.EnableAutoStockChain(True)
                    log("   automatic stock chain on:", jl.AutoStockChainEnabled())
                except Exception as e:
                    log("   automatic stock chain FAILED", e)
        if want_holes:
            run_holes(model, targets, data, mats, stepover, apply_now, created, frames, chip_break)
        if defaults_used:
            warn("no saved settings, made with hyperMILL defaults: " + ", ".join(sorted(defaults_used)))
        for k, ops in sorted(MISSED.items()):
            warn("%s kept hyperMILL's value in %d job(s): %s" % (k, len(ops), ", ".join(sorted(set(ops)))))
        if apply_now:
            save_jobs(created)
            for jl in targets:
                for jb in jl.GetJobs():
                    log("   job:", jl.Name, "|", jb.Name, "|", jb.Status)
        if apply_now and want_hints and hint_queue:
            ui.info("Boundaries", "All toolpaths are created.\n\nNext: one picture per toolpath that needs a boundary or surface selection.")
            state = {"on": True}
            for jn, nm, jb in hint_queue:
                if not state.get("on", True):
                    break
                boundary_hint(ui, jn, nm, state, part, jb)
        n = len(created)
        if apply_now:
            msg = ("%d toolpath(s) created, no tools yet.\n\nNext:\n1 attach the pocket features to the milling toolpaths\n2 set the stock references\n"
                   "3 run part_wizard_2 (tools and cutting data)\n4 calculate\n\nDetails: part_wizard_1_log.txt") % n
        else:
            msg = "Dry run done, nothing created. The plan is in part_wizard_1_log.txt."
        if warnings:
            msg += "\n\nCheck by hand:\n" + "\n".join(warnings[:12])
        ui.info("Part wizard 1", msg)
    except Exception:
        log("FAILED:", traceback.format_exc())
        try:
            ui.info("Part wizard 1", "Failed. See part_wizard_1_log.txt.")
        except Exception:
            pass
    finally:
        if write_log:
            _write_log()

if __name__ == "__main__":
    run()
