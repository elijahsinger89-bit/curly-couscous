#!/usr/bin/env python3
"""Every hyperMILL script folder in copy_to_python_folder must carry what hyperMILL needs to run it:
  .om\\configuration.json   Type Script, StartupFile = a .py in the folder
  .vscode\\settings.json, tasks.json, launch.json   (settings name the folder's own libs path)
and every script zip must hold those files for the scripts it holds.
Folders that are not scripts: tool_library, icons. Run: python3 tests/test_script_folders.py"""
import os
import sys
import json
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CP = os.path.join(ROOT, "copy_to_python_folder")
NOT_SCRIPTS = {"tool_library", "icons"}
VSCODE = ("settings.json", "tasks.json", "launch.json")
fails = []


def check(cond, label):
    print(("ok   " if cond else "FAIL ") + label)
    if not cond:
        fails.append(label)


scripts = sorted(d for d in os.listdir(CP) if os.path.isdir(os.path.join(CP, d)) and d not in NOT_SCRIPTS and not d.startswith((".", "_")))
for d in scripts:
    p = os.path.join(CP, d)
    cfg = os.path.join(p, ".om", "configuration.json")
    ok = os.path.isfile(cfg)
    if ok:
        c = json.load(open(cfg, encoding="utf-8"))
        ok = c.get("Type") == "Script" and os.path.isfile(os.path.join(p, c.get("StartupFile", "")))
    check(ok, "%s: .om\\configuration.json with its startup file" % d)
    vs = [os.path.isfile(os.path.join(p, ".vscode", n)) for n in VSCODE]
    st = os.path.join(p, ".vscode", "settings.json")
    check(all(vs) and ("/python/%s/libs" % d) in open(st, encoding="utf-8").read(), "%s: .vscode settings / tasks / launch" % d)

for z in sorted(n for n in os.listdir(ROOT) if n.endswith(".zip")):
    names = set(zipfile.ZipFile(os.path.join(ROOT, z)).namelist())
    held = sorted(set(n.split("/")[1] for n in names if n.startswith("copy_to_python_folder/") and n.endswith(".py")
                      and n.split("/")[1] in scripts))
    missing = ["%s/%s" % (d, f) for d in held for f in [".om/configuration.json"] + [".vscode/" + v for v in VSCODE]
               if "copy_to_python_folder/%s/%s" % (d, f) not in names]
    check(not missing, "%s: .om / .vscode for %s%s" % (z, ", ".join(held) or "(no scripts)", (" - MISSING " + ", ".join(missing)) if missing else ""))

print("\n%d failed" % len(fails) if fails else "\nALL SCRIPT FOLDER CHECKS PASSED")
sys.exit(1 if fails else 0)
