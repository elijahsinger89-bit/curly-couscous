# tk_probe.py - hyperMILL 35. Can the holder screens use a real window (tkinter) instead of hyperMILL's input dialogs?
# Changes NOTHING in hyperMILL: no tools, no jobs, no settings.
# Screen: two ticks
#   A  Window in a separate Python (safe)          on by default
#      Starts a separate Python process that opens a tkinter window (two linked drop-downs, a drawn holder outline,
#      a stick-out box) and hands the choice back in a file. hyperMILL waits while the window is open.
#   B  Window inside hyperMILL (save your work first)   off by default
#      The same window in hyperMILL's own Python. It can freeze hyperMILL: save first.
# Always (no window): which Python hyperMILL runs, whether "import tkinter" works in it, which python.exe files exist.
# Log: C:\Users\Public\Documents\OPEN MIND\tk_probe_log.txt (written line by line: if hyperMILL freezes, close it and
# send the log anyway)
import os, sys, json, time, shutil, tempfile, platform, traceback, subprocess, datetime

OUT_DIR = r"C:\Users\Public\Documents\OPEN MIND"
TITLE = "tkinter probe"
LOGNAME = "tk_probe_log.txt"
TIMEOUT_S = 600                      # test A: the window is closed after 10 minutes
T_A = "A: window in a separate Python (safe)"
T_B = "B: window inside hyperMILL (save your work first)"
_f = [None]

# the window (same code for test A in its own process and test B inside hyperMILL)
CHILD = r'''
import sys, json, os

# 930-HA10-S-20-100A outline from its export, mm (radius, height from the nose); the HSK contact face is at 100
OUTLINE = [(0, 149.9), (35.5, 149.9), (38.0, 100.0), (49.96, 100.0), (49.96, 71.06), (25.0, 71.0), (25.0, 53.2),
           (21.0, 49.2), (21.0, 17.2), (19.17, 1.06), (17.97, 0.0), (0, 0.0)]
HOLDERS = {"Sandvik": ["930-HA10-S-20-100", "930-HA10-HD-20-100", "930-HA10-S-12-095"],
           "REGO-FIX": ["PG 25 HSK-A100 (demo)", "ER 32 HSK-A100 (demo)"],
           "Haimer": ["A100.140.20 (demo)", "A100.140.12 (demo)"]}


def main(res_path):
    out = {"python": sys.version, "executable": sys.executable}

    def save():
        with open(res_path, "w") as f:
            json.dump(out, f)
    try:
        import tkinter as tk
        from tkinter import ttk
    except Exception as e:
        out.update(ok=False, stage="import tkinter", error=repr(e))
        save()
        return out
    out["tk"] = str(tk.TkVersion)
    try:
        root = tk.Tk()
    except Exception as e:
        out.update(ok=False, stage="open window", error=repr(e))
        save()
        return out
    out.update(ok=False, stage="window closed without OK")
    root.title("tkinter probe - holder screen demo (changes nothing)")
    try:
        root.attributes("-topmost", True)
    except Exception:
        pass
    frm = ttk.Frame(root, padding=10)
    frm.grid(sticky="nsew")
    ttk.Label(frm, text="Tool T331580900  8mm ball  -  shank 8 mm", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, columnspan=2, sticky="w")
    ttk.Label(frm, text="Manufacturer").grid(row=1, column=0, sticky="w", pady=(8, 0))
    mfg = ttk.Combobox(frm, values=sorted(HOLDERS), state="readonly", width=34)
    mfg.grid(row=2, column=0, sticky="w")
    ttk.Label(frm, text="Holder (refilters when the manufacturer changes)").grid(row=3, column=0, sticky="w", pady=(8, 0))
    hold = ttk.Combobox(frm, values=[], state="readonly", width=34)
    hold.grid(row=4, column=0, sticky="w")
    ttk.Label(frm, text="Stick-out (in)").grid(row=5, column=0, sticky="w", pady=(8, 0))
    stick = ttk.Entry(frm, width=12)
    stick.insert(0, "1.250")
    stick.grid(row=6, column=0, sticky="w")
    cv = tk.Canvas(frm, width=240, height=380, background="white", highlightthickness=1, highlightbackground="#999999")
    cv.grid(row=1, column=1, rowspan=8, padx=(14, 0))

    def draw(*_):
        cv.delete("all")
        name = hold.get()
        if not name.startswith("930-HA10-S-20-100"):
            cv.create_text(120, 190, text="outline drawn for\n930-HA10-S-20-100 only\n(probe demo)", justify="center")
            return
        k, cx, base = 2.3, 120, 360                       # px per mm, axis x, nose y
        right = [(cx + r * k, base - y * k) for r, y in OUTLINE]
        left = [(cx - r * k, base - y * k) for r, y in reversed(OUTLINE)]
        cv.create_polygon(*[c for p in right + left for c in p], fill="#d7dde3", outline="#2b2d2f")
        fy = base - 100.0 * k
        cv.create_line(10, fy, 230, fy, fill="#cd1316", dash=(4, 3))
        cv.create_text(12, fy - 8, text="HSK face (machine side)", anchor="w", fill="#cd1316")
        cv.create_text(12, base + 10, text="nose (workpiece side)", anchor="w", fill="#004288")

    def pick_mfg(*_):
        hold["values"] = HOLDERS.get(mfg.get(), [])
        hold.set(hold["values"][0] if hold["values"] else "")
        draw()
    mfg.bind("<<ComboboxSelected>>", pick_mfg)
    hold.bind("<<ComboboxSelected>>", draw)

    def ok():
        out.update(ok=True, stage="OK pressed", manufacturer=mfg.get(), holder=hold.get(), stickout=stick.get())
        root.destroy()
    btns = ttk.Frame(frm)
    btns.grid(row=8, column=0, sticky="w", pady=(16, 0))
    ttk.Button(btns, text="OK", command=ok).grid(row=0, column=0)
    ttk.Button(btns, text="Cancel", command=root.destroy).grid(row=0, column=1, padx=(8, 0))
    mfg.set("Sandvik")
    pick_mfg()
    if os.environ.get("TKPROBE_AUTOCLOSE"):               # automatic test only
        root.after(700, ok)
    root.mainloop()
    save()
    return out


if __name__ == "__main__":
    main(sys.argv[1])
'''


def log(*a):
    s = " ".join(str(x) for x in a)
    if _f[0]:
        try:
            _f[0].write(s + "\n"); _f[0].flush()
        except Exception:
            pass
    else:
        print(s)


def _gui():
    import om.cad.gui as g
    return g


def info(t):
    try:
        g = _gui()
        g.ShowMessageBox(g.MessageBoxType.INFORMATION, TITLE, t)
    except Exception:
        print(t)


def events():
    try:
        _gui().ProcessEvents()
    except Exception:
        pass


def ask():
    """(test A, test B); without hyperMILL: from TKPROBE_TESTS ('A', 'B', 'AB')."""
    try:
        g = _gui()
    except Exception:
        t = os.environ.get("TKPROBE_TESTS", "A")
        return "A" in t, "B" in t
    dlg = g.InputDialog(TITLE + " (changes nothing in hyperMILL)")
    dlg.AddBool(T_A, defaultValue=True)
    dlg.AddBool(T_B, defaultValue=False)
    ok, v = dlg.Show()
    if not ok:
        return None
    return bool(v.get(T_A)), bool(v.get(T_B))


def environment():
    log("python:", sys.version.replace("\n", " "))
    log("executable:", sys.executable)
    log("prefix:", sys.prefix, "| base_prefix:", getattr(sys, "base_prefix", ""), "| exec_prefix:", sys.exec_prefix)
    log("platform:", platform.platform())
    for k in ("PYTHONHOME", "PYTHONPATH", "TCL_LIBRARY", "TK_LIBRARY", "PATH"):
        v = os.environ.get(k, "")
        log("env %s:" % k, (v[:300] + " ...") if len(v) > 300 else (v or "-"))
    log("sys.path:")
    for p in sys.path:
        log("   ", p)
    # files that tkinter needs (Windows: Lib\tkinter, DLLs\_tkinter.pyd, tcl86t.dll, tk86t.dll, tcl\tcl8.6\init.tcl)
    found = []
    for root in sorted(set([sys.prefix, getattr(sys, "base_prefix", sys.prefix), os.path.dirname(sys.executable or "")])):
        if not root or not os.path.isdir(root):
            continue
        for d, subs, files in os.walk(root):
            if d[len(root):].count(os.sep) > 3:
                subs[:] = []
                continue
            for n in files:
                nl = n.lower()
                if nl.startswith("_tkinter") or nl.startswith(("tcl8", "tk8", "tcl9", "tk9")) or nl == "init.tcl" or \
                        (nl.startswith(("tcl", "tk")) and nl.endswith(".dll")):
                    found.append(os.path.join(d, n))
            if os.path.basename(d).lower() == "tkinter":
                found.append(d + os.sep)
    log("tkinter files under the Python folders: %d" % len(found))
    for p in found[:40]:
        log("   ", p)
    try:
        import tkinter
        log("import tkinter in hyperMILL's Python: OK | Tk", tkinter.TkVersion, "| Tcl", tkinter.TclVersion)
        return True
    except Exception as e:
        log("import tkinter in hyperMILL's Python: FAILED |", repr(e))
        return False


def candidates():
    """python executables to start test A with (never hyperMILL.exe itself)."""
    out = []

    def add(p, why):
        if p and os.path.isfile(p) and os.path.normcase(os.path.abspath(p)) not in [os.path.normcase(os.path.abspath(x)) for x, _ in out]:
            out.append((p, why))
    add(os.environ.get("TKPROBE_PYTHON", ""), "TKPROBE_PYTHON")
    exe = sys.executable or ""
    if os.path.basename(exe).lower().startswith("python"):
        add(exe, "sys.executable")
    for d in (os.path.dirname(exe), sys.prefix, getattr(sys, "base_prefix", ""), sys.exec_prefix):
        for n in ("pythonw.exe", "python.exe"):
            if d:
                add(os.path.join(d, n), "next to hyperMILL's Python")
    # hyperMILL's own interpreter (the one each script's .vscode\settings.json names), newest version first
    shared = r"C:\Program Files\OPEN MIND\Shared"
    try:
        for v in sorted(os.listdir(shared), reverse=True):
            for n in ("pythonw.exe", "python.exe"):
                add(os.path.join(shared, v, "python", n), "hyperMILL's interpreter (Shared\\%s\\python)" % v)
    except Exception:
        pass
    for n in ("pythonw", "python", "py"):
        add(shutil.which(n) or "", "on PATH")
    return out


def run_child(py, env, tag):
    """Test A with one python: (result dict or None, stderr text)."""
    tmp = tempfile.mkdtemp(prefix="tk_probe_")
    child = os.path.join(tmp, "tk_probe_window.py")
    res = os.path.join(tmp, "result.json")
    errp = os.path.join(tmp, "stderr.txt")
    with open(child, "w", encoding="utf-8") as f:
        f.write(CHILD)
    flags = 0x08000000 if os.name == "nt" else 0              # CREATE_NO_WINDOW: no console window behind it
    log("test A (%s): starting %s" % (tag, py))
    with open(errp, "w") as ef:
        p = subprocess.Popen([py, child, res], env=env, stdout=ef, stderr=ef, creationflags=flags)
        t0 = time.time()
        while p.poll() is None:
            events()
            time.sleep(0.1)
            if time.time() - t0 > TIMEOUT_S:
                p.kill()
                log("test A (%s): no answer after %d s, stopped" % (tag, TIMEOUT_S))
                break
    err = open(errp, encoding="utf-8", errors="replace").read().strip()
    log("test A (%s): exit code %s after %.1f s" % (tag, p.returncode, time.time() - t0))
    if err:
        log("test A (%s) stderr:\n%s" % (tag, err[:2000]))
    try:
        with open(res) as f:
            r = json.load(f)
        log("test A (%s) result:" % tag, json.dumps(r))
        return r, err
    except Exception:
        log("test A (%s): no result file" % tag)
        return None, err


def test_a():
    cands = candidates()
    log("python executables found: %d" % len(cands))
    for p, why in cands:
        log("   ", p, "(%s)" % why)
    if not cands:
        return "A: no python.exe found next to hyperMILL's Python or on PATH (see the log)."
    tried = []
    for py, why in cands:
        envs = [("environment as is", dict(os.environ))]
        clean = dict((k, v) for k, v in os.environ.items() if k not in ("PYTHONHOME", "PYTHONPATH"))
        if len(clean) != len(os.environ):
            envs.append(("without PYTHONHOME / PYTHONPATH", clean))
        for tag, env in envs:
            r, err = run_child(py, env, tag)
            if r and r.get("stage") not in ("import tkinter", "open window"):
                what = "%s / %s / stick-out %s" % (r.get("manufacturer"), r.get("holder"), r.get("stickout")) if r.get("ok") else "closed without OK"
                return "A: WORKED - %s (%s), Tk %s.\n   Choice handed back: %s" % (py, tag, r.get("tk"), what)
            tried.append("%s (%s): %s" % (py, tag, (r or {}).get("error") or (err.splitlines()[-1] if err else "no result")))
    return "A: did not work.\n" + "\n".join("   " + t for t in tried)


def test_b():
    log("test B: window inside hyperMILL's Python")
    ns = {"__name__": "tk_probe_inside"}
    exec(compile(CHILD, "tk_probe_window", "exec"), ns)
    res = os.path.join(tempfile.mkdtemp(prefix="tk_probe_b_"), "result.json")
    r = ns["main"](res)
    log("test B result:", json.dumps(r))
    if r.get("stage") in ("import tkinter", "open window"):
        return "B: did not work - %s: %s" % (r.get("stage"), r.get("error"))
    what = "%s / %s / stick-out %s" % (r.get("manufacturer"), r.get("holder"), r.get("stickout")) if r.get("ok") else "closed without OK"
    return "B: WORKED inside hyperMILL, Tk %s. Choice: %s" % (r.get("tk"), what)


def run():
    try:
        d = OUT_DIR if os.path.isdir(OUT_DIR) else tempfile.gettempdir()
        _f[0] = open(os.path.join(d, LOGNAME), "w", encoding="utf-8")
    except Exception:
        _f[0] = None
    try:
        log(TITLE, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        tests = ask()
        if tests is None:
            log("cancelled"); return
        a, b = tests
        log("tests: A", a, "| B", b)
        inside = environment()
        msg = ["import tkinter in hyperMILL's Python: %s" % ("OK" if inside else "not available")]
        if a:
            msg.append(test_a())
        if b:
            msg.append(test_b() if inside else "B: skipped (tkinter is not in hyperMILL's Python)")
        msg += ["", "Nothing in hyperMILL was changed. Send %s." % LOGNAME]
        log("\n".join(msg))
        info("\n".join(msg))
    except Exception:
        log("FAILED:", traceback.format_exc())
        info("Failed. Send %s." % LOGNAME)
    finally:
        if _f[0]:
            try:
                _f[0].close()
            except Exception:
                pass
            _f[0] = None


if __name__ == "__main__":
    run()
