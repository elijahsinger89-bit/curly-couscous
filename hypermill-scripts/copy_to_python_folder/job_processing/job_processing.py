# job_processing.py - hyperMILL 35. The front-of-job menu: one button for building a job.
# Screen: What (drop-down):
#   Tools                 tool_center: tool wizard / selector / generator / search
#   Part wizard 1         builds the toolpaths of a part
#   Part wizard 2         puts library tools and cutting data in the toolpaths
#   Tool numbering        renumbers the document's tools to the numbering standard (tool_numbering)
#   Holder attacher       not built yet
#   B program rename      compound jobs -> B_<part>_<step>_<machine>
#   Restore job names     toolpath names back to "<number>: <toolpath type>"
#   Show toolpaths of one tool   light bulb on for one tool's toolpaths
# The chosen script is loaded from its own folder every time (hyperMILL keeps imported modules between runs) and its
# run() is called: it works exactly as when started from its own button. The last choice is offered first next time.
# Go to machine (posting, MDA, order / sister / setup sheets) is the other button.
# Log: C:\Users\Public\Documents\OPEN MIND\job_processing_log.txt
import os, json, tempfile, traceback, datetime, importlib.util

PY_DIR = r"C:\Users\Public\Documents\OPEN MIND\python"
OUT_DIR = r"C:\Users\Public\Documents\OPEN MIND"
HERE = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.path.join(PY_DIR, "job_processing")
SCRIPT_DIRS = [PY_DIR, os.path.join(HERE, "..")]
TITLE = "Job processing"
# (label in the drop-down, folder, script file); folder None = not built yet
MENU = [
    ("Tools: wizard / selector / generator / search", "tool_center", "tool_center.py"),
    ("Part wizard 1: build the toolpaths", "part_wizard_1", "part_wizard_1.py"),
    ("Part wizard 2: tools and cutting data in the toolpaths", "part_wizard_2", "part_wizard_2.py"),
    ("Tool numbering: tool numbers to the standard", "tool_numbering", "tool_numbering.py"),
    ("Holder attacher (not built yet)", None, None),
    ("B program rename: compound jobs to B_part_step_machine", "b_program_rename", "b_program_rename.py"),
    ("Restore job names: number and toolpath type", "restore_job_names", "restore_job_names.py"),
    ("Show toolpaths of one tool (light bulb)", "show_tool_toolpaths", "show_tool_toolpaths.py"),
]
lines = []


def log(*a):
    lines.append(" ".join(str(x) for x in a))


def _gui():
    import om.cad.gui as g
    return g


def info(t):
    g = _gui()
    g.ShowMessageBox(g.MessageBoxType.INFORMATION, TITLE, t)


def pick(v, options):
    if isinstance(v, int) and not isinstance(v, bool):
        return v if 0 <= v < len(options) else 0
    return options.index(v) if v in options else 0


def out_dir():
    return OUT_DIR if os.path.isdir(OUT_DIR) else tempfile.gettempdir()


def last_choice():
    try:
        with open(os.path.join(out_dir(), "job_processing_last.json"), encoding="utf-8") as f:
            return json.load(f).get("choice", "")
    except Exception:
        return ""


def save_choice(label):
    try:
        with open(os.path.join(out_dir(), "job_processing_last.json"), "w", encoding="utf-8") as f:
            json.dump({"choice": label}, f)
    except Exception:
        pass


def find_script(folder, fname):
    for d in SCRIPT_DIRS:
        p = os.path.normpath(os.path.join(d, folder, fname))
        if os.path.isfile(p):
            return p
    return None


def start(path, folder):
    """Loads the script from its file (fresh) and calls its run()."""
    spec = importlib.util.spec_from_file_location("jp_" + folder, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    if not callable(getattr(m, "run", None)):
        raise RuntimeError("%s has no run()" % os.path.basename(path))
    m.run()


def run():
    try:
        log(TITLE, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        labels = [m[0] for m in MENU]
        lc = last_choice()
        g = _gui()
        dlg = g.InputDialog(TITLE)
        dlg.AddDropDown("What", labels, defaultIndex=labels.index(lc) if lc in labels else 0)
        ok, v = dlg.Show()
        if not ok:
            log("cancelled"); return
        label, folder, fname = MENU[pick(v.get("What"), labels)]
        log("chosen:", label)
        if folder is None:
            info("%s\n\nThis one is not built yet." % label.replace(" (not built yet)", "")); return
        save_choice(label)
        path = find_script(folder, fname)
        if path is None:
            info("%s is not installed.\n\nCopy the folder %s from copy_to_python_folder into\n%s\nand restart hyperMILL." % (
                label.split(":")[0], folder, PY_DIR)); return
        log("starting:", path)
        start(path, folder)
        log("finished:", folder)
    except Exception:
        log("FAILED:", traceback.format_exc())
        try:
            info("Failed. See job_processing_log.txt (and the log of the script that was started).")
        except Exception:
            pass
    finally:
        try:
            with open(os.path.join(out_dir(), "job_processing_log.txt"), "w", encoding="utf-8") as f:
                f.write("\n".join(lines) + "\n")
        except Exception:
            pass


if __name__ == "__main__":
    run()
