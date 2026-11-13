# compound_probe.py - hyperMILL 35
# Read-only probe: logs how the Python API exposes compound jobs, job names,
# child jobs, job order and the tool on each job. Changes nothing in the
# document: it only calls attributes whose names start with Get / Is / Has /
# Count (and only with no arguments) and reads plain attributes. Each tool is
# exported to a temp file to read its ncTool id (the name NEWT uses); the
# temp file is deleted.
# Log: C:\Users\Public\Documents\OPEN MIND\compound_probe_log.txt

import datetime
import traceback

LOG = r"C:\Users\Public\Documents\OPEN MIND\compound_probe_log.txt"
MAX_VALUE = 300          # characters kept per value
MAX_LINES = 8000         # log cap
READ_PREFIXES = ("Get", "Is", "Has", "Count")
NEVER = ("Set", "Create", "Delete", "Remove", "Add", "Run", "Calc", "Apply", "Export", "Import",
         "Rename", "Move", "Insert", "Update", "Post", "Simulate", "Generate", "Clear", "Reset",
         "Save", "Load", "Open", "Close", "Copy", "Paste", "Execute", "Start", "Stop")
WATCH = ("compound", "group", "parent", "child", "sub", "chapter", "name", "comment", "nc",
         "post", "file", "tool", "type", "kind", "uuid", "index", "order", "job")

lines = []
seen_classes = set()


def log(s=""):
    if len(lines) < MAX_LINES:
        lines.append(str(s))


def short(v):
    try:
        s = repr(v)
    except Exception as e:
        s = "<repr error %s>" % e
    return s if len(s) <= MAX_VALUE else s[:MAX_VALUE] + "..."


def public(obj):
    try:
        return [n for n in dir(obj) if not n.startswith("_")]
    except Exception as e:
        return ["<dir error %s>" % e]


def safe_read(obj, name):
    """Read an attribute; call it only when it is a no-argument read method."""
    if name.startswith(NEVER):
        return "<skipped: not a read>"
    try:
        a = getattr(obj, name)
    except Exception as e:
        return "<getattr error %s>" % e
    if callable(a):
        if not name.startswith(READ_PREFIXES):
            return "<method, not called>"
        try:
            return a()
        except TypeError as e:
            return "<needs arguments: %s>" % e
        except Exception as e:
            return "<call error %s>" % e
    return a


def iterable(v):
    if isinstance(v, (str, bytes, dict)):
        return False
    try:
        iter(v)
        return True
    except Exception:
        return False


def describe_class(obj, label):
    cls = type(obj).__name__
    if cls in seen_classes:
        return
    seen_classes.add(cls)
    names = public(obj)
    log("  [class %s, first seen as %s] %d public names:" % (cls, label, len(names)))
    for i in range(0, len(names), 8):
        log("    " + ", ".join(names[i:i + 8]))


def describe(obj, indent, label):
    pad = " " * indent
    describe_class(obj, label)
    log("%s%s  class=%s" % (pad, label, type(obj).__name__))
    for n in public(obj):
        low = n.lower()
        if not any(w in low for w in WATCH):
            continue
        v = safe_read(obj, n)
        if isinstance(v, str) and v.startswith("<method, not called>"):
            log("%s  %s : method (not called)" % (pad, n))
            continue
        if iterable(v) and not isinstance(v, str):
            try:
                items = list(v)
            except Exception as e:
                log("%s  %s : <iterate error %s>" % (pad, n, e))
                continue
            log("%s  %s : %d item(s) %s" % (pad, n, len(items), short([type(x).__name__ for x in items[:5]])))
        else:
            log("%s  %s = %s" % (pad, n, short(v)))


def children_of(job):
    """Every no-argument read that returns a list of objects that look like jobs."""
    out = []
    for n in public(job):
        if not n.startswith(READ_PREFIXES) and n not in ("Jobs", "Children", "SubJobs"):
            continue
        low = n.lower()
        if not any(w in low for w in ("job", "child", "sub", "member", "item")):
            continue
        v = safe_read(job, n)
        if iterable(v) and not isinstance(v, str):
            try:
                items = list(v)
            except Exception:
                continue
            if items:
                out.append((n, items))
    return out


def name_of(obj):
    for n in ("Name", "GetName", "Title", "GetTitle", "Text", "GetText"):
        if hasattr(obj, n):
            v = safe_read(obj, n)
            if isinstance(v, str):
                return v
    return "?"


def tool_line(job):
    for n in ("GetTool", "Tool"):
        if hasattr(job, n):
            t = safe_read(job, n)
            if t is None or isinstance(t, str):
                return "tool: %s" % short(t)
            parts = []
            for f in ("Name", "Number", "UUID", "Id", "ID", "NcNumber", "Comment", "Type"):
                if hasattr(t, f):
                    parts.append("%s=%s" % (f, short(safe_read(t, f))))
            return "tool: " + ", ".join(parts)
    return "tool: <no GetTool>"


CFG_WATCH = ("NC", "FILE", "NAME", "POST", "COMP", "OUT", "PROG", "TOOL")


def cfg_lines(job, pad):
    """Job settings whose key mentions NC output, file, name, post or compound."""
    if not hasattr(job, "GetCfgParameters"):
        return
    cfg = safe_read(job, "GetCfgParameters")
    if not isinstance(cfg, dict):
        log("%s  GetCfgParameters -> %s" % (pad, short(cfg)))
        return
    keys = sorted(k for k in cfg if any(w in str(k).upper() for w in CFG_WATCH))
    log("%s  cfg: %d keys, %d about NC/file/name/post/compound/tool:" % (pad, len(cfg), len(keys)))
    for k in keys:
        log("%s    %s = %s" % (pad, k, short(cfg[k])))


def walk(job, indent, path, depth):
    pad = " " * indent
    if type(job).__name__ not in seen_classes:
        describe(job, indent, "child " + path)
    log("%s%s  name=%r  class=%s  %s" % (pad, path, name_of(job), type(job).__name__, tool_line(job)))
    cfg_lines(job, pad)
    if depth > 3:
        return
    for attr, items in children_of(job):
        log("%s  children via %s(): %d" % (pad, attr, len(items)))
        for i, c in enumerate(items, 1):
            walk(c, indent + 4, "%s.%d" % (path, i), depth + 1)


def tool_ids(jobs_seen):
    """For each distinct tool: the ncTool id / name from the tool's own export (the string
    tool_load_mda writes into NEWT). Exports to a temp file, reads it, deletes it."""
    import os, re, tempfile
    import xml.etree.ElementTree as ET
    log("")
    log("=== tool IDs from the tool export (what NEWT uses) ===")
    done = 0
    for uuid, t in jobs_seen.items():
        if done >= 40:
            log("  (stopped after 40 tools)")
            break
        done += 1
        name = str(safe_read(t, "Name"))
        p = os.path.join(tempfile.gettempdir(), "compound_probe_%s.omtdx" % re.sub(r"[^A-Za-z0-9_.-]", "_", name)[:60])
        try:
            if not t.Export(p):
                log("  %s : export returned False" % name)
                continue
            n = ET.parse(p).getroot().find(".//ncTools/ncTool")
            if n is None:
                log("  %s : no ncTool in the export" % name)
            else:
                log("  Name=%r Number=%r -> ncTool id=%r ncNumber=%r name=%r" % (
                    name, safe_read(t, "Number"), n.get("id"), n.get("ncNumber"), n.get("name")))
        except Exception as e:
            log("  %s : export not read: %s" % (name, e))
        finally:
            try:
                os.remove(p)
            except Exception:
                pass


def collect_tools(job, out, depth=0):
    if hasattr(job, "GetTool"):
        t = safe_read(job, "GetTool")
        if t is not None and not isinstance(t, str) and hasattr(t, "UUID"):
            out.setdefault(str(safe_read(t, "UUID")), t)
    if depth < 3:
        for _, items in children_of(job):
            for c in items:
                collect_tools(c, out, depth + 1)


def main():
    log("compound_probe  %s" % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    import om
    app = om.Application()
    doc = safe_read(app, "CurrentDocument")
    if doc is None or isinstance(doc, str):
        log("No open document: %s" % short(doc))
        return "Open a document with compound jobs, then run the probe again."
    log("document: %s" % short(safe_read(doc, "FullPath")))
    model = safe_read(doc, "CamModel")
    log("inch mode: %s" % short(safe_read(model, "IsInchMode")))
    jls = safe_read(model, "JobListSet")
    log("")
    log("=== JobListSet ===")
    describe(jls, 0, "JobListSet")
    joblists = safe_read(jls, "GetJobLists")
    if not iterable(joblists):
        log("GetJobLists returned %s" % short(joblists))
        return "No job lists found. Log written."
    joblists = list(joblists)
    njobs = 0
    tools = {}
    for li, jl in enumerate(joblists, 1):
        log("")
        log("=== JOBLIST %d: %r ===" % (li, name_of(jl)))
        describe(jl, 0, "JobList")
        jobs = safe_read(jl, "GetJobs")
        if not iterable(jobs):
            log("  GetJobs returned %s" % short(jobs))
            continue
        jobs = list(jobs)
        njobs += len(jobs)
        log("")
        log("  --- GetJobs() order (compare with the tree) ---")
        for ji, job in enumerate(jobs, 1):
            log("  %3d  %r  class=%s" % (ji, name_of(job), type(job).__name__))
        log("")
        log("  --- every job, its readable attributes, and children ---")
        for ji, job in enumerate(jobs, 1):
            log("")
            describe(job, 2, "job %d.%d" % (li, ji))
            walk(job, 2, "%d.%d" % (li, ji), 0)
            collect_tools(job, tools)
    tool_ids(tools)
    return "Probe finished: %d joblist(s), %d top-level job(s). Send the log:\n%s" % (len(joblists), njobs, LOG)


def finish(msg):
    try:
        with open(LOG, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
    except Exception as e:
        msg += "\nCould not write the log: %s" % e
    try:
        import om.cad.gui as g
        g.CleanOutput(g.UIOutputWindow.ALL)
        g.WriteToOutput("\n".join(lines[:400]), g.UIOutputWindow.ALL)
        g.ShowMessageBox(g.MessageBoxType.INFORMATION, "Compound job probe", msg)
    except Exception:
        print(msg)


try:
    result = main()
except Exception:
    log("")
    log("FAILED:")
    log(traceback.format_exc())
    result = "Probe stopped with an error. Send the log:\n%s" % LOG
finish(result)
