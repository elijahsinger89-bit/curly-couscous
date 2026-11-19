# release_check.py - the go-to-machine check: every job of a B program is calculated, has no errors, and has been run
# through Simulation Center without a collision since its last change.
# How hyperMILL 35 records it (release_probe v1-v5, 17 Nov 2026):
#   - Each job's POF file (Job.PofFileName) has a header line "0: ucid(<toolpath id>)". Recalculating a job gives it a new
#     id; regrouping keeps it.
#   - Simulation Center writes POF\<toolpath id>.ccrpt for every toolpath of the run: "CC_RESULT 1" = the run was clean,
#     "CC_RESULT 0" = the run had a collision (every toolpath of that run gets 0). Changing a job deletes its .ccrpt.
#   - Job.POFStatus UP_TO_DATE = calculated; Job.Status ERRORS = the job has errors.
#   - The job tree's light bulb is the toolpath display, not a simulation status.
import os
import re

VERSION = "2026-11-19"
HEADER_BYTES = 65536
UCID_RE = re.compile(rb"ucid\(([0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12})\)")
CLEAN = "CC_RESULT 1"
COLLISION = "CC_RESULT 0"

R_ERRORS = "has errors"
R_NOT_CALC = "not calculated"
R_NO_POF = "no toolpath file (not calculated)"
R_NO_ID = "no toolpath id in its POF file"
R_NOT_SIM = "not simulated, or changed since it was simulated"
R_COLLISION = "Simulation Center run had a collision: fix it and re-simulate"


def val(x):
    return x() if callable(x) else x


def text(x):
    try:
        v = val(x)
    except Exception:
        return ""
    return "" if v is None else str(v)


def enum_name(v):
    s = str(v)
    return s.split(".")[-1].split(":")[0].strip("<> ") if "." in s else s


def name_of(obj):
    return text(getattr(obj, "Name", ""))


def pof_path(job, doc_folder):
    p = text(getattr(job, "PofFileName", ""))
    if not p:
        return ""
    if os.path.isabs(p) or re.match(r"^[A-Za-z]:[\\/]", p):
        return p
    return os.path.join(doc_folder, "POF", p)


def read_ucid(pof):
    """The toolpath id from the POF header, lower case; '' when there is none."""
    try:
        with open(pof, "rb") as f:
            m = UCID_RE.search(f.read(HEADER_BYTES))
    except Exception:
        return ""
    return m.group(1).decode().lower() if m else ""


class Ccrpt:
    """.ccrpt files of one POF folder, looked up by toolpath id (any case)."""
    def __init__(self):
        self._dirs = {}

    def result(self, pof_folder, ucid):
        if pof_folder not in self._dirs:
            try:
                self._dirs[pof_folder] = {n.lower(): n for n in os.listdir(pof_folder) if n.lower().endswith(".ccrpt")}
            except Exception:
                self._dirs[pof_folder] = {}
        n = self._dirs[pof_folder].get(ucid.lower() + ".ccrpt")
        if n is None:
            return None
        try:
            with open(os.path.join(pof_folder, n), "rb") as f:
                return f.read(256).decode("utf-8", "replace").strip()
        except Exception as e:
            return "<not read: %s>" % e

    def run_time(self, pof_folder, ucid):
        """When Simulation Center wrote the result (the run), 'YYYY-MM-DD HH:MM'; '' when unknown."""
        n = self._dirs.get(pof_folder, {}).get(ucid.lower() + ".ccrpt")
        if n is None:
            return ""
        try:
            import datetime
            return datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(pof_folder, n))).strftime("%Y-%m-%d %H:%M")
        except Exception:
            return ""


def check_job(job, doc_folder, ccrpt):
    """dict(name, ok, reason, ucid, result)."""
    r = dict(name=name_of(job), ok=False, reason="", ucid="", result="", run="")
    status = enum_name(val(getattr(job, "Status", "")))
    pofs = enum_name(val(getattr(job, "POFStatus", "")))
    if status == "ERRORS":
        r["reason"] = R_ERRORS
        return r
    if pofs != "UP_TO_DATE":
        r["reason"] = "%s (%s)" % (R_NOT_CALC, pofs or "no POF status")
        return r
    pof = pof_path(job, doc_folder)
    if not pof or not os.path.isfile(pof):
        r["reason"] = R_NO_POF
        return r
    r["ucid"] = read_ucid(pof)
    if not r["ucid"]:
        r["reason"] = R_NO_ID
        return r
    res = ccrpt.result(os.path.dirname(pof), r["ucid"])
    r["result"] = res or ""
    if res is None:
        r["reason"] = R_NOT_SIM
    elif res == CLEAN:
        r["ok"] = True
    elif res == COLLISION:
        r["reason"] = R_COLLISION
        r["run"] = ccrpt.run_time(os.path.dirname(pof), r["ucid"])
    else:
        r["reason"] = "unknown Simulation Center result %r" % res
    return r


def check_compound(cj, doc_folder, ccrpt):
    """dict(ok, jobs=[check_job ...], failed=[...])."""
    try:
        jobs = list(cj.GetJobs())
    except Exception:
        jobs = []
    res = [check_job(j, doc_folder, ccrpt) for j in jobs]
    failed = [x for x in res if not x["ok"]]
    return dict(ok=bool(res) and not failed, jobs=res, failed=failed)
