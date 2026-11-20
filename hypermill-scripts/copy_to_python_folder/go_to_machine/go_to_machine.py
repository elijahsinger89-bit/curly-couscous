# go_to_machine.py - hyperMILL 35. The job-end menu: checks the B programs, posts them, writes what goes to the machine.
# Screen 1: Joblist (one or all), Part number, Machine (defaults: the last B program rename), Package:
#   Validation      bare minimum to prove the job: post, B program list, tool load MDA with NO sisters, order sheet
#                   (1 of each tool and holder), sister tool sheet to fill in during prove-out
#   Production      everything: post, B program list, tool load MDA WITH sisters and tool life, order sheet (1 + sisters),
#                   NC master setup sheet. Sisters / tool life come from the filled sister tool sheet (the newest one in
#                   go to machine\VALIDATION_*; its path can be changed). None found: stops before posting.
#   Pick functions  nothing ticked: tick what you want. Without a sister sheet the tool load MDA asks sisters on screens.
# Screen 2: the functions, ticked by the package (any can be unticked or ticked): Post the B programs, B program list,
#   Tool load MDA, Order sheet, Sister tool sheet, NC master setup sheet; Programmer (remembered); Sister sheet (not for
#   Validation). Nothing ticked = check only.
# A B program is a compound job named B_<part>_<step>_<machine> (b_program_rename). It passes when every job in it:
#   is calculated (POFStatus UP_TO_DATE), has no errors (Status not ERRORS), and has been run through Simulation Center
#   without a collision since its last change (tool_library\release_check.py: POF header toolpath id -> POF\<id>.ccrpt
#   "CC_RESULT 1").
# Posting: when B programs fail, a warning with the list, then Post: No - post nothing / Post all / Post only the ones
# that pass. Stops when a step number is used twice. Warns about names over 24 characters.
# Output (NC files stay where the post writes them): <document folder>\go to machine\VALIDATION_<date> or
# PRODUCTION_<date> (Pick functions: go to machine); if it cannot be written: C:\Users\Public\Documents\OPEN MIND.
#   - when only some B programs were posted: B program list and documents: Only the posted ones / All B programs
#   - <document>_B_PROGRAMS.json / .csv (tool_library\B_PROGRAM_LIST_FORMAT.txt) for the generator's Import B list;
#     B programs left out are listed in it as "not posted"; for every B program the NC file is read (posted now, or
#     already there when not posting): radius_comp = G41/G42 found, r_params = R parameters it uses, cycle800 = its
#     CYCLE800 plane when it has exactly one ("" = none = nest face; several, or only a turning-tool alignment:
#     cycle800_note SEVERAL / TURNING)
#   - <DOCUMENT>_TOOL_LOAD.MPF from the installed tool_load_mda script (sisters = extra tools). Tools of B programs that
#     count with SETPIECE without a tool life get a warning (the control only counts pieces with tool life monitoring).
#   - <document>_ORDER.xlsx, <document>_SISTERS.xlsx, <document>_SETUP.docx (tool_library\job_docs.py; templates in
#     tool_library\templates). Tool numbers that do not follow NUMBER_STANDARD are listed.
# Log: C:\Users\Public\Documents\OPEN MIND\go_to_machine_log.txt
import os, re, csv, json, time, shutil, tempfile, traceback, datetime, importlib.util

PY_DIR   = r"C:\Users\Public\Documents\OPEN MIND\python"
OUT_DIR  = r"C:\Users\Public\Documents\OPEN MIND"
HERE     = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.path.join(PY_DIR, "go_to_machine")
LIB_DIRS = (os.path.join(PY_DIR, "tool_library"), os.path.join(HERE, "..", "tool_library"))
TLM_FILES = (os.path.join(PY_DIR, "tool_load_mda", "tool_load_mda.py"), os.path.join(HERE, "..", "tool_load_mda", "tool_load_mda.py"))
NUMBER_STANDARD = "HELLER"          # tool_numbers.STANDARDS: tool IDs that do not follow it are listed
OUT_SUB  = "go to machine"          # folder in the document folder for everything but the NC files
TITLE    = "Go to machine"
PACKAGES = ["Validation", "Production", "Pick functions"]
F_POST, F_BLIST, F_MDA = "Post the B programs", "B program list (generator)", "Tool load MDA"
F_ORDER, F_SISTER, F_SETUP = "Order sheet", "Sister tool sheet", "NC master setup sheet"
FUNCS = (F_POST, F_BLIST, F_MDA, F_ORDER, F_SISTER, F_SETUP)
PRESET = {"Validation": (F_POST, F_BLIST, F_MDA, F_ORDER, F_SISTER),
          "Production": (F_POST, F_BLIST, F_MDA, F_ORDER, F_SETUP),
          "Pick functions": ()}
F_PROG, F_SHEET = "Programmer", "Sister sheet (sisters, tool life)"
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


# ---------------- tool load MDA ----------------
def tool_mda(progs, setpiece_ids, folder, doc_name, label, table=None, ask=True):
    """<DOCUMENT>_TOOL_LOAD.MPF with the installed tool_load_mda script. ask = sisters / tool life screens; else from
    table {tool id: (sisters, life)} (sister sheet), missing = 0 sisters (only the turning tip / cut screen shows).
    Returns (message lines, {tool id: (sisters, life)} or None)."""
    p = next((os.path.normpath(f) for f in TLM_FILES if os.path.exists(os.path.normpath(f))), None)
    if p is None:
        return ["", "Tool load MDA not written: tool_load_mda.py not found in %s" % os.path.join(PY_DIR, "tool_load_mda")], None
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
        return out + ["Tool load MDA not written: no tool could be read (no gage length: %s)" % (", ".join(no_gage) or "-")], None
    tools.sort(key=lambda d: (tlm._f(d["id"]) is None, tlm._f(d["id"]) or 0, d["id"]))
    need = set(i for i in setpiece_ids if i in ids)
    if ask:
        counts = tlm.ask_counts(tools, tlm.load_last(), need)
    else:
        counts = tlm.fixed_counts(tools, table)
        if not tlm.ask_turning(tools):
            counts = None
    if counts is None:
        log("tool load MDA cancelled at sisters / tool life")
        return out + ["Tool load MDA cancelled: not written."], None
    if ask:
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
    return out, counts


# ---------------- job-end documents (tool_library: job_docs, tool_info, office_fill, tool_numbers) ----------------
def load_docs_lib():
    """job_docs and the modules it imports, fresh (hyperMILL keeps imported modules between runs)."""
    import sys, importlib
    p = lib_file("job_docs.py")
    if p is None:
        raise RuntimeError("job_docs.py not found in tool_library")
    d = os.path.dirname(p)
    if d not in sys.path:
        sys.path.insert(0, d)
    mods = {}
    for n in ("tool_numbers", "office_fill", "tool_info", "job_docs"):
        m = importlib.import_module(n)
        if os.path.normcase(os.path.dirname(os.path.abspath(m.__file__))) != os.path.normcase(d):
            sys.modules.pop(n, None)                  # another copy was imported first: use this folder's
            m = importlib.import_module(n)
        importlib.reload(m)
        mods[n] = m
    return mods


def program_tools(progs):
    """Tools of the B programs in the order they are first used (step order, job order)."""
    out, seen = [], set()
    for pr in sorted(progs, key=lambda p: p["step"]):
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
                out.append(t)
    return out


def sim_date(progs):
    """Newest Simulation Center run (yyyy-mm-dd) of the B programs' toolpaths, or ''."""
    runs = [j.get("run") for p in progs for j in p.get("jobs", []) if j.get("run")]
    return max(runs)[:10] if runs else ""


def material_of(lists, names, scope):
    for jl, n in zip(lists, names):
        if scope in ("All joblists", n):
            try:
                m = val(getattr(jl, "Material", ""))
                s = str(val(getattr(m, "Name", m)) or "").strip()
                if s and not s.startswith("<"):
                    return s
            except Exception:
                pass
    return ""


def newest_sister_sheet(folder):
    """The newest *_SISTERS.xlsx in <document folder>\\go to machine\\VALIDATION_*, or ''."""
    root = os.path.join(folder, OUT_SUB)
    best = ("", 0.0)
    try:
        for d in os.listdir(root):
            if not d.upper().startswith("VALIDATION_"):
                continue
            for n in os.listdir(os.path.join(root, d)):
                if n.upper().endswith("_SISTERS.XLSX") and not n.startswith("~$"):
                    p = os.path.join(root, d, n)
                    t = os.path.getmtime(p)
                    if t > best[1]:
                        best = (p, t)
    except Exception:
        pass
    return best[0]


def last_settings():
    try:
        with open(os.path.join(out_dir(), "go_to_machine_last.json"), encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_settings(d):
    try:
        with open(os.path.join(out_dir(), "go_to_machine_last.json"), "w", encoding="utf-8") as f:
            json.dump(d, f, indent=1)
    except Exception as e:
        log("settings not saved:", e)


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
        last, st = last_rename(), last_settings()
        g = _gui()
        dlg = g.InputDialog(TITLE)
        dlg.AddDropDown("Joblist", scopes, defaultIndex=0)
        dlg.AddText("Part number", defaultValue=last.get("part", ""))
        dlg.AddText("Machine", defaultValue=last.get("machine", ""))
        dlg.AddDropDown("Package", PACKAGES, defaultIndex=PACKAGES.index(st.get("package")) if st.get("package") in PACKAGES else 0)
        ok, v = dlg.Show()
        if not ok:
            log("cancelled"); return
        scope = scopes[pick_index(v.get("Joblist"), scopes)]
        part, machine = str(v.get("Part number", "")).strip(), str(v.get("Machine", "")).strip()
        package = PACKAGES[pick_index(v.get("Package"), PACKAGES)]
        err = bp.input_errors(part, machine, "10", "10")
        if err:
            info("Fix these first:\n\n" + "\n".join(err)); return
        # ---- screen 2: what to make (ticked by the package; untick or tick any) ----
        dlg = g.InputDialog("%s | %s" % (TITLE, package) + ("" if package == "Pick functions" else " (untick what you do not want)"))
        for f in FUNCS:
            dlg.AddBool(f, defaultValue=f in PRESET[package])
        dlg.AddText(F_PROG, defaultValue=st.get("programmer") or os.environ.get("USERNAME", ""))
        if package != "Validation":
            dlg.AddText(F_SHEET, defaultValue=newest_sister_sheet(folder))
        ok, v = dlg.Show()
        if not ok:
            log("cancelled at the functions screen"); return
        funcs = dict((f, bool(v.get(f))) for f in FUNCS)
        programmer = str(v.get(F_PROG, "") or "").strip()
        sheet_path = str(v.get(F_SHEET, "") or "").strip().strip('"') if package != "Validation" else ""
        save_settings({"package": package, "programmer": programmer})
        log("joblist:", scope, "| part:", part, "| machine:", machine or "-", "| package:", package, "|",
            ", ".join(f for f in FUNCS if funcs[f]) or "check only", "| sister sheet:", sheet_path or "-")
        # ---- sisters / tool life: validation 0, production the filled sister sheet ----
        table, docs = None, {}
        if package == "Production" and (funcs[F_MDA] or funcs[F_ORDER] or funcs[F_SETUP]) and not os.path.isfile(sheet_path):
            info("Production needs the sister sheet filled in during validation (Sisters, Tool Life):\n%s\n\nRun Validation "
                 "first, fill the sheet and save it, or give its path on the second screen." % (sheet_path or "(none found)"))
            return
        if sheet_path and os.path.isfile(sheet_path):
            docs = load_docs_lib()
            table, sprobs = docs["job_docs"].read_sister_sheet(sheet_path)
            log("sister sheet:", sheet_path, "|", len(table), "tools |", sprobs)
            if sprobs:
                info("Sister sheet: these were read as 0:\n" + "\n".join(sprobs))
        # ---- check ----
        chosen = [(n, [bp.classify(cj, n) for cj in bp.compound_jobs(jl)]) for jl, n in zip(lists, names)
                  if scope == "All joblists" or n == scope]
        progs, left, problems = collect(bp, rc, chosen, part, machine, folder)
        npass = sum(1 for p in progs if p["ok"])
        nfail = len(progs) - npass
        rep = report_lines(progs, left, problems, "%s  %s  part %s  machine %s  %s" % (TITLE, scope, part, machine or "-", package))
        for ln in rep:
            log(ln)
        output("\n".join(rep))
        if not progs:
            info("No compound job in %s is named B_%s_<step>%s. Run B program rename (Job processing) first." % (
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
            info("\n".join(summary + ["", "Nothing posted, nothing written. Fix these first (run B program rename):"] + twice)); return
        if not any(funcs.values()):
            info("\n".join(summary + ["", "Check only: nothing posted, nothing written."])); return

        # ---- post ----
        msg, pick, targets = [], 0, progs
        if funcs[F_POST]:
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
            res, ok, written = post(model, targets, folder)
            found = {stem(p): p for p in written}
            missing = [p["name"] for p in targets if p["name"].lower() not in found]
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
        else:
            found = {stem(p): p for p in snapshot(folder) if p.lower().endswith(NC_EXT)}
            msg.append("Not posted (%s unticked). NC facts read from the NC files already there (%d)." % (F_POST, len(found)))
            if nfail:
                msg.append("%d of %d B programs fail the check (see the output window)." % (nfail, len(progs)))
        # ---- what the list and the documents hold ----
        scope_progs = targets
        if len(targets) != len(progs):
            inc = ["Only the %d posted" % len(targets), "All %d B programs" % len(progs)]
            if choose(TITLE + " | B program list and documents", "Include", inc) == 1:
                scope_progs = progs
            log("B program list and documents:", "all B programs" if scope_progs is progs else "only the posted ones")
        keep = set(p["name"] for p in scope_progs)
        dropped = [p for p in progs if p["name"] not in keep]
        drop_names = set(p["name"] for p in dropped)
        today = datetime.date.today().strftime("%Y-%m-%d")
        sub = {"Validation": "VALIDATION_", "Production": "PRODUCTION_"}.get(package)
        dest = os.path.join(folder, OUT_SUB, sub + today) if (folder and sub) else (os.path.join(folder, OUT_SUB) if folder else "")
        if dest:
            try:
                os.makedirs(dest, exist_ok=True)
            except Exception as e:
                log("cannot create", dest, e)
        if not dest or not writable(dest):
            dest = out_dir()
        log("output folder:", dest)
        msg += ["", "Output folder: " + dest]
        base = os.path.splitext(path.replace("\\", "/").split("/")[-1])[0] or "document"
        label = "all" if scope == "All joblists" else scope
        # ---- B program list for the generator ----
        data = {"steps": [], "refused": []}
        if funcs[F_BLIST] or funcs[F_MDA]:
            rules_path = lib_file("brk_rules.csv")
            rules = bp.load_rules(rules_path) if rules_path else []
            chosen_x = [(n, [e for e in es if e["name"] not in drop_names]) for n, es in chosen]
            data, xproblems = bp.build_export(chosen_x, part, machine, inch, rules, path,
                                              datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            for x in xproblems:
                log("export:", x)
            if funcs[F_BLIST]:
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
        # ---- tool load MDA ----
        counts = None
        if funcs[F_MDA]:
            setpiece_ids = set(s["tool"] for s in data["steps"] if s.get("setpiece"))
            try:
                mlines, counts = tool_mda(scope_progs, setpiece_ids, dest, base, label,
                                          table=None if package == "Validation" else table,
                                          ask=(package == "Pick functions" and table is None))
                msg += mlines
            except Exception:
                log("tool load MDA FAILED:", traceback.format_exc())
                msg += ["", "Tool load MDA failed (see go_to_machine_log.txt)."]
        if package == "Validation":
            counts = {}
        elif counts is None:
            counts = table or {}
        # ---- documents ----
        if funcs[F_ORDER] or funcs[F_SISTER] or funcs[F_SETUP]:
            try:
                msg += documents(scope_progs, funcs, counts, dest, base, package, today, dict(
                    part=part, machine=machine, material_type=material_of(lists, names, scope), date=today,
                    programmer=programmer, sim_date=sim_date(scope_progs), job=base, program=label), docs or None)
            except Exception:
                log("documents FAILED:", traceback.format_exc())
                msg += ["", "Documents failed (see go_to_machine_log.txt)."]
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


def documents(progs, funcs, counts, dest, base, package, today, header, docs=None):
    """Order sheet, sister tool sheet, NC master setup for the tools of progs. Returns message lines."""
    docs = docs or load_docs_lib()
    jd, ti, tn = docs["job_docs"], docs["tool_info"], docs["tool_numbers"]
    tmpd = tempfile.mkdtemp(prefix="gtm_tools_")
    infos = [ti.read(t, tmpd) for t in program_tools(progs)]
    for i in infos:
        log("tool:", i["id"], "|", ti.description(i), "| order", i["order_code"] or "-", "(%s)" % (i["order_from"] or "none"),
            "| reach", i["reach"], "| holders", [h["name"] for h in i["holders"]], "| missing", i["missing"])
    out = ["", "Documents: %d tool%s" % (len(infos), "" if len(infos) == 1 else "s")]
    if funcs.get(F_ORDER):
        p, n, marked = jd.order_sheet(os.path.join(dest, base + "_ORDER.xlsx"), infos, counts,
                                      "TOOL ORDER - %s - %s - %s" % (header.get("part") or base, package.upper(), today))
        out += ["  Order sheet: %d line%s%s" % (n, "" if n == 1 else "s", (", %d to check (yellow)" % marked) if marked else ""), "    " + p]
    if funcs.get(F_SISTER):
        p = jd.sister_sheet(os.path.join(dest, base + "_SISTERS.xlsx"), infos, header)
        out += ["  Sister tool sheet: fill Sisters (extra tools) and Tool Life, save; Production reads it", "    " + p]
    if funcs.get(F_SETUP):
        p = jd.setup_sheet(os.path.join(dest, base + "_SETUP.docx"), infos, header, counts)
        out += ["  NC master setup: QTY = 1 + sisters" + ("" if counts else " (no sister counts: QTY 1)"), "    " + p]
    no_order = [i["id"] for i in infos if not i["order_code"] or i["order_from"] == "Tool name"]
    if no_order:
        out.append("  Order no. missing or taken from the tool name: " + ", ".join(no_order[:10]) + (" ..." if len(no_order) > 10 else ""))
    no_holder = [i["id"] for i in infos if "holder" in i["missing"]]
    if no_holder:
        out.append("  No holder in hyperMILL (holder / stick-out blank): " + ", ".join(no_holder[:10]) + (" ..." if len(no_holder) > 10 else ""))
    off = [i["id"] for i in infos if not tn.follows(i["id"], NUMBER_STANDARD)[0]]
    if off:
        out.append("  Tool numbers not in the %s standard (Tool numbering, Job processing): %d - %s" % (
            NUMBER_STANDARD, len(off), ", ".join(off[:6]) + (" ..." if len(off) > 6 else "")))
    shutil.rmtree(tmpd, ignore_errors=True)
    return out


if __name__ == "__main__":
    run()
