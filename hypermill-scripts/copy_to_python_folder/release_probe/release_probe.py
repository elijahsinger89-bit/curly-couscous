# release_probe.py - hyperMILL 35 - release probe v2 (read-only)
# For the go-to-machine (release) script. Finds:
#   1. the posting call: every Post / Nc / Output / Simulation member of the om objects, with its signature (docstring)
#   2. how a job shows it has (or has not) been run through Simulation Center: status values on every compound job
#      and job, then a summary of which values differ between them
# v2 (v1 froze hyperMILL):
#   - the log is written line by line: after a freeze its last line shows where it stopped
#   - no om submodule is imported: only modules hyperMILL has already loaded are listed
#   - application, document, CAM model, job list set and job list: names and signatures only, nothing read or called
#     (except what the rename and export scripts already use: CurrentDocument, FullPath, CamModel, JobListSet,
#     GetJobLists, GetCompoundJobs, GetJobs, GetNcFileMode)
#   - per compound job and job only: Is* / Has* flags, Get*Status / Get*State / Get*Simul*, properties with those
#     words, and GetCfgParameters keys about simulation / status. Time, result, NC values: listed, not read.
#   - a read slower than 0.5 s is not repeated; the scan stops after 60 compound jobs or 120 s
# Changes nothing. Post, Simulate, Calc and every other write method are listed with their signature, never called.
# Before running: run Simulation Center on SOME of the first 60 compound jobs, not all, and note which.
# Log: C:\Users\Public\Documents\OPEN MIND\release_probe_log.txt
import os
import sys
import time
import datetime
import tempfile
import traceback
import collections

VERSION = "release_probe v2"
OUT_DIR = r"C:\Users\Public\Documents\OPEN MIND"
LOG_NAME = "release_probe_log.txt"
TITLE = "Release probe"
MAX_VALUE = 200
MAX_LINE = 2000
MAX_LINES = 30000
MAX_DOC = 700
MAX_COMPOUNDS = 60
MAX_SECONDS = 120.0
SLOW = 0.5
NEVER = ("Set", "Create", "Delete", "Remove", "Add", "Run", "Calc", "Apply", "Export", "Import",
         "Rename", "Move", "Insert", "Update", "Post", "Simulate", "Generate", "Clear", "Reset",
         "Save", "Load", "Open", "Close", "Copy", "Paste", "Execute", "Start", "Stop", "Lock",
         "Clone", "Replace", "Link", "Write", "Sync", "Resort", "Optimize", "Enable", "Check", "Show")
# member names worth a signature (listed, never called)
DOC_KW = ("post", "simul", "calc", "generat", "output", "export", "machin", "status", "state", "valid",
          "collis", "check", "verif", "time", "result", "error", "warn", "change", "modif", "dirty", "process", "file")
CASE_KW = ("Nc", "NC")          # NC output, matched with case (lower-case "nc" is in too many words)
# member names read on compound jobs and jobs
READ_KW = ("status", "state", "simul")
# GetCfgParameters keys shown per job (upper case match)
CFG_KW = ("SIM", "STAT", "CALC", "COLL", "CHECK", "VALID", "CHANGE", "MODIF", "ERR", "WARN")
SKIP = ("GetTool", "GetParent", "GetJobs", "GetCfgParameters", "GetCompoundJobs", "GetJobTreeNodes")

lines = []
_log = {"f": None}
slow = {}
calls = {"n": 0}


def log(s=""):
    s = str(s)
    if len(s) > MAX_LINE:
        s = s[:MAX_LINE] + " ..."
    if len(lines) > MAX_LINES:
        return
    if len(lines) == MAX_LINES:
        s = "(log cap reached)"
    lines.append(s)
    f = _log["f"]
    if f is not None:
        try:
            f.write(s + "\n")
            f.flush()
        except Exception:
            pass


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
    except Exception:
        return []


def kw(name, words):
    n = name.lower()
    return any(w in n for w in words) or (words is DOC_KW and any(w in name for w in CASE_KW))


def is_module(x):
    return type(x).__name__ == "module"


def class_attr(owner, name):
    """The member as defined on the class (or module): never runs a property or a method."""
    src = owner if isinstance(owner, type) or is_module(owner) else type(owner)
    try:
        return True, getattr(src, name)
    except Exception:
        return False, None


def kind_of(owner, name):
    found, a = class_attr(owner, name)
    if not found:
        return "attr"                       # set on the instance: a plain value
    if isinstance(a, property) or type(a).__name__ in ("property", "getset_descriptor", "member_descriptor"):
        return "prop"
    if isinstance(a, type):
        return "class"
    return "def" if callable(a) else "attr"


def doc_of(owner, name):
    found, a = class_attr(owner, name)
    if not found:
        return ""
    d = getattr(a, "__doc__", None) or ""
    if isinstance(a, property) and not d:
        return ""
    d = " | ".join(x.strip() for x in str(d).strip().splitlines() if x.strip())
    return d[:MAX_DOC]


def timed(label, fn):
    """Calls fn once, unless this member was slow before. Returns (value, note)."""
    if label in slow:
        return None, "<slow before: not read>"
    t = time.perf_counter()
    try:
        v = fn()
        note = ""
    except TypeError as e:
        v, note = None, "<needs arguments: %s>" % e
    except Exception as e:
        v, note = None, "<error %s>" % e
    dt = time.perf_counter() - t
    calls["n"] += 1
    if dt > SLOW:
        slow[label] = dt
        log("  SLOW: %s took %.1f s, not read again" % (label, dt))
    return v, note


def names_only(obj, label):
    """Every public name with its kind, and the signature of posting / status members. Nothing is read or called."""
    log("")
    log("--- %s  class=%s  (names only) ---" % (label, type(obj).__name__))
    names = public(obj)
    for i in range(0, len(names), 8):
        log("  " + ", ".join(names[i:i + 8]))
    for n in names:
        if kw(n, DOC_KW):
            log("  %-5s %s  %s" % (kind_of(obj, n), n, doc_of(obj, n)))


# ---------------- 1. loaded om modules ----------------
def module_list():
    log("")
    log("=== 1. om MODULES ALREADY LOADED (nothing imported) ===")
    mods = sorted((k, m) for k, m in list(sys.modules.items()) if m is not None and (k == "om" or k.startswith("om.")))
    for name, m in mods:
        log("")
        log("module %s" % name)
        for n in public(m):
            found, a = class_attr(m, n)
            if not found or is_module(a):
                continue
            if isinstance(a, type):
                try:
                    members = getattr(a, "__members__", None)
                except Exception:
                    members = None
                if hasattr(members, "keys") and len(members):
                    log("  enum %s: %s" % (n, ", ".join(list(members)[:60])))
                    continue
                hits = [x for x in public(a) if kw(x, DOC_KW)]
                log("  class %s  (%d members%s)" % (n, len(public(a)), ", %d posting/status" % len(hits) if hits else ""))
                for x in hits:
                    log("      %-5s %s  %s" % (kind_of(a, x), x, doc_of(a, x)))
            elif callable(a):
                log("  def %s  %s" % (n, doc_of(m, n) if kw(n, DOC_KW) else ""))


# ---------------- 2./3. status of compound jobs and jobs ----------------
def prefixed(n, *prefixes):
    """IsX / HasX / GetX: the prefix followed by a capital (not Isolate, Hash, Getter)."""
    return any(n.startswith(p) and len(n) > len(p) and n[len(p)].isupper() for p in prefixes)


def readable(obj, n):
    if n in SKIP or n.startswith(NEVER):
        return False
    k = kind_of(obj, n)
    if k == "def":
        return prefixed(n, "Is", "Has") or (prefixed(n, "Get") and kw(n, READ_KW))
    if k in ("prop", "attr"):
        return kw(n, READ_KW) or prefixed(n, "Is", "Has")
    return False


def status_of(obj, level, values, verbose=False):
    """Status values of one object into values[level.member]; returns the line text."""
    parts = []
    cls = type(obj).__name__
    for n in public(obj):
        if not readable(obj, n):
            continue
        if verbose:
            log("    reading %s.%s" % (cls, n))
        k = kind_of(obj, n)
        v, note = timed("%s.%s" % (cls, n), (lambda n=n: getattr(obj, n)()) if k == "def" else (lambda n=n: getattr(obj, n)))
        s = note or short(v, 80)
        values[level + "." + n].append(s)
        parts.append("%s=%s" % (n, s))
    if hasattr(obj, "GetCfgParameters"):
        if verbose:
            log("    reading %s.GetCfgParameters" % cls)
        cfg, note = timed("%s.GetCfgParameters" % cls, lambda: obj.GetCfgParameters())
        if isinstance(cfg, dict):
            for key in sorted(cfg, key=str):
                if any(w in str(key).upper() for w in CFG_KW):
                    s = short(cfg[key], 80)
                    values[level + ".cfg " + str(key)].append(s)
                    parts.append("%s=%s" % (key, s))
    return " | ".join(parts)


def name_of(obj):
    try:
        v = obj.Name
        v = v() if callable(v) else v
        return v if isinstance(v, str) else str(v)
    except Exception:
        return "?"


def scan(joblists):
    values = collections.defaultdict(list)
    t0 = time.perf_counter()
    done = 0
    first = True
    log("")
    log("=== 3. STATUS OF COMPOUND JOBS (C) AND JOBS (J): first %d compound jobs ===" % MAX_COMPOUNDS)
    for jl in joblists:
        log("")
        log("joblist %r" % name_of(jl))
        for ci, c in enumerate(list(jl.GetCompoundJobs()), 1):
            jobs = list(c.GetJobs())
            if not jobs:
                log("  C%-3d %r  (note, empty)" % (ci, name_of(c)))
                continue
            if done >= MAX_COMPOUNDS:
                log("  (stopped after %d compound jobs)" % MAX_COMPOUNDS)
                return values
            if time.perf_counter() - t0 > MAX_SECONDS:
                log("  (stopped after %d s)" % int(MAX_SECONDS))
                return values
            if first:
                log("  C%-3d %r  (first compound job: each read is logged before it is made)" % (ci, name_of(c)))
            line = status_of(c, "C", values, verbose=first)
            log("  C%-3d %r  %s" % (ci, name_of(c), line))
            for j in jobs:
                if first:
                    log("        J %r  (first job: each read is logged before it is made)" % name_of(j))
                log("        J %r  %s" % (name_of(j), status_of(j, "J", values, verbose=first)))
                first = False
            done += 1
    return values


def summary(values):
    log("")
    log("=== 4. SUMMARY: values per member over all objects (DIFFERS = candidates for 'simulated / not simulated') ===")
    for key in sorted(values):
        cnt = collections.Counter(values[key])
        tag = "DIFFERS" if len(cnt) > 1 else "same   "
        log("  %s  %-40s %s" % (tag, key, ", ".join("%s x%d" % (v, c) for v, c in cnt.most_common(6))))
    if slow:
        log("")
        log("  slow members (read once): " + ", ".join("%s %.1f s" % (k, v) for k, v in sorted(slow.items())))


# ---------------- 5. files next to the document ----------------
def folder_listing(path):
    log("")
    log("=== 5. FILES NEXT TO THE DOCUMENT (simulation results may be saved there) ===")
    folder = os.path.dirname(str(path)) if path else ""
    if not folder or not os.path.isdir(folder):
        log("  folder not found: %r" % folder)
        return
    log("  %s" % folder)
    n = 0

    def entry(p, rel):
        try:
            st = os.stat(p)
            log("  %s  %10d  %s" % (datetime.datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d %H:%M"), st.st_size, rel))
        except Exception as e:
            log("  %s  (%s)" % (rel, e))

    try:
        items = sorted(os.listdir(folder))
    except Exception as e:
        log("  not listed: %s" % e)
        return
    for f in items:
        p = os.path.join(folder, f)
        if os.path.isdir(p):
            try:
                sub = sorted(os.listdir(p))
            except Exception as e:
                log("  %s\\  (not listed: %s)" % (f, e))
                continue
            log("  %s\\  %d entries" % (f, len(sub)))
            for s in sub[:20]:
                entry(os.path.join(p, s), os.path.join(f, s))
            n += min(len(sub), 20)
        else:
            entry(p, f)
            n += 1
        if n >= 300:
            log("  (listing stopped at 300 entries)")
            return


# ---------------- main ----------------
def main():
    log("%s  %s" % (VERSION, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    import om
    module_list()
    app = om.Application()
    doc = app.CurrentDocument
    if doc is None:
        log("No open document.")
        return "Open a document with compound jobs, then run the probe again."
    path = doc.FullPath
    path = path() if callable(path) else path
    log("")
    log("document: %s" % short(path))
    model = doc.CamModel
    jls = model.JobListSet
    joblists = list(jls.GetJobLists())
    log("")
    log("=== 2. OBJECTS: names and signatures (posting / NC / status members) ===")
    names_only(app, "Application")
    names_only(doc, "Document")
    names_only(model, "CamModel")
    names_only(jls, "JobListSet")
    if joblists:
        jl = joblists[0]
        names_only(jl, "JobList %r" % name_of(jl))
        if hasattr(jl, "GetNcFileMode"):
            v, note = timed("JobList.GetNcFileMode", lambda: jl.GetNcFileMode())
            log("  GetNcFileMode = %s" % (note or short(v)))
        comp = next((c for c in jl.GetCompoundJobs() if list(c.GetJobs())), None)
        if comp is not None:
            names_only(comp, "CompoundJob %r" % name_of(comp))
            names_only(list(comp.GetJobs())[0], "Job %r" % name_of(list(comp.GetJobs())[0]))
    values = scan(joblists)
    summary(values)
    log("")
    log("reads made: %d" % calls["n"])
    folder_listing(path if isinstance(path, str) else "")
    log("")
    log("finished")
    return "Release probe finished.\nSend the log:\n%s\nand say which compound jobs you ran through Simulation Center." % (
        os.path.join(out_dir(), LOG_NAME))


def run():
    lines[:] = []
    slow.clear()
    calls["n"] = 0
    logp = os.path.join(out_dir(), LOG_NAME)
    try:
        _log["f"] = open(logp, "w", encoding="utf-8")
    except Exception:
        _log["f"] = None
    try:
        msg = main()
    except Exception:
        log("")
        log("FAILED:")
        log(traceback.format_exc())
        msg = "Probe stopped with an error. Send the log:\n%s" % logp
    finally:
        try:
            _log["f"].close()
        except Exception:
            pass
        _log["f"] = None
    try:
        import om.cad.gui as g
        g.CleanOutput(g.UIOutputWindow.ALL)
        g.WriteToOutput("\n".join(lines[:400]), g.UIOutputWindow.ALL)
        g.ShowMessageBox(g.MessageBoxType.INFORMATION, TITLE, msg)
    except Exception:
        print(msg)


if __name__ == "__main__":
    run()
