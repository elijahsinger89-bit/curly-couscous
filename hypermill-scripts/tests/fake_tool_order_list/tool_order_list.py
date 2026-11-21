# Stand-in for the installed tool_order_list.py (hyperMILL_automation package): the functions go_to_machine uses -
# catalog(), tool_row(tool, jobs, cat), _f(), lines - with the same row keys the real script writes.
lines = []


def log(*a):
    lines.append(" ".join(str(x) for x in a))


def _f(x):
    try:
        return float(str(x).replace('"', "").strip())
    except Exception:
        return None


def catalog():
    log("catalog designations:", 1)
    return {"End mill": ({"manufacturer": "Walter"}, "walter_endmills.csv")}


def tool_row(tool, jobs, cat):
    name = str(tool.Name)
    hit = name in cat
    return {
        "Manufacturer": cat[name][0]["manufacturer"] if hit else "",
        "Order number (EDP / order code)": name,
        "Designation": name,
        "Tool type": "",
        "Diameter (in)": "",
        "NC tool (internal)": str(tool.ID),
        "Toolpaths using it": len(jobs),
        "Toolpath names": " ; ".join(jobs),
        "In tool_library": "yes" if hit else "no - check the manufacturer data",
    }
