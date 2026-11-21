# compound_probe.py - hyperMILL 35 - probe v2
# Read-only probe of compound jobs. Changes nothing in the document: it only
# calls attributes whose names start with Get / Is / Has / Count (with no
# arguments) and reads plain attributes. Write methods are listed, never called.
# v2: one line per tree node, a tool summary per compound job, the compound job
# class described in full; the per-job dumps of v1 (which filled the log after
# 122 jobs) are gone.
# Log: C:\Users\Public\Documents\OPEN MIND\compound_probe_log.txt

import datetime
import traceback

LOG = r"C:\Users\Public\Documents\OPEN MIND\compound_probe_log.txt"
MAX_VALUE = 300
MAX_LINES = 20000
READ_PREFIXES = ("Get", "Is", "Has", "Count")
NEVER = ("Set", "Create", "Delete", "Remove", "Add", "Run", "Calc", "Apply", "Export", "Import",
         "Rename", "Move", "Insert", "Update", "Post", "Simulate", "Generate", "Clear", "Reset",
         "Save", "Load", "Open", "Close", "Copy", "Paste", "Execute", "Start", "Stop", "Lock",
         "Clone", "Replace", "Link", "Write", "Sync", "Resort", "Optimize", "Enable", "Check")

lines = []


def log(s=""):
    if len(lines) < MAX_LINES:
        lines.append(str(s))
    elif len(lines) == MAX_LINES:
        lines.append("(log cap reached)")


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


def as_list(v):
    try:
        return list(v) if iterable(v) else []
    except Exception:
        return []


def name_of(obj):
    if obj is None:
        return "-"
    v = safe_read(obj, "Name")
    return v if isinstance(v, str) else "?"


def key_of(obj):
    """Stable identity for an hyperMILL object (Python wrappers differ per call)."""
    if obj is None:
        return None
    for a in ("UUID", "ID"):
        if hasattr(obj, a):
            v = safe_read(obj, a)
            if not (isinstance(v, str) and v.startswith("<")):
                return "%s:%s" % (a, v)
    return "NAME:" + name_of(obj)


def full_dump(obj, label):
    """Every public name, and the value of every readable one."""
    log("  [%s] class=%s" % (label, type(obj).__name__))
    names = public(obj)
    for i in range(0, len(names), 8):
        log("    " + ", ".join(names[i:i + 8]))
    for n in names:
        v = safe_read(obj, n)
        if isinstance(v, str) and v in ("<method, not called>", "<skipped: not a read>"):
            continue
        if iterable(v):
            items = as_list(v)
            log("    %s : %d item(s) %s" % (n, len(items), short([type(x).__name__ for x in items[:6]])))
            if items and n.startswith("Get"):
                for x in items[:6]:
                    log("        %s  name=%r" % (type(x).__name__, name_of(x)))
        elif isinstance(v, dict):
            log("    %s : dict, %d keys" % (n, len(v)))
            for k in sorted(v)[:200]:
                log("        %s = %s" % (k, short(v[k])))
        else:
            log("    %s = %s" % (n, short(v)))


def tool_of(job):
    t = safe_read(job, "GetTool") if hasattr(job, "GetTool") else None
    if t is None or isinstance(t, str):
        return None
    return t


def tool_id(t):
    if t is None:
        return "-"
    v = safe_read(t, "ID")
    return str(v) if not (isinstance(v, str) and v.startswith("<")) else str(safe_read(t, "Number"))


def export_check(tools):
    """tool.ID against the ncTool id in the tool's own export (what tool_load_mda uses)."""
    import os, re, tempfile
    import xml.etree.ElementTree as ET
    log("")
    log("=== tool.ID vs ncTool id from the export ===")
    for t in list(tools.values())[:8]:
        name = name_of(t)
        p = os.path.join(tempfile.gettempdir(), "compound_probe_%s.omtdx" % re.sub(r"[^A-Za-z0-9_.-]", "_", name)[:60])
        try:
            if not t.Export(p):
                log("  %s : export returned False" % name)
                continue
            n = ET.parse(p).getroot().find(".//ncTools/ncTool")
            nid = n.get("id") if n is not None else None
            log("  name=%r  tool.ID=%r  ncTool id=%r  %s" % (name, tool_id(t), nid, "SAME" if str(nid) == tool_id(t) else "DIFFERENT"))
        except Exception as e:
            log("  %s : export not read: %s" % (name, e))
        finally:
            try:
                os.remove(p)
            except Exception:
                pass


def probe_joblist(li, jl, tools):
    log("")
    log("=== JOBLIST %d: %r ===" % (li, name_of(jl)))
    log("  NcFileMode = %s" % short(safe_read(jl, "GetNcFileMode")))
    log("  MdfFileName = %s" % short(safe_read(jl, "MdfFileName")))
    comps = as_list(safe_read(jl, "GetCompoundJobs"))
    nodes = as_list(safe_read(jl, "GetJobTreeNodes"))
    jobs = as_list(safe_read(jl, "GetJobs"))
    log("  GetCompoundJobs: %d   GetJobTreeNodes: %d   GetJobs: %d" % (len(comps), len(nodes), len(jobs)))

    # full description of the compound job object (first two, plus the first empty one)
    log("")
    log("  --- compound job object ---")
    for c in comps[:2]:
        full_dump(c, "compound %r" % name_of(c))

    # jobs grouped by their compound (job.GetParent / job.CompoundJob)
    members = {}
    loose = []
    for j in jobs:
        parent = safe_read(j, "GetParent") if hasattr(j, "GetParent") else None
        if parent is None or isinstance(parent, str):
            parent = safe_read(j, "CompoundJob") if hasattr(j, "CompoundJob") else None
        if parent is None or isinstance(parent, str) or type(parent).__name__ != "CompoundJob":
            loose.append(j)
            continue
        members.setdefault(key_of(parent), []).append(j)
        t = tool_of(j)
        if t is not None:
            tools.setdefault(key_of(t), t)

    log("")
    log("  --- compound jobs in GetCompoundJobs() order: jobs, tool IDs ---")
    for ci, c in enumerate(comps, 1):
        m = members.get(key_of(c), [])
        ids = []
        for j in m:
            tid = tool_id(tool_of(j))
            if tid not in ids:
                ids.append(tid)
        flag = "EMPTY" if not m else ("MIXED TOOLS" if len(ids) > 1 else "one tool")
        log("  %3d  %-44r jobs=%-3d tools=%-28s %s  key=%s" % (ci, name_of(c), len(m), ",".join(ids), flag, key_of(c)))
    if loose:
        log("")
        log("  --- jobs in no compound job: %d ---" % len(loose))
        for j in loose[:50]:
            log("       %r  tool=%s" % (name_of(j), tool_id(tool_of(j))))

    log("")
    log("  --- GetJobTreeNodes() order (compare with the tree screenshot) ---")
    for ni, n in enumerate(nodes, 1):
        cls = type(n).__name__
        if cls == "CompoundJob":
            log("  %4d  C  %r" % (ni, name_of(n)))
        else:
            parent = safe_read(n, "GetParent") if hasattr(n, "GetParent") else None
            log("  %4d  J      %r  tool=%s  in=%r" % (ni, name_of(n), tool_id(tool_of(n)), name_of(parent) if parent is not None and not isinstance(parent, str) else "-"))


def main():
    log("compound_probe v2  %s" % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    import om
    doc = safe_read(om.Application(), "CurrentDocument")
    if doc is None or isinstance(doc, str):
        log("No open document: %s" % short(doc))
        return "Open a document with compound jobs, then run the probe again."
    log("document: %s" % short(safe_read(doc, "FullPath")))
    model = safe_read(doc, "CamModel")
    jls = safe_read(model, "JobListSet")
    joblists = as_list(safe_read(jls, "GetJobLists"))
    tools = {}
    for li, jl in enumerate(joblists, 1):
        probe_joblist(li, jl, tools)
    export_check(tools)
    return "Probe v2 finished: %d joblist(s). Send the log:\n%s" % (len(joblists), LOG)


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
