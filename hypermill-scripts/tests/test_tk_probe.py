#!/usr/bin/env python3
"""Headless test of tk_probe.py (fake om in tests/fake_om; a virtual display from Xvfb).
Needs a Python WITH tkinter for the 'worked' cases (TK_PY, default /usr/bin/python3.12) and one WITHOUT it (NO_TK_PY);
cases whose interpreter is missing are skipped and say so. The window closes itself (TKPROBE_AUTOCLOSE).
Run: python3 tests/test_tk_probe.py"""
import os
import sys
import time
import shutil
import tempfile
import subprocess
import importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(HERE, "fake_om"))
import om.cad.gui as gui       # noqa: E402  (fake)

SCRIPT = os.path.join(ROOT, "copy_to_python_folder", "tk_probe", "tk_probe.py")
TK_PY = os.environ.get("TK_PY", "/usr/bin/python3.12")
NO_TK_PY = os.environ.get("NO_TK_PY", "/usr/bin/python3.13")
tmp = tempfile.mkdtemp(prefix="tkp_")
tempfile.tempdir = tmp
LOG = os.path.join(tmp, "tk_probe_log.txt")
fails = []


def check(cond, label):
    print(("ok   " if cond else "FAIL ") + label)
    if not cond:
        fails.append(label)


def has_tk(py):
    return os.path.isfile(py) and subprocess.call([py, "-c", "import tkinter"], stderr=subprocess.DEVNULL) == 0


xvfb = None
if not os.environ.get("DISPLAY") and shutil.which("Xvfb"):
    xvfb = subprocess.Popen(["Xvfb", ":97", "-screen", "0", "1024x768x24"], stderr=subprocess.DEVNULL)
    os.environ["DISPLAY"] = ":97"
    time.sleep(1.0)
os.environ["TKPROBE_AUTOCLOSE"] = "1"


def run(a=True, b=False, cands=None):
    gui.SCRIPT[:] = [lambda d: (True, {d.fields[0][1]: a, d.fields[1][1]: b})]
    gui.BOXES.clear(); gui.SHOWN.clear()
    spec = importlib.util.spec_from_file_location("tkp_under_test", SCRIPT)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    if cands is not None:
        m.candidates = lambda: [(p, "test") for p in cands]
    m.run()
    return gui.BOXES[-1], open(LOG, encoding="utf-8").read()


# ---- screen and the always-on environment part
box, lg = run(a=False, b=False)
check(gui.SHOWN[0][0].startswith("tkinter probe") and [f[1] for f in gui.SHOWN[0][1]] == [
      "A: window in a separate Python (safe)", "B: window inside hyperMILL (save your work first)"]
      and [f[2] for f in gui.SHOWN[0][1]] == [True, False], "screen: A on, B off by default")
check("python:" in lg and "sys.path:" in lg and "import tkinter in hyperMILL's Python:" in lg and "Nothing in hyperMILL was changed" in box,
      "environment logged, message says nothing changed")

# ---- test A with a Python that has tkinter: window opens, choice comes back
if has_tk(TK_PY) and os.environ.get("DISPLAY"):
    box, lg = run(cands=[TK_PY])
    check("A: WORKED - " + TK_PY in box and "Choice handed back: Sandvik / 930-HA10-S-20-100 / stick-out 1.250" in box,
          "A with tkinter: window opened in a separate process, choice handed back")
    check('"ok": true' in lg and "exit code 0" in lg, "A: result file and exit code in the log")
else:
    print("skip A-worked: no Python with tkinter (%s) or no display" % TK_PY)

# ---- test A with a Python without tkinter: says why
if os.path.isfile(NO_TK_PY) and not has_tk(NO_TK_PY):
    box, lg = run(cands=[NO_TK_PY])
    check("A: did not work." in box and "No module named 'tkinter'" in box, "A without tkinter: did not work, the reason shown")
else:
    print("skip A-failed: no Python without tkinter (%s)" % NO_TK_PY)

# ---- no candidates
box, lg = run(cands=[])
check("A: no python.exe found" in box, "A: no python found: says so")

# ---- test B (window inside the probe's own Python): run the probe outside hyperMILL with a Python that has tkinter
if has_tk(TK_PY) and os.environ.get("DISPLAY"):
    env = dict(os.environ, TKPROBE_TESTS="B")
    out = subprocess.run([TK_PY, SCRIPT], env=env, capture_output=True, text=True, timeout=60).stdout
    check("B: WORKED inside hyperMILL, Tk" in out and "Sandvik / 930-HA10-S-20-100 / stick-out 1.250" in out,
          "B: window inside the same Python works (outside hyperMILL here)")
box, lg = run(a=False, b=True)
if "OK" not in box.split("\n")[0]:
    check("B: skipped (tkinter is not in hyperMILL's Python)" in box, "B skipped when the running Python has no tkinter")

if xvfb:
    xvfb.terminate()
shutil.rmtree(tmp, ignore_errors=True)
print("\n%d failed" % len(fails) if fails else "\nALL TK PROBE CHECKS PASSED")
sys.exit(1 if fails else 0)
