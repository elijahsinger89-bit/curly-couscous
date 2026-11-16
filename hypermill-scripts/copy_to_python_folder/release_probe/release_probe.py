# release_probe.py - hyperMILL 35 - release probe v3 (read-only)
# For the go-to-machine (release) script.
# v2 found: JobListSet.CalculateNC / Run / RunAll, JobList.GenerateNCListFile, GetGenerateAndReleaseNcInfo,
#   CheckNcStatus / HasNcStatus, Job.Status (JobStatus), Job.POFStatus (POFStatus), Job.PofFileName, and that Simulation
#   Center writes POF\ files and VNC\<joblist>.nclist / .settings. hyperMILL's API has no help text (no signatures).
# v3 reads:
#   1. the arguments of every method of JobListSet, JobList, CompoundJob and Job WITHOUT running it: each built-in
#      hyperMILL method is called with one made-up keyword argument; hyperMILL rejects the call before running anything
#      and lists the arguments it accepts. Anything that is not a built-in hyperMILL method is skipped, and so is every
#      method that changes the document (Set, Create, Delete, Remove, Reset ...): only the name is listed.
#   2. every compound job (no 60 cap): Status, POFStatus, PofFileName of each job, HasNcStatus of the compound job
#   3. the text of the VNC\ files and the newest files in POF\ and NC\
# Changes nothing. A read slower than 2 s is not repeated; the scan stops after 300 s.
# Log (written line by line): C:\Users\Public\Documents\OPEN MIND\release_probe_log.txt
import os
import time
import types
import datetime
import tempfile
import traceback
import collections

VERSION = "release_probe v3"
OUT_DIR = r"C:\Users\Public\Documents\OPEN MIND"
LOG_NAME = "release_probe_log.txt"
TITLE = "Release probe"
MAX_LINE = 2000
MAX_LINES = 40000
MAX_SECONDS = 300.0
SLOW = 2.0          # seconds: a read slower than this is not repeated on other jobs
SIG_KW = "release_probe_signature_only_9f3c"      # no hyperMILL method has an argument with this name
# methods that change the document: their arguments are not asked (not needed for posting or status)
SIG_SKIP = ("Set", "Create", "Delete", "Remove", "Clear", "Reset", "Move", "Rename", "Insert", "Lock", "Replace", "Write",
            "Import", "Export", "Clone", "Link", "Enable", "Optimize", "Sync", "Resort", "Update", "Apply", "Copy", "Paste",
            "Override", "Change", "Add")
MAX_TEXT_FILE = 65536
JOB_READS = ("Status", "POFStatus", "PofFileName")

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


def short(v, n=120):
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


def name_of(obj):
    try:
        v = obj.Name
        v = v() if callable(v) else v
        return v if isinstance(v, str) else str(v)
    except Exception:
        return "?"


def timed(label, fn):
    """Calls fn once, unless this member was slow before. Returns (value, note)."""
    if label in slow:
        return None, "<slow before: not read>"
    t = time.perf_counter()
    try:
        v, note = fn(), ""
    except Exception as e:
        v, note = None, "<error %s>" % str(e).splitlines()[0][:150]
    dt = time.perf_counter() - t
    calls["n"] += 1
    if dt > SLOW:
        slow[label] = dt
        log("  SLOW: %s took %.1f s, not read again" % (label, dt))
    return v, note


# ---------------- 1. signatures without running anything ----------------
def is_native(raw):
    """A built-in (compiled) hyperMILL method: pybind11 'instancemethod' around a builtin function. These reject an
    unknown keyword argument before running. Plain Python functions are never called."""
    f = getattr(raw, "__func__", raw)
    return isinstance(f, types.BuiltinFunctionType) and type(raw).__name__ in ("instancemethod", "builtin_function_or_method")


def overloads(text):
    """The 'following argument types are supported' list from a pybind11 TypeError."""
    out, on = [], False
    for ln in str(text).splitlines():
        s = ln.strip()
        if "argument types are supported" in s:
            on = True
            continue
        if on:
            if not s or s.startswith("Invoked with"):
                break
            out.append(s)
    return out


def signatures(obj, label):
    log("")
    log("--- %s  class=%s ---" % (label, type(obj).__name__))
    cls = type(obj)
    for n in public(obj):
        try:
            raw = getattr(cls, n)
        except Exception:
            continue                                   # instance value, not a method
        if isinstance(raw, property) or type(raw).__name__ in ("property", "getset_descriptor", "member_descriptor"):
            log("  prop  %s" % n)
            continue
        if not callable(raw) or isinstance(raw, type):
            continue
        if n.startswith(SIG_SKIP):
            log("  def   %s  (changes the document: arguments not asked)" % n)
            continue
        if not is_native(raw):
            log("  def   %s  (not a built-in method: skipped)" % n)
            continue
        try:
            getattr(obj, n)(**{SIG_KW: None})
            log("  def   %s  !! accepted the made-up argument (it may have run)" % n)
        except TypeError as e:
            ov = overloads(e)
            if ov:
                for o in ov:
                    log("  def   %s%s" % (n, o[o.index("("):] if "(" in o else " " + o))
            else:
                log("  def   %s  <%s>" % (n, str(e).splitlines()[0][:200]))
        except Exception as e:
            log("  def   %s  <%s: %s>" % (n, type(e).__name__, str(e).splitlines()[0][:200] if str(e) else ""))


# ---------------- 2. status of every compound job ----------------
def enum_name(v):
    s = str(v)
    return s.split(".")[-1].split(":")[0].strip("<> ") if "." in s else s


def scan(joblists):
    t0 = time.perf_counter()
    tot = collections.Counter()
    first = True
    log("")
    log("=== 2. EVERY COMPOUND JOB: HasNcStatus | per job: Status, POFStatus, PofFileName ===")
    for jl in joblists:
        log("")
        log("joblist %r" % name_of(jl))
        for ci, c in enumerate(list(jl.GetCompoundJobs()), 1):
            if time.perf_counter() - t0 > MAX_SECONDS:
                log("  (stopped after %d s)" % int(MAX_SECONDS))
                return tot
            jobs = list(c.GetJobs())
            if not jobs:
                log("  C%-3d %r  (note, empty)" % (ci, name_of(c)))
                continue
            if first:
                log("    reading CompoundJob.HasNcStatus")
            hn, note = timed("CompoundJob.HasNcStatus", lambda: c.HasNcStatus())
            log("  C%-3d %r  HasNcStatus=%s" % (ci, name_of(c), note or hn))
            for j in jobs:
                vals = []
                for n in JOB_READS:
                    if first:
                        log("    reading Job.%s" % n)
                    v, note = timed("Job." + n, lambda n=n: getattr(j, n))
                    v = note or (enum_name(v) if n != "PofFileName" else str(v).replace("\\", "/").split("/")[-1])
                    vals.append("%s=%s" % (n, v))
                    if n != "PofFileName":
                        tot["%s=%s" % (n, v)] += 1
                first = False
                log("        J %-50r %s" % (name_of(j), "  ".join(vals)))
    return tot


# ---------------- 3. files ----------------
def newest(folder, k=15):
    try:
        es = [(e.stat().st_mtime, e.stat().st_size, e.name) for e in os.scandir(folder) if e.is_file()]
    except Exception as e:
        log("  not listed: %s" % e)
        return
    es.sort(reverse=True)
    log("  %s\\  %d files, newest %d:" % (os.path.basename(folder), len(es), min(k, len(es))))
    for t, s, n in es[:k]:
        log("    %s  %10d  %s" % (datetime.datetime.fromtimestamp(t).strftime("%Y-%m-%d %H:%M:%S"), s, n))


def files(path):
    log("")
    log("=== 3. FILES ===")
    folder = os.path.dirname(str(path)) if path else ""
    if not folder or not os.path.isdir(folder):
        log("  folder not found: %r" % folder)
        return
    log("  %s" % folder)
    vnc = os.path.join(folder, "VNC")
    if os.path.isdir(vnc):
        for n in sorted(os.listdir(vnc)):
            p = os.path.join(vnc, n)
            if not os.path.isfile(p):
                continue
            st = os.stat(p)
            log("")
            log("  VNC\\%s  %d bytes  %s" % (n, st.st_size, datetime.datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d %H:%M:%S")))
            if st.st_size <= MAX_TEXT_FILE:
                try:
                    with open(p, "rb") as f:
                        data = f.read()
                    for enc in ("utf-8-sig", "utf-16", "cp1252"):
                        try:
                            txt = data.decode(enc)
                            break
                        except Exception:
                            txt = None
                    for ln in (txt or repr(data[:2000])).splitlines():
                        log("    | " + ln)
                except Exception as e:
                    log("    not read: %s" % e)
    else:
        log("  no VNC folder")
    for sub in ("POF", "NC"):
        p = os.path.join(folder, sub)
        if os.path.isdir(p):
            log("")
            newest(p)


# ---------------- main ----------------
def main():
    log("%s  %s" % (VERSION, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    import om
    doc = om.Application().CurrentDocument
    if doc is None:
        log("No open document.")
        return "Open a document with compound jobs, then run the probe again."
    path = doc.FullPath
    path = path() if callable(path) else path
    log("document: %s" % short(path, 300))
    jls = doc.CamModel.JobListSet
    joblists = list(jls.GetJobLists())
    log("")
    log("=== 1. ARGUMENTS OF EVERY METHOD (nothing run: a made-up keyword makes hyperMILL list them) ===")
    signatures(jls, "JobListSet")
    if joblists:
        jl = joblists[0]
        signatures(jl, "JobList %r" % name_of(jl))
        comp = next((c for c in jl.GetCompoundJobs() if list(c.GetJobs())), None)
        if comp is not None:
            signatures(comp, "CompoundJob %r" % name_of(comp))
            job = list(comp.GetJobs())[0]
            signatures(job, "Job %r" % name_of(job))
    tot = scan(joblists)
    log("")
    log("=== TOTALS ===")
    for k, v in sorted(tot.items()):
        log("  %-40s %d" % (k, v))
    if slow:
        log("  slow members (read once): " + ", ".join("%s %.1f s" % (k, v) for k, v in sorted(slow.items())))
    log("  reads made: %d" % calls["n"])
    files(path if isinstance(path, str) else "")
    log("")
    log("finished")
    return "Release probe v3 finished.\nSend the log:\n%s" % os.path.join(out_dir(), LOG_NAME)


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
