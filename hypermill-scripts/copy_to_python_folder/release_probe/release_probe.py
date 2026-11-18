# release_probe.py - hyperMILL 35 - release probe v4 (read-only)
# For the go-to-machine (release) script: how to tell a job has been run through Simulation Center, and is unchanged.
# Known from v1-v3: Simulation Center writes POF\<uuid>.ccrpt (13 bytes) and POF\<uuid>_@...rsf for each simulated job,
#   and nothing for jobs it did not simulate. Job.POFStatus does not tell simulated from not simulated. The job tree shows
#   no simulation status (the light bulb is the toolpath display). POF files are rewritten without toolpath changes
#   (regrouping), so dates cannot tell "changed since simulated".
# v4 reads:
#   1. PofFile: its constructor and members (arguments asked with a made-up keyword: hyperMILL refuses the call before
#      running anything), and every method of the core classes whose arguments mention PofFile
#   2. every job (also jobs outside compound jobs): UUID, ID, Status, POFStatus, PofFileName, the POF file's date, the
#      .ccrpt of that UUID (date, the 13 bytes as text and hex), and - when PofFile opens a file by name - the
#      GetMovementsCheckSum() of a temporary COPY of the job's POF file, next to the .ccrpt bytes
#   3. .ccrpt files no job matches, the VNC\ files and the .omgcfg they point to
# Changes nothing in the document. Methods that change the document are never called or asked.
# A read slower than 2 s is not repeated; the job scan stops after 300 s.
# Log (written line by line): C:\Users\Public\Documents\OPEN MIND\release_probe_log.txt
import os
import re
import sys
import time
import types
import datetime
import tempfile
import traceback

VERSION = "release_probe v4"
OUT_DIR = r"C:\Users\Public\Documents\OPEN MIND"
LOG_NAME = "release_probe_log.txt"
TITLE = "Release probe"
MAX_LINE = 2000
MAX_LINES = 40000
MAX_SECONDS = 300.0
SLOW = 2.0
SIG_KW = "release_probe_signature_only_9f3c"      # no hyperMILL method has an argument with this name
SIG_SKIP = ("Set", "Create", "Delete", "Remove", "Clear", "Reset", "Move", "Rename", "Insert", "Lock", "Replace", "Write",
            "Import", "Export", "Clone", "Link", "Enable", "Optimize", "Sync", "Resort", "Update", "Apply", "Copy", "Paste",
            "Override", "Change", "Add", "Run", "Calculate", "Generate", "Post", "Simulate", "Save", "Load", "Open",
            "Close", "Execute", "Start", "Stop")
MAX_TEXT_FILE = 65536
MAX_TEXT_LINES = 300

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


def short(v, n=160):
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


def stamp(t):
    return datetime.datetime.fromtimestamp(t).strftime("%Y-%m-%d %H:%M:%S")


def timed(label, fn):
    """Calls fn once, unless this member was slow before. Returns (value, note)."""
    if label in slow:
        return None, "<slow before: not read>"
    t = time.perf_counter()
    try:
        v, note = fn(), ""
    except Exception as e:
        v, note = None, "<error %s>" % (str(e).splitlines() or [type(e).__name__])[0][:150]
    dt = time.perf_counter() - t
    calls["n"] += 1
    if dt > SLOW:
        slow[label] = dt
        log("  SLOW: %s took %.1f s, not read again" % (label, dt))
    return v, note


def enum_name(v):
    s = str(v)
    return s.split(".")[-1].split(":")[0].strip("<> ") if "." in s else s


def uuid_key(u):
    return str(u).strip().strip("{}").lower()


# ---------------- arguments without running anything ----------------
def is_native(raw):
    """A built-in (compiled) hyperMILL function: rejects an unknown keyword argument before running."""
    f = getattr(raw, "__func__", raw)
    return isinstance(f, types.BuiltinFunctionType) and type(raw).__name__ in ("instancemethod", "builtin_function_or_method")


def overloads(text):
    out, on = [], False
    for ln in str(text).splitlines():
        s = ln.strip()
        if "argument types are supported" in s:
            on = True
            continue
        if on:
            if not s or s.startswith("Invoked with"):
                break
            out.append(s[s.index("("):] if "(" in s else s)
    return out


def ask(fn):
    """fn calls something with the made-up keyword. Returns (overloads, note)."""
    try:
        fn()
        return [], "!! accepted the made-up argument (it may have run)"
    except TypeError as e:
        ov = overloads(e)
        return ov, ("" if ov else "<%s>" % (str(e).splitlines() or ["TypeError"])[0][:200])
    except Exception as e:
        return [], "<%s: %s>" % (type(e).__name__, (str(e).splitlines() or [""])[0][:200])


def is_prop(raw):
    return isinstance(raw, property) or type(raw).__name__ in ("property", "getset_descriptor", "member_descriptor")


def find_class(name, near):
    mods = []
    m = sys.modules.get(getattr(type(near), "__module__", "") or "")
    if m is not None:
        mods.append(m)
    mods += [v for k, v in sorted(sys.modules.items()) if v is not None and (k == "om" or k.startswith("om."))]
    for mod in mods:
        try:
            c = mod.__dict__.get(name)
        except Exception:
            c = None
        if isinstance(c, type):
            return c, mod
    return None, None


def pof_class(job):
    """PofFile: constructor and members. Returns (class, opens_by_name, checksum_without_args)."""
    log("")
    log("=== 1. PofFile (arguments asked, nothing run) ===")
    cls, mod = find_class("PofFile", job)
    if cls is None:
        log("  PofFile class not found in the loaded om modules")
        return None, False, False
    log("  %s.PofFile" % mod.__name__)
    ov, note = ask(lambda: cls(**{SIG_KW: None}))
    for o in ov:
        log("  init  PofFile%s" % o)
    if note:
        log("  init  %s" % note)
    # pybind11 writes constructors as "PofFile(fileName: str)" (no self, no result)
    by_name = any(re.match(r"^\((self: [^,()]+, )?\w+: str\)( -> None)?$", o) for o in ov)
    cs_ok = False
    for n in public(cls):
        try:
            raw = cls.__dict__[n] if n in cls.__dict__ else getattr(cls, n)
        except Exception:
            continue
        if is_prop(raw):
            log("  prop  %s" % n)
            continue
        f = getattr(cls, n, None)
        if not callable(f) or isinstance(f, type) or n.startswith(SIG_SKIP) or not is_native(f):
            log("  def   %s  (not asked)" % n)
            continue
        ov, note = ask(lambda f=f: f(**{SIG_KW: None}))
        for o in ov:
            log("  def   %s%s" % (n, o))
            if n == "GetMovementsCheckSum" and re.match(r"^\(self: [^,()]+\) -> ", o):
                cs_ok = True
        if note:
            log("  def   %s  %s" % (n, note))
    log("  opens a POF file by name: %s | GetMovementsCheckSum without arguments: %s" % (by_name, cs_ok))
    return cls, by_name, cs_ok


def who_returns_pof(job):
    """Methods of the core classes whose arguments or result mention PofFile."""
    log("")
    log("--- methods that take or return a PofFile ---")
    mod = sys.modules.get(getattr(type(job), "__module__", "") or "")
    if mod is None:
        log("  core module not in sys.modules: skipped")
        return
    hits, asked = 0, 0
    for cname in sorted(mod.__dict__):
        c = mod.__dict__[cname]
        if not isinstance(c, type) or hasattr(c, "__members__"):
            continue
        for n in public(c):
            if n.startswith(SIG_SKIP):
                continue
            f = getattr(c, n, None)
            if f is None or is_prop(c.__dict__.get(n)) or not callable(f) or isinstance(f, type) or not is_native(f):
                continue
            asked += 1
            ov, _ = ask(lambda f=f: f(**{SIG_KW: None}))
            for o in ov:
                if "PofFile" in o or "CheckSum" in o or "Simul" in o or "Collision" in o:
                    log("  %s.%s%s" % (cname, n, o))
                    hits += 1
    log("  %d methods asked, %d mention PofFile / CheckSum / Simul / Collision" % (asked, hits))


# ---------------- 2. every job ----------------
def read_bytes(p, n=4096):
    try:
        with open(p, "rb") as f:
            return f.read(n)
    except Exception as e:
        return None


def show_bytes(b):
    if b is None:
        return "not read"
    try:
        t = b.decode("utf-8")
    except Exception:
        t = None
    return "text=%r hex=%s" % (t if t is not None else "(binary)", b.hex(" "))


def checksum(pof_cls, pof):
    """GetMovementsCheckSum of a temporary COPY of the POF file: the job's own POF file is only read, never opened by
    hyperMILL's PofFile (in case opening it writes)."""
    import shutil
    tmpdir = tempfile.mkdtemp(prefix="release_probe_")
    cp = os.path.join(tmpdir, os.path.basename(pof))
    try:
        shutil.copyfile(pof, cp)
        obj, note = timed("PofFile(name)", lambda: pof_cls(cp))
        if obj is None:
            return "not read: %s" % note
        cs, note = timed("PofFile.GetMovementsCheckSum", lambda: obj.GetMovementsCheckSum())
        del obj
        return note or "%s%s" % (short(cs), ("  (hex %x)" % cs) if isinstance(cs, int) and not isinstance(cs, bool) else "")
    except Exception as e:
        return "not read: %s" % e
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


def scan(joblists, folder, pof_cls, by_name, cs_ok):
    log("")
    log("=== 2. EVERY JOB: UUID, status, POF file, .ccrpt (Simulation Center), checksum ===")
    pofdir = os.path.join(folder, "POF")
    try:
        names = {n.lower(): n for n in os.listdir(pofdir)}
    except Exception as e:
        names = {}
        log("  POF folder not listed: %s" % e)
    used = set()
    t0 = time.perf_counter()
    first = True
    for jl in joblists:
        log("")
        log("joblist %r" % name_of(jl))
        owner = {}
        for c in list(jl.GetCompoundJobs()):
            for j in list(c.GetJobs()):
                u, _ = timed("Job.UUID", lambda j=j: j.UUID)
                owner[uuid_key(u)] = name_of(c)
        for j in list(jl.GetJobs()):
            if time.perf_counter() - t0 > MAX_SECONDS:
                log("  (stopped after %d s)" % int(MAX_SECONDS))
                return used, names
            vals = {}
            for n in ("UUID", "ID", "Status", "POFStatus", "PofFileName"):
                if first:
                    log("    reading Job.%s" % n)
                v, note = timed("Job." + n, lambda n=n: getattr(j, n))
                vals[n] = note or (enum_name(v) if n in ("Status", "POFStatus") else v)
            first = False
            key = uuid_key(vals["UUID"])
            log("")
            log("  J %r  in %r" % (name_of(j), owner.get(key, "(no compound job)")))
            log("      UUID=%s  ID=%s  Status=%s  POFStatus=%s" % (vals["UUID"], vals["ID"], vals["Status"], vals["POFStatus"]))
            pf = str(vals["PofFileName"] or "")
            pof = pf if os.path.isabs(pf) or re.match(r"^[A-Za-z]:[\\/]", pf) else os.path.join(pofdir, pf)
            try:
                st = os.stat(pof)
                log("      POF  %s  %s  %d bytes" % (pf, stamp(st.st_mtime), st.st_size))
            except Exception:
                log("      POF  %s  (file not found)" % pf)
            cc = names.get(key + ".ccrpt")
            if cc:
                used.add(cc)
                p = os.path.join(pofdir, cc)
                b = read_bytes(p)
                log("      CCRPT %s  %s  %s" % (cc, stamp(os.stat(p).st_mtime), show_bytes(b)))
            else:
                log("      CCRPT none (not simulated)")
            rsf = [names[k] for k in names if k.startswith(key + "_@") and k.endswith(".rsf")]
            if rsf:
                log("      RSF  %s" % ", ".join(sorted(rsf)))
            if pof_cls is not None and by_name and cs_ok and os.path.exists(pof):
                log("      CHECKSUM %s" % checksum(pof_cls, pof))
    return used, names


# ---------------- 3. files ----------------
def show_text(p, label):
    try:
        st = os.stat(p)
    except Exception:
        log("  %s  (not found: %s)" % (label, p))
        return
    log("")
    log("  %s  %d bytes  %s" % (label, st.st_size, stamp(st.st_mtime)))
    b = read_bytes(p, MAX_TEXT_FILE)
    txt = None
    for enc in ("utf-8-sig", "utf-16", "cp1252"):
        try:
            txt = b.decode(enc)
            break
        except Exception:
            pass
    for i, ln in enumerate((txt or repr(b[:2000])).splitlines()):
        if i >= MAX_TEXT_LINES:
            log("    | ... (%d lines shown)" % MAX_TEXT_LINES)
            break
        log("    | " + ln)


def files(folder, used, names):
    log("")
    log("=== 3. FILES ===")
    rest = sorted(v for k, v in names.items() if k.endswith(".ccrpt") and v not in used)
    log("  .ccrpt files no job matches: %d" % len(rest))
    for cc in rest:
        p = os.path.join(folder, "POF", cc)
        log("    %s  %s  %s" % (cc, stamp(os.stat(p).st_mtime), show_bytes(read_bytes(p))))
    vnc = os.path.join(folder, "VNC")
    if not os.path.isdir(vnc):
        log("  no VNC folder")
        return
    for n in sorted(os.listdir(vnc)):
        p = os.path.join(vnc, n)
        if not os.path.isfile(p):
            continue
        show_text(p, "VNC\\" + n)
        if n.lower().endswith(".nclist"):
            b = read_bytes(p, MAX_TEXT_FILE) or b""
            for m in re.finditer(r'omgcfg file="([^"]+)"', b.decode("utf-8", "replace")):
                show_text(m.group(1), "omgcfg " + m.group(1))


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
    folder = os.path.dirname(str(path))
    joblists = list(doc.CamModel.JobListSet.GetJobLists())
    job = next((j for jl in joblists for j in list(jl.GetJobs())), None)
    pof_cls, by_name, cs_ok = (None, False, False)
    if job is not None:
        pof_cls, by_name, cs_ok = pof_class(job)
        who_returns_pof(job)
    used, names = scan(joblists, folder, pof_cls, by_name, cs_ok)
    files(folder, used, names)
    log("")
    log("reads made: %d" % calls["n"])
    if slow:
        log("slow members (read once): " + ", ".join("%s %.1f s" % (k, v) for k, v in sorted(slow.items())))
    log("finished")
    return "Release probe v4 finished.\nSend the log:\n%s" % os.path.join(out_dir(), LOG_NAME)


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
