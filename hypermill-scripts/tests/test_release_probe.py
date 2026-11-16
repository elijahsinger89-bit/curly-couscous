#!/usr/bin/env python3
"""Headless test of release_probe.py v2 (fake om in tests/fake_om): read-only, nothing imported, log written line by
line, signatures listed, status compared, slow members read once, 60 compound job cap.
Run: python3 tests/test_release_probe.py"""
import os
import sys
import enum
import time
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
CALLED = []          # members the probe must never run
SEEN = {}            # evidence gathered inside reads


def check(cond, label):
    print(("ok   " if cond else "FAIL ") + label)
    if not cond:
        fails.append(label)


tmp = tempfile.mkdtemp(prefix="rp_")
tempfile.tempdir = tmp
LOGP = os.path.join(tmp, "release_probe_log.txt")


class SimJob(om.Job):
    """A job with the kind of members the real API may have."""
    slow_calls = 0

    def __init__(self, name, tool, simulated):
        om.Job.__init__(self, name, tool, {"*AUFMASS": "0", "*SIM_STATUS": "1" if simulated else "0"})
        self._sim = simulated

    def IsSimulated(self):
        if "log_at_first_read" not in SEEN:
            SEEN["log_at_first_read"] = open(LOGP, encoding="utf-8").read() if os.path.exists(LOGP) else ""
        return self._sim

    def GetCalculationState(self):
        return "CALCULATED"

    def IsSlowCheck(self):
        SimJob.slow_calls += 1
        time.sleep(0.6)
        return True

    def GetMachiningTime(self):
        CALLED.append("GetMachiningTime")
        return 12.5

    def Isolate(self):
        CALLED.append("Isolate")

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

    def GetPostprocessorName(self):
        CALLED.append("GetPostprocessorName")
        return "SIEMENS_ONE"


class HeavyDoc(om.Document):
    def GetBoundingBox(self):
        CALLED.append("Document.GetBoundingBox")

    def IsModified(self):
        CALLED.append("Document.IsModified")
        return True


om.SimulationState = enum.Enum("SimulationState", "NOT_SIMULATED SIMULATED COLLISION")

docdir = os.path.join(tmp, "job")
os.makedirs(os.path.join(docdir, "sim"))
doc = os.path.join(docdir, "PART_OP200.hmc")
for p in (doc, os.path.join(docdir, "sim", "PART_OP200.simresult")):
    open(p, "w").close()
fm = om.Tool("905083900", "Facemill", "faceMill", 2.0)
cs = [om.CompoundJob("---- note ----"),
      om.CompoundJob("B_PART_010_HF5", [SimJob("a", fm, True), SimJob("b", fm, True)]),
      om.CompoundJob("B_PART_020_HF5", [SimJob("c", fm, False)])]
many = [om.CompoundJob("B_PART_%03d_HF5" % (100 + i), [SimJob("m%d" % i, fm, False)]) for i in range(70)]
om._App.CurrentDocument = HeavyDoc(doc, om.Model([PostList("OP200", cs), PostList("OP300", many)]))

before = set(k for k in sys.modules if k == "om" or k.startswith("om."))
spec = importlib.util.spec_from_file_location("rp_under_test", SCRIPT)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
gui.BOXES.clear()
t = time.perf_counter()
m.run()
took = time.perf_counter() - t
after = set(k for k in sys.modules if k == "om" or k.startswith("om."))
check(os.path.exists(LOGP), "log written (fallback folder)")
txt = open(LOGP, encoding="utf-8").read()
check("FAILED" not in txt and txt.rstrip().endswith("finished"), "probe ran to the end without an error")
check(CALLED == [], "nothing run that is not a status read: %s" % CALLED)
check(after == before, "no om module imported (%s)" % sorted(after - before))
check("reading SimJob.IsSimulated" in SEEN.get("log_at_first_read", ""), "log is on disk before each read of the first job (freeze shows where)")
check("PostProcess(self: om.cam.Job, path: str) -> bool" in txt, "job posting signature in the log")
check("PostCompoundJobs(self, jobs: list, folder: str) -> int" in txt, "joblist posting signature in the log")
check("GetPostprocessorName" in txt, "joblist NC member listed (not called)")
check("enum SimulationState: NOT_SIMULATED, SIMULATED, COLLISION" in txt, "status enum listed with its values")
check("module om.cad.gui" in txt, "already loaded submodules listed")
check("GetNcFileMode = 'COMPOUNDJOB_AS_SINGLE_JOB'" in txt, "NC file mode read")
dif = [ln for ln in txt.splitlines() if "DIFFERS" in ln]
check(any("J.IsSimulated" in ln and "False x" in ln and "True x2" in ln for ln in dif), "summary: IsSimulated differs")
check(any("J.cfg *SIM_STATUS" in ln for ln in dif), "summary: cfg *SIM_STATUS differs")
check(any("same" in ln and "J.GetCalculationState" in ln for ln in txt.splitlines()), "summary: a value that never changes is marked same")
check(SimJob.slow_calls == 1 and "SLOW: SimJob.IsSlowCheck took" in txt, "slow member read once, then skipped")
check("(stopped after 60 compound jobs)" in txt and "B_PART_157_HF5" in txt and "'B_PART_158_HF5'" not in txt,
      "scan stops after 60 compound jobs")
check(took < 10, "probe finished in %.1f s" % took)
check("(note, empty)" in txt, "note compound job shown as a note")
check(os.path.join("sim", "PART_OP200.simresult") in txt, "files next to the document listed")
check("Send the log" in gui.BOXES[-1] and "Simulation Center" in gui.BOXES[-1], "final message asks for the log")

shutil.rmtree(tmp, ignore_errors=True)
print()
print("FAILURES: %d" % len(fails) if fails else "ALL RELEASE PROBE CHECKS PASSED")
sys.exit(1 if fails else 0)
