# release_probe.py - hyperMILL 35 - release probe v5 (read-only)
# For the go-to-machine (release) script: which toolpath ID (ucid) belongs to which job.
# Known from v1-v4:
#   - Simulation Center writes POF\<ucid>.ccrpt ("CC_RESULT 1") per simulated toolpath. The ucid is not the job UUID.
#   - Changing a job deletes its .ccrpt; regrouping (POF rewritten, toolpath unchanged) keeps it.
#   - C:\TEMP\OPEN MIND\VMCenter\<joblist>\<joblist>.omgcfg lists the simulated POF files with ucid and crc (POF names
#     from the time of the simulation).
#   - GetMovementsCheckSum covers movements only (a feed change keeps it): not used.
# v5 reads, per job:
#   - the job's POF file bytes (read only): every GUID in it, and where each .ccrpt ucid appears (ASCII and UTF-16)
#   - PofFile.GetCfgParameters() of a temporary COPY of the POF file (hyperMILL never opens the original)
#   - the job's own settings (GetCfgParameters): values that are GUIDs or ucids
#   - the CRC32 of the POF file, compared with the crc values in the .omgcfg
# then a summary: each .ccrpt ucid and the job(s) it was found in.
# Changes nothing in the document and nothing in the POF folder. A read slower than 2 s is not repeated.
# Log (written line by line): C:\Users\Public\Documents\OPEN MIND\release_probe_log.txt
import os
import re
import sys
import time
import types
import zlib
import shutil
import datetime
import tempfile
import traceback

VERSION = "release_probe v5"
OUT_DIR = r"C:\Users\Public\Documents\OPEN MIND"
LOG_NAME = "release_probe_log.txt"
TITLE = "Release probe"
MAX_LINE = 2000
MAX_LINES = 40000
MAX_SECONDS = 300.0
SLOW = 2.0
SIG_KW = "release_probe_signature_only_9f3c"
MAX_POF_BYTES = 64 * 1024 * 1024
MAX_GUIDS = 12
FULL_CFG_JOBS = 2                    # PofFile.GetCfgParameters printed in full for the first jobs with a POF
GUID = re.compile(rb"[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12}")
GUID_S = re.compile(r"[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12}")

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


def key(u):
    return str(u).strip().strip("{}").lower()


def read_bytes(p, n):
    try:
        with open(p, "rb") as f:
            return f.read(n)
    except Exception:
        return None


def printable(b):
    return "".join(chr(c) if 32 <= c < 127 else "." for c in b)


# ---------------- PofFile class (arguments asked without running, as v4) ----------------
def is_native(raw):
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
    try:
        fn()
        return [], "!! accepted the made-up argument"
    except TypeError as e:
        return overloads(e), ""
    except Exception as e:
        return [], "<%s>" % type(e).__name__


def find_pof_class(job):
    mods = []
    m = sys.modules.get(getattr(type(job), "__module__", "") or "")
    if m is not None:
        mods.append(m)
    mods += [v for k, v in sorted(sys.modules.items()) if v is not None and (k == "om" or k.startswith("om."))]
    for mod in mods:
        c = mod.__dict__.get("PofFile") if hasattr(mod, "__dict__") else None
        if isinstance(c, type):
            ov, _ = ask(lambda: c(**{SIG_KW: None}))
            by_name = any(re.match(r"^\((self: [^,()]+, )?\w+: str\)( -> None)?$", o) for o in ov)
            f = getattr(c, "GetCfgParameters", None)
            cfg_ok = False
            if f is not None and is_native(f):
                ov2, _ = ask(lambda: f(**{SIG_KW: None}))
                cfg_ok = any(re.match(r"^\(self: [^,()]+\) -> ", o) for o in ov2)
            log("PofFile: %s.PofFile  opens by name: %s  GetCfgParameters without arguments: %s" % (mod.__name__, by_name, cfg_ok))
            return c if (by_name and cfg_ok) else None
    log("PofFile: not found in the loaded om modules")
    return None


def pof_cfg(pof_cls, pof):
    """PofFile.GetCfgParameters() of a temporary COPY of the POF file."""
    tmpdir = tempfile.mkdtemp(prefix="release_probe_")
    cp = os.path.join(tmpdir, os.path.basename(pof))
    try:
        shutil.copyfile(pof, cp)
        obj, note = timed("PofFile(name)", lambda: pof_cls(cp))
        if obj is None:
            return None, note
        cfg, note = timed("PofFile.GetCfgParameters", lambda: obj.GetCfgParameters())
        del obj
        return cfg, note
    except Exception as e:
        return None, str(e)
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


# ---------------- .ccrpt and .omgcfg ----------------
def ccrpt_files(pofdir):
    out = {}
    try:
        for n in os.listdir(pofdir):
            if n.lower().endswith(".ccrpt"):
                p = os.path.join(pofdir, n)
                b = read_bytes(p, 256) or b""
                out[key(n[:-6])] = dict(name=n, text=b.decode("utf-8", "replace").strip(), time=os.stat(p).st_mtime)
    except Exception as e:
        log("  POF folder not listed: %s" % e)
    return out


def omgcfg_entries(folder):
    """[(pof file, ucid, crc)] from every .omgcfg the VNC\\*.nclist files point to."""
    out = []
    vnc = os.path.join(folder, "VNC")
    if not os.path.isdir(vnc):
        return out
    for n in sorted(os.listdir(vnc)):
        if not n.lower().endswith(".nclist"):
            continue
        t = (read_bytes(os.path.join(vnc, n), 65536) or b"").decode("utf-8", "replace")
        for m in re.finditer(r'omgcfg file="([^"]+)"', t):
            g = (read_bytes(m.group(1), 1 << 20) or b"").decode("utf-8", "replace")
            for e in re.finditer(r'<pof file="([^"]+)"\s+ucid="([^"]+)"\s+crc="([^"]+)"', g):
                out.append((e.group(1), key(e.group(2)), e.group(3)))
    return out


# ---------------- per job ----------------
def search_pof(b, ccr):
    """GUIDs in the POF bytes, and the offsets of each .ccrpt ucid (ASCII any case, UTF-16LE)."""
    guids, seen = [], set()
    for m in GUID.finditer(b):
        g = m.group().decode().lower()
        if g not in seen:
            seen.add(g)
            guids.append((g, m.start()))
    low = b.lower()                     # ASCII letters only: also lower-cases UTF-16LE text
    hits = []
    for u in ccr:
        for form, needle in (("ascii", u.encode()), ("utf16", u.encode("utf-16-le"))):
            i = low.find(needle)
            if i >= 0:
                hits.append((u, form, i, printable(b[max(0, i - 40):i + len(needle) + 20])))
    return guids, hits


def scan(joblists, folder, pof_cls, ccr, omg):
    log("")
    log("=== 2. EVERY JOB ===")
    pofdir = os.path.join(folder, "POF")
    found = {u: [] for u in ccr}
    omg_by_crc = {}
    for f, u, c in omg:
        omg_by_crc.setdefault(c, []).append((f, u))
    t0 = time.perf_counter()
    full = 0
    for jl in joblists:
        log("")
        log("joblist %r" % name_of(jl))
        owner = {}
        for c in list(jl.GetCompoundJobs()):
            for j in list(c.GetJobs()):
                u, _ = timed("Job.UUID", lambda j=j: j.UUID)
                owner[key(u)] = name_of(c)
        for j in list(jl.GetJobs()):
            if time.perf_counter() - t0 > MAX_SECONDS:
                log("  (stopped after %d s)" % int(MAX_SECONDS))
                return found
            vals = {}
            for n in ("UUID", "ID", "Status", "POFStatus", "PofFileName"):
                v, note = timed("Job." + n, lambda n=n: getattr(j, n))
                vals[n] = note or (enum_name(v) if n in ("Status", "POFStatus") else v)
            jname = name_of(j)
            log("")
            log("  J %r  in %r" % (jname, owner.get(key(vals["UUID"]), "(no compound job)")))
            log("      UUID=%s  ID=%s  Status=%s  POFStatus=%s" % (vals["UUID"], vals["ID"], vals["Status"], vals["POFStatus"]))
            # the job's own settings
            jc, note = timed("Job.GetCfgParameters", lambda: j.GetCfgParameters())
            if isinstance(jc, dict):
                gk = [(k, v) for k, v in sorted(jc.items(), key=lambda kv: str(kv[0])) if GUID_S.search(str(v))]
                log("      job settings with a GUID value: %s" % (", ".join("%s=%s" % (k, v) for k, v in gk[:MAX_GUIDS]) or "none"))
                for k, v in jc.items():
                    for u in ccr:
                        if u in str(v).lower():
                            found[u].append("%s (job setting %s)" % (jname, k))
            else:
                log("      job settings not read: %s" % note)
            # the POF file
            pf = str(vals["PofFileName"] or "")
            pof = pf if os.path.isabs(pf) or re.match(r"^[A-Za-z]:[\\/]", pf) else os.path.join(pofdir, pf)
            if not os.path.isfile(pof):
                log("      POF  %s  (file not found)" % pf)
                continue
            st = os.stat(pof)
            b = read_bytes(pof, MAX_POF_BYTES) or b""
            crc = str(zlib.crc32(b) & 0xFFFFFFFF)
            log("      POF  %s  %s  %d bytes  crc32=%s%s" % (os.path.basename(pof), stamp(st.st_mtime), st.st_size, crc,
                  ("  = omgcfg crc of %s" % ", ".join("%s ucid %s" % (os.path.basename(f), u) for f, u in omg_by_crc[crc]))
                  if crc in omg_by_crc else ""))
            guids, hits = search_pof(b, ccr)
            log("      GUIDs in the POF file: %s" % (", ".join("%s@%d" % g for g in guids[:MAX_GUIDS]) or "none") +
                (" (+%d more)" % (len(guids) - MAX_GUIDS) if len(guids) > MAX_GUIDS else ""))
            for u, form, i, ctx in hits:
                log("      UCID %s in the POF file (%s, offset %d): %s" % (u, form, i, ctx))
                found[u].append("%s (POF file %s)" % (jname, form))
            if pof_cls is not None:
                cfg, note = pof_cfg(pof_cls, pof)
                if isinstance(cfg, dict):
                    if full < FULL_CFG_JOBS:
                        log("      PofFile.GetCfgParameters: %d keys" % len(cfg))
                        for k in sorted(cfg, key=str):
                            log("        %s = %s" % (k, short(cfg[k], 200)))
                        full += 1
                    else:
                        gk = [(k, v) for k, v in sorted(cfg.items(), key=lambda kv: str(kv[0])) if GUID_S.search(str(v))]
                        log("      PofFile settings with a GUID value: %s" % (", ".join("%s=%s" % (k, v) for k, v in gk[:MAX_GUIDS]) or "none"))
                    for k, v in cfg.items():
                        for u in ccr:
                            if u in str(v).lower():
                                found[u].append("%s (PofFile setting %s)" % (jname, k))
                else:
                    log("      PofFile settings not read: %s" % note)
    return found


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
    log("")
    log("=== 1. .ccrpt FILES AND THE .omgcfg ===")
    ccr = ccrpt_files(os.path.join(folder, "POF"))
    for u, d in sorted(ccr.items()):
        log("  %s  %s  %r" % (d["name"], stamp(d["time"]), d["text"]))
    if not ccr:
        log("  no .ccrpt files")
    omg = omgcfg_entries(folder)
    for f, u, c in omg:
        log("  omgcfg  %s  ucid %s  crc %s  %s" % (os.path.basename(f), u, c, ".ccrpt exists" if u in ccr else "no .ccrpt"))
    job = next((j for jl in joblists for j in list(jl.GetJobs())), None)
    pof_cls = find_pof_class(job) if job is not None else None
    found = scan(joblists, folder, pof_cls, ccr, omg)
    log("")
    log("=== 3. SUMMARY: each .ccrpt ucid and where it was found ===")
    for u in sorted(found):
        log("  %s  %r  ->  %s" % (u, ccr[u]["text"], "; ".join(found[u]) or "NOT FOUND in any job"))
    log("")
    log("reads made: %d" % calls["n"])
    if slow:
        log("slow members (read once): " + ", ".join("%s %.1f s" % (k, v) for k, v in sorted(slow.items())))
    log("finished")
    return "Release probe v5 finished.\nSend the log:\n%s" % os.path.join(out_dir(), LOG_NAME)


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
