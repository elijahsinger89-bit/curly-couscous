"""
strategies.py - machining strategy database for the part wizards.

Maps part types to ordered operations per setup (Op10, Op20, Op30). Every
operation name is an operation in job_types.py; its settings per material are in job_settings.json.

    import strategies
    strategies.plan("wing_rib", "N - Aluminum", "Op10")      # full step detail
    strategies.operations("landing_gear_beam", "S - Titanium", "Op10")  # operation names
    strategies.setup_for("wing_rib", "AE10958 ... Op20")     # 'Op20'
    strategies.parts()                                       # catalog listing

Pure Python, no hyperMILL imports: runs offline for checking.
"""
VERSION = "2026-10-14-b"


# ----------------------------------------------------------------------------
# Operation catalog: the 21 operations with saved settings in job_settings.json
# ----------------------------------------------------------------------------
OPS = {
    "Face Mill":                 ("face",   "Bullnose end mill used as face mill"),
    "Rough HEM":                 ("rough",  "3D optimized HEM roughing, large ap / small ae"),
    "Pocket HEM":                ("rough",  "HEM roughing confined to pockets, helical entry"),
    "Rough Traditional":         ("rough",  "3D optimized conventional roughing"),
    "3D Plunge Roughing":        ("rough",  "Plunge roughing, long overhang or weak setup"),
    "Plunge Milling":            ("rough",  "Plunge milling of slots and pockets"),
    "Automatic Rest Machining":  ("rest",   "Ball mill rest machining of remaining material"),
    "Contour Finish":            ("finish", "2D contour finish of walls"),
    "Plane Finish":              ("finish", "Flat floor finish"),
    "3D Profile Finish Ball":    ("finish", "3D profile finish with ball mill"),
    "Z Level Shape Finish":      ("finish", "Constant Z finish of steep faces"),
    "Centering":                 ("hole",   "Spot / center drill"),
    "Drill":                     ("hole",   "Standard drilling"),
    "Peck Drill":                ("hole",   "Peck drilling, deep holes"),
    "Chip Break Drill":          ("hole",   "Chip breaking cycle for long-chip materials"),
    "Helical Drilling":          ("hole",   "Helical interpolation of large holes"),
    "Boring":                    ("hole",   "Finish boring"),
    "Reaming":                   ("hole",   "Reaming to tolerance"),
    "Thread Milling":            ("hole",   "Thread milling"),
    "Tapping":                   ("hole",   "Tapping"),
    "Chamfer on 3D Model":       ("deburr", "Edge break and hole chamfers"),
    "Swarf Curve":               ("finish", "5-axis swarf along a curve, created directly"),
    "Swarf Surface":             ("finish", "5-axis swarf on surfaces, created directly"),
}
DIRECT_OPS = ("Swarf Curve", "Swarf Surface")   # created with CreateJob and hyperMILL's default settings (no saved settings)

# ----------------------------------------------------------------------------
# Step helpers. when = feature flag required ("flag") or absent ("!flag")
# ----------------------------------------------------------------------------
def S(op, why, when=None, count=1):
    """count = how many times the operation is made in this position (Pocket HEM count=6 makes six pocket jobs)."""
    assert op in OPS, op
    return {"op": op, "why": why, "when": when, "manual": False, "count": count}

def M(text, when=None):
    """Operation with no toolpath type: shown in the plan as a by-hand step."""
    return {"op": None, "why": text, "when": when, "manual": True, "count": 1}

def HOLES(chamfer=True):
    steps = [
        S("Centering", "Spot every hole so drills start on location", "holes"),
        S("Drill", "Drill through and blind holes", "holes"),
        S("Peck Drill", "Deep holes (over 4xD): peck to clear chips", "deep_holes"),
        S("Chip Break Drill", "Long-chip material: break chips", "stringy_chips"),
        S("Helical Drilling", "Large holes: helical ramp, lower force than drilling", "large_bores"),
        S("Boring", "Finish bore to size by circular interpolation or boring", "bores"),
        S("Reaming", "Ream to tolerance where specified", "reamed_holes"),
        S("Thread Milling", "Thread mill large or hard-material threads", "mill_threads"),
        S("Tapping", "Tap small threads", "tapped_holes"),
    ]
    if chamfer:
        steps.append(S("Chamfer on 3D Model", "Break hole and edge chamfers last", "holes"))
    return steps

# ----------------------------------------------------------------------------
# Material rules, keyed on the ISO letter that starts the material group
# ----------------------------------------------------------------------------
MATERIAL_RULES = {
    "P": {"swap": {}, "drop": [], "notes": ["Low alloy / carbon steel: HEM roughing at full flute length is the baseline."]},
    "M": {"swap": {"Rough Traditional": "Rough HEM"}, "drop": [],
          "notes": ["Stainless work hardens: keep constant chip load, no dwelling, light finish pass depth over 0.005 in."]},
    "K": {"swap": {}, "drop": [], "notes": ["Cast iron: dry or air blast; no flood on HEM."]},
    "N": {"swap": {}, "drop": [],
          "notes": ["Aluminum / copper alloys: highest spindle speed; thin walls take overlapping light passes."]},
    "S": {"swap": {"Rough Traditional": "Rough HEM"}, "drop": [],
          "notes": ["Titanium / HRSA: low ae, high ap, constant engagement, roll in and out of cut, high pressure coolant."]},
    "H": {"swap": {"Rough HEM": "Rough Traditional", "Pocket HEM": "Rough Traditional"},
          "drop": ["Plunge Milling", "3D Plunge Roughing"],
          "notes": ["Hardened steel: rough in the soft state if the process allows; finish only with small stock left."]},
}

def iso_letter(material_group):
    return (material_group or "?").strip()[:1].upper()

# ----------------------------------------------------------------------------
# Part catalog
# ----------------------------------------------------------------------------
PARTS = {}

def P(key, name, family, iso, source, features, setups, apply, ordered=False):
    """ordered=True: the step order is final (no geometry reordering, no merging of repeated operations)."""
    PARTS[key] = {"name": name, "family": family, "iso": iso, "source": source,
                  "features": set(features), "setups": setups, "apply": apply, "ordered": ordered}

SAND = "Sandvik Coromant aerospace application guide"
GEN = "General shop practice; CIMCO CNC handbook ch.7 operation order (face, contour, pocket, spot, drill, counterbore)"

# ---- Aluminum structure ----------------------------------------------------
P("wing_rib", "Wing rib", "Aluminum structure", ["N"], SAND + ": Wing ribs",
  ["flat_faces", "thin_wall", "deep_pocket", "holes"],
  {"Op10": [
      S("Face Mill", "Skim the datum face first", "flat_faces"),
      S("Rough HEM", "High-speed roughing, small ap/ae, high Vc, to clear the bulk"),
      S("Pocket HEM", "Pockets: helical entry, no pilot drill needed", "deep_pocket"),
      S("Contour Finish", "Walls in overlapping slicing passes; thin walls (15:1 to 30:1) use step support, finish last", "thin_wall"),
      S("Plane Finish", "Pocket floors and web faces", "flat_faces"),
      M("Corner slicing: successive light passes with a dedicated Al end mill, low radial immersion", "thin_wall"),
      *HOLES()],
   "Op20": [
      S("Face Mill", "Machine the second side datum"),
      S("Rough HEM", "Clear second side; leave uniform wall thickness"),
      S("Contour Finish", "Finish outer profile and flanges"),
      S("Plane Finish", "Finish web floors"),
      S("Chamfer on 3D Model", "Deburr all edges")]},
  ["Wall thickness to height decides passes: ratio 15:1 to 30:1 uses step support in overlapping passes.",
   "Use balanced tools and the highest spindle speed the machine allows.",
   "Run roughing on both sides before any finish so internal stress releases first."])

P("wing_spar", "Wing spar / long pocketed beam", "Aluminum structure", ["N"],
  SAND + ": Aluminum components (spars, skins, ribs); thin wall strategy",
  ["flat_faces", "thin_wall", "deep_pocket", "holes", "thin_floor", "warpage"],
  {"Op10": [
      S("Face Mill", "Datum face", "flat_faces"),
      S("Rough HEM", "Bulk removal with constant engagement"),
      S("Pocket HEM", "Pocket clearing, leave 0.02-0.04 in floor and wall stock", "deep_pocket"),
      S("Plane Finish", "Floors last; thin floors in a spiral from center out", "thin_floor"),
      S("Contour Finish", "Walls: semi pass then finish pass after the floor", "thin_wall"),
      *HOLES()],
   "Op20": [
      S("Rough HEM", "Back side bulk removal"),
      S("Plane Finish", "Back side faces"),
      S("Contour Finish", "Outer profile"),
      S("Chamfer on 3D Model", "Deburr")]},
  ["Long parts: machine symmetrically from the center out to limit bow.",
   "Leave stock for a spring pass on thin sections."])

P("heat_sink_enclosure", "Thin-wall enclosure / heat sink", "Aluminum structure", ["N"],
  GEN + "; Sandvik Coromant thin-wall guidance",
  ["flat_faces", "thin_wall", "deep_pocket", "holes", "tapped_holes"],
  {"Op10": [
      S("Face Mill", "Face the top"),
      S("Rough HEM", "Clear outer form"),
      S("Pocket HEM", "Internal cavity", "deep_pocket"),
      S("Contour Finish", "Fin and wall finish in light passes", "thin_wall"),
      S("Plane Finish", "Cavity floor"),
      *HOLES()],
   "Op20": [
      S("Face Mill", "Face the base"),
      S("Rough HEM", "Back side relief"),
      S("Plane Finish", "Mounting faces"),
      S("Chamfer on 3D Model", "Deburr")]},
  ["Soft jaws or a vacuum fixture avoid clamp distortion.",
   "Finish thin fins with ae under 0.1 in and a climb pass only."])

# ---- Composite structure (edge trim and hole making only) --------------------
P("central_wing_box", "Central wing box (composite stack)", "Composite structure", ["N"],
  SAND + ": Central wing box",
  ["flat_faces", "holes", "stringy_chips"],
  {"Op10": [
      S("Plane Finish", "Surface machine the carbon skin: PCD cutter, minimal splintering", "flat_faces"),
      S("Contour Finish", "Edge trim"),
      S("Centering", "Spot through the stack", "holes"),
      S("Drill", "Drill carbon/Al/Ti stack with solid carbide -O geometry, 3-10xD", "holes"),
      S("Chip Break Drill", "Stack with titanium layer: break chips", "stringy_chips"),
      S("Chamfer on 3D Model", "Deburr", "holes")]},
  ["Different layers need different feeds: program the metal layer with its own data.",
   "No coolant on dry CFRP; vacuum extraction for dust."])

P("vertical_tail_frame", "Vertical tail frame (composite and Al)", "Composite structure", ["N"],
  SAND + ": Vertical tails",
  ["holes", "flat_faces"],
  {"Op10": [
      S("Contour Finish", "Edge trim"),
      S("Plane Finish", "Mating faces"),
      S("Centering", "Spot holes", "holes"),
      S("Drill", "CFRP-grade solid carbide drills, 3-10xD, minimal delamination", "holes"),
      S("Boring", "Final hole size where tolerance requires", "holes")]},
  ["Main challenges are hole making, edging and surface machining."])

P("composite_wing_skin", "Composite wing skin / panel", "Composite structure", ["N"],
  SAND + ": Wings (CoroMill Century, Sturtz milling, CoroDrill 863)",
  ["flat_faces", "holes", "3d_surface"],
  {"Op10": [
      S("Plane Finish", "Surface machine flat areas with a PCD face cutter", "flat_faces"),
      S("3D Profile Finish Ball", "Contoured skin: tilt the tool 2-10 degrees (Sturtz) for about 3x faster surface generation", "3d_surface"),
      S("Contour Finish", "Edge trim"),
      S("Drill", "Carbon-grade drills, depth 3-10xD", "holes"),
      S("Chamfer on 3D Model", "Edge break", "holes")]},
  ["Sturtz milling: tilt the cutter 2-10 degrees, large stepover, versus ball-end scanning.",
   "Ball-end scanning example: 0.139 in stepover versus 0.433 in with Sturtz at the same data."])

# ---- Titanium structure --------------------------------------------------------
P("engine_mount", "Engine mount (titanium)", "Titanium structure", ["S"],
  SAND + ": Engine mounts",
  ["flat_faces", "deep_slot", "holes", "boss"],
  {"Op10": [
      S("Face Mill", "Datum faces", "flat_faces"),
      S("Rough HEM", "Outer form with low ae, high ap, roll in and out"),
      S("Plunge Milling", "Deep center slot: plunge when set-up is weak or overhang is long", "deep_slot"),
      S("Rough HEM", "Deep slot in side-milling passes when the machine is stable and powerful", "!deep_slot"),
      M("Deep slot alternative: side and face cutter, or high-feed cutter at up to 0.04 in/tooth with low ap", "deep_slot"),
      S("Contour Finish", "Walls"),
      S("Plane Finish", "Faces and slot floor"),
      *HOLES()],
   "Op20": [
      S("Rough HEM", "Second side"),
      S("Contour Finish", "Profile finish"),
      S("Plane Finish", "Faces"),
      S("Chamfer on 3D Model", "Deburr")]},
  ["Deep slot is the hardest feature: choose between side-milling, high-feed light method, or plunging.",
   "Plunge needs a reasonable stepover to stay productive."])

P("thrust_fitting", "Thrust fitting (titanium)", "Titanium structure", ["S"],
  SAND + ": Thrust fittings",
  ["flat_faces", "long_reach", "holes"],
  {"Op10": [
      S("Face Mill", "Datum faces", "flat_faces"),
      S("Rough HEM", "2D profile milling at high productivity, low ae"),
      S("Contour Finish", "Profile finish with the shortest possible tool; long reach sets the overhang", "long_reach"),
      S("Plane Finish", "Faces"),
      *HOLES()],
   "Op20": [
      S("Rough HEM", "Second side"),
      S("Contour Finish", "Profile finish"),
      S("Chamfer on 3D Model", "Deburr")]},
  ["Main challenge is long overhang tooling: keep assembly short and rigid, largest possible adapter, tapered adapter for small cutters."])

P("pylon_bracket", "Pylon bracket (titanium)", "Titanium structure", ["S"],
  SAND + ": Pylon brackets",
  ["flat_faces", "deep_slot", "closed_angle", "holes", "3d_surface"],
  {"Op10": [
      S("Face Mill", "Datum faces", "flat_faces"),
      S("Rough HEM", "Open design: roughing with exchangeable head cutter"),
      S("Plunge Milling", "Deep narrow slots when rigid side cutters are not possible", "deep_slot"),
      S("Automatic Rest Machining", "Closed angles: slicing with a ball nose clears remaining material", "closed_angle"),
      S("3D Profile Finish Ball", "Closed pockets and angles with conical ball nose; 4 axis for one closed side, 5 axis for both", "closed_angle"),
      S("Contour Finish", "Walls"),
      S("Plane Finish", "Floors"),
      M("Closed angles under 90 degrees need 4- or 5-axis positioning; 3-axis toolpaths cover open geometry only", "closed_angle"),
      *HOLES()],
   "Op20": [
      S("Rough HEM", "Back side"),
      S("Contour Finish", "Profile finish"),
      S("Chamfer on 3D Model", "Deburr")]},
  ["Slicing method for closed corners, ball nose in multiple passes with low engagement."])

P("landing_gear_beam", "Landing gear beam (titanium)", "Titanium structure", ["S"],
  SAND + ": Landing gear beams",
  ["flat_faces", "deep_pocket", "thin_floor", "thin_wall", "boss", "holes"],
  {"Op10": [
      S("Face Mill", "Rough face: roll into cut clockwise so chip thickness at exit is zero; round insert style", "flat_faces"),
      S("Rough HEM", "2D profile roughing, high-pressure coolant at 70 bar or more"),
      S("Pocket HEM", "Pockets: circular ramp, low ap, high feed per tooth; no pilot drill", "deep_pocket"),
      S("Rough HEM", "Open the pocket by spiral morph with large corner radii", "deep_pocket"),
      S("Plane Finish", "Thin floors: spiral morph from center, constant light stock for the finish cut", "thin_floor"),
      S("Contour Finish", "Walls and corners; corners in slicing passes", "thin_wall"),
      *HOLES()],
   "Op20": [
      S("Rough HEM", "Back side"),
      S("Plane Finish", "Back faces"),
      S("Contour Finish", "Outer profile"),
      S("Chamfer on 3D Model", "Deburr")]},
  ["Thin floors deflect: machine the floor last with minimal remaining stock and optimized ap/ae.",
   "Always use coolant on titanium; through-spindle at 70 bar and about 13 gal/min is the recommendation."])

P("main_fitting", "Main landing gear fitting (300M or Ti-5553)", "Titanium and high alloy steel", ["S", "P"],
  SAND + ": Main fittings",
  ["flat_faces", "boss", "deep_holes", "3d_surface", "turned", "holes"],
  {"Op10": [
      M("Rough and finish turn the bores and OD on a mill-turn or lathe first", "turned"),
      S("Face Mill", "Datum faces", "flat_faces"),
      S("Rough HEM", "Roll in around bosses, round insert style, high feed"),
      S("Z Level Shape Finish", "Semi-finish profile with ball nose", "3d_surface"),
      S("3D Profile Finish Ball", "Finish copy milling of contoured surfaces", "3d_surface"),
      S("Contour Finish", "Boss and wall finish"),
      S("Peck Drill", "Deep hole drilling", "deep_holes"),
      *HOLES()],
   "Op20": [
      S("Rough HEM", "Second side"),
      S("Contour Finish", "Profile finish"),
      S("Chamfer on 3D Model", "Deburr")]},
  ["Main challenges: deep hole drilling, internal turning, profile milling."])

# ---- Stainless / high alloy steel ---------------------------------------------
P("flap_track", "Flap track (15-5 PH)", "Stainless and high alloy steel", ["M"],
  SAND + ": Flap tracks",
  ["flat_faces", "deep_pocket", "deep_slot", "holes"],
  {"Op10": [
      S("Face Mill", "Enter the cut at 50% feed until fully engaged", "flat_faces"),
      S("Rough HEM", "2D profile roughing"),
      S("Pocket HEM", "Deep narrow pockets: high-feed pocketing, secure at long overhang", "deep_pocket"),
      S("Rough HEM", "Deep slot in side-milling passes", "deep_slot"),
      S("Contour Finish", "Profile finish"),
      S("Plane Finish", "Slot and pocket floors"),
      *HOLES()],
   "Op20": [
      S("Rough HEM", "Second side"),
      S("Contour Finish", "Profile finish"),
      S("Chamfer on 3D Model", "Deburr")]},
  ["Narrow deep pockets mean long overhang and vibration risk: reduce ae, keep ap high."])

P("slat_track", "Slat track (maraging steel)", "Stainless and high alloy steel", ["P", "M"],
  SAND + ": Slat tracks",
  ["flat_faces", "deep_pocket", "deep_slot", "holes"],
  {"Op10": [
      S("Face Mill", "Enter at 50% feed until fully engaged", "flat_faces"),
      S("Rough HEM", "2D profile roughing, tough long-edge cutter"),
      S("Pocket HEM", "2D pocket roughing", "deep_pocket"),
      S("Rough HEM", "Deep slot, side-milling passes", "deep_slot"),
      S("Contour Finish", "Profile finish"),
      S("Plane Finish", "Floors"),
      *HOLES()],
   "Op20": [
      S("Rough HEM", "Second side"),
      S("Contour Finish", "Profile finish"),
      S("Chamfer on 3D Model", "Deburr")]},
  ["Rough in the annealed state when possible; finish after heat treat with small stock."])

# ---- Engine rotating and casing ------------------------------------------------
P("fan_disc", "Fan disc (titanium)", "Engine rotating", ["S"],
  SAND + ": Fan discs",
  ["turned", "deep_slot", "holes", "bores"],
  {"Op10": [
      M("Turn the internal chambers and OD with dampened SL70 blades, direct grooving for roughing", "turned"),
      S("Rough HEM", "Tulip slots: full-slot or trochoidal roughing instead of broaching", "deep_slot"),
      S("Contour Finish", "Tulip slot profile with the same tool"),
      S("Centering", "Spot flange holes", "holes"),
      S("Peck Drill", "Flange holes in titanium", "holes"),
      S("Boring", "Finish bores", "bores"),
      S("Chamfer on 3D Model", "Deburr", "holes")]},
  ["Tulip slot roughing uses an engineered cutter; verify slot form tool before relying on the generic toolpath."])

P("fan_casing", "Fan casing (titanium)", "Engine casing", ["S"],
  SAND + ": Fan casings",
  ["turned", "boss", "large_bores", "bores", "mill_threads", "holes"],
  {"Op10": [
      M("Turn ID/OD with round inserts and high-pressure coolant", "turned"),
      S("Rough HEM", "High-feed side milling around bosses; roll-in, round insert style"),
      S("Helical Drilling", "Large holes: helical ramp lowers force; drilling suffers interrupted exit", "large_bores"),
      S("Contour Finish", "Boss walls"),
      S("Plane Finish", "Boss and flange faces"),
      S("Centering", "Spot", "holes"),
      S("Drill", "Short-hole drilling", "holes"),
      S("Boring", "Finish bore by circular interpolation: one tool covers many sizes", "bores"),
      S("Thread Milling", "Thread mill in titanium", "mill_threads"),
      S("Chamfer on 3D Model", "Deburr", "holes")]},
  ["Cutting temperature is the key: coolant always, no ceramic on titanium."])

P("impeller", "Impeller (titanium or HRSA)", "Engine rotating", ["S"],
  SAND + ": Impellers",
  ["blades", "3d_surface", "deep_slot", "holes", "bores"],
  {"Op10": [
      S("Rough HEM", "Roughing slot between blades: trochoidal with roll entry, controlled engagement arc", "blades"),
      S("Plunge Milling", "Plunge roughing of small deep slots with limited tool diameter, long overhang", "deep_slot"),
      S("Automatic Rest Machining", "Rest between blades after the rough", "blades"),
      S("Z Level Shape Finish", "Semi-finish blade and hub with ball nose", "3d_surface"),
      S("3D Profile Finish Ball", "Point milling finish; tilt for reach", "3d_surface"),
      M("Blade flank finish with conical ball nose needs 5-axis simultaneous; the 3-axis toolpaths only approximate", "blades"),
      S("Drill", "Bolt holes: solid carbide HRSA drill", "holes"),
      S("Boring", "Finish bore by circular interpolation", "bores"),
      S("Chamfer on 3D Model", "Deburr", "holes")]},
  ["Requires a 5-axis machine with good simultaneous dynamics and 5-axis CAM.",
   "Flank milling is fastest when the CAM and tool allow it."])

P("blisk_titanium", "Blisk (titanium)", "Engine rotating", ["S"],
  SAND + ": Aerospace blisk in titanium",
  ["blades", "3d_surface", "deep_slot"],
  {"Op10": [
      S("Rough HEM", "Rough slotting between blades: high feed side milling, small radial engagement", "blades"),
      S("Plunge Milling", "Plunge slots with Gannet-type cutter, small deep slots, long overhang", "deep_slot"),
      S("Automatic Rest Machining", "Rest clear to even semi-finish stock", "blades"),
      S("Z Level Shape Finish", "Semi-finish hub and fillet", "3d_surface"),
      S("3D Profile Finish Ball", "Finish blade with ball nose, lollipop for undercuts", "3d_surface"),
      M("Blade flank semi-finish and finish: 5-axis flank milling with conical ball or barrel tools", "blades")]},
  ["Overhang up to 6xD with modular EH system; balance tool length with stiffness."])

P("blisk_hrsa", "Blisk (HRSA, hot side)", "Engine rotating", ["S"],
  SAND + ": Aerospace Blisk in HRSA",
  ["blades", "3d_surface", "deep_slot", "holes"],
  {"Op10": [
      S("Rough HEM", "Engineered rough slot concept or high feed side milling, small ae, grade for nickel alloy", "blades"),
      S("Plunge Milling", "Rough open between blades with plunge milling", "deep_slot"),
      S("Automatic Rest Machining", "Rest stock before semi-finish", "blades"),
      S("Z Level Shape Finish", "Semi-finish", "3d_surface"),
      S("3D Profile Finish Ball", "Finish blade, ceramic ball nose where speed matters", "3d_surface"),
      M("Blade flank finish is 5-axis simultaneous", "blades"),
      S("Drill", "Short hole drilling in nickel alloy", "holes")]},
  ["Hot-side blisks are nickel alloys: expect the lowest cutting speeds and highest tool wear in this catalog."])

P("turbine_disc", "Turbine disc (HRSA)", "Engine rotating", ["S"],
  SAND + ": Turbine disc; Running red hot (first, intermediate, last stage machining)",
  ["turned", "scallop", "holes", "bores"],
  {"Op10": [
      M("First stage: turn basic shape in the soft condition (about 25 HRC), productivity first", "turned"),
      S("Rough HEM", "Scallop roughing with exchangeable-head cutter", "scallop")],
   "Op20": [
      M("Intermediate stage after aging (36-46 HRC): turn to near net with stock left", "turned"),
      S("Contour Finish", "Scallop finish with high-feed side milling concept to avoid burrs", "scallop"),
      S("Centering", "Spot holes", "holes"),
      S("Drill", "Short-hole drilling for nickel alloy", "holes"),
      S("Boring", "Finish bores", "bores"),
      S("Chamfer on 3D Model", "Deburr", "holes")],
   "Op30": [
      M("Last stage: finish turn, surface integrity first, small depth of cut, carbide or CBN", "turned")]},
  ["HRSA has three stages: first (soft), intermediate (aged, stock left), last (final surface).",
   "Critical rotating parts need a certified process: do not change tools or data after release."])

P("spool", "Spool (HRSA)", "Engine rotating", ["S"],
  SAND + ": Aerospace spool",
  ["turned", "deep_slot", "holes"],
  {"Op10": [
      M("Turn deep internal chambers with dampened blades; trochoidal turning with ceramic", "turned"),
      S("Rough HEM", "Tulip grooves: trochoidal roughing", "deep_slot"),
      S("Contour Finish", "Groove profile finish"),
      S("Drill", "Holes", "holes"),
      S("Chamfer on 3D Model", "Deburr", "holes")]},
  ["Two hard features: deep internal chambers (turning) and external tulip grooves (milling)."])

P("combustion_casing", "Combustion casing (Inconel / Waspaloy)", "Engine casing", ["S"],
  SAND + ": Combustion casing",
  ["turned", "boss", "large_bores", "bores", "mill_threads", "tapped_holes", "holes", "deep_holes"],
  {"Op10": [
      M("Turn casing profile; the large milling content is the bigger cost driver", "turned"),
      S("Rough HEM", "Heavy milling: high feed roughing with large cutting width"),
      S("Helical Drilling", "Large holes by helical ramp", "large_bores"),
      S("Automatic Rest Machining", "Stock left around bosses"),
      S("Contour Finish", "Semi-finish with high feed side milling"),
      S("Plane Finish", "Casing floor and flange faces: high-speed super finishing"),
      S("Centering", "Spot", "holes"),
      S("Drill", "Short hole drilling for nickel alloy", "holes"),
      S("Peck Drill", "Deeper holes", "deep_holes"),
      S("Boring", "Finish bore by circular interpolation", "bores"),
      S("Thread Milling", "Thread mill nickel alloy threads", "mill_threads"),
      S("Tapping", "Tap small threads", "tapped_holes"),
      S("Chamfer on 3D Model", "Deburr", "holes")]},
  ["Roll-in toolpath around bosses with round inserts reduces notch wear."])

P("shaft", "Engine shaft (HRSA or high alloy steel)", "Engine rotating", ["S", "P"],
  SAND + ": Shaft; Turning exotic materials",
  ["turned", "bores", "holes", "mill_threads"],
  {"Op10": [
      M("Turn OD/ID with dampened boring bars (up to 14xD); multi-task machine", "turned"),
      S("Rough HEM", "Flange and spline milling", "!turned"),
      S("Contour Finish", "Flange profile"),
      S("Drill", "Short hole drilling", "holes"),
      S("Boring", "Finish bore by circular interpolation", "bores"),
      S("Thread Milling", "Thread mill", "mill_threads"),
      S("Chamfer on 3D Model", "Deburr", "holes")]},
  ["Challenges are length and internal features: multi-task machines with dampened tooling."])

# ---- General machined parts ----------------------------------------------------
P("manifold_block", "Hydraulic / fluid manifold block", "General machined parts", ["N", "P", "M"],
  GEN,
  ["flat_faces", "holes", "deep_holes", "cross_holes", "tapped_holes", "bores", "pocket"],
  {"Op10": [
      S("Face Mill", "Face top and datum", "flat_faces"),
      S("Rough HEM", "Contour and pockets", "pocket"),
      S("Pocket HEM", "Valve cavities", "pocket"),
      S("Contour Finish", "Outer contour"),
      S("Plane Finish", "Cavity floors and sealing faces"),
      S("Centering", "Spot all ports", "holes"),
      S("Drill", "Port drilling", "holes"),
      S("Peck Drill", "Deep cross drilled passages", "deep_holes"),
      S("Boring", "Valve cavity bores", "bores"),
      S("Thread Milling", "Large port threads", "mill_threads"),
      S("Tapping", "Tapped ports", "tapped_holes"),
      S("Chamfer on 3D Model", "Deburr cross-hole intersections", "holes")],
   "Op20": [S("Face Mill", "Face second side"), *HOLES()],
   "Op30": [S("Face Mill", "Face third side"), *HOLES()]},
  ["Cross-hole intersections: drill smaller to larger, deburr last.",
   "Plan one side per Op; machine the sealing faces last in the setup."])

P("valve_body", "Valve body / pump housing", "General machined parts", ["P", "M", "K"],
  GEN + "; MAPAL hydraulic valve housing machining (bores and seats)",
  ["flat_faces", "holes", "bores", "tapped_holes", "pocket", "reamed_holes"],
  {"Op10": [
      S("Face Mill", "Face mounting flange", "flat_faces"),
      S("Rough HEM", "Outer form"),
      S("Contour Finish", "Flange outline"),
      S("Plane Finish", "Gasket faces"),
      S("Centering", "Spot", "holes"),
      S("Drill", "Pilot and through holes", "holes"),
      S("Helical Drilling", "Large bores: rough by helical interpolation", "bores"),
      S("Boring", "Finish bore valve seats", "bores"),
      S("Reaming", "Ream guide bores to tolerance", "reamed_holes"),
      S("Tapping", "Tapped holes", "tapped_holes"),
      S("Chamfer on 3D Model", "Deburr", "holes")],
   "Op20": [S("Face Mill", "Second side flange"), S("Contour Finish", "Profile"), *HOLES()]},
  ["Rough bores first, finish bores after all faces are cut, so face stress does not move the bore."])

P("gearbox_housing", "Gearbox housing", "General machined parts", ["K", "N", "P"],
  GEN,
  ["flat_faces", "pocket", "holes", "bores", "tapped_holes", "large_bores"],
  {"Op10": [
      S("Face Mill", "Parting face", "flat_faces"),
      S("Rough HEM", "Internal pockets and bosses", "pocket"),
      S("Pocket HEM", "Cavity", "pocket"),
      S("Helical Drilling", "Bearing bores roughed by helical interpolation", "large_bores"),
      S("Boring", "Bearing bores to size after the face is finished", "bores"),
      S("Plane Finish", "Bearing shoulders and faces"),
      *HOLES()],
   "Op20": [S("Face Mill", "Opposite flange"), S("Rough HEM", "External form"), S("Contour Finish", "Profile"), *HOLES()]},
  ["Bearing bores in one setup with the parting face to hold concentricity and perpendicularity."])

P("bearing_housing_flange", "Bearing housing / flange", "General machined parts", ["P", "M", "N"],
  GEN,
  ["flat_faces", "bores", "holes", "tapped_holes", "turned"],
  {"Op10": [
      M("Turn OD/ID on a lathe where available", "turned"),
      S("Face Mill", "Face", "flat_faces"),
      S("Rough HEM", "Contour and bolt pad relief", "!turned"),
      S("Contour Finish", "Profile"),
      S("Plane Finish", "Seal faces"),
      S("Helical Drilling", "Large center bore", "bores"),
      S("Boring", "Finish bore", "bores"),
      *HOLES()],
   "Op20": [S("Face Mill", "Back face"), S("Contour Finish", "Back profile"), S("Chamfer on 3D Model", "Deburr")]},
  ["Bolt circle holes after bore so a hole pattern error cannot move the bore."])

P("end_cap_cylinder", "Hydraulic cylinder end cap / cover plate", "General machined parts", ["P", "M"],
  GEN,
  ["flat_faces", "pocket", "bores", "holes", "tapped_holes"],
  {"Op10": [
      S("Face Mill", "Face", "flat_faces"),
      S("Rough HEM", "Contour"),
      S("Pocket HEM", "Seal and port pockets", "pocket"),
      S("Contour Finish", "Profile"),
      S("Plane Finish", "Sealing faces"),
      S("Boring", "Seal gland bore", "bores"),
      *HOLES()],
   "Op20": [S("Face Mill", "Back face"), S("Contour Finish", "Back profile"), *HOLES()]},
  ["Seal gland surface finish drives the finishing stepover; use a final spring pass."])

P("plate_bracket", "Plate / bracket from plate stock", "General machined parts", ["P", "M", "N"],
  GEN,
  ["flat_faces", "pocket", "holes", "tapped_holes"],
  {"Op10": [
      S("Face Mill", "Face top", "flat_faces"),
      S("Rough HEM", "Outside contour"),
      S("Pocket HEM", "Pockets", "pocket"),
      S("Contour Finish", "Contour and pocket walls"),
      S("Plane Finish", "Pocket floors"),
      *HOLES()],
   "Op20": [S("Face Mill", "Flip and face"), S("Contour Finish", "Back features"), *HOLES()]},
  ["CIMCO order: face, contour, pocket, spot drill, drill, counterbore last."])

P("fixture_plate", "Fixture / tooling plate", "General machined parts", ["P", "K"],
  GEN,
  ["flat_faces", "holes", "tapped_holes", "bores"],
  {"Op10": [
      S("Face Mill", "Face and flatness"),
      S("Contour Finish", "Edge profile"),
      S("Centering", "Spot hole grid", "holes"),
      S("Drill", "Grid holes", "holes"),
      S("Reaming", "Dowel holes", "bores"),
      S("Tapping", "Tapped grid", "tapped_holes"),
      S("Chamfer on 3D Model", "Deburr", "holes")],
   "Op20": [S("Face Mill", "Flip and face to thickness"), S("Chamfer on 3D Model", "Deburr")]},
  ["Hole grid position matters more than speed: spot then drill with the same tool holder if possible."])

# ---- Mold and die ----------------------------------------------------------------
P("mold_cavity", "Injection mold cavity / core", "Mold and die", ["P", "H"],
  "General mold practice; hyperMILL 3D strategies (roughing, rest roughing, equidistant, profile finishing)",
  ["flat_faces", "3d_surface", "steep_walls", "pocket", "deep_pocket", "holes"],
  {"Op10": [
      S("Face Mill", "Top face and parting plane", "flat_faces"),
      S("Rough HEM", "3D optimized roughing with a large tool"),
      S("Automatic Rest Machining", "Rest material with a smaller ball or bull tool before semi-finish"),
      S("Z Level Shape Finish", "Semi-finish and finish steep faces with constant Z", "steep_walls"),
      S("3D Profile Finish Ball", "Finish shallow areas with ball nose and constant scallop", "3d_surface"),
      S("Plane Finish", "Parting plane and flat faces", "flat_faces"),
      S("Contour Finish", "Vertical walls and shutoffs"),
      *HOLES()],
   "Op20": [S("Face Mill", "Back or base plane"), S("Contour Finish", "Outline"), *HOLES()]},
  ["Keep finish stock even before the heat-treated finish; rest machine to hold the ball nose at an even load.",
   "For hardened cavities (H group) the settings swap to conventional roughing and drop plunge."])

P("die_forging_insert", "Forging die / stamping die insert", "Mold and die", ["H", "P"],
  "General die practice; hardened steel finishing",
  ["flat_faces", "3d_surface", "steep_walls", "pocket", "holes"],
  {"Op10": [
      S("Face Mill", "Top and reference faces", "flat_faces"),
      S("Rough HEM", "Soft-state roughing (swapped to conventional on H)"),
      S("Automatic Rest Machining", "Rest clear to even stock"),
      S("Z Level Shape Finish", "Steep faces", "steep_walls"),
      S("3D Profile Finish Ball", "Impression finish", "3d_surface"),
      S("Contour Finish", "Edges and shutoffs"),
      S("Plane Finish", "Flat faces", "flat_faces"),
      *HOLES(chamfer=False)]},
  ["Hardened dies: rough soft, heat treat, finish only: use the H material settings for the finish."])

# ---- Defense ---------------------------------------------------------------------
P("lower_receiver", "Lower receiver (forged aluminum)", "Defense", ["N"],
  "Elijah's sequence for the receiver; hyperMILL batching of forging-based parts",
  ["flat_faces", "pocket", "deep_pocket", "3d_surface", "holes", "reamed_holes", "tapped_holes", "deep_holes"],
  {"Op10": [
      S("Contour Finish", "Contour milling: outside profile and walls"),
      S("Pocket HEM", "Pocket milling, six pockets", "pocket", count=6),
      S("Plane Finish", "3D plane machining, four floors", count=4),
      S("Contour Finish", "Contour milling, four wall finishes", count=4),
      S("Automatic Rest Machining", "Rest machining, two passes", count=2),
      S("Swarf Curve", "Swarf finish guided by a curve"),
      S("Swarf Surface", "Swarf finish on surfaces"),
      *HOLES()],
   "Op20": [
      S("Face Mill", "Opposite side datum"),
      S("Rough HEM", "Second side form"),
      S("Contour Finish", "Profile finish"),
      S("Reaming", "Pin holes to tolerance", "reamed_holes"),
      S("Chamfer on 3D Model", "Deburr all edges")]},
  ["Forging: first operation sets datums from the forging parting line; rough both sides before finishing pin holes.",
   "Many pocket corners: finish with the smallest tool the pocket corner radius allows."],
  ordered=True)

P("upper_receiver", "Upper receiver / bolt carrier housing", "Defense", ["N", "P"],
  "General practice; ITAR work stays inside your own shop and joblist naming",
  ["flat_faces", "pocket", "bores", "holes", "tapped_holes", "deep_holes", "mill_threads"],
  {"Op10": [
      S("Face Mill", "Datum face", "flat_faces"),
      S("Rough HEM", "Form and internal cavity"),
      S("Pocket HEM", "Ejection port and cavity", "pocket"),
      S("Contour Finish", "Walls"),
      S("Plane Finish", "Cavity floors"),
      S("Helical Drilling", "Barrel bore pilot by helical interpolation", "bores"),
      S("Boring", "Finish bores to size", "bores"),
      S("Thread Milling", "Barrel nut thread", "mill_threads"),
      *HOLES()],
   "Op20": [S("Face Mill", "Opposite face"), S("Contour Finish", "Profile"), S("Chamfer on 3D Model", "Deburr")]},
  ["Bore and thread in one setup to hold concentricity between the barrel thread and the bolt-carrier bore."])

P("defense_bracket_armor", "Vehicle / armor bracket (plate steel or aluminum)", "Defense", ["P", "M", "N"],
  GEN,
  ["flat_faces", "pocket", "holes", "tapped_holes", "bores"],
  {"Op10": [
      S("Face Mill", "Face top", "flat_faces"),
      S("Rough HEM", "Outline and open pockets"),
      S("Pocket HEM", "Pockets", "pocket"),
      S("Contour Finish", "Profile finish"),
      S("Plane Finish", "Pocket floors"),
      *HOLES()],
   "Op20": [S("Face Mill", "Flip and face"), S("Contour Finish", "Back profile"), S("Chamfer on 3D Model", "Deburr")]},
  ["Armor plate (hardened): switch the material group to H and the swap rules apply."])

# ---- Weldments -----------------------------------------------------------------
P("weldment_frame", "Weldment frame (stress-relieved)", "Weldments", ["P", "M"],
  "General fabrication machining practice",
  ["flat_faces", "pocket", "bores", "large_bores", "holes", "tapped_holes", "warpage"],
  {"Op10": [
      S("Face Mill", "Skim datum pads: weld distortion means the first cut is the reference, take the minimum"),
      S("Rough HEM", "Light rough on all faces, leave 0.03-0.06 in for the second pass"),
      S("Contour Finish", "Machine mating edges"),
      S("Helical Drilling", "Large bores by helical interpolation", "large_bores"),
      *HOLES(chamfer=False)],
   "Op20": [
      S("Face Mill", "Face the opposite side after stress has relaxed"),
      S("Rough HEM", "Remove remaining scale and weld material"),
      S("Boring", "Finish bores last", "bores"),
      S("Plane Finish", "Finish mounting faces last"),
      S("Contour Finish", "Final profile"),
      S("Chamfer on 3D Model", "Deburr")]},
  ["Verify the weldment is stress relieved before machining; machining before relief moves the part.",
   "Leave finish stock on every face after rough, then finish after a rest, in the same fixturing.",
   "Locate on the weldment's most stable faces; probe for true position of machined features (the toolpaths do not probe)."])

P("weldment_machine_base", "Large machine base weldment", "Weldments", ["P"],
  "General fabrication machining practice",
  ["flat_faces", "pocket", "holes", "tapped_holes", "bores", "warpage"],
  {"Op10": [
      S("Face Mill", "Face reference pads", "flat_faces"),
      S("Rough HEM", "Pads and ways, leave finish stock"),
      S("Pocket HEM", "Pockets and cutouts", "pocket"),
      S("Plane Finish", "Linear guide pads, flat to tolerance"),
      S("Contour Finish", "Edge profiles"),
      *HOLES(chamfer=False)],
   "Op20": [
      S("Face Mill", "Opposite pads"),
      S("Plane Finish", "Finish pads after relaxation"),
      S("Boring", "Bore finishes", "bores"),
      S("Chamfer on 3D Model", "Deburr")]},
  ["Work in the same orientation the part will run: flatness is judged in its final support."])

# ---- Injection mold ---------------------------------------------------------------
P("mold_base_plate", "Mold base plate (A / B plate, pockets)", "Injection mold", ["P"],
  "General mold-base practice",
  ["flat_faces", "pocket", "deep_pocket", "holes", "deep_holes", "tapped_holes", "bores", "reamed_holes"],
  {"Op10": [
      S("Face Mill", "Parting face flat and parallel", "flat_faces"),
      S("Rough HEM", "Insert pocket roughing"),
      S("Pocket HEM", "Insert and runner pockets", "pocket"),
      S("Contour Finish", "Pocket walls to size for the insert fit"),
      S("Plane Finish", "Pocket floors"),
      S("Centering", "Spot ejector, guide pin and cooling holes", "holes"),
      S("Peck Drill", "Cooling lines and ejector pin holes: deep holes", "deep_holes"),
      S("Drill", "Bolt holes", "holes"),
      S("Reaming", "Guide pin and bushing holes", "reamed_holes"),
      S("Boring", "Leader pin bores", "bores"),
      S("Tapping", "Tapped holes", "tapped_holes"),
      S("Chamfer on 3D Model", "Deburr", "holes")],
   "Op20": [S("Face Mill", "Back face parallel"), S("Plane Finish", "Mounting face"), *HOLES()]},
  ["Pocket corner radius and depth tolerance set insert fit: finish pocket walls with a spring pass."])

P("molding_surface_block", "Molding surface block (core / cavity insert)", "Injection mold", ["P", "H"],
  "General mold practice; hyperMILL 3D strategies",
  ["flat_faces", "3d_surface", "steep_walls", "deep_pocket", "holes"],
  {"Op10": [
      S("Face Mill", "Back and parting faces", "flat_faces"),
      S("Rough HEM", "3D optimized rough with a large tool"),
      S("Automatic Rest Machining", "Rest with a smaller ball nose before semi-finish; leave even stock for polish"),
      S("Z Level Shape Finish", "Steep walls with constant Z; blend into shallow zones", "steep_walls"),
      S("3D Profile Finish Ball", "Shallow molding surfaces, small constant scallop; ball size from smallest radius", "3d_surface"),
      S("Plane Finish", "Flat shutoffs and parting faces", "flat_faces"),
      S("Contour Finish", "Vertical walls, shutoffs and draft-free zones"),
      S("Centering", "Spot ejector pin and vent holes", "holes"),
      S("Drill", "Ejector pin and water line holes", "holes"),
      S("Peck Drill", "Deep cooling holes", "deep_holes")],
   "Op20": [S("Face Mill", "Back face to size"), S("Contour Finish", "Outline to fit the pocket"), S("Chamfer on 3D Model", "Deburr")]},
  ["Leave 0.0002-0.0005 in polish stock on the molding surface depending on finish spec.",
   "Spot-check surface finish; run finishing as one uninterrupted job to avoid tool-change witness marks.",
   "Hardened (H group): use the H material settings for finish only, rough in the soft state."])

P("mold_ejector_plate", "Mold ejector / retainer plate", "Injection mold", ["P"],
  "General mold-base practice",
  ["flat_faces", "holes", "deep_holes", "tapped_holes", "reamed_holes", "pocket"],
  {"Op10": [
      S("Face Mill", "Face and thickness", "flat_faces"),
      S("Pocket HEM", "Retainer and spring pockets", "pocket"),
      S("Contour Finish", "Pocket walls"),
      S("Plane Finish", "Pocket floors"),
      S("Centering", "Spot ejector pin grid", "holes"),
      S("Drill", "Pin and bolt hole pattern", "holes"),
      S("Peck Drill", "Deep holes", "deep_holes"),
      S("Reaming", "Return pin and bushing holes", "reamed_holes"),
      S("Tapping", "Tapped holes", "tapped_holes"),
      S("Chamfer on 3D Model", "Deburr", "holes")],
   "Op20": [S("Face Mill", "Back face"), *HOLES()]},
  ["Pin hole position matters over speed: spot every hole and drill the whole pattern with one tool."])

# ---- Space propulsion and structures ----------------------------------------------
P("rocket_injector_plate", "Rocket engine injector plate", "Space propulsion", ["S", "N", "M"],
  "General practice for injector faceplates; orifice and hole-pattern machining",
  ["flat_faces", "holes", "deep_holes", "pocket", "reamed_holes", "bores", "stringy_chips", "mill_threads"],
  {"Op10": [
      S("Face Mill", "Face the injector face to flatness", "flat_faces"),
      S("Rough HEM", "Manifold and groove roughing"),
      S("Pocket HEM", "Propellant manifold pockets", "pocket"),
      S("Contour Finish", "Seal grooves and walls"),
      S("Plane Finish", "Manifold floors and seal faces"),
      S("Centering", "Spot every injector element", "holes"),
      S("Drill", "Orifice and element drilling: the pattern is the part", "holes"),
      S("Peck Drill", "Deep elements", "deep_holes"),
      S("Chip Break Drill", "Small deep holes in stainless, Inconel or copper alloys", "stringy_chips"),
      S("Reaming", "Orifices to flow tolerance", "reamed_holes"),
      S("Boring", "Interface bores", "bores"),
      S("Thread Milling", "Fastener threads", "mill_threads"),
      S("Chamfer on 3D Model", "Deburr orifice entries and edges", "holes")],
   "Op20": [
      S("Face Mill", "Opposite face"),
      S("Plane Finish", "Flange faces"),
      S("Contour Finish", "Outer profile"),
      S("Chamfer on 3D Model", "Deburr")]},
  ["Orifice diameter and surface finish set flow: measure and flow-test, do not rely on the job settings alone.",
   "Material group sets the whole plan: use S for Inconel/stainless plates, N - Copper for copper alloy faceplates."])

P("thrust_chamber_liner", "Thrust chamber / regen liner (copper alloy)", "Space propulsion", ["N"],
  "General practice for regeneratively cooled chambers",
  ["flat_faces", "deep_slot", "3d_surface", "holes", "bores"],
  {"Op10": [
      M("Turn inner contour on a lathe where available", "bores"),
      S("Rough HEM", "Cooling channel roughing: high speed, light radial engagement"),
      S("Plunge Milling", "Deep narrow channels where side milling is not possible", "deep_slot"),
      S("Contour Finish", "Channel walls"),
      S("Plane Finish", "Channel floors"),
      S("Z Level Shape Finish", "Contoured throat and chamber surfaces", "3d_surface"),
      S("Drill", "Manifold ports", "holes"),
      S("Chamfer on 3D Model", "Deburr channel edges", "holes")]},
  ["Copper is gummy and soft: sharp polished tools, flood coolant, avoid burr smearing in channels.",
   "Channel geometry is a fine 5-axis or multi-axis problem; these toolpaths give 3-axis approximations."])

P("satellite_panel_bracket", "Satellite panel / bracket (lightweighted aluminum)", "Space structures", ["N"],
  SAND + ": Wing ribs and thin-wall aluminum strategy applied to lightweighted flight hardware",
  ["flat_faces", "thin_wall", "thin_floor", "deep_pocket", "holes", "tapped_holes"],
  {"Op10": [
      S("Face Mill", "Datum face", "flat_faces"),
      S("Rough HEM", "High-speed roughing of pockets with low ae"),
      S("Pocket HEM", "Lightweighting pockets", "deep_pocket"),
      S("Plane Finish", "Webs: thin floors in a spiral from center", "thin_floor"),
      S("Contour Finish", "Walls in light overlapping passes", "thin_wall"),
      *HOLES()],
   "Op20": [S("Face Mill", "Flip datum"), S("Rough HEM", "Back lightweighting"), S("Plane Finish", "Back webs"), S("Contour Finish", "Outer profile"), S("Chamfer on 3D Model", "Deburr")]},
  ["Flight hardware is inspected first article: log every operation and keep tool data fixed after approval."])

# ---- More aerospace ---------------------------------------------------------------
P("fuselage_bulkhead", "Fuselage bulkhead / frame (7075 aluminum)", "Aluminum structure", ["N"],
  SAND + ": Aluminum components; thin wall and slicing strategy",
  ["flat_faces", "thin_wall", "thin_floor", "deep_pocket", "holes", "warpage"],
  {"Op10": [
      S("Face Mill", "Datum face of the plate", "flat_faces"),
      S("Rough HEM", "Open the large pockets at high speed, small ae"),
      S("Pocket HEM", "Pocket clearing, leave 0.02 in wall and floor stock", "deep_pocket"),
      S("Plane Finish", "Webs from the center out", "thin_floor"),
      S("Contour Finish", "Walls in two passes; semi then finish", "thin_wall"),
      *HOLES()],
   "Op20": [S("Rough HEM", "Back side pockets"), S("Plane Finish", "Back webs"), S("Contour Finish", "Outer profile"), S("Chamfer on 3D Model", "Deburr")]},
  ["Large plate parts bow when one side is removed: rough both sides before any finish pass.",
   "Vacuum or strap fixturing: check hold-down at web thickness under 0.080 in."])

P("seat_track", "Seat track / long extruded rail", "Aluminum structure", ["N"],
  GEN + "; long thin-wall extrusion practice",
  ["flat_faces", "thin_wall", "holes", "pocket", "warpage"],
  {"Op10": [
      S("Face Mill", "Datum and end faces", "flat_faces"),
      S("Rough HEM", "Slot and window roughing"),
      S("Pocket HEM", "Window pockets", "pocket"),
      S("Contour Finish", "Window walls and slot flanks", "thin_wall"),
      *HOLES()],
   "Op20": [S("Contour Finish", "Back features"), S("Chamfer on 3D Model", "Deburr")]},
  ["Machine long rails in sections from the clamped end outward to keep straightness."])

P("clevis_lug_fitting", "Clevis / lug fitting (titanium or steel)", "Titanium structure", ["S", "P"],
  SAND + ": Main fittings; Thrust fittings",
  ["flat_faces", "boss", "bores", "holes", "deep_slot"],
  {"Op10": [
      S("Face Mill", "Datum faces", "flat_faces"),
      S("Rough HEM", "Clevis form and lug thickness"),
      S("Plunge Milling", "Deep clevis slot when overhang is long", "deep_slot"),
      S("Contour Finish", "Lug faces and slot walls"),
      S("Plane Finish", "Lug faces flat and parallel"),
      S("Helical Drilling", "Lug bore roughing by helical interpolation", "bores"),
      S("Boring", "Lug bore to size in one setup with both lugs", "bores"),
      *HOLES()],
   "Op20": [S("Rough HEM", "Opposite side form"), S("Contour Finish", "Profile"), S("Chamfer on 3D Model", "Deburr")]},
  ["Bore both lugs in one setup for alignment; leave bearing seat finish for the last cut."])

P("aero_actuator_housing", "Hydraulic actuator housing (aerospace)", "Titanium and high alloy steel", ["S", "P", "M"],
  SAND + ": Main fittings (deep hole drilling); general hydraulic housing practice",
  ["flat_faces", "pocket", "deep_holes", "cross_holes", "bores", "tapped_holes", "reamed_holes", "holes"],
  {"Op10": [
      S("Face Mill", "Mounting face", "flat_faces"),
      S("Rough HEM", "External form"),
      S("Pocket HEM", "Port pockets", "pocket"),
      S("Contour Finish", "Profile"),
      S("Plane Finish", "Port faces"),
      S("Centering", "Spot ports", "holes"),
      S("Peck Drill", "Long cylinder and cross passages", "deep_holes"),
      S("Boring", "Cylinder bore finish", "bores"),
      S("Reaming", "Valve bores", "reamed_holes"),
      S("Thread Milling", "Port threads in difficult material", "tapped_holes"),
      S("Chamfer on 3D Model", "Deburr cross-hole intersections", "cross_holes")],
   "Op20": [S("Face Mill", "Opposite side"), *HOLES()]},
  ["Cross-hole intersections: drill and deburr in that order, flush the passages after machining."])

P("compressor_vane_ring", "Compressor vane ring / stator case", "Engine casing", ["S"],
  SAND + ": Fan casings; Combustion casing",
  ["turned", "boss", "bores", "holes", "3d_surface", "pocket"],
  {"Op10": [
      M("Turn ID/OD and flanges first", "turned"),
      S("Rough HEM", "Vane windows by high-feed side milling"),
      S("Pocket HEM", "Window pockets", "pocket"),
      S("Contour Finish", "Window walls"),
      S("Boring", "Rabbet bores", "bores"),
      S("Drill", "Flange bolt holes", "holes"),
      S("Chamfer on 3D Model", "Deburr", "holes")]},
  ["Windows in a rotating pattern: keep the same tool and data for all windows."])

P("turbine_blade_dovetail", "Turbine blade root / dovetail slot", "Engine rotating", ["S"],
  SAND + ": Fan discs (tulip slot milling replaces broaching)",
  ["deep_slot", "3d_surface"],
  {"Op10": [
      S("Rough HEM", "Rough the slot with a trochoidal pass, small ae"),
      S("Contour Finish", "Slot profile with a form tool or ball nose in multiple passes", "deep_slot"),
      S("Z Level Shape Finish", "Root form", "3d_surface"),
      M("Dovetail form needs an engineered form cutter; verify profile and gauge fit")]},
  ["Dovetail geometry is tolerance critical: inspect the first slot before running the pattern."])

P("aero_gearbox_housing", "Accessory gearbox housing (cast magnesium or aluminum)", "Engine casing", ["N"],
  GEN,
  ["flat_faces", "pocket", "bores", "large_bores", "holes", "tapped_holes", "mill_threads"],
  {"Op10": [
      S("Face Mill", "Parting face", "flat_faces"),
      S("Rough HEM", "Cavity and bosses"),
      S("Pocket HEM", "Gear cavities", "pocket"),
      S("Helical Drilling", "Bearing bores roughed", "large_bores"),
      S("Boring", "Bearing bores to size", "bores"),
      S("Plane Finish", "Bearing shoulders"),
      *HOLES()],
   "Op20": [S("Face Mill", "Mounting face"), S("Contour Finish", "Profile"), *HOLES()]},
  ["Magnesium: chips ignite. Use coolant, never dry, and keep fines swept."])

P("cold_plate", "Cold plate / liquid heat exchanger plate", "Aluminum structure", ["N"],
  GEN,
  ["flat_faces", "pocket", "thin_wall", "holes", "tapped_holes"],
  {"Op10": [
      S("Face Mill", "Seal face", "flat_faces"),
      S("Rough HEM", "Fluid channels"),
      S("Pocket HEM", "Channel pockets", "pocket"),
      S("Contour Finish", "Channel walls", "thin_wall"),
      S("Plane Finish", "Channel floors and seal land"),
      *HOLES()],
   "Op20": [S("Face Mill", "Back face"), S("Plane Finish", "Mounting face"), S("Chamfer on 3D Model", "Deburr")]},
  ["Seal land flatness is the tightest tolerance: finish it last in the setup with a sharp tool."])

# ---- More space -----------------------------------------------------------------------
P("rocket_nozzle_extension", "Nozzle extension / bell (nickel or titanium)", "Space propulsion", ["S"],
  "General practice for propulsion hardware",
  ["turned", "3d_surface", "flat_faces", "holes"],
  {"Op10": [
      M("Turn the bell contour and flanges", "turned"),
      S("Z Level Shape Finish", "Contoured wall where milled", "3d_surface"),
      S("Contour Finish", "Flange edges"),
      S("Drill", "Flange bolt circle", "holes"),
      S("Chamfer on 3D Model", "Deburr", "holes")]},
  ["Thin large-diameter shells: support the shell during machining; milling content is small."])

P("turbopump_housing", "Turbopump housing / volute", "Space propulsion", ["S"],
  "General practice for propulsion hardware",
  ["flat_faces", "3d_surface", "bores", "large_bores", "holes", "mill_threads"],
  {"Op10": [
      S("Face Mill", "Flange faces", "flat_faces"),
      S("Rough HEM", "Volute roughing with low ae"),
      S("Automatic Rest Machining", "Rest in volute corners"),
      S("Z Level Shape Finish", "Volute walls", "3d_surface"),
      S("3D Profile Finish Ball", "Volute floor", "3d_surface"),
      S("Helical Drilling", "Shaft bore rough", "large_bores"),
      S("Boring", "Seal and bearing bores", "bores"),
      S("Thread Milling", "Threads in nickel alloy", "mill_threads"),
      S("Drill", "Bolt holes", "holes"),
      S("Chamfer on 3D Model", "Deburr", "holes")]},
  ["Flow surface finish affects performance: finish the volute in one uninterrupted job."])

P("satellite_housing", "Satellite electronics housing / box", "Space structures", ["N"],
  SAND + ": thin-wall aluminum strategy",
  ["flat_faces", "thin_wall", "thin_floor", "pocket", "holes", "tapped_holes"],
  {"Op10": [
      S("Face Mill", "Seal flange", "flat_faces"),
      S("Rough HEM", "Cavity roughing"),
      S("Pocket HEM", "Component pockets", "pocket"),
      S("Contour Finish", "Walls to 0.030 in or thinner in light passes", "thin_wall"),
      S("Plane Finish", "Floors", "thin_floor"),
      *HOLES()],
   "Op20": [S("Face Mill", "Back face"), S("Rough HEM", "Back lightweighting"), S("Contour Finish", "Profile"), S("Chamfer on 3D Model", "Deburr")]},
  ["Flight hardware: clean machine, no cutting fluid residue in the cavity before release."])

P("rf_waveguide", "RF waveguide / antenna feed (aluminum or copper)", "Space structures", ["N"],
  "General RF hardware practice",
  ["pocket", "thin_wall", "holes", "tapped_holes", "bores"],
  {"Op10": [
      S("Rough HEM", "Channel roughing"),
      S("Pocket HEM", "Channel pockets", "pocket"),
      S("Contour Finish", "Channel walls to tolerance, final pass sharp", "thin_wall"),
      S("Plane Finish", "Channel floors and flange faces"),
      S("Boring", "Probe and iris bores", "bores"),
      *HOLES()]},
  ["Channel dimensions set RF performance: finish walls and floor with the same tool, constant stock."])

P("gimbal_mount", "Gimbal / pointing mount (titanium)", "Space structures", ["S"],
  SAND + ": titanium structure practice",
  ["flat_faces", "pocket", "thin_wall", "bores", "holes"],
  {"Op10": [
      S("Face Mill", "Datum", "flat_faces"),
      S("Rough HEM", "Lightweighting rough"),
      S("Pocket HEM", "Pockets", "pocket"),
      S("Contour Finish", "Ribs and walls", "thin_wall"),
      S("Boring", "Bearing bores", "bores"),
      *HOLES()],
   "Op20": [S("Rough HEM", "Back side"), S("Contour Finish", "Profile"), S("Chamfer on 3D Model", "Deburr")]},
  ["Bearing bore coaxiality needs both bores finished in one setup."])

# ---- More defense -------------------------------------------------------------------------
P("suppressor_baffle", "Suppressor baffle / blast chamber (titanium, stainless or Inconel)", "Defense", ["S", "M"],
  "General practice",
  ["turned", "holes", "3d_surface", "bores"],
  {"Op10": [
      M("Turn baffle cones and bore on a lathe", "turned"),
      S("Contour Finish", "Port profiles", "3d_surface"),
      S("Drill", "Gas ports", "holes"),
      S("Boring", "Bullet path bore", "bores"),
      S("Chamfer on 3D Model", "Deburr ports", "holes")]},
  ["Mostly turned parts: milling covers cross ports and flats."])

P("optic_mount", "Optic mount / Picatinny rail section", "Defense", ["N", "P"],
  "General practice",
  ["flat_faces", "pocket", "holes", "tapped_holes"],
  {"Op10": [
      S("Face Mill", "Base datum", "flat_faces"),
      S("Rough HEM", "Rail and slot form"),
      S("Contour Finish", "Rail flanks to gauge"),
      S("Plane Finish", "Seat faces"),
      *HOLES()],
   "Op20": [S("Contour Finish", "Back features"), S("Chamfer on 3D Model", "Deburr")]},
  ["Rail slot width and pitch are gauged: finish all slots with one tool."])

P("turret_ring_housing", "Turret ring / vehicle housing (steel)", "Defense", ["P", "H"],
  GEN,
  ["flat_faces", "large_bores", "bores", "holes", "tapped_holes"],
  {"Op10": [
      S("Face Mill", "Face"),
      S("Rough HEM", "Form"),
      S("Helical Drilling", "Large center bore", "large_bores"),
      S("Boring", "Bearing bore", "bores"),
      S("Plane Finish", "Bearing seat"),
      *HOLES()],
   "Op20": [S("Face Mill", "Back face"), S("Contour Finish", "Profile"), *HOLES()]},
  ["Heavy parts: verify weight and fixturing; use rough pass then a rest before finishing bores."])

# ---- Medical ----------------------------------------------------------------------------------
P("hip_stem", "Hip stem (titanium)", "Medical", ["S", "M"],
  "General orthopedic implant practice",
  ["3d_surface", "flat_faces", "holes"],
  {"Op10": [
      S("Rough HEM", "Rough the neck and stem form with low ae"),
      S("Automatic Rest Machining", "Rest clear the neck transition"),
      S("Z Level Shape Finish", "Steep faces of the neck and shoulder", "3d_surface"),
      S("3D Profile Finish Ball", "Stem surface with small constant scallop", "3d_surface"),
      S("Contour Finish", "Edges and flats"),
      S("Chamfer on 3D Model", "Edge break all sharp corners")],
   "Op20": [S("Rough HEM", "Second side"), S("3D Profile Finish Ball", "Blend surfaces", "3d_surface"), S("Chamfer on 3D Model", "Deburr")]},
  ["Final surface is polished or blasted: leave polish stock per drawing.",
   "No tool marks or witness lines on bearing surfaces; run finishing as a single job."])

P("knee_femoral", "Knee femoral component (cobalt chrome or titanium)", "Medical", ["S"],
  "General orthopedic implant practice",
  ["3d_surface", "steep_walls"],
  {"Op10": [
      S("Rough HEM", "Condyle roughing, high speed, low ae"),
      S("Automatic Rest Machining", "Rest clear condyle blends"),
      S("Z Level Shape Finish", "Steep articulating faces", "steep_walls"),
      S("3D Profile Finish Ball", "Articulating surface with smallest scallop the finish allows", "3d_surface"),
      S("Chamfer on 3D Model", "Edge break")]},
  ["Articulating surface is polished: spec the leave stock before polish.",
   "Cobalt chrome work hardens: constant chip load and no dwelling."])

P("bone_plate", "Bone plate (titanium or stainless)", "Medical", ["S", "M"],
  "General orthopedic practice",
  ["flat_faces", "holes", "3d_surface"],
  {"Op10": [
      S("Face Mill", "Face stock", "flat_faces"),
      S("Rough HEM", "Plate outline"),
      S("Contour Finish", "Outline to size"),
      S("Z Level Shape Finish", "Countersinks and ramps", "3d_surface"),
      S("Centering", "Spot screw holes", "holes"),
      S("Drill", "Screw holes", "holes"),
      S("Chamfer on 3D Model", "Countersinks and edge break", "holes")],
   "Op20": [S("Face Mill", "Contoured back face"), S("3D Profile Finish Ball", "Anatomical contour", "3d_surface")]},
  ["Hole pattern positions are inspected on every plate: control tool wear on the drill."])

P("spinal_cage", "Spinal interbody cage (titanium or PEEK)", "Medical", ["S"],
  "General orthopedic practice",
  ["pocket", "3d_surface", "holes"],
  {"Op10": [
      S("Rough HEM", "Outline and window"),
      S("Pocket HEM", "Graft window", "pocket"),
      S("Contour Finish", "Window walls and teeth flanks"),
      S("3D Profile Finish Ball", "Contoured faces", "3d_surface"),
      S("Chamfer on 3D Model", "Deburr teeth"),
      S("Drill", "Instrument hole", "holes")]},
  ["Small features: use the smallest rigid tools; PEEK needs sharp polished tools and no coolant additives."])

P("surgical_instrument", "Surgical instrument handle / body (stainless)", "Medical", ["M"],
  "General instrument practice",
  ["flat_faces", "pocket", "holes", "tapped_holes", "mill_threads"],
  {"Op10": [
      S("Face Mill", "Face", "flat_faces"),
      S("Rough HEM", "Profile"),
      S("Contour Finish", "Profile finish"),
      S("Plane Finish", "Flats"),
      *HOLES()],
   "Op20": [S("Contour Finish", "Back features"), S("Chamfer on 3D Model", "Deburr")]},
  ["Passivate after machining; avoid carbon-steel contamination from tools and fixtures."])

P("dental_abutment", "Dental implant abutment / small titanium part", "Medical", ["S"],
  "General dental practice",
  ["holes", "tapped_holes", "3d_surface"],
  {"Op10": [
      S("Rough HEM", "Outer form"),
      S("Z Level Shape Finish", "Emergence profile", "3d_surface"),
      S("Centering", "Spot screw hole", "holes"),
      S("Drill", "Screw channel", "holes"),
      S("Thread Milling", "Micro thread", "tapped_holes"),
      S("Chamfer on 3D Model", "Deburr")]},
  ["Micro tools: speeds and feeds from the tool database may exceed small-tool limits."])

P("orthopedic_trial", "Orthopedic trial / instrument tray (aluminum or stainless)", "Medical", ["N", "M"],
  "General practice",
  ["pocket", "flat_faces", "holes", "3d_surface"],
  {"Op10": [
      S("Face Mill", "Face", "flat_faces"),
      S("Rough HEM", "Outline"),
      S("Pocket HEM", "Pockets", "pocket"),
      S("Contour Finish", "Walls"),
      S("3D Profile Finish Ball", "Contoured trial surface", "3d_surface"),
      *HOLES()]},
  ["Laser marking and anodizing follow: leave marking area flat and clean."])

# ---- Automotive and motorsport -----------------------------------------------------------------
P("cylinder_head", "Cylinder head", "Automotive", ["N", "K"],
  GEN + "; high-volume prismatic practice",
  ["flat_faces", "pocket", "bores", "holes", "deep_holes", "tapped_holes", "3d_surface"],
  {"Op10": [
      S("Face Mill", "Deck face to flatness", "flat_faces"),
      S("Rough HEM", "Combustion chambers and pockets", "pocket"),
      S("Z Level Shape Finish", "Chamber walls", "3d_surface"),
      S("Plane Finish", "Deck face final pass"),
      S("Centering", "Spot", "holes"),
      S("Drill", "Bolt and coolant holes", "holes"),
      S("Peck Drill", "Oil and water galleries", "deep_holes"),
      S("Boring", "Valve guide and seat bores", "bores"),
      S("Tapping", "Spark plug and bolt threads", "tapped_holes"),
      S("Chamfer on 3D Model", "Deburr", "holes")],
   "Op20": [S("Face Mill", "Intake and exhaust faces"), *HOLES()],
   "Op30": [S("Face Mill", "Cam cover face"), *HOLES()]},
  ["Deck face flatness is tight: final pass with a wiper or fresh tool.",
   "Cast aluminum is abrasive: use PCD where cycle volume justifies."])

P("engine_block", "Engine block (cast iron or aluminum)", "Automotive", ["K", "N"],
  GEN,
  ["flat_faces", "pocket", "large_bores", "bores", "holes", "deep_holes", "tapped_holes"],
  {"Op10": [
      S("Face Mill", "Deck face", "flat_faces"),
      S("Rough HEM", "Pockets and bosses"),
      S("Helical Drilling", "Cylinder bore rough by helical interpolation", "large_bores"),
      S("Boring", "Cylinder bore semi-finish; honing follows", "bores"),
      S("Plane Finish", "Deck face"),
      S("Centering", "Spot", "holes"),
      S("Drill", "Head bolt and coolant holes", "holes"),
      S("Peck Drill", "Oil galleries", "deep_holes"),
      S("Tapping", "Bolt threads", "tapped_holes")],
   "Op20": [S("Face Mill", "Pan rail"), S("Boring", "Main bearing bores", "bores"), *HOLES()]},
  ["Cylinder bores and main bores are finished after the deck and pan rail are cut: bores last.",
   "Gray iron: dry machine or air blast."])

P("transmission_case", "Transmission case (cast aluminum)", "Automotive", ["N"],
  GEN,
  ["flat_faces", "pocket", "large_bores", "bores", "holes", "tapped_holes", "mill_threads"],
  {"Op10": [
      S("Face Mill", "Bell housing face", "flat_faces"),
      S("Rough HEM", "Cavity"),
      S("Pocket HEM", "Gear cavities", "pocket"),
      S("Helical Drilling", "Bearing bores rough", "large_bores"),
      S("Boring", "Bearing bores finish", "bores"),
      S("Plane Finish", "Joint face"),
      *HOLES()],
   "Op20": [S("Face Mill", "Pan face"), S("Contour Finish", "Profile"), *HOLES()]},
  ["Bore pattern relative to the bell housing face must hold: bore from the same datum."])

P("brake_caliper", "Brake caliper body", "Automotive", ["N", "K"],
  GEN,
  ["flat_faces", "pocket", "large_bores", "bores", "holes", "tapped_holes", "3d_surface"],
  {"Op10": [
      S("Face Mill", "Mounting face", "flat_faces"),
      S("Rough HEM", "Bridge and pocket"),
      S("Contour Finish", "Piston face outline"),
      S("Helical Drilling", "Piston bores rough", "large_bores"),
      S("Boring", "Piston bores to finish size", "bores"),
      S("Z Level Shape Finish", "Contoured bridge surfaces", "3d_surface"),
      *HOLES()],
   "Op20": [S("Face Mill", "Opposite mounting face"), S("Contour Finish", "Profile"), *HOLES()]},
  ["Piston bores need surface finish for seals: final pass sharp tool, controlled feed."])

P("turbo_housing", "Turbocharger housing / volute (cast iron or stainless)", "Automotive", ["K", "M"],
  GEN,
  ["flat_faces", "3d_surface", "bores", "holes"],
  {"Op10": [
      S("Face Mill", "Flange face", "flat_faces"),
      S("Rough HEM", "Volute"),
      S("Z Level Shape Finish", "Volute walls", "3d_surface"),
      S("3D Profile Finish Ball", "Volute floor", "3d_surface"),
      S("Boring", "Turbine bore", "bores"),
      *HOLES()]},
  ["Hot-side castings are abrasive and hard: rest machine before finishing."])

P("wheel_hub_upright", "Wheel hub / suspension upright", "Automotive", ["N", "P"],
  GEN,
  ["flat_faces", "pocket", "3d_surface", "large_bores", "bores", "holes", "tapped_holes"],
  {"Op10": [
      S("Face Mill", "Datum", "flat_faces"),
      S("Rough HEM", "Form and pockets"),
      S("Pocket HEM", "Lightweighting pockets", "pocket"),
      S("Z Level Shape Finish", "Organic webs", "3d_surface"),
      S("Contour Finish", "Walls"),
      S("Helical Drilling", "Bearing bore rough", "large_bores"),
      S("Boring", "Bearing bore", "bores"),
      *HOLES()],
   "Op20": [S("Face Mill", "Opposite side"), S("Rough HEM", "Back pockets"), S("Contour Finish", "Profile"), *HOLES()]},
  ["Motorsport: billet 7075 or 6061 uprights are lightweighted: keep wall thickness against drawing."])

P("control_arm", "Suspension control arm / link", "Automotive", ["N", "P"],
  GEN,
  ["flat_faces", "pocket", "bores", "holes", "thin_wall"],
  {"Op10": [
      S("Face Mill", "Datum", "flat_faces"),
      S("Rough HEM", "Arm form"),
      S("Pocket HEM", "Lightweighting", "pocket"),
      S("Contour Finish", "Walls", "thin_wall"),
      S("Boring", "Bushing bores in one setup", "bores"),
      *HOLES()],
   "Op20": [S("Rough HEM", "Back side"), S("Contour Finish", "Profile"), S("Chamfer on 3D Model", "Deburr")]},
  ["Bushing bore spacing is the critical dimension: bore both in the same setup."])

P("intake_manifold", "Intake manifold (aluminum)", "Automotive", ["N"],
  GEN,
  ["flat_faces", "3d_surface", "pocket", "holes", "tapped_holes"],
  {"Op10": [
      S("Face Mill", "Port faces", "flat_faces"),
      S("Rough HEM", "Plenum and runners"),
      S("Z Level Shape Finish", "Runner walls", "3d_surface"),
      S("3D Profile Finish Ball", "Runner floors", "3d_surface"),
      S("Plane Finish", "Gasket faces"),
      *HOLES()],
   "Op20": [S("Face Mill", "Throttle body face"), *HOLES()]},
  ["Flow surfaces are often left as cast; machine only gasket faces and bores unless the drawing says otherwise."])

P("piston_forged", "Piston crown / forged piston (aluminum)", "Automotive", ["N"],
  GEN,
  ["turned", "pocket", "3d_surface", "holes", "bores"],
  {"Op10": [
      M("Turn ring grooves and skirt on a lathe", "turned"),
      S("Rough HEM", "Valve reliefs and dome"),
      S("3D Profile Finish Ball", "Dome contour", "3d_surface"),
      S("Drill", "Oil holes", "holes"),
      S("Boring", "Wrist pin bore", "bores")]},
  ["Wrist pin bore position relative to the crown is critical: bore after the crown is finished."])

# ---- Oil and gas, energy -----------------------------------------------------------------------
P("frac_fluid_end", "Frac pump fluid end (alloy steel or PH stainless)", "Oil gas and energy", ["P", "M"],
  "General high-pressure pump practice",
  ["flat_faces", "pocket", "large_bores", "bores", "deep_holes", "cross_holes", "holes", "tapped_holes"],
  {"Op10": [
      S("Face Mill", "Datum face", "flat_faces"),
      S("Rough HEM", "External form"),
      S("Helical Drilling", "Plunger and valve bores rough", "large_bores"),
      S("Boring", "Plunger and valve seats finish", "bores"),
      S("Peck Drill", "Discharge and suction passages", "deep_holes"),
      S("Thread Milling", "Large studs and ports", "tapped_holes"),
      S("Chamfer on 3D Model", "Deburr cross bores and passages", "cross_holes")],
   "Op20": [S("Face Mill", "Opposite side"), *HOLES()],
   "Op30": [S("Face Mill", "Third side"), *HOLES()]},
  ["Cross-bore intersections are fatigue critical: radius or deburr per drawing.",
   "Large forgings: rough all faces before finishing bores."])

P("wellhead_body", "Wellhead / Christmas tree body", "Oil gas and energy", ["P", "M"],
  "General API equipment practice",
  ["flat_faces", "large_bores", "bores", "holes", "tapped_holes", "turned"],
  {"Op10": [
      M("Turn bore and flange faces on a lathe or vertical turning lathe", "turned"),
      S("Face Mill", "Flange faces", "flat_faces"),
      S("Rough HEM", "Outlets and bosses"),
      S("Helical Drilling", "Side outlets rough", "large_bores"),
      S("Boring", "Side outlet bores", "bores"),
      S("Thread Milling", "Studs", "tapped_holes"),
      *HOLES()]},
  ["API flange ring grooves: finish with a sharp tool in a single pass for sealing surface finish."])

P("choke_valve_body", "Choke / control valve body (duplex or super duplex)", "Oil gas and energy", ["M"],
  "General practice",
  ["flat_faces", "pocket", "bores", "holes", "cross_holes", "tapped_holes", "mill_threads"],
  {"Op10": [
      S("Face Mill", "Flange face", "flat_faces"),
      S("Rough HEM", "Body form"),
      S("Pocket HEM", "Internal cavities", "pocket"),
      S("Boring", "Seat bores", "bores"),
      S("Thread Milling", "Gland and port threads", "mill_threads"),
      *HOLES()],
   "Op20": [S("Face Mill", "Opposite flange"), *HOLES()]},
  ["Duplex work hardens: constant chip load, rigid tooling, flood coolant."])

P("api_flange", "API / ANSI flange (steel or stainless)", "Oil gas and energy", ["P", "M"],
  GEN,
  ["flat_faces", "bores", "holes", "turned"],
  {"Op10": [
      M("Turn bore, OD, face and ring groove on a lathe", "turned"),
      S("Face Mill", "Face", "flat_faces"),
      S("Contour Finish", "OD profile"),
      S("Centering", "Spot bolt circle", "holes"),
      S("Drill", "Bolt holes", "holes"),
      S("Chamfer on 3D Model", "Deburr", "holes")]},
  ["Bolt circle on a rotary or in a drill cycle: spot each hole first."])

P("pump_casing", "Centrifugal pump casing (cast stainless or iron)", "Oil gas and energy", ["M", "K"],
  GEN,
  ["flat_faces", "3d_surface", "bores", "large_bores", "holes"],
  {"Op10": [
      S("Face Mill", "Suction and discharge faces", "flat_faces"),
      S("Rough HEM", "Volute"),
      S("Z Level Shape Finish", "Volute walls", "3d_surface"),
      S("Helical Drilling", "Shaft bore rough", "large_bores"),
      S("Boring", "Shaft and wear ring bores", "bores"),
      *HOLES()],
   "Op20": [S("Face Mill", "Opposite faces"), *HOLES()]},
  ["Cast stainless is gummy: rigid tooling, positive geometry."])

P("downhole_tool_housing", "Downhole tool housing (alloy steel or Inconel)", "Oil gas and energy", ["P", "S"],
  "General practice",
  ["turned", "pocket", "deep_holes", "bores", "holes", "mill_threads"],
  {"Op10": [
      M("Turn OD, ID and threads on a lathe", "turned"),
      S("Rough HEM", "Flats and pockets"),
      S("Pocket HEM", "Sensor pockets", "pocket"),
      S("Contour Finish", "Pocket walls"),
      S("Peck Drill", "Long cross passages", "deep_holes"),
      S("Thread Milling", "Port threads", "mill_threads"),
      S("Chamfer on 3D Model", "Deburr", "holes")]},
  ["Long slender parts: support with a steady rest or tailstock; milling is secondary."])

# ---- Semiconductor and electronics ---------------------------------------------------------------
P("vacuum_chamber", "Vacuum chamber / process chamber (6061 or stainless)", "Semiconductor and electronics", ["N", "M"],
  "General semiconductor equipment practice",
  ["flat_faces", "pocket", "large_bores", "holes", "tapped_holes", "bores"],
  {"Op10": [
      S("Face Mill", "Flange face", "flat_faces"),
      S("Rough HEM", "Chamber cavity"),
      S("Pocket HEM", "Cavity pockets", "pocket"),
      S("Contour Finish", "Walls"),
      S("Plane Finish", "Seal faces, final pass sharp, no scratches"),
      S("Helical Drilling", "Port bores", "large_bores"),
      S("Boring", "Port bore finish", "bores"),
      *HOLES()],
   "Op20": [S("Face Mill", "Lid face"), S("Plane Finish", "Seal face"), *HOLES()]},
  ["Seal faces need low Ra: leave stock for a light final pass; clean with approved coolant only."])

P("wafer_chuck", "Wafer chuck / vacuum chuck plate", "Semiconductor and electronics", ["N"],
  "General semiconductor equipment practice",
  ["flat_faces", "pocket", "holes", "3d_surface"],
  {"Op10": [
      S("Face Mill", "Datum face", "flat_faces"),
      S("Rough HEM", "Back-side channels"),
      S("Pocket HEM", "Vacuum channels", "pocket"),
      S("Plane Finish", "Wafer seat to flatness, final pass light"),
      S("Contour Finish", "Edge profile"),
      S("Centering", "Vacuum ports", "holes"),
      S("Drill", "Vacuum holes", "holes")]},
  ["Flatness within 0.0005 in: stress relieve between rough and finish."])

P("gas_manifold", "Gas distribution manifold (316 stainless)", "Semiconductor and electronics", ["M"],
  "General semiconductor equipment practice",
  ["flat_faces", "pocket", "holes", "deep_holes", "cross_holes", "bores", "tapped_holes"],
  {"Op10": [
      S("Face Mill", "Top face", "flat_faces"),
      S("Rough HEM", "Contour"),
      S("Pocket HEM", "Seal pockets", "pocket"),
      S("Plane Finish", "Seal faces"),
      S("Centering", "Spot ports", "holes"),
      S("Peck Drill", "Gas passages", "deep_holes"),
      S("Boring", "Port bores", "bores"),
      S("Tapping", "Port threads", "tapped_holes"),
      S("Chamfer on 3D Model", "Deburr cross passages", "cross_holes")],
   "Op20": [S("Face Mill", "Second face"), *HOLES()],
   "Op30": [S("Face Mill", "Third face"), *HOLES()]},
  ["Passages must be burr free: deburr cross intersections and flush."])

P("showerhead_plate", "Showerhead / gas distribution plate (many small holes)", "Semiconductor and electronics", ["N", "M"],
  "General practice",
  ["flat_faces", "holes", "pocket", "stringy_chips"],
  {"Op10": [
      S("Face Mill", "Face to flatness", "flat_faces"),
      S("Rough HEM", "Plenum pocket"),
      S("Plane Finish", "Plenum floor"),
      S("Centering", "Spot every hole position", "holes"),
      S("Drill", "Small holes in a controlled pattern", "holes"),
      S("Chip Break Drill", "Deep small holes in stainless", "stringy_chips"),
      S("Chamfer on 3D Model", "Deburr hole exits", "holes")]},
  ["Thousands of holes: tool life and breakage decide run time: log hole count per drill."])

# ---- Tooling and fixtures --------------------------------------------------------------------------------
P("soft_jaws", "Soft jaws / workholding jaws", "Tooling and fixtures", ["N", "P"],
  GEN,
  ["flat_faces", "pocket", "holes", "tapped_holes"],
  {"Op10": [
      S("Face Mill", "Jaw face", "flat_faces"),
      S("Rough HEM", "Part pocket"),
      S("Pocket HEM", "Pocket", "pocket"),
      S("Contour Finish", "Pocket to size, light spring pass"),
      S("Plane Finish", "Seat"),
      *HOLES()]},
  ["Cut the pocket at the clamp pressure the part will see."])

P("tombstone_fixture", "Tombstone / fixture block", "Tooling and fixtures", ["P", "N"],
  GEN,
  ["flat_faces", "holes", "tapped_holes", "reamed_holes", "bores"],
  {"Op10": [
      S("Face Mill", "Top datum", "flat_faces"),
      S("Contour Finish", "Edge profile"),
      S("Centering", "Spot grid", "holes"),
      S("Drill", "Tapped hole grid and clamp holes", "holes"),
      S("Reaming", "Dowel holes", "reamed_holes"),
      S("Tapping", "Tapped grid", "tapped_holes"),
      S("Chamfer on 3D Model", "Deburr", "holes")],
   "Op20": [S("Face Mill", "Second face"), *HOLES()],
   "Op30": [S("Face Mill", "Third face"), *HOLES()]},
  ["Hole grid: drill and tap each face in one setup; verify face-to-face squareness."])

P("progressive_die_plate", "Progressive die plate / stripper (tool steel)", "Tooling and fixtures", ["P", "H"],
  "General die-making practice",
  ["flat_faces", "pocket", "holes", "reamed_holes", "bores", "tapped_holes"],
  {"Op10": [
      S("Face Mill", "Face and thickness", "flat_faces"),
      S("Rough HEM", "Window roughing, leave 0.010-0.020 in"),
      S("Pocket HEM", "Pockets", "pocket"),
      S("Contour Finish", "Windows and profiles"),
      S("Centering", "Spot", "holes"),
      S("Drill", "Screw and dowel holes", "holes"),
      S("Reaming", "Dowel holes", "reamed_holes"),
      S("Tapping", "Tapped holes", "tapped_holes")],
   "Op20": [S("Face Mill", "Back face"), S("Plane Finish", "Seat faces"), S("Chamfer on 3D Model", "Deburr")]},
  ["Heat treat between rough and finish: leave stock; windows are finished by wire EDM or hard milling."])

P("punch_die_insert", "Punch / die insert (hardened)", "Tooling and fixtures", ["H"],
  "General die practice",
  ["flat_faces", "3d_surface", "steep_walls", "holes"],
  {"Op10": [
      S("Face Mill", "Reference faces", "flat_faces"),
      S("Rough HEM", "Hard roughing (swapped to conventional for H groups)"),
      S("Z Level Shape Finish", "Steep faces", "steep_walls"),
      S("3D Profile Finish Ball", "Form surfaces", "3d_surface"),
      S("Contour Finish", "Walls"),
      S("Drill", "Screw holes", "holes")]},
  ["Hard milling: shallow ap, high speed, short tools, rigid holders."])

P("inspection_fixture", "Inspection / CMM fixture plate", "Tooling and fixtures", ["N"],
  GEN,
  ["flat_faces", "holes", "tapped_holes", "pocket", "3d_surface"],
  {"Op10": [
      S("Face Mill", "Datum face", "flat_faces"),
      S("Rough HEM", "Nest roughing"),
      S("Pocket HEM", "Nest pockets", "pocket"),
      S("3D Profile Finish Ball", "Nest contour to part shape", "3d_surface"),
      S("Contour Finish", "Edge and locators"),
      *HOLES()]},
  ["Locator surfaces are references: finish with a fresh tool and measure."])

# ---- More injection mold -----------------------------------------------------------------------------------
P("mold_slide_lifter", "Mold slide / lifter / core insert (hardened)", "Injection mold", ["P", "H"],
  "General mold practice",
  ["flat_faces", "3d_surface", "steep_walls", "holes"],
  {"Op10": [
      S("Face Mill", "Back faces", "flat_faces"),
      S("Rough HEM", "Form"),
      S("Z Level Shape Finish", "Steep walls and shutoffs", "steep_walls"),
      S("3D Profile Finish Ball", "Feature surfaces", "3d_surface"),
      S("Contour Finish", "Guide faces"),
      *HOLES(chamfer=False)]},
  ["Wear surfaces and slide faces carry fit tolerances: spring pass and measure."])

P("hot_runner_manifold", "Hot runner manifold (tool steel)", "Injection mold", ["P"],
  "General practice",
  ["flat_faces", "pocket", "deep_holes", "cross_holes", "bores", "tapped_holes", "holes"],
  {"Op10": [
      S("Face Mill", "Datum", "flat_faces"),
      S("Rough HEM", "Heater channels"),
      S("Pocket HEM", "Pockets", "pocket"),
      S("Centering", "Spot", "holes"),
      S("Peck Drill", "Melt channels, long deep holes", "deep_holes"),
      S("Boring", "Nozzle seats", "bores"),
      S("Tapping", "Plug and port threads", "tapped_holes"),
      S("Chamfer on 3D Model", "Deburr cross channels so no flash traps melt", "cross_holes")],
   "Op20": [S("Face Mill", "Second face"), *HOLES()]},
  ["Melt channel intersections must be burr free and polished: deburr and flush."])

P("core_pin", "Core pin / small mold insert", "Injection mold", ["H", "P"],
  "General mold practice",
  ["3d_surface", "steep_walls", "holes"],
  {"Op10": [
      S("Rough HEM", "Form"),
      S("Z Level Shape Finish", "Pin walls", "steep_walls"),
      S("3D Profile Finish Ball", "Tip radius", "3d_surface"),
      S("Contour Finish", "Shoulder and body")]},
  ["Small tools: keep stickout minimal; grind or EDM where milling cannot hold size."])

P("blow_mold_half", "Blow mold half (aluminum)", "Injection mold", ["N"],
  "General mold practice",
  ["flat_faces", "3d_surface", "steep_walls", "holes", "deep_holes"],
  {"Op10": [
      S("Face Mill", "Parting face", "flat_faces"),
      S("Rough HEM", "Cavity"),
      S("Automatic Rest Machining", "Rest in corners"),
      S("Z Level Shape Finish", "Cavity walls", "steep_walls"),
      S("3D Profile Finish Ball", "Cavity surface; polish or blast follows", "3d_surface"),
      S("Centering", "Spot vent and water", "holes"),
      S("Peck Drill", "Cooling lines", "deep_holes")],
   "Op20": [S("Face Mill", "Back face"), S("Contour Finish", "Outline"), S("Chamfer on 3D Model", "Deburr")]},
  ["Aluminum mold: cavity surface cuts fast; leave blasting stock per finish spec."])

P("compression_mold_plate", "Compression / rubber mold plate", "Injection mold", ["P"],
  GEN,
  ["flat_faces", "pocket", "holes", "deep_holes", "tapped_holes"],
  {"Op10": [
      S("Face Mill", "Face", "flat_faces"),
      S("Rough HEM", "Cavities"),
      S("Pocket HEM", "Cavities", "pocket"),
      S("Contour Finish", "Cavity walls"),
      S("Plane Finish", "Cavity floors"),
      *HOLES()],
   "Op20": [S("Face Mill", "Back face"), *HOLES()]},
  ["Flash grooves and vents are small: use a dedicated small tool at the end."])

# ---- Robotics, automation, optics -------------------------------------------------------------------------------
P("robot_arm_link", "Robot arm link / structural arm (aluminum)", "Robotics and optics", ["N"],
  GEN,
  ["flat_faces", "thin_wall", "pocket", "bores", "holes", "tapped_holes"],
  {"Op10": [
      S("Face Mill", "Datum", "flat_faces"),
      S("Rough HEM", "Arm form"),
      S("Pocket HEM", "Lightweight pockets", "pocket"),
      S("Contour Finish", "Ribs and walls", "thin_wall"),
      S("Boring", "Joint bores", "bores"),
      *HOLES()],
   "Op20": [S("Rough HEM", "Back side"), S("Contour Finish", "Profile"), S("Boring", "Joint bores from the same datum", "bores"), S("Chamfer on 3D Model", "Deburr")]},
  ["Joint bore spacing and parallelism matter: bore all joints in one setup."])

P("harmonic_drive_housing", "Strain-wave / gear reducer housing", "Robotics and optics", ["N"],
  GEN,
  ["flat_faces", "bores", "large_bores", "holes", "tapped_holes", "pocket"],
  {"Op10": [
      S("Face Mill", "Mounting face", "flat_faces"),
      S("Rough HEM", "Outer form"),
      S("Pocket HEM", "Cavity", "pocket"),
      S("Helical Drilling", "Bearing bore rough", "large_bores"),
      S("Boring", "Bearing and flexspline bores", "bores"),
      S("Plane Finish", "Seats"),
      *HOLES()],
   "Op20": [S("Face Mill", "Opposite face"), S("Contour Finish", "Profile"), *HOLES()]},
  ["Bores and seats in one setup hold concentricity."])

P("gripper_finger", "Gripper finger / end effector", "Robotics and optics", ["N", "M"],
  GEN,
  ["flat_faces", "pocket", "3d_surface", "holes", "tapped_holes"],
  {"Op10": [
      S("Face Mill", "Datum", "flat_faces"),
      S("Rough HEM", "Outline"),
      S("Pocket HEM", "Pockets", "pocket"),
      S("3D Profile Finish Ball", "Form-fit surface", "3d_surface"),
      S("Contour Finish", "Profile"),
      *HOLES()]},
  ["Soft stock removal on the grip surface; check the contour against the product."])

P("optical_mount", "Mirror / optical mount (aluminum)", "Robotics and optics", ["N"],
  "General optical hardware practice",
  ["flat_faces", "pocket", "thin_wall", "holes", "tapped_holes", "bores"],
  {"Op10": [
      S("Face Mill", "Mounting datum", "flat_faces"),
      S("Rough HEM", "Outline"),
      S("Pocket HEM", "Mirror seat pocket", "pocket"),
      S("Plane Finish", "Seat flatness"),
      S("Boring", "Optic bore", "bores"),
      *HOLES()],
   "Op20": [S("Face Mill", "Back face"), S("Contour Finish", "Profile"), S("Chamfer on 3D Model", "Deburr")]},
  ["Optical seats: stress relieve between rough and finish; light final pass with fresh tool."])

P("telescope_housing", "Telescope / camera housing (aluminum)", "Robotics and optics", ["N"],
  "General optical housing practice",
  ["flat_faces", "thin_wall", "pocket", "bores", "large_bores", "holes"],
  {"Op10": [
      S("Face Mill", "Flange face", "flat_faces"),
      S("Rough HEM", "Cavity"),
      S("Pocket HEM", "Pockets", "pocket"),
      S("Contour Finish", "Thin walls light passes", "thin_wall"),
      S("Helical Drilling", "Barrel bore rough", "large_bores"),
      S("Boring", "Lens seats", "bores"),
      *HOLES()],
   "Op20": [S("Face Mill", "Opposite flange"), S("Contour Finish", "Profile"), *HOLES()]},
  ["Lens seats are perpendicular to the bore: machine in one setup."])

# ---- General: marine, consumer, motorsport ------------------------------------------------------------------------
P("propeller_blade", "Marine propeller (bronze or stainless)", "General machined parts", ["N", "M"],
  "General marine practice",
  ["blades", "3d_surface", "bores", "flat_faces"],
  {"Op10": [
      S("Face Mill", "Hub faces", "flat_faces"),
      S("Rough HEM", "Blade passages", "blades"),
      S("Automatic Rest Machining", "Rest", "blades"),
      S("Z Level Shape Finish", "Blade faces", "3d_surface"),
      S("3D Profile Finish Ball", "Blade finish", "3d_surface"),
      S("Boring", "Hub bore and taper", "bores"),
      M("5-axis blade finish gives the best surface; 3-axis toolpaths approximate it", "blades")]},
  ["Aluminum bronze is abrasive and tough: carbide tooling with rigid set-up."])

P("unibody_enclosure", "Unibody enclosure / consumer housing (aluminum)", "General machined parts", ["N"],
  "General consumer electronics practice",
  ["flat_faces", "thin_wall", "pocket", "holes", "tapped_holes", "3d_surface"],
  {"Op10": [
      S("Face Mill", "Datum", "flat_faces"),
      S("Rough HEM", "Cavity"),
      S("Pocket HEM", "Pockets", "pocket"),
      S("Contour Finish", "Thin walls with light passes", "thin_wall"),
      S("3D Profile Finish Ball", "Cosmetic surfaces, small constant scallop", "3d_surface"),
      S("Plane Finish", "Cosmetic flats"),
      *HOLES()],
   "Op20": [S("Face Mill", "Back face"), S("Rough HEM", "Back features"), S("Contour Finish", "Profile"), S("Chamfer on 3D Model", "Chamfers per drawing")]},
  ["Cosmetic faces: one tool, one pass, no tool changes mid-surface."])

P("crank_arm", "Bicycle crank arm / small billet component (aluminum)", "General machined parts", ["N"],
  "General practice",
  ["flat_faces", "pocket", "thin_wall", "3d_surface", "holes", "tapped_holes"],
  {"Op10": [
      S("Face Mill", "Datum", "flat_faces"),
      S("Rough HEM", "Arm form"),
      S("Pocket HEM", "Weight-saving pockets", "pocket"),
      S("Contour Finish", "Walls", "thin_wall"),
      S("3D Profile Finish Ball", "Arm contours", "3d_surface"),
      *HOLES()],
   "Op20": [S("Rough HEM", "Back side"), S("3D Profile Finish Ball", "Back contours", "3d_surface"), S("Chamfer on 3D Model", "Deburr")]},
  ["Two-sided billet parts: rough both sides before any finish pass."])

P("drone_frame_plate", "Drone / UAV frame plate", "General machined parts", ["N"],
  "General practice",
  ["flat_faces", "pocket", "holes", "thin_wall"],
  {"Op10": [
      S("Face Mill", "Face plate stock", "flat_faces"),
      S("Rough HEM", "Outline"),
      S("Pocket HEM", "Lightening pockets", "pocket"),
      S("Contour Finish", "Walls", "thin_wall"),
      *HOLES()]},
  ["Thin plate: tabs hold the part; leave tab stock for a final trim."])

# ----------------------------------------------------------------------------
# Hole classes for color coding (CAD face color -> operations)
# Priority order: first match wins when a hole fits several classes.
# ----------------------------------------------------------------------------
HOLE_CLASSES = [
    # key,        color name, RGB,            test description,                    operations
    ("thread",    "yellow",  (255, 255, 0),   "threaded hole (cosmetic or fake thread)", ["Centering", "Drill", "Tapping", "Chamfer on 3D Model"]),
    ("thread_mill","orange", (255, 140, 0),   "thread larger than 0.75 in / 20 mm or hard material", ["Centering", "Drill", "Thread Milling", "Chamfer on 3D Model"]),
    ("tight",     "green",   (0, 176, 80),    "tight tolerance: reamed or bored",       ["Centering", "Drill", "Reaming", "Chamfer on 3D Model"]),
    ("tight_bore","teal",    (0, 150, 150),   "tight tolerance and over 0.75 in / 20 mm: bored", ["Helical Drilling", "Boring", "Chamfer on 3D Model"]),
    ("large",     "red",     (220, 40, 40),   "large bore, rough only (over 0.75 in / 20 mm)", ["Helical Drilling", "Chamfer on 3D Model"]),
    ("deep",      "blue",    (50, 100, 230),  "deep hole over 4xD",                      ["Centering", "Peck Drill", "Chamfer on 3D Model"]),
    ("drill",     "gray",    (160, 160, 160), "drill only, no tolerance callout",        ["Centering", "Drill", "Chamfer on 3D Model"]),
]
HOLE_LARGE_IN = 0.75      # hole diameter at which helical interpolation replaces drilling
HOLE_DEEP_XD = 4.0        # depth / diameter ratio for peck drilling

def classify_hole(diameter_in, depth_in, threaded=False, tight_tol=False, hard_material=False):
    """Return the hole class key for one hole. Dimensions in inches."""
    large = diameter_in > HOLE_LARGE_IN
    if threaded:
        return "thread_mill" if (large or hard_material) else "thread"
    if tight_tol:
        return "tight_bore" if large else "tight"
    if large:
        return "large"
    if depth_in > HOLE_DEEP_XD * diameter_in:
        return "deep"
    return "drill"

def hole_class(key):
    for c in HOLE_CLASSES:
        if c[0] == key:
            return {"key": c[0], "color": c[1], "rgb": c[2], "test": c[3], "ops": list(c[4])}
    raise KeyError(key)

def hole_operations(class_counts):
    """Union of hole operations for a dict {class key: count>0}, in hole-sequence order."""
    order = ["Centering", "Helical Drilling", "Drill", "Peck Drill", "Boring", "Reaming",
             "Thread Milling", "Tapping", "Chamfer on 3D Model"]
    need = set()
    for k, n in class_counts.items():
        if n:
            need.update(hole_class(k)["ops"])
    return [o for o in order if o in need]

# ----------------------------------------------------------------------------
# API
# ----------------------------------------------------------------------------
def parts():
    """List of (key, name, family, iso list) sorted by family."""
    return sorted(((k, v["name"], v["family"], v["iso"]) for k, v in PARTS.items()),
                  key=lambda r: (r[2], r[1]))


# ----------------------------------------------------------------------------
# Machine and setup count. The shop runs 5-axis machines, so most parts finish
# in 1 to 3 setups. MAX_SETUPS = None keeps each part's own setups; 1, 2 or 3
# folds the later setups into the last kept one. The folded steps are
# re-sequenced by operation category and marked "[merged from OpNN]".
# ----------------------------------------------------------------------------
MAX_SETUPS = None
FIVE_AXIS = True

_CAT_RANK = {"face": 0, "rough": 1, "rest": 2, "finish": 3, "hole": 4, "deburr": 5}
_HOLE_RANK = {"Centering": 0, "Drill": 1, "Peck Drill": 1, "Chip Break Drill": 1,
              "Helical Drilling": 1, "Boring": 2, "Reaming": 3, "Thread Milling": 4, "Tapping": 4}

def _resequence(steps):
    lead = []
    steps = list(steps)
    while steps and steps[0]["op"] is None:
        lead.append(steps.pop(0))
    groups = []
    for st in steps:
        if st["op"] is None and groups:
            groups[-1][1].append(st)
        else:
            groups.append((st, []))
    groups.sort(key=lambda g: (_CAT_RANK.get(OPS[g[0]["op"]][0], 3),
                               _HOLE_RANK.get(g[0]["op"], 0)))
    out = list(lead)
    for st, manuals in groups:
        out.append(st)
        out.extend(manuals)
    return out

WARPAGE = False   # force warpage stages for every part (the wizard feature checkbox does it per part)

def _warp_on(part, feats=None):
    f = PARTS[part]["features"] if feats is None else feats
    return bool(WARPAGE or "warpage" in f)

def _expand_warpage(base):
    """Split the first setup into a rough stage and a reface-and-finish stage:
    stage 1 roughs all sides, release and re-clamp flat, stage 2 refaces the datum, then finishing.
    Later setups shift by one key."""
    keys = sorted(base)
    first = base[keys[0]]
    rough, rest, seen_fin = [], [], False
    for st in first:
        cat = OPS[st["op"]][0] if st["op"] else None
        if cat in ("face", "rough") or (cat is None and not seen_fin):
            rough.append(dict(st))
        else:
            if cat:
                seen_fin = True
            rest.append(dict(st))
    if not any(x["op"] for x in rough) or not any(x["op"] for x in rest):
        return base   # nothing to split: composite panels, parts with no cutting in one half
    rough.append(M("Release the clamps: stress relieve or let the part rest, then re-clamp flat with light pressure and indicate flatness"))
    stage2 = [S("Face Mill", "Reface the datum after flattening"), *rest]
    out = {"Op10": rough, "Op20": stage2}
    for i, k in enumerate(keys[1:], 3):
        out["Op%d0" % i] = base[k]
    return out

def _setups(part, feats=None):
    base = PARTS[part]["setups"]
    if _warp_on(part, feats):
        base = _expand_warpage(base)
    keys = sorted(base)
    n = MAX_SETUPS
    if not n or n >= len(keys):
        return base
    keep = keys[:n]
    merged = {k: list(base[k]) for k in keep}
    extra = []
    for k in keys[n:]:
        for st in base[k]:
            st = dict(st)
            st["why"] += " [merged from %s]" % k
            extra.append(st)
    last = keep[-1]
    steps = _resequence(merged[last] + extra)
    if n == 1:
        steps.append(M("Clamped face and stock tab: cut the tab and finish the clamped face in a second operation or a soft-jaw flip if the print needs it"))
    merged[last] = steps
    return merged

FIVE_AXIS_NOTES = [
    "5-axis machine: position with 3+2 to reach each face in one setup; tilt the tool to shorten stickout and reach undercuts.",
    "5-axis machine: drill and tap each hole group with the tool normal to the face in a 3+2 position.",
    "Fewer setups: hold the part on a stock tab, dovetail or zero-point so five faces are reachable, and check head and holder collision in simulation.",
]

def setup_for(part, joblist_name, default="Op10", features=None):
    """Setup key for a joblist name. Reads the number after "Op" (any case, optional space):
    Op20, op 20, OP20 and Op2 all mean setup 20. Returns None when the name carries a setup
    number this part does not have (no operations are planned for that joblist). A name with
    no Op number at all returns the default setup."""
    import re
    keys = sorted(_setups(part, features))
    nums = [int(n) for n in re.findall(r"op[\s_\-]*0*(\d+)", joblist_name or "", flags=re.I)]
    if not nums:
        return default if default in keys else keys[0]
    for n in nums:
        n = n * 10 if n < 10 else n
        k = "Op%d" % n
        if k in keys:
            return k
    return None

def _active(step, features):
    w = step["when"]
    if w is None:
        return True
    if w.startswith("!"):
        return w[1:] not in features
    return w in features

# A feature that works on a drilled hole needs the holes themselves.
IMPLIES = {"tapped_holes": "holes", "reamed_holes": "holes", "deep_holes": "holes",
           "stringy_chips": "holes", "mill_threads": "holes", "cross_holes": "holes"}

def _close(features):
    f = set(features)
    for k, v in IMPLIES.items():
        if k in f:
            f.add(v)
    return f

def plan(part, material_group, setup="Op10", features=None):
    """Ordered steps for one setup. features=None uses the part's default feature set;
    pass a set to override (for example drop 'thin_wall' or add 'deep_holes')."""
    p = PARTS[part]
    feats = _close(p["features"] if features is None else features)
    rules = MATERIAL_RULES.get(iso_letter(material_group), {"swap": {}, "drop": [], "notes": []})
    out, seen = [], set()
    for st in _setups(part, feats).get(setup, []):
        if not _active(st, feats):
            continue
        st = dict(st)
        if st["op"] in rules["drop"]:
            continue
        if st["op"] in rules["swap"]:
            st["why"] += " [material swap from %s]" % st["op"]
            st["op"] = rules["swap"][st["op"]]
        key = (st["op"], st["why"])
        if key in seen:
            continue
        seen.add(key)
        out.append(st)
    return out

def operations(part, material_group, setup="Op10", features=None):
    """Operation names in application order, duplicates removed (first use wins
    for position). Manual-only steps are excluded."""
    ops = []
    for st in sequenced_plan(part, material_group, setup, features):
        if st["op"] and st["op"] not in ops:
            ops.append(st["op"])
    return ops


def operation_sequence(part, material_group, setup="Op10", features=None):
    """Operation names in the exact order they are made, each repeated n times (no duplicate removal)."""
    seq = []
    for st in sequenced_plan(part, material_group, setup, features):
        if st["op"]:
            seq.extend([st["op"]] * int(st.get("count", 1)))
    return seq


# ----------------------------------------------------------------------------
# Research layer: sourced notes appended to a part's notes, plus a map from our
# generic operations to the real hyperMILL toolpath type (menu names, v35).
# Sources: Walter titanium aerospace article (MSC betterMRO), DME machining
# tolerances guide, MMS blisk roughing article (Sandvik CoroMill M5C331),
# Sandvik aerospace guides from earlier segments.
# ----------------------------------------------------------------------------
HYPERMILL_TYPE = {
    "Face Mill": "2D Milling > Face Milling",
    "Rough HEM": "3D Milling > 3D Optimized Roughing (HEM settings)",
    "Pocket HEM": "2D Milling > Pocket Milling / 3D Optimized Roughing",
    "Rough Traditional": "3D Milling > 3D Optimized Roughing",
    "3D Plunge Roughing": "3D Advanced > 3D Plunge Roughing",
    "Plunge Milling": "2D Milling > Plunge Milling",
    "Automatic Rest Machining": "3D Advanced > 3D Automatic Rest Machining",
    "Contour Finish": "2D Milling > Contour Milling",
    "Plane Finish": "3D Milling > 3D Plane Machining",
    "3D Profile Finish Ball": "3D Milling > 3D Profile Finishing",
    "Z Level Shape Finish": "3D Milling > 3D Z Level Shape Finishing",
    "Centering": "Drilling > Centering",
    "Drill": "Drilling > Simple Drilling",
    "Peck Drill": "Drilling > Drilling with Pecking",
    "Chip Break Drill": "Drilling > Drilling with Chip Break",
    "Helical Drilling": "Drilling > Helical Drilling",
    "Boring": "Drilling > Boring",
    "Reaming": "Drilling > Reaming",
    "Thread Milling": "Drilling > Thread Milling",
    "Tapping": "Drilling > Tapping",
    "Chamfer on 3D Model": "2D Milling > Chamfer Milling on 3D Model",
    "Swarf Curve": "5X Milling > Swarf Machining (curve)",
    "Swarf Surface": "5X Milling > Swarf Machining (surfaces)",
}

# Mold plate hole tolerances (DME guide, inch). Used to justify ream / bore.
MOLD_TOL_IN = {
    "ejector / core pin hole": "+0.0005/+0.001 -> ream",
    "leader pin bore": "+0.0006/+0.0011, location +-0.001 -> ream or bore",
    "bushing bore": "+0.0004/+0.0008 -> bore or ream",
    "dowel hole": "+0.0008/+0.003 -> ream",
    "finish pocket / bore": "+-0.001, alignment +-0.0005 -> finish bore, interpolate last",
    "eye bolt tap drill": "0/+0.06 -> drill only",
}

_TI_WALTER = [
    "Walter Ti6Al4V pocket test: porcupine/tangential cutter ~130 sfm, 0.006 in/tooth, 1.46 in ap in two steps (~12.9 in3/min); "
    "high-feed face mill ~197 sfm, 0.028 in/tooth, 0.6 in ap (~5.7 in3/min).",
    "Walter Ti pocketing: constant-engagement toolpath (HEM), solid carbide ~380 sfm, 0.005 in/tooth, ap ~1.9 in, ae ~0.08 in. "
    "Semi-finish ae ~0.15 in, finish ae ~0.012 in.",
]
RESEARCH = {
    "blisk_titanium": ["Sandvik: disc cutter (CoroMill M5C331) that follows the blade-to-blade profile removes the slot in one "
                       "continuous multiaxis motion instead of stepped plunges. Leave uniform stock for semi-finish."],
    "blisk_hrsa": ["Same disc-cutter idea as titanium; in HRSA ceramic or round-insert roughing needs a rigid machine."],
    "engine_mount": _TI_WALTER, "thrust_fitting": _TI_WALTER, "pylon_bracket": _TI_WALTER,
    "landing_gear_beam": _TI_WALTER, "clevis_lug_fitting": _TI_WALTER, "fan_casing": _TI_WALTER,
    "mold_ejector_plate": ["DME tolerances (in): ejector/core pin holes +0.0005/+0.001 (ream); leader pin bore +0.0006/+0.0011, "
                           "location +-0.001; bushing bore +0.0004/+0.0008; dowel +0.0008/+0.003; eye bolt tap drill 0/+0.06."],
    "mold_base_plate": ["DME tolerances (in): finish pocket +-0.001 size and depth, alignment +-0.0005; leader pin bore "
                        "+0.0006/+0.0011; bushing bore +0.0004/+0.0008. Pockets: rough, semi, then finish in one setup."],
    "molding_surface_block": ["Finish pockets and bores to +-0.001 with +-0.0005 alignment: take a spring pass on the last cut."],
}

WARP_NOTES = [
    "Warpage: rough all sides leaving 0.040 in (0.060 in on weldments), release and stress relieve, re-clamp flat, reface the datum, then finish.",
    "Warpage: indicate flatness after re-clamping and before the reface; rework the first stage if the part moved more than the stock left.",
]

def notes(part, material_group, features=None):
    """Application notes for a part plus the material rule notes."""
    p = PARTS[part]
    return (list(p["apply"]) + RESEARCH.get(part, [])
            + (WARP_NOTES if _warp_on(part, features) else [])
            + (FIVE_AXIS_NOTES if FIVE_AXIS else [])
            + MATERIAL_RULES.get(iso_letter(material_group), {"notes": []})["notes"])

def find(text):
    """Part keys whose name/family matches text (case-insensitive)."""
    t = text.lower()
    return [k for k, v in PARTS.items() if t in k or t in v["name"].lower() or t in v["family"].lower()]

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        for k, n, f, iso in parts():
            print("%-24s %-48s %s" % (k, n, f))
    else:
        part = sys.argv[1]
        mat = sys.argv[2] if len(sys.argv) > 2 else "S - Titanium"
        for setup in sorted(PARTS[part]["setups"]):
            print("==", PARTS[part]["name"], "|", mat, "|", setup)
            for st in plan(part, mat, setup):
                print("  %-26s %s" % (st["op"] or "(manual)", st["why"]))
        print("notes:")
        for n in notes(part, mat):
            print("  -", n)

# ----------------------------------------------------------------------------
# Wizard data: industries, shape pictures, feature labels
# ----------------------------------------------------------------------------
INDUSTRIES = [
    ("Aerospace", ["Aluminum structure", "Composite structure", "Titanium structure",
                   "Titanium and high alloy steel", "Stainless and high alloy steel",
                   "Engine rotating", "Engine casing"]),
    ("Space", ["Space propulsion", "Space structures"]),
    ("Defense", ["Defense"]),
    ("Mold and die", ["Injection mold", "Mold and die"]),
    ("Fabrication and weldments", ["Weldments"]),
    ("Medical", ["Medical"]),
    ("Automotive and motorsport", ["Automotive"]),
    ("Oil gas and energy", ["Oil gas and energy"]),
    ("Semiconductor and electronics", ["Semiconductor and electronics"]),
    ("Tooling and fixtures", ["Tooling and fixtures"]),
    ("Robotics and optics", ["Robotics and optics"]),
    ("General industrial", ["General machined parts"]),
]

# icon file, label, parts that look like it
SHAPES = [
    ("plate_pockets", "Flat plate with pockets and holes",
     ["plate_bracket", "fixture_plate", "mold_base_plate", "mold_ejector_plate", "end_cap_cylinder", "defense_bracket_armor",
      "soft_jaws", "progressive_die_plate", "inspection_fixture", "compression_mold_plate", "wafer_chuck",
      "showerhead_plate", "drone_frame_plate", "cold_plate", "tombstone_fixture", "rf_waveguide"]),
    ("ribbed_thin", "Thin-wall ribbed frame or webbed structure",
     ["wing_rib", "wing_spar", "satellite_panel_bracket", "heat_sink_enclosure", "landing_gear_beam",
      "fuselage_bulkhead", "seat_track", "satellite_housing", "robot_arm_link", "control_arm", "gimbal_mount", "unibody_enclosure"]),
    ("block_ports", "Solid block with many cross-drilled holes",
     ["manifold_block", "valve_body", "rocket_injector_plate", "gearbox_housing", "aero_actuator_housing",
      "gas_manifold", "hot_runner_manifold", "choke_valve_body"]),
    ("cast_housing", "Large cast or forged housing with bores",
     ["cylinder_head", "engine_block", "transmission_case", "brake_caliper", "turbo_housing", "pump_casing",
      "wellhead_body", "frac_fluid_end", "aero_gearbox_housing", "harmonic_drive_housing", "turret_ring_housing",
      "turbopump_housing", "vacuum_chamber", "telescope_housing", "intake_manifold"]),
    ("round_ring", "Round ring, flange or disc",
     ["bearing_housing_flange", "fan_disc", "turbine_disc", "spool", "fan_casing", "combustion_casing",
      "compressor_vane_ring", "api_flange", "rocket_nozzle_extension", "piston_forged"]),
    ("shaft_long", "Long round shaft or tube", ["shaft", "downhole_tool_housing", "suppressor_baffle"]),
    ("blades", "Bladed rotor, blisk, impeller or propeller",
     ["blisk_titanium", "blisk_hrsa", "impeller", "turbine_blade_dovetail", "propeller_blade"]),
    ("contoured_surface", "Contoured 3D molding surface or die",
     ["molding_surface_block", "mold_cavity", "die_forging_insert", "thrust_chamber_liner", "punch_die_insert",
      "mold_slide_lifter", "core_pin", "blow_mold_half"]),
    ("bracket_fitting", "Chunky bracket or fitting with a deep slot",
     ["engine_mount", "thrust_fitting", "pylon_bracket", "main_fitting", "flap_track", "slat_track",
      "clevis_lug_fitting", "wheel_hub_upright", "gripper_finger", "optic_mount", "crank_arm", "optical_mount"]),
    ("receiver", "Forged housing with an internal cavity",
     ["lower_receiver", "upper_receiver"]),
    ("organic_implant", "Organic freeform part (implant, instrument)",
     ["hip_stem", "knee_femoral", "bone_plate", "spinal_cage", "dental_abutment", "orthopedic_trial", "surgical_instrument"]),
    ("weldment", "Welded steel frame", ["weldment_frame", "weldment_machine_base"]),
    ("composite_panel", "Large thin composite panel",
     ["central_wing_box", "vertical_tail_frame", "composite_wing_skin"]),
]

FEATURE_LABELS = {
    "flat_faces": "Flat faces to skim", "thin_wall": "Thin walls", "thin_floor": "Thin floors",
    "deep_pocket": "Deep pockets", "pocket": "Pockets", "deep_slot": "Deep slot",
    "closed_angle": "Closed angles under 90 degrees", "boss": "Bosses", "3d_surface": "Contoured 3D surfaces",
    "steep_walls": "Steep walls", "blades": "Blades", "scallop": "Scallops", "long_reach": "Long reach needed",
    "holes": "Holes", "deep_holes": "Deep holes over 4xD", "tapped_holes": "Tapped holes",
    "mill_threads": "Thread milled threads", "reamed_holes": "Reamed holes", "bores": "Finish bores",
    "large_bores": "Large bores over 0.75 in", "stringy_chips": "Long-chip material drilling",
    "cross_holes": "Cross holes", "turned": "Turned features (done elsewhere)",
    "warpage": "Warpage risk: flatten and reface",
}

def industry_of(part):
    fam = PARTS[part]["family"]
    for name, fams in INDUSTRIES:
        if fam in fams:
            return name
    return "General industrial"

def parts_in_industry(industry):
    return [k for k, v in sorted(PARTS.items(), key=lambda kv: kv[1]["name"]) if industry_of(k) == industry]

def relevant_features(part):
    """All feature flags that any step of this part tests, in label order."""
    flags = set()
    for steps in PARTS[part]["setups"].values():  # original setups: every flag any step tests
        for st in steps:
            w = st["when"]
            if w:
                flags.add(w.lstrip("!"))
    flags |= PARTS[part]["features"]
    flags.add("warpage")
    return [f for f in FEATURE_LABELS if f in flags]


# ============================================================================
# Sequencing layer
#   1. sequenced_plan / sequence_text : numbered steps, each with the reason
#      for its position
#   2. RULES / check_part              : ordering rules every part must satisfy;
#      allowed exceptions are listed in EXCEPTIONS with a written reason
#   3. SETUP_GUIDE / setup_guide       : what each setup does and what it leaves
#   4. adjust_steps                    : geometry-driven reordering
# Set ADJUST = False to return the original hand-written order unchanged.
# ============================================================================
ADJUST = True

_FINISH = ("Contour Finish", "Plane Finish", "Z Level Shape Finish", "3D Profile Finish Ball")
_ROUGH = ("Rough HEM", "Rough Traditional", "Pocket HEM", "3D Plunge Roughing", "Plunge Milling")
_DRILL = ("Drill", "Peck Drill", "Chip Break Drill")
_SIZE = ("Reaming", "Tapping", "Thread Milling")

POSITION_WHY = {
    "Face Mill": "First: creates the datum surface every later toolpath references.",
    "Rough HEM": "After facing: removes the bulk while the part is at its stiffest.",
    "Rough Traditional": "After facing: removes the bulk while the part is at its stiffest.",
    "Pocket HEM": "With roughing: clears pockets before any finishing tool touches the part.",
    "3D Plunge Roughing": "With roughing: bulk removal for long reach or weak setups.",
    "Plunge Milling": "With roughing: bulk removal in slots and pockets.",
    "Automatic Rest Machining": "After roughing: clears what the large tool left so finishing tools see even stock.",
    "Contour Finish": "After roughing and rest: finishes walls with even stock left.",
    "Plane Finish": "After roughing and rest: finishes floors and flat faces with even stock left.",
    "Z Level Shape Finish": "After roughing and rest: finishes steep surfaces at constant Z.",
    "3D Profile Finish Ball": "After the steep and flat finishing: blends the contoured surface.",
    "Centering": "Before drilling: spot so every drill starts on location.",
    "Drill": "After spotting: opens the hole.",
    "Peck Drill": "After spotting: opens deep holes with chip clearance.",
    "Chip Break Drill": "After spotting: opens holes in long-chip material.",
    "Helical Drilling": "Before boring: opens large holes with lower force than a drill.",
    "Boring": "After the hole is opened: sizes it, before reaming where both are used.",
    "Reaming": "After drilling: the reamer needs a straight, correctly sized pilot hole.",
    "Thread Milling": "After the hole is sized: thread last so no later cut disturbs it.",
    "Tapping": "After the hole is drilled: thread last so no later cut disturbs it.",
    "Chamfer on 3D Model": "Last: breaks every edge after all cutting is done.",
    "Swarf Curve": "After rest machining: swarf finishes the steep walls with the flank of the tool.",
    "Swarf Surface": "After rest machining: swarf finishes the steep walls with the flank of the tool.",
}

# (rule id, description, check function over op list -> bool OK)
def _chamfer_last(ops):
    return "Chamfer on 3D Model" not in ops or ops[-1] == "Chamfer on 3D Model"

def _holes_after_finish(ops):
    # a drilling, reaming or tapping step must not precede a finishing step.
    # Opening or boring a large bore (Helical Drilling, Boring, Thread Milling)
    # before floor finishing is a standing allowance.
    late = set(_DRILL) | {"Centering", "Reaming", "Tapping"}
    for i, o in enumerate(ops):
        if o in late and any(x in _FINISH for x in ops[i + 1:]):
            return False
    return True

RULES = [
    ("R1", "Face Mill before roughing",
     lambda ops: all(not (o in _ROUGH and "Face Mill" in ops[ops.index(o) + 1:]) for o in ops)),
    ("R2", "Roughing before finishing and rest machining",
     lambda ops: all(not (o in _FINISH + ("Automatic Rest Machining",) and any(r in _ROUGH for r in ops[ops.index(o) + 1:])) for o in ops)),
    ("R3", "Rest machining before finishing",
     lambda ops: all(not (o == "Automatic Rest Machining" and any(f in _FINISH for f in ops[:ops.index(o)])) for o in ops)),
    ("R4", "Centering before drilling",
     lambda ops: all(not (o == "Centering" and any(d in _DRILL for d in ops[:ops.index(o)])) for o in ops)),
    ("R5", "Drilling before reaming and tapping",
     lambda ops: all(not (o in ("Reaming", "Tapping") and any(d in _DRILL for d in ops[ops.index(o) + 1:])) for o in ops)),
    ("R6", "Helical Drilling before Boring",
     lambda ops: not ("Helical Drilling" in ops and "Boring" in ops and ops.index("Helical Drilling") > ops.index("Boring"))),
    ("R7", "Chamfer last", _chamfer_last),
    ("R8", "Drilling, reaming and tapping after finishing", _holes_after_finish),
]

# (part, setup, rule id) -> written reason the order is correct for that part
EXCEPTIONS = {
    ("engine_block", "*", "R6"): "Main bearing bores are cast cored and bored directly; helical drilling applies only to the other large holes.",
    ("main_fitting", "*", "R4"): "The large main bore is peck drilled from solid without a spot; the small holes are spotted after.",
}

def check_part(part, material_group="P - Low Carbon Steel"):
    """Rule violations for every setup of a part: list of (setup, rule id, description).
    Exceptions with a written reason are excluded."""
    bad = []
    for setup in sorted(_setups(part)):
        ops = [st["op"] for st in sequenced_plan(part, material_group, setup) if st["op"]]
        for rid, desc, fn in RULES:
            if not fn(ops) and (part, setup, rid) not in EXCEPTIONS and (part, "*", rid) not in EXCEPTIONS:
                bad.append((setup, rid, desc))
    return bad

# ---- geometry-driven reordering -------------------------------------------
def _move_after_last(steps, mover_ops, anchor_ops, why):
    """Move steps whose op is in mover_ops to after the last step whose op is in anchor_ops."""
    movers = [s for s in steps if s["op"] in mover_ops]
    rest = [s for s in steps if s["op"] not in mover_ops]
    idx = max([i for i, s in enumerate(rest) if s["op"] in anchor_ops], default=-1)
    if idx < 0 or not movers:
        return steps
    new = rest[:idx + 1] + [dict(m, seq_note=why) for m in movers] + rest[idx + 1:]
    return new if [s["op"] for s in new] != [s["op"] for s in steps] else steps

def adjust_steps(steps, feats):
    """Reorder by geometry. Operation sets never change, only the order."""
    out = list(steps)
    if "thin_wall" in feats:
        out = _move_after_last(
            out, ("Contour Finish",), ("Plane Finish", "Z Level Shape Finish", "3D Profile Finish Ball"),
            "Thin walls: finished last among the finishing cuts so the wall keeps its stock and stiffness while floors are cut.")
    if "thin_floor" in feats:
        out = _move_after_last(
            out, ("Plane Finish",), ("Contour Finish", "Z Level Shape Finish", "3D Profile Finish Ball"),
            "Thin floors: walls finish first, floor last in one light pass so wall cutting forces do not flex it.")
    # chamfer always last among machine operations
    ch = [s for s in out if s["op"] == "Chamfer on 3D Model"]
    if ch and [s for s in out if s["op"]][-1]["op"] != "Chamfer on 3D Model":
        out = [s for s in out if s["op"] != "Chamfer on 3D Model"] + [dict(c, seq_note="Moved last: edges are broken after all cutting.") for c in ch]
    return out

def sequenced_plan(part, material_group, setup="Op10", features=None):
    """plan() with geometry reordering applied and a position reason on each step.
    Each step dict gains n (number, machine and manual steps counted), position_why."""
    feats = _close(PARTS[part]["features"] if features is None else features)
    steps = plan(part, material_group, setup, features)
    if ADJUST and not PARTS[part].get("ordered"):
        steps = adjust_steps(steps, feats)
    out = []
    for i, st in enumerate(steps, 1):
        st = dict(st)
        st["n"] = i
        st["position_why"] = st.pop("seq_note", None) or (POSITION_WHY.get(st["op"], "") if st["op"] else "Manual step.")
        out.append(st)
    return out

# ---- setup guidance --------------------------------------------------------
SETUP_GUIDE = {
    "Aluminum structure": {
        "Op10": "Datum: clamp on the stock rim or sacrificial tabs; face the first side, rough the pockets, leave tabs and 0.010 in on thin walls.",
        "Op20": "Flip on the finished datum with soft jaws or vacuum; machine the second side, cut tabs last, deburr."},
    "Composite structure": {
        "Op10": "Datum: vacuum fixture with indexed pins; trim and drill the first face.",
        "Op20": "Second face or stack drilling on the mating tool."},
    "Titanium structure": {
        "Op10": "Datum: rigid vise or fixture plate, short stickout; rough all features with 0.040 in left on walls.",
        "Op20": "Flip on finished faces; finish remaining features and holes."},
    "Titanium and high alloy steel": {
        "Op10": "Datum: bore or forging pad; rough in the softest heat-treat state, leave 0.040 in.",
        "Op20": "After heat treat if required: finish datum faces, bores and holes."},
    "Stainless and high alloy steel": {
        "Op10": "Datum: first face on the vise or fixture; rough and drill in the annealed state.",
        "Op20": "Flip on finished faces; finish."},
    "Engine rotating": {
        "Op10": "Datum: chuck or arbor on the bore; rough and semi-finish, leave stock on blades and flow path.",
        "Op20": "Second side or finish pass on the finished bore datum."},
    "Engine casing": {
        "Op10": "Datum: flange face and pilot diameter; finish the datum first, rough the rest.",
        "Op20": "Flip on the finished flange; machine the opposite side."},
    "General machined parts": {
        "Op10": "Datum: largest flat face down in the vise or on parallels; face and rough.",
        "Op20": "Flip on the finished face; machine the second side."},
    "Mold and die": {
        "Op10": "Datum: fixture on the finished back face; rough in the soft state.",
        "Op20": "Second side, then finish after heat treat as required."},
    "Injection mold": {
        "Op10": "Datum: ground plate faces; machine pockets and holes in one setup to hold hole-to-pocket position.",
        "Op20": "Flip on the ground face; machine the second side."},
    "Defense": {
        "Op10": "Datum: vise or dedicated fixture on the forging or plate; face, rough, drill the pattern.",
        "Op20": "Flip on the finished face; machine the second side and finish."},
    "Weldments": {
        "Op10": "Datum: stress relieve before any cutting; face the mounting surfaces, leave 0.030 in for the second pass.",
        "Op20": "After the second stress relief: finish mounting faces and bores."},
    "Medical": {
        "Op10": "Datum: dedicated fixture or stock tab; rough and semi-finish, leave a tab.",
        "Op20": "Flip on the finished datum; remove the tab and finish."},
    "Automotive": {
        "Op10": "Datum: locating pins and clamps on cast pads; machine datum faces and bores first.",
        "Op20": "Second side on the finished datum faces."},
    "Oil gas and energy": {
        "Op10": "Datum: first end face and bore; rough with large stock, leave 0.060 in.",
        "Op20": "Flip on the finished end; machine the second end and ports."},
    "Semiconductor and electronics": {
        "Op10": "Datum: vacuum or soft jaws on the stock; finish first side to flatness.",
        "Op20": "Flip on the finished face; finish second side and pattern."},
    "Tooling and fixtures": {
        "Op10": "Datum: vise on parallels; face, rough and drill.",
        "Op20": "Flip on the finished face and finish."},
    "Robotics and optics": {
        "Op10": "Datum: soft jaws or fixture; rough and semi-finish, leave 0.010 in on thin sections.",
        "Op20": "Flip on the finished datum; finish."},
    "Space propulsion": {
        "Op10": "Datum: chuck or bore datum; rough with stock for stress release.",
        "Op20": "After stress relief: finish features and pattern."},
    "Space structures": {
        "Op10": "Datum: vacuum or stock tabs; rough and lightweight pockets, leave 0.010 in on thin walls.",
        "Op20": "Flip on the finished datum; finish."},
}
SETUP_DEFAULT = {"Op10": "Datum: first face on the fixture; face and rough.",
                 "Op20": "Flip on the finished datum; machine the second side.",
                 "Op30": "Third setup: remaining features on the finished datums.",
                 "Op40": "Fourth setup: remaining features on the finished datums.",
                 "Op50": "Fifth setup: remaining features on the finished datums.",
                 "Op60": "Sixth setup: remaining features on the finished datums."}
WARP_GUIDE = {
    "Op10": "Stage 1: rough all sides, leave 0.040 in (0.060 in on weldments); release the clamps and stress relieve or rest the part before the next stage.",
    "Op20": "Stage 2: re-clamp flat with light pressure, indicate flatness, reface the datum, then finish.",
}

def setup_guide(part, setup, features=None):
    if setup is None:
        return ""
    fam = PARTS[part]["family"]
    warp = _warp_on(part, features)
    if warp and setup in WARP_GUIDE:
        text = WARP_GUIDE[setup]
    else:
        # a setup shifted by warpage keeps the family text of the setup it came from
        src = setup
        if warp and setup > "Op20":
            src = "Op%d0" % (int(setup[2:]) // 10 - 1)
        text = SETUP_GUIDE.get(fam, {}).get(src) or SETUP_DEFAULT.get(setup, "")
    n_full = len(_expand_warpage(PARTS[part]["setups"]) if warp else PARTS[part]["setups"])
    if MAX_SETUPS and MAX_SETUPS < n_full and setup == sorted(_setups(part, features))[-1]:
        text += " Merged setup: the later setups are folded in; reach the other faces with 5-axis positioning."
    return text

def sequence_text(part, material_group, setup="Op10", features=None):
    """Printable numbered sequence with reasons, plus the setup guide."""
    lines = ["%s | %s | %s" % (PARTS[part]["name"], material_group, setup), "  " + setup_guide(part, setup, features)]
    for st in sequenced_plan(part, material_group, setup, features):
        if not st["op"]:
            lines.append("  %2d. (manual)                  %s" % (st["n"], st["why"]))
            continue
        lines.append("  %2d. %-26s %s" % (st["n"], st["op"], st["position_why"]))
        if st["why"] and st["why"] != st["position_why"]:
            lines.append("      %s" % st["why"])
    return "\n".join(lines)
