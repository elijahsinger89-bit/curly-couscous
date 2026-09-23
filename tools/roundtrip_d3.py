#!/usr/bin/env python3
"""
THE ROUND-TRIP PROOF. D-236.

model/main-panel.json is a HAND TRANSCRIPTION of D3's geometry, and a hand
transcription is the hand-that-types failure F-119 and G-55 already caught in
this build. This proves the copy.

It reads enclosure-layout.md INDEPENDENTLY - it does not import the model's
own printer - pulls every figure out of D3's tables, and compares field by
field against the model.

MATCH means the transcription is proved and a drawing may be generated from
the model. A DIFF NAMES THE ROW and nothing is drawn until it is resolved.

What it proves: THE FIGURES. Not D3's prose, not its reasons, not its
blockers' wording. A drawing consumes figures, so figures are what the proof
has to cover, and claiming more than that would be the thing this build
spends its time removing.

Exit 0 on a clean round trip, 1 on any mismatch.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL = json.load(open(os.path.join(ROOT, "model", "main-panel.json")))
DOC = open(os.path.join(ROOT, "enclosure-layout.md"), encoding="utf-8").read()

fails, checks = [], 0

def num(t):
    """The cell's figure. Bold and units stripped.

    A cell may hold an EXPRESSION rather than a figure - B1 position 1 reads
    '63 mm + 5 mm each side = 73'. The figure is what follows the '=', never
    the first number, and taking the first number there gets 63 where the
    occupancy is 73. F-127."""
    if t is None: return None
    t = t.replace('**', '').replace(',', '')
    if '=' in t: t = t.split('=')[-1]
    m = re.search(r'(\d+(?:\.\d+)?)', t)
    return float(m.group(1)) if m else None

def section(head, nxt):
    i = DOC.find(head)
    if i < 0: return ""
    j = DOC.find(nxt, i + len(head))
    return DOC[i:j if j > 0 else len(DOC)]

def rows(block):
    out = []
    for ln in block.split("\n"):
        if not ln.strip().startswith("|"): continue
        if re.match(r'^\|[\s:\-|]+\|?\s*$', ln): continue
        out.append([c.strip() for c in ln.strip().strip("|").split("|")])
    return out

def check(label, doc_val, model_val):
    global checks
    checks += 1
    a = float(doc_val) if doc_val is not None else None
    b = float(model_val) if model_val is not None else None
    if a is None and b is None: return
    if a is None or b is None or abs(a - b) > 1e-6:
        fails.append(f"{label}: D3 says {doc_val!r}, model says {model_val!r}")

# ---- 3.1 the enclosure -----------------------------------------------------
s31 = section("## SHEET 3.1.", "## SHEET 3.2.")
d31 = {}
for r in rows(s31):
    if len(r) >= 2:
        k = r[0].replace('**', '').strip().lower()
        if k: d31[k] = num(r[1])
e = MODEL["enclosure"]
check("3.1 box width",    d31.get("box width"),    e["box"]["width"])
check("3.1 box height",   d31.get("box height"),   e["box"]["height"])
check("3.1 box depth",    d31.get("box depth"),    e["box"]["depth"])
check("3.1 plate width",  d31.get("plate width"),  e["plate"]["width"])
check("3.1 plate height", d31.get("plate height"), e["plate"]["height"])

# ---- 3.2 bands, rail totals, demand ----------------------------------------
s32 = section("## SHEET 3.2.", "## SHEET 3.3.")
band_h, totals, rail_tot, demand = {}, {}, {}, {}
for r in rows(s32):
    c0 = r[0].replace('**', '').strip()
    if re.match(r'^B[1-4]\b', c0) and len(r) >= 3:
        band_h[c0.split(',')[0].strip()] = num(r[-1])
    if c0 == "" and len(r) >= 3:
        totals[r[1].replace('**', '').split(',')[0].strip().lower()] = num(r[2])
    m = re.match(r'^2 x (\d+) mm$', c0)
    if m and len(r) >= 4:
        rail_tot["d" + m.group(1)] = num(r[3])
    if len(r) == 4 and c0 and not c0.startswith("Duct") and not c0.startswith("Item") \
       and "TOTAL" not in r[2] and not re.match(r'^2 x \d+ mm$', c0):
        demand[c0] = (num(r[1]), num(r[2]), num(r[3]))
for b in MODEL["bands"]:
    check(f"3.2 band {b['id']} height", band_h.get(b["id"]), b["height"])
check("3.2 used",         totals.get("used"),         MODEL["band_totals"]["used"])
check("3.2 plate height", totals.get("plate height"), MODEL["band_totals"]["plate_height"])
check("3.2 slack",        totals.get("slack"),        MODEL["band_totals"]["slack"])
for k, v in MODEL["rail_total"].items():
    check(f"3.2 total rail {k}", rail_tot.get(k), v)
for d in MODEL["demand"]:
    got = demand.get(d["item"])
    if got is None:
        fails.append(f"3.2 demand row missing from D3: {d['item']!r}")
        checks += 1
        continue
    check(f"3.2 demand {d['item']} each",  got[0], d["each"])
    check(f"3.2 demand {d['item']} count", got[1], d["count"] or None)
    check(f"3.2 demand {d['item']} total", got[2], d["total"])
tot = [r for r in rows(s32) if len(r) == 4 and "TOTAL" in r[2]]
check("3.2 demand TOTAL", num(tot[0][3]) if tot else None, MODEL["demand_total"])

# ---- 3.3 rail positions ----------------------------------------------------
# B1 and B2 are  Position | Device | Rail | Note
# B3 and B4 are  Group | Ways | Rail | (Runs)      - NO position column.
s33 = section("## SHEET 3.3.", "## SHEET 3.4.")
BOUNDS = {"B1_items": ("### B1.", "### B2."), "B2_items": ("### B2.", "### B3."),
          "B3_items": ("### B3.", "### B4."), "B4_items": ("### B4.", None)}
for key, (a, b) in BOUNDS.items():
    i = s33.find(a)
    j = s33.find(b) if b else len(s33)
    blk = s33[i:j]
    has_pos = key in ("B1_items", "B2_items")
    doc = []
    for r in rows(blk):
        c0 = r[0].replace('**', '').strip()
        if c0.lower() in ("position", "group", "") or c0.lower().startswith("used"):
            continue
        if has_pos:
            doc.append((r[1].replace('**', '').strip(), num(r[2]), None))
        else:
            doc.append((c0, num(r[1]) if len(r) > 1 else None, num(r[2]) if len(r) > 2 else None))
    mod = MODEL[key]
    checks += 1
    if len(doc) != len(mod):
        fails.append(f"3.3 {key}: D3 has {len(doc)} item rows, model has {len(mod)}")
    for i2, m in enumerate(mod):
        if i2 >= len(doc): break
        name = m.get("device") or m.get("group")
        dname, v1, v2 = doc[i2]
        checks += 1
        if dname != name:
            fails.append(f"3.3 {key} pos {m['pos']}: D3 names {dname!r}, model names {name!r}")
        if has_pos:
            check(f"3.3 {key} {name} rail", v1, m["rail"])
        else:
            want = m.get("ways") if m.get("ways") else m.get("carriers")
            check(f"3.3 {key} {name} ways", v1 if v1 else None, want if want else None)
            check(f"3.3 {key} {name} rail", v2, m["rail"])

# ---- the terminal envelope, stated in 3.2.2 rather than in a rail table ------
te = MODEL["terminal_envelope"]
for label, v in (("height above rail", te["height_above_rail"]),
                 ("depth off the rail face", te["depth_off_rail"]),
                 ("overall including the DIN clip", te["overall_height_with_din_clip"])):
    checks += 1
    if not re.search(rf'{int(v)}\s*mm', s32):
        fails.append(f"3.2.2 terminal {label}: {v} mm not found in D3 sheet 3.2")

# ---- 3.5 the bottom face ---------------------------------------------------
s35 = section("## SHEET 3.5.", "## SHEET 3.6.")
bf = MODEL["bottom_face"]
for row_key, head, nxt in (("row_A", "**ROW A,", "**ROW B,"), ("row_B", "**ROW B,", "**Three constraints")):
    i, j = s35.find(head), s35.find(nxt)
    entries = []
    for r in rows(s35[i:j]):
        c0 = r[0].replace('**', '').strip()
        if not c0 or c0.lower() == "order": continue
        entries.append(r[1].replace('**', '').strip())
    checks += 1
    if entries != bf[row_key]["entries"]:
        fails.append(f"3.5 {row_key}: D3 order {entries}, model order {bf[row_key]['entries']}")
    checks += 1
    if len(entries) != bf[row_key]["count"]:
        fails.append(f"3.5 {row_key}: D3 has {len(entries)} grips, model says {bf[row_key]['count']}")
checks += 1
if bf["row_A"]["count"] + bf["row_B"]["count"] != bf["grip_count"]:
    fails.append("3.5 grip count does not equal row A plus row B")

# ---- 3.6 the door ----------------------------------------------------------
s36 = section("## SHEET 3.6.", "## SHEET 3.7.")
doc_dev = []
for r in rows(s36):
    c0 = r[0].replace('**', '').strip()
    # the position table's first cell is "1", "1, HINGE end", "5, LATCH end".
    # the depth table's is a bare row count whose second cell is a millimetre
    # figure, so a name test separates them without depending on order.
    if re.match(r'^\d+(,|\s|$)', c0) and len(r) > 1 and num(r[1]) is None:
        doc_dev.append(r[1].replace('**', '').strip())
mod_dev = [d["device"] for d in MODEL["door"]["devices"]]
checks += 1
if doc_dev != mod_dev:
    fails.append(f"3.6 device order: D3 {doc_dev}, model {mod_dev}")
depth = {}
for r in rows(s36):
    n0 = num(r[0])
    if n0 and len(r) > 1 and num(r[1]) and n0 in (1, 2, 3):
        depth[str(int(n0))] = num(r[1])
for k, v in MODEL["door"]["depth_by_rows"].items():
    check(f"3.6 depth at {k} row(s)", depth.get(k), v)

# ---- 3.7 the ground bars ---------------------------------------------------
s37 = section("## SHEET 3.7.", "## SHEET 3.8.")
gb = MODEL["ground_bars"]
checks += 1
if f"{gb['each']['length']}" not in s37:
    fails.append(f"3.7 bar length {gb['each']['length']} not found in D3")
checks += 1
if str(gb["min_hole_spacing"]) not in s37:
    fails.append(f"3.7 min hole spacing {gb['min_hole_spacing']} not found in D3")
land = re.search(r'([A-Za-z-]+) landings\.\s*([A-Za-z-]+) used\.\s*([A-Za-z-]+) spare', s37)
WORDS = {"twelve": 12, "twenty-four": 24, "twentyfour": 24}
if land:
    check("3.7 landings total", WORDS.get(land.group(1).lower()), gb["landings"]["total"])
    check("3.7 landings used",  WORDS.get(land.group(2).lower()), gb["landings"]["used"])
    check("3.7 landings spare", WORDS.get(land.group(3).lower()), gb["landings"]["spare"])
else:
    fails.append("3.7 landings sentence not found")
    checks += 1

# ---- empties: the model may not invent a figure D3 leaves blank -------------
EMPTIES = [("enclosure.door_to_plate_clear_depth", MODEL["enclosure"]["door_to_plate_clear_depth"]),
           ("enclosure.usable_door_area_inset",   MODEL["enclosure"]["usable_door_area_inset"]),
           ("enclosure.mounting_holes",           MODEL["enclosure"]["mounting_holes"]),
           ("bottom_face.x_positions",            MODEL["bottom_face"]["x_positions"]),
           ("door.c_c_floor",                     MODEL["door"]["c_c_floor"]),
           ("ducts.chosen_width",                 MODEL["ducts"]["chosen_width"])]
for name, v in EMPTIES:
    checks += 1
    if v is not None:
        fails.append(f"EMPTY CELL FILLED BY THE MODEL: {name} = {v!r}. D3 leaves it empty with a blocker.")

# ---- report ----------------------------------------------------------------
print(f"ROUND TRIP: model/main-panel.json against enclosure-layout.md")
print(f"{checks} field comparisons")
print()
if fails:
    print(f"MISMATCHES: {len(fails)}   NOTHING IS DRAWN UNTIL THESE ARE RESOLVED")
    for f in fails: print(f"  {f}")
else:
    print("CLEAN. Every figure in the model is the figure D3 holds, and every cell")
    print("D3 leaves empty is empty in the model. The transcription is proved.")
sys.exit(1 if fails else 0)
