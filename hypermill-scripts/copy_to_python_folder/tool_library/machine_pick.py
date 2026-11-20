# machine_pick.py - machine model and spindle dialogs for the part wizards. The spindle's max rpm becomes
# tool_builder.MAX_RPM, which caps every speed in the cutting data (speed cut back, feed follows at the same chip load).
# The last choice is remembered in the temp folder and offered first next time.
import os, json, tempfile
import tool_builder as tb

LAST = os.path.join(tempfile.gettempdir(), "hypermill_machine_last.json")

def _load():
    try:
        with open(LAST, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def _save(d):
    try:
        with open(LAST, "w", encoding="utf-8") as f:
            json.dump(d, f)
    except Exception:
        pass

def label(r):
    return ("%s - %s rpm, %s kW, %s Nm" % (r["spindle"], r["rpm"], r["kw"], r["torque_nm"]))[:56]

def _index(v, options):
    if isinstance(v, int) and not isinstance(v, bool):
        return v if 0 <= v < len(options) else 0
    return list(options).index(v) if v in options else 0

def pick_spindle(new_dialog, title, log=None):
    """Two drop-downs: machine model, then spindle. new_dialog(title) returns an om.cad.gui.InputDialog.
    Sets tool_builder.MAX_RPM and returns the spindle row (model, spindle, rpm, kw, torque_nm ...) or None when cancelled."""
    rows = tb.load_rows("machines.csv")
    models = []
    for r in rows:
        if r["model"] not in models:
            models.append(r["model"])
    last = _load()
    while True:
        dlg = new_dialog(title)
        dlg.AddDropDown("Machine model", models, defaultIndex=models.index(last["machine"]) if last.get("machine") in models else 0)
        ok, vals = dlg.Show()
        if not ok:
            return None
        model = models[_index(vals["Machine model"], models)]
        sps = [r for r in rows if r["model"] == model]
        labels = [label(r) for r in sps] + ["<< Back"]
        names = [r["spindle"] for r in sps]
        dlg = new_dialog("%s | %s" % (title, model))
        dlg.AddDropDown("Spindle", labels, defaultIndex=names.index(last["spindle"]) if last.get("spindle") in names and last.get("machine") == model else 0)
        ok, vals = dlg.Show()
        if not ok:
            return None
        i = _index(vals["Spindle"], labels)
        if i == len(labels) - 1:
            continue
        sp = sps[i]
        tb.MAX_RPM = float(sp["rpm"])
        _save(dict(machine=model, spindle=sp["spindle"]))
        if log:
            log("machine:", model, "| spindle:", sp["spindle"], "| max rpm", sp["rpm"])
        return sp
