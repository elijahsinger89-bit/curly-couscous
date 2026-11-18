#!/usr/bin/env python3
"""Headless test of restore_job_names.py (fake om in tests/fake_om). Run: python3 tests/test_restore_job_names.py"""
import os
import sys
import tempfile
import importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(HERE, "fake_om"))
import om                      # noqa: E402  (fake)
import om.cad.gui as gui       # noqa: E402  (fake)

SCRIPT = os.path.join(ROOT, "copy_to_python_folder", "restore_job_names", "restore_job_names.py")
fails = []


def check(cond, label):
    print(("ok   " if cond else "FAIL ") + label)
    if not cond:
        fails.append(label)


class HJob(om.Job):
    """A real-shaped job: number in *JOBID, type in LocCycleName; mode 'name' / 'cfg' (Name follows *JOBNAME) / 'stuck'."""
    def __init__(self, name, tool, jobid, cycle, mode="name"):
        self._mode = "name"
        om.Job.__init__(self, name, tool, {"*JOBID": jobid, "*JOBNAME": name} if jobid is not None else {"*JOBNAME": name})
        self._name, self.LocCycleName, self._mode = name, cycle, mode
        self.UUID = "J-%s" % name

    @property
    def Name(self):
        return self._name

    @Name.setter
    def Name(self, v):
        if self._mode == "name":
            self._name = v
        elif self._mode == "stuck":
            raise RuntimeError("read-only")

    def SetCfgParameters(self, d):
        if self._mode == "cfg" and "*JOBNAME" in d:
            self._name = d["*JOBNAME"]


tmp = tempfile.mkdtemp(prefix="rjn_")
tempfile.tempdir = tmp
T = om.Tool
t1, t2 = T("905080900", "Ceramic"), T("903080900", "Turn")


def build():
    jobs = [HJob("2: T905080900 ROUGH CERAMIC TURN TOP FACE_2", t1, "2", "Contour Turning"),
            HJob("3: 3d Optimized Royghibg", t1, "3", "3D Optimized Roughing"),
            HJob("T2 ROUGH CERAMIC TURN UNDER OD FLANGE", t1, "4", "Contour Turning", mode="cfg"),
            HJob("5: 2D Contour", t2, "5", "2D Contour"),                      # already right
            HJob("OP4 T903080900 ROUGH CERAMIC TURN ID", t2, None, "Contour Turning"),   # no *JOBID, no number in name
            HJob("6: whatever", t2, None, "Contour Turning"),                  # no *JOBID: number from the name
            HJob("7: stuck name", t2, "7", "Pocket Milling", mode="stuck"),
            HJob("8: no type", t2, "8", "")]
    cs = [om.CompoundJob("B_00948602_025_020_HF5", jobs[:2]), om.CompoundJob("B_00948602_025_030_HF5", jobs[2:4]),
          om.CompoundJob("RGH ID & Bottom +0.040", []), om.CompoundJob("B_00948602_025_080_HF5", jobs[4:])]
    om._App.CurrentDocument = om.Document(os.path.join(tmp, "doc.hmc"), om.Model([om.JobList("Op4", cs)]))
    return jobs, cs


def run(answers):
    gui.SCRIPT[:] = answers
    gui.BOXES.clear(); gui.SHOWN.clear()
    spec = importlib.util.spec_from_file_location("rjn_under_test", SCRIPT)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    m.OUT_DIR = tmp
    m.run()
    left = len(gui.SCRIPT)
    gui.SCRIPT.clear()
    return left


def first(fmt=0):
    return lambda dlg: (True, {"Joblist": 0, "Name format": fmt})


def rename(yes):
    return lambda dlg: (True, {"Rename": 1 if yes else 0})


jobs, cs = build()
left = run([first(), rename(True)])
names = [j.Name for j in jobs]
check(left == 0 and names == ["2: Contour Turning", "3: 3D Optimized Roughing", "4: Contour Turning", "5: 2D Contour",
                              "OP4 T903080900 ROUGH CERAMIC TURN ID", "6: Contour Turning", "7: stuck name", "8: no type"],
      "restored to N: Type (number from *JOBID, else the name); %s" % names)
check([c.Name for c in cs] == ["B_00948602_025_020_HF5", "B_00948602_025_030_HF5", "RGH ID & Bottom +0.040", "B_00948602_025_080_HF5"],
      "compound jobs (B programs, dividers) untouched")
box = gui.BOXES[-1]
check("Renamed 4 toolpaths." in box and "1 already named right." in box and "2 left alone" in box and
      "Could not rename:" in box and "7: stuck name" in box, "message: renamed, already right, left alone, failed")
out = "\n".join(gui.OUTPUT)
check("2: T905080900 ROUGH CERAMIC TURN TOP FACE_2" in out and "->  2: Contour Turning" in out and "(no job number)" in out and
      "(no toolpath type)" in out, "output window: old -> new list and reasons")
logt = open(os.path.join(tmp, "restore_job_names_log.txt")).read()
check("renamed  3: 3d Optimized Royghibg -> 3: 3D Optimized Roughing  (Name)" in logt and
      "renamed  T2 ROUGH CERAMIC TURN UNDER OD FLANGE -> 4: Contour Turning  (*JOBNAME)" in logt, "log: old -> new and how (Name / *JOBNAME)")

# answer No: nothing changes
jobs, cs = build()
left = run([first(), rename(False)])
check(left == 0 and jobs[0].Name == "2: T905080900 ROUGH CERAMIC TURN TOP FACE_2" and "Nothing renamed." in gui.BOXES[-1], "No: nothing renamed")

# tool ID format
jobs, cs = build()
left = run([first(1), rename(True)])
check(jobs[0].Name == "2: T905080900 Contour Turning" and jobs[3].Name == "5: T903080900 2D Contour", "format N: T<tool ID> Type")

# second run: only the toolpath that could not be renamed is offered again
left = run([first(1), rename(False)])
check(left == 0 and "1 to rename, 5 already right, 2 left alone." in "\n".join(gui.OUTPUT), "second run: only the stuck toolpath left to rename")
jobs, cs = build()
for j in jobs:
    if j._mode == "stuck":
        j._mode = "name"
run([first(), rename(True)])
left = run([first()])
check(left == 0 and "Nothing to rename" in gui.BOXES[-1], "run after everything is right: nothing to rename, no question")

print()
print("FAILURES: %d" % len(fails) if fails else "ALL RESTORE JOB NAMES CHECKS PASSED")
sys.exit(1 if fails else 0)
