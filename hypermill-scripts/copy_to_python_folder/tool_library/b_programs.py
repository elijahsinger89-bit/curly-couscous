# b_programs.py - B program names for compound jobs (shared: b_program_rename now, the go-to-machine script later).
# Name rule (same as the SINUMERIK generator): B_<part>_<step>_<machine>
#   step zero-padded to 3 digits, 4 when any step of the run is 1000 or more
#   part and machine: letters, digits, _ ; machine may be blank (then B_<part>_<step>)
#   24 characters at most (SINUMERIK program name limit)
# Step 1 belongs to the probe program the generator writes, so the first B program step is 2 or more.
# Compound job kinds:
#   note   no jobs inside (used as a comment / divider): skipped, keeps its text, takes no step number
#   one    every job inside uses the same tool: renamed
#   mixed  jobs with different tools: not renamed (a B program runs one tool: no T/M6, L_RUN_NESTS loads it)
#   notool jobs without a tool: not renamed
# hyperMILL 35 API used (confirmed by compound_probe v2): JobList.GetCompoundJobs() in tree order, CompoundJob.Name,
# .UUID, .GetJobs(), .GetCfgParameters()["*CPJOBNAME"], .SetCfgParameters(), Job.GetTool(), Tool.ID (= the ncTool id
# tool_load_mda writes into NEWT).
import re

VERSION = "2026-11-13"
MAX_NAME = 24
MAX_STEP = 9999
PROBE_STEP = 1
NAME_PART = re.compile(r"^[A-Za-z0-9_]+$")
PROGRAM_RULE = re.compile(r"^[A-Za-z_][A-Za-z_][A-Za-z0-9_]{0,22}$")


def val(x):
    return x() if callable(x) else x


def text(x):
    try:
        v = val(x)
    except Exception:
        return ""
    return "" if v is None else str(v)


# ---------------- name rule ----------------
def width_for(last_step):
    return 4 if last_step >= 1000 else 3


def program_name(part, step, width, machine=""):
    return "B_%s_%0*d%s" % (part, width, step, ("_" + machine) if machine else "")


def max_machine_len(part, width):
    """Longest machine designation that keeps B_<part>_<step>_<machine> within MAX_NAME."""
    return MAX_NAME - (2 + len(part) + 1 + width + 1)


def as_int(s):
    try:
        f = float(str(s).strip())
    except Exception:
        return None
    return int(f) if f == int(f) else None


def input_errors(part, machine, start, advance):
    """Problems with the four inputs, as plain messages (empty list = fine)."""
    err = []
    if not part:
        err.append("Part number is empty.")
    elif not NAME_PART.match(part):
        err.append("Part number can only use letters, digits and _ (no - or spaces): %s" % part)
    if machine and not NAME_PART.match(machine):
        err.append("Machine can only use letters, digits and _ (no - or spaces): %s" % machine)
    s, a = as_int(start), as_int(advance)
    if s is None:
        err.append("Starting step must be a whole number: %s" % start)
    elif s <= PROBE_STEP:
        err.append("Starting step must be %d or more: step %d is the probe program." % (PROBE_STEP + 1, PROBE_STEP))
    if a is None or (a is not None and a < 1):
        err.append("Advance must be a whole number of 1 or more: %s" % advance)
    return err


# ---------------- reading the document ----------------
def compound_jobs(joblist):
    try:
        return list(joblist.GetCompoundJobs())
    except Exception:
        return []


def tool_id(tool):
    if tool is None:
        return ""
    for a in ("ID", "Number"):
        if hasattr(tool, a):
            v = text(getattr(tool, a))
            if v:
                return v
    return text(getattr(tool, "Name", ""))


def classify(cj, joblist_name=""):
    """One compound job -> dict(name, uuid, joblist, kind, jobs, tools[ids], tool_names[], obj)."""
    try:
        jobs = list(cj.GetJobs())
    except Exception:
        jobs = []
    ids, names, notool = [], [], 0
    for j in jobs:
        try:
            t = j.GetTool()
        except Exception:
            t = None
        if t is None:
            notool += 1
            continue
        i = tool_id(t)
        if i not in ids:
            ids.append(i)
            names.append(text(getattr(t, "Name", "")))
    if not jobs:
        kind = "note"
    elif notool:
        kind = "notool"
    elif len(ids) > 1:
        kind = "mixed"
    else:
        kind = "one"
    return dict(name=text(cj.Name), uuid=text(getattr(cj, "UUID", "")), joblist=joblist_name, kind=kind,
                jobs=len(jobs), tools=ids, tool_names=names, obj=cj)


# ---------------- the plan ----------------
def plan(entries, part, machine, start, advance, other_names):
    """entries: classify() dicts in tree order; an entry with pick=False is left as it is.
    other_names: names of compound jobs in the document that this run does not rename.
    Returns dict(rows, renames, width, errors). Each row: entry + action + new name.
      action: rename | same (already has its new name) | note | mixed | notool | unpicked"""
    s, a = as_int(start), as_int(advance)
    todo = [e for e in entries if e["kind"] == "one" and e.get("pick", True)]
    last = s + a * (len(todo) - 1) if todo else s
    width = width_for(last)
    rows, errors, step = [], [], s
    for e in entries:
        r = dict(e)
        if e["kind"] != "one":
            r["action"], r["new"] = e["kind"], ""
        elif not e.get("pick", True):
            r["action"], r["new"] = "unpicked", ""
        else:
            r["step"] = step
            r["new"] = program_name(part, step, width, machine)
            r["action"] = "same" if r["new"] == e["name"] else "rename"
            step += a
        rows.append(r)
    if todo and last > MAX_STEP:
        errors.append("The last step would be %d (max %d). Lower the starting step or the advance." % (last, MAX_STEP))
    longest = max((len(r["new"]) for r in rows if r.get("new")), default=0)
    if longest > MAX_NAME:
        room = max_machine_len(part, width)
        errors.append("Names would be %d characters (max %d). %s" % (
            longest, MAX_NAME,
            "With this part number the machine can be at most %d characters." % room if room > 0
            else "The part number is too long for the rule."))
    else:
        bad = [r["new"] for r in rows if r.get("new") and not PROGRAM_RULE.match(r["new"])]
        if bad:
            errors.append("Names break the SINUMERIK program name rule: %s" % ", ".join(bad[:5]))
    taken = set(other_names)
    clash = [r["new"] for r in rows if r.get("new") and r["new"] in taken]
    if clash:
        errors.append("These names already belong to compound jobs this run does not rename: %s" % ", ".join(clash[:10]))
    renames = [r for r in rows if r["action"] == "rename"]
    return dict(rows=rows, renames=renames, width=width, errors=errors)


def row_text(r):
    """One line for the output window and the log."""
    tools = ",".join(r["tools"]) or "-"
    if r["action"] in ("rename", "same"):
        return "%-24s <- %s   (T %s, %d job%s)%s" % (r["new"], r["name"], tools, r["jobs"], "" if r["jobs"] == 1 else "s",
                                                     "   already named" if r["action"] == "same" else "")
    why = {"note": "note, skipped", "mixed": "NOT RENAMED: more than one tool (%s)" % tools,
           "notool": "NOT RENAMED: a job has no tool", "unpicked": "not picked, left as it is"}[r["action"]]
    return "%-24s    %s   %s" % ("", r["name"], why)


# ---------------- writing a name ----------------
def get_name(cj):
    return text(cj.Name)


def set_name(cj, new):
    """Sets a compound job name and reads it back. Tries the Name property (how part_wizard_1 names jobs), then the
    *CPJOBNAME setting. Returns (ok, how)."""
    try:
        cj.Name = new
        if get_name(cj) == new:
            return True, "Name"
    except Exception as e:
        how_err = "Name: %s" % e
    else:
        how_err = "Name: did not change"
    try:
        cj.SetCfgParameters({"*CPJOBNAME": new})
        cfg = cj.GetCfgParameters()
        if get_name(cj) == new or text(cfg.get("*CPJOBNAME")) == new:
            return True, "*CPJOBNAME"
        return False, how_err + "; *CPJOBNAME: did not change"
    except Exception as e:
        return False, how_err + "; *CPJOBNAME: %s" % e
