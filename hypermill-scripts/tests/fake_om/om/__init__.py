# Fake hyperMILL 35 'om' module for headless tests. Shapes follow compound_probe v2 (real document, 12 Nov 2026).
WRITES = []


class Tool:
    def __init__(self, tid, name=None, ttype="endMill", dia=0.5, unit="inch"):
        self.ID = tid
        self.Number = int(tid) if tid.isdigit() else 0
        self.Name = name or tid
        self.UUID = "{T-%s}" % tid
        self._type, self._dia, self._unit = ttype, dia, unit

    def Export(self, path):
        with open(path, "w", encoding="utf-8") as f:
            f.write('<root><tools><tool type="%s"><param name="lengthOfUnit" value="%s"/>'
                    '<param name="toolDiameter" value="%s"/></tool></tools>'
                    '<ncTools><ncTool id="%s" name="%s"/></ncTools></root>' % (self._type, self._unit, self._dia, self.ID, self.Name))
        return True


class Job:
    def __init__(self, name, tool, cfg=None):
        self.Name = name
        self._tool = tool
        self._cfg = dict(cfg or {})

    def GetTool(self):
        return self._tool

    def GetCfgParameters(self):
        return dict(self._cfg)


class CompoundJob:
    """mode: 'name' (Name settable), 'cfg' (Name read-only, follows *CPJOBNAME), 'stuck' (nothing changes)."""
    _n = 0

    def __init__(self, name, jobs=(), mode="name"):
        CompoundJob._n += 1
        self.UUID = "{C-%04d}" % CompoundJob._n
        self._name = name
        self._jobs = list(jobs)
        self._mode = mode

    @property
    def Name(self):
        return self._name

    @Name.setter
    def Name(self, v):
        WRITES.append(("Name", self.UUID, v))
        if self._mode == "name":
            self._name = v
        elif self._mode == "stuck":
            raise RuntimeError("read-only")

    def GetJobs(self):
        return list(self._jobs)

    def GetCfgParameters(self):
        return {"*CPJOBNAME": self._name, "*AUFMASS": "0.025"}

    def SetCfgParameters(self, d):
        WRITES.append(("cfg", self.UUID, dict(d)))
        if self._mode == "cfg" and "*CPJOBNAME" in d:
            self._name = d["*CPJOBNAME"]


class JobList:
    def __init__(self, name, compounds):
        self.Name = name
        self._c = compounds

    def GetCompoundJobs(self):
        return list(self._c)

    def GetJobs(self):
        return [j for c in self._c for j in c.GetJobs()]


class JobListSet:
    def __init__(self, lists):
        self._l = lists

    def GetJobLists(self):
        return list(self._l)


class Model:
    def __init__(self, lists, inch=True):
        self.JobListSet = JobListSet(lists)
        self._inch = inch

    def IsInchMode(self):
        return self._inch


class Document:
    def __init__(self, path, model):
        self.FullPath = path
        self.CamModel = model


class _App:
    CurrentDocument = None


def Application():
    return _App
