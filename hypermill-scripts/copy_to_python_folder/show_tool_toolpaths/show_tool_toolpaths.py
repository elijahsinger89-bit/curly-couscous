# show_tool_toolpaths.py - hyperMILL 35
# Turns on the toolpath display (the light bulb in the job tree) for every toolpath of one tool.
# Screen: Joblist (one or all), Tool (T<ID>  name  - number of toolpaths), Show:
#   "This tool only"   this tool's toolpaths on, every other toolpath off
#   "Add this tool"    this tool's toolpaths on, the others left as they are
#   "Everything on"    every toolpath on (the tool is not used)
# Compound jobs (B programs) holding a toolpath of the tool are turned on first, then each toolpath is set.
#
# The light bulb is not in our API notes (a Job has no display member in the release_probe dump). The script tries,
# in this order, and uses the first that works:
#   1. a display member on the job (DISPLAY_PROPS / DISPLAY_SETTERS / DISPLAY_PAIRS below)
#   2. the job's property set: GetProperty / SetProperty with a display name
#   3. the job tree nodes (JobList.GetJobTreeNodes): a display member on the toolpath's node
#   4. om.cad.UnhideEntity / HideEntity on the job
# The log says which one was used. If none works nothing is changed and the log lists what a toolpath, its
# property set and its tree node offer: send the log. Job settings (GetCfgParameters) are never changed.
# Log (written line by line): C:\Users\Public\Documents\OPEN MIND\show_tool_toolpaths_log.txt
import os, re, tempfile, traceback, datetime

# ---------------- SETTINGS ----------------
OUT_DIR = r"C:\Users\Public\Documents\OPEN MIND"
DISPLAY_PROPS = ("ToolpathVisible", "ToolPathVisible", "IsToolpathVisible", "IsToolPathVisible", "ShowToolpath",
                 "ShowToolPath", "ToolpathVisibility", "ToolPathVisibility", "ToolpathDisplay", "DisplayToolpath",
                 "Visible", "IsVisible", "Visibility", "Shown", "IsShown")
DISPLAY_SETTERS = ("SetToolpathVisible", "SetToolPathVisible", "SetToolpathVisibility", "SetToolPathVisibility",
                   "SetVisible", "SetVisibility", "SetShown")
DISPLAY_PAIRS = (("ShowToolpath", "HideToolpath"), ("ShowToolPath", "HideToolPath"), ("Show", "Hide"))
# ------------------------------------------

TITLE = "Show toolpaths of one tool"
LOGNAME = "show_tool_toolpaths_log.txt"
MODES = ["This tool only", "Add this tool", "Everything on"]
AUTO_RE = re.compile(r"visib|bulb", re.I)                                   # other members tried as the light bulb
LOOK_RE = re.compile(r"visib|show|display|hide|bulb|shown|draw|light|lamp", re.I)   # only listed in the log
NODES = {}                                                                  # UUID -> job tree node
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


def key_of(o):
    return text(getattr(o, "UUID", "")) or str(id(o))


def tool_of(job):
    try:
        return job.GetTool()
    except Exception:
        return None


def tool_label(t):
    """T<ID>  name"""
    tid = ""
    for a in ("ID", "Number"):
        tid = text(getattr(t, a, ""))
        if tid:
            break
    name = text(getattr(t, "Name", ""))
    return ("T%s  %s" % (tid, name)).strip() if tid else (name or "(tool without ID)")


def members(obj):
    try:
        return sorted(m for m in dir(obj) if not m.startswith("_"))
    except Exception:
        return []


def log_members(title, obj):
    m = members(obj)
    log("%s  %s (%d members):" % (title, type(obj).__name__, len(m)))
    for i in range(0, len(m), 8):
        log("  " + ", ".join(m[i:i + 8]))
    log("  display-looking:", [x for x in m if LOOK_RE.search(x)] or "none")


def tree(jl):
    """[(compound job or None, [toolpaths])] in tree order: compound jobs first, then toolpaths outside them."""
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


# ---------------- finding the light bulb ----------------
def as_bool(v):
    """True / False for a display value (bool, 0 / 1, 'true' / 'false'), else None."""
    v = getattr(v, "Value", v)
    if isinstance(v, bool):
        return v
    if isinstance(v, int) and v in (0, 1):
        return bool(v)
    s = text(v).lower()
    return {"true": True, "false": False, "1": True, "0": False}.get(s)


def find_member(obj):
    """1. / 3. a display member: ("prop", name), ("set", name), ("pair", (on, off)) or None."""
    names = members(obj)
    props = [n for n in DISPLAY_PROPS if n in names] + \
            [n for n in names if AUTO_RE.search(n) and n not in DISPLAY_PROPS and not n.startswith("Set")]
    for n in props:
        log("  reading %s.%s" % (type(obj).__name__, n))
        try:
            v = getattr(obj, n)
        except Exception as e:
            log("    -> error", e); continue
        if callable(v) or not isinstance(v, (bool, int)):
            log("    -> not a yes / no value:", repr(v)[:80]); continue
        try:
            setattr(obj, n, v)                         # same value back: checks it can be written
            return ("prop", n)
        except Exception as e:
            log("    -> read only (%s)" % e)
    for n in list(DISPLAY_SETTERS) + [n for n in names if n.startswith("Set") and AUTO_RE.search(n[3:])]:
        if callable(getattr(obj, n, None)):
            return ("set", n)
    for on, off in DISPLAY_PAIRS:
        if callable(getattr(obj, on, None)) and callable(getattr(obj, off, None)):
            return ("pair", (on, off))
    return None


def bag_names(obj):
    """Names in the job's property set (PropertySet / GetPropertySet), as far as they can be listed."""
    ps = None
    for a in ("PropertySet", "GetPropertySet"):
        if not hasattr(obj, a):
            continue
        try:
            log("  reading %s.%s" % (type(obj).__name__, a))
            ps = val(getattr(obj, a))
            if ps is not None:
                log_members("  property set", ps)
                break
        except Exception as e:
            log("    -> error", e)
    if ps is None:
        return []
    items = None
    try:
        items = list(ps)
    except Exception:
        for a in ("GetNames", "Names", "GetPropertyNames", "PropertyNames", "Keys", "keys", "GetProperties",
                  "Properties", "GetAll", "Items"):
            if not hasattr(ps, a):
                continue
            try:
                items = list(val(getattr(ps, a)))
                log("  listed with", a)
                break
            except Exception as e:
                log("  %s -> error %s" % (a, e))
    out = []
    for it in items or []:
        n = it if isinstance(it, str) else (text(getattr(it, "Name", "")) or text(getattr(it, "name", "")))
        if n:
            out.append(n)
    log("  property names (%d):" % len(out), ", ".join(out[:300]) or "none listed")
    return out


def find_bag(obj):
    """2. ("bag", name) when GetProperty(name) gives a yes / no value and SetProperty takes it back."""
    if not (callable(getattr(obj, "GetProperty", None)) and callable(getattr(obj, "SetProperty", None))):
        return None
    names = bag_names(obj)
    for n in [x for x in names if AUTO_RE.search(x)] + [x for x in DISPLAY_PROPS if x not in names]:
        try:
            v = obj.GetProperty(n)
        except Exception as e:
            log("  GetProperty(%r) -> error %s" % (n, str(e)[:100])); continue
        log("  GetProperty(%r) -> %r" % (n, v))
        b = as_bool(v)
        if b is None:
            continue
        try:
            obj.SetProperty(n, b)
            return ("bag", n)
        except Exception as e:
            log("  SetProperty(%r, %r) -> error %s" % (n, b, str(e)[:100]))
    return None


def children(nd):
    for a in ("GetChildren", "Children", "GetChildNodes", "ChildNodes", "GetNodes", "Nodes", "GetSubNodes"):
        if hasattr(nd, a):
            try:
                return list(val(getattr(nd, a)) or [])
            except Exception:
                pass
    return []


def node_key(nd):
    """UUID of the job / compound job a tree node stands for."""
    for a in ("Job", "GetJob", "CompoundJob", "GetCompoundJob", "Entity", "GetEntity", "Object", "GetObject",
              "Item", "GetItem", "CamEntity", "GetCamEntity"):
        if hasattr(nd, a):
            try:
                o = val(getattr(nd, a))
                k = text(getattr(o, "UUID", "")) if o is not None else ""
                if k:
                    return k
            except Exception:
                pass
    for a in ("UUID", "EntityUUID", "JobUUID", "ObjectUUID"):
        k = text(getattr(nd, a, ""))
        if k:
            return k
    return ""


def find_node(lists, sample):
    """3. ("node", how): a display member on the job tree node of the toolpath."""
    first, total = None, 0
    for jl in lists:
        try:
            log("  reading %s.GetJobTreeNodes()" % text(jl.Name))
            todo = list(jl.GetJobTreeNodes() or [])
        except Exception as e:
            log("    -> error", str(e)[:200]); continue
        depth = 0
        while todo and depth < 8:
            nxt = []
            for nd in todo:
                total += 1
                first = first or nd
                k = node_key(nd)
                if k:
                    NODES[k] = nd
                nxt += children(nd)
            todo, depth = nxt, depth + 1
    log("  job tree nodes: %d, matched to a job: %d" % (total, len(NODES)))
    if first is not None:
        log_members("  first node", first)
    nd = NODES.get(key_of(sample))
    if nd is None:
        log("  no node for the first toolpath")
        return None
    how = find_member(nd)
    return ("node", how) if how else None


def find_cad(sample):
    """4. ("cad", as_list): om.cad.UnhideEntity takes the toolpath. Tried on a toolpath that goes on anyway."""
    try:
        import om.cad as c
    except Exception:
        return None
    for n in ("UnhideEntity", "HideEntity"):
        log("  om.cad.%s: %s" % (n, (text(getattr(getattr(c, n, None), "__doc__", "")) or "no help text")[:300]))
    if not (callable(getattr(c, "UnhideEntity", None)) and callable(getattr(c, "HideEntity", None))):
        return None
    for as_list in (False, True):
        try:
            r = c.UnhideEntity([sample] if as_list else sample)
            log("  UnhideEntity(%s) -> %r" % ("[toolpath]" if as_list else "toolpath", r))
            if r is not False:
                return ("cad", as_list)
        except Exception as e:
            log("  UnhideEntity(%s) -> error %s" % ("[toolpath]" if as_list else "toolpath", str(e)[:200]))
    return None


# ---------------- switching ----------------
def switch(obj, how, on):
    """Turns the display of obj on / off. Returns '' or the error."""
    kind, n = how
    if kind == "node":
        nd = NODES.get(key_of(obj))
        return switch(nd, n, on) if nd is not None else "no job tree node"
    try:
        if kind == "prop":
            setattr(obj, n, bool(on))
        elif kind == "set":
            getattr(obj, n)(bool(on))
        elif kind == "pair":
            getattr(obj, n[0] if on else n[1])()
        elif kind == "bag":
            obj.SetProperty(n, bool(on))
        elif kind == "cad":
            import om.cad as c
            f = c.UnhideEntity if on else c.HideEntity
            f([obj]) if n else f(obj)
        return ""
    except Exception as e:
        return str(e)[:160]


def is_on(obj, how):
    """The display state as read back, or None when it cannot be read."""
    kind, n = how
    try:
        if kind == "node":
            nd = NODES.get(key_of(obj))
            return is_on(nd, n) if nd is not None else None
        if kind == "prop":
            return bool(getattr(obj, n))
        if kind == "bag":
            return as_bool(obj.GetProperty(n))
    except Exception:
        pass
    return None


def refresh():
    try:
        import om.cad as c
        c.RefreshView()
        return
    except Exception as e:
        log("RefreshView:", str(e)[:120])
    try:
        _gui().ProcessEvents()
    except Exception:
        pass


def run():
    try:
        d = OUT_DIR if os.path.isdir(OUT_DIR) else tempfile.gettempdir()
        _f[0] = open(os.path.join(d, LOGNAME), "w", encoding="utf-8")
    except Exception:
        _f[0] = None
    try:
        import om
        log(TITLE, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        doc = om.Application().CurrentDocument
        if doc is None:
            info("No document open."); return
        log("document:", text(doc.FullPath))
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

        sel = [i for i, n in enumerate(names) if scope == "All joblists" or n == scope]
        groups = [grp for i in sel for grp in trees[i]]
        mine = lambda j: mode == 2 or (tool_of(j) is not None and key_of(tool_of(j)) == tk)
        own = [j for _, js in groups for j in js if mine(j)]
        if not own:
            info("%s has no toolpaths in %s." % (tool_label(tools[tk]), scope)); return
        sample = own[0]
        log("finding the light bulb on:", text(getattr(sample, "Name", "")))
        how = None
        for step, find in (("1. member on the toolpath", lambda: find_member(sample)),
                           ("2. property set of the toolpath", lambda: find_bag(sample)),
                           ("3. job tree node", lambda: find_node([lists[i] for i in sel], sample)),
                           ("4. om.cad Unhide / Hide", lambda: find_cad(sample))):
            log(step)
            try:
                how = find()
            except Exception:
                log("  failed:", traceback.format_exc())
            if how:
                break
        log("light bulb:", how or "NOT FOUND")
        if how is None:
            log_members("toolpath", sample)
            try:
                cfg = sample.GetCfgParameters()
                log("  job settings like display (not changed):",
                    {k: x for k, x in cfg.items() if LOOK_RE.search(k)} or "none")
            except Exception:
                pass
            cj0 = next((cj for cj, _ in groups if cj is not None), None)
            if cj0 is not None:
                log_members("compound job", cj0)
            info("The toolpath display (light bulb) was not found, so nothing was changed.\n\n"
                 "Send %s (it lists what a toolpath offers)." % LOGNAME)
            return

        # mode "Add this tool": what the other toolpaths show now, to put back if a compound job switch changes them
        before = {}
        if mode == 1:
            for _, js in groups:
                for j in js:
                    if not mine(j):
                        before[key_of(j)] = is_on(j, how)
        on_n, off_n, failed, cj_err = 0, 0, [], []
        for cj, js in groups:
            if cj is not None:
                any_mine = any(mine(j) for j in js)
                if any_mine or mode == 0:
                    err = switch(cj, how, any_mine)
                    if err:
                        cj_err.append("%s: %s" % (text(getattr(cj, "Name", "")), err))
            for j in js:
                want = mine(j)
                if not want and mode == 1:
                    b = before.get(key_of(j))
                    if b is not None and is_on(j, how) != b:
                        switch(j, how, b)             # put back
                    continue
                err = switch(j, how, want)
                if err:
                    failed.append("%s: %s" % (text(getattr(j, "Name", "")), err))
                elif want:
                    on_n += 1
                else:
                    off_n += 1
        refresh()
        wrong = [text(getattr(j, "Name", "")) for _, js in groups for j in js
                 if (mine(j) or mode == 0) and is_on(j, how) is not None and is_on(j, how) != mine(j)]
        log("on:", on_n, "| off:", off_n, "| failed:", len(failed), "| read back wrong:", len(wrong))
        for f in failed:
            log("  FAILED", f)
        for w in wrong:
            log("  READ BACK WRONG", w)
        for e in cj_err:
            log("  compound job not switched:", e)
        what = "Every toolpath" if mode == 2 else tool_label(tools[tk])
        msg = ["%s: %d toolpath%s on%s." % (what, on_n, "" if on_n == 1 else "s", (", %d off" % off_n) if off_n else "")]
        if failed or wrong:
            msg += ["", "%d could not be switched (see %s)." % (len(failed) + len(wrong), LOGNAME)]
        if how[0] in ("set", "pair", "cad") or (how[0] == "node" and how[1][0] != "prop"):
            msg += ["", "If the light bulbs did not change, send %s." % LOGNAME]
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
