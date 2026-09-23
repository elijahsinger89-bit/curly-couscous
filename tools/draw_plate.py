#!/usr/bin/env python3
"""
D3 SHEET 3.2 AND 3.3 AS A DRAWING. Generated from model/main-panel.json.

IT DRAWS NOTHING THE MODEL DOES NOT HOLD. Where the model is null the drawing
says EMPTY on the face of the sheet, in the place the figure would go, so a
missing dimension is visible rather than absent.

It is an ELEVATION: the plate face, X and Y. There is no section, because the
depth axis has five null cells and a section drawn through them would be the
drawing inventing geometry - the exact thing the round-trip proof exists to
stop.

Refuses to run if tools/roundtrip_d3.py has not passed.

    python3 tools/draw_plate.py > plate-elevation.svg
"""
import json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rc = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "roundtrip_d3.py")],
                    capture_output=True, text=True)
if rc.returncode != 0:
    sys.stderr.write("ROUND TRIP FAILED. NOTHING IS DRAWN.\n" + rc.stdout)
    sys.exit(1)

M = json.load(open(os.path.join(ROOT, "model", "main-panel.json")))
plate, box = M["plate"] if "plate" in M else M["enclosure"]["plate"], M["enclosure"]["box"]

S = 1.4                      # px per mm
PAD = 150
DUCT = 25                    # the SMALLEST catalogue width, drawn dashed and labelled EMPTY
W = box["width"] * S + PAD * 2
H = box["height"] * S + PAD * 2 + 120

def x(mm): return PAD + (box["width"] - plate["width"]) / 2 * S + mm * S
def y(mm): return PAD + box["height"] * S - (box["height"] - plate["height"]) / 2 * S - mm * S

o = []
A = o.append
A(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:.0f}" height="{H:.0f}" '
  f'viewBox="0 0 {W:.0f} {H:.0f}" font-family="ui-monospace,Menlo,Consolas,monospace">')
A('<style>'
  ':root{--ink:#111;--pale:#888;--empty:#b23;--bg:#fff}'
  '@media (prefers-color-scheme: dark){:root{--ink:#e8e8e8;--pale:#888;--empty:#f66;--bg:#151515}}'
  'text{fill:var(--ink)}.s{font-size:11px}.t{font-size:15px;font-weight:700}'
  '.e{fill:var(--empty);font-size:11px;font-weight:700}'
  '.d{stroke:var(--pale);stroke-width:1;fill:none;stroke-dasharray:5 4}'
  '.l{stroke:var(--ink);stroke-width:1.2;fill:none}'
  '.f{fill:none;stroke:var(--ink);stroke-width:1}'
  '</style>')
A(f'<rect width="{W:.0f}" height="{H:.0f}" fill="var(--bg)"/>')

A(f'<text x="{PAD}" y="42" class="t">MAIN PANEL - PLATE ELEVATION, PORTRAIT</text>')
A(f'<text x="{PAD}" y="62" class="s">GENERATED from model/main-panel.json. Not drawn. '
  f'Round trip against enclosure-layout.md passed before this sheet was written.</text>')
A(f'<text x="{PAD}" y="78" class="s">Scale {S} px per mm. Box {box["width"]} x {box["height"]} x '
  f'{box["depth"]}. Plate {plate["width"]} x {plate["height"]}.</text>')
A(f'<text x="{PAD}" y="94" class="e">RECTANGLES ARE RAIL WIDTH x BAND ENVELOPE. A device\'s own '
  f'height above the rail is EMPTY for every part but two, so it is not drawn.</text>')

# box and plate
A(f'<rect x="{PAD}" y="{PAD}" width="{box["width"]*S:.1f}" height="{box["height"]*S:.1f}" class="f"/>')
A(f'<text x="{PAD+4}" y="{PAD-8}" class="s">BOX {box["width"]} x {box["height"]}</text>')
A(f'<rect x="{x(0):.1f}" y="{y(plate["height"]):.1f}" width="{plate["width"]*S:.1f}" '
  f'height="{plate["height"]*S:.1f}" class="l"/>')

# bands, stacked from an UNALLOCATED bottom margin
bands = sorted(M["bands"], key=lambda b: b["order"])
slack = M["band_totals"]["slack"]
base = 0.0
A(f'<text x="{x(0):.1f}" y="{y(0)+18:.1f}" class="e">BOTTOM MARGIN EMPTY - the {slack} mm of slack '
  f'is not allocated between margins and horizontal ducts, so every band Y floats with it</text>')

KEYS = {"B1": "B1_items", "B2": "B2_items", "B3": "B3_items", "B4": "B4_items"}
for b in bands:
    h = b["height"]
    A(f'<rect x="{x(DUCT):.1f}" y="{y(base+h):.1f}" width="{(plate["width"]-2*DUCT)*S:.1f}" '
      f'height="{h*S:.1f}" class="d"/>')
    A(f'<text x="{x(0)-96:.1f}" y="{y(base+h/2)+4:.1f}" class="s">{b["id"]} {b["name"]}</text>')
    A(f'<text x="{x(0)-96:.1f}" y="{y(base+h/2)+18:.1f}" class="s">{h} mm</text>')
    cur = DUCT
    for it in M[KEYS[b["id"]]]:
        wmm = it["rail"]
        name = it.get("device") or it.get("group")
        A(f'<rect x="{x(cur):.1f}" y="{y(base+h):.1f}" width="{wmm*S:.1f}" height="{h*S:.1f}" class="l"/>')
        cx, cy = x(cur + wmm / 2), y(base + h / 2)
        A(f'<text x="{cx:.1f}" y="{cy:.1f}" class="s" text-anchor="middle" '
          f'transform="rotate(-90 {cx:.1f} {cy:.1f})">{name[:28]}</text>')
        A(f'<text x="{cx:.1f}" y="{y(base)-5:.1f}" class="s" text-anchor="middle">{wmm:g}</text>')
        cur += wmm
    # THE DRAWING CHECKS THE DOCUMENT WHILE IT DRAWS IT. A band's stated "Used"
    # figure must equal the sum of the rows above it, and a drawing that lays the
    # rows out end to end is the first thing that ever adds them.
    # B1's stated figure is "of 256 BESIDE the NDR", so the NDR's own 73 mm is
    # outside that frame. Comparing across frames is F-128's defect and the check
    # must not commit it while reporting it.
    ssum = round(cur - DUCT - (73 if b["id"] == "B1" else 0), 1)
    stated = M[f'{b["id"]}_used']
    lo = stated.get("value", stated.get("min"))
    hi = stated.get("value", stated.get("max"))
    ok = lo is not None and (abs(ssum - lo) < 0.05 or abs(ssum - hi) < 0.05)
    txt = f'{ssum:g} laid out, of {b["rail_usable"]["d25"]}'
    A(f'<text x="{x(cur+6):.1f}" y="{y(base+h/2)+4:.1f}" class="s">{txt}</text>')
    if not ok:
        A(f'<text x="{x(cur+6):.1f}" y="{y(base+h/2)+18:.1f}" class="e">'
          f'D3 SAYS {lo:g}{"" if lo==hi else " to %g"%hi} USED. THE ROWS SUM TO {ssum:g}. F-130</text>')
        sys.stderr.write(f"BAND {b['id']}: rows sum to {ssum}, D3 states {lo} to {hi}\n")
    base += h

# the ducts: width not chosen
for xm in (0, plate["width"] - DUCT):
    A(f'<rect x="{x(xm):.1f}" y="{y(plate["height"]):.1f}" width="{DUCT*S:.1f}" '
      f'height="{plate["height"]*S:.1f}" class="d"/>')
A(f'<text x="{x(2):.1f}" y="{y(plate["height"])-8:.1f}" class="e">DUCT WIDTH EMPTY - drawn at the '
  f'smallest catalogue size, 25 mm. 40, 60, 80, 100 and 150 also clear the rail budget at 60 and below.</text>')

# ground bars, in the slack below B1
gb = M["ground_bars"]
gy = base + 10
for i in range(gb["count"]):
    A(f'<rect x="{x(DUCT + 6 + i*(gb["each"]["length"]+8)):.1f}" y="{y(gy+gb["each"]["width"]):.1f}" '
      f'width="{gb["each"]["length"]*S:.1f}" height="{gb["each"]["width"]*S:.1f}" class="l"/>')
A(f'<text x="{x(DUCT+6):.1f}" y="{y(gy)-3:.1f}" class="s">TWO GROUND BARS, {gb["each"]["length"]} '
  f'each, side by side below B1. Holes at least {gb["min_hole_spacing"]} apart. Y POSITION EMPTY.</text>')

# the footer: what is empty, counted
yy = PAD + box["height"] * S + 34
A(f'<text x="{PAD}" y="{yy}" class="t">EMPTY ON THIS SHEET, WITH ITS OWNER</text>')
for i, (what, who) in enumerate([
    ("Duct width, and therefore every band's usable rail", "MAIN-PANEL, after the conductor list and a gauge"),
    ("The 72 mm of slack, split between margins and horizontal ducts", "MAIN-PANEL"),
    ("Device height above the rail, 4 of 5 parts", "OWNER, measured with a caliper. F-128"),
    ("Device depth off the rail, 4 of 5 parts - no section can be drawn", "OWNER, measured with a caliper. F-128"),
    ("The five sense-circuit burdens' carrier", "MAIN-PANEL. No part yet, so nothing to measure"),
]):
    A(f'<text x="{PAD}" y="{yy+20+i*16}" class="s">EMPTY  {what}  -  {who}</text>')
A('</svg>')
print("\n".join(o))
