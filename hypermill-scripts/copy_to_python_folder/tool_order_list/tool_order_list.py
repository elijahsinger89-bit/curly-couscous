# tool_order_list.py - every tool used in one joblist (operation) of the open document, written to a CSV for ordering.
# Order number = the tool's Ordering code, else the NC tool comment (Common > Comment), else the tool name; Kennametal and GARR
# tools found in the catalog tables also get their EDP number. The NC tool name (M_...) is internal and only listed for reference.
# Columns: manufacturer, order number, designation, description, grade/coating, sizes, inserts, catalog page, NC number and
# the toolpaths that use it. Tools built by the wizards are looked up in the tool_library catalog tables (order number =
# Walter designation, Kennametal and GARR EDP number); any other tool is read from its own hyperMILL tool data.
# Output: <document folder>\<document>_<joblist>_tool_order.csv (else C:\Users\Public\Documents\OPEN MIND\), opened when done.
# Log: C:\Users\Public\Documents\OPEN MIND\tool_order_list_log.txt
import os, csv, re, tempfile, traceback
import xml.etree.ElementTree as ET

PY_DIR   = r"C:\Users\Public\Documents\OPEN MIND\python"
LIB_DIR  = os.path.join(PY_DIR, "tool_library")
OUT_DIR  = r"C:\Users\Public\Documents\OPEN MIND"
OPEN_CSV = True          # open the CSV when done
MM = 25.4

lines = []
def log(*a):
    lines.append(" ".join(str(x) for x in a))

def val(x):
    return x() if callable(x) else x

def _f(x):
    try:
        return float(str(x).replace('"', "").strip())
    except Exception:
        return None

def inch(mm):
    v = _f(mm)
    return "" if v is None or v == 0 else "%.4f" % (v / MM)

# ---------------- catalog tables ----------------
SKIP = ("cutting", "usage", "feed", "map", "vrr", "machines", "inserts")

def catalog():
    """designation -> (row, table file) from every tool table in tool_library."""
    out = {}
    if not os.path.isdir(LIB_DIR):
        log("tool_library not found:", LIB_DIR); return out
    for fn in sorted(os.listdir(LIB_DIR)):
        if not fn.endswith(".csv") or any(s in fn for s in SKIP):
            continue
        try:
            with open(os.path.join(LIB_DIR, fn), encoding="utf-8-sig") as fh:
                for r in csv.DictReader(fh):
                    d = (r.get("designation") or "").strip()
                    if d and d not in out:
                        out[d] = (r, fn)
        except Exception as e:
            log("table not read:", fn, str(e)[:100])
    log("catalog designations:", len(out))
    return out

def kind_of(fn):
    for k, t in (("endmills", "Solid end mill"), ("drills", "Drill"), ("xdrills", "Insert / exchangeable-tip drill"), ("spotdrills", "Spot drill"),
                 ("taps", "Tap"), ("threadmills", "Thread mill"), ("reamers", "Reamer"), ("facemills", "Face mill body"),
                 ("shoulder", "Shoulder mill body"), ("hfcopy", "High-feed / copy mill body"), ("profile", "Inserted ball nose body"),
                 ("chamfer_ins", "Inserted chamfer mill body"), ("boring", "Boring head"), ("slot", "Slot / disc cutter body")):
        if k in fn:
            return t
    return ""

# ---------------- hyperMILL tool data ----------------
def tool_xml(tool):
    """Parameters of the tool element in the tool's own export (manufacturer, comment, sizes), holder and NC tool name."""
    p = os.path.join(tempfile.gettempdir(), "tool_order_list_%s.omtdx" % re.sub(r"[^A-Za-z0-9_.-]", "_", str(tool.Name))[:60])
    out = {}
    try:
        if not tool.Export(p):
            return out
        root = ET.parse(p).getroot()
        t = root.find(".//tools/tool")
        if t is not None:
            out["_type"] = t.get("type", "")
            out["_toolname"] = t.get("name", "")
            for prm in t.findall("param"):
                out[prm.get("name")] = prm.get("value")
                if "order" in str(prm.get("name")).lower() and (prm.get("value") or "").strip():
                    out["_ordering"] = prm.get("value").strip()          # Ordering code field of the tool
        h = root.find(".//holders/holder")
        if h is not None:
            out["_holder"] = h.get("name", "")
        n = root.find(".//ncTools/ncTool")
        if n is not None:
            out["_ncname"] = n.get("name", "")
            c = n.find("param[@name='comment']")
            if c is not None:
                out["_nccomment"] = (c.get("value") or "").strip()      # Common > Comment: the order number
    except Exception as e:
        log("export not read:", tool.Name, str(e)[:100])
    finally:
        try:
            os.remove(p)
        except Exception:
            pass
    return out

def tool_row(tool, jobs, cat):
    internal = str(val(tool.Name))
    x = tool_xml(tool)
    # order number: Ordering code, else the NC tool comment (Common > Comment), else the tool name; the NC tool name is internal
    cands = [v for v in (x.get("_ordering"), x.get("_nccomment"), x.get("_toolname"), internal) if v]
    name = next((v for v in cands if v in cat), cands[0] if cands else internal)
    hit = cat.get(name)
    r, fn = hit if hit else ({}, "")
    mf = r.get("manufacturer") or x.get("manufacturer") or ""
    edp = (r.get("edp") or "").strip()
    order = edp or name
    dia = r.get("dia_in") or (inch(r.get("dia_mm")) if r.get("dia_mm") else "") or ("%.4f" % _f(x["toolDiameter"]) if _f(x.get("toolDiameter")) else "")
    desc = r.get("title") or r.get("description") or r.get("series") or kind_of(fn) or x.get("_type", "")
    if r.get("shape") and r.get("shape") not in desc:
        desc = (desc + " " + r["shape"]).strip()
    inserts = r.get("insert_type") or ""
    if r.get("insert_grades"):
        inserts = (inserts + " | grades " + r["insert_grades"]).strip(" |")
    return {
        "Manufacturer": mf,
        "Order number (EDP / order code)": order,
        "Designation": name,
        "Family": r.get("family", ""),
        "Tool type": kind_of(fn) or x.get("_type", ""),
        "Description": desc,
        "Grade / coating": " / ".join(v for v in (r.get("grade", ""), r.get("coating", "")) if v),
        "Performance level": r.get("tier", ""),
        "Diameter (in)": dia,
        "Diameter (mm)": r.get("dia_mm", ""),
        "Corner radius (in)": inch(r.get("corner_r_mm")) or ("%.4f" % _f(x["cornerRadius"]) if _f(x.get("cornerRadius")) else ""),
        "Flutes": r.get("flutes") or r.get("z") or x.get("cuttingEdges", ""),
        "Cutting / thread length (in)": inch(r.get("flute_len_mm") or r.get("thread_len_mm") or r.get("depth_max_mm") or r.get("lc_mm")) or (x.get("cuttingLength") or ""),
        "Reach (in)": inch(r.get("reach_mm")),
        "Overall length (in)": inch(r.get("oal_mm") or r.get("l1_mm")) or (x.get("toolTotalLength") or ""),
        "Shank (in)": inch(r.get("shank_dia_mm")) or (x.get("toolShaftDiameter") or ""),
        "Interface": r.get("interface", ""),
        "Thread": r.get("thread") or r.get("thread_range", ""),
        "Tolerance": r.get("tolerance", ""),
        "Coolant": r.get("coolant", ""),
        "Inserts (order separately)": inserts,
        "Catalog": " ".join(v for v in (r.get("source", ""), ("p" + r["page"]) if r.get("page") else "") if v),
        "Holder in hyperMILL": x.get("_holder", ""),
        "NC tool (internal)": x.get("_ncname") or internal,
        "Toolpaths using it": len(jobs),
        "Toolpath names": " ; ".join(jobs),
        "Tool comment": x.get("comment", ""),
        "In tool_library": "yes" if hit else "no - check the manufacturer data",
    }

# ---------------- dialogs ----------------
def _gui():
    import om.cad.gui as g
    return g

def choose(title, label, options):
    g = _gui()
    dlg = g.InputDialog(title)
    dlg.AddDropDown(label, list(options), defaultIndex=0)
    ok, vals = dlg.Show()
    if not ok:
        return None
    v = vals.get(label)
    if isinstance(v, int) and not isinstance(v, bool):
        return v if 0 <= v < len(options) else 0
    return list(options).index(v) if v in options else 0

def info(title, text):
    g = _gui()
    g.ShowMessageBox(g.MessageBoxType.INFORMATION, title, text)

# ---------------- main ----------------
def run():
    path = ""
    try:
        import om
        doc = om.Application().CurrentDocument
        if doc is None:
            info("Tool order list", "No document open."); return
        model = doc.CamModel
        lists = list(model.JobListSet.GetJobLists())
        if not lists:
            info("Tool order list", "No joblists in this document."); return
        names = [str(jl.Name) for jl in lists]
        k = choose("Tool order list", "Operation (joblist)", names + ["All joblists"])
        if k is None:
            log("cancelled"); return
        picked = lists if k == len(names) else [lists[k]]
        label = "all" if k == len(names) else names[k]
        log("joblists:", ", ".join(str(jl.Name) for jl in picked))
        used, order = {}, []
        for jl in picked:
            for j in jl.GetJobs():
                try:
                    t = j.GetTool()
                except Exception:
                    t = None
                if t is None:
                    log("no tool:", jl.Name, "|", j.Name); continue
                u = str(t.UUID).strip("{}").upper()
                if u not in used:
                    used[u] = (t, []); order.append(u)
                used[u][1].append("%s: %s" % (jl.Name, j.Name))
        if not order:
            info("Tool order list", "No toolpath in %s has a tool." % label); return
        cat = catalog()
        rows = []
        for u in order:
            t, jobs = used[u]
            try:
                rows.append(tool_row(t, jobs, cat))
            except Exception:
                log("tool row FAILED:", getattr(t, "Name", "?"), traceback.format_exc()[-300:])
        rows.sort(key=lambda r: (r["Manufacturer"], r["Tool type"], _f(r["Diameter (in)"]) or 0, r["Designation"]))
        folder, base = OUT_DIR, "document"
        try:
            fp = str(val(doc.FullPath) or "")
            if fp:
                folder = os.path.dirname(fp) or OUT_DIR
                base = os.path.splitext(os.path.basename(fp))[0]
        except Exception:
            pass
        fname = "%s_%s_tool_order.csv" % (base, re.sub(r"[^A-Za-z0-9_-]", "_", label))
        path = os.path.join(folder, fname)
        try:
            f = open(path, "w", newline="", encoding="utf-8-sig")
        except Exception:
            path = os.path.join(OUT_DIR, fname); f = open(path, "w", newline="", encoding="utf-8-sig")
        with f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader(); w.writerows(rows)
        missing = [r["Designation"] for r in rows if r["In tool_library"] != "yes"]
        log("written:", path, "|", len(rows), "tools |", len(missing), "not in tool_library:", missing)
        msg = "%d tool(s) from %s written to:\n%s" % (len(rows), label, path)
        if missing:
            msg += "\n\nNot in the tool library (manufacturer and order number from the hyperMILL tool data only):\n" + "\n".join(missing[:15])
        info("Tool order list", msg)
        if OPEN_CSV:
            try:
                os.startfile(path)
            except Exception:
                pass
    except Exception:
        log("FAILED:", traceback.format_exc())
        try:
            info("Tool order list", "Failed. See tool_order_list_log.txt.")
        except Exception:
            pass
    finally:
        try:
            with open(os.path.join(OUT_DIR, "tool_order_list_log.txt"), "w", encoding="utf-8") as fh:
                fh.write("\n".join(lines))
        except Exception:
            pass

if __name__ == "__main__":
    run()
