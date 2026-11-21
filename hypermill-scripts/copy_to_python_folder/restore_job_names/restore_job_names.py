# restore_job_names.py - hyperMILL 35
# Renames every toolpath (job) back to its number and toolpath type, e.g. "2: 3D Optimized Roughing", "7: Contour Turning".
#   number        = the job number hyperMILL gave the job: Job.ID, else its *JOBID setting, else the "N:" in front of the name
#   toolpath type = Job.LocCycleName (the cycle name hyperMILL puts in a new job's name)
# Name format (first screen):  "N: Type"  or  "N: T<tool ID> Type"  (the default names in your documents carry the tool ID)
# Compound jobs (B programs, dividers) keep their names. Toolpaths already named right are left alone.
# Screens: Joblist (one or all), Name format -> the list of changes in the output window -> Rename? No / Yes.
# Log (old -> new for every toolpath, so a name can be typed back): C:\Users\Public\Documents\OPEN MIND\restore_job_names_log.txt
import os, re, tempfile, traceback, datetime

OUT_DIR = r"C:\Users\Public\Documents\OPEN MIND"
TITLE = "Restore toolpath names"
FORMATS = ["N: Type", "N: T<tool ID> Type"]
MAX_BOX_LINES = 30
lines = []


def log(*a):
    lines.append(" ".join(str(x) for x in a))


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
    rows = str(t).split("\n")
    if len(rows) > MAX_BOX_LINES:
        rows = rows[:MAX_BOX_LINES - 1] + ["... full list in the output window and restore_job_names_log.txt"]
    g.ShowMessageBox(g.MessageBoxType.INFORMATION, TITLE, "\n".join(rows))


def output(t):
    g = _gui()
    try:
        g.CleanOutput(g.UIOutputWindow.ALL)
        g.WriteToOutput(t, g.UIOutputWindow.ALL)
        g.ProcessEvents()
    except Exception:
        pass


def pick(v, options):
    if isinstance(v, int) and not isinstance(v, bool):
        return v if 0 <= v < len(options) else 0
    return options.index(v) if v in options else 0


def cfg_of(job):
    try:
        return job.GetCfgParameters() or {}
    except Exception:
        return {}


def tool_id(job):
    try:
        t = job.GetTool()
    except Exception:
        t = None
    if t is None:
        return ""
    for a in ("ID", "Number", "Name"):
        v = text(getattr(t, a, ""))
        if v:
            return v
    return ""


def whole(v):
    """'12', 12, '12.0' -> '12'; anything else -> ''"""
    t = text(v)
    if re.match(r"^\d+(\.0*)?$", t):
        n = int(float(t))
        return str(n) if n > 0 else ""
    return ""


def name_number(name):
    m = re.match(r"^\s*(\d+)\s*:", name)
    return m.group(1) if m else ""


def id_trusted(jobs):
    """Job.ID is used only when it matches the "N:" of every toolpath that still has one (else it is not the job number)."""
    pairs = [(whole(getattr(j, "ID", None)), name_number(text(getattr(j, "Name", "")))) for j in jobs]
    pairs = [p for p in pairs if p[0] and p[1]]
    bad = [p for p in pairs if p[0] != p[1]]
    log("Job.ID check: %d toolpaths with N: and ID, %d differ -> Job.ID %s" % (len(pairs), len(bad), "NOT used" if bad else "used"))
    return not bad


def number_of(job, name, use_id=True):
    for v in ((getattr(job, "ID", None) if use_id else None), cfg_of(job).get("*JOBID", "")):
        n = whole(v)
        if n:
            return n
    m = re.match(r"^\s*(\d+)\s*:", name)
    return m.group(1) if m else ""


def why_not(job):
    """what the job holds, for the log when a toolpath is left alone"""
    cfg = cfg_of(job)
    ids = dict((k, text(v)) for k, v in cfg.items() if "ID" in str(k).upper() and len(text(v)) < 40) if hasattr(cfg, "items") else {}
    return "ID=%r *JOBID=%r cfg *ID*=%s LocCycleName=%r CycleName=%r JobType=%r" % (
        text(getattr(job, "ID", "")), text(cfg.get("*JOBID", "")), ids, text(getattr(job, "LocCycleName", "")),
        text(getattr(job, "CycleName", "")), text(getattr(job, "JobType", "")))


def type_of(job):
    t = text(getattr(job, "LocCycleName", ""))
    if not t:
        t = text(getattr(job, "CycleName", "")).split("|")[-1].strip()
    return t


def target(job, fmt, use_id=True):
    """(new name, reason it can't be made)"""
    name = text(getattr(job, "Name", ""))
    n, t = number_of(job, name, use_id), type_of(job)
    if not n:
        return "", "no job number"
    if not t:
        return "", "no toolpath type"
    if fmt == 1:
        tid = tool_id(job)
        return ("%s: T%s %s" % (n, tid, t) if tid else "%s: %s" % (n, t)), ""
    return "%s: %s" % (n, t), ""


def set_name(job, new):
    """Name property first, then the *JOBNAME setting; read back. Returns (ok, how)."""
    try:
        job.Name = new
        if text(job.Name) == new:
            return True, "Name"
        err = "Name did not change"
    except Exception as e:
        err = "Name: %s" % e
    try:
        job.SetCfgParameters({"*JOBNAME": new})
        if text(job.Name) == new or text(cfg_of(job).get("*JOBNAME", "")) == new:
            return True, "*JOBNAME"
        return False, err + "; *JOBNAME did not change"
    except Exception as e:
        return False, err + "; *JOBNAME: %s" % e


def jobs_of(jl):
    """Toolpaths of a joblist in tree order: inside compound jobs, then any outside them."""
    out, seen = [], set()
    def add(j):
        k = text(getattr(j, "UUID", "")) or id(j)
        if k not in seen:
            seen.add(k)
            out.append(j)
    try:
        for cj in jl.GetCompoundJobs():
            for j in cj.GetJobs():
                add(j)
    except Exception:
        log("compound jobs not read:", traceback.format_exc())
    try:
        for j in jl.GetJobs():
            add(j)
    except Exception:
        pass
    return out


def run():
    try:
        import om
        log(TITLE, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        doc = om.Application().CurrentDocument
        if doc is None:
            info("No document open."); return
        log("document:", text(doc.FullPath))
        lists = list(doc.CamModel.JobListSet.GetJobLists())
        names = [text(jl.Name) for jl in lists]
        if not names:
            info("No joblists in this document."); return
        scopes = names + (["All joblists"] if len(names) > 1 else [])
        g = _gui()
        dlg = g.InputDialog(TITLE)
        dlg.AddDropDown("Joblist", scopes, defaultIndex=0)
        dlg.AddDropDown("Name format", FORMATS, defaultIndex=0)
        ok, v = dlg.Show()
        if not ok:
            log("cancelled"); return
        scope = scopes[pick(v.get("Joblist"), scopes)]
        fmt = pick(v.get("Name format"), FORMATS)
        log("joblist:", scope, "| format:", FORMATS[fmt])
        changes, same, skipped = [], 0, []
        for jl, n in zip(lists, names):
            if scope != "All joblists" and n != scope:
                continue
            jobs = jobs_of(jl)
            use_id = id_trusted(jobs)
            for j in jobs:
                old = text(getattr(j, "Name", ""))
                new, why = target(j, fmt, use_id)
                if why:
                    skipped.append((old, why))
                    log("left alone:", old, "|", why_not(j))
                elif new == old:
                    same += 1
                else:
                    changes.append((j, old, new))
        rep = ["%s  %s  format %s" % (TITLE, scope, FORMATS[fmt]), ""]
        rep += ["  %-44s ->  %s" % (o, nw) for _, o, nw in changes] or ["  nothing to rename"]
        if skipped:
            rep += ["", "Left alone:"] + ["  %-44s  (%s)" % s for s in skipped]
        rep += ["", "%d to rename, %d already right, %d left alone." % (len(changes), same, len(skipped))]
        for ln in rep:
            log(ln)
        output("\n".join(rep))
        if not changes:
            info("Nothing to rename: %d toolpath%s already named right%s." % (
                same, "" if same == 1 else "s", (", %d left alone (see the output window)" % len(skipped)) if skipped else "")); return
        dlg = g.InputDialog(TITLE + " | %d toolpath%s" % (len(changes), "" if len(changes) == 1 else "s"))
        opts = ["No - change nothing", "Yes - rename %d toolpath%s" % (len(changes), "" if len(changes) == 1 else "s")]
        dlg.AddDropDown("Rename", opts, defaultIndex=0)
        ok, v = dlg.Show()
        if not ok or pick(v.get("Rename"), opts) != 1:
            log("not renamed (answered No)"); info("Nothing renamed."); return
        done, failed = 0, []
        for j, old, new in changes:
            ok, how = set_name(j, new)
            log(("renamed  " if ok else "FAILED   ") + "%s -> %s  (%s)" % (old, new, how))
            if ok:
                done += 1
            else:
                failed.append("%s: %s" % (old, how))
        msg = ["Renamed %d toolpath%s." % (done, "" if done == 1 else "s")]
        if same:
            msg.append("%d already named right." % same)
        if skipped:
            msg.append("%d left alone (no job number or no toolpath type): see the output window." % len(skipped))
        if failed:
            msg += ["", "Could not rename:"] + ["  " + f for f in failed]
        msg += ["", "Old names are in restore_job_names_log.txt."]
        info("\n".join(msg))
    except Exception:
        log("FAILED:", traceback.format_exc())
        try:
            info("Failed. See restore_job_names_log.txt.")
        except Exception:
            pass
    finally:
        try:
            d = OUT_DIR if os.path.isdir(OUT_DIR) else tempfile.gettempdir()
            with open(os.path.join(d, "restore_job_names_log.txt"), "w", encoding="utf-8") as f:
                f.write("\n".join(lines) + "\n")
        except Exception:
            pass


if __name__ == "__main__":
    run()
