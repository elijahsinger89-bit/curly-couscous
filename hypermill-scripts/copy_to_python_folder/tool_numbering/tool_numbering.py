# tool_numbering.py - hyperMILL 35. Tool numbers of the open document to a numbering standard (tool_library\tool_numbers.py).
# Screen 1: Standard (HELLER M_ / T_; COMPANY_X 9-digit: rule not set yet), Tools from (one joblist, all joblists, every
#   tool in the document), Apply (unticked = list only, the default).
# Per tool: kept when its ID follows the standard and matches the tool (type, diameter); else a new ID:
#   milling M_[type][diameter][variant][copy]: the type from its old M_ number when it has one, else from the hyperMILL
#   tool type and geometry; a radius mill over 1.25 in (could be a face / hi-feed mill built as a bullnose) and a tap
#   (cut or form) are asked. Turning T_[type][ISO][hand][variant][copy]: type, insert ISO and hand are asked.
#   Variant = the first free one (1-9) among every tool of the document; copy 0 (sisters are DUPLO on the control).
# Screen 2 (only when needed): the asked tools, 4 per screen.
# The list (old -> new, why) goes to the output window and the log. Apply writes the new NC-Number and ID through
#   temporary numbers first (hyperMILL refuses a duplicate NC-Number) - APPLY_METHOD below must be set from the
#   tool_field_probe log; until then Apply says so and nothing changes.
# After renumbering, the posted B programs, the tool load MDA and the B program list hold the old names: post again.
# Log: C:\Users\Public\Documents\OPEN MIND\tool_numbering_log.txt
import os, re, sys, tempfile, traceback, datetime, importlib

# ---------------- SETTINGS ----------------
APPLY_METHOD = ""        # "" = list only (until the tool_field_probe log shows how); "fields" = set Number and ID on the tool
BIG_RADIUS_MILL_IN = 1.25
# ------------------------------------------
PY_DIR = r"C:\Users\Public\Documents\OPEN MIND\python"
OUT_DIR = r"C:\Users\Public\Documents\OPEN MIND"
HERE = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.path.join(PY_DIR, "tool_numbering")
LIB_DIRS = [os.path.join(PY_DIR, "tool_library"), os.path.join(HERE, "..", "tool_library")]
TITLE = "Tool numbering"
STD_LABELS = ["HELLER (M_ milling, T_ turning)", "COMPANY_X (9-digit) - rule not set yet"]
STD_KEYS = ["HELLER", "COMPANY_X"]
PER_SCREEN = 4
lines = []


def log(*a):
    lines.append(" ".join(str(x) for x in a))


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


def output(t):
    g = _gui()
    try:
        g.CleanOutput(g.UIOutputWindow.ALL)
        g.WriteToOutput(t, g.UIOutputWindow.ALL)
        g.ProcessEvents()
    except Exception:
        pass


def pick(v, options):
    if isinstance(v, int) and not isinstance(v, bool):
        return v if 0 <= v < len(options) else 0
    return options.index(v) if v in options else 0


def load_lib():
    d = next((os.path.normpath(x) for x in LIB_DIRS if os.path.isfile(os.path.join(x, "tool_numbers.py"))), None)
    if d is None:
        raise RuntimeError("tool_library (tool_numbers.py) not found")
    if d not in sys.path:
        sys.path.insert(0, d)
    mods = {}
    for n in ("tool_numbers", "tool_info"):
        m = importlib.import_module(n)
        importlib.reload(m)
        mods[n] = m
    return mods


def tools_of(model, lists, choice):
    """(tools, source) for the 'Tools from' choice."""
    if choice == "All tools in the document":
        return list(model.ToolSet.GetTools())
    out, seen = [], set()
    for jl in lists:
        if choice not in ("All joblists", text(jl.Name)):
            continue
        for j in jl.GetJobs():
            try:
                t = j.GetTool()
            except Exception:
                t = None
            if t is not None and text(t.UUID) not in seen:
                seen.add(text(t.UUID))
                out.append(t)
    return out


ISO_RE = re.compile(r"\b([CDKRSTVW])([ABCDEFHMNOPRS])[A-Z]{0,2}[ -]?\d")


def iso_guess(i):
    """Two insert letters (CN, DC ...) from the insert designation in the tool / holder comment, or ''."""
    for s in [i.get("tool_comment", "")] + [h.get("comment", "") for h in i.get("holders", [])]:
        m = ISO_RE.search(str(s).upper())
        if m:
            return m.group(1) + m.group(2)
    return ""


def plan(infos, tn):
    """[{tool, info, old, new, why, ask}] - new None until asked. Milling only gets a type here; turning is asked."""
    rows = []
    for t, i in infos:
        old = i["id"]
        p = tn.parse(old)
        r = dict(tool=t, info=i, old=old, new=None, why="", ask=None, code=None)
        if i["turning"]:
            if p and p["kind"] == "T":
                r["new"], r["why"] = old, "kept (T_ standard)"
            else:
                r["ask"] = "turning"
                r["why"] = "turning tool: type, insert and hand asked"
            rows.append(r)
            continue
        dia = i.get("dia")
        if dia is None:
            r["why"] = "no diameter in the tool: left as it is"
            r["new"] = old
            rows.append(r)
            continue
        if p and p["kind"] == "M" and abs(p["dia_in"] - round(dia, 3)) < 0.0006:
            r["new"], r["why"] = old, "kept (follows the standard)"
            rows.append(r)
            continue
        if p and p["kind"] == "M":
            r["code"], sure = p["type"], True
            r["why"] = "type %02d from the old number; its diameter %s is not the tool's %s" % (p["type"], tn.inch(p["dia_in"]), tn.inch(dia))
        else:
            r["code"], sure = tn.type_from_hm(i.get("type"), dia, i.get("corner_r") or 0, i.get("angle") if i.get("angle_kind") == "point" else None)
            if r["code"] in (10, 11) and dia > BIG_RADIUS_MILL_IN:
                sure = False
            r["why"] = "type %02d %s from the hyperMILL %s" % (r["code"], tn.MILL_TYPES.get(r["code"], ""), i.get("type") or "tool")
        if not sure:
            r["ask"] = "milling"
        rows.append(r)
    return rows


MILL_ASK = [10, 11, 12, 13, 40, 41, 42, 43, 44, 46, 47, 70, 71, 99]


def ask(rows, tn):
    """Screen 2: asked tools PER_SCREEN at a time. Fills r['code'] (milling) or r['turn'] (turning). False = cancelled."""
    todo = [r for r in rows if r["ask"]]
    g = _gui()
    m_opts = ["%02d %s" % (c, tn.MILL_TYPES[c]) for c in MILL_ASK]
    t_opts = ["%02d %s" % (c, n) for c, n in sorted(tn.TURN_TYPES.items())]
    hands = ["R", "L", "N"]
    for s in range(0, len(todo), PER_SCREEN):
        page = todo[s:s + PER_SCREEN]
        dlg = g.InputDialog("%s | tools %d-%d of %d asked" % (TITLE, s + 1, s + len(page), len(todo)))
        for r in page:
            i = r["info"]
            tag = "%s %s" % (r["old"], (i.get("nc_name") or i.get("tool_name") or "")[:40])
            if r["ask"] == "milling":
                cur = "%02d %s" % (r["code"], tn.MILL_TYPES.get(r["code"], ""))
                dlg.AddDropDown(tag + "  type", m_opts, defaultIndex=m_opts.index(cur) if cur in m_opts else 0)
            else:
                dlg.AddDropDown(tag + "  turning type", t_opts, defaultIndex=0)
                dlg.AddText(tag + "  insert ISO (2 letters)", defaultValue=iso_guess(i))
                dlg.AddDropDown(tag + "  hand", hands, defaultIndex=0)
        ok, v = dlg.Show()
        if not ok:
            return False
        for r in page:
            i = r["info"]
            tag = "%s %s" % (r["old"], (i.get("nc_name") or i.get("tool_name") or "")[:40])
            if r["ask"] == "milling":
                r["code"] = MILL_ASK[pick(v.get(tag + "  type"), m_opts)]
                r["why"] = "type %02d %s (asked)" % (r["code"], tn.MILL_TYPES[r["code"]])
            else:
                code = sorted(tn.TURN_TYPES)[pick(v.get(tag + "  turning type"), t_opts)]
                iso = re.sub(r"[^A-Z]", "", text(v.get(tag + "  insert ISO (2 letters)")).upper())[:2]
                r["turn"] = (code, iso, hands[pick(v.get(tag + "  hand"), hands)])
                r["why"] = "turning %02d %s, insert %s, hand %s (asked)" % (code, tn.TURN_TYPES[code], iso or "?", r["turn"][2])
    return True


def assign(rows, tn, all_ids):
    """New IDs: the first free variant among every ID of the document that stays."""
    renamed = set(r["old"].upper() for r in rows if r["new"] is None)
    used = set(x.upper() for x in all_ids if x.upper() not in renamed)
    for r in rows:
        if r["new"] is not None:
            continue
        try:
            if r.get("turn"):
                c, iso, hand = r["turn"]
                make = lambda v, c=c, iso=iso, hand=hand: tn.turn_id(c, iso, hand, v, 0)
            else:
                d = r["info"]["dia"]
                make = lambda v, c=r["code"], d=d: tn.mill_id(c, d, v, 0)
            new = tn.free_variant(make, used)
        except ValueError as e:
            r["new"], r["why"] = r["old"], "not renumbered: %s" % e
            continue
        if new is None:
            r["new"], r["why"] = r["old"], "not renumbered: variants 1-9 all used"
            continue
        r["new"] = new
        used.add(new.upper())


def apply_numbers(rows, tn):
    """Writes the new NC-Number and ID (APPLY_METHOD 'fields'), through temporary numbers. Returns (done, failed)."""
    change = [r for r in rows if r["new"] != r["old"]]
    if APPLY_METHOD != "fields":
        return [], [(r["old"], "Apply is not set up yet (APPLY_METHOD, from the tool_field_probe log)") for r in change]
    done, failed = [], []
    base = 990000000
    for k, r in enumerate(change):                          # 1: temporary numbers, so no two tools share one on the way
        try:
            r["tool"].Number = base + k
            r["tool"].ID = "TMP_%d" % k
        except Exception as e:
            failed.append((r["old"], "temporary number refused: %s" % str(e)[:120]))
            r["skip"] = True
    for r in change:                                         # 2: the new numbers
        if r.get("skip"):
            continue
        try:
            r["tool"].Number = tn.number_of(r["new"])
            r["tool"].ID = r["new"]
            done.append(r)
        except Exception as e:
            failed.append((r["old"], "refused: %s" % str(e)[:120]))
    return done, failed


def run():
    try:
        import om
        log(TITLE, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "| apply method:", APPLY_METHOD or "(list only)")
        mods = load_lib()
        tn, ti = mods["tool_numbers"], mods["tool_info"]
        doc = om.Application().CurrentDocument
        if doc is None:
            info("No document open."); return
        model = doc.CamModel
        lists = list(model.JobListSet.GetJobLists())
        names = [text(jl.Name) for jl in lists]
        sources = names + (["All joblists"] if len(names) > 1 else []) + ["All tools in the document"]
        g = _gui()
        dlg = g.InputDialog(TITLE)
        dlg.AddDropDown("Standard", STD_LABELS, defaultIndex=0)
        dlg.AddDropDown("Tools from", sources, defaultIndex=len(sources) - 1)
        dlg.AddBool("Apply (unticked = list only)", False)
        ok, v = dlg.Show()
        if not ok:
            log("cancelled"); return
        std = STD_KEYS[pick(v.get("Standard"), STD_LABELS)]
        src = sources[pick(v.get("Tools from"), sources)]
        do_apply = bool(v.get("Apply (unticked = list only)"))
        log("standard:", std, "| tools from:", src, "| apply:", do_apply)
        if not tn.STANDARD_READY.get(std):
            info("%s: %s.\n\nSend the rule and it will be added." % (std, tn.NOT_READY)); return
        tools = tools_of(model, lists, src)
        if not tools:
            info("No tools in %s." % src); return
        tmpd = tempfile.mkdtemp(prefix="tool_numbering_")
        infos = [(t, ti.read(t, tmpd)) for t in tools]
        all_ids = [text(getattr(t, "ID", "")) for t in model.ToolSet.GetTools()]
        rows = plan(infos, tn)
        if any(r["ask"] for r in rows) and not ask(rows, tn):
            log("cancelled on the asked tools"); return
        assign(rows, tn, all_ids)
        change = [r for r in rows if r["new"] != r["old"]]
        rep = ["%s  %s  %s" % (TITLE, std, src), "", "%-14s %-14s %s" % ("old ID", "new ID", "why")]
        for r in rows:
            rep.append("%-14s %-14s %s" % (r["old"], r["new"] if r["new"] != r["old"] else "(kept)", r["why"]))
        for ln in rep:
            log(ln)
        output("\n".join(rep))
        msg = ["%d tool%s: %d to renumber, %d kept. The full list is in the output window." % (
            len(rows), "" if len(rows) == 1 else "s", len(change), len(rows) - len(change))]
        msg += ["  %s -> %s" % (r["old"], r["new"]) for r in change[:12]] + (["  ..."] if len(change) > 12 else [])
        if change and do_apply:
            done, failed = apply_numbers(rows, tn)
            log("applied:", len(done), "| failed:", failed)
            if done:
                msg += ["", "Renumbered %d tool%s." % (len(done), "" if len(done) == 1 else "s"),
                        "Post the B programs again and make a new tool load MDA and B program list (Go to machine):",
                        "the old ones hold the old tool names."]
            if failed:
                msg += ["", "Not changed (%d):" % len(failed)] + ["  %s: %s" % f for f in failed[:8]]
        elif change:
            msg += ["", "List only: nothing changed. Tick Apply to renumber."]
        info("\n".join(msg))
    except Exception:
        log("FAILED:", traceback.format_exc())
        try:
            info("Failed. See tool_numbering_log.txt.")
        except Exception:
            pass
    finally:
        try:
            d = OUT_DIR if os.path.isdir(OUT_DIR) else tempfile.gettempdir()
            with open(os.path.join(d, "tool_numbering_log.txt"), "w", encoding="utf-8") as f:
                f.write("\n".join(lines) + "\n")
        except Exception:
            pass


if __name__ == "__main__":
    run()
