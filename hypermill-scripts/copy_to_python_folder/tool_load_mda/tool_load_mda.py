# tool_load_mda.py - the NC tools of the open document as one Sinumerik MDA program that creates every tool and sister on the
# control (paste the file into MDA and cycle start).
# Screens: 1 source: one joblist, all joblists, or every tool in the document
#          2 per tool (5 tools per screen): sisters = EXTRA tools (default 0 = the tool only, 1 = two tools on the
#            control) and tool life in pieces (blank or 0 = no tool life monitoring)
#          3 turning tools only (5 per screen): tip direction, and cut direction for 500 / 510
# Per tool and sister the program writes:
#   R999=GETT("<ID>",<sister>)        is that tool and sister already on the control? (-1 = no)
#   IF (R999<=0) ... ENDIF            only then:
#   R999=NEWT("<ID>",<sister>)        creates the tool; the control picks the internal T number and returns it in R999
#   $TC_TP8   = 2                       status: enabled
#   $TC_DP1   = Siemens tool type       from the hyperMILL tool type (SIEMENS_TYPE below)
#   $TC_DP3   = gage length             length 1
#   turning tools (the NC tool has a turning cutting profile) instead:
#   $TC_DP1   = 500-550                 from the insert shape (TURN_TYPE below)
#   $TC_DP2   = tip direction 1-9       preset from hyperMILL's first cutting point (TIP_FROM_HM), chosen on screen 3
#   $TC_DP3   = setting length Z        length 1, radial
#   $TC_DP4   = setting length X        length 2, axial
#   $TC_DP11  = cut direction           500 / 510 only: 1 down, 2 up, 3 left, 4 right (arrows on the control). It must
#                                       point to the tip's corner (CUT_OK), else the screen asks again
#   $TC_TPC4  = HD                      HD_MIN for tools smaller than HD_MIN, the tool diameter at or above it
#   $TC_TPC5  = HL                      gage length
#   tool life entered: $TC_TP9 = 2 (piece count monitoring), $TC_MOP13 = $TC_MOP4 = pieces
# Tool name on the control = the NC tool ID (Common > ID). A tool and sister already on the control are left exactly as
# they are (measured length, remaining life): NEWT would stop with alarm 14020 on them. Running the program twice is safe.
# The sisters and tool life entered are remembered per tool ID (tool_load_mda_last.json) and offered next time; tip and
# cut direction too (tool_load_mda_turning.json). Files from before 21 Nov 2026 held the total number of tools: they are
# read as extras (total - 1) once and saved in the new form.
# go_to_machine uses this script (tool_data, ask_counts, fixed_counts, program, write_program, load_last, save_last) after
# posting; there the tool life of tools whose B program counts with SETPIECE is marked "tool life (SETPIECE)".
# Output: <document folder>\<document>_TOOL_LOAD.MPF (else C:\Users\Public\Documents\OPEN MIND\), opened in Notepad when done.
# Log: C:\Users\Public\Documents\OPEN MIND\tool_load_mda_log.txt
import os, re, json, tempfile, traceback, datetime
import xml.etree.ElementTree as ET

# ---------------- SETTINGS ----------------
OUT_DIR    = r"C:\Users\Public\Documents\OPEN MIND"
OPEN_FILE  = True          # open the program in Notepad when done
R_VAR      = "R999"        # R parameter that holds the T number NEWT returns
UNIT       = "inch"        # units written to the control: "inch" or "mm"
HD_MIN_IN  = 4.0           # HD: this value for every tool smaller than it, the tool diameter at or above it (inches)
PER_SCREEN = 5             # tools per sisters / tool life screen (2 rows each)
# hyperMILL tool type -> Siemens tool type ($TC_DP1). Types not listed: matched by the words in KEYWORDS, else DEFAULT_TYPE.
SIEMENS_TYPE = {
    "endMill": 120, "radiusMill": 120, "ballMill": 110, "lollipop": 110, "faceMill": 140, "facemill": 140,
    "drilTool": 200, "centerDrill": 220, "spotDrill": 220, "countersink": 230, "tapTool": 240, "threadMill": 145,
    "reamer": 250, "boringBar": 210, "chamferedcutter": 155, "Tslotcutter": 150, "woodruff": 150,
}
KEYWORDS = (("spot", 220), ("center", 220), ("sink", 230), ("tap", 240), ("thread", 145), ("ream", 250), ("bor", 210),
            ("drill", 200), ("dril", 200), ("face", 140), ("ball", 110), ("chamfer", 155), ("slot", 150), ("disc", 150))
DEFAULT_TYPE = 120
# Turning tools: insert shape (hyperMILL insert type) -> Siemens type. Matched by the words, else TURN_DEFAULT.
# rhombic: 500 roughing when the insert angle is ROUGH_ANGLE or more (80 deg), else 510 finishing.
TURN_TYPE = (("round", 550), ("circ", 550), ("button", 550), ("groov", 520), ("plung", 520), ("part", 530),
             ("thread", 540), ("square", 500), ("trian", 500), ("trigon", 500))
TURN_DEFAULT = 500
ROUGH_ANGLE = 75.0
# hyperMILL cutting point position -> Siemens tip direction ($TC_DP2). Not found: TIP_DEFAULT.
TIP_FROM_HM = {"topright": 1, "topleft": 2, "bottomleft": 3, "bottomright": 4, "right": 5, "top": 6, "left": 7,
               "bottom": 8, "center": 9, "centre": 9}
TIP_DEFAULT = 2
# Cut direction ($TC_DP11), only for these types (the control shows no arrow on the others)
CUT_TYPES = (500, 510)
CUT_OPTIONS = ("1 \u2193", "2 \u2191", "3 \u2190", "4 \u2192")      # down, up, left, right
# Tip 1 upper right, 2 upper left, 3 lower left, 4 lower right: the arrow must point to that corner (else the control
# shows a warning). Tips 5-9 are not checked.
CUT_OK = {1: (2, 4), 2: (2, 3), 3: (1, 3), 4: (1, 4)}
CUT_PRESET = {1: 2, 2: 3, 3: 3, 4: 1}
TURN_CUT = 3               # cut direction preset for tips 5-9
# ------------------------------------------

MM = 25.4
TITLE = "Tool load MDA"
lines = []

def log(*a):
    lines.append(" ".join(str(x) for x in a))

def val(x):
    return x() if callable(x) else x

def _f(x):
    try:
        return float(str(x).strip())
    except Exception:
        return None

def _gui():
    import om.cad.gui as g
    return g

def info(text):
    g = _gui()
    g.ShowMessageBox(g.MessageBoxType.INFORMATION, TITLE, text)

def choose(label, options):
    g = _gui()
    dlg = g.InputDialog(TITLE)
    dlg.AddDropDown(label, list(options), defaultIndex=0)
    ok, vals = dlg.Show()
    if not ok:
        return None
    v = vals.get(label)
    if isinstance(v, int) and not isinstance(v, bool):
        return v if 0 <= v < len(options) else 0
    return list(options).index(v) if v in options else 0

def siemens_type(htype):
    if htype in SIEMENS_TYPE:
        return SIEMENS_TYPE[htype]
    low = str(htype or "").lower()
    for word, code in KEYWORDS:
        if word in low:
            return code
    return DEFAULT_TYPE

def turn_type(insert, angle):
    low = str(insert or "").lower()
    if "rhomb" in low or "diamond" in low:
        return 500 if (angle is not None and angle >= ROUGH_ANGLE) else 510
    for word, code in TURN_TYPE:
        if word in low:
            return code
    return TURN_DEFAULT

def cut_ok(tip, cut):
    return cut in CUT_OK.get(tip, (1, 2, 3, 4))

def cut_preset(tip):
    return CUT_PRESET.get(tip, TURN_CUT)

def tip_of(pos):
    return TIP_FROM_HM.get(re.sub(r"[^a-z]", "", str(pos or "").lower()))

def _num(el, name):
    x = el.find("param[@name='%s']" % name) if el is not None else None
    return _f(x.get("value")) if x is not None else None

def _turning(n, t, root, d):
    """Turning data from the NC tool n and tool t: type, L1 / L2, hyperMILL cutting points."""
    prof = n.findall("cuttingProfiles/cuttingProfile") if n is not None else []
    turn = [c for c in prof if c.get("type") == "turning" and str(_num(c, "enabled")) != "0.0"]
    setups = n.findall("turningSetups/turningSetup") if n is not None else []
    if not (turn or (setups and not prof)):
        return
    d["turning"] = True
    ins = root.find(".//inserts/insert")
    d["insert"] = ins.get("type", "") if ins is not None else ""
    d["stype"] = turn_type(d["insert"], _num(ins, "insertAngle"))
    d["hm_pos"] = [str(_param(s, "cuttingEdgePosition")) for s in setups]
    d["tip"] = (tip_of(d["hm_pos"][0]) if d["hm_pos"] else None) or TIP_DEFAULT
    d["cut"] = cut_preset(d["tip"]) if d["stype"] in CUT_TYPES else None
    # Setting length Z = radial (L1), X = axial (L2): the NC tool's when set there, else the tool's
    for el in (n, t):
        z, x = _num(el, "settingLengthZ"), _num(el, "settingLengthX")
        if el is not None and (z or x):
            unit = _param(el, "lengthOfUnit") or "inch"
            d["l1"], d["l2"] = to_unit(z or 0.0, unit), to_unit(x or 0.0, unit)
            d["l_from"] = "NC tool" if el is n else "tool"
            break

def _param(el, name):
    x = el.find("param[@name='%s']" % name) if el is not None else None
    return x.get("value") if x is not None else None

def tool_data(tool):
    """ID, gage length and diameter (in UNIT), hyperMILL tool type and NC tool name, from the tool's own export.
    Turning tools also: turning=True, stype, l1 (radial), l2 (axial), tip, cut, hm_pos (hyperMILL cutting points)."""
    p = os.path.join(tempfile.gettempdir(), "tool_load_mda_%s.omtdx" % re.sub(r"[^A-Za-z0-9_.-]", "_", str(val(tool.Name)))[:60])
    d = dict(id=str(val(tool.Number)), gage=None, dia=None, htype="", ncname=str(val(tool.Name)), turning=False,
             stype=None, l1=None, l2=None, tip=None, cut=None, hm_pos=[], insert="", l_from="")
    try:
        if not tool.Export(p):
            log("export failed:", d["ncname"]); return d
        root = ET.parse(p).getroot()
        n = root.find(".//ncTools/ncTool")
        if n is not None:
            d["id"] = n.get("id") or n.get("ncNumber") or d["id"]
            d["ncname"] = n.get("name") or d["ncname"]
            nu = n.find("param[@name='lengthOfUnit']")
            g = n.find("param[@name='gageLength']")
            if g is not None and _f(g.get("value")) is not None:
                d["gage"] = to_unit(_f(g.get("value")), nu.get("value") if nu is not None else "inch")
        t = root.find(".//tools/tool")
        if t is not None:
            d["htype"] = t.get("type", "")
            tu = t.find("param[@name='lengthOfUnit']")
            dia = t.find("param[@name='toolDiameter']")
            if dia is not None and _f(dia.get("value")) is not None:
                d["dia"] = to_unit(_f(dia.get("value")), tu.get("value") if tu is not None else "inch")
        _turning(n, t, root, d)
        if d["stype"] is None:
            d["stype"] = siemens_type(d["htype"])
    except Exception as e:
        log("export not read:", d["ncname"], str(e)[:120])
    finally:
        try:
            os.remove(p)
        except Exception:
            pass
    return d

def to_unit(v, unit):
    """Value in the tool file's unit -> UNIT."""
    src_mm = str(unit).lower().startswith("m")
    if UNIT == "mm":
        return v if src_mm else v * MM
    return v / MM if src_mm else v

def hd_of(dia):
    hd_min = HD_MIN_IN if UNIT == "inch" else HD_MIN_IN * MM
    return hd_min if (dia is None or dia < hd_min - 1e-9) else dia

def last_path():
    return os.path.join(OUT_DIR if os.path.isdir(OUT_DIR) else tempfile.gettempdir(), "tool_load_mda_last.json")


FORMAT_KEY, FORMAT = "_sisters", "extras"     # marks a tool_load_mda_last.json that holds extras, not totals


def load_last():
    """{tool ID: (sisters, life)} from the last runs; sisters = extra tools. A file without the format mark holds totals
    (before 21 Nov 2026): read as total - 1."""
    try:
        with open(last_path(), encoding="utf-8") as f:
            raw = json.load(f)
    except Exception:
        return {}
    old = raw.get(FORMAT_KEY) != FORMAT
    out = {}
    for k, v in raw.items():
        if k == FORMAT_KEY:
            continue
        try:
            s, life = int(v[0]), int(v[1])
        except Exception:
            continue
        out[k] = (max(0, s - 1) if old else s, life)
    if old and out:
        log("tool_load_mda_last.json held totals: read as extras (total - 1)")
    return out


def save_last(counts):
    d = load_last()
    d.update(counts)
    try:
        with open(last_path(), "w", encoding="utf-8") as f:
            data = {FORMAT_KEY: FORMAT}
            data.update({k: list(v) for k, v in d.items()})
            json.dump(data, f, indent=1)
    except Exception as e:
        log("last values not saved:", e)


def fixed_counts(tools, table=None):
    """{id: (sisters, life)} without screens: from table {id: (sisters, life)} (the filled sister sheet), else 0 sisters
    and no tool life (validation: one of each tool)."""
    table = table or {}
    out = {}
    for t in tools:
        s, life = table.get(t["id"], (0, 0))
        out[t["id"]] = (max(0, int(s or 0)), max(0, int(life or 0)))
    return out


def turn_path():
    return os.path.join(os.path.dirname(last_path()), "tool_load_mda_turning.json")


def load_turn():
    """{tool ID: (tip, cut)} from the last runs."""
    try:
        with open(turn_path(), encoding="utf-8") as f:
            return {k: (int(v[0]), int(v[1])) for k, v in json.load(f).items()}
    except Exception:
        return {}


def save_turn(vals):
    d = load_turn()
    d.update(vals)
    try:
        with open(turn_path(), "w", encoding="utf-8") as f:
            json.dump({k: list(v) for k, v in d.items()}, f, indent=1)
    except Exception as e:
        log("turning values not saved:", e)


def ask_turning(tools):
    """Screen 3: tip direction (and cut direction for 500 / 510) per turning tool, PER_SCREEN per screen. Preset: last
    run when the pair is allowed, else hyperMILL. A cut direction that does not point to the tip: message, same screen
    again. Sets t["tip"], t["cut"]. Returns False when cancelled."""
    turn = [t for t in tools if t.get("turning")]
    if not turn:
        return True
    g = _gui()
    last = load_turn()
    tips = [str(i) for i in range(1, 10)]
    cuts = list(CUT_OPTIONS)
    for t in turn:
        tip, cut = last.get(t["id"], (t["tip"], t.get("cut") or 0))
        if 1 <= tip <= 9:
            t["tip"] = tip
        if t.get("cut") is not None:
            t["cut"] = cut if (1 <= cut <= len(cuts) and cut_ok(t["tip"], cut)) else cut_preset(t["tip"])
    allowed = "arrow to the tip: " + "  ".join("%d %s" % (k, "".join(cuts[c - 1][-1] for c in v)) for k, v in sorted(CUT_OK.items()))

    def labels(t):
        hm = t["hm_pos"][0] if t["hm_pos"] else "none"
        return "%s  tip direction (hyperMILL %s)" % (t["id"], hm), "%s  cut direction" % t["id"]

    def pick(v, opts, cur):
        if isinstance(v, int) and not isinstance(v, bool):
            return v + 1 if 0 <= v < len(opts) else cur
        return opts.index(v) + 1 if v in opts else cur

    for start in range(0, len(turn), PER_SCREEN):
        page = turn[start:start + PER_SCREEN]
        while True:
            dlg = g.InputDialog("%s | turning tools %d-%d of %d | %s" % (TITLE, start + 1, start + len(page), len(turn), allowed))
            for t in page:
                lt, lc = labels(t)
                dlg.AddDropDown(lt, tips, defaultIndex=t["tip"] - 1)
                if t.get("cut") is not None:
                    dlg.AddDropDown(lc, cuts, defaultIndex=t["cut"] - 1)
            ok, vals = dlg.Show()
            if not ok:
                return False
            bad = []
            for t in page:
                lt, lc = labels(t)
                t["tip"] = pick(vals.get(lt), tips, t["tip"])
                if t.get("cut") is not None:
                    t["cut"] = pick(vals.get(lc), cuts, t["cut"])
                    if not cut_ok(t["tip"], t["cut"]):
                        bad.append("%s: tip %d takes cut %s" % (t["id"], t["tip"], " or ".join(cuts[c - 1] for c in CUT_OK[t["tip"]])))
            if not bad:
                break
            log("cut direction does not point to the tip, asked again:", bad)
            info("The cut direction must point to the tip, else the control shows a warning:\n" + "\n".join(bad))
    save_turn({t["id"]: (t["tip"], t.get("cut") or 0) for t in turn})
    return True


def ask_counts(tools, defaults=None, need_life=None):
    """Sisters (extra tools: 0 = the tool only) and tool life per tool, PER_SCREEN tools per screen, then the turning
    tools' screen (ask_turning). Returns {id: (sisters, life)} or None when cancelled.
    defaults: {id: (sisters, life)} shown instead of 0 / blank. need_life: IDs whose tool life field is labelled
    "tool life (SETPIECE)" (their B program counts with SETPIECE, which needs tool life monitoring on the control)."""
    g = _gui()
    defaults = defaults or {}
    need_life = need_life or set()
    out = {}

    def labels(t):
        tag = "%s  D%.4f" % (t["id"], t["dia"]) if t["dia"] else t["id"]
        return "%s  sisters" % tag, "%s  tool life%s" % (tag, " (SETPIECE)" if t["id"] in need_life else "")

    for start in range(0, len(tools), PER_SCREEN):
        page = tools[start:start + PER_SCREEN]
        dlg = g.InputDialog("%s | tools %d-%d of %d | sisters = extra tools (0 = this tool only, 1 = two)" % (
            TITLE, start + 1, start + len(page), len(tools)))
        for t in page:
            ls, ll = labels(t)
            sis, life = defaults.get(t["id"], (0, 0))
            dlg.AddText(ls, defaultValue=str(sis))
            dlg.AddText(ll, defaultValue=str(life) if life else "")
        ok, vals = dlg.Show()
        if not ok:
            return None
        for t in page:
            ls, ll = labels(t)
            def num(label):
                s = str(vals.get(label) or "").strip()
                try:
                    return max(0, int(float(s))) if s else 0
                except Exception:
                    return None
            sis = num(ls)
            life = num(ll)
            if sis is None or life is None:
                info("%s: sisters and tool life must be whole numbers. Written with 0 sisters and no tool life." % t["id"])
                log("bad entry, 0 sisters / no tool life:", t["id"], vals.get(ls), vals.get(ll))
                sis, life = 0, 0
            out[t["id"]] = (sis, life)
    if not ask_turning(tools):
        return None
    return out


def write_program(text, folder, doc_name):
    """<DOCUMENT>_TOOL_LOAD.MPF in folder (else OUT_DIR, else the temp folder). Returns the path."""
    fname = re.sub(r"[^A-Za-z0-9_]", "_", doc_name).upper()[:30] + "_TOOL_LOAD.MPF"
    for d in (folder, OUT_DIR, tempfile.gettempdir()):
        if not d:
            continue
        path = os.path.join(d, fname)
        try:
            with open(path, "w", newline="\n", encoding="ascii", errors="replace") as fh:
                fh.write(text)
            return path
        except Exception:
            continue
    raise IOError("tool load program not written: no writable folder")

def program(tools, counts, doc_name, source):
    f = lambda v: "%.4f" % v
    p = ["; TOOL LOAD - %s - %s - %s" % (doc_name, source, datetime.datetime.now().strftime("%Y-%m-%d %H:%M")),
         "; units %s | name = NC tool ID | HL = gage length | HD = %s below %s, else diameter" % (UNIT, f(hd_of(None)), f(hd_of(None))),
         "; a tool and sister already on the control (GETT finds it) is left as it is; running this twice is safe"]
    if any(t.get("turning") for t in tools):
        p.append("; turning tools: L1 = setting length Z (radial), L2 = setting length X (axial), DP2 tip direction, DP11 cut direction")
    p.append("")
    made = 0
    for t in tools:
        sis, life = counts.get(t["id"], (0, 0))
        for s in range(1, sis + 2):            # the tool (DUPLO 1) and its extra sisters (DUPLO 2 ...)
            p += ['%s=GETT("%s",%d)' % (R_VAR, t["id"], s),
                  "IF (%s<=0)" % R_VAR,
                  '  %s=NEWT("%s",%d)' % (R_VAR, t["id"], s),
                  "  $TC_TP8[%s]=2" % R_VAR,
                  "  $TC_DP1[%s,1]=%d" % (R_VAR, t.get("stype") or siemens_type(t["htype"]))]
            if t.get("turning"):
                p += ["  $TC_DP2[%s,1]=%d" % (R_VAR, t["tip"]),
                      "  $TC_DP3[%s,1]=%s" % (R_VAR, f(t["l1"] or 0.0)),
                      "  $TC_DP4[%s,1]=%s" % (R_VAR, f(t["l2"] or 0.0))]
                if t.get("cut"):
                    p += ["  $TC_DP11[%s,1]=%d" % (R_VAR, t["cut"])]
            else:
                p += ["  $TC_DP3[%s,1]=%s" % (R_VAR, f(t["gage"]))]
            p += ["  $TC_TPC4[%s]=%s" % (R_VAR, f(hd_of(t["dia"]))),
                  "  $TC_TPC5[%s]=%s" % (R_VAR, f(t["gage"]))]
            if life:
                p += ["  $TC_TP9[%s]=2" % R_VAR, "  $TC_MOP13[%s,1]=%d" % (R_VAR, life), "  $TC_MOP4[%s,1]=%d" % (R_VAR, life)]
            p += ["ENDIF", ""]
            made += 1
    p.append("M30")
    return "\n".join(p) + "\n", made

def run():
    path = ""
    try:
        import om
        doc = om.Application().CurrentDocument
        if doc is None:
            info("No document open."); return
        model = doc.CamModel
        lists = list(model.JobListSet.GetJobLists())
        names = [str(val(jl.Name)) for jl in lists]
        opts = names + (["All joblists"] if lists else []) + ["All tools in the document"]
        k = choose("Tools from", opts)
        if k is None:
            log("cancelled"); return
        source = opts[k]
        picked = []
        if source == "All tools in the document":
            picked = list(model.ToolSet.GetTools())
        else:
            seen = set()
            for jl in (lists if source == "All joblists" else [lists[k]]):
                for j in jl.GetJobs():
                    try:
                        t = j.GetTool()
                    except Exception:
                        t = None
                    if t is None:
                        continue
                    u = str(val(t.UUID))
                    if u not in seen:
                        seen.add(u); picked.append(t)
        log("source:", source, "|", len(picked), "tools")
        if not picked:
            info("No tools in %s." % source); return
        tools, ids = [], set()
        for t in picked:
            d = tool_data(t)
            if d["id"] in ids:
                log("duplicate ID left out:", d["id"], d["ncname"]); continue
            if d["gage"] is None:
                log("no gage length, left out:", d["id"], d["ncname"]); continue
            ids.add(d["id"]); tools.append(d)
            log("tool:", d["id"], "|", d["ncname"], "|", d["htype"], "-> type", d["stype"], "| gage", d["gage"], "| dia", d["dia"])
            if d["turning"]:
                log("  turning:", d["insert"], "| L1", d["l1"], "L2", d["l2"], "from", d["l_from"] or "nowhere (written as 0)",
                    "| hyperMILL cutting points", d["hm_pos"], "-> tip", d["tip"], "| cut", d["cut"])
        if not tools:
            info("None of the tools could be read. See tool_load_mda_log.txt."); return
        tools.sort(key=lambda d: (_f(d["id"]) is None, _f(d["id"]) or 0, d["id"]))
        counts = ask_counts(tools, load_last())
        if counts is None:
            log("cancelled at sisters / tool life"); return
        save_last(counts)
        doc_name, folder = "document", OUT_DIR
        try:
            fp = str(val(doc.FullPath) or "")
            if fp:
                folder = os.path.dirname(fp) or OUT_DIR
                doc_name = os.path.splitext(os.path.basename(fp))[0]
        except Exception:
            pass
        text, made = program(tools, counts, doc_name, source)
        path = write_program(text, folder, doc_name)
        extra = sum(counts.get(t["id"], (0, 0))[0] for t in tools)
        log("written:", path, "|", made, "tool entries |", len(tools), "tools |", extra, "extra sisters")
        info("%d tools and %d extra sister%s (%d entries) written to:\n%s\n\nPaste it into MDA and cycle start." % (
            len(tools), extra, "" if extra == 1 else "s", made, path))
        if OPEN_FILE:
            try:
                import subprocess
                subprocess.Popen(["notepad.exe", path])
            except Exception:
                pass
    except Exception:
        log("FAILED:", traceback.format_exc())
        try:
            info("Failed. See tool_load_mda_log.txt.")
        except Exception:
            pass
    finally:
        for p in (os.path.join(OUT_DIR, "tool_load_mda_log.txt"), os.path.join(tempfile.gettempdir(), "tool_load_mda_log.txt")):
            try:
                with open(p, "w", encoding="utf-8") as fh:
                    fh.write("\n".join(lines))
                break
            except Exception:
                continue

if __name__ == "__main__":
    run()
