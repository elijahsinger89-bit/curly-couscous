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
# After posting:
#   - the NC files written or updated (document folder and its NC folder, before / after)
#   - when only some B programs were posted: B program list and tool sheet: Only the posted ones / All B programs
#   - <document>_B_PROGRAMS.json / .csv (tool_library\B_PROGRAM_LIST_FORMAT.txt) for the generator's Import B list;
#     B programs left out are listed in it as "not posted"
#   - the tool sheet <document>_<joblist>_tool_order.csv: the columns and catalog lookup of the installed
#     tool_order_list script (tool_order_list.py: catalog, tool_row), one row per tool of those B programs,
#     "Toolpath names" = <B program>: <toolpath>
# Log: C:\Users\Public\Documents\OPEN MIND\go_to_machine_log.txt
import os, re, csv, json, time, tempfile, traceback, datetime, importlib.util

PY_DIR   = r"C:\Users\Public\Documents\OPEN MIND\python"
OUT_DIR  = r"C:\Users\Public\Documents\OPEN MIND"
HERE     = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.path.join(PY_DIR, "go_to_machine")
LIB_DIRS = (os.path.join(PY_DIR, "tool_library"), os.path.join(HERE, "..", "tool_library"))
TOL_FILES = (os.path.join(PY_DIR, "tool_order_list", "tool_order_list.py"), os.path.join(HERE, "..", "tool_order_list", "tool_order_list.py"))
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
        ok, v = dlg.Show()
        if not ok:
            log("cancelled"); return
        scope = scopes[pick_index(v.get("Joblist"), scopes)]
        part, machine = str(v.get("Part number", "")).strip(), str(v.get("Machine", "")).strip()
        action = pick_index(v.get("Action"), ACTIONS)
        log("joblist:", scope, "| part:", part, "| machine:", machine or "-", "| action:", ACTIONS[action])
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
            summary.append("Fail:")
            for p in fails:
                why = sorted(set(j["reason"] for j in p["failed"])) or ["no jobs"]
                summary.append("  %s  %s" % (p["name"], "; ".join(why)))
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
        dest = folder if folder and writable(folder) else out_dir()
        base = os.path.splitext(path.replace("\\", "/").split("/")[-1])[0] or "document"
        # ---- B program list for the generator ----
        rules_path = lib_file("brk_rules.csv")
        rules = bp.load_rules(rules_path) if rules_path else []
        chosen_x = [(n, [e for e in es if e["name"] not in drop_names]) for n, es in chosen]
        data, xproblems = bp.build_export(chosen_x, part, machine, inch, rules, path,
                                          datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        for p in dropped:
            data["refused"].append(dict(name=p["name"], joblist=p["joblist"], reason="not posted: failed the go-to-machine check"))
        if data["steps"] and not any("used twice" in x for x in xproblems):
            pj, pc = bp.write_export(data, dest, base)
            log("B program list:", pj, "|", pc)
            msg += ["", "B program list for the generator (Import B list): %d B program%s" % (len(data["steps"]), "" if len(data["steps"]) == 1 else "s"), "  " + pj]
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
