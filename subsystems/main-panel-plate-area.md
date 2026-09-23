# MAIN-PANEL: what 16 by 12 actually costs

**Issue 2, 2026-09-23.** Issue 1 returned 2026-09-11 against D-188 and G-51, and owed
eleven lookups. **They are back, in parts.md under "Panel component dimensions",
D-194. This issue runs the arithmetic and gives the verdict.**

**This is arithmetic and a verdict. It is not a layout and it proposes no placement.**

Read: agents.md; G-51, D-188, D-190, D-191, D-192, D-193 and D-194; parts.md in full
including the new section; electrical-schematic.md for the roster; order.md;
cable-and-terminal-schedule.md; wiring-schedule.md; subsystems/entry-faces.md; G-30,
D-072 and F-055 for the duty separation.

**No other file was edited.**

**Issue 1's contradiction is corrected, per D-193: the lookup list was ELEVEN. Issue 1
said nineteen in one place and eleven in another. Eleven was right.**

---

## 1. THE VERDICT, FIRST

**The box the owner already holds is NOT the right size. It is short.**

**Neither is 16 by 12.** The nearest real box to that target - a Hoffman QLINE I
400 x 300, the only thing that approximates it - is short by about 11 mm of rail.
**16 by 12 does not fail by a lot. It fails.**

**The answer is a 16 x 14, panel 374.65 x 327.15 mm.** It is the next standard step in
every family the owner checked - Stahlin, Allied Moulded, Integra and Hoffman all go
14 x 12 x 6, then 16 x 14 x 7 or 8 - and it clears the demand with 190 mm of rail to
spare, which is what the four unchosen devices and the five burdens need.

| Box, portrait per G-51 | Plate, mm | Rail available | Demand | Margin |
|---|---|---|---|---|
| **14 x 12** | 276 x 324 | 379 mm | 568 mm | **-189** |
| **Hoffman QLINE I 400 x 300**, the closest thing to a true 16 x 12 | 260 x 360 | 557 mm | 568 mm | **-11** |
| **QILISU, the box on the shelf** | **271 x 359** | **590 mm** | 568 mm | **+22** |
| **16 x 14** | **327 x 375** | **758 mm** | 568 mm | **+190** |

**The QILISU's +22 mm is not a margin.** The tree's only modular-device reference is
the 22.32 at 17.5 mm of rail. **Four unchosen devices at one module each is about
70 mm, and that alone overruns it three times over** - before the five sense-circuit
burdens, before the two ground bars' plate real estate, and before any wire-bending
space at a rail end.

**And the demand is understated, which makes the verdict stronger rather than weaker.**
353 mm of the 568 is the terminal bank at 57 ways, **and 57 is a floor that excludes
every panel-internal conductor** - wiring-schedule.md section 7 says so in terms.

**One number would change this and nobody has it:** the conductor outside diameter,
which sizes the two vertical wireways. Section 6.

---

## 2. WIDTH: THE GLAND FACE, AND ISSUE 1 WAS WRONG ABOUT IT

**Issue 1 named the bottom face as the binding constraint and said one lookup would
settle it. The lookup came back and the answer is that the face is not binding at
all, on either candidate box.**

**Issue 1's error, stated plainly: I treated the bottom face as a LINE when it is a
RECTANGLE.** The QILISU's bottom face is 340 x 183 mm - 13.39 x 7.20 in - and 183 mm
of depth takes two rows of grips without touching anything. **Issue 1 computed eleven
grips across one row and stopped.**

### 2.1 The gland count is not eleven. It is fifteen.

**Lookup 11 changes the count upward.** A standard 15 A duplex does not panel-mount;
the build uses Bell 5320-0 weatherproof device boxes with TayMac covers, **mounted to
the wall beside the panel and fed by cord grips.**

**So the four receptacle feeds leave the panel through grips instead of terminating at
a face.** RUN-018, RUN-019 and RUN-020 stop being FACE entries and become bottom-face
gland entries, and R-PI's feed to the Pi brick's box becomes a fourth.

**Eleven becomes fifteen.**

### 2.2 The arithmetic, at the C-C figures that came back

**No manufacturer publishes a minimum centre-to-centre, so geometry decides: 1.10 in
for 3/8, 1.30 in for 1/2, 1.15 to 1.20 mixed.** The floor is not the flat width -
across-corners is about 1.15x flats, and **that is what collides first when a nut
rotates**, so the constraint is dynamic rather than static.

Half a nut's across-corners at each end of a row: 3/8 gives 0.75 x 1.15 / 2 = 0.43 in
a side; 1/2 gives 0.97 x 1.15 / 2 = 0.56 in a side.

**Fifteen grips plus one deliberate separation gap is fifteen pitches.**

| Arrangement | Span needed | QILISU face, 13.39 in | 16 x 14 face, 14 in |
|---|---|---|---|
| One row, 15 grips, all 3/8 | 15 x 1.10 + 0.86 = **17.36 in** | **NO** | **NO** |
| One row, all 1/2 | 15 x 1.30 + 1.12 = **20.62 in** | NO | NO |
| **Two rows, 8 and 7, all 3/8** | longer row 8 x 1.10 + 0.86 = **9.66 in** | **YES**, 3.73 in spare | **YES** |
| **Two rows, all 1/2** | 8 x 1.30 + 1.12 = **11.52 in** | **YES**, 1.87 in spare | **YES** |

**Row-to-row spacing is the same C-C rule applied in the other axis: 1.30 in at worst,
against 7.20 in of face depth on the QILISU.** Not close.

### 2.3 So width does not decide it, and the separation still survives

**The three ordering constraints are unchanged and all three are satisfiable in two
rows**: RUN-005 and RUN-006 provably non-adjacent at either end, F-029; RUN-007 and
RUN-008 holding the gap between them and neither split; SEG-A - now RUN-010, RUN-011,
RUN-015 and the four receptacle feeds - not the realistic neighbour of the sense runs.
**Two rows makes that EASIER rather than harder, because a row is a second axis to
separate on.**

**Where the grips sit on the face and at what spacing is INTERCONNECT's under D-146.
The order is MAIN-PANEL's and is still undecided** - entry-faces.md covers CBL-02 and
CBL-03 only, and that has not changed.

**One cost of two rows, stated rather than hidden:** the back row's locknuts need
wrench access with the front row's cables already in place, and the back row's cables
pass the front row inside the box. **That is a build and repair cost, not a
protection**, so G-51 permits spending it. It belongs in D4 as a sequence: land the
back row first.

---

## 3. VERTICAL: THE NDR's 185 mm DECIDES THE PLATE

**Two figures are hard and neither is tradeable.**

**The NDR-240-24 is VERTICAL MOUNTING ONLY, AC in at the bottom and DC out at the top,
and any other orientation voids the cooling figures.** 63 x 125.2 x 113.5 mm, with
40 mm above, 20 mm below, 5 mm each side and 15 mm from another heat source.
**Vertical budget at full load: 185 mm.** That is a clearance, and G-51 says a
clearance is not spent.

**The terminal block figure has a trap in it and the owner caught it.** McMaster's
70 mm is **overall height including the DIN clip, which is not height above the rail.**
Equivalent parts at the same pitch give 44 mm above the rail and 56 mm off the rail
face. **Use 6.2 mm per way, 70 mm vertical envelope, 56 mm depth.**

### 3.1 Band heights

| Band | Height | Source |
|---|---|---|
| **NDR-240-24** | **185 mm** | 125.2 + 40 above + 20 below. Not tradeable |
| Relay rail: 94.74SMA + 55.34 + 094.71 clip | **71 mm** | 70.5 mm, rounded for cover clearance |
| Contactor rail: 22.32 | **88.8 mm** | Taller than a relay band, so a rail carrying a 22.32 costs 88.8 rather than 71 |
| Terminal rail | **70 mm** | The corrected envelope |
| Ground bar, 2450K14 | **12.7 mm** plus landing space | Not a rail item. It bolts to the plate |

**Suppression costs nothing, and that closes an item Issue 1 carried as 0 to 7 extra
positions.** Lookup 9: the SMA ships with the 094.71 metal clip and the coil-side slot
takes the 99.01 module, **both fit, neither is sacrificed, and the module sits inside
the socket envelope so it adds no height.** Not a 99.02, which is the box-clamp
family; and the plastic 094.91.3 clip is instead of the metal one, not in addition.

### 3.2 Bands that fit in each plate height

The NDR's 185 mm band is a full band, but a rail can run beside it in the width the
NDR does not occupy - 63 mm plus 5 mm each side is 73 mm.

| Box | Plate height | NDR band | Remainder | Further bands at 71 |
|---|---|---|---|---|
| 14 x 12 | 324 mm | 185 | 139 | **1** |
| QLINE I | 360 mm | 185 | 175 | **2** |
| QILISU | 359 mm | 185 | 174 | **2** |
| 16 x 14 | 375 mm | 185 | 190 | **2** |

**Nothing in this range gets a third band below the NDR.** 16 x 14 has 49 mm left
over after two, QILISU has 33, and neither is a band.

---

## 4. THE DEMAND, IN RAIL MILLIMETRES

Rail occupancy from D-194. **Every figure is the owner's lookup; none is derived here.**

| Item | Each | Count | Total |
|---|---|---|---|
| Relay envelopes: 94.74SMA socket with 55.34 | **30 mm** | 6 | **180 mm** |
| KM-DRV, Finder 22.32, one module | **17.5 mm** | 1 | **17.5 mm** |
| KM-CHIL, if it is the orphaned second 22.32 | 17.5 mm | 1 | **17.5 mm** |
| Terminal blocks | **6.2 mm per way** | **57 ways** | **353.4 mm** |
| End plates | 1 to 2 mm outside the pitch | say 2 banks | ~4 mm |
| | | **Rail demand** | **~572 mm, call it 568 to 572** |
| NDR-240-24 | 63 + 5 each side | 1 | **73 mm**, inside its own band |

**Not in the total, and each is a real addition:**

- **K-PERM-P, +30 mm**, if K-PERM splits. ?16, and order.md recommends buying the
  fourth gold either way.
- **Four unchosen devices** - the main disconnect, two overcurrent devices, the R-PI
  fuse holder. **Their footprint cannot be looked up because nobody has said what they
  are.** On the tree's only modular reference, 17.5 mm each, that is about **70 mm**.
- **Five sense-circuit burdens.** parts.md puts the burden for S-08 and S-03 in the
  main panel and no file says what holds them. Still true after eleven lookups.
- **Two ground bars.** Section 5.
- **Wire-bending space at each rail end**, and any horizontal duct.

**The 9 mm air gap between adjacent 22.32s does NOT apply here.** It is required only
if ambient is over 40 C with contacts over 20 A; KM-CHIL carries 7.5 A continuous.
**So KM-DRV and KM-CHIL may sit adjacent and that is 9 mm not spent.**

### 4.1 Rail available, and the comparison

**Two vertical wireways stay.** They are the class separation - LINE down one, 24 V
and signal down the other - and G-51 forbids spending a separation to make a box fit.
**Sized at the catalog minimum that is plausible, 25 mm each**, so 50 mm off the plate
width. Section 6 is why that number is provisional.

| Box, portrait | Plate W | Rail per band | Band beside NDR | Two more bands | **Rail available** | Demand | **Margin** |
|---|---|---|---|---|---|---|---|
| 14 x 12 | 276 | 226 | 153 | 226 (one only) | **379** | 568 | **-189** |
| QLINE I 400x300 | 260 | 210 | 137 | 210 + 210 | **557** | 568 | **-11** |
| **QILISU** | **271** | **221** | **148** | 221 + 221 | **590** | 568 | **+22** |
| **16 x 14** | **327** | **277** | **204** | 277 + 277 | **758** | 568 | **+190** |

**Read the two middle rows together, because that is the whole answer.** A true 16 x
12 misses by 11 mm. The box on the shelf clears by 22 mm. **Both numbers are smaller
than one unchosen device, and there are four of them.**

---

## 5. THE GROUND BAR: THE PART BOUGHT IS NOT WHAT THE STUDY ASSUMED

**McMaster 2450K14 is a tin-plated copper block, 5.75 x 0.50 x 0.50 in - 146 x 12.7 x
12.7 mm - twelve 1/4-28 tapped holes, 14 to 6 AWG. NO INSULATORS AND NO MOUNTING
HARDWARE.** A true insulated 12-way bar is a 12.5 x 2.5 in envelope at 9 in C-C, and
that is not what is on the shelf.

**Two are bought, and D-192 rules that two bonded bars are one ground point** - the
jumper is not a landing, and the bars are never split by class.

**Three consequences for the plate, none of which was in Issue 1.**

**1. They are not rail items.** It sits on the panel or bolts through its own ends.
**So it competes for plate AREA, not for rail length**, and it can live in dead space
below a terminal rail where nothing 70 mm tall will go. That is the one piece of good
news in this section.

**2. Bolting through its own ends puts two holes in the plate, at least 5.0 in
apart**, because closer than that the drill meets the taps. **Two bars is four holes
in a 4.5 mm plate.** Two bars end to end is 292 mm of linear run, **which does not fit
across the QILISU's 221 mm of rail field and does not fit across the 16 x 14's 277
either**, so they stack rather than abut. That is fine and it is worth stating,
because "two bars" reads as a line and it is not one.

**3. NO INSULATORS, AND THE PLATE MATERIAL IS STILL NOT ON FILE.** A bare copper block
bolted flat to a plate is bonded to that plate. **If the QILISU's 4.5 mm plate is
steel, the bar bonds it; if it is plastic, the bar floats on it.** parts.md gives the
plate a thickness and no material, and D-165's "the plate is plastic" is recorded of
the parallel build. **This is a requirement, not a lookup about a bar: state the
plate's material, then decide whether the bar needs standoffs.** It is the same gap
Issue 1 found and the eleven lookups did not close it.

---

## 6. THE ONE NUMBER THAT WOULD CHANGE THE VERDICT

**The two vertical wireways are sized at 25 mm here as a plausible catalog minimum,
and nobody has the number that actually sizes them.**

Duct fill is **50 percent of interior cross-section, NFPA 79 section 13.5.2, not NEC.**
Knock nominal W x H down to about 90 percent for wall thickness, then fill 50 percent
of that. Catalog shortcut: **N = (W x H) / (1.75 x D squared)**, where D is the
conductor outside diameter.

**D is not on file and cannot be, because no wire gauge has been chosen** - D5
deliberately has no gauge column, and my own file forbids stating one from memory.

**What it does to the verdict:**

| Duct pair | QILISU rail available | 16 x 14 rail available |
|---|---|---|
| 2 x 12.7 mm, the 0.5 in catalog size | **665** - clears | 812 - clears |
| **2 x 25 mm** | **590 - fails once devices land** | **758 - clears** |
| 2 x 40 mm | 500 - fails | 668 - clears |
| 2 x 60 mm | 410 - fails | **548 - fails** |

**So the QILISU survives only on 0.5 in ducts, and 16 x 14 survives up to about
50 mm.**

**Is dropping to a 0.5 in duct spending a protection, a margin or a clearance?** It is
none of the three. **The 50 percent figure is a code limit; the 30 to 40 percent shop
practice exists so the cover still snaps on**, which is a build and repair cost.
**G-51 does not forbid spending that** - but it cannot be decided without D, and
picking a duct before picking a conductor is the wrong order.

**Stated as the owner's choice rather than as a recommendation: if you want the box on
the shelf to work, the question is whether every conductor in the panel fits two
half-inch ducts at 50 percent fill, and that is one measurement after the wire is
chosen.** MAIN-PANEL does not recommend designing to the limit.

---

## 7. WHAT REMOVING THE RECEPTACLES FREES, AND WHAT IT COSTS

Asked directly, so answered directly.

**It frees nothing from the plate, because receptacles were never in the plate budget.**
D-046 put them in an enclosure FACE, and main-panel-buy.md placed them on a side or
front face, not on the plate. **Issue 1 counted them as a face item and a depth item
and never as plate area.**

**What it does free, and all of it is real:**

- **A face.** Four rectangular cutouts, their cord-cap clearance and bend radius, and
  a cord anchor beside each, all gone.
- **Interior depth beside the LINE duct**, which main-panel-buy.md flagged as
  needing checking before the rails were fixed.
- **The enclosure-rating objection dissolves.** main-panel-buy.md's sharpest point was
  that D-047 gaskets five top-face holes while D-046 puts open receptacles with cord
  caps on another face, **so you would buy a rating the box does not have.** With no
  receptacle in any face, **the box's worst penetration is the top-face devices and
  the cord grips, which is exactly what D-110 and F-088 already address.** That
  objection is answered by a lookup rather than by a part.

**What it costs: four more bottom-face glands, eleven to fifteen.** Section 2.

**And one thing that is not mine to fix. LOOKUP 11 CONTRADICTS D-046.** D-046 reads
"the receptacles are PANEL MOUNTED in the enclosure face and the cords plug into them
from outside", and it closed F-023 on that basis. **The lookup says a standard 15 A
duplex does not panel-mount at all.** D-046 is superseded by a fact about the part.
**Reported, not fixed, per rule 2.** What follows for BOSS: D-046 restated; P-03,
P-04 and P-05's End A rewritten, since all three say "relay-switched receptacle, panel
mounted in the enclosure face"; **and RUN-018, RUN-019 and RUN-020's A-face cell goes
from FACE to BOTTOM, with a new RUN- id for the R-PI feed** - a new id under D-149,
never a suffix.

---

## 8. THE FOUR DEVICES THAT ARE NOT LOOKUPS

**The owner asks what each needs to BE. Requirement and search term. No part is
named.** D-193 records that these four cannot be looked up because nobody has said
what they are.

### 8.1 The main disconnect, ?1

| | |
|---|---|
| **What it protects** | **Nothing.** It is not a protective device. It exists so the panel can be worked on dead |
| **What it must interrupt** | **Every branch circuit that enters, together.** D-137 makes that at least two - BUS-A and BUS-B. A disconnect that opens one of two leaves the panel live and reading off |
| **Rated against** | Breaking under load, not merely isolating, at the sum of every 120 V load in the panel |
| **Failure mode** | **Its position must be readable.** A disconnect whose state cannot be seen is not a disconnect, and this panel has no lamp that goes out when it opens - PL-Y is downstream of KM-DRV and PL-R is downstream of K-PERM |
| **Search** | `enclosure door interlocked disconnect switch DIN rail two pole`; `load break main switch DIN rail 120 V padlockable` |

**And the G-48 question that should be asked before any part is bought: does it need to
be IN the panel.** The building branch breaker is already a means of disconnection if
it can be locked off. **That is zero parts, zero rail millimetres and zero buy lines,
against one device, one rail position, one step and about 17.5 mm of the margin this
whole study is about.** What the in-panel device buys over a locked-off breaker is
that the person opening the box can see the state at the box. **MAIN-PANEL does not
choose. Both satisfy "a means of disconnection that can be locked off and verified
dead at the panel", and only one of them costs plate.**

### 8.2 The two overcurrent devices, ?2 and ?3

**They are not one requirement. BUS-B is the hard one.**

| | BUS-A | BUS-B, the dedicated chiller circuit |
|---|---|---|
| **What it protects** | The NDR primary, FV-1, and the transfer, manifold and R-PI feeds | The chiller and loop pump feed |
| **Carry** | The sum of those at 120 V | **7.5 A continuous** - 6 A chiller plus 1.5 A pump |
| **The hard requirement** | Selectivity with the building breaker | **It must NOT trip on the compressor's starting inrush, and parts.md states outright that the DBE-200's locked rotor current is NOT PUBLISHED.** The trip curve has to be chosen against a current nobody has measured |
| **Failure mode** | Fails open. A device that fails closed is not a protection | **The same, plus one this panel cannot see: a nuisance trip on BUS-B is SILENT.** D-108 leaves nothing in the panel wired to the chiller, so the compressor stops and nothing reports it. **That is F-110's self-masking shape arriving on a breaker** |
| **Search** | `supplementary protector UL 1077 versus branch circuit breaker UL 489` | `DIN rail circuit breaker C curve versus D curve motor starting`; `hermetic compressor inrush breaker curve selection`; `JBJ Arctica DBE-200 locked rotor amperage nameplate` |

**The distinction that decides the part, and it decides P-01 with it: a supplementary
protector is not a branch-circuit overcurrent device.** If the building breaker is the
branch protection, these two are supplementary and may be small. If it is not, they
must be branch-rated, and that is a different part at a different size. **P-01 is OPEN
and nothing may be bought against it, rule 9.**

### 8.3 The R-PI fuse holder

| | |
|---|---|
| **What it protects** | The conductor feeding the Pi's receptacle, **so that a fault there cannot take BUS-A and therefore the whole panel** |
| **What it must interrupt** | A 27 W USB-C brick at 120 V. A very small load |
| **Rated against** | **The brick's plug-in surge.** A switch-mode supply charges its input capacitor on connection, so a fast-acting element sized on running current will nuisance-blow |
| **Failure mode** | **Fails open, and its state must be readable without dismantling.** P-07 says the Pi has power whenever the panel does and **nothing in the panel can power-cycle it**, so a blown fuse here is an invisible dead Pi diagnosed by elimination |
| **Search** | `DIN rail fuse holder blown fuse indicator`; `time delay fuse switch mode power supply inrush` |

**G-48 on the indicator: one part, no extra step, and what it prevents is the one
failure in this panel that presents as "the Pi is dead and nothing says why".** It
goes in, and it goes in HERE and nowhere else.

### 8.4 KM-CHIL, ?8

| | |
|---|---|
| **What it switches** | One receptacle feed carrying the chiller and the loop pump, **7.5 A continuous plus an unpublished compressor locked-rotor inrush** |
| **Rated against** | **Not a resistive 7.5 A.** A hermetic compressor is a motor load: the rating class is motor duty, not AC-1. **The number that sizes it is the INRUSH** - the same lesson the fill solenoid taught at 0.58 A against 0.21 A holding |
| **Coil** | **BLOCKED. ?9 is open: whether its coil hangs on node PB or on KM-DRV decides whether the Pi can stop the water system, which G-26 forbids.** A coil voltage follows from which bus it is on, so no device may be chosen first. Rule 9 |
| **Failure mode** | **It must DROP OUT cleanly on loss of coil supply.** A contactor that does not release on a sagging rail is a chiller that does not stop when the permissive drops, and stopping when the permissive drops is the entire content of D-137 |
| **G-30** | It carries an ARC pole. **If it is the orphaned second 22.32 and that family's poles share a contact volume - ?26, F-055 - nothing quiet may ever go on its second pole**, which matters because S-18's Pi-read exit wants exactly that pole |
| **Footprint if it is the second 22.32** | 17.5 mm rail, 88.8 mm above rail, 60.8 mm deep, **and the 9 mm inter-device air gap does not apply at 7.5 A** |
| **Search** | `modular contactor AC-3 rating single phase hermetic compressor`; `definite purpose contactor 2 pole 120 V coil 20 A` |

---

## 9. WHAT IS UNCHANGED FROM ISSUE 1

Stated because "no change" is a result.

**The counts.** 16 to 24 rail positions, now narrowed at one end: **suppression costs
zero positions**, so the range is 16 to 17 plus the four unchosen devices and whatever
carries five burdens. **57 clamps is still a floor** and the panel-internal conductor
list is still unwritten and still MAIN-PANEL's.

**G-30 is still not threatened by a small box.** It separates poles inside a relay and
the separation is bought by order.md's six envelopes. **F-055 is unaffected by
enclosure size: S-08 has nowhere to move whatever the box is.**

**Portrait is still right for this panel, and the lookups vindicate it rather than
costing it.** Mounted landscape the QILISU gives 359 mm of width and 271 of height -
**and 271 mm takes the NDR's 185 mm band plus exactly one more**, which is 545 mm of
rail against 568 of demand. **Portrait beats landscape on this box by 45 mm of rail.**
G-51's rule and this panel's arithmetic agree.

**Double-decks are still out, on D-190's safety argument, and that lever was gone
before this issue started.**

**The plate material is still not on file, and section 5 gives it a second reason to
matter.**

---

## 10. WHAT THIS ISSUE FOUND THAT NO FILE PREVIOUSLY SAID

**a. Lookup 11 contradicts D-046**, a frozen decision that closed F-023. Section 7.
Reported, not fixed.

**b. The gland count is fifteen, not eleven**, and it went up because of the lookup
that was supposed to take something away.

**c. A nuisance trip on the chiller's overcurrent device is silent**, for the same
reason F-110's dry-run failure is silent: D-108 leaves nothing in the panel wired to
the chiller. **F-110 was about the loop pump; this is the same blindness arriving on a
breaker**, and nobody has said it.

**d. Issue 1's own binding constraint was wrong.** The bottom face is a rectangle, not
a line, and two rows of grips clear it on both candidate boxes with room. **The
constraint that actually binds is the NDR's 185 mm vertical band against a plate
height, which Issue 1 could not see because it had no height figure for anything.**

---

## 11. STATUS

**Finished as a study. The arithmetic is run and the verdict is given.**

**The verdict: buy a 16 x 14. The QILISU on the shelf is short by more than its
apparent 22 mm margin, and a true 16 x 12 is short outright.**

**The one thing that would reverse it** is the conductor OD, which decides whether two
half-inch wireways carry the panel at NFPA 79's 50 percent fill. **That is a
measurement after the wire is chosen, and choosing a duct before a conductor is the
wrong order.** MAIN-PANEL does not recommend designing to the limit to keep a box.

**Not delivered, and deliberately: no layout, no placement, no rail order.** D-188
asked for the arithmetic and the verdict.

**What remains MAIN-PANEL's and is not blocked on anybody: the panel-internal
conductor list.** It is the largest unknown left in the demand figure, it is the
reason 57 clamps is a floor rather than a count, and wiring-schedule.md section 7
correctly assigns it here.
