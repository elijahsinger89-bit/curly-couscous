#!/usr/bin/env python3
"""Headless test of release_probe.py v4 (fake om in tests/fake_om).
Built-in hyperMILL methods are imitated by functions marked _native that reject an unknown keyword the way pybind11
does (the real mechanism was checked against compiled pybind11 modules: argument lists back, nothing run).
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
RAN = []             # native calls that actually ran
OPENED = []          # paths PofFile was opened on


def check(cond, label):
    print(("ok   " if cond else "FAIL ") + label)
    if not cond:
        fails.append(label)


def native(sig):
    """A fake built-in method: an unknown keyword is rejected before running, listing sig like pybind11."""
    def deco(fn):
        def wrapper(*a, **kw):
            known = set(fn.__code__.co_varnames[1:fn.__code__.co_argcount])
            if set(kw) - known:
                raise TypeError("%s(): incompatible function arguments. The following argument types are supported:\n"
                                "    1. %s\n\nInvoked with: kwargs: %s" % (fn.__name__, sig, kw))
            RAN.append(fn.__name__)
            return fn(*a, **kw)
        wrapper._native = True
        wrapper.__name__ = fn.__name__
        return wrapper
    return deco


class PofFile:
    """Fake om.cam._hmCoreX64.PofFile: opened by file name, checksum of the movements."""
    def __init__(self, *a, **kw):
        if kw:
            raise TypeError("__init__(): incompatible constructor arguments. The following argument types are supported:\n"
                            "    1. om.cam._hmCoreX64.PofFile(fileName: str)\n\nInvoked with: kwargs: %s" % kw)
        RAN.append("PofFile()")
        OPENED.append(a[0])
        with open(a[0], "rb") as f:
            self._sum = sum(f.read()) * 1000003

    @native("(self: om.cam._hmCoreX64.PofFile) -> int")
    def GetMovementsCheckSum(self):
        return self._sum

    @native("(self: om.cam._hmCoreX64.PofFile, fileName: str) -> bool")
    def WriteToFile(self, fileName):
        return True


class PS(enum.Enum):
    UP_TO_DATE = 0
    NEEDS_CALCULATION = 3


class JS(enum.Enum):
    UP_TO_DATE = 1


class SimJob(om.Job):
    def __init__(self, name, n, uuid, pof_ok=True):
        om.Job.__init__(self, name, None, {})
        self.UUID, self.ID, self._n, self._pof = uuid, n, n, pof_ok

    @property
    def Status(self):
        return JS.UP_TO_DATE

    @property
    def POFStatus(self):
        return PS.UP_TO_DATE if self._pof else PS.NEEDS_CALCULATION

    @property
    def PofFileName(self):
        return "Op10_%d.pof" % self._n

    @native("(self: om.cam._hmCoreX64.Job, uuid: str) -> om.cam._hmCoreX64.PofFile")
    def GetPofFile(self, uuid):
        return None

    @native("(self: om.cam._hmCoreX64.Job, params: dict) -> None")
    def SetCfgParameters(self, params):
        return None


class LooseList(om.JobList):
    def __init__(self, name, compounds, loose):
        om.JobList.__init__(self, name, compounds)
        self._loose = loose

    def GetJobs(self):
        return om.JobList.GetJobs(self) + list(self._loose)


SIM = ["{F36764A2-81B9-4B51-AD7F-522E0E1CE34D}", "{BFBAB6AE-0137-454A-A2FE-4D14274F09F7}"]
NOT = ["{11111111-2222-3333-4444-555555555555}"]
LOOSE = ["{AAAAAAAA-BBBB-CCCC-DDDD-EEEEEEEEEEEE}"]

tmp = tempfile.mkdtemp(prefix="rp_")
tempfile.tempdir = tmp
LOGP = os.path.join(tmp, "release_probe_log.txt")
docdir = os.path.join(tmp, "job")
for d in ("VNC", "POF", "NC"):
    os.makedirs(os.path.join(docdir, d))
doc = os.path.join(docdir, "Machining model.hmc")
open(doc, "w").close()
pofdir = os.path.join(docdir, "POF")
for n in (1, 2, 3, 4):
    with open(os.path.join(pofdir, "Op10_%d.pof" % n), "wb") as f:
        f.write(bytes([n]) * 50)
for u in SIM:
    k = u.strip("{}").lower()
    with open(os.path.join(pofdir, k + ".ccrpt"), "wb") as f:
        f.write(b"1234567890123")
    open(os.path.join(pofdir, k + "_@_x_y_t0@z_r90_r90+90.rsf"), "w").close()
with open(os.path.join(pofdir, "99999999-0000-0000-0000-000000000000.ccrpt"), "wb") as f:
    f.write(b"\x00\x01OLDREPORT\x02\x03")
omg = os.path.join(tmp, "VMCenter", "Op10", "Op10.omgcfg")
os.makedirs(os.path.dirname(omg))
with open(omg, "w", encoding="utf-8") as f:
    f.write('<omgcfg>\n  <job uuid="F36764A2-81B9-4B51-AD7F-522E0E1CE34D" pof="Op10_1.pof"/>\n</omgcfg>\n')
with open(os.path.join(docdir, "VNC", "Op10.nclist"), "w", encoding="utf-8") as f:
    f.write('<?xml version="1.0" encoding="utf-8"?>\n<nclist context="ToolpathPreview">\n  <omgcfgs>\n'
            '    <omgcfg file="%s"/>\n  </omgcfgs>\n</nclist>\n' % omg)

cs = [om.CompoundJob("simulated", [SimJob("1: Contour", 1, SIM[0]), SimJob("2: Rough", 2, SIM[1])]),
      om.CompoundJob("not simulated", [SimJob("Chamfer", 3, NOT[0])])]
model = om.Model([LooseList("Op10", cs, [SimJob("9: loose", 4, LOOSE[0], pof_ok=False)])])
om._App.CurrentDocument = om.Document(doc, model)
before = {n: open(os.path.join(pofdir, n), "rb").read() for n in os.listdir(pofdir)}

spec = importlib.util.spec_from_file_location("rp_under_test", SCRIPT)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
real_is_native = m.is_native
m.is_native = lambda raw: getattr(raw, "_native", False) or real_is_native(raw)
gui.BOXES.clear()
om.WRITES.clear()
m.run()
txt = open(LOGP, encoding="utf-8").read()
after = {n: open(os.path.join(pofdir, n), "rb").read() for n in os.listdir(pofdir)}

check("FAILED" not in txt and txt.rstrip().endswith("finished"), "probe ran to the end without an error")
check(set(RAN) <= {"PofFile()", "GetMovementsCheckSum"} and not om.WRITES, "only PofFile and its checksum ran (%s)" % sorted(set(RAN)))
check(before == after, "POF folder unchanged (every file byte for byte)")
check(OPENED and all(not p.startswith(pofdir) for p in OPENED), "PofFile opened only temporary copies, never the job's POF file")
check("init  PofFile(fileName: str)" in txt and "def   GetMovementsCheckSum(self: om.cam._hmCoreX64.PofFile) -> int" in txt,
      "PofFile constructor and checksum arguments listed")
check("def   WriteToFile  (not asked)" in txt, "PofFile write method: not asked")
check("opens a POF file by name: True | GetMovementsCheckSum without arguments: True" in txt, "PofFile usable for a checksum")
check("SimJob.GetPofFile(self: om.cam._hmCoreX64.Job, uuid: str) -> om.cam._hmCoreX64.PofFile" in txt,
      "methods returning a PofFile found across the core classes")
check("SimJob.SetCfgParameters" not in txt.split("=== 2.")[0].split("methods that take or return")[1], "write methods not asked in the class scan")
blocks = txt.split("\n  J ")
sim1 = next(b for b in blocks if b.startswith("'1: Contour'"))
check("in 'simulated'" in sim1 and "UUID={F36764A2-81B9-4B51-AD7F-522E0E1CE34D}" in sim1 and
      "CCRPT f36764a2-81b9-4b51-ad7f-522e0e1ce34d.ccrpt" in sim1 and "text='1234567890123'" in sim1 and
      "31 32 33 34 35 36 37 38 39 30 31 32 33" in sim1, "simulated job: its .ccrpt found by UUID, bytes as text and hex")
check("RSF  f36764a2-81b9-4b51-ad7f-522e0e1ce34d_@_x_y_t0@z_r90_r90+90.rsf" in sim1, "simulated job: .rsf listed")
check("CHECKSUM %d" % (1 * 50 * 1000003) in sim1, "simulated job: checksum of its POF (copy) shown")
chamfer = next(b for b in blocks if b.startswith("'Chamfer'"))
check("CCRPT none (not simulated)" in chamfer, "not simulated job: no .ccrpt")
loose = next(b for b in blocks if b.startswith("'9: loose'"))
check("in '(no compound job)'" in loose and "POFStatus=NEEDS_CALCULATION" in loose, "job outside compound jobs scanned")
check(".ccrpt files no job matches: 1" in txt and "99999999-0000-0000-0000-000000000000.ccrpt" in txt and "OLDREPORT" in txt,
      "unmatched .ccrpt listed with its bytes")
check('<job uuid="F36764A2-81B9-4B51-AD7F-522E0E1CE34D" pof="Op10_1.pof"/>' in txt, "omgcfg text shown")
check("Send the log" in gui.BOXES[-1], "final message asks for the log")

shutil.rmtree(tmp, ignore_errors=True)
print()
print("FAILURES: %d" % len(fails) if fails else "ALL RELEASE PROBE CHECKS PASSED")
sys.exit(1 if fails else 0)
