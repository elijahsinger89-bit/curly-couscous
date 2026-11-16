# release_probe.py - hyperMILL 35 - release probe v1 (read-only)
# For the go-to-machine (release) script. Finds:
#   1. the posting call: every Post / Nc / Output / Simulation method on the om objects, with its signature (docstring)
#   2. how a job shows it has (or has not) been run through Simulation Center: every status-like value on every
#      compound job and job, then a summary of which values differ between them
# Changes nothing in the document: calls only methods named Get* / Is* / Has* / Count* with no arguments and reads
# plain attributes. Post, Simulate, Calc and every other write method are listed with their signature, never called.
# Before running: run Simulation Center on SOME compound jobs, not all, and note which ones (the summary compares them).
# Log: C:\Users\Public\Documents\OPEN MIND\release_probe_log.txt
import os
import datetime
import tempfile
import traceback
import collections

VERSION = "release_probe v1"
OUT_DIR = r"C:\Users\Public\Documents\OPEN MIND"
LOG_NAME = "release_probe_log.txt"
TITLE = "Release probe"
MAX_VALUE = 200
MAX_LINE = 2000
MAX_LINES = 30000
MAX_DOC = 700
READ_PREFIXES = ("Get", "Is", "Has", "Count")
NEVER = ("Set", "Create", "Delete", "Remove", "Add", "Run", "Calc", "Apply", "Export", "Import",
         "Rename", "Move", "Insert", "Update", "Post", "Simulate", "Generate", "Clear", "Reset",
         "Save", "Load", "Open", "Close", "Copy", "Paste", "Execute", "Start", "Stop", "Lock",
         "Clone", "Replace", "Link", "Write", "Sync", "Resort", "Optimize", "Enable", "Check", "Show")
# member names worth a signature (posting, NC output, simulation, status)
DOC_KW = ("post", "simul", "sim", "calc", "generat", "output", "export", "machin", "status", "state", "valid",
          "collis", "check", "verif", "time", "result", "error", "warn", "change", "modif", "dirty", "process", "file")
# member names read on every compound job and job (status-like)
STATUS_KW = ("stat", "simul", "sim", "calc", "valid", "collis", "check", "verif", "changed", "modif", "dirty", "error",
             "warn", "time", "date", "post", "output", "result", "locked", "frozen", "active", "suppress", "visible")
# job / compound cfg keys read on every job (upper case match)
CFG_KW = ("SIM", "STAT", "CALC", "COLL", "CHECK", "VALID", "POST", "NC", "TIME", "DATE", "CHANGE", "MODIF", "ERR", "WARN")
SKIP_STATUS = ("GetTool", "GetParent", "GetJobs", "GetCfgParameters", "GetCompoundJobs", "GetJobTreeNodes")

lines = []


def log(s=""):
    s = str(s)
    if len(s) > MAX_LINE:
        s = s[:MAX_LINE] + " ..."
    if len(lines) < MAX_LINES:
        lines.append(s)
    elif len(lines) == MAX_LINES:
        lines.append("(log cap reached)")


def out_dir():
    return OUT_DIR if os.path.isdir(OUT_DIR) else tempfile.gettempdir()


def short(v, n=MAX_VALUE):
    try:
        s = repr(v)
    except Exception as e:
        s = "<repr error %s>" % e
    return s if len(s) <= n else s[:n] + "..."


def public(obj):
    try:
        return [n for n in dir(obj) if not n.startswith("_")]
    except Exception as e:
        return []


CASE_KW = ("Nc", "NC")          # NC output, matched with case (lower-case "nc" is in too many words)


def kw(name, words):
    n = name.lower()
    return any(w in n for w in words) or any(w in name for w in CASE_KW)


def safe_read(obj, name):
    """Plain attribute: read. Method: called only when named Get/Is/Has/Count and it takes no arguments."""
    if name.startswith(NEVER):
        return "<skipped: not a read>"
    try:
        a = getattr(obj, name)
    except Exception as e:
        return "<getattr error %s>" % e
    if callable(a) and not isinstance(a, type):
        if not name.startswith(READ_PREFIXES):
            return "<method, not called>"
        try:
            return a()
        except TypeError as e:
            return "<needs arguments: %s>" % e
        except Exception as e:
            return "<call error %s>" % e
    return a


def is_note(v):
    return isinstance(v, str) and v.startswith("<")


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


def doc_of(owner, name):
    """Signature / docstring from the class attribute (never calls it)."""
    try:
        a = getattr(type(owner) if not isinstance(owner, type) and not _is_module(owner) else owner, name)
    except Exception:
        return ""
    if isinstance(a, property):
        return "property"
    d = getattr(a, "__doc__", None) or ""
    d = " | ".join(x.strip() for x in str(d).strip().splitlines() if x.strip())
    return d[:MAX_DOC]


def _is_module(x):
    return type(x).__name__ == "module"


def kind_of(owner, name):
    try:
        a = getattr(type(owner) if not isinstance(owner, type) and not _is_module(owner) else owner, name)
    except Exception:
        return "?"
    if isinstance(a, property):
        return "prop"
    if isinstance(a, type):
        return "class"
    return "def" if callable(a) else "attr"


# ---------------- 1. API: modules, classes, enums, signatures ----------------
def module_tree(om):
    import pkgutil
    import importlib
    log("")
    log("=== 1. om MODULES ===")
    mods = [om]
    names = set()
    try:
        for m in pkgutil.walk_packages(getattr(om, "__path__", []), om.__name__ + "."):
            names.add(m.name)
    except Exception as e:
        log("  walk_packages: %s" % e)
    for n in sorted(names):
        if n.count(".") > 3:
            continue
        try:
            mods.append(importlib.import_module(n))
        except Exception as e:
            log("  %s : not imported (%s)" % (n, e))
    seen = set()
    for m in mods:
        if m.__name__ in seen:
            continue
        seen.add(m.__name__)
        log("")
        log("module %s" % m.__name__)
        for n in public(m):
            try:
                a = getattr(m, n)
            except Exception:
                continue
            if _is_module(a):
                if a.__name__.startswith("om") and a.__name__ not in seen and a not in mods:
                    mods.append(a)
                continue
            if isinstance(a, type):
                members = getattr(a, "__members__", None)
                if hasattr(members, "keys") and len(members):
                    log("  enum %s: %s" % (n, ", ".join(list(members)[:60])))
                    continue
                hits = [x for x in public(a) if kw(x, DOC_KW)]
                log("  class %s  (%d members%s)" % (n, len(public(a)), ", %d posting/status" % len(hits) if hits else ""))
                for x in hits:
                    log("      %-5s %s  %s" % (kind_of(a, x), x, doc_of(a, x)))
            elif callable(a):
                log("  def %s  %s" % (n, doc_of(m, n) if kw(n, DOC_KW) else ""))


def object_dump(obj, label):
    """Every public name with its kind, the value of every readable one, and the signature of posting/status members."""
    log("")
    log("--- %s  class=%s ---" % (label, type(obj).__name__))
    if obj is None or is_note(obj):
        log("  %s" % short(obj)); return
    names = public(obj)
    for i in range(0, len(names), 8):
        log("  " + ", ".join(names[i:i + 8]))
    for n in names:
        k = kind_of(obj, n)
        if k == "def" and not n.startswith(READ_PREFIXES):
            if kw(n, DOC_KW):
                log("  def   %s  %s" % (n, doc_of(obj, n)))
            continue
        v = safe_read(obj, n)
        if iterable(v):
            items = as_list(v)
            log("  %-5s %s : %d item(s) %s" % (k, n, len(items), short([type(x).__name__ for x in items[:4]])))
        elif isinstance(v, dict):
            log("  %-5s %s : dict, %d keys" % (k, n, len(v)))
            for key in sorted(v, key=str)[:400]:
                log("        %s = %s" % (key, short(v[key])))
        else:
            log("  %-5s %s = %s%s" % (k, n, short(v), ("   " + doc_of(obj, n)) if k == "def" and kw(n, DOC_KW) else ""))


# ---------------- 2. status of every compound job and job ----------------
def status_of(obj, level, values):
    """Status-like values of one object into values[level.name] -> repr; returns the line text."""
    parts = []
    for n in public(obj):
        if n in SKIP_STATUS or not kw(n, STATUS_KW) or n.startswith(NEVER):
            continue
        if kind_of(obj, n) == "def" and not n.startswith(READ_PREFIXES):
            continue
        v = safe_read(obj, n)
        if iterable(v) or isinstance(v, dict):
            v = "<%d items>" % len(as_list(v)) if iterable(v) else "<dict %d>" % len(v)
        s = short(v, 80)
        values[level + "." + n].append(s)
        parts.append("%s=%s" % (n, s))
    cfg = safe_read(obj, "GetCfgParameters") if hasattr(obj, "GetCfgParameters") else None
    if isinstance(cfg, dict):
        for key in sorted(cfg, key=str):
            if any(w in str(key).upper() for w in CFG_KW):
                s = short(cfg[key], 80)
                values[level + ".cfg " + str(key)].append(s)
                parts.append("%s=%s" % (key, s))
    return " | ".join(parts)


def scan_status(joblists):
    values = collections.defaultdict(list)
    first_job = None
    log("")
    log("=== 3. STATUS OF EVERY COMPOUND JOB (C) AND JOB (J) ===")
    for jl in joblists:
        log("")
        log("joblist %r" % name_of(jl))
        log("  JL  %s" % status_of(jl, "JL", values))
        for ci, c in enumerate(as_list(safe_read(jl, "GetCompoundJobs")), 1):
            jobs = as_list(safe_read(c, "GetJobs"))
            if not jobs:
                log("  C%-3d %r  (note, empty)" % (ci, name_of(c)))
                continue
            log("  C%-3d %r  %s" % (ci, name_of(c), status_of(c, "C", values)))
            for j in jobs:
                if first_job is None:
                    first_job = j
                log("        J %r  %s" % (name_of(j), status_of(j, "J", values)))
    log("")
    log("=== 4. SUMMARY: values per member over all objects (DIFFERS = candidates for 'simulated / not simulated') ===")
    for key in sorted(values):
        cnt = collections.Counter(values[key])
        tag = "DIFFERS" if len(cnt) > 1 else "same   "
        log("  %s  %-40s %s" % (tag, key, ", ".join("%s x%d" % (v, c) for v, c in cnt.most_common(6))))
    return first_job


# ---------------- 5. files next to the document ----------------
def folder_listing(path):
    log("")
    log("=== 5. FILES NEXT TO THE DOCUMENT (simulation results may be saved there) ===")
    folder = os.path.dirname(str(path)) if path else ""
    if not folder or not os.path.isdir(folder):
        log("  folder not found: %r" % folder); return
    log("  %s" % folder)
    n = 0
    for root, dirs, files in os.walk(folder):
        depth = root[len(folder):].count(os.sep)
        if depth > 1:
            dirs[:] = []
            continue
        for f in sorted(files):
            p = os.path.join(root, f)
            try:
                st = os.stat(p)
                log("  %s  %10d  %s" % (datetime.datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d %H:%M"), st.st_size,
                                        os.path.relpath(p, folder)))
            except Exception as e:
                log("  %s  (%s)" % (f, e))
            n += 1
            if n >= 300:
                log("  (listing stopped at 300 files)"); return


# ---------------- main ----------------
def main():
    log("%s  %s" % (VERSION, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    import om
    module_tree(om)
    app = om.Application()
    doc = safe_read(app, "CurrentDocument")
    if doc is None or is_note(doc):
        log("No open document: %s" % short(doc))
        return "Open a document with compound jobs, then run the probe again."
    path = safe_read(doc, "FullPath")
    log("")
    log("document: %s" % short(path))
    model = safe_read(doc, "CamModel")
    jls = safe_read(model, "JobListSet")
    joblists = as_list(safe_read(jls, "GetJobLists"))
    log("")
    log("=== 2. OBJECTS: every member, readable values, signatures of posting / status members ===")
    object_dump(app, "Application")
    object_dump(doc, "Document")
    object_dump(model, "CamModel")
    object_dump(jls, "JobListSet")
    comp = None
    for jl in joblists[:1]:
        object_dump(jl, "JobList %r" % name_of(jl))
        for c in as_list(safe_read(jl, "GetCompoundJobs")):
            if as_list(safe_read(c, "GetJobs")):
                comp = c
                break
    if comp is not None:
        object_dump(comp, "CompoundJob %r" % name_of(comp))
    first_job = scan_status(joblists)
    if first_job is not None:
        log("")
        log("=== 6. FIRST JOB IN FULL ===")
        object_dump(first_job, "Job %r" % name_of(first_job))
    folder_listing(path if isinstance(path, str) else "")
    return "Release probe finished: %d joblist(s).\nSend the log:\n%s\nand say which compound jobs you ran through Simulation Center." % (
        len(joblists), os.path.join(out_dir(), LOG_NAME))


def run():
    try:
        msg = main()
    except Exception:
        log("")
        log("FAILED:")
        log(traceback.format_exc())
        msg = "Probe stopped with an error. Send the log:\n%s" % os.path.join(out_dir(), LOG_NAME)
    try:
        with open(os.path.join(out_dir(), LOG_NAME), "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
    except Exception as e:
        msg += "\nCould not write the log: %s" % e
    try:
        import om.cad.gui as g
        g.CleanOutput(g.UIOutputWindow.ALL)
        g.WriteToOutput("\n".join(lines[:400]), g.UIOutputWindow.ALL)
        g.ShowMessageBox(g.MessageBoxType.INFORMATION, TITLE, msg)
    except Exception:
        print(msg)


if __name__ == "__main__":
    run()
