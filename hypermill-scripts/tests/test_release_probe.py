#!/usr/bin/env python3
"""Headless test of release_probe.py (fake om in tests/fake_om): read-only, finds signatures and differing status.
Run: python3 tests/test_release_probe.py"""
import os
import sys
import enum
import shutil
import tempfile
import importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(HERE, "fake_om"))
import om                      # noqa: E402  (fake)
import om.cad.gui as gui       # noqa: E402  (fake)

SCRIPT = os.path.join(ROOT, "copy_to_python_folder", "release_probe", "release_probe.py")
fails = []
CALLED = []


def check(cond, label):
    print(("ok   " if cond else "FAIL ") + label)
    if not cond:
        fails.append(label)


class SimJob(om.Job):
    """A job with the kind of members the real API may have."""
    def __init__(self, name, tool, simulated):
        om.Job.__init__(self, name, tool, {"*AUFMASS": "0", "*SIM_STATUS": "1" if simulated else "0"})
        self._sim = simulated

    def IsSimulated(self):
        return self._sim

    def GetCalculationState(self):
        return "CALCULATED"

    def PostProcess(self, path):
        """PostProcess(self: om.cam.Job, path: str) -> bool  Writes the NC file."""
        CALLED.append("PostProcess")
        raise RuntimeError("the probe must never call this")

    def Simulate(self):
        """Simulate(self) -> None"""
        CALLED.append("Simulate")


class PostList(om.JobList):
    def PostCompoundJobs(self, jobs, folder):
        """PostCompoundJobs(self, jobs: list, folder: str) -> int  Posts the compound jobs."""
        CALLED.append("PostCompoundJobs")

    def GetNcFileMode(self):
        return "COMPOUNDJOB_AS_SINGLE_JOB"


om.SimulationState = enum.Enum("SimulationState", "NOT_SIMULATED SIMULATED COLLISION")

tmp = tempfile.mkdtemp(prefix="rp_")
tempfile.tempdir = tmp
docdir = os.path.join(tmp, "job")
os.makedirs(os.path.join(docdir, "sim"))
doc = os.path.join(docdir, "PART_OP200.hmc")
for p in (doc, os.path.join(docdir, "sim", "PART_OP200.simresult")):
    open(p, "w").close()
fm = om.Tool("905083900", "Facemill", "faceMill", 2.0)
cs = [om.CompoundJob("---- note ----"),
      om.CompoundJob("B_PART_010_HF5", [SimJob("a", fm, True), SimJob("b", fm, True)]),
      om.CompoundJob("B_PART_020_HF5", [SimJob("c", fm, False)])]
om._App.CurrentDocument = om.Document(doc, om.Model([PostList("OP200", cs)]))

spec = importlib.util.spec_from_file_location("rp_under_test", SCRIPT)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
gui.BOXES.clear()
m.run()
logp = os.path.join(tmp, "release_probe_log.txt")
check(os.path.exists(logp), "log written (fallback folder)")
txt = open(logp, encoding="utf-8").read()
check("FAILED" not in txt, "probe ran without an error")
check(CALLED == [], "nothing called: Post / Simulate never run (%s)" % CALLED)
check("PostProcess(self: om.cam.Job, path: str) -> bool" in txt, "job posting signature in the log")
check("PostCompoundJobs(self, jobs: list, folder: str) -> int" in txt, "joblist posting signature in the log")
check("enum SimulationState: NOT_SIMULATED, SIMULATED, COLLISION" in txt, "status enum listed with its values")
check("module om.cad.gui" in txt, "submodules listed")
dif = [ln for ln in txt.splitlines() if "DIFFERS" in ln]
check(any("J.IsSimulated" in ln and "True x2" in ln and "False x1" in ln for ln in dif), "summary: IsSimulated differs (True x2, False x1)")
check(any("J.cfg *SIM_STATUS" in ln for ln in dif), "summary: cfg *SIM_STATUS differs")
check(any("same" in ln and "J.GetCalculationState" in ln for ln in txt.splitlines()), "summary: a value that never changes is marked same")
check("(note, empty)" in txt, "note compound job shown as a note")
check(os.path.join("sim", "PART_OP200.simresult") in txt, "files next to the document listed")
check("=== 6. FIRST JOB IN FULL ===" in txt and "def   PostProcess" in txt, "first job dumped in full, write methods listed not called")
check("Send the log" in gui.BOXES[-1] and "Simulation Center" in gui.BOXES[-1], "final message asks for the log")

shutil.rmtree(tmp, ignore_errors=True)
print()
print("FAILURES: %d" % len(fails) if fails else "ALL RELEASE PROBE CHECKS PASSED")
sys.exit(1 if fails else 0)
