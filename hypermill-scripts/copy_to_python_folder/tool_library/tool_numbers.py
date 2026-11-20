# tool_numbers.py - tool numbering standards and the short tool description. Used by the tool builder, the tool numbering
# script and go_to_machine (docs/hyperMILL_design_notes.md section 1, from ToolNameGenerator.xlsx).
#
# HELLER standard
#   milling  M_[TYPE 2][DIAMETER 4][VARIANT 1][COPY 1]      M_11050010 = bullnose, .500, variant 1, copy 0
#            DIAMETER = thousandths of an inch, 4 digits (0.375 -> 0375, 1.000 -> 1000)
#   turning  T_[TYPE 2][ISO 2][HAND 1][VARIANT 1][COPY 1]   T_10CNR10 = OD rough, CN insert, right hand, variant 1, copy 0
#            ISO = first two letters of the insert designation (CN = CNMG); GR grooving, TH threading, FM form
#   VARIANT 1-9: a different tool with the same type and size (corner radius, reach, holder, coating, rougher / finisher).
#   COPY 0-9: stays 0. Sisters on the control share the name and split on the DUPLO number.
#   On the control: 32 characters max, A-Z 0-9 _, called quoted: T="M_11050010".
#   hyperMILL NC Number = the digits after M_ (11050010). T_ tools: not in the standard; here TYPE + the two ISO letters as
#   01-26 + HAND (R 1, L 2, N 3) + VARIANT + COPY (T_10CNR10 -> 100314110): 9 digits, never equal to an M_ number.
# COMPANY_X standard: the 9-digit company code. Rule not set yet.
import re

STANDARDS = ("HELLER", "COMPANY_X")
STANDARD_READY = {"HELLER": True, "COMPANY_X": False}
NOT_READY = "the Company X numbering rule is not set up yet"

MILL_TYPES = {
    10: "Flat (square) endmill", 11: "Bullnose (corner-radius) endmill", 12: "Ball endmill", 13: "Chamfer mill",
    14: "Engraving / marking", 15: "Taper / draft endmill", 16: "Roughing (corncob)", 17: "Plunge mill",
    20: "Barrel - general", 21: "Barrel - conical", 22: "Barrel - tangent", 23: "Barrel - lens", 24: "Barrel - Form-F / oval",
    30: "T-slot", 31: "Dovetail", 32: "Lollipop / undercut", 33: "Keyseat / Woodruff", 34: "Corner-rounding",
    35: "Form (profile)",
    40: "Face mill (indexable)", 41: "Shell mill", 42: "Hi-feed mill", 43: "Square-shoulder / 90 deg",
    44: "Indexable endmill", 46: "Disc / slot mill", 47: "Plunge mill (indexable)",
    50: "Carbide drill", 51: "HSS / cobalt drill", 52: "Insert drill", 53: "Spot drill", 54: "Center drill",
    55: "Gun / deep-hole drill", 56: "Step drill",
    60: "Reamer", 61: "Bore / fine-bore", 62: "Countersink", 63: "Counterbore", 64: "Back countersink / counterbore",
    70: "Cut tap", 71: "Form tap", 72: "Thread mill", 73: "Helical / multi-thread mill", 74: "Indexable thread mill",
    90: "Spindle probe", 91: "Tool setter", 92: "Deburr tool", 99: "Unclassified / special",
}
TURN_TYPES = {
    10: "OD rough", 11: "OD finish", 12: "OD profiling", 13: "Back-turning", 14: "Shoulder / 90 deg",
    20: "Boring rough", 21: "Boring finish", 22: "Boring profiling", 23: "Back-boring",
    30: "Facing rough", 31: "Facing finish",
    40: "Parting / cutoff", 41: "OD grooving square", 42: "OD grooving profile / form", 43: "Face grooving", 44: "ID grooving",
    50: "Threading OD", 51: "Threading ID", 52: "Threading face / scroll",
    60: "Center drill (turret)", 61: "Drill (turret)", 62: "Reamer (turret)", 63: "Tap (turret)",
    70: "Form tool", 71: "Knurling", 72: "Radius / chamfer form",
    90: "Turret probe", 91: "Tool setter / eye", 99: "Special",
}
HANDS = {"R": 1, "L": 2, "N": 3}
MILL_RE = re.compile(r"^M_(\d{2})(\d{4})([1-9])(\d)$")
TURN_RE = re.compile(r"^T_(\d{2})([A-Z]{2})([RLN])([1-9])(\d)$")


# ---------------- ids and numbers ----------------
def mill_id(type_code, dia_in, variant=1, copy=0):
    """'M_11050010'. dia_in in inch (0.0005 to 9.9995)."""
    t, d = int(type_code), int(round(float(dia_in) * 1000))
    if t not in MILL_TYPES:
        raise ValueError("milling type %s is not in the standard" % type_code)
    if not 0 < d <= 9999:
        raise ValueError("diameter %.4f in does not fit 4 digits of thousandths" % float(dia_in))
    if not (1 <= int(variant) <= 9 and 0 <= int(copy) <= 9):
        raise ValueError("variant must be 1-9 and copy 0-9")
    return "M_%02d%04d%d%d" % (t, d, int(variant), int(copy))


def turn_id(type_code, iso2, hand, variant=1, copy=0):
    """'T_10CNR10'."""
    t, iso, h = int(type_code), str(iso2 or "").upper()[:2], str(hand or "").upper()
    if t not in TURN_TYPES:
        raise ValueError("turning type %s is not in the standard" % type_code)
    if not re.match(r"^[A-Z]{2}$", iso):
        raise ValueError("ISO must be two letters (CN, DN, GR, TH, FM ...)")
    if h not in HANDS:
        raise ValueError("hand must be R, L or N")
    if not (1 <= int(variant) <= 9 and 0 <= int(copy) <= 9):
        raise ValueError("variant must be 1-9 and copy 0-9")
    return "T_%02d%s%s%d%d" % (t, iso, h, int(variant), int(copy))


def parse(tool_id):
    """{'kind': 'M'|'T', 'type', 'dia_in' | 'iso','hand', 'variant', 'copy'} or None when it does not follow HELLER."""
    s = str(tool_id or "").strip()
    m = MILL_RE.match(s)
    if m and int(m.group(1)) in MILL_TYPES and int(m.group(2)) > 0:
        return {"kind": "M", "type": int(m.group(1)), "dia_in": int(m.group(2)) / 1000.0,
                "variant": int(m.group(3)), "copy": int(m.group(4))}
    m = TURN_RE.match(s)
    if m and int(m.group(1)) in TURN_TYPES:
        return {"kind": "T", "type": int(m.group(1)), "iso": m.group(2), "hand": m.group(3),
                "variant": int(m.group(4)), "copy": int(m.group(5))}
    return None


def number_of(tool_id):
    """hyperMILL NC Number for an M_ / T_ id, or None."""
    p = parse(tool_id)
    if p is None:
        return None
    if p["kind"] == "M":
        return int(str(tool_id)[2:])
    a, b = (ord(c) - 64 for c in p["iso"])
    return int("%02d%02d%02d%d%d%d" % (p["type"], a, b, HANDS[p["hand"]], p["variant"], p["copy"]))


def follows(tool_id, standard="HELLER"):
    """(True, '') or (False, reason)."""
    if standard == "COMPANY_X":
        return False, NOT_READY
    s = str(tool_id or "").strip()
    if not s:
        return False, "no ID"
    if len(s) > 32 or not re.match(r"^[A-Z0-9_]+$", s):
        return False, "only A-Z, 0-9 and _ (max 32) are allowed on the control"
    if parse(s) is None:
        return False, "not M_[type][diameter][variant][copy] or T_[type][ISO][hand][variant][copy]"
    return True, ""


def free_variant(make, used):
    """First id make(variant) for variant 1-9 that is not in used (compared upper case), or None."""
    taken = set(str(u).upper() for u in used)
    for v in range(1, 10):
        i = make(v)
        if i.upper() not in taken:
            return i
    return None


# ---------------- type codes ----------------
def workbook_code(kind, data_code, row=None):
    """The standard's milling type code for a tool the builder makes. kind = the builder kind, data_code = the type_code
    column of the catalog table (or hole_tools.TYPE_CODE); 12 of those differ from the workbook (design notes table)."""
    row = row or {}
    c = int(data_code)
    shape = str(row.get("shape") or "").lower()
    if kind in ("endmill", "profilemill") and c in (10, 11, 12, 13, 17, 20):
        return c                                            # flat, bullnose, ball, chamfer, plunge, barrel match
    if kind == "endmill" and c == 14:
        return {"corner rounding": 34, "deburrer": 92, "highfeed": 11}.get(shape, 99)
    if kind == "endmill" and c == 16:
        return 99                                           # routers: no type in the standard
    if kind == "profilemill" or c == 19:
        return 44                                           # inserted ball nose
    if kind == "chamfer":
        return 13                                           # solid and inserted chamfer mills
    if kind == "facemill":
        return {14: 40, 15: 43, 16: 42, 17: 42}.get(c, 40)
    if kind == "slot":                                      # walter_slot.csv: kind column disc / slot / circlip / tslot / chamfer
        return 30 if str(row.get("kind") or shape).lower() == "tslot" else 46
    if kind == "drill":
        return 50
    if kind == "spotdrill":
        return 54 if c == 54 else 53
    if kind == "xdrill":
        return 52
    if kind == "boring":
        return 61
    if kind == "tap":
        return 71 if str(row.get("form") or "").lower().startswith("form") else 70
    if kind == "reamer":
        return 60
    if kind == "threadmill":
        return 72
    return c if c in MILL_TYPES else 99


def type_from_hm(hm_type, dia_in=0.0, corner_r=0.0, cone_angle=None):
    """(code, sure) for an existing hyperMILL milling tool. sure = False: ask (a radius mill can be a face or hi-feed mill
    built as a bullnose end mill; a tap can be a cut or form tap)."""
    t = str(hm_type or "").lower()
    d, r = float(dia_in or 0), float(corner_r or 0)
    if t in ("ballmill",):
        return 12, True
    if t in ("radiusmill", "endmill", "torusmill", "flatmill"):
        if r <= 0.0005:
            return 10, d <= 1.25
        if d and r >= d / 2 - 0.001:
            return 12, True
        return 11, d <= 1.25
    if t in ("driltool", "drill"):
        a = float(cone_angle or 140)
        if a <= 65:
            return 54, True
        if a <= 125:
            return 53, True
        return 50, True
    if t in ("chamferedcutter", "chamfermill", "countersink"):
        return 13, True
    if t == "reamer":
        return 60, True
    if t in ("taptool", "tap"):
        return 70, False
    if t in ("threadmill",):
        return 72, True
    if t in ("tslotcutter",):
        return 30, True
    if t in ("boringbar",):
        return 61, True
    return 99, False


# ---------------- short description (Common Name, tool part) ----------------
ABBR = {10: "EM", 11: "BR", 12: "BN", 13: "CH", 16: "EM", 17: "EM", 34: "CR", 40: "FM", 41: "FM", 42: "HFM", 43: "SQ",
        44: "BN", 46: "SLOT", 30: "TSLOT", 50: "DR", 51: "DR", 52: "DR", 53: "SP", 54: "CD", 60: "RM", 61: "BB",
        70: "TAP", 71: "TAP", 72: "TM", 92: "DEBURR"}


def inch(v, places=3):
    """.750 / 1.500 (no leading zero below 1)."""
    s = ("%." + str(places) + "f") % float(v)
    return s[1:] if s.startswith("0.") else s


def describe(type_code, dia_in, corner_r=None, flutes=None, loc=None, thread=None):
    """Tool part of the Common Name, e.g. '.750 BR R.03 6FL L1.50', 'TAP 1/4-20 UNC', '2.000 FM'."""
    t = int(type_code)
    ab = ABBR.get(t, "TOOL")
    if t in (70, 71, 72) and thread:
        return "%s %s" % (ab, str(thread).strip())
    parts = [inch(dia_in), ab]
    if t == 11 and corner_r:
        parts.append("R" + inch(corner_r, 2 if round(float(corner_r), 2) == round(float(corner_r), 3) else 3))
    if flutes and t in (10, 11, 12, 13, 16, 17, 34):
        parts.append("%dFL" % int(float(flutes)))
    if loc and t in (10, 11, 12, 16, 17, 50, 51, 60):
        parts.append("L" + inch(loc, 2))
    return " ".join(parts)
