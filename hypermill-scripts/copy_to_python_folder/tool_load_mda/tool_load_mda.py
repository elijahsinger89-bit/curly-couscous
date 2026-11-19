# tool_load_mda.py - the NC tools of the open document as one Sinumerik MDA program that creates every tool and sister on the
# control (paste the file into MDA and cycle start).
# Screens: 1 source: one joblist, all joblists, or every tool in the document
#          2 per tool (5 tools per screen): number of sisters (default 1, 0 = leave the tool out) and tool life in pieces
#            (blank or 0 = no tool life monitoring)
# Per tool and sister the program writes:
#   R999=GETT("<ID>",<sister>)        is that tool and sister already on the control? (-1 = no)
#   IF (R999<=0) ... ENDIF            only then:
#   R999=NEWT("<ID>",<sister>)        creates the tool; the control picks the internal T number and returns it in R999
#   $TC_TP8   = 2                       status: enabled
#   $TC_DP1   = Siemens tool type       from the hyperMILL tool type (SIEMENS_TYPE below)
#   $TC_DP3   = gage length             length 1
#   $TC_TPC4  = HD                      HD_MIN for tools smaller than HD_MIN, the tool diameter at or above it
#   $TC_TPC5  = HL                      gage length
#   tool life entered: $TC_TP9 = 2 (piece count monitoring), $TC_MOP13 = $TC_MOP4 = pieces
# Tool name on the control = the NC tool ID (Common > ID). A tool and sister already on the control are left exactly as
# they are (measured length, remaining life): NEWT would stop with alarm 14020 on them. Running the program twice is safe.
# The sisters and tool life entered are remembered per tool ID (tool_load_mda_last.json) and offered next time.
# go_to_machine uses this script (tool_data, ask_counts, program, write_program, load_last, save_last) after posting;
# there the tool life of tools whose B program counts with SETPIECE is marked "tool life (SETPIECE)".
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

def tool_data(tool):
    """ID, gage length and diameter (in UNIT), hyperMILL tool type and NC tool name, from the tool's own export."""
    p = os.path.join(tempfile.gettempdir(), "tool_load_mda_%s.omtdx" % re.sub(r"[^A-Za-z0-9_.-]", "_", str(val(tool.Name)))[:60])
    d = dict(id=str(val(tool.Number)), gage=None, dia=None, htype="", ncname=str(val(tool.Name)))
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


def load_last():
    """{tool ID: (sisters, life)} from the last runs."""
    try:
        with open(last_path(), encoding="utf-8") as f:
            return {k: (int(v[0]), int(v[1])) for k, v in json.load(f).items()}
    except Exception:
        return {}


def save_last(counts):
    d = load_last()
    d.update(counts)
    try:
        with open(last_path(), "w", encoding="utf-8") as f:
            json.dump({k: list(v) for k, v in d.items()}, f, indent=1)
    except Exception as e:
        log("last values not saved:", e)


def ask_counts(tools, defaults=None, need_life=None):
    """Sisters and tool life per tool, PER_SCREEN tools per screen. Returns {id: (sisters, life)} or None when cancelled.
    defaults: {id: (sisters, life)} shown instead of 1 / blank. need_life: IDs whose tool life field is labelled
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
        dlg = g.InputDialog("%s | tools %d-%d of %d" % (TITLE, start + 1, start + len(page), len(tools)))
        for t in page:
            ls, ll = labels(t)
            sis, life = defaults.get(t["id"], (1, 0))
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
                info("%s: sisters and tool life must be whole numbers. Tool left out." % t["id"])
                log("bad entry, left out:", t["id"], vals.get(ls), vals.get(ll))
                sis, life = 0, 0
            out[t["id"]] = (sis, life)
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
         "; a tool and sister already on the control (GETT finds it) is left as it is; running this twice is safe", ""]
    made = 0
    for t in tools:
        sis, life = counts.get(t["id"], (1, 0))
        for s in range(1, sis + 1):
            p += ['%s=GETT("%s",%d)' % (R_VAR, t["id"], s),
                  "IF (%s<=0)" % R_VAR,
                  '  %s=NEWT("%s",%d)' % (R_VAR, t["id"], s),
                  "  $TC_TP8[%s]=2" % R_VAR,
                  "  $TC_DP1[%s,1]=%d" % (R_VAR, siemens_type(t["htype"])),
                  "  $TC_DP3[%s,1]=%s" % (R_VAR, f(t["gage"])),
                  "  $TC_TPC4[%s]=%s" % (R_VAR, f(hd_of(t["dia"]))),
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
            log("tool:", d["id"], "|", d["ncname"], "|", d["htype"], "-> type", siemens_type(d["htype"]), "| gage", d["gage"], "| dia", d["dia"])
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
        if not made:
            info("Every tool was set to 0 sisters. No program written."); return
        path = write_program(text, folder, doc_name)
        left =[t["id"] for t in tools if counts.get(t["id"], (1, 0))[0] == 0]
        log("written:", path, "|", made, "tool entries |", len(tools), "tools |", "left out (0 sisters):", left)
        info("%d tool(s) with sisters written to:\n%s\n\nPaste it into MDA and cycle start.%s" % (
            made, path, ("\nLeft out (0 sisters): " + ", ".join(left)) if left else ""))
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
