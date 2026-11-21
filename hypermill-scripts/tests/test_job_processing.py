#!/usr/bin/env python3
"""Headless test of job_processing.py (the front-of-job menu). Run: python3 tests/test_job_processing.py"""
import os
import sys
import json
import tempfile
import importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(HERE, "fake_om"))
import om                      # noqa: E402  (fake)
import om.cad.gui as gui       # noqa: E402  (fake)

SCRIPT = os.path.join(ROOT, "copy_to_python_folder", "job_processing", "job_processing.py")
tmp = tempfile.mkdtemp(prefix="jp_")
tempfile.tempdir = tmp
fails = []


def check(cond, label):
    print(("ok   " if cond else "FAIL ") + label)
    if not cond:
        fails.append(label)


# stand-in scripts: each run() records that it ran, and the module is fresh each time
scripts = os.path.join(tmp, "python")
for folder in ("tool_center", "part_wizard_1", "b_program_rename"):
    os.makedirs(os.path.join(scripts, folder))
    with open(os.path.join(scripts, folder, folder + ".py"), "w") as f:
        f.write("import os, tempfile\nCOUNT = 0\n"
                "def run():\n    global COUNT\n    COUNT += 1\n"
                "    open(os.path.join(tempfile.gettempdir(), 'ran.txt'), 'a').write('%s %d\\n' % (os.path.basename(__file__), COUNT))\n"
                "if __name__ == '__main__':\n    run()\n")
with open(os.path.join(scripts, "part_wizard_1", "part_wizard_1.py"), "a") as f:
    f.write("def run():\n    raise RuntimeError('boom')\n")


def run(choice):
    gui.SCRIPT[:] = [lambda d: (True, {"What": choice}) if choice is not None else (False, {})]
    gui.BOXES.clear(); gui.SHOWN.clear()
    spec = importlib.util.spec_from_file_location("jp_under_test", SCRIPT)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    m.SCRIPT_DIRS = [scripts]
    m.run()
    return m


RAN = os.path.join(tmp, "ran.txt")
m = run(0)
labels = gui.SHOWN[0][1][0][2][0]
check(labels[0].startswith("Tools:") and any(l.startswith("Part wizard 1") for l in labels) and any(l.startswith("Tool numbering") for l in labels)
      and any("Holder attacher" in l for l in labels) and any(l.startswith("Show toolpaths") for l in labels), "menu lists the front-of-job scripts")
check(not any("Go to machine" in l or "go_to_machine" in l for l in labels), "Go to machine is the other button, not in this menu")
check(open(RAN).read() == "tool_center.py 1\n", "Tools: tool_center's run() started")
run(0)
check(open(RAN).read().splitlines()[-1] == "tool_center.py 1", "loaded fresh every time (module count starts at 1 again)")
run(5)
check(open(RAN).read().splitlines()[-1] == "b_program_rename.py 1", "B program rename started")
run(None)
check(gui.SHOWN[0][1][0][2][1] == 5, "last choice offered first (B program rename)")
run(4)
check("not built yet" in gui.BOXES[-1], "holder attacher: not built yet")
run(6)
check("is not installed" in gui.BOXES[-1] and "restore_job_names" in gui.BOXES[-1], "script not installed: says which folder to copy")
run(1)
log = open(os.path.join(tmp, "job_processing_log.txt")).read()
check("Failed." in gui.BOXES[-1] and "RuntimeError: boom" in log, "a script that fails: message, traceback in the log")
check(json.load(open(os.path.join(tmp, "job_processing_last.json")))["choice"].startswith("Part wizard 1"), "choice remembered")

print("\n%d failed" % len(fails) if fails else "\nALL JOB PROCESSING CHECKS PASSED")
sys.exit(1 if fails else 0)
