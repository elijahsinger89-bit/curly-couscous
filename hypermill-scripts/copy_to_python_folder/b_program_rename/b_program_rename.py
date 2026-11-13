# b_program_rename.py - hyperMILL 35
# Renames compound jobs to B program names for the SINUMERIK nest framework: B_<part>_<step>_<machine>
# (each compound job posts as one NC file named after it, and the generator's step table calls it by that name).
# Screens: 1 action (rename / undo last rename) and joblist (one or all)
#          2 part number, machine, starting step, advance, which compound jobs (all with one tool / pick)
#          3 pick screens (10 per screen), only when "Pick" was chosen
#          4 review: old -> new list in the output window, then Rename yes / no
# Rules: empty compound jobs (notes, dividers) are skipped, keep their text and take no step number.
#        A compound job whose jobs use more than one tool, or a job without a tool, is not renamed.
#        Steps count up in tree order from the starting step by the advance. 3-digit steps, 4 when the last is 1000+.
#        24 characters at most. A new name may not belong to a compound job the run leaves alone.
# Undo: the old names are saved before renaming; "Undo last rename" puts them back.
# Log: C:\Users\Public\Documents\OPEN MIND\b_program_rename_log.txt
import os, json, tempfile, traceback, datetime

PY_DIR    = r"C:\Users\Public\Documents\OPEN MIND\python"
OUT_DIR   = r"C:\Users\Public\Documents\OPEN MIND"
HERE      = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.path.join(PY_DIR, "b_program_rename")
LIB_DIRS  = (os.path.join(PY_DIR, "tool_library"), os.path.join(HERE, "..", "tool_library"))
TITLE     = "B program rename"
PER_SCREEN = 10
MAX_BOX_LINES = 30
BOX_WIDTH = 90
ACTIONS   = ["Rename compound jobs", "Undo last rename"]
WHICH     = ["All with one tool", "Pick, 10 per screen"]

lines = []


def log(*a):
    lines.append(" ".join(str(x) for x in a))


def out_dir():
    return OUT_DIR if os.path.isdir(OUT_DIR) else tempfile.gettempdir()


def out_path(name):
    return os.path.join(out_dir(), name)


def load_bp():
    """b_programs.py by file path, fresh every run (hyperMILL keeps imported modules between runs)."""
    import importlib.util
    for d in LIB_DIRS:
        p = os.path.normpath(os.path.join(d, "b_programs.py"))
        if os.path.exists(p):
            spec = importlib.util.spec_from_file_location("hm_b_programs", p)
            m = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(m)
            m.LOADED_FROM = p
            return m
    raise RuntimeError("b_programs.py not found in tool_library")


# ---------------- dialogs ----------------
def _gui():
    import om.cad.gui as g
    return g


def info(text_):
    import textwrap
    g = _gui()
    rows = []
    for ln in str(text_).split("\n"):
        rows += textwrap.wrap(ln, BOX_WIDTH, subsequent_indent="   ", break_long_words=False,
                              break_on_hyphens=False) or [""]
    if len(rows) > MAX_BOX_LINES:
        rows = rows[:MAX_BOX_LINES - 1] + ["... full list in the output window and b_program_rename_log.txt"]
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


def load_last():
    try:
        with open(out_path("b_program_rename_last.json"), encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_last(d):
    try:
        with open(out_path("b_program_rename_last.json"), "w", encoding="utf-8") as f:
            json.dump(d, f)
    except Exception:
        pass


def val(x):
    return x() if callable(x) else x


# ---------------- document ----------------
def all_compounds(model, bp):
    """[(joblist, joblist name, compound entries in tree order)] for every joblist."""
    out = []
    for jl in model.JobListSet.GetJobLists():
        name = str(val(jl.Name))
        out.append((jl, name, [bp.classify(cj, name) for cj in bp.compound_jobs(jl)]))
    return out


def find_by_uuid(model, bp, uuid):
    for jl in model.JobListSet.GetJobLists():
        for cj in bp.compound_jobs(jl):
            if str(val(getattr(cj, "UUID", ""))) == uuid:
                return cj
    return None


# ---------------- rename ----------------
def screen_inputs(last, counts):
    g = _gui()
    vals0 = dict(part=last.get("part", ""), machine=last.get("machine", ""),
                 start=str(last.get("start", "10")), advance=str(last.get("advance", "10")), which=0)
    while True:
        dlg = g.InputDialog("%s | %d to rename, %d notes, %d not renamable" % (TITLE, counts[0], counts[1], counts[2]))
        dlg.AddText("Part number", defaultValue=vals0["part"])
        dlg.AddText("Machine", defaultValue=vals0["machine"])
        dlg.AddText("Starting step", defaultValue=vals0["start"])
        dlg.AddText("Advance", defaultValue=vals0["advance"])
        dlg.AddDropDown("Compound jobs", WHICH, defaultIndex=vals0["which"])
        ok, v = dlg.Show()
        if not ok:
            return None
        vals0 = dict(part=str(v.get("Part number", "")).strip(), machine=str(v.get("Machine", "")).strip(),
                     start=str(v.get("Starting step", "")).strip(), advance=str(v.get("Advance", "")).strip(),
                     which=pick_index(v.get("Compound jobs"), WHICH))
        return vals0


def screen_pick(entries):
    """Pick screens, 10 compound jobs each. Sets entry['pick']. Returns False on Cancel."""
    g = _gui()
    cands = [e for e in entries if e["kind"] == "one"]
    pages = (len(cands) + PER_SCREEN - 1) // PER_SCREEN
    for p in range(pages):
        chunk = cands[p * PER_SCREEN:(p + 1) * PER_SCREEN]
        dlg = g.InputDialog("%s | pick %d of %d" % (TITLE, p + 1, pages))
        labels = []
        for i, e in enumerate(chunk, p * PER_SCREEN + 1):
            label = ("%3d  %s" % (i, e["name"]))[:60]
            labels.append(label)
            dlg.AddBool(label, defaultValue=True)
        ok, v = dlg.Show()
        if not ok:
            return False
        for e, label in zip(chunk, labels):
            e["pick"] = bool(v.get(label, True))
    return True


def do_rename(model, doc, bp, scope):
    last = load_last()
    lists = all_compounds(model, bp)
    chosen = [x for x in lists if scope is None or x[1] == scope]
    entries = [e for _, _, es in chosen for e in es]
    if not entries:
        info("No compound jobs in %s." % (scope or "the document")); return
    counts = (sum(e["kind"] == "one" for e in entries), sum(e["kind"] == "note" for e in entries),
              sum(e["kind"] in ("mixed", "notool") for e in entries))
    log("compound jobs:", len(entries), "| one tool:", counts[0], "| notes:", counts[1], "| not renamable:", counts[2])
    if counts[0] == 0:
        info("No compound job with exactly one tool in %s. Nothing to rename." % (scope or "the document")); return
    while True:
        v = screen_inputs(last, counts)
        if v is None:
            log("cancelled at the inputs"); return
        last.update(part=v["part"], machine=v["machine"], start=v["start"], advance=v["advance"])
        err = bp.input_errors(v["part"], v["machine"], v["start"], v["advance"])
        if err:
            info("Fix these first:\n\n" + "\n".join(err)); continue
        for e in entries:
            e["pick"] = True
        if v["which"] == 1 and not screen_pick(entries):
            log("cancelled at the pick screens"); return
        picked_uuids = set(e["uuid"] for e in entries if e["kind"] == "one" and e.get("pick", True))
        others = [e["name"] for _, _, es in lists for e in es if e["uuid"] not in picked_uuids]
        pl = bp.plan(entries, v["part"], v["machine"], v["start"], v["advance"], others)
        if pl["errors"]:
            info("Fix these first:\n\n" + "\n".join(pl["errors"])); continue
        break
    save_last(last)
    report = ["%s  %s  part %s  machine %s  start %s  advance %s" % (TITLE, scope or "all joblists", v["part"],
              v["machine"] or "-", v["start"], v["advance"]), ""]
    cur = None
    for r in pl["rows"]:
        if r["joblist"] != cur:
            cur = r["joblist"]
            report.append("joblist " + cur)
        report.append("  " + bp.row_text(r))
    for ln in report:
        log(ln)
    output("\n".join(report))
    n = len(pl["renames"])
    same = sum(r["action"] == "same" for r in pl["rows"])
    refused = [r for r in pl["rows"] if r["action"] in ("mixed", "notool")]
    summary = ["%d compound job%s to rename, %d already named, %d notes skipped." % (n, "" if n == 1 else "s", same, counts[1])]
    if refused:
        summary.append("")
        summary.append("Not renamed (split them into one tool each):")
        summary += ["  %s  (T %s)" % (r["name"], ",".join(r["tools"]) or "none") for r in refused]
    summary.append("")
    summary.append("First and last:")
    named = [r for r in pl["rows"] if r.get("new")]
    for r in named[:3] + (named[-2:] if len(named) > 5 else []):
        summary.append("  %s <- %s" % (r["new"], r["name"]))
    summary.append("")
    summary.append("Full list in the output window.")
    info("\n".join(summary))
    if n == 0:
        return
    g = _gui()
    opts = ["No - leave the names as they are", "Yes - rename %d compound job%s" % (n, "" if n == 1 else "s")]
    dlg = g.InputDialog(TITLE + " | confirm")
    dlg.AddDropDown("Rename", opts, defaultIndex=0)
    ok, cv = dlg.Show()
    if not ok or pick_index(cv.get("Rename"), opts) != 1:
        log("not renamed (review only)"); info("Nothing renamed."); return
    undo = dict(document=str(val(doc.FullPath)), time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                items=[dict(uuid=r["uuid"], joblist=r["joblist"], old=r["name"], new=r["new"]) for r in pl["renames"]])
    undo_file = out_path("b_program_rename_undo.json")
    with open(undo_file, "w", encoding="utf-8") as f:
        json.dump(undo, f, indent=1)
    log("undo file:", undo_file)
    done, failed = 0, None
    for r in pl["renames"]:
        ok_, how = bp.set_name(r["obj"], r["new"])
        log("  %s -> %s : %s" % (r["name"], r["new"], ("ok via " + how) if ok_ else ("FAILED " + how)))
        if not ok_:
            failed = (r, how); break
        done += 1
    if failed:
        r, how = failed
        info("Renamed %d of %d, then stopped:\n%s -> %s\n%s\n\nThe rest keep their names. Undo last rename puts the %d back." % (
            done, n, r["name"], r["new"], how, done))
    else:
        info("Renamed %d compound job%s.\nUndo: run %s again and choose Undo last rename." % (n, "" if n == 1 else "s", TITLE))


# ---------------- undo ----------------
def do_undo(model, doc, bp):
    undo_file = out_path("b_program_rename_undo.json")
    try:
        with open(undo_file, encoding="utf-8") as f:
            undo = json.load(f)
    except Exception:
        info("No rename to undo."); return
    path = str(val(doc.FullPath))
    if os.path.normcase(undo.get("document", "")) != os.path.normcase(path):
        info("The last rename was made in another document:\n%s\n\nOpen that document to undo it." % undo.get("document", "?")); return
    items = undo.get("items", [])
    g = _gui()
    opts = ["No - keep the names", "Yes - put back %d old name%s (renamed %s)" % (len(items), "" if len(items) == 1 else "s", undo.get("time", "?"))]
    dlg = g.InputDialog(TITLE + " | undo")
    dlg.AddDropDown("Undo", opts, defaultIndex=0)
    ok, cv = dlg.Show()
    if not ok or pick_index(cv.get("Undo"), opts) != 1:
        info("Nothing changed."); return
    back, skipped = 0, []
    for it in items:
        cj = find_by_uuid(model, bp, it["uuid"])
        if cj is None:
            skipped.append("%s (not found)" % it["new"]); continue
        if bp.get_name(cj) != it["new"]:
            skipped.append("%s (renamed since: %s)" % (it["new"], bp.get_name(cj))); continue
        ok_, how = bp.set_name(cj, it["old"])
        log("  undo %s -> %s : %s" % (it["new"], it["old"], ("ok via " + how) if ok_ else ("FAILED " + how)))
        if ok_:
            back += 1
        else:
            skipped.append("%s (%s)" % (it["new"], how))
    try:
        os.replace(undo_file, out_path("b_program_rename_undo_used.json"))
    except Exception:
        pass
    msg = "Put back %d old name%s." % (back, "" if back == 1 else "s")
    if skipped:
        msg += "\n\nLeft as they are:\n" + "\n".join("  " + s for s in skipped)
    info(msg)


# ---------------- main ----------------
def run():
    try:
        bp = load_bp()
        log(TITLE, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "| b_programs", bp.VERSION, bp.LOADED_FROM)
        import om
        doc = om.Application().CurrentDocument
        if doc is None:
            info("No document open."); return
        log("document:", val(doc.FullPath))
        model = doc.CamModel
        names = [str(val(jl.Name)) for jl in model.JobListSet.GetJobLists()]
        if not names:
            info("No joblists in this document."); return
        scopes = names + (["All joblists"] if len(names) > 1 else [])
        g = _gui()
        dlg = g.InputDialog(TITLE)
        dlg.AddDropDown("Action", ACTIONS, defaultIndex=0)
        dlg.AddDropDown("Joblist", scopes, defaultIndex=0)
        ok, v = dlg.Show()
        if not ok:
            log("cancelled"); return
        action = pick_index(v.get("Action"), ACTIONS)
        scope = scopes[pick_index(v.get("Joblist"), scopes)]
        log("action:", ACTIONS[action], "| joblist:", scope)
        if action == 1:
            do_undo(model, doc, bp)
        else:
            do_rename(model, doc, bp, None if scope == "All joblists" else scope)
    except Exception:
        log("FAILED:", traceback.format_exc())
        try:
            info("Failed. See b_program_rename_log.txt.")
        except Exception:
            pass
    finally:
        try:
            with open(out_path("b_program_rename_log.txt"), "w", encoding="utf-8") as f:
                f.write("\n".join(lines) + "\n")
        except Exception:
            pass


if __name__ == "__main__":
    run()
