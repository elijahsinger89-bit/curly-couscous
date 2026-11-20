# job_types.py - every milling and drilling toolpath type the part wizards can create (77 of hyperMILL 35's 89 CreateJob codes;
# the 12 turning cycles are left out). All 89 codes were created successfully in hyperMILL by probe_create_jobs.
#
# Per operation: CreateJob code, menu group, and the rule part_wizard_2 uses to pick the tool:
#   hole     = a hole operation of hole_jobs (diameter and depth from the attached Generic Hole features)
#   chamfer  = chamfer mill (Walter MC501) or a 90 degree spot drill for manufacturers without chamfer mills
#   rough    = end mill sized by the pocket diameter limit only (roughing; rest machining takes the corners)
#   corner   = end mill sized by the smallest pocket corner radius and the diameter limit (finishing, rest)
#   floor    = end mill sized by the diameter limit; floor corner radius turns a flat into a corner radius tool
#   default  = default tool size below, flute at least 1 x D (or the deepest attached feature)
#   face     = inserted face mill, else an end mill
#   hand     = no matching tool type in the library yet (T-slot, hale, barrel, gun drill, back boring, brush): tool it by hand
# usage = primary usage key of tool_usage.py (orders the first-choice families, picks the cutting-data set)
# shape / dia = default tool when the operation has no saved settings in job_settings.json
#
# The 21 operations the part plans use keep their own names (Rough HEM, Pocket HEM ...) and have saved settings per material in
# job_settings.json. Every other type is created with hyperMILL's default settings.

#        operation name,                       code,     group,        rule,      usage,          shape,    dia
_T = [
    # operations with saved settings (used by the part plans)
    ("Face Mill",                          "Face",   "2D",          "face",    "finish_floor", "radius", 1.0),
    ("Contour Finish",                     "Cc",     "2D",          "corner",  "finish_wall",  "flat",   0.5),
    ("Pocket HEM",                         "Ccp",    "2D",          "rough",   "hem",          "radius", 0.5),
    ("Plunge Milling",                     "Pl3x",   "2D",          "rough",   "",             "flat",   0.5),
    ("Chamfer on 3D Model",                "Ccc",    "2D",          "chamfer", "",             "",       0.0),
    ("Rough HEM",                          "Slr3",   "3D",          "rough",   "hem",          "radius", 0.5),
    ("Rough Traditional",                  "Slr3",   "3D",          "rough",   "rough",        "radius", 0.5),
    ("3D Plunge Roughing",                 "Plun",   "3D",          "rough",   "",             "flat",   0.5),
    ("Automatic Rest Machining",           "Rmat2",  "3D",          "corner",  "semi",         "ball",   0.375),
    ("Plane Finish",                       "Pln",    "3D",          "floor",   "finish_floor", "flat",   0.5),
    ("Z Level Shape Finish",               "Slf3",   "3D",          "corner",  "profile3d",    "ball",   0.375),
    ("3D Profile Finish Ball",             "Prof",   "3D",          "default", "profile3d",    "ball",   0.375),
    ("Swarf Curve",                        "F1X5",   "5X",          "corner",  "finish_wall",  "flat",   0.5),
    ("Swarf Surface",                      "F1X5",   "5X",          "corner",  "finish_wall",  "flat",   0.5),
    ("Centering",                          "DcenX5", "Drilling",    "hole",    "",             "",       0.0),
    ("Drill",                              "DdrX5",  "Drilling",    "hole",    "",             "",       0.0),
    ("Chip Break Drill",                   "DcbX5",  "Drilling",    "hole",    "",             "",       0.0),
    ("Peck Drill",                         "DpecX5", "Drilling",    "hole",    "",             "",       0.0),
    ("Reaming",                            "DrmX5",  "Drilling",    "hole",    "",             "",       0.0),
    ("Tapping",                            "DtapX5", "Drilling",    "hole",    "",             "",       0.0),
    ("Boring",                             "DborX5", "Drilling",    "hole",    "",             "",       0.0),
    ("Helical Drilling",                   "DmdX5",  "Drilling",    "hole",    "",             "",       0.0),
    ("Thread Milling",                     "DntmX5", "Drilling",    "hole",    "",             "",       0.0),
    # every other milling and drilling type (hyperMILL default settings)
    ("Contour Milling on 3D Model",        "Cc3D",   "2D",          "corner",  "finish_wall",  "flat",   0.5),
    ("T-Slot Milling on 3D Model",         "Ts3D",   "2D",          "hand",    "",             "",       0.0),
    ("Inclined Contouring",                "Ccin",   "2D",          "corner",  "finish_wall",  "flat",   0.5),
    ("Inclined Pocketing",                 "Ccpin",  "2D",          "rough",   "hem",          "radius", 0.5),
    ("Rectangular Pocket",                 "Rp",     "2D",          "rough",   "hem",          "radius", 0.5),
    ("2D Rest Machining",                  "Rif2",   "2D",          "corner",  "semi",         "flat",   0.25),
    ("Playback Milling",                   "Plb",    "2D",          "default", "",             "flat",   0.5),
    ("Hale Machining",                     "Cch",    "2D",          "hand",    "",             "",       0.0),
    ("3D Iso Machining",                   "Iso",    "3D",          "default", "profile3d",    "ball",   0.375),
    ("3D Free Path Milling",               "Curv",   "3D",          "default", "profile3d",    "ball",   0.375),
    ("3D Arbitrary Stock Roughing",        "Stoc2",  "3D",          "rough",   "hem",          "radius", 0.5),
    ("3D Z Level Finishing",               "Zfin",   "3D",          "corner",  "profile3d",    "ball",   0.375),
    ("3D Complete Finishing",              "Zopt",   "3D",          "default", "profile3d",    "ball",   0.375),
    ("3D Equidistant Finishing",           "Scal",   "3D",          "default", "profile3d",    "ball",   0.375),
    ("3D Corner Rest Machining",           "Rcm",    "3D",          "corner",  "semi",         "ball",   0.25),
    ("3D Cutting Edge Machining",          "Ecut",   "3D",          "default", "profile3d",    "ball",   0.25),
    ("3D Rework Machining",                "Rwrk",   "3D",          "corner",  "semi",         "ball",   0.25),
    ("3D Curve Flow Machining",            "Edm2",   "3D",          "default", "profile3d",    "ball",   0.375),
    ("3D Rib / Groove Machining",          "Rbx3",   "3D",          "corner",  "semi",         "ball",   0.25),
    ("3D Form Pocket",                     "Form",   "3D",          "rough",   "hem",          "radius", 0.5),
    ("3D Pencil Milling",                  "Pecl",   "3D",          "corner",  "profile3d",    "ball",   0.25),
    ("5X Optimized Rest Roughing",         "OrX5",   "5X",          "rough",   "hem",          "radius", 0.375),
    ("5X Profile Finishing",               "Pf2X5",  "5X",          "default", "profile3d",    "ball",   0.375),
    ("5X Profile Finishing (old)",         "PfX5",   "5X",          "default", "profile3d",    "ball",   0.375),
    ("5X Z Level Finishing",               "ZfX5",   "5X",          "corner",  "profile3d",    "ball",   0.375),
    ("5X Iso Machining",                   "Is2X5",  "5X",          "default", "profile3d",    "ball",   0.375),
    ("5X Equidistant Finishing",           "ScX5",   "5X",          "default", "profile3d",    "ball",   0.375),
    ("5X Rest Machining",                  "RmX5",   "5X",          "corner",  "semi",         "ball",   0.25),
    ("5X Corner Rest Machining",           "RcX5",   "5X",          "corner",  "semi",         "ball",   0.25),
    ("5X Free Path Machining",             "CvX5",   "5X",          "default", "profile3d",    "ball",   0.375),
    ("5X Rework Machining",                "RwrkX5", "5X",          "corner",  "semi",         "ball",   0.25),
    ("5X Z Level Roughing",                "RuppX5", "5X",          "rough",   "hem",          "radius", 0.5),
    ("5X Cutting Edge Plunge",             "PlX5",   "5X",          "rough",   "",             "flat",   0.5),
    ("5X Cutting Edge Swarf",              "TmX5",   "5X",          "corner",  "finish_wall",  "flat",   0.5),
    ("5X Radial Machining",                "RaX5",   "5X",          "default", "profile3d",    "ball",   0.375),
    ("5X Halfpipe Machining",              "Th2X5",  "5X",          "default", "profile3d",    "ball",   0.375),
    ("5X Top Milling",                     "TpX5",   "5X",          "default", "profile3d",    "ball",   0.375),
    ("5X Iso Top Milling",                 "IsX5",   "5X",          "default", "profile3d",    "ball",   0.375),
    ("5X Contouring",                      "CtX5",   "5X",          "corner",  "finish_wall",  "flat",   0.5),
    ("5X Swarf Cutting two Curves",        "F2X5",   "5X",          "corner",  "finish_wall",  "flat",   0.5),
    ("5X Swarf Cutting Planes",            "FPX5",   "5X",          "corner",  "finish_wall",  "flat",   0.5),
    ("5X Shape Offset Roughing",           "SlrX5",  "5X",          "rough",   "hem",          "radius", 0.5),
    ("5X Shape Offset Finishing",          "SlfX5",  "5X",          "default", "profile3d",    "ball",   0.375),
    ("5X Tangent Machining",               "RtX5",   "5X",          "hand",    "",             "",       0.0),
    ("5X Tangent Plane Machining",         "TplnX5", "5X",          "hand",    "",             "",       0.0),
    ("5X Prismatic Fillet Finishing",      "PcfX5",  "5X",          "corner",  "profile3d",    "ball",   0.25),
    ("5X Deburring",                       "GDbrX5", "5X",          "chamfer", "",             "",       0.0),
    ("5X Hole Deburring",                  "DdbrX5", "Drilling",    "chamfer", "",             "",       0.0),
    ("Optimized Deep Hole Drilling",       "Dda2X5", "Drilling",    "hole",    "",             "",       0.0),
    ("Optimized Deep Hole Drilling (old)", "DdaX5",  "Drilling",    "hole",    "",             "",       0.0),
    ("Back Boring",                        "DbborX5","Drilling",    "hand",    "",             "",       0.0),
    ("Helical Thread Drilling/Milling",    "DhtmX5", "Drilling",    "hole",    "",             "",       0.0),
    ("Circular Pocket",                    "DcpX5",  "Drilling",    "hole",    "",             "",       0.0),
    ("Gun Drilling",                       "DcdX5",  "Drilling",    "hand",    "",             "",       0.0),
    ("5X Helical Drilling",                "DsdX5",  "Drilling",    "hole",    "",             "",       0.0),
    ("Hole Brushing",                      "DbrsX5", "Drilling",    "hand",    "",             "",       0.0),
]
OPS = {n: dict(name=n, code=c, group=g, rule=r, usage=u, shape=s, dia=d) for n, c, g, r, u, s, d in _T}

# hole operations: which hole_jobs operation picks the tool
HOLE_OP = {"Centering": "Centering", "Drill": "Drill", "Chip Break Drill": "Drill", "Peck Drill": "Peck Drill", "Reaming": "Reaming",
           "Tapping": "Tapping", "Boring": "Boring", "Helical Drilling": "Helical Drilling", "Thread Milling": "Thread Milling",
           "Optimized Deep Hole Drilling": "Peck Drill", "Optimized Deep Hole Drilling (old)": "Peck Drill",
           "Helical Thread Drilling/Milling": "Thread Milling", "Circular Pocket": "Helical Drilling", "5X Helical Drilling": "Helical Drilling"}

# hyperMILL's own cycle and job names -> operation (job names made by part_wizard_1 contain these; longest match wins)
NAMES = {"Face Milling": "Face Mill", "Contour Milling": "Contour Finish", "Pocket Milling": "Pocket HEM", "Plunge Milling": "Plunge Milling",
         "Chamfer Milling on 3D Model": "Chamfer on 3D Model", "3D Optimized Roughing": "Rough HEM",
         "3D Optimized Roughing Traditional": "Rough Traditional", "3D Plunge Roughing": "3D Plunge Roughing",
         "3D Automatic Rest Machining": "Automatic Rest Machining", "3D Plane Machining": "Plane Finish",
         "3D Z Level Shape Finishing": "Z Level Shape Finish", "3D Profile Finishing": "3D Profile Finish Ball",
         "5X Swarf Cutting one Curve": "Swarf Curve", "Centering": "Centering", "Simple Drilling": "Drill",
         "Drilling with Chip Break": "Chip Break Drill", "Drilling with Pecking": "Peck Drill", "Reaming": "Reaming", "Tapping": "Tapping",
         "Boring": "Boring", "Helical Drilling": "Helical Drilling", "Thread Milling": "Thread Milling",
         "Rest Machining": "2D Rest Machining", "Optimized deep Hole Drilling": "Optimized Deep Hole Drilling",
         "Optimized deep hole drilling(old)": "Optimized Deep Hole Drilling (old)"}
for _n in OPS:
    NAMES.setdefault(_n, _n)
# names hyperMILL prints for the types whose operation name differs from the menu name
_MENU = {"5X Profile Finishing (new)": "5X Profile Finishing", "5X Profile Finishing (old)": "5X Profile Finishing (old)"}
NAMES.update(_MENU)

def op_from_name(text):
    """Operation from a job or cycle name, or None. The longest matching name wins ('5X Helical Drilling' before 'Helical Drilling')."""
    t = str(text or "").lower()
    best = None
    for k, op in NAMES.items():
        if k.lower() in t and (best is None or len(k) > len(best[0])):
            best = (k, op)
    return best[1] if best else None

def picker_labels():
    """'group | operation' labels for the add-a-toolpath picker, operations with saved settings first in each group."""
    order = ["2D", "3D", "5X", "Drilling"]
    return ["%s | %s" % (OPS[n]["group"], n) for g in order for n in OPS if OPS[n]["group"] == g]
