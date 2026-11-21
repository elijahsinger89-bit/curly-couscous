# tool_info.py - one reader for a document tool: everything the job-end documents need, from the tool object and its own
# export (Tool.Export). Used by job_docs (setup sheet, order sheet, sister sheet) and go_to_machine.
# Field rule (docs/hyperMILL_design_notes.md section 2, plan 21 Nov; holder / extension part ASSUMED until the holder attacher):
#   Common: NC-Number = ID = the tool number; Name = short description; Comment = holder / extension text
#   Tool:   Name = manufacturer long name; Comment = catalog no. | grade | cutting-data source; Ordering code = EDP
#   Holder: name = holder EDP; Extension (collet, extension): name = its EDP
# Order code of the cutter: the Ordering code field, else "EDP <x>" in the Tool comment, else the Tool comment of a tool
# built before (Kennametal templates keep the EDP there), else the Tool name. Every fallback is noted in "notes".
# Lengths come back in inch (exports in mm are converted).
import os, re, tempfile
import xml.etree.ElementTree as ET

MM = 25.4
TURN_TYPES = ("insertttool", "groovettool", "threadttool", "turningtool")
ORDER_RE = re.compile(r"order", re.I)
EDP_RE = re.compile(r"\bEDP\s*[:#]?\s*([A-Za-z0-9.\-/]+)", re.I)


def val(x):
    return x() if callable(x) else x


def text(x):
    try:
        return str(val(x) or "").strip()
    except Exception:
        return ""


def _f(x):
    try:
        return float(x)
    except Exception:
        return None


def params(el):
    return {p.get("name"): p.get("value") for p in el.findall("param")} if el is not None else {}


def export_root(tool, folder=None):
    """The tool's own export, parsed, or None."""
    folder = folder or tempfile.gettempdir()
    p = os.path.join(folder, "tool_info_%s.omtdx" % re.sub(r"[^A-Za-z0-9_.-]", "_", text(getattr(tool, "UUID", "")) or text(tool.Name))[:60])
    try:
        if not tool.Export(p):
            return None
        return ET.parse(p).getroot()
    except Exception:
        return None


def read(tool, folder=None):
    """dict with: id, number, nc_name, nc_comment, type, tool_name, tool_comment, manufacturer, order_code, order_from,
    dia, corner_r, angle, angle_kind, flute_len, reach, gage, oal, pitch, turning, insert, holders, extensions, components,
    notes, missing. Lengths in inch."""
    i = {"id": text(getattr(tool, "ID", "")), "number": text(getattr(tool, "Number", "")), "nc_name": "", "nc_comment": "",
         "type": "", "tool_name": text(getattr(tool, "Name", "")), "tool_comment": "", "manufacturer": "", "order_code": "",
         "order_from": "", "dia": None, "corner_r": None, "angle": None, "angle_kind": "", "flute_len": None, "reach": None,
         "gage": None, "oal": None, "pitch": None, "turning": False, "insert": "", "holders": [], "extensions": [],
         "components": [], "notes": [], "missing": []}
    root = export_root(tool, folder)
    if root is None:
        i["notes"].append("tool export not read")
        i["missing"].append("export")
        return i
    t = root.find(".//tools/tool")
    tp = params(t)
    unit = (tp.get("lengthOfUnit") or "inch").lower()
    k = MM if unit.startswith("mm") or unit.startswith("milli") else 1.0
    L = lambda v: (_f(v) / k) if _f(v) is not None else None
    if t is not None:
        i["type"] = t.get("type", "")
        i["tool_name"] = t.get("name", "") or i["tool_name"]
        i["tool_comment"] = (tp.get("comment") or "").strip()
        i["manufacturer"] = (tp.get("manufacturer") or "").strip()
        i["dia"] = L(tp.get("toolDiameter") or tp.get("nominalDiameter"))
        i["corner_r"] = L(tp.get("cornerRadius"))
        i["flute_len"] = L(tp.get("cuttingLength"))
        i["oal"] = L(tp.get("toolTotalLength"))
        i["pitch"] = L(tp.get("pitch"))
        if tp.get("coneAngle"):
            i["angle"], i["angle_kind"] = _f(tp.get("coneAngle")), "point"
        elif tp.get("chamferAngle"):
            i["angle"], i["angle_kind"] = _f(tp.get("chamferAngle")), "chamfer"
        for name, v in tp.items():
            if name and ORDER_RE.search(name) and (v or "").strip():
                i["order_code"], i["order_from"] = v.strip(), "Ordering code"
                break
    n = root.find(".//ncTools/ncTool")
    np_ = params(n)
    if n is not None:
        i["id"] = n.get("id") or i["id"]
        i["number"] = n.get("ncNumber") or i["number"]
        i["nc_name"] = n.get("name", "")
        i["nc_comment"] = (np_.get("comment") or "").strip()
        nk = MM if (np_.get("lengthOfUnit") or unit).lower().startswith("m") else 1.0
        i["gage"] = (_f(np_.get("gageLength")) / nk) if _f(np_.get("gageLength")) is not None else None
        for c in n.findall("components/component"):
            i["components"].append({"type": c.get("type", ""), "name": c.get("name", "")})
            if c.get("type") == "tool" and c.get("reach"):
                i["reach"] = _f(c.get("reach")) / nk
    for h in root.findall(".//holders/holder") + root.findall(".//toolHolders/toolHolder"):
        i["holders"].append({"name": h.get("name", ""), "comment": (params(h).get("comment") or "").strip()})
    for e in root.findall(".//extensions/extension"):
        i["extensions"].append({"name": e.get("name", ""), "comment": (params(e).get("comment") or "").strip()})
    ins = root.find(".//inserts/insert")
    if ins is not None or i["type"].lower() in TURN_TYPES:
        i["turning"] = True
        ip = params(ins)
        i["insert"] = ins.get("type", "") if ins is not None else ""
        if ip.get("cornerRadius"):
            i["corner_r"] = L(ip.get("cornerRadius"))
        if ip.get("insertAngle"):
            i["angle"], i["angle_kind"] = _f(ip.get("insertAngle")), "insert"
    if not i["order_code"]:
        m = EDP_RE.search(i["tool_comment"])
        if m:
            i["order_code"], i["order_from"] = m.group(1), "Tool comment (EDP)"
        elif re.match(r"^[A-Za-z0-9.\-/]{5,}$", i["tool_comment"]):
            i["order_code"], i["order_from"] = i["tool_comment"], "Tool comment"
        elif i["tool_name"]:
            i["order_code"], i["order_from"] = i["tool_name"], "Tool name"
        if i["order_code"]:
            i["notes"].append("order no. from the %s (no Ordering code)" % i["order_from"])
    if not i["order_code"]:
        i["missing"].append("order no.")
    if not i["nc_name"] or i["nc_name"] == i["id"] or re.match(r"^[MT]_\w+$", i["nc_name"]):
        i["missing"].append("description (Common > Name)")
    if i["dia"] is None:
        i["missing"].append("diameter")
    if not i["holders"] and not i["turning"]:
        i["missing"].append("holder")
    if i["holders"] and i["reach"] is None:
        i["missing"].append("reach (stick-out)")
    return i


def description(i):
    """What the setup sheet shows as the tool: Common Name when it is a description, else the Tool name."""
    nm = i.get("nc_name") or ""
    return nm if nm and nm != i.get("id") and not re.match(r"^[MT]_\w+$", nm) else (i.get("tool_name") or nm)


def assembly(i):
    """Holder, collet / extension names for the TOOL / COLLET / HOLDER / EXTENSION column."""
    parts = [h["name"] + (" (%s)" % h["comment"] if h.get("comment") else "") for h in i.get("holders", []) if h.get("name")]
    parts += [e["name"] + (" (%s)" % e["comment"] if e.get("comment") else "") for e in i.get("extensions", []) if e.get("name")]
    return " | ".join(parts) or (i.get("nc_comment") or "")
