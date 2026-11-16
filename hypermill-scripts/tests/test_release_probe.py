#!/usr/bin/env python3
"""Headless test of release_probe.py v3 (fake om in tests/fake_om).
Built-in hyperMILL methods are imitated by functions marked _native that reject an unknown keyword the way pybind11
does (the real mechanism was checked against a compiled pybind11 module: argument lists back, nothing run).
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
RAN = []             # native methods that actually ran (must stay empty)
SEEN = {}


def check(cond, label):
    print(("ok   " if cond else "FAIL ") + label)
    if not cond:
        fails.append(label)


def native(sig):
    """A fake built-in method: an unknown keyword is rejected before running, listing sig like pybind11."""
    def deco(fn):
        def wrapper(self, *a, **kw):
            known = set(fn.__code__.co_varnames[1:fn.__code__.co_argcount])
            if set(kw) - known:
                raise TypeError("%s(): incompatible function arguments. The following argument types are supported:\n"
                                "    1. %s\n\nInvoked with: <obj>, kwargs: %s" % (fn.__name__, sig, kw))
            RAN.append(fn.__name__)
            return fn(self, *a, **kw)
        wrapper._native = True
        wrapper.__name__ = fn.__name__
        return wrapper
    return deco


class PS(enum.Enum):
    UP_TO_DATE = 0
    NEEDS_CALCULATION = 3


class JS(enum.Enum):
    UP_TO_DATE = 1
    WARNINGS = 3


tmp = tempfile.mkdtemp(prefix="rp_")
tempfile.tempdir = tmp
LOGP = os.path.join(tmp, "release_probe_log.txt")


class SimJob(om.Job):
    slow_reads = 0

    def __init__(self, name, tool, pof_ok, slow=False):
        om.Job.__init__(self, name, tool, {})
        self._pof, self._slow = pof_ok, slow

    @property
    def POFStatus(self):
        if "log_at_first_read" not in SEEN:
            SEEN["log_at_first_read"] = open(LOGP, encoding="utf-8").read() if os.path.exists(LOGP) else ""
        return PS.UP_TO_DATE if self._pof else PS.NEEDS_CALCULATION

    @property
    def Status(self):
        if self._slow:
            SimJob.slow_reads += 1
            time.sleep(0.6)
        return JS.UP_TO_DATE

    @property
    def PofFileName(self):
        return r"C:\job\POF\00948602-025_B_OP200_02_%s.pof" % self.Name.split(":")[0]

    @native("(self: om.cam._hmCoreX64.Job) -> bool")
    def CheckPofStatus(self):
        return True

    @native("(self: om.cam._hmCoreX64.Job, propName: str) -> bool")
    def HasError(self, propName):
        return False

    @native("(self: om.cam._hmCoreX64.Job, params: dict) -> None")
    def SetCfgParameters(self, params):
        return None


class FakeCompound(om.CompoundJob):
    @native("(self: om.cam._hmCoreX64.CompoundJob) -> bool")
    def HasNcStatus(self):
        return False

    @native("(self: om.cam._hmCoreX64.CompoundJob) -> om.cam._hmCoreX64.NcInfo")
    def GetGenerateAndReleaseNcInfo(self):
        return None


class FakeJobList(om.JobList):
    @native("(self: om.cam._hmCoreX64.JobList, path: str) -> bool")
    def GenerateNCListFile(self, path):
        return True

    @native("(self: om.cam._hmCoreX64.JobList) -> None")
    def DeleteAllJobs(self):
        return None


class FakeJobListSet(om.JobListSet):
    @native("(self: om.cam._hmCoreX64.JobListSet, jobLists: list, folder: str) -> bool")
    def CalculateNC(self, jobLists, folder):
        return True

    @native("(self: om.cam._hmCoreX64.JobListSet) -> None")
    def RunAll(self):
        return None


docdir = os.path.join(tmp, "job")
for d in ("VNC", "POF", "NC"):
    os.makedirs(os.path.join(docdir, d))
doc = os.path.join(docdir, "PART_OP200.hmc")
open(doc, "w").close()
with open(os.path.join(docdir, "VNC", "00948602-025_B_OP200_02.nclist"), "w", encoding="utf-8") as f:
    f.write("B_PART_010_HF5\nB_PART_1240_HF5\n")
with open(os.path.join(docdir, "POF", "00948602-025_B_OP200_02_410.pof"), "w") as f:
    f.write("x")
with open(os.path.join(docdir, "NC", "B_PART_010_HF5.mpf"), "w") as f:
    f.write("x")

fm = om.Tool("905083900", "Facemill", "faceMill", 2.0)
cs = [FakeCompound("---- note ----"),
      FakeCompound("B_PART_010_HF5", [SimJob("1: rough", fm, True, slow=True), SimJob("2: rough", fm, True, slow=True)])]
cs += [FakeCompound("B_PART_%03d_HF5" % (20 + 10 * i), [SimJob("%d: finish" % (400 + i), fm, i % 2 == 0)]) for i in range(80)]
model = om.Model([FakeJobList("00948602-025_B_OP200_02", cs)])
model.JobListSet = FakeJobListSet(model.JobListSet.GetJobLists())
om._App.CurrentDocument = om.Document(doc, model)

spec = importlib.util.spec_from_file_location("rp_under_test", SCRIPT)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
real_is_native = m.is_native
m.is_native = lambda raw: getattr(raw, "_native", False) or real_is_native(raw)
m.SLOW = 0.5
gui.BOXES.clear()
om.WRITES.clear()
m.run()
txt = open(LOGP, encoding="utf-8").read()

check("FAILED" not in txt and txt.rstrip().endswith("finished"), "probe ran to the end without an error")
check(set(RAN) == {"HasNcStatus"} and not om.WRITES, "only the HasNcStatus status read ran, nothing written (%s)" % sorted(set(RAN)))
check("def   CalculateNC(self: om.cam._hmCoreX64.JobListSet, jobLists: list, folder: str) -> bool" in txt,
      "CalculateNC arguments listed without running it")
check("def   RunAll(self: om.cam._hmCoreX64.JobListSet) -> None" in txt, "RunAll (no arguments) listed without running it")
check("def   GenerateNCListFile(self: om.cam._hmCoreX64.JobList, path: str) -> bool" in txt, "GenerateNCListFile arguments")
check("def   GetGenerateAndReleaseNcInfo(self: om.cam._hmCoreX64.CompoundJob) -> om.cam._hmCoreX64.NcInfo" in txt,
      "GetGenerateAndReleaseNcInfo arguments and return type")
check("def   HasError(self: om.cam._hmCoreX64.Job, propName: str) -> bool" in txt, "job method arguments")
check("def   SetCfgParameters  (changes the document: arguments not asked)" in txt and
      "def   DeleteAllJobs  (changes the document: arguments not asked)" in txt, "write methods: name only, never called")
check("def   GetJobs  (not a built-in method: skipped)" in txt, "plain Python method: skipped")
check("prop  POFStatus" in txt, "properties listed")
check("reading Job.POFStatus" in SEEN.get("log_at_first_read", ""), "log on disk before the first read")
check("'B_PART_810_HF5'" in txt, "every compound job scanned (81, no 60 cap)")
check("J '400: finish'" in txt and "POFStatus=UP_TO_DATE" in txt and "POFStatus=NEEDS_CALCULATION" in txt
      and "PofFileName=00948602-025_B_OP200_02_401.pof" in txt, "job line: Status, POFStatus, POF file name")
check("POFStatus=NEEDS_CALCULATION" in txt and "POFStatus=UP_TO_DATE " in txt.replace("\n", " ") and
      any(ln.strip().startswith("POFStatus=UP_TO_DATE") and ln.strip().endswith("42") for ln in txt.splitlines()),
      "totals: POFStatus counts (2 + 40 up to date)")
check(SimJob.slow_reads == 1 and "SLOW: Job.Status took" in txt and "Status=<slow before: not read>" in txt,
      "slow member read once, then skipped")
check("    | B_PART_1240_HF5" in txt, "VNC .nclist text printed")
check("00948602-025_B_OP200_02_410.pof" in txt and "B_PART_010_HF5.mpf" in txt, "newest POF and NC files listed")
check("Send the log" in gui.BOXES[-1], "final message asks for the log")

shutil.rmtree(tmp, ignore_errors=True)
print()
print("FAILURES: %d" % len(fails) if fails else "ALL RELEASE PROBE CHECKS PASSED")
sys.exit(1 if fails else 0)
