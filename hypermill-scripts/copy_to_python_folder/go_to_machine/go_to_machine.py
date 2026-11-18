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
# After posting: the NC files written or updated (document folder and its NC folder, before / after), and
# <document>_B_PROGRAMS.json / .csv (tool_library\B_PROGRAM_LIST_FORMAT.txt) for the generator's Import B list.
# Log: C:\Users\Public\Documents\OPEN MIND\go_to_machine_log.txt
import os, json, time, tempfile, traceback, datetime, importlib.util

PY_DIR   = r"C:\Users\Public\Documents\OPEN MIND\python"
OUT_DIR  = r"C:\Users\Public\Documents\OPEN MIND"
HERE     = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.path.join(PY_DIR, "go_to_machine")
LIB_DIRS = (os.path.join(PY_DIR, "tool_library"), os.path.join(HERE, "..", "tool_library"))
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
        # ---- B program list for the generator ----
        rules_path = lib_file("brk_rules.csv")
        rules = bp.load_rules(rules_path) if rules_path else []
        data, xproblems = bp.build_export(chosen, part, machine, inch, rules, path,
                                          datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        if data["steps"] and not any("used twice" in x for x in xproblems):
            dest = folder if folder and writable(folder) else out_dir()
            base = os.path.splitext(path.replace("\\", "/").split("/")[-1])[0] or "document"
            pj, pc = bp.write_export(data, dest, base)
            log("B program list:", pj, "|", pc)
            msg += ["", "B program list for the generator (Import B list):", "  " + pj]
        for x in xproblems:
            log("export:", x)
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
