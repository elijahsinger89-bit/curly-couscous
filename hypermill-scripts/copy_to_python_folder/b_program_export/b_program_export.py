# b_program_export.py - hyperMILL 35
# Writes the B program list for the SINUMERIK generator ("Import B list"): every compound job named
# B_<part>_<step>_<machine> with its tool and the breakage / measuring presets from tool_library\brk_rules.csv.
# This is the export step of the go-to-machine script, runnable on its own until that script exists.
# Screen: joblist (one or all), part number, machine (defaults: the last B program rename).
# Left out and listed: notes (empty compound jobs, silently), compound jobs with more than one tool or a job without a
# tool, and names that do not follow the rule for this part and machine (run b_program_rename first).
# Stops without writing when a step number is used twice.
# Output: <document folder>\<document>_B_PROGRAMS.json and .csv (else C:\Users\Public\Documents\OPEN MIND).
# Format: tool_library\B_PROGRAM_LIST_FORMAT.txt
# Log: C:\Users\Public\Documents\OPEN MIND\b_program_export_log.txt
import os, json, tempfile, traceback, datetime

PY_DIR   = r"C:\Users\Public\Documents\OPEN MIND\python"
OUT_DIR  = r"C:\Users\Public\Documents\OPEN MIND"
HERE     = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.path.join(PY_DIR, "b_program_export")
LIB_DIRS = (os.path.join(PY_DIR, "tool_library"), os.path.join(HERE, "..", "tool_library"))
TITLE    = "B program export"
MAX_BOX_LINES = 30
BOX_WIDTH = 90

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


def load_bp():
    import importlib.util
    p = lib_file("b_programs.py")
    if p is None:
        raise RuntimeError("b_programs.py not found in tool_library")
    spec = importlib.util.spec_from_file_location("hm_b_programs", p)
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
        rows = rows[:MAX_BOX_LINES - 1] + ["... full list in the output window and b_program_export_log.txt"]
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
        p = os.path.join(folder, "b_program_export_write_test.tmp")
        with open(p, "w") as f:
            f.write("x")
        os.remove(p)
        return True
    except Exception:
        return False


def run():
    try:
        bp = load_bp()
        log(TITLE, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "| b_programs", bp.VERSION, bp.LOADED_FROM)
        import om
        doc = om.Application().CurrentDocument
        if doc is None:
            info("No document open."); return
        path = str(val(doc.FullPath))
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
        ok, v = dlg.Show()
        if not ok:
            log("cancelled"); return
        scope = scopes[pick_index(v.get("Joblist"), scopes)]
        part, machine = str(v.get("Part number", "")).strip(), str(v.get("Machine", "")).strip()
        err = bp.input_errors(part, machine, "10", "10")
        if err:
            info("Fix these first:\n\n" + "\n".join(err)); return
        chosen = [(n, [bp.classify(cj, n) for cj in bp.compound_jobs(jl)]) for jl, n in zip(lists, names)
                  if scope == "All joblists" or n == scope]
        rules_path = lib_file("brk_rules.csv")
        rules = bp.load_rules(rules_path) if rules_path else []
        log("rules:", rules_path or "brk_rules.csv not found: every step gets the default presets", "|", len(rules), "rows")
        created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data, problems = bp.build_export(chosen, part, machine, inch, rules, path, created)
        report = ["%s  %s  part %s  machine %s  %s" % (TITLE, scope, part, machine or "-", data["units"]), ""]
        for s in data["steps"]:
            report.append("%5d  %-24s T %-12s %-14s D %-8s brk %s tol %-7s %s" % (
                s["step"], s["program"], s["tool"], s["tool_type"] or "-",
                ("%.4f" % s["diameter"]) if s["diameter"] is not None else "-",
                "on " if s["brk"] else "off", s["brk_tol"] or "BLANK", s["rule"]))
        if data["refused"]:
            report.append("")
            report.append("Left out:")
            report += ["  %s  (%s)" % (r["name"], r["reason"]) for r in data["refused"]]
        if problems:
            report.append("")
            report += ["PROBLEM: " + p for p in problems]
        for ln in report:
            log(ln)
        output("\n".join(report))
        twice = [p for p in problems if "used twice" in p]
        if twice:
            info("Nothing written. Fix these first (run b_program_rename):\n\n" + "\n".join(twice)); return
        if not data["steps"]:
            info("No compound job in %s is named B_%s_<step>%s. Nothing written." % (scope, part, ("_" + machine) if machine else "")); return
        folder = os.path.dirname(path)
        if not folder or not writable(folder):
            folder = out_dir()
        base = os.path.splitext(path.replace("\\", "/").split("/")[-1])[0] or "document"
        pj, pc = bp.write_export(data, folder, base)
        log("written:", pj, "|", pc)
        blank = sum(1 for s in data["steps"] if s["brk"] and not s["brk_tol"])
        msg = ["%d B program%s written:" % (len(data["steps"]), "" if len(data["steps"]) == 1 else "s"), pj, pc, ""]
        if blank:
            msg.append("%d step%s with break check on and no tolerance: fill brk_tol in tool_library\\brk_rules.csv, "
                       "or in the generator after the import." % (blank, "" if blank == 1 else "s"))
        if data["refused"]:
            msg.append("")
            msg.append("Left out:")
            msg += ["  %s  (%s)" % (r["name"], r["reason"]) for r in data["refused"]]
        others = [p for p in problems if "used twice" not in p]
        if others:
            msg.append("")
            msg += others
        msg.append("")
        msg.append("Generator: Import B list, pick the .json file.")
        info("\n".join(msg))
    except Exception:
        log("FAILED:", traceback.format_exc())
        try:
            info("Failed. See b_program_export_log.txt.")
        except Exception:
            pass
    finally:
        try:
            with open(os.path.join(out_dir(), "b_program_export_log.txt"), "w", encoding="utf-8") as f:
                f.write("\n".join(lines) + "\n")
        except Exception:
            pass


if __name__ == "__main__":
    run()
