# go_to_machine.py - hyperMILL 35
# Checks the B programs of a joblist and posts them, then writes the B program list for the SINUMERIK generator.
# Screen: Joblist (one or all), Part number, Machine (defaults: the last B program rename), Action:
#   Check only      lists every B program as OK or FAIL with the reason; posts and writes nothing
#   Check and post  the same check, then posts with JobListSet.CalculateNC([compound job UUIDs]) and writes the list
# A B program is a compound job named B_<part>_<step>_<machine> (b_program_rename). It passes when every job in it:
#   is calculated (POFStatus UP_TO_DATE), has no errors (Status not ERRORS), and has been run through Simulation Center
#   without a collision since its last change (tool_library\release_check.py: POF header toolpath id -> POF\<id>.ccrpt
#   "CC_RESULT 1").
# When B programs fail: a warning with the list, then Post: No - post nothing / Post all / Post only the ones that pass.
# Stops without posting when a step number is used twice. Warns about names over 24 characters.
# After posting (everything except the NC files goes into the "go to machine" folder in the document folder;
# if it cannot be written: C:\Users\Public\Documents\OPEN MIND):
#   - the NC files written or updated (document folder and its NC folder, before / after)
#   - when only some B programs were posted: B program list and tool sheet: Only the posted ones / All B programs
#   - <document>_B_PROGRAMS.json / .csv (tool_library\B_PROGRAM_LIST_FORMAT.txt) for the generator's Import B list;
#     B programs left out are listed in it as "not posted"; for every posted B program the NC file is read:
#     radius_comp = G41/G42 found (CMC radius wear needs cutter compensation), r_params = R parameters it uses
#     (the generator keeps its CMC R blocks clear of them), cycle800 = the B program's CYCLE800 plane when it has
#     exactly one ("" = none = nest face; several, or only a turning-tool alignment: cycle800_note SEVERAL / TURNING),
#     offered by the generator as the probe swivel for the probe step and CMC
#   - the tool sheet <document>_<joblist>_tool_order.csv: the columns and catalog lookup of the installed
#     tool_order_list script (tool_order_list.py: catalog, tool_row), one row per tool of those B programs,
#     "Toolpath names" = <B program>: <toolpath>
#   - "Tool load MDA" ticked (first screen, on by default): <DOCUMENT>_TOOL_LOAD.MPF from the installed tool_load_mda
#     script for the tools of those B programs: sisters and tool life per tool (remembered per tool ID), NEWT per sister.
#     Tools of B programs that count with SETPIECE are marked "tool life (SETPIECE)"; left blank they get a warning,
#     because the control only counts pieces with tool life monitoring ($TC_TP9=2, $TC_MOP13 / $TC_MOP4).
# Log: C:\Users\Public\Documents\OPEN MIND\go_to_machine_log.txt
import os, re, csv, json, time, tempfile, traceback, datetime, importlib.util

PY_DIR   = r"C:\Users\Public\Documents\OPEN MIND\python"
OUT_DIR  = r"C:\Users\Public\Documents\OPEN MIND"
HERE     = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.path.join(PY_DIR, "go_to_machine")
LIB_DIRS = (os.path.join(PY_DIR, "tool_library"), os.path.join(HERE, "..", "tool_library"))
TOL_FILES = (os.path.join(PY_DIR, "tool_order_list", "tool_order_list.py"), os.path.join(HERE, "..", "tool_order_list", "tool_order_list.py"))
TLM_FILES = (os.path.join(PY_DIR, "tool_load_mda", "tool_load_mda.py"), os.path.join(HERE, "..", "tool_load_mda", "tool_load_mda.py"))
MDA_LABEL = "Tool load MDA"
OUT_SUB  = "go to machine"          # folder in the document folder for the B program list, tool sheet and MDA
TITLE    = "Go to machine"
ACTIONS  = ["Check only", "Check and post"]
MAX_BOX_LINES = 30
BOX_WIDTH = 90
NC_EXT   = (".mpf", ".spf", ".nc", ".h", ".txt", ".ptp", ".cnc", ".iso", ".min")

lines = []


def log(*a):
    lines.append(" ".join(str(x) for x in a))


def out_dir():
    return OUT_DIR if os.path.isdir(OUT_DIR) else tempfile.gettempdir()


def lib_file(name):
    for d in LIB_DIRS:
        p = os.path.normpath(os.path.join(d, name))
        if os.path.exists(p):
            return p
    return None


def load_lib(name, modname):
    """Library by file path, fresh every run (hyperMILL keeps imported modules between runs)."""
    p = lib_file(name)
    if p is None:
        raise RuntimeError(name + " not found in tool_library")
    spec = importlib.util.spec_from_file_location(modname, p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    m.LOADED_FROM = p
    return m


def _gui():
    import om.cad.gui as g
    return g


def info(text_):
    import textwrap
    g = _gui()
    rows = []
    for ln in str(text_).split("\n"):
        rows += textwrap.wrap(ln, BOX_WIDTH, subsequent_indent="   ", break_long_words=False, break_on_hyphens=False) or [""]
    if len(rows) > MAX_BOX_LINES:
        rows = rows[:MAX_BOX_LINES - 1] + ["... full list in the output window and go_to_machine_log.txt"]
    g.ShowMessageBox(g.MessageBoxType.INFORMATION, TITLE, "\n".join(rows))


def output(text_):
    g = _gui()
    try:
        g.CleanOutput(g.UIOutputWindow.ALL)
        g.WriteToOutput(text_, g.UIOutputWindow.ALL)
        g.ProcessEvents()
    except Exception:
        pass


def pick_index(v, options):
    if isinstance(v, int) and not isinstance(v, bool):
        return v if 0 <= v < len(options) else 0
    return options.index(v) if v in options else 0


def val(x):
    return x() if callable(x) else x


def last_rename():
    try:
        with open(os.path.join(out_dir(), "b_program_rename_last.json"), encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def writable(folder):
    try:
        p = os.path.join(folder, "go_to_machine_write_test.tmp")
        with open(p, "w") as f:
            f.write("x")
        os.remove(p)
        return True
    except Exception:
        return False


def snapshot(folder):
    """{path: (mtime, size)} of the document folder and its NC folder (where the post writes)."""
    snap = {}
    for d in (folder, os.path.join(folder, "NC")):
        try:
            for n in os.listdir(d):
                p = os.path.join(d, n)
                if os.path.isfile(p):
                    st = os.stat(p)
                    snap[p] = (st.st_mtime, st.st_size)
        except Exception:
            pass
    return snap


def stem(p):
    return os.path.splitext(os.path.basename(p))[0].lower()


def choose(title, label, opts):
    g = _gui()
    dlg = g.InputDialog(title)
    dlg.AddDropDown(label, opts, defaultIndex=0)
    ok, v = dlg.Show()
    return pick_index(v.get(label), opts) if ok else 0


# ---------------- check ----------------
def collect(bp, rc, chosen, part, machine, folder):
    """B programs (in tree order) with their check, things left out, problems."""
    progs, left, problems, seen = [], [], [], {}
    cache = rc.Ccrpt()
    for jl_name, entries in chosen:
        for e in entries:
            if e["kind"] == "note":
                continue
            if e["kind"] in ("mixed", "notool"):
                left.append("%s  (%s)" % (e["name"], "more than one tool" if e["kind"] == "mixed" else "a job has no tool"))
                continue
            st = bp.step_of(e["name"], part, machine)
            if st is None:
                left.append("%s  (not a B program name for part %s machine %s)" % (e["name"], part, machine or "-"))
                continue
            if st in seen:
                problems.append("Step %d is used twice: %s and %s" % (st, seen[st], e["name"]))
                continue
            seen[st] = e["name"]
            c = rc.check_compound(e["obj"], folder, cache)
            progs.append(dict(step=st, name=e["name"], joblist=jl_name, obj=e["obj"], uuid=str(val(getattr(e["obj"], "UUID", ""))),
                              ok=c["ok"], jobs=c["jobs"], failed=c["failed"], long=bp.too_long(e["name"])))
    return progs, left, problems


def fail_lines(fails, r_collision):
    """The fail list for the pop-up. B programs that fail only because their Simulation Center run had a collision are
    one line per run: hyperMILL marks every toolpath of a run with the run's result, so the file can't say which one
    collided. Every other failure is one line per B program. (The output window keeps the full list.)"""
    runs, others = {}, []
    for p in fails:
        if p["failed"] and all(j["reason"] == r_collision for j in p["failed"]):
            key = ", ".join(sorted(set(j.get("run") or "time unknown" for j in p["failed"])))
            runs.setdefault(key, []).append(p["name"])
        else:
            others.append(p)
    out = []
    for key, names in runs.items():
        out.append("Simulation Center run of %s had a collision: %d B program%s marked (%s)." % (
            key, len(names), "" if len(names) == 1 else "s", names[0] if len(names) == 1 else names[0] + " ... " + names[-1]))
        out.append("  hyperMILL marks every toolpath of a run; Simulation Center shows which one collided.")
        out.append("  Simulate each B program on its own so a collision marks only that one.")
    if others:
        out.append("Fail:")
        for p in others:
            why = sorted(set(j["reason"] for j in p["failed"])) or ["no jobs"]
            out.append("  %s  %s" % (p["name"], "; ".join(why)))
    return out


def report_lines(progs, left, problems, head):
    rep = [head, ""]
    for p in progs:
        rep.append("  %-4s %-26s %d job%s%s" % ("OK" if p["ok"] else "FAIL", p["name"], len(p["jobs"]),
                                                "" if len(p["jobs"]) == 1 else "s", "   NAME OVER 24 CHARACTERS" if p["long"] else ""))
        for j in p["failed"]:
            rep.append("         %s: %s" % (j["name"], j["reason"]))
        if not p["jobs"]:
            rep.append("         no jobs")
    if left:
        rep += ["", "Not B programs (not posted):"] + ["  " + x for x in left]
    if problems:
        rep += [""] + ["PROBLEM: " + x for x in problems]
    return rep


# ---------------- tool sheet ----------------
def tool_sheet(progs, folder, out_folder, base, label):
    """<base>_<label>_tool_order.csv from the installed tool_order_list script. Returns (path, rows, missing) or a
    reason string when it was not written."""
    p = next((os.path.normpath(f) for f in TOL_FILES if os.path.exists(os.path.normpath(f))), None)
    if p is None:
        return "tool_order_list.py not found in %s" % os.path.join(PY_DIR, "tool_order_list")
    spec = importlib.util.spec_from_file_location("hm_tool_order_list", p)
    tol = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tol)
    log("tool_order_list:", p)
    used, order = {}, []
    for pr in progs:
        for j in list(pr["obj"].GetJobs()):
            try:
                t = j.GetTool()
            except Exception:
                t = None
            if t is None:
                continue
            u = str(val(getattr(t, "UUID", "")) or val(getattr(t, "Name", ""))).strip("{}").upper()
            if u not in used:
                used[u] = (t, [])
                order.append(u)
            used[u][1].append("%s: %s" % (pr["name"], str(val(getattr(j, "Name", "")))))
    if not order:
        return "no tools in those B programs"
    cat = tol.catalog()
    rows = []
    for u in order:
        t, jobs = used[u]
        try:
            rows.append(tol.tool_row(t, jobs, cat))
        except Exception:
            log("tool sheet row FAILED:", val(getattr(t, "Name", "?")), traceback.format_exc()[-300:])
    for ln in getattr(tol, "lines", []):
        log("  tool_order_list:", ln)
    if not rows:
        return "no tool row could be read"
    try:
        rows.sort(key=lambda r: (r.get("Manufacturer", ""), r.get("Tool type", ""), tol._f(r.get("Diameter (in)")) or 0, r.get("Designation", "")))
    except Exception:
        pass
    path = os.path.join(out_folder, "%s_%s_tool_order.csv" % (base, re.sub(r"[^A-Za-z0-9_-]", "_", label)))
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    missing = [r.get("Designation", "?") for r in rows if r.get("In tool_library", "yes") != "yes"]
    log("tool sheet:", path, "|", len(rows), "tools |", len(missing), "not in tool_library:", missing)
    return path, rows, missing


# ---------------- tool load MDA ----------------
def tool_mda(progs, setpiece_ids, folder, doc_name, label):
    """<DOCUMENT>_TOOL_LOAD.MPF with the installed tool_load_mda script. Returns message lines."""
    p = next((os.path.normpath(f) for f in TLM_FILES if os.path.exists(os.path.normpath(f))), None)
    if p is None:
        return ["", "Tool load MDA not written: tool_load_mda.py not found in %s" % os.path.join(PY_DIR, "tool_load_mda")]
    spec = importlib.util.spec_from_file_location("hm_tool_load_mda", p)
    tlm = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tlm)
    log("tool_load_mda:", p)
    picked, seen = [], set()
    for pr in progs:
        for j in list(pr["obj"].GetJobs()):
            try:
                t = j.GetTool()
            except Exception:
                t = None
            if t is None:
                continue
            u = str(val(getattr(t, "UUID", "")) or val(getattr(t, "Name", "")))
            if u not in seen:
                seen.add(u)
                picked.append(t)
    tools, ids, no_gage = [], set(), []
    for t in picked:
        d = tlm.tool_data(t)
        if d["id"] in ids:
            continue
        if d["gage"] is None:
            no_gage.append(d["id"])
            continue
        ids.add(d["id"])
        tools.append(d)
    for ln in getattr(tlm, "lines", []):
        log("  tool_load_mda:", ln)
    out = [""]
    if not tools:
        return out + ["Tool load MDA not written: no tool could be read (no gage length: %s)" % (", ".join(no_gage) or "-")]
    tools.sort(key=lambda d: (tlm._f(d["id"]) is None, tlm._f(d["id"]) or 0, d["id"]))
    need = set(i for i in setpiece_ids if i in ids)
    counts = tlm.ask_counts(tools, tlm.load_last(), need)
    if counts is None:
        log("tool load MDA cancelled at sisters / tool life")
        return out + ["Tool load MDA cancelled: not written."]
    tlm.save_last(counts)
    text, made = tlm.program(tools, counts, doc_name, "go_to_machine " + label)
    path = tlm.write_program(text, folder, doc_name)
    extra = sum(counts.get(t["id"], (0, 0))[0] for t in tools)
    blank = [t["id"] for t in tools if t["id"] in need and counts.get(t["id"], (0, 0))[1] == 0]
    log("tool load MDA:", path, "|", made, "tool entries |", len(tools), "tools |", extra, "extra sisters | no gage:", no_gage, "| SETPIECE without tool life:", blank)
    out += ["Tool load MDA: %d tool%s + %d extra sister%s (%d entr%s) - paste into MDA, cycle start:" % (
        len(tools), "" if len(tools) == 1 else "s", extra, "" if extra == 1 else "s", made, "y" if made == 1 else "ies"), "  " + path]
    if no_gage:
        out.append("  left out (no gage length): " + ", ".join(no_gage))
    if blank:
        out.append("  WARNING - SETPIECE counts these tools but no tool life was entered (the control will not count them): " + ", ".join(blank))
    return out


# ---------------- posted NC file facts (for the generator's CMC checks) ----------------
_G4142 = re.compile(r"(?<![A-Z0-9_$])G4[12](?![0-9])")
_RNUM = re.compile(r"(?<![A-Z0-9_$.])R([0-9]+)(?![0-9])")
_RIND = re.compile(r"(?<![A-Z0-9_$.])R\[")


_C800 = re.compile(r"^(?:N[0-9]+\s+)?(CYCLE800\s*\((.*)\))\s*$", re.I)
_PLANE_ARGS = (1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)    # _TC _MODE _X0.._Z0 _A.._C _X1.._Z1 (0-based)


def _split_args(t):
    out, cur, ins, depth = [], "", False, 0
    for ch in t:
        if ch == '"':
            ins = not ins
        if not ins and ch in "([":
            depth += 1
        if not ins and ch in ")]":
            depth -= 1
        if not ins and depth == 0 and ch == ",":
            out.append(cur.strip())
            cur = ""
            continue
        cur += ch
    out.append(cur.strip())
    return out


def _num(x):
    try:
        return round(float(x), 6) if x != "" else 0.0
    except ValueError:
        return x


def plane_of(line):
    """None for CYCLE800() (deselect); ("TURNING", line) for a tool alignment (_ST hundreds 2 or 3);
    (key, line) for a plane - the key leaves out retraction, direction and display mode."""
    m = _C800.match(line.strip())
    if not m or not m.group(2).strip():
        return None
    args = _split_args(m.group(2))
    args += [""] * (16 - len(args))
    try:
        st = abs(int(float(args[2] or 0)))
    except ValueError:
        st = 0
    if (st // 100) % 10 in (2, 3):
        return ("TURNING", m.group(1))
    return (tuple(args[1] if i == 1 else _num(args[i]) for i in _PLANE_ARGS), m.group(1))


def nc_facts(p):
    """(radius_comp, sorted R numbers, indirect R used, CYCLE800 planes {key: first line}, turning alignment seen)
    of one NC file: comments (;) and strings left out."""
    comp, rs, ind, planes, turning = False, set(), False, {}, False
    with open(p, encoding="latin-1", errors="replace") as f:
        for raw in f:
            pl = plane_of(raw.split(";", 1)[0])
            if pl and pl[0] == "TURNING":
                turning = True
            elif pl and pl[0] not in planes:
                planes[pl[0]] = pl[1]
            code = re.sub(r'"[^"]*"', '""', raw.upper().split(";", 1)[0])
            if _G4142.search(code):
                comp = True
            rs.update(int(m) for m in _RNUM.findall(code))
            if _RIND.search(code):
                ind = True
    return comp, sorted(rs), ind, planes, turning


def add_nc_facts(steps, found):
    """radius_comp / r_params on the B list steps whose NC file was written now. Returns message lines."""
    out, comp_no, with_r, ind, several, turn = [], [], [], [], [], []
    for s in steps:
        p = found.get(str(s.get("program", "")).lower())
        if not p:
            continue
        try:
            comp, rs, indirect, planes, turning = nc_facts(p)
        except Exception as e:
            log("NC read failed:", p, e)
            continue
        s["radius_comp"], s["r_params"] = comp, rs
        if len(planes) == 1:
            s["cycle800"] = list(planes.values())[0]
        elif len(planes) > 1:
            s["cycle800_note"] = "SEVERAL"
            several.append(s["program"])
        elif turning:
            s["cycle800_note"] = "TURNING"
            turn.append(s["program"])
        else:
            s["cycle800"] = ""
        log("NC facts:", s["program"], "| G41/G42:", comp, "| R:", rs, "| indirect R:", indirect,
            "| CYCLE800 planes:", list(planes.values()), "| turning alignment:", turning)
        if not comp:
            comp_no.append(s["program"])
        if rs:
            with_r.append("%s (R%s)" % (s["program"], ", R".join(str(r) for r in rs[:6]) + (" ..." if len(rs) > 6 else "")))
        if indirect:
            ind.append(s["program"])
    if with_r:
        out.append("R parameters in posted B programs (kept out of CMC R blocks): " + "; ".join(with_r))
    if ind:
        out.append("WARNING - R[...] with a computed number (cannot be checked): " + ", ".join(ind))
    if comp_no:
        out.append("No G41/G42 (CMC radius wear has no effect there): " + ", ".join(comp_no[:8]) + (" ..." if len(comp_no) > 8 else ""))
    if several:
        out.append("Several CYCLE800 planes, none stored (pick the probe plane in the generator): " + ", ".join(several))
    if turn:
        out.append("Only a turning-tool CYCLE800, no plane stored (pick the probe plane in the generator): " + ", ".join(turn))
    return out


# ---------------- post ----------------
def post(model, targets, folder):
    """CalculateNC with the compound job UUIDs; returns (returned value or error text, ok, written files)."""
    uuids = [p["uuid"] for p in targets]
    log("CalculateNC uuids:", uuids)
    before = snapshot(folder)
    t = time.time()
    try:
        res = model.JobListSet.CalculateNC(uuids)
        ok = True
    except Exception as e:
        res, ok = "%s: %s" % (type(e).__name__, e), False
    log("CalculateNC returned: %r  (%.1f s)" % (res, time.time() - t))
    after = snapshot(folder)
    written = sorted(p for p in after if before.get(p) != after[p] and p.lower().endswith(NC_EXT))
    for p in written:
        log("  written:", p)
    return res, ok, written


def run():
    try:
        bp = load_lib("b_programs.py", "hm_b_programs")
        rc = load_lib("release_check.py", "hm_release_check")
        log(TITLE, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "| b_programs", bp.VERSION, "| release_check", rc.VERSION)
        import om
        doc = om.Application().CurrentDocument
        if doc is None:
            info("No document open."); return
        path = str(val(doc.FullPath))
        folder = os.path.dirname(path)
        log("document:", path)
        model = doc.CamModel
        inch = bool(val(model.IsInchMode))
        lists = list(model.JobListSet.GetJobLists())
        names = [str(val(jl.Name)) for jl in lists]
        if not names:
            info("No joblists in this document."); return
        scopes = names + (["All joblists"] if len(names) > 1 else [])
        last = last_rename()
        g = _gui()
        dlg = g.InputDialog(TITLE)
        dlg.AddDropDown("Joblist", scopes, defaultIndex=0)
        dlg.AddText("Part number", defaultValue=last.get("part", ""))
        dlg.AddText("Machine", defaultValue=last.get("machine", ""))
        dlg.AddDropDown("Action", ACTIONS, defaultIndex=0)
        dlg.AddBool(MDA_LABEL, defaultValue=True)
        ok, v = dlg.Show()
        if not ok:
            log("cancelled"); return
        scope = scopes[pick_index(v.get("Joblist"), scopes)]
        part, machine = str(v.get("Part number", "")).strip(), str(v.get("Machine", "")).strip()
        action = pick_index(v.get("Action"), ACTIONS)
        want_mda = bool(v.get(MDA_LABEL, True))
        log("joblist:", scope, "| part:", part, "| machine:", machine or "-", "| action:", ACTIONS[action], "| tool load MDA:", want_mda)
        err = bp.input_errors(part, machine, "10", "10")
        if err:
            info("Fix these first:\n\n" + "\n".join(err)); return
        chosen = [(n, [bp.classify(cj, n) for cj in bp.compound_jobs(jl)]) for jl, n in zip(lists, names)
                  if scope == "All joblists" or n == scope]
        progs, left, problems = collect(bp, rc, chosen, part, machine, folder)
        npass = sum(1 for p in progs if p["ok"])
        nfail = len(progs) - npass
        rep = report_lines(progs, left, problems, "%s  %s  part %s  machine %s  %s" % (TITLE, scope, part, machine or "-", ACTIONS[action]))
        for ln in rep:
            log(ln)
        output("\n".join(rep))
        if not progs:
            info("No compound job in %s is named B_%s_<step>%s. Run b_program_rename first." % (
                scope, part, ("_" + machine) if machine else "")); return
        summary = ["%d B program%s: %d pass, %d fail." % (len(progs), "" if len(progs) == 1 else "s", npass, nfail)]
        fails = [p for p in progs if not p["ok"]]
        if fails:
            summary.append("")
            summary += fail_lines(fails, rc.R_COLLISION)
        longs = [p["name"] for p in progs if p["long"]]
        if longs:
            summary += ["", "WARNING - names over 24 characters (the generator refuses them):"] + ["  " + n for n in longs]
        if left:
            summary += ["", "%d compound job%s not posted (not B programs): see the output window." % (len(left), "" if len(left) == 1 else "s")]
        twice = [x for x in problems if "used twice" in x]
        if twice:
            info("\n".join(summary + ["", "Nothing posted. Fix these first (run b_program_rename):"] + twice)); return
        if action == 0:
            info("\n".join(summary + ["", "Check only: nothing posted, nothing written."])); return

        # ---- post ----
        if nfail:
            info("WARNING: %d of %d B programs fail the check.\n\n" % (nfail, len(progs)) + "\n".join(summary[2:] if len(summary) > 2 else summary))
            opts = ["No - post nothing", "Post all %d (%d fail the check)" % (len(progs), nfail)]
            if npass:
                opts.append("Post only the %d that pass" % npass)
            pick = choose(TITLE + " | WARNING: %d fail the check" % nfail, "Post", opts)
            if pick == 0:
                log("not posted (warning answered No)"); info("Nothing posted."); return
            targets = progs if pick == 1 else [p for p in progs if p["ok"]]
            if pick == 1:
                log("POSTED WITH FAILURES:", ", ".join(p["name"] for p in fails))
        else:
            pick = choose(TITLE + " | confirm", "Post", ["No - do not post", "Yes - post %d B program%s" % (len(progs), "" if len(progs) == 1 else "s")])
            if pick != 1:
                log("not posted (confirm answered No)"); info("Nothing posted."); return
            targets = progs
        res, ok, written = post(model, targets, folder)
        found = {stem(p): p for p in written}
        missing = [p["name"] for p in targets if p["name"].lower() not in found]
        msg = []
        if not ok:
            msg.append("Posting failed: %s" % res)
        else:
            msg.append("Posted %d B program%s (CalculateNC returned %r)." % (len(targets), "" if len(targets) == 1 else "s", res))
        msg.append("NC files written or updated: %d" % len(written))
        msg += ["  " + os.path.relpath(p, folder) for p in written[:12]]
        if missing:
            msg += ["", "No NC file found for:"] + ["  " + n for n in missing]
        if pick == 1 and nfail:
            msg += ["", "Posted although %d fail the check." % nfail]
        # ---- what the B program list and the tool sheet hold ----
        scope_progs = targets
        if len(targets) != len(progs):
            inc = ["Only the %d posted" % len(targets), "All %d B programs" % len(progs)]
            if choose(TITLE + " | B program list and tool sheet", "Include", inc) == 1:
                scope_progs = progs
            log("B program list and tool sheet:", "all B programs" if scope_progs is progs else "only the posted ones")
        keep = set(p["name"] for p in scope_progs)
        dropped = [p for p in progs if p["name"] not in keep]
        drop_names = set(p["name"] for p in dropped)
        dest = os.path.join(folder, OUT_SUB) if folder else ""
        if dest:
            try:
                os.makedirs(dest, exist_ok=True)
            except Exception as e:
                log("cannot create", dest, e)
        if not dest or not writable(dest):
            dest = out_dir()
        log("output folder:", dest)
        base = os.path.splitext(path.replace("\\", "/").split("/")[-1])[0] or "document"
        # ---- B program list for the generator ----
        rules_path = lib_file("brk_rules.csv")
        rules = bp.load_rules(rules_path) if rules_path else []
        chosen_x = [(n, [e for e in es if e["name"] not in drop_names]) for n, es in chosen]
        data, xproblems = bp.build_export(chosen_x, part, machine, inch, rules, path,
                                          datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        for p in dropped:
            data["refused"].append(dict(name=p["name"], joblist=p["joblist"], reason="not posted: failed the go-to-machine check"))
        try:
            facts = add_nc_facts(data["steps"], found)
        except Exception:
            log("NC facts FAILED:", traceback.format_exc())
            facts = []
        if data["steps"] and not any("used twice" in x for x in xproblems):
            pj, pc = bp.write_export(data, dest, base)
            log("B program list:", pj, "|", pc)
            msg += ["", "B program list for the generator (Import B list): %d B program%s" % (len(data["steps"]), "" if len(data["steps"]) == 1 else "s"), "  " + pj]
            msg += ["  " + x for x in facts]
        for x in xproblems:
            log("export:", x)
        # ---- tool sheet ----
        try:
            ts = tool_sheet(scope_progs, folder, dest, base, "all" if scope == "All joblists" else scope)
        except Exception:
            log("tool sheet FAILED:", traceback.format_exc())
            ts = "failed (see go_to_machine_log.txt)"
        if isinstance(ts, tuple):
            tp, trows, tmissing = ts
            msg += ["", "Tool sheet: %d tool%s" % (len(trows), "" if len(trows) == 1 else "s"), "  " + tp]
            if tmissing:
                msg.append("  not in tool_library: " + ", ".join(tmissing[:8]))
        else:
            msg += ["", "Tool sheet not written: " + ts]
        # ---- tool load MDA ----
        if want_mda:
            setpiece_ids = set(s["tool"] for s in data["steps"] if s.get("setpiece"))
            try:
                msg += tool_mda(scope_progs, setpiece_ids, dest, base, "all" if scope == "All joblists" else scope)
            except Exception:
                log("tool load MDA FAILED:", traceback.format_exc())
                msg += ["", "Tool load MDA failed (see go_to_machine_log.txt)."]
        for ln in msg:
            log(ln)
        info("\n".join(msg))
    except Exception:
        log("FAILED:", traceback.format_exc())
        try:
            info("Failed. See go_to_machine_log.txt.")
        except Exception:
            pass
    finally:
        try:
            with open(os.path.join(out_dir(), "go_to_machine_log.txt"), "w", encoding="utf-8") as f:
                f.write("\n".join(lines) + "\n")
        except Exception:
            pass


if __name__ == "__main__":
    run()
