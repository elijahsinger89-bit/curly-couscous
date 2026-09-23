# D3 - ENCLOSURE LAYOUT SHEETS

**Where each device physically sits: rails, ducts, faces, penetrations and gland
positions.**

| | |
|---|---|
| Document | **D3**, per document-plan.md section 1.2 |
| Owner | **MAIN-PANEL** for the main panel's sheets. PUMP-BOXES and DISPLAY-BOX own their own boxes' sheets and none is written |
| Issue | 1, 2026-09-23 |
| Read by | The builder, before building the panel |
| Read when | With D1 and D2, before building starts. D5 and D4 are generated from D2, D3 and D6 |
| Split | **D-208.** An enclosure layout sheet has two independent halves. **The interior sheets, 3.1 to 3.7, are produced here. The wall-position sheet, 3.8, is empty with its blocker named** |

## HOW TO READ THIS DOCUMENT

**D3 carries GEOMETRY. Device identity comes from D2** - document-plan.md section
3.2, and the 1st Edition's own defect is the reason: its plate sheet carried a device
label that was typed rather than computed, and it was wrong. **Every device name
below is D2's.**

**What is deliberately not here:** any conductor fact, which is D5's; any jacket,
terminal or landing, which is D6's; **any quantity, count, total or price, which is
D7's and appears in no drawing sheet in this set**; and any reasoning, which is the
tree's.

**Counts follow G-46.** A cell that can NEVER be filled is marked **n/a with its
reason** and counted separately from one that is merely **empty with its blocker**.
Section 4 collects both.

**Every spacing below obeys G-52.** Any fastener spacing that assumes the part is
stationary has ignored the tool. **Across-corners is about 1.15x flats and that is
what collides first when a nut rotates.** Where no figure exists, the spacing is
named as a lookup rather than stated.

---

## SHEET 3.1. THE ENCLOSURE, AND ITS ORIENTATION

**Qilipsu, already owned. Overall 508 x 419 x 201 mm. Mounting plate 468 x 379 mm,
4.5 mm thick, PC/ABS. Box polycarbonate.** D-199 and D-195.

**The enclosure study is CLOSED and no other box is specified.** D-196's 16 x 14
verdict is withdrawn. Nothing below re-derives it.

### Orientation: PORTRAIT, per G-51

**G-51 is frozen: portrait, not landscape, on every box.** So:

| | mm | in |
|---|---|---|
| Box width | **419** | 16.50 |
| Box height | **508** | 20.00 |
| Box depth | **201** | 7.91 |
| **Plate width** | **379** | 14.92 |
| **Plate height** | **468** | 18.43 |

**The bottom face, which carries every grip, is 419 x 201 mm.** The top face, which
carries the five 22 mm devices, is the same.

**This differs from D-199's own arithmetic and the difference is reported in section
5, not resolved here.** D-199 works the plate as 468 wide by 379 high, which is
landscape, and its "814 mm across two rails at 407 usable" is only possible at a
468 mm width. **The sheet does not depend on which is right: the demand clears in
both, and portrait clears it four times over.** Section 3.2 gives both.

---

## SHEET 3.2. THE PLATE: BANDS AND RAILS

### 3.2.1 The one dimension that sets everything

**The NDR-240-24 is VERTICAL MOUNTING ONLY, AC in at the bottom and DC out at the
top, and any other orientation voids the cooling figures.** 63 x 125.2 x 113.5 mm,
with 40 mm above, 20 mm below, 5 mm each side, and 15 mm from another heat source.

**Vertical budget at full load: 185 mm.** That is a clearance and G-51 does not spend
a clearance.

### 3.2.2 Band heights

| Band | Height | Source |
|---|---|---|
| Supply band | **185 mm** | 125.2 + 40 above + 20 below |
| Relay band | **71 mm** | 94.74SMA socket + 55.34 + 094.71 metal clip = 70.5, rounded for cover clearance |
| Terminal band | **70 mm** | The corrected envelope. **McMaster's 70 mm is overall height INCLUDING the DIN clip, which is not height above the rail** - 44 mm above rail, 56 mm off the rail face |
| Contactor, if on its own band | 88.8 mm | Finder 22.32 height above rail |

### 3.2.3 Four bands, and where the slack is

| Band | Contents | Height |
|---|---|---|
| **B1**, lowest | Supply, LINE protection, KM-CHIL, LINE terminals | **185 mm** |
| **B2** | Six relay envelopes and KM-DRV | **71 mm** |
| **B3** | 24 V terminals | **70 mm** |
| **B4**, highest | SENSE terminals, the five burdens, lamp pairs | **70 mm** |
| | **Used** | **396 mm** |
| | **Plate height** | **468 mm** |
| | **Slack, for horizontal ducts and edge margins** | **72 mm** |

**B1 is the lowest band deliberately and the NDR's own terminals are the reason: AC
in at its bottom faces the LINE grips directly below it, DC out at its top faces the
24 V bands above it.** The supply's position is not a preference - main-panel-poles.md
already ruled the supply low, because a duct above a heat source is better than a
relay above one, and the band's own 40 mm is the clearance that enforces it.

**The band order is D-072's duty tiers rendered as geometry: arcing loads at the
bottom, coil switching in the middle, quiet at the top.** It is not a new rule.

### 3.2.4 Rail available against rail demand

Two vertical wireways at the sides, one per class group. **Their width is EMPTY with
its blocker - section 3.4 - so the table below runs at each catalog size.**

| Duct pair | Rail per band | B1 rail, less the NDR's 73 mm | **Total rail** |
|---|---|---|---|
| 2 x 25 mm | 329 | 256 | **1243 mm** |
| 2 x 40 mm | 299 | 226 | **1123 mm** |
| 2 x 60 mm | 259 | 186 | **963 mm** |

**Demand:**

| Item | Each | Count | Total |
|---|---|---|---|
| Relay envelopes, 94.74SMA with 55.34 | 30 mm | 6 | **180.0** |
| KM-DRV, Finder 22.32 | 17.5 mm | 1 | **17.5** |
| BUS-A overcurrent | 17.5 mm | 1 | **17.5** |
| BUS-B overcurrent | 17.5 mm | 1 | **17.5** |
| R-PI fuse holder | 6.2 mm | 1 | **6.2** |
| KM-CHIL, motor-rated contactor | 45 mm | 1 | **45.0** |
| Disconnect | **0 mm** | **n/a** | **0** |
| Terminal ways | 6.2 mm | **58** | **359.6** |
| End plates, three banks | 2 mm | 3 | **6.0** |
| | | **TOTAL** | **649.3 mm** |

**649.3 against 1243. Fifty-two percent used at 25 mm ducts, and it still clears at
60 mm ducts.** The spare takes K-PERM-P at +30 mm if K-PERM splits, the five burdens,
and the 59th terminal way if the leak console uses three legs rather than two.

**Cross-check in D-199's landscape:** 814 mm less the NDR's 73 is 741 mm of rail
against 649.3. **It clears by 92 mm, at 88 percent used, with no room for K-PERM-P or
the burdens.** Portrait is not only compliant with G-51, it is the arrangement that
leaves margin.

### 3.2.5 The demand figure corrects D-199's, and the verdict is unaffected

**D-199 states 584.2 mm. The supportable figure is 649.3 mm.** D-199 computes
568 - 70 + 86.2, treating a 70 mm placeholder as though it were inside the 568.
**It was not: the plate-area study listed the four unchosen devices under "not in the
total".** The correct operation is 568.4, less 17.5 because KM-CHIL ceased to be a
22.32, plus 86.2 for the five devices, plus the terminal count moving from 57 ways to
58 and three banks of end plates.

**Reported rather than hidden because the conclusion is untouched: 649.3 clears
1243 mm as comfortably as 584.2 did, and it clears the landscape figure too.**

---

## SHEET 3.3. RAIL POSITIONS AND WHAT SITS AT EACH

**One rule governs every position along a rail, and it is main-panel-poles.md's:
power envelopes at the LINE-duct end, quiet envelopes at the signal-duct end, so no
conductor crosses the plate to reach its own class's duct.**

### B1. The supply and LINE band. Rail usable 256 mm beside the NDR.

| Position | Device | Rail | Note |
|---|---|---|---|
| 1 | **NDR-240-24** | **73** | **63 mm body plus 5 mm each side. CORRECTED 2026-09-23, F-127: this cell read "63 mm + 5 mm each side = 73", which is an EXPRESSION where every other cell in this column is a FIGURE, and a reader taking the first number gets 63 against an occupancy of 73.** **AC terminals DOWN, DC terminals UP. Vertical only.** 40 mm clear above to B2's rail, 20 mm clear below, 15 mm from any other heat source |
| 2 | **BUS-A overcurrent** | 17.5 | Protects the supply primary, FV-1 and the transfer, manifold and R-PI feeds |
| 3 | **BUS-B overcurrent** | 17.5 | The dedicated chiller circuit |
| 4 | **R-PI fuse holder** | 6.2 | Indicating type. **The lamp sits across the fuse, not in series with the load** |
| 5 | **KM-CHIL** | 45 | **POSITION ONLY, NOT A PART ON THIS SHEET.** See below |
| 6 | **LINE terminal bank**, 16 to 17 ways | 99.2 to 105.4 | RUN-010, RUN-011, RUN-015 and the four receptacle feeds |
| | **Used** | **195.6 to 201.8 of 256** | |

**KM-CHIL gets a position and a note.** The device is specified in parts.md and
**stays BLOCKED on the rung that decides which bus its coil hangs on**, which decides
whether the Pi can stop the water system. **Rule 9: nothing is built against it.** Its
45 mm is held; its depth off the rail is EMPTY.

**The disconnect has no position and never will have one.** D-200: a lockable 2-pole
building breaker upstream satisfies the requirement, so this is **n/a, not a vacancy**.

### B2. The relay band. Rail usable 329 mm.

**Ordered power-end to quiet-end, so that the three power envelopes' LINE conductors
reach the LINE duct without crossing the plate.**

| Position | Device | Rail | Duty |
|---|---|---|---|
| 1 | **K-FILL-S** | 30 | power |
| 2 | **K-FILL-D-P** | 30 | power |
| 3 | **K-DRY-P** | 30 | power |
| 4 | **KM-DRV** | 17.5 | **24 V voltage class, ARC duty.** D-150's own case |
| 5 | **K-PERM** | 30 | quiet |
| 6 | **K-FILL-D-Q** | 30 | quiet |
| 7 | **K-DRY-Q** | 30 | quiet |
| | **Used** | **197.5 of 329** | Spare 131.5 |

**Suppression adds nothing here.** The 94.74SMA ships with the 094.71 metal clip and
its coil-side slot takes the 99.01 module; **both fit, neither is sacrificed, and the
module sits inside the socket envelope so it adds no height and no rail.** Not a
99.02, which is the box-clamp family. The plastic 094.91.3 clip is instead of the
metal one, not in addition.

**K-PERM-P, if K-PERM splits, takes position 8 at +30 mm.** Held in the spare.

**KM-DRV's 9 mm inter-device air gap does not apply: n/a.** It is required only above
40 C ambient with contacts over 20 A, and the room runs 62 to 65 F.

### B3. The 24 V terminal band. Rail usable 329 mm.

| Group | Ways | Rail | Runs |
|---|---|---|---|
| Motor supply out | 4 | 24.8 | RUN-001, RUN-002 |
| Permissive coil drive | 2 | 12.4 | RUN-005 |
| **Day tank floats** | 8 | 49.6 | RUN-012. **Both conductors of every float come home; no series link in the wet zone** |
| **Storage floats** | 8 | 49.6 | RUN-013 |
| E-STOP | 2 | 12.4 | Top face |
| RESET, three blocks | 6 | 37.2 | Top face |
| End plates | | 2.0 | |
| | **30 ways** | **188.0 of 329** | |

**Every float terminal is SINGLE-TIER.** D-190 removed double-decks everywhere, and
the float chain is the reason: **every terminal in a series interlock chain sits at a
different point of the chain, so a tier slip bypasses the elements between them and
makes a float permanently MADE** - the precise inverse of D-154's fail-safe topology.

### B4. The quiet band. Rail usable 329 mm.

| Group | Ways | Rail |
|---|---|---|
| S-08 readback | 2 | 12.4 |
| S-03 and the D-042 inhibit, one changeover pair | 2 | 12.4 |
| S-20 and its complement, one changeover pair | 2 | 12.4 |
| PL-R, PL-G, PL-Y | 6 | 37.2 |
| **The five sense-circuit burdens** | 5 carriers | 31.0 |
| End plates | | 2.0 |
| | **12 ways + 5 carriers** | **107.4 of 329** |

**The five burdens get a home on this sheet for the first time.** parts.md puts the
burden for S-08 and S-03 in the main panel and no file has ever said what holds them.
**They sit in the quiet band because that is where the circuits they belong to land**,
and the carrier type is EMPTY with its blocker.

**RUN-007 and RUN-008 each carry a G-27 complementary pair from one changeover pole.
Neither pair may be split across terminal groups.**

---

## SHEET 3.4. THE DUCTS

### 3.4.1 Two vertical wireways, full plate height, one per class group

| Duct | Carries | Population |
|---|---|---|
| **LINE duct** | The 120 V system | **Six vertical conductors only.** LINE is concentrated in B1, so the only LINE that climbs is the switched hot to and from three relay poles in B2 - K-FILL-S's solenoid pole, K-FILL-D-P's transfer pole and K-DRY-P's manifold pole, two conductors each |
| **24 V and signal duct** | The 24 V system and every sense circuit | **The busy one.** It runs B1 to B4: the coil bus up from the supply, the permissive string, both float chains, all five sense circuits and their burdens, and the three lamp pairs |

**Putting the LINE terminals in B1, directly above the LINE grips, is what makes the
LINE duct nearly empty.** That is a consequence of the band order rather than a
separate decision, and it is the cheapest thing on this sheet.

**Horizontal ducts, if fitted, come out of the 72 mm of slack in section 3.2.3.**

### 3.4.2 Fill. EMPTY, with two blockers named.

**The limit is 50 percent of interior cross-section, NFPA 79 section 13.5.2, not
NEC.** Knock nominal W x H down to about 90 percent for wall thickness, then fill
50 percent of that. Catalog shortcut: **N = (W x H) / (1.75 x D squared)**.

**Shop practice designs to 30 to 40 percent so the cover still snaps on. The LIMIT is
50 and this sheet does not design to a limit.**

**Two things block the fill figure and only one is a lookup:**

1. **D, the conductor outside diameter.** No wire gauge has been chosen anywhere in
   the tree. Searched parts.md, order.md, D2, D5 and D6: **D5 has no gauge column by
   design.**
2. **The panel-internal conductor list.** wiring-schedule.md section 7 states that
   every conductor internal to this panel is unwritten and is MAIN-PANEL's to fill.
   **The duct population above is a class description, not a count**, except the LINE
   duct's six.

**Available widths, so the choice is bounded: 25, 40, 60, 80, 100, 150 mm, or 0.5,
0.75, 1, 1.5, 2, 2.5, 3, 4 and 6 in.** Section 3.2.4 shows the rail budget clears at
every size up to 60 mm.

---

## SHEET 3.5. THE BOTTOM FACE: FIFTEEN GRIPS IN TWO ROWS

**Face: 419 x 201 mm - 16.50 x 7.91 in.** Every cord grip is on this face and nothing
else penetrates it. Owner-given, parts.md.

### 3.5.1 The count is fifteen, not eleven

**Lookup 11 raised it.** A standard 15 A duplex does not panel-mount; the build uses
Bell 5320-0 weatherproof device boxes with TayMac covers, **on the wall beside the
panel, fed by cord grips.** So RUN-018, RUN-019 and RUN-020 stop being face entries
and become grips, and R-PI's feed is a fourth.

**What that frees inside the box: nothing off the plate, because receptacles were
never on the plate.** It frees a face, the interior depth behind it, and
main-panel-buy.md's objection that gasketing five top-face holes while leaving open
receptacles in another face buys a rating the box does not have. **With no receptacle
in any face, the box's worst penetration is the top-face devices and the grips, which
is what D-110 and F-088 already address.**

### 3.5.2 Two rows is REQUIRED, and the separation is why

| Arrangement | Pitches | Span at 1.10 in | Against 419 mm |
|---|---|---|---|
| One row of 15, no separation gap | 14 | 16.26 in = **413 mm** | fits by 6 mm |
| **One row of 15 with the SEG-A gap** | 15 | 17.36 in = **441 mm** | **DOES NOT FIT** |
| **Two rows, 8 and 7** | 7 and 6 | **8.56 in = 217 mm** and 7.46 in = 190 mm | **fits, with 202 mm spare** |

**So one row fails only when the segregation gap is included, and G-51 forbids
spending a separation to make a box fit.** Two rows is the answer and the separation
is the reason, not the count.

**G-52 on the pitch: the floor is not the flat width.** 3/8 flats are 0.75 in and 1/2
are 0.95 to 0.98; across-corners is about 1.15x, so half a nut at each end of a row is
0.43 in for 3/8 and 0.56 in for 1/2. **Use 1.10 in C-C for 3/8, 1.30 in for 1/2, and
1.15 to 1.20 in for a mixed pair. Row-to-row C-C is the same rule in the other axis**,
and 201 mm of face depth carries it with room.

### 3.5.3 The rows ARE the segregation, and the split falls out as 8 and 7

**Not a number halved. The classes count 7 and 8 by themselves.**

**ROW A, at the FRONT of the face, seven grips, all SEG-A:**

| Order | Run | What |
|---|---|---|
| 1 | **RUN-010** | Building branch circuit in |
| 2 | **RUN-011** | FV-1 fill solenoid |
| 3 | R-XFER feed | Transfer pump device box |
| 4 | R-MAN feed | Manifold pump device box |
| 5 | R-CHIL feed | Chiller and loop pump device box |
| 6 | R-PI feed | Pi brick device box |
| 7 | **RUN-015** | Leak console. **LINE-rated on every conductor, CBL-06** |

**ROW B, at the BACK nearest the plate, eight grips, everything else:**

| Order | Run | Class and duty |
|---|---|---|
| 1 | **RUN-001** | 24 V, ARC |
| 2 | **RUN-002** | 24 V, ARC |
| 3 | **RUN-012** | 24 V, COIL. Day tank floats |
| 4 | **RUN-013** | 24 V, COIL. Storage floats |
| 5 | **RUN-005** | 24 V, COIL. Permissive coil drive |
| 6 | **RUN-007** | 24 V, SENSE |
| 7 | **RUN-008** | 24 V, SENSE |
| 8 | **RUN-006** | 24 V, SENSE. Readback |

**Three constraints, all satisfied by that order:**

- **F-029: RUN-005 and RUN-006 are provably non-adjacent at this end as well as at
  the display box**, separated by RUN-007 and RUN-008. A short between them would make
  the readback follow the command, which is precisely and only the failure G-09 exists
  to detect.
- **RUN-007 and RUN-008 hold that gap and neither may be moved out of it.**
- **SEG-A is a whole row away from the sense entries**, which is D-049's short case
  answered by the wiring plan rather than by circuit design.

**Row B is the back row because its cables rise to B2, B3 and B4 and the back row
rises straight up the plate face. Row A is the front row because LINE terminates in
B1, directly above it, and has the shortest rise in the box.**

**Which face and the ORDER on it are MAIN-PANEL's under D-146. WHERE on the face and
the spacing are INTERCONNECT's**, so the X positions above are EMPTY and the order is
not.

---

## SHEET 3.6. THE DOOR: FIVE 22 mm DEVICES

**MOVED FROM THE TOP FACE TO THE DOOR 2026-09-23 BY THE OWNER, D-232, ON F-122. The
top face now carries NOTHING and has no penetration of any kind.**

**The reason, and it is the owner's: an E-stop that requires an overhead reach is not an
E-stop.** At the 1829 mm sightline both offered placements put the top face at or above
eye level, **and D3 itself placed the E-stop "so a struck palm lands on nothing else",
which is a statement that this device is struck with a palm. A palm strike is a
chest-height action.**

**And the second reason, which is not ergonomic: the top face is the upward-facing
penetration that sets the assembly's rating regardless of what is gasketed on it. Five
gasketed devices on a horizontal face is a rating bought and then spent on the one
surface that collects standing water.**

**D-047's reasoning was about sealing. THE CONSEQUENCE WAS OPERABILITY, AND THE
CONSEQUENCE WAS NEVER WEIGHED AGAINST IT.**

### 3.6.1 What this move does NOT change

**The device order and every reason for it, unaltered.** It is stated left to right as
the operator faces the panel, which is a datum statement and not a description, **and
that sentence is as true of a door as of a roof.**

**ORDER REVERSED 2026-09-23, D-234, when the hinge was answered. See 3.6.7: every reason
below is a positional relation and none names an end, so the reversal changes no reason.**

| Position | Device | Why here |
|---|---|---|
| 1, **HINGE end** | **RESET** | **At the opposite end from E-STOP**, so a person clearing a trip cannot strike the E-stop while reaching for it. **And it is the deepest body, now at the smallest arc** |
| 2 | **PL-G**, filling | |
| 3 | **PL-Y**, healthy | |
| 4 | **PL-R**, permissive lost | Adjacent to E-STOP, because E-STOP is what causes it. **Reading the two together is the diagnosis** |
| 5, **LATCH end** | **E-STOP** | At one end, so a struck palm lands on nothing else |

**And nothing in D4, D5 or D6 changes. The five devices' conductors land where they
landed. Only the face they pass through moves.** Zero rows, zero joints, zero runs.

### 3.6.2 Depth behind the face. UNCHANGED AS A FIGURE, INVERTED AS A PROBLEM

Schneider XB5A with ZBE screw blocks, measured from the front face with the gasket
compressed:

| Rows of blocks | Depth |
|---|---|
| 1 | **43 mm** |
| 2 | 55 mm |
| 3 | **68 mm** |

**A DOUBLE BLOCK IS TWO ROWS. Side-by-side blocks add no depth - only stacked rows do.**

**RESET needs at least two NO blocks** - one to latch K-PERM, one to re-arm K-DRY, which
is a MAKE and not a break because D-154 settled that K-DRY energised is the permitted
state - **and a third if it proves the lamps.** Three blocks SIDE BY SIDE is one row at
43 mm. **Plan 68 mm only if three ROWS turn out to be necessary.**

### 3.6.3 THE COLLISION HAS INVERTED, AND THIS IS THE ONE REAL COST OF THE MOVE

**On the top face the bodies hung DOWN from the roof into the door-side volume, which
was empty**, and the old 3.6.3 bought that clearance by choosing where along the depth
axis to drill: *"the clearance is bought by where the hole goes, not by moving a rail."*

**ON THE DOOR THE BODIES HANG BACKWARD, TOWARD THE PLATE.** The door-side volume stops
being empty because the devices are now in it, **and what they point at is B1 to B4 -
the supply, the contactors, the relays and the terminals.**

**The clearance can no longer be bought by choosing a hole position, because every hole
on the door points the same way.**

| | |
|---|---|
| Box depth, overall | **201 mm** |
| Deepest device body | **68 mm** at three rows, 43 mm at one |
| **Clear depth, closed door's inner face to the plate's front surface** | **EMPTY. Not on file.** Owner is measuring it with the mounting holes, 2026-09-23 |
| **Then the question** | Whether the deepest device body clears the tallest device on the plate **in the band it lands over**, which is B1's supply and contactors at the bottom and B4's terminals at the top |

**AND ONE THING THE MOVE BUYS BACK: the door opens, so the bodies swing with it.**
Nothing behind them has to be reachable past them. **A device on a door is easier to
service than one hanging from a roof, not harder.**

### 3.6.4 Hole spacing. EMPTY, with its blocker, and its face has changed

**508 x 419 mm of door, against 419 x 201 of top face.** The five holes now sit on the
LONG axis of a larger face, **so the spacing constraint is looser than it was and the
BLOCKER IS THE SAME ONE.**

**The C-C FLOOR is not stated and must not be assumed.** Lookup 10 returned depth only.
**G-52 governs it: the floor is the bezel and the rear collar at across-corners while a
collar nut is being turned, not the 22 mm bore.**

**AND THE USABLE DOOR AREA IS NOT 508 x 419.** A gasketed door has a sealing perimeter
and usually a stiffening rib inset from it, **and no figure for either is on file.** It
is the same measurement as the door-to-plate depth and is taken in the same minute.

### 3.6.5 G-52 ARRIVES ON THE HINGE, AND IT IS NEW

**A device body near the HINGE sweeps a smaller arc than one near the LATCH. Spacing
that assumes the door is stationary has ignored the swing.**

**This did not exist on the top face and it is not a spacing rule - it is a CLEARANCE
rule against whatever the door sweeps past**: the enclosure's own frame, and anything
mounted on the wall beside the panel.

**ANSWERED 2026-09-23, see 3.6.7. HINGED ON THE LEFT AS THE OPERATOR FACES IT.** The
clearance question against the frame and against anything on the wall beside the panel
**stays open and is what the door-to-plate and usable-area measurements feed.**

### 3.6.7 THE HINGE IS ANSWERED, AND THE DEVICE ORDER REVERSES. D-234

**Owner, 2026-09-23, without a tape: THE DOOR IS HINGED ON THE LEFT AS HE FACES IT, so
the latch is on the right, and THE E-STOP GOES AT THE LATCH END.**

**He asked for this to be CONFIRMED against the order rather than adopted, because the
order was written for a different face. CONFIRMED, AND THE ORDER REVERSES.**

**Every reason in 3.6.1 is a POSITIONAL RELATION AND NOT AN ABSOLUTE END:**

| The reason as written | Does it name an end? |
|---|---|
| E-STOP "at one end, so a struck palm lands on nothing else" | **No. AN end** |
| PL-R "adjacent to E-STOP, because E-STOP is what causes it" | **No. Relative to E-STOP** |
| RESET "at the opposite end from E-STOP" | **No. Opposite to E-STOP** |

**So reversing the whole row satisfies all three unchanged.**

    RESET   PL-G   PL-Y   PL-R   E-STOP
    hinge ...................... latch

**AND THE REVERSAL BUYS SOMETHING NOBODY DESIGNED FOR. RESET IS THE DEEPEST BODY** - at
least two NO blocks and a third if it proves the lamps, 55 to 68 mm, against E-STOP's one
row at 43 mm - **and the reversal lands it at the HINGE, which is the SMALLEST ARC. The
deepest body gets the least swing, for free.**

**ONE THING THAT IS NOT A REASON, AND IT IS THE OWNER'S OWN: "the arc is largest and a
palm strike lands squarely" does not decide it.** The door is CLOSED when anybody strikes
the E-stop, **so both ends strike equally.** The arc bears on clearance while swinging,
not on the strike. **The ruling is right and the stated reason is not the one that
carries it; the real one is the RESET depth above.**

**AND ONE OBJECTION, RAISED AND ANSWERED SO NOBODY RE-RAISES IT: an E-stop at the latch
end travels furthest when the door opens and is the most likely of the five to be knocked
by the door swinging into something. THAT RESOLVES IN THE SAFE DIRECTION** - a knocked
E-stop stops the machine - **so it is not an objection.**

**Consequence for D5 section 5.1: the flexing loop lives on the HINGE side, so E-STOP's
conductors now cross the full door width to reach their clamp. A length, not a problem,
and the longest of the five.**

### 3.6.6 The top face, now

**SOLID. No penetration, no device, no gasket, no blank.**

**D-047 is SUPERSEDED rather than reversed, D-232: the top face stops carrying devices,
so there is nothing on it to gasket.** The decision was right about sealing and is now
moot rather than wrong.

**AND F-025's TOP-FACE HALF CLOSES.** It was live: *"the requirement for each 22 mm
device's rating IN THAT ORIENTATION is still live."* **A device on a vertical door has
no upward orientation to be rated in.** One open item goes away and it was not counted
as a benefit until the move was costed.

---

## SHEET 3.7. THE GROUND BARS

**Two McMaster 2450K14: tin-plated copper blocks, 5.75 x 0.50 x 0.50 in - 146.05 x
12.7 x 12.7 mm - twelve 1/4-28 tapped holes each, 14 to 6 AWG. NO INSULATORS AND NO
MOUNTING HARDWARE.**

### 3.7.1 Placement

**Not a rail item. It bolts to the plate.** So it competes for plate area rather than
for rail length.

**Side by side, below B1, in the 72 mm of vertical slack** - the lowest point on the
plate, nearest the grips through which every grounding conductor arrives.

**Insulators: n/a.** The plate is PC/ABS and the box is polycarbonate, so **a bare
copper block bolted flat to this plate bonds to nothing.** D-195, F-118.

**Through-drilling: holes at least 127 mm - 5.0 in - apart, or the drill meets the
taps.** Two bars is four plate holes.

### 3.7.2 Capacity

**Twenty-four landings. Twelve used. Twelve spare.**

| # | What lands | Count |
|---|---|---|
| 1-2 | Pump box A and pump box B local bars, daisied home | 2 |
| 3-6 | **The display box local bar, four times** - one grounding conductor per jacket, four jackets | 4 |
| 7 | The building branch circuit's equipment ground | 1 |
| 8 | FV-1's ground | 1 |
| 9-12 | The four receptacle device boxes' grounds, arriving through their feed grips | 4 |
| 13 | The leak console's EGC, **if it needs one** | EMPTY |
| - | **The enclosure's own bonding** | **n/a. Nothing in this box is metal** |

### 3.7.3 The five steps, per G-49

**One action each, with an acceptance condition observable at that moment.**

1. **Drill the two plate holes for ground bar 1**, centres at least 127 mm apart.
   *Accept:* offer the bar up to the plate and confirm each hole lines up with clear
   material, not with a tapped hole.
2. **Fit ground bar 1 to the plate.** *Accept:* the bar does not rock when pressed at
   either end.
3. **Fit ground bar 2 to the plate, beside bar 1.** *Accept:* as step 2, and a driver
   reaches every tapped hole on both bars without fouling the other bar.
4. **Fit the inter-bar jumper between bar 1 and bar 2.** *Accept:* **C-25** - a meter
   reads continuity across the jumper.
5. **Confirm both bars are otherwise empty before any conductor lands.** *Accept:*
   twenty-four tapped holes are empty except the jumper's two.

**The jumper is fitted FIRST and it is NOT a landing.** D-192: it is never removed to
free a way and nothing else shares its holes. **If it is treated as a landing somebody
eventually removes it, and at that moment half the equipment grounds in the build are
floating with everything still looking correctly built.**

**The bars are NEVER split by class.** Two bars bonded together are one ground point;
putting 24 V grounds on one and 120 V on the other is the single-point rule defeated
by tidiness.

---

## SHEET 3.8. THE WALL POSITION. EMPTY.

**This sheet states where the enclosure sits on the wall: the mounting-hole
coordinates a person drills, the outline extent that collides, and the approach
direction of every run.**

**IT IS EMPTY AND IT IS BLOCKED ON M-02.**

| | |
|---|---|
| Blocker | **M-02**, OPEN. DOSING's manifold and PUMP-BOXES both claim wall space and the tubing between them sets the spacing. DOSING and PUMP-BOXES jointly, INTERCONNECT arbitrates |
| Why nothing can be stated | **Every value on this sheet is a coordinate from one datum**, and the datum is on a wall whose occupancy is not settled. A coordinate written against a moving layout is worse than a blank one |
| What would fill it | **wall-survey.md**, the form already written: one named physical datum with both axes stated, then per item the named feature, its X and Y, and the item's extent from that feature |
| What it blocks in turn | Every RUN- cut length, which is the wall run plus 3 ft under D-090. **A relationship cannot be cut from** |

**This sheet being empty does not block sheets 3.1 to 3.7.** D-208: an enclosure
layout sheet has two independent halves and the interior needs no survey at all. **A
document half of which is blocked is not a blocked document.**

**Also empty and not MAIN-PANEL's: the pump box and display box interior sheets.**
D3 covers all four enclosures and each box's owner writes its own. Not blocked -
unwritten, by PUMP-BOXES and DISPLAY-BOX.

---

## 4. THE COUNTS, PER G-46

**Counted separately, because a cell that can never be filled and one that has not
been filled yet are opposite things, and a completion figure that mixes them is
wrong.**

### 4.1 n/a - CAN NEVER BE FILLED. Five.

| # | Cell | Reason |
|---|---|---|
| 1 | **The disconnect's rail position and footprint** | **There is no part.** A lockable 2-pole building breaker upstream satisfies the requirement, D-200. Not a vacancy |
| 2 | **The enclosure's equipment bonding, and its ground-bar way** | **Nothing in this box is metal.** Plate PC/ABS, box polycarbonate, D-195 |
| 3 | **Ground bar insulators** | Same reason. A bare block on a plastic plate bonds to nothing |
| 4 | **KM-DRV's 9 mm inter-device air gap** | The condition never occurs: it applies above 40 C ambient with contacts over 20 A, and the room runs 62 to 65 F |
| 5 | **Suppression module rail millimetres** | The 99.01 sits INSIDE the 94.74SMA envelope beside the 094.71 clip. There is no position to allocate |

### 4.2 EMPTY - NOT YET FILLED. Eight.

| # | Cell | Blocked on | Whose |
|---|---|---|---|
| 1 | **Duct width and fill percentage** | The conductor OD, no gauge chosen anywhere; **and the panel-internal conductor list** | Lookup, and MAIN-PANEL |
| 2 | **Grip thread size per run, 3/8 or 1/2, and therefore the exact C-C** | Cable selection, itself blocked on CBL-01 to CBL-04 | INTERCONNECT |
| 3 | **Grip X positions on the bottom face** | The wall layout. **Order is stated; position is not mine** under D-146 | INTERCONNECT |
| 4 | **22 mm device hole C-C** | A lookup nobody has run. Lookup 10 returned depth only. **G-52: the floor is the collar at across-corners while it turns** | Lookup |
| 5 | **Ground bar mounting hardware, and the gap between the two bars** | A 1/4-28 across-corners figure. **G-52 again: space for a fitting is not space to fit it** | Lookup |
| 6 | **KM-CHIL's coil bus, and its depth off the rail** | The open rung deciding whether its coil hangs on the permissive coil bus or on KM-DRV. **Rule 9** | MAIN-PANEL and the owner |
| 7 | **The leak console's Form C leg count, two or three** | MAIN-PANEL owes it. It moves the terminal count by one way | MAIN-PANEL |
| 8 | **Sheet 3.8, the wall position, entire** | **M-02** | DOSING, PUMP-BOXES, INTERCONNECT |

### 4.3 The terminal count, restated

**58 ways, and it supersedes the plate-area study's 56 to 57.** Two corrections: the
gland-side conductors recount to 36 rather than 34, and the four receptacle feeds are
now field conductors through grips rather than face terminations - the same 8 ways,
on the other side of a gland.

| Band | Group | Ways |
|---|---|---|
| B1 | LINE | **16**, or 17 at three console legs |
| B3 | 24 V | **30** |
| B4 | SENSE | **12** |

**It is still a floor and the floor is now known to be close to final.** The parallel
build carries 129 conductors on 51 terminal footprints using 316 mm of 66 positions.
**Not this build's number and not adopted as one, per G-53 - it says the floor is not
about to double, which is the difference between a margin and a guess.**

---

## 5. TWO THINGS REPORTED, NOT FIXED

**Rule 2: a boundary defect is reported, never fixed.**

### 5.1 The tree holds TWO boxes under one name, and they differ by 109 mm

| Source | Name | Overall | Plate |
|---|---|---|---|
| **parts.md**, lookup 2, the authoritative facts file | **QILISU** | 425 x 340 x 183 | **359 x 271** |
| **D-199** and the instruction for this sheet | **QILIPSU** | 508 x 419 x 201 | **468 x 379** |

**Both are described as the box the owner actually holds. The names differ by one
syllable and the plates differ by 109 mm of length and 108 of width.**

**This sheet is built on D-199's figures, as instructed.** If parts.md's are the real
ones, **every band arithmetic in section 3.2 is wrong and the plate-area study's
verdict returns**: a 359 x 271 plate takes the 185 mm supply band plus two more, not
three, and 649.3 mm of demand against 590 mm of rail does not clear.

**It is one measurement to settle and it should be settled before a hole is drilled.**

### 5.2 D-199's arithmetic is landscape and G-51 is frozen portrait

D-199 works the plate as 468 wide by 379 high and states 814 mm across two rails at
407 usable. **A 407 mm rail is impossible at a 379 mm plate width, so that figure is
landscape.** G-51 is frozen: portrait, not landscape, on every box.

**Nothing is lost by resolving it toward the rule.** Portrait gives 1243 mm of rail
against landscape's 741 and four bands against two, so **the sheet is more comfortable
in the orientation G-51 requires.** This is the second time the arithmetic has
vindicated portrait on a real box rather than costing anything for it.

---

## 6. STATUS

**Stopped part-way.** MAIN-PANEL does not declare itself finished, rule 7.

**Produced: seven interior sheets, 3.1 to 3.7**, covering the enclosure and its
orientation, the plate's bands and rails, every rail position and what sits at it, the
duct runs, fifteen grips in two rows on the bottom face, five devices on the top face,
and the ground bars with their five steps.

**Not produced and named as blocked: sheet 3.8, the wall position, on M-02.**

**Not MAIN-PANEL's:** the pump box and display box interior sheets, which belong to
PUMP-BOXES and DISPLAY-BOX and are unwritten rather than blocked.

**Five cells are n/a with their reasons. Eight are empty with their blockers.** Three
of the eight are lookups, three are other agents' or the owner's, and **two are
MAIN-PANEL's own: the leak console's leg count, and the panel-internal conductor
list.** The second is unblocked, unwritten, and is the only thing left that could move
the demand figure.
