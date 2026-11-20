# tool_center.py - one command for building library tools in the open document. Pick the path:
#   Tool wizard     the best first-choice tool of each performance level; pick one
#   Tool selector   performance level, then the first-choice families, the family and the tool
#   Tool generator  every tool of the type at the size (all performance levels, any rating for the material), families grouped
#                   by the material's catalog rating (primary, suitable, not rated), then the family and the tool
#   Tool search     type a family, series, product name or catalog number (md133, harvi 4, X5) instead of picking a tool type,
#                   then the same size screen and every tool of that family at the size
# All four show the same screens first: machine, spindle (its max rpm caps every speed and feed), manufacturer, tool type and
# material, size with every limit for the tool type and the primary usage. All four end with the cutting-data sets and generate.
# A message box with INTRO opens before the path screen; untick "Show path descriptions at start" to skip it (remembered in
# tool_center_last.json).
# The screens are in tool_flow.py. The material drop-down starts on the material of the document's joblists (the first joblist that has one).
# Logs: C:\Users\Public\Documents\OPEN MIND\tool_wizard_log.txt, tool_selector_log.txt, tool_generator_log.txt, tool_search_log.txt
import os, sys, json, tempfile, importlib, importlib.util, traceback

PY_DIR  = r"C:\Users\Public\Documents\OPEN MIND\python"
LIB_DIR = os.path.join(PY_DIR, "tool_library")
HERE    = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.path.join(PY_DIR, "tool_center")
TITLE   = "Tool center"
PATHS   = ["Tool wizard", "Tool selector", "Tool generator", "Tool search"]
LAST_FILES = (r"C:\Users\Public\Documents\OPEN MIND\tool_center_last.json",
              os.path.join(tempfile.gettempdir(), "tool_center_last.json"))     # same file tool_flow.py remembers its screens in
SHOW_INTRO = "Show path descriptions at start"
INTRO = """TOOL WIZARD - fewest choices
One tool per performance level, picked for you. You pick the level.
Use when you need a good tool fast and the family does not matter.

TOOL SELECTOR - more choices
Pick the level, then a first-choice family, then the exact tool.
Use when you want to compare first-choice families, lengths and grades.

TOOL GENERATOR - every choice
Every tool of the type at the size: all levels, every material rating.
Use when the first-choice tools do not fit (reach, length, shank) or you want a tool the catalog does not rate first choice.

TOOL SEARCH - direct
Type a family, product name or catalog number (md133, harvi 4, H1TE4RA0500).
Use when you already know the tool or family you want.

All four use the same machine, spindle, manufacturer, material and size screens, and build the tool the same way."""

def load_last():
    for p in LAST_FILES:
        try:
            with open(p, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            continue
    return {}

def save_last(d):
    for p in LAST_FILES:
        try:
            with open(p, "w", encoding="utf-8") as f:
                json.dump(d, f)
            return
        except Exception:
            continue

def _gui():
    import om.cad.gui as g
    return g

def _load(name):
    """Module next to this script, loaded fresh (hyperMILL keeps imported modules between runs)."""
    path = os.path.join(HERE, name + ".py")
    spec = importlib.util.spec_from_file_location("tool_center_" + name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

def joblist_material(model):
    """Material group of the document's joblists that the tool library knows (material_map.csv): the first joblist with one."""
    known = []
    try:
        if LIB_DIR not in sys.path:
            sys.path.insert(0, LIB_DIR)
        import tool_numbers
        importlib.reload(tool_numbers)
        import tool_builder as tb
        importlib.reload(tb)
        known = [r["hypermill_material"] for r in tb.load_rows("material_map.csv")]
    except Exception:
        pass
    found = []
    try:
        for jl in model.JobListSet.GetJobLists():
            m = str(jl.Material or "").strip()
            if m and m not in found:
                found.append(m)
    except Exception:
        pass
    for m in found:
        if not known or m in known:
            return m, found
    return None, found

def run():
    g = _gui()
    try:
        import om
        doc = om.Application().CurrentDocument
        if doc is None:
            g.ShowMessageBox(g.MessageBoxType.INFORMATION, TITLE, "No document open."); return
        model = doc.CamModel
        mat, found = joblist_material(model)
        last = load_last()
        show = last.get("show_intro", True) is not False
        if show:
            g.ShowMessageBox(g.MessageBoxType.INFORMATION, TITLE, INTRO)
        dlg = g.InputDialog(TITLE + (" | joblist material: %s" % mat if mat else ""))
        dlg.AddDropDown("Path", PATHS, defaultIndex=0)
        dlg.AddBool(SHOW_INTRO, defaultValue=show)
        ok, vals = dlg.Show()
        if not ok:
            return
        want = bool(vals.get(SHOW_INTRO, show))
        if want != show:
            last["show_intro"] = want
            save_last(last)
        v = vals.get("Path")
        i = v if isinstance(v, int) and not isinstance(v, bool) else (PATHS.index(v) if v in PATHS else 0)
        _load("tool_flow").run(model=model, default_mat=mat, mode=("wizard", "selector", "generator", "search")[i])
    except Exception:
        tb_txt = traceback.format_exc()
        for p in (r"C:\Users\Public\Documents\OPEN MIND\tool_center_log.txt",):
            try:
                with open(p, "w", encoding="utf-8") as f:
                    f.write(tb_txt)
            except Exception:
                pass
        try:
            g.ShowMessageBox(g.MessageBoxType.INFORMATION, TITLE, "Failed. See tool_center_log.txt.")
        except Exception:
            pass

if __name__ == "__main__":
    run()
