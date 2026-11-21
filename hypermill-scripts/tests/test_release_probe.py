#!/usr/bin/env python3
"""Headless test of release_probe.py v5 (fake om in tests/fake_om): finds which .ccrpt ucid belongs to which job, in the
POF bytes (ASCII and UTF-16), in PofFile settings (read from a copy) and in job settings; CRC32 against the omgcfg.
Run: python3 tests/test_release_probe.py"""
import os
import sys
import zlib
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
RAN = []
OPENED = []


def check(cond, label):
    print(("ok   " if cond else "FAIL ") + label)
    if not cond:
        fails.append(label)


def native(sig):
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


U_ASCII = "f36764a2-81b9-4b51-ad7f-522e0e1ce34d"      # stored as text in job 1's POF
U_UTF16 = "bfbab6ae-0137-454a-a2fe-4d14274f09f7"      # stored as UTF-16 in job 2's POF
U_CFG = "ba0ff6bd-42b7-430d-bda4-1e4f0aab9059"        # only in job 3's PofFile settings
U_JOB = "010cbcb0-e345-4f88-b7ff-2aa5765902c7"        # only in job 4's own settings
U_LOST = "599d8def-e111-4693-b209-9adc8136718e"       # in no job


class PofFile:
    def __init__(self, *a, **kw):
        if kw:
            raise TypeError("__init__(): incompatible constructor arguments. The following argument types are supported:\n"
                            "    1. om.cam._hmCoreX64.PofFile(arg0: str)\n\nInvoked with: kwargs: %s" % kw)
        RAN.append("PofFile()")
        OPENED.append(a[0])
        self._name = os.path.basename(a[0])

    @native("(self: om.cam._hmCoreX64.PofFile) -> Dict[str, str]")
    def GetCfgParameters(self):
        d = {"*POF_VERSION": "35", "*JOB_NAME": self._name}
        if self._name == "Op10_3.pof":
            d["*UCID"] = "{%s}" % U_CFG.upper()
        return d


class PS(enum.Enum):
    UP_TO_DATE = 0


class JS(enum.Enum):
    UP_TO_DATE = 1


class SimJob(om.Job):
    def __init__(self, name, n, uuid, cfg=None):
        om.Job.__init__(self, name, None, cfg or {})
        self.UUID, self.ID, self._n = uuid, n, n
        self.Status, self.POFStatus = JS.UP_TO_DATE, PS.UP_TO_DATE

    @property
    def PofFileName(self):
        return "Op10_%d.pof" % self._n


tmp = tempfile.mkdtemp(prefix="rp_")
tempfile.tempdir = tmp
LOGP = os.path.join(tmp, "release_probe_log.txt")
docdir = os.path.join(tmp, "job")
for d in ("VNC", "POF"):
    os.makedirs(os.path.join(docdir, d))
doc = os.path.join(docdir, "Machining model.hmc")
open(doc, "w").close()
pofdir = os.path.join(docdir, "POF")
pofs = {1: b"POF35\x00HDR ucid=" + U_ASCII.upper().encode() + b"\x00 moves...",
        2: b"POF35\x00" + ("UCID " + U_UTF16).encode("utf-16-le") + b"\x00 moves...",
        3: b"POF35\x00 no id here, other guid 12345678-aaaa-bbbb-cccc-1234567890ab",
        4: b"POF35\x00 plain"}
for n, b in pofs.items():
    with open(os.path.join(pofdir, "Op10_%d.pof" % n), "wb") as f:
        f.write(b)
for u in (U_ASCII, U_UTF16, U_CFG, U_JOB, U_LOST):
    with open(os.path.join(pofdir, u + ".ccrpt"), "wb") as f:
        f.write(b"CC_RESULT 1\r\n")
omg = os.path.join(tmp, "VMCenter", "Op10", "Op10.omgcfg")
os.makedirs(os.path.dirname(omg))
crc1 = zlib.crc32(pofs[1]) & 0xFFFFFFFF
with open(omg, "w", encoding="utf-8") as f:
    f.write('<?xml version="1.0"?>\n<omgview>\n'
            '  <pof file="C:/x/POF/Op10_12.pof" ucid="%s" crc="%d"/>\n'
            '  <pof file="C:/x/POF/Op10_15.pof" ucid="%s" crc="99"/>\n'
            '  <pof file="C:/x/POF/Op10_9.pof" ucid="deadbeef-0000-0000-0000-000000000000" crc="98"/>\n'
            '</omgview>\n' % (U_ASCII, crc1, U_UTF16))
with open(os.path.join(docdir, "VNC", "Op10.nclist"), "w", encoding="utf-8") as f:
    f.write('<nclist>\n  <omgcfgs>\n    <omgcfg file="%s"/>\n  </omgcfgs>\n</nclist>\n' % omg)

cs = [om.CompoundJob("simulated", [SimJob("1: Contour", 1, "{8BB95839-1487-4A7A-B409-185B80531841}"),
                                   SimJob("2: Rough", 2, "{801E7A55-4AED-4E7C-AA30-7975E962D08B}"),
                                   SimJob("3: Pocket", 3, "{48388DD2-E2A6-42CC-BB79-F4ACDF6D5AB9}"),
                                   SimJob("4: Drill", 4, "{EDD50599-D3AA-42AF-85B8-B1A9CDA1E6AD}",
                                          {"*SIM_REF": U_JOB, "*FRAME_UUID": "{11111111-2222-3333-4444-555555555555}"})]),
      om.CompoundJob("not calculated", [SimJob("9: Contour", 9, "{71FDBDA0-581D-458F-8670-C3C39A07EF0F}")])]
om._App.CurrentDocument = om.Document(doc, om.Model([om.JobList("Op10", cs)]))
before = {n: open(os.path.join(pofdir, n), "rb").read() for n in os.listdir(pofdir)}

spec = importlib.util.spec_from_file_location("rp_under_test", SCRIPT)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
real_is_native = m.is_native
m.is_native = lambda raw: getattr(raw, "_native", False) or real_is_native(raw)
gui.BOXES.clear()
m.run()
txt = open(LOGP, encoding="utf-8").read()
after = {n: open(os.path.join(pofdir, n), "rb").read() for n in os.listdir(pofdir)}
summary = txt.split("=== 3. SUMMARY")[1]

check("FAILED" not in txt and txt.rstrip().endswith("finished"), "probe ran to the end without an error")
check(set(RAN) <= {"PofFile()", "GetCfgParameters"} and not om.WRITES, "only PofFile and its settings read (%s)" % sorted(set(RAN)))
check(before == after, "POF folder unchanged")
check(OPENED and all(not p.startswith(pofdir) for p in OPENED), "PofFile opened only temporary copies")
check("PofFile: rp_under_test" not in txt and "opens by name: True  GetCfgParameters without arguments: True" in txt,
      "PofFile usable: opens by name, settings without arguments")
check("%s.ccrpt" % U_LOST in txt and "'CC_RESULT 1'" in txt, ".ccrpt files listed with their text")
check("omgcfg  Op10_12.pof  ucid %s  crc %d  .ccrpt exists" % (U_ASCII, crc1) in txt and
      "ucid deadbeef-0000-0000-0000-000000000000  crc 98  no .ccrpt" in txt, "omgcfg entries listed with .ccrpt or not")
check("crc32=%d  = omgcfg crc of Op10_12.pof ucid %s" % (crc1, U_ASCII) in txt, "POF CRC32 matched to the omgcfg crc")
check("UCID %s in the POF file (ascii" % U_ASCII in txt, "ucid found as text in the POF (case-insensitive)")
check("UCID %s in the POF file (utf16" % U_UTF16 in txt, "ucid found as UTF-16 in the POF")
check("12345678-aaaa-bbbb-cccc-1234567890ab@" in txt, "other GUIDs in the POF file listed")
check("*POF_VERSION = '35'" in txt and txt.count("PofFile.GetCfgParameters: 2 keys") == 2 and "PofFile settings with a GUID value: *UCID" in txt,
      "PofFile settings: in full for the first 2 jobs, GUID values for the rest")
check("job settings with a GUID value: *FRAME_UUID={11111111-2222-3333-4444-555555555555}, *SIM_REF=%s" % U_JOB in txt,
      "job settings with GUID values listed")
check("%s  'CC_RESULT 1'  ->  1: Contour (POF file ascii)" % U_ASCII in summary, "summary: ucid -> job 1 via POF text")
check("%s  'CC_RESULT 1'  ->  2: Rough (POF file utf16)" % U_UTF16 in summary, "summary: ucid -> job 2 via POF UTF-16")
check("%s  'CC_RESULT 1'  ->  3: Pocket (PofFile setting *UCID)" % U_CFG in summary, "summary: ucid -> job 3 via PofFile setting")
check("%s  'CC_RESULT 1'  ->  4: Drill (job setting *SIM_REF)" % U_JOB in summary, "summary: ucid -> job 4 via job setting")
check("%s  'CC_RESULT 1'  ->  NOT FOUND in any job" % U_LOST in summary, "summary: ucid in no job")
check("Op10_9.pof  (file not found)" in txt, "job without a POF file: noted")
check("Send the log" in gui.BOXES[-1], "final message asks for the log")

shutil.rmtree(tmp, ignore_errors=True)
print()
print("FAILURES: %d" % len(fails) if fails else "ALL RELEASE PROBE CHECKS PASSED")
sys.exit(1 if fails else 0)
