# show_tool_toolpaths.py - hyperMILL 35 (v2). Turns on the toolpath display (the light bulb in the job tree) for every
# toolpath of one tool.
# Screen: Joblist (one or all), Tool (T<ID>  name  - number of toolpaths), Show:
#   "This tool only"   this tool's toolpaths on, every other toolpath off
#   "Add this tool"    this tool's toolpaths on, the others left as they are
#   "Everything on"    every toolpath on
# The light bulb (v1 log, 20 Nov 2026): the job setting *SHOW_NCPATH ('1' on, '0' off), else the job property ShowNCPaths.
#   Before changing anything the script reads both on every toolpath and lists the ones that are on (the log and the
#   output window): a bulb you turned on by hand must be in that list. It uses the one that reads on somewhere
#   (*SHOW_NCPATH first); when nothing reads on it uses ROUTE below and says so.
# Safety: one toolpath (one with a Simulation Center result when there is one) is switched alone, then checked: still
#   calculated, same status, same toolpath id, and its Simulation Center result (.ccrpt) still there. If hyperMILL counted the switch as a change to the toolpath, that one
#   is switched back, nothing else is touched, and the message says what changed (re-simulate that B program if its
#   result is gone). Run it on a scratch copy the first time.
# Compound jobs (B programs) that hold the setting are switched with their toolpaths.
# Log: C:\Users\Public\Documents\OPEN MIND\show_tool_toolpaths_log.txt (written line by line)
import os, re, sys, tempfile, traceback, datetime, importlib.util

# ---------------- SETTINGS ----------------
OUT_DIR = r"C:\Users\Public\Documents\OPEN MIND"
CFG_KEY = "*SHOW_NCPATH"       # job setting for the light bulb
PROP_KEY = "ShowNCPaths"       # job property, the second candidate
ROUTE = "cfg"                  # used when no toolpath reads on: "cfg" (*SHOW_NCPATH) or "prop" (ShowNCPaths)
SAFETY_TEST = True             # switch one toolpath first and check it was not counted as a change
# ------------------------------------------
PY_DIR = r"C:\Users\Public\Documents\OPEN MIND\python"
HERE = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.path.join(PY_DIR, "show_tool_toolpaths")
LIB_DIRS = [os.path.join(PY_DIR, "tool_library"), os.path.join(HERE, "..", "tool_library")]
TITLE = "Show toolpaths of one tool"
LOGNAME = "show_tool_toolpaths_log.txt"
MODES = ["This tool only", "Add this tool", "Everything on"]
lines = []
_f = [None]


def log(*a):
    s = " ".join(str(x) for x in a)
    lines.append(s)
    if _f[0]:
        try:
            _f[0].write(s + "\n"); _f[0].flush()
        except Exception:
            pass


def val(x):
    return x() if callable(x) else x


def text(x):
    try:
        return str(val(x) or "").strip()
    except Exception:
        return ""


def enum_name(v):
    return str(getattr(v, "name", v) or "")


def _gui():
    import om.cad.gui as g
    return g


def info(t):
    g = _gui()
    g.ShowMessageBox(g.MessageBoxType.INFORMATION, TITLE, t)


def output(t):
    g = _gui()
    try:
        g.CleanOutput(g.UIOutputWindow.ALL)
        g.WriteToOutput(t, g.UIOutputWindow.ALL)
        g.ProcessEvents()
    except Exception:
        pass


def events():
    try:
        _gui().ProcessEvents()
    except Exception:
        pass


def pick(v, options):
    if isinstance(v, int) and not isinstance(v, bool):
        return v if 0 <= v < len(options) else 0
    return options.index(v) if v in options else 0


def key_of(o):
    return text(getattr(o, "UUID", "")) or str(id(o))


def tool_of(job):
    try:
        return job.GetTool()
    except Exception:
        return None


def tool_label(t):
    tid = ""
    for a in ("ID", "Number"):
        tid = text(getattr(t, a, ""))
        if tid:
            break
    name = text(getattr(t, "Name", ""))
    return ("T%s  %s" % (tid, name)).strip() if tid else (name or "(tool without ID)")


def tree(jl):
    """[(compound job or None, [toolpaths])] in tree order."""
    out, seen = [], set()
    try:
        for cj in jl.GetCompoundJobs():
            js = []
            for j in cj.GetJobs():
                if key_of(j) not in seen:
                    seen.add(key_of(j)); js.append(j)
            out.append((cj, js))
    except Exception:
        log("compound jobs not read:", traceback.format_exc())
    loose = []
    try:
        for j in jl.GetJobs():
            if key_of(j) not in seen:
                seen.add(key_of(j)); loose.append(j)
    except Exception:
        pass
    if loose:
        out.append((None, loose))
    return out


# ---------------- the light bulb ----------------
def on_value(v):
    """True / False / None (unknown) for a bulb value: '1' / '0', True / False, 1 / 0."""
    v = getattr(v, "Value", v)
    if isinstance(v, bool):
        return v
    if isinstance(v, (int, float)):
        return bool(v) if v in (0, 1) else None
    s = text(v).lower()
    return {"1": True, "0": False, "true": True, "false": False}.get(s)


def read_cfg(obj):
    try:
        cfg = obj.GetCfgParameters()
        return cfg.get(CFG_KEY) if CFG_KEY in cfg else None
    except Exception:
        return None


def read_prop(obj):
    try:
        return obj.GetProperty(PROP_KEY)
    except Exception:
        return None


def get_state(obj, route):
    return on_value(read_cfg(obj) if route == "cfg" else read_prop(obj))


def set_state(obj, route, on):
    """Switches the bulb; '' or the error."""
    try:
        if route == "cfg":
            obj.SetCfgParameters({CFG_KEY: "1" if on else "0"})
        else:
            old = read_prop(obj)
            new = (bool(on) if isinstance(old, bool) else (1 if on else 0) if isinstance(old, int) else ("1" if on else "0"))
            obj.SetProperty(PROP_KEY, new)
        return ""
    except Exception as e:
        return str(e)[:160]


# ---------------- safety check ----------------
def load_rc():
    for d in LIB_DIRS:
        p = os.path.normpath(os.path.join(d, "release_check.py"))
        if os.path.isfile(p):
            spec = importlib.util.spec_from_file_location("sst_release_check", p)
            m = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(m)
            return m
    return None


def snapshot(job, folder, rc):
    """What would tell us hyperMILL counted the switch as a change: status, POF status, toolpath id, .ccrpt present."""
    s = {"status": enum_name(val(getattr(job, "Status", ""))), "pof_status": enum_name(val(getattr(job, "POFStatus", ""))),
         "ucid": "", "ccrpt": None}
    if rc is None:
        return s
    try:
        pof = rc.pof_path(job, folder)
        if pof and os.path.isfile(pof):
            s["ucid"] = rc.read_ucid(pof) or ""
            if s["ucid"]:
                d = os.path.dirname(pof)
                s["ccrpt"] = any(n.lower() == s["ucid"].lower() + ".ccrpt" for n in os.listdir(d))
    except Exception as e:
        log("snapshot:", str(e)[:120])
    return s


def changed(before, after):
    out = []
    for k, what in (("status", "status"), ("pof_status", "calculation status"), ("ucid", "toolpath id")):
        if before[k] != after[k]:
            out.append("%s %s -> %s" % (what, before[k] or "-", after[k] or "-"))
    if before["ccrpt"] and not after["ccrpt"]:
        out.append("Simulation Center result (.ccrpt) deleted")
    return out


def run():
    try:
        d = OUT_DIR if os.path.isdir(OUT_DIR) else tempfile.gettempdir()
        _f[0] = open(os.path.join(d, LOGNAME), "w", encoding="utf-8")
    except Exception:
        _f[0] = None
    try:
        import om
        log(TITLE, "v2", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        doc = om.Application().CurrentDocument
        if doc is None:
            info("No document open."); return
        path = text(doc.FullPath)
        folder = os.path.dirname(path)
        log("document:", path)
        lists = list(doc.CamModel.JobListSet.GetJobLists())
        names = [text(jl.Name) for jl in lists]
        if not names:
            info("No joblists in this document."); return
        scopes = names + (["All joblists"] if len(names) > 1 else [])
        trees = [tree(jl) for jl in lists]
        tools, count = {}, {}
        for tr in trees:
            for _, js in tr:
                for j in js:
                    t = tool_of(j)
                    if t is not None:
                        k = key_of(t)
                        tools.setdefault(k, t)
                        count[k] = count.get(k, 0) + 1
        if not tools:
            info("No toolpath in this document has a tool."); return

        def sort_key(k):
            lab = tool_label(tools[k])
            m = re.match(r"^T(\d+)", lab)
            return (0, int(m.group(1)), lab) if m else (1, 0, lab)
        tkeys = sorted(tools, key=sort_key)
        tlabels = ["%s  - %d toolpath%s" % (tool_label(tools[k]), count[k], "" if count[k] == 1 else "s") for k in tkeys]
        g = _gui()
        dlg = g.InputDialog(TITLE)
        dlg.AddDropDown("Joblist", scopes, defaultIndex=len(scopes) - 1)
        dlg.AddDropDown("Tool", tlabels, defaultIndex=0)
        dlg.AddDropDown("Show", MODES, defaultIndex=0)
        ok, v = dlg.Show()
        if not ok:
            log("cancelled"); return
        scope = scopes[pick(v.get("Joblist"), scopes)]
        tk = tkeys[pick(v.get("Tool"), tlabels)]
        mode = pick(v.get("Show"), MODES)
        log("joblist:", scope, "| tool:", tool_label(tools[tk]), "| show:", MODES[mode])
        groups = [grp for (n, tr) in zip(names, trees) if scope in ("All joblists", n) for grp in tr]
        mine = lambda j: mode == 2 or (tool_of(j) is not None and key_of(tool_of(j)) == tk)

        # ---- 1. read both candidates on every toolpath (nothing changed yet) ----
        rows, cfg_on, prop_on = [], [], []
        for cj, js in groups:
            for j in js:
                c, p = read_cfg(j), read_prop(j)
                nm = text(getattr(j, "Name", ""))
                rows.append("  %-50s %-10s %-6s %s" % (nm[:50], text(getattr(tool_of(j), "ID", "")) if tool_of(j) else "-", repr(c), repr(p)))
                if on_value(c):
                    cfg_on.append(nm)
                if on_value(p):
                    prop_on.append(nm)
        log("before (name | tool | %s | %s):" % (CFG_KEY, PROP_KEY))
        for r in rows:
            log(r)
        if cfg_on:
            route, why = "cfg", "%s reads on for: %s" % (CFG_KEY, ", ".join(cfg_on[:6]))
        elif prop_on:
            route, why = "prop", "%s reads on for: %s" % (PROP_KEY, ", ".join(prop_on[:6]))
        else:
            route, why = ROUTE, "no toolpath reads on before the change: used %s (ROUTE)" % (CFG_KEY if ROUTE == "cfg" else PROP_KEY)
        log("light bulb:", route, "|", why)
        output("\n".join(["%s - toolpaths that read ON before the change:" % TITLE, "  %s: %s" % (CFG_KEY, ", ".join(cfg_on) or "none"),
                          "  %s: %s" % (PROP_KEY, ", ".join(prop_on) or "none"), "", "every toolpath (name | tool | %s | %s):" % (CFG_KEY, PROP_KEY)] + rows))
        targets = [(j, mine(j)) for cj, js in groups for j in js if mine(j) or mode == 0]
        todo = [(j, want) for j, want in targets if get_state(j, route) is not want]
        cjs = [(cj, any(mine(j) for j in js)) for cj, js in groups if cj is not None]
        cjs = [(cj, want) for cj, want in cjs if (want or mode == 0) and (read_cfg(cj) if route == "cfg" else read_prop(cj)) is not None]
        if not todo:
            info("Nothing to switch: the toolpaths are already as asked.\n\n" + why); return

        # ---- 2. safety: one toolpath alone, checked ----
        rc = load_rc() if SAFETY_TEST else None
        if SAFETY_TEST:
            snaps = [(j, w, snapshot(j, folder, rc)) for j, w in todo]
            # one WITH a Simulation Center result, so a deleted result shows here (one B program to re-simulate at worst)
            test = (next(((j, w, s) for j, w, s in snaps if w and s["ccrpt"]), None)
                    or next(((j, w, s) for j, w, s in snaps if s["ccrpt"]), None) or snaps[0])
            j, w, before = test
            old = get_state(j, route)
            err = set_state(j, route, w)
            events()
            after = snapshot(j, folder, rc)
            now = get_state(j, route)
            ch = changed(before, after)
            log("safety test on %r: %s -> %s | before %s | after %s | %s" % (text(j.Name), old, now, before, after, err or "no error"))
            if err or ch or now is not w:
                if not err and now is not old:
                    set_state(j, route, bool(old))
                    events()
                msg = ["Stopped after one toolpath: %s" % text(j.Name)]
                if err:
                    msg.append("The switch was refused: " + err)
                elif now is not w:
                    msg.append("%s did not change (reads %r). It is not the light bulb: send %s." % (CFG_KEY if route == "cfg" else PROP_KEY, now, LOGNAME))
                if ch:
                    msg += ["hyperMILL counted the switch as a change to the toolpath:"] + ["  " + c for c in ch] + [
                        "It was switched back; nothing else was touched."]
                    if any("ccrpt" in c for c in ch):
                        msg.append("Re-simulate that B program: its Simulation Center result is gone.")
                info("\n".join(msg)); return
            todo = [(jj, ww) for jj, ww in todo if jj is not j]
            log("safety test passed")

        # ---- 3. the rest ----
        failed, wrong = [], []
        for cj, want in cjs:
            if get_state(cj, route) is not want:
                e = set_state(cj, route, want)
                if e:
                    failed.append("%s: %s" % (text(cj.Name), e))
        for j, want in todo:
            e = set_state(j, route, want)
            if e:
                failed.append("%s: %s" % (text(j.Name), e))
        events()
        for j, want in targets:
            if get_state(j, route) is not want:
                wrong.append(text(j.Name))
        on_n = sum(1 for _, w in targets if w)
        off_n = sum(1 for _, w in targets if not w)
        log("on:", on_n, "| off:", off_n, "| failed:", failed, "| read back wrong:", wrong)
        what = "Every toolpath" if mode == 2 else tool_label(tools[tk])
        msg = ["%s: %d toolpath%s on%s." % (what, on_n, "" if on_n == 1 else "s", (", %d off" % off_n) if off_n else ""),
               "", "Light bulb: " + why]
        if failed or wrong:
            msg += ["", "%d not switched (see %s): %s" % (len(failed) + len(wrong), LOGNAME, ", ".join((failed + wrong)[:5]))]
        msg += ["", "If the toolpaths do not show, click into the job list once (screen refresh)."]
        info("\n".join(msg))
    except Exception:
        log("FAILED:", traceback.format_exc())
        try:
            info("Failed. See %s." % LOGNAME)
        except Exception:
            pass
    finally:
        if _f[0]:
            try:
                _f[0].close()
            except Exception:
                pass
            _f[0] = None


if __name__ == "__main__":
    run()
