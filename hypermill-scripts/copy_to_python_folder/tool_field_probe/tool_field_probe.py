# tool_field_probe.py - hyperMILL 35. Run ONCE on a SCRATCH copy of a document. Send back:
#   C:\Users\Public\Documents\OPEN MIND\tool_field_probe_log.txt
#   C:\Users\Public\Documents\OPEN MIND\tool_field_probe_export.xml
# What it finds out (for tool numbering, the holder attacher and the job-end documents):
#   - the name of the Ordering code field, and the holder / extension blocks, in a tool's own export
#   - which tool fields Python can change in place (ID, Number, Name, Comment ...), and ToolSet.Rename
#   - whether a job can be given another tool (Job.SetToolByUUID / SetTool)
#   - whether openpyxl / docx are installed in hyperMILL's Python
# Screen: Tool (pick one WITH a holder, and an extension if you have one), Second tool (for the job tool-swap test),
#   Try writes (unticked = read only, nothing changes).
# Try writes changes the picked tool and one of its jobs, then puts every value back. The job may need recalculating
#   afterwards: use a scratch copy of the document.
# The log is written line by line; if hyperMILL freezes, close it and send the log anyway.
import os, re, sys, shutil, tempfile, traceback, datetime
import xml.etree.ElementTree as ET

OUT_DIR = r"C:\Users\Public\Documents\OPEN MIND"
TITLE = "Tool field probe"
LOGNAME = "tool_field_probe_log.txt"
EXPORTNAME = "tool_field_probe_export.xml"
FIELDS = ("Name", "ID", "Id", "Number", "NCNumber", "NcNumber", "Comment", "NCName", "NcName", "NCComment",
          "OrderingCode", "Description", "Manufacturer")          # tried in place with Try writes, when present
LOOK_RE = re.compile(r"order|article|edp|catalog|supplier|manufact|comment|name|descr|reach|gage|length|number|^id$", re.I)
lines = []
_f = [None]


def log(*a):
    s = " ".join(str(x) for x in a)
    lines.append(s)
    if _f[0]:
        try:
            _f[0].write(s + "\n"); _f[0].flush()
        except Exception:
            pass


def val(x):
    return x() if callable(x) else x


def text(x):
    try:
        return str(val(x) or "").strip()
    except Exception:
        return ""


def _gui():
    import om.cad.gui as g
    return g


def info(t):
    g = _gui()
    g.ShowMessageBox(g.MessageBoxType.INFORMATION, TITLE, t)


def pick(v, options):
    if isinstance(v, int) and not isinstance(v, bool):
        return v if 0 <= v < len(options) else 0
    return options.index(v) if v in options else 0


def helptext(obj):
    try:
        return " ".join((getattr(obj, "__doc__", "") or "").split())[:260]
    except Exception:
        return ""


def dump_members(title, obj, read_props=True):
    """Every public member: methods with their help line, properties with their value (each read logged first)."""
    try:
        names = sorted(n for n in dir(obj) if not n.startswith("_"))
    except Exception as e:
        log(title, ": dir() failed", e); return
    log("--- %s  class=%s  (%d members)" % (title, type(obj).__name__, len(names)))
    for n in names:
        try:
            a = getattr(type(obj), n, None)
        except Exception:
            a = None
        if callable(a) and not isinstance(a, property):
            log("  def  %-28s %s" % (n, helptext(a)))
            continue
        if not read_props:
            log("  prop %s" % n); continue
        log("  reading %s" % n)
        try:
            v = getattr(obj, n)
        except Exception as e:
            log("  prop %-28s -> error %s" % (n, str(e)[:120])); continue
        if callable(v):
            log("  def  %-28s %s" % (n, helptext(v)))
        else:
            log("  prop %-28s = %r" % (n, v if isinstance(v, (int, float, bool, str)) or v is None else type(v).__name__))


def python_facts():
    log("=== 1. PYTHON ===")
    log("version:", sys.version.replace("\n", " "))
    log("executable:", getattr(sys, "executable", ""))
    for m in ("openpyxl", "docx", "lxml", "xlsxwriter", "win32com"):
        try:
            __import__(m)
            log("  import %-10s yes" % m)
        except Exception as e:
            log("  import %-10s no (%s)" % (m, str(e)[:80]))


def module_names():
    log("=== 2. om.cam NAMES ABOUT TOOLS ===")
    try:
        import om.cam as cam
        hits = [n for n in dir(cam) if re.search(r"tool|holder|extension|assembl|component|coupling", n, re.I)]
        for n in sorted(hits):
            log("  %-32s %s" % (n, helptext(getattr(cam, n, None))))
        if not hits:
            log("  none")
    except Exception as e:
        log("  om.cam not read:", e)


def export_tool(tool):
    """The tool's own export: saved as tool_field_probe_export.xml; structure and the interesting params logged."""
    log("=== 5. THE TOOL'S EXPORT ===")
    p = os.path.join(tempfile.gettempdir(), "tool_field_probe.omtdx")
    try:
        ok = tool.Export(p)
        log("Export ->", ok)
    except Exception:
        log("Export FAILED:", traceback.format_exc()); return
    try:
        d = OUT_DIR if os.path.isdir(OUT_DIR) else tempfile.gettempdir()
        shutil.copy(p, os.path.join(d, EXPORTNAME))
        log("copy saved:", os.path.join(d, EXPORTNAME))
    except Exception as e:
        log("copy not saved:", e)
    try:
        root = ET.parse(p).getroot()
    except Exception as e:
        log("export not read:", e); return
    counts = {}

    def walk(el, path, depth):
        tag = path + "/" + el.tag
        counts[tag] = counts.get(tag, 0) + 1
        if counts[tag] > 3 or depth > 12:       # repeated blocks (tecsets, cutting profiles) only logged 3 times
            return
        attrs = {k: v[:60] for k, v in el.attrib.items()}
        ps = [(q.get("name"), q.get("value")) for q in el.findall("param")]
        hits = [(k, (v or "")[:80]) for k, v in ps if k and LOOK_RE.search(k)]
        log("%s%s %s%s" % ("  " * depth, el.tag, attrs if attrs else "", "  params: %d" % len(ps) if ps else ""))
        for k, v in hits:
            log("%s    %s = %r" % ("  " * depth, k, v))
        for c in el:
            if c.tag != "param":
                walk(c, tag, depth + 1)
    walk(root, "", 0)
    rep = sorted((k, v) for k, v in counts.items() if v > 3)
    if rep:
        log("repeated blocks (first 3 logged):", ", ".join("%s x%d" % (k.split("/")[-1], v) for k, v in rep))
    names = sorted(set(q.get("name") for q in root.iter("param") if q.get("name")))
    log("every param name in the export (%d):" % len(names))
    for i in range(0, len(names), 10):
        log("  " + ", ".join(names[i:i + 10]))


def try_writes(tool, ts, jobs_of_tool, second):
    log("=== 7. TRY WRITES (every value is put back) ===")
    numbers = []
    try:
        numbers = [int(val(t.Number)) for t in ts.GetTools()]
    except Exception:
        pass
    free = (max(numbers) if numbers else 0) + 7000
    for n in FIELDS:
        if not hasattr(tool, n):
            continue
        log("field %s:" % n)
        try:
            orig = getattr(tool, n)
        except Exception as e:
            log("  read failed:", e); continue
        if callable(orig):
            log("  is a method, not a field"); continue
        test = free if isinstance(orig, int) and not isinstance(orig, bool) else (str(orig) + "_P")
        try:
            setattr(tool, n, test)
        except Exception as e:
            log("  write refused: %s" % str(e)[:160]); continue
        try:
            back = getattr(tool, n)
            log("  wrote %r, reads back %r -> %s" % (test, back, "CHANGES" if back == test else "does not change"))
        except Exception as e:
            log("  read back failed:", e)
        try:
            setattr(tool, n, orig)
            log("  put back %r, reads %r" % (orig, getattr(tool, n)))
        except Exception as e:
            log("  PUT BACK FAILED (fix by hand: %s = %r): %s" % (n, orig, e))
    if hasattr(ts, "Rename"):
        nm = text(getattr(tool, "Name", ""))
        try:
            r = ts.Rename(tool.UUID, nm + "_P")
            log("ToolSet.Rename(uuid, name_P) -> %r; Name now %r" % (r, text(tool.Name)))
            ts.Rename(tool.UUID, nm)
            log("renamed back; Name now %r" % text(tool.Name))
        except Exception as e:
            log("ToolSet.Rename failed:", str(e)[:160])
    if not jobs_of_tool:
        log("job swap: the tool is not used in a job, not tried"); return
    if second is None:
        log("job swap: no second tool picked, not tried"); return
    j = jobs_of_tool[0]
    log("job swap on %r" % text(getattr(j, "Name", "")))
    for how in ("SetToolByUUID", "SetTool"):
        f = getattr(j, how, None)
        if not callable(f):
            log("  %s: not there" % how); continue
        arg = second.UUID if how == "SetToolByUUID" else second
        try:
            r = f(arg)
            now = j.GetTool()
            ok = now is not None and text(now.UUID) == text(second.UUID)
            log("  %s(second) -> %r; job tool now %r -> %s" % (how, r, text(getattr(now, "Name", "")), "SWAPS" if ok else "no change"))
            f(tool.UUID if how == "SetToolByUUID" else tool)
            back = j.GetTool()
            log("  put back: job tool now %r" % text(getattr(back, "Name", "")))
        except Exception as e:
            log("  %s failed: %s" % (how, str(e)[:200]))


def run():
    try:
        d = OUT_DIR if os.path.isdir(OUT_DIR) else tempfile.gettempdir()
        _f[0] = open(os.path.join(d, LOGNAME), "w", encoding="utf-8")
    except Exception:
        _f[0] = None
    try:
        import om
        log(TITLE, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        python_facts()
        module_names()
        doc = om.Application().CurrentDocument
        if doc is None:
            info("No document open."); return
        log("document:", text(doc.FullPath))
        model = doc.CamModel
        ts = model.ToolSet
        log("=== 3. TOOLSET ===")
        dump_members("ToolSet", ts, read_props=False)
        tools = list(ts.GetTools())
        if not tools:
            info("No tools in this document."); return
        labels = ["%s  |  %s" % (text(getattr(t, "ID", "")) or text(getattr(t, "Number", "")), text(t.Name)) for t in tools]
        g = _gui()
        dlg = g.InputDialog(TITLE)
        dlg.AddDropDown("Tool", labels, defaultIndex=0)
        dlg.AddDropDown("Second tool", ["(none)"] + labels, defaultIndex=0)
        dlg.AddBool("Try writes (scratch copy only)", False)
        ok, v = dlg.Show()
        if not ok:
            log("cancelled"); return
        tool = tools[pick(v.get("Tool"), labels)]
        k2 = pick(v.get("Second tool"), ["(none)"] + labels)
        second = tools[k2 - 1] if k2 > 0 else None
        writes = bool(v.get("Try writes (scratch copy only)"))
        log("tool:", labels[tools.index(tool)], "| second:", labels[tools.index(second)] if second else "(none)", "| try writes:", writes)
        log("=== 4. THE TOOL OBJECT ===")
        dump_members("Tool", tool)
        export_tool(tool)
        log("=== 6. JOBS USING THE TOOL ===")
        jobs = []
        for jl in model.JobListSet.GetJobLists():
            try:
                for j in jl.GetJobs():
                    t = j.GetTool()
                    if t is not None and text(t.UUID) == text(tool.UUID):
                        jobs.append(j)
            except Exception:
                log("joblist not read:", traceback.format_exc()[-200:])
        log("jobs using it:", len(jobs))
        if jobs:
            for n in ("GetTool", "SetTool", "SetToolByUUID", "RemoveTool", "ReplaceBy"):
                f = getattr(type(jobs[0]), n, None) or getattr(jobs[0], n, None)
                log("  Job.%-14s %s" % (n, ("there: " + helptext(f)) if f is not None else "not there"))
        if writes:
            try_writes(tool, ts, jobs, second)
        log("done")
        info("Done. Send %s and %s (in %s)." % (LOGNAME, EXPORTNAME, OUT_DIR))
    except Exception:
        log("FAILED:", traceback.format_exc())
        try:
            info("Failed. Send %s." % LOGNAME)
        except Exception:
            pass
    finally:
        if _f[0]:
            try:
                _f[0].close()
            except Exception:
                pass
            _f[0] = None


if __name__ == "__main__":
    run()
