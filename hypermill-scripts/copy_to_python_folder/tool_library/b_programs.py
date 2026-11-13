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
    ids, names, notool, first_tool = [], [], 0, None
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
            if first_tool is None:
                first_tool = t
    if not jobs:
        kind = "note"
    elif notool:
        kind = "notool"
    elif len(ids) > 1:
        kind = "mixed"
    else:
        kind = "one"
    purposes = [job_purpose(j) for j in jobs]
    return dict(name=text(cj.Name), uuid=text(getattr(cj, "UUID", "")), joblist=joblist_name, kind=kind,
                jobs=len(jobs), tools=ids, tool_names=names, obj=cj, tool_obj=first_tool,
                purpose=compound_purpose(purposes), purposes=purposes)


# ---------------- roughing / finishing from the stock to leave ----------------
# A job with stock to leave (allowance) is roughing; zero stock to leave is finishing; a job without allowance settings
# (drilling, tapping, reaming ...) has no purpose. Keys from tool_library\job_settings.json: *AUFMASS (stock to leave),
# *AUFMASS_Z (axial), *AUFMASS_HORI (floors). Finishing ops there all use 0; roughing 0.0118-0.0197 in.
ALLOWANCE_KEYS = ("*AUFMASS", "*AUFMASS_Z", "*AUFMASS_HORI")
FINISH_MAX_STOCK = 0.0001       # stock to leave at or below this (document units) counts as zero = finishing


def job_purpose(job):
    try:
        cfg = job.GetCfgParameters()
    except Exception:
        return ""
    vals = []
    for k in ALLOWANCE_KEYS:
        try:
            v = float(str(cfg.get(k, "")).strip())
        except Exception:
            continue
        vals.append(abs(v))
    if not vals:
        return ""
    return "finish" if max(vals) <= FINISH_MAX_STOCK else "rough"


def compound_purpose(purposes):
    """finish when any job finishes (the tighter break tolerance), rough when any roughs, else ''."""
    if "finish" in purposes:
        return "finish"
    if "rough" in purposes:
        return "rough"
    return ""


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


# ======================================================================================================================
# B program list export (for the SINUMERIK generator's "Import B list"; the go-to-machine script calls build_export)
# File format: B_PROGRAM_LIST_FORMAT.txt (tool_library and the generator folder hold the same text).
# ======================================================================================================================
import csv
import json
import os
import tempfile
import xml.etree.ElementTree as ET

FORMAT = "SINUMERIK_B_PROGRAM_LIST"
FORMAT_VERSION = 1
MM = 25.4
RULE_COLUMNS = ("tool_type", "purpose", "dia_min", "dia_max", "units", "brk_check", "brk_tol", "measure", "measure_always",
                "max_brk", "life", "setpiece", "note")


def step_of(name, part, machine):
    """Step number from a B program name with this part and machine, else None."""
    m = re.match(r"^B_%s_(\d{3,4})%s$" % (re.escape(part), ("_" + re.escape(machine)) if machine else ""), name)
    return int(m.group(1)) if m else None


def _f(x):
    try:
        return float(str(x).strip())
    except Exception:
        return None


def tool_info(tool, inch):
    """Type and diameter from the tool's own export (same reading as tool_load_mda), diameter in document units."""
    d = dict(type="", dia=None)
    name = re.sub(r"[^A-Za-z0-9_.-]", "_", text(getattr(tool, "Name", "")) or "tool")[:60]
    p = os.path.join(tempfile.gettempdir(), "b_programs_%s.omtdx" % name)
    try:
        if not tool.Export(p):
            return d
        root = ET.parse(p).getroot()
        t = root.find(".//tools/tool")
        if t is not None:
            d["type"] = t.get("type", "")
            u = t.find("param[@name='lengthOfUnit']")
            dia = t.find("param[@name='toolDiameter']")
            if dia is not None and _f(dia.get("value")) is not None:
                v = _f(dia.get("value"))
                src_mm = str(u.get("value") if u is not None else "inch").lower().startswith("m")
                d["dia"] = (v / MM if src_mm else v) if inch else (v if src_mm else v * MM)
    except Exception:
        pass
    finally:
        try:
            os.remove(p)
        except Exception:
            pass
    if not d["type"]:
        d["type"] = text(getattr(tool, "Type", "")).split(".")[-1].split(":")[0]
    return d


def load_rules(path):
    """brk_rules.csv -> list of dicts (UTF-8, # lines are comments)."""
    rows = []
    with open(path, encoding="utf-8-sig", newline="") as f:
        lines_ = [ln for ln in f if ln.strip() and not ln.lstrip().startswith("#")]
    for r in csv.DictReader(lines_):
        rows.append({k: (r.get(k) or "").strip() for k in RULE_COLUMNS})
    return rows


def _flag(v, default):
    v = str(v).strip().lower()
    if v in ("1", "yes", "y", "true", "on"):
        return True
    if v in ("0", "no", "n", "false", "off"):
        return False
    return default


def match_rule(rules, tool_type, dia, inch, purpose=""):
    """First row whose tool_type matches (* = any), whose purpose matches (rough / finish / none; * or blank = any)
    and whose diameter range holds dia (in the row's units)."""
    for r in rules:
        rt = r["tool_type"]
        if rt != "*" and rt.lower() != str(tool_type).lower():
            continue
        rp = r.get("purpose", "").lower()
        if rp not in ("", "*") and rp != (purpose or "none"):
            continue
        row_inch = not r["units"].upper().startswith("M")
        d = dia                                   # document units
        if d is not None and inch and not row_inch:
            d = d * MM                            # inch document, metric row
        elif d is not None and not inch and row_inch:
            d = d / MM                            # metric document, inch row
        lo, hi = _f(r["dia_min"]), _f(r["dia_max"])
        if d is not None and ((lo is not None and d < lo) or (hi is not None and d >= hi)):
            continue
        if d is None and (lo is not None or hi is not None):
            continue
        return r
    return None


def presets(rule, inch):
    """Generator step flags from a rule row; tolerance in document units, blank stays blank."""
    if rule is None:
        return dict(brk=True, brk_tol="", meas=True, meas_always=False, max_brk=2, life=1, setpiece=True, rule="none")
    tol = _f(rule["brk_tol"])
    if tol is not None:
        row_inch = not rule["units"].upper().startswith("M")
        if row_inch and not inch:
            tol = tol * MM
        elif inch and not row_inch:
            tol = tol / MM
        tol = ("%.4f" if inch else "%.3f") % tol
    life = _f(rule["life"])
    mb = _f(rule["max_brk"])
    return dict(brk=_flag(rule["brk_check"], True), brk_tol=tol if tol is not None else "",
                meas=_flag(rule["measure"], True), meas_always=_flag(rule["measure_always"], False),
                max_brk=int(mb) if mb else 2, life=int(life) if life else 1, setpiece=_flag(rule["setpiece"], True),
                rule=("%s %s %s-%s %s" % (rule["tool_type"], rule.get("purpose", "") or "*", rule["dia_min"] or "", rule["dia_max"] or "", rule["note"])).strip())


def build_export(chosen, part, machine, inch, rules, document, created):
    """chosen: [(joblist name, classify() entries in tree order)]. Returns (data, problems)."""
    steps, refused, problems, seen = [], [], [], {}
    for jl_name, entries in chosen:
        for e in entries:
            if e["kind"] == "note":
                continue
            if e["kind"] in ("mixed", "notool"):
                refused.append(dict(name=e["name"], joblist=jl_name,
                                    reason="more than one tool (%s)" % ",".join(e["tools"]) if e["kind"] == "mixed"
                                    else "a job has no tool"))
                continue
            st = step_of(e["name"], part, machine)
            if st is None:
                refused.append(dict(name=e["name"], joblist=jl_name, reason="not a B program name for part %s machine %s" % (part, machine or "-")))
                continue
            if st in seen:
                problems.append("Step %d is used twice: %s and %s" % (st, seen[st], e["name"]))
                continue
            seen[st] = e["name"]
            tool = e.get("tool_obj")
            ti = tool_info(tool, inch) if tool is not None else dict(type="", dia=None)
            rule = match_rule(rules, ti["type"], ti["dia"], inch, e.get("purpose", ""))
            p = presets(rule, inch)
            tid = e["tools"][0]
            if len(tid) > 25 or '"' in tid:
                problems.append("Tool ID %r of %s is longer than 25 characters or has a quote" % (tid, e["name"]))
            steps.append(dict(step=st, program=e["name"], tool=tid, tool_name=(e["tool_names"] or [""])[0],
                              tool_type=ti["type"], diameter=round(ti["dia"], 4) if ti["dia"] is not None else None,
                              jobs=e["jobs"], purpose=e.get("purpose", ""), joblist=jl_name, brk=p["brk"], brk_tol=p["brk_tol"], meas=p["meas"],
                              meas_always=p["meas_always"], max_brk=p["max_brk"], life=p["life"], setpiece=p["setpiece"],
                              rule=p["rule"]))
    order = [s["step"] for s in steps]
    if order != sorted(order):
        problems.append("Steps are not in ascending tree order (the generator runs them in tree order).")
    data = dict(format=FORMAT, version=FORMAT_VERSION, created=created, source="hyperMILL b_programs.py " + VERSION,
                document=document, joblists=[c[0] for c in chosen], part=part, machine=machine,
                units="INCH" if inch else "METRIC", steps=steps, refused=refused)
    return data, problems


def write_export(data, folder, base):
    """<base>_B_PROGRAMS.json and .csv in folder. Returns the two paths."""
    pj = os.path.join(folder, base + "_B_PROGRAMS.json")
    pc = os.path.join(folder, base + "_B_PROGRAMS.csv")
    with open(pj, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=1)
    cols = ("step", "program", "tool", "tool_name", "tool_type", "diameter", "jobs", "purpose", "brk", "brk_tol", "meas",
            "meas_always", "max_brk", "life", "setpiece", "rule", "joblist")
    with open(pc, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(cols)
        for s in data["steps"]:
            w.writerow([s.get(c, "") for c in cols])
    return pj, pc
