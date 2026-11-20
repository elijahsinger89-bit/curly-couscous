# job_settings.py - job settings for every operation the part wizards create, per material group and material:
# the CreateJob code (Slr3, Ccp, DdrX5 ...), the job name, the default tool shape and size, and the job's '*KEY' settings
# (stock to leave, stepdown, stepover, clearance, approach ...). Stored in job_settings.json next to this file.
# The part wizards create every toolpath with Joblist.CreateJob and write these settings with SetCfgParameters. No macros.
#
# job_settings.json layout: {material group: {material: {operation: {stepover: settings}}}}
#   material group = the joblist material, e.g. "S - Nickel Based"
#   stepover       = "Percent stepover", "Distance stepover", or "" when the operation has one version
#   settings       = {"code", "jobname", "tool_shape", "tool_dia_in", "params": {"*KEY": "value"}}
# Edit a value in params to change what new toolpaths get.
import os, json

HERE = os.path.dirname(os.path.abspath(__file__))
FILE = os.path.join(HERE, "job_settings.json")

def load(log, path=FILE):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    log("job settings:", path, "|", sum(len(o) for g in data.values() for m in g.values() for o in m.values()), "operation settings")
    return data

def groups(data):
    return sorted(data)

def materials(data, group):
    return sorted(data.get(group, {}))

def find(data, group, material, op, stepover):
    """(label, stepover used, settings) or None. Takes the stepover asked for; an operation with only one version uses that one."""
    ops = data.get(group, {}).get(material, {}).get(op)
    if not ops:
        return None
    for key in (stepover, ""):
        if key in ops:
            return "%s | %s" % (material, op), key, ops[key]
    key = sorted(ops)[0]
    return "%s | %s" % (material, op), key, ops[key]
