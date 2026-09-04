# Entry faces and entry order. CBL-02 and CBL-03

**Returned 2026-09-04 by PUMP-BOXES and DISPLAY-BOX, against D-146.** One question,
two boxes, answered together because the same two rules decide both.

**What this states:** which face each cable enters, and the order of entries on that
face. **What it does not state, because D-146 gives it to INTERCONNECT:** where on
the face, and the spacing. **And per the hard limits on this pass: no dimension, no
gland size, no gland count, no part number.** How many glands carry the entries below
is not stated here and is not derivable from the order.

---

## 1. THE TWO RULES THAT DECIDED EVERY FACE

**Rule 1. The design sheds rather than seals, so an upward-facing penetration is the
worst case and needs a reason.** D-047, and D-092 in terms: the assembly's rating is
set by its worst penetration regardless of what is fitted above. Neither box has a
reason, so neither box has a top entry.

**Rule 2. A drip loop only sheds if the entry is at or below the cable's lowest
approach.** D-121 and D-126 put the field cord's drip loop OUTSIDE the box, and
D-090's cut rule spends a drip-loop allowance per grip rather than only at the tank.
INTERCONNECT graded the consequence STRUCTURAL at K-03: a drip loop on an
upward-facing entry is not a drip loop, and no addition changes that.

**Both point down. Both boxes enter on the BOTTOM face.**

**A third source agrees and is recorded with its provenance rather than as
corroboration, per G-37.** The 1st Edition set appears to hold that every grip is on
the bottom face, *"never the top or the sides"*, with a drip loop outside. B-16,
observed in that set and UNVERIFIED. It is not a second source for D-047; it is an
old build that reached the same place, and under G-40b it is the starting point on a
question this tree had no position on. **The answer here does not depend on it.**

**What is NOT a reason for any face below:** where a cable comes from. No entry in
this document was chosen by a run, a wall layout or an approach direction. M-02 and
Z5 are open and nothing here waits on them.

---

## 2. PUMP-BOXES. CBL-02

### 2.1 The premise the face names hang on, and it is PUMP-BOXES' own

**Each box mounts to the dosing wall with its back to the wall and its LID FACING THE
ROOM.** Box mounting and the lid as a sealing face are PUMP-BOXES' open items and
this settles the orientation half of them.

**The reason is D-047 and it is about the wet side, not the cable side.** The head is
outside the box and the motor body is inside it, so the barbs, the tube and every
tubing joint sit on the lid. **A lid facing up puts the whole wet assembly directly
above the box's own sealing face and its head penetrations, and puts a tube change
over them.** A lid facing the room puts them beside it. The box sheds either way only
if the lid is vertical.

**It also serves the tube change PUMP-BOXES owes DOSING** - access and clearance to a
head that is at hand height on a wall rather than on top of a box.

**So, for both boxes, standing at the box facing the lid and the heads, which is how
a tube is changed:** the LID is in front of you, the BOTTOM face is below it, the
BACK is against the wall.

### 2.2 The face

**BOTTOM FACE, on the box body. Both boxes. Every cable.**

**Two reasons from inside, either sufficient:**

1. **The lid is a heavy serviceable assembly carrying four motor bodies and it is
   removed as a unit.** Anything landed on it moves with it and drags wiring. That is
   already on file as the reason the pull-down landing mounts to the box BODY and not
   the lid, and a cable entry is the same argument with more mass on the end of it.
   **A cable entering the lid tethers the one part of this box that has to come off.**
2. **The lid is already committed.** It is the head penetration under CBL-05 and a
   sealing face. A second class of penetration on the same surface is a second
   question on a face that has not answered its first.

**And the other faces, named rather than assumed away:** the back is against the
wall; the top is rule 1; the sides are the same shed argument as the top with less
force, and carry no reason to differ from B-16.

### 2.3 The order on that face

**Two entries per box today. Reading the bottom face LEFT TO RIGHT as you stand at
the box facing the lid:**

| Order | Box A | Box B | What it is |
|---|---|---|---|
| **1, left end** | RUN-001 | RUN-002 | Driver motor supply, from KM-DRV. 24 V, ARC duty |
| **2, right end** | RUN-003 | RUN-004 | Step and direction, plus the VDD feed and its return. SIGNAL |

**Left and right are the same on both boxes. The two boxes are one build, not a
mirrored pair**, because a mirrored pair is two builds of one thing and G-44 puts the
burden on that.

**The reason for the order is what is inside, and it is the driver board's own
geometry.** Each 6121 has its power and motor screw block on one side and its logic
header on the other, confirmed from the photograph in parts.md. **The four drivers in
a box are set the same way round, so all four power blocks face one end of the box
and all four logic headers face the other.** The motor supply enters at the power-block
end and the step and direction enter at the logic end. **Nothing crosses the box.**

**Why the full width of the face and not merely two separate entries:** a 24 V ARC-duty
break into eight drivers with bulk capacitors, and the logic pins of drivers whose EN
defaults ENABLED and whose severed DIR is the worst outcome in the fail-safe sweep,
are the two most different things in this box. **Separation inside the box is the only
adjacency remedy available to PUMP-BOXES that costs nothing**, which is the G-44 test
D-156 applied to the standpipe tie groups and the same answer.

**The order survives a split.** RUN-003 and RUN-004 are marked as expected to split on
F-030's per-signal returns, and under D-149 their ids retire when they do. **The rule
is not keyed to an id: everything arriving from the display box enters at the logic
end, the motor supply enters at the power-block end.** Whatever the jackets are called
after the split, that still places them.

**Not stated, and not by omission:** no separate equipment-ground entry. CBL-07's own
text says the boxes are plastic and offer no bonding path, and every equipment ground
lands on a ground bar. RUN-017's segregation cell reads "rides its circuit". **If
CBL-07 returns a separate bonding run to each box, it takes the face and the position
of the circuit it protects and adds no new rule here.**

---

## 3. DISPLAY-BOX. CBL-03

### 3.1 The premise

**The box mounts on the wall with its display facing the operator**, which M-03 owns
and which the gasketed display cutout already assumes. **Standing at the box facing
the display:** the display cover is in front of you, the BOTTOM face is below it, the
BACK is against the wall.

### 3.2 The face

**BOTTOM FACE. Every cable.**

**Reasons from inside:**

1. **The front is the operator's display and the face that opens.** Every landing in
   this box is on the back plate: the logic board, the Pi, the two carriers. **A cable
   entering the cover has to bridge the joint that opens**, and the cutout in that
   cover is gasketed, which is the youngest part in the assembly under D-092's own
   argument.
2. **The box must be opened before it is commissioned and after.** C-14 switches each
   EZO circuit from UART to I2C by a jumper procedure BEFORE the box is closed, and
   the EZO mode pin differs by circuit type. Anything tethering the cover is disturbed
   by a build step that is already on the list.
3. Top is rule 1. Back is the wall. Sides carry no reason to differ from B-16.

### 3.3 The order on that face

**Reading the bottom face LEFT TO RIGHT as you stand at the box facing the display:**

| Order | RUN | What it is | Class |
|---|---|---|---|
| **1, left end** | RUN-016 | Probes to the EZO circuits and their carriers | SIGNAL, SEG-D |
| **2** | RUN-003 | Step and direction to pump box A, plus the VDD feed | SIGNAL, SEG-C |
| **3** | RUN-004 | Step and direction to pump box B, plus the VDD feed | SIGNAL, SEG-C |
| **4** | RUN-005 | Permissive coil drive to KM-DRV | 24 V, COIL |
| **5** | RUN-007 | S-03, both legs of one changeover pole | 24 V, SENSE |
| **6** | RUN-008 | S-20, both legs of one changeover pole | 24 V, SENSE |
| **7** | RUN-006 | KM-DRV pole 2, the permissive readback | 24 V, SENSE |
| **8, right end** | RUN-009 | Pi power | LINE, contested |

**Two rules generated that order and both come from inside the box.**

**Rule A. The order follows the internal zones, from the most susceptible thing in
the box to the least.** The EZO carriers and their probe conductors are at one end,
alone, which is what SEG-D says about probes and what the carriers are FOR. The
logic board's output side is next. Its 24 V isolated side is next. Pi power is at the
far end, as far from the probes as this face allows. **Nothing crosses the box to
reach its landing, and no conductor class is interleaved with another.**

**Rule B, and it is the one worth the pass. RUN-005 AND RUN-006 ARE NOT ADJACENT
ENTRIES.** F-029: they are the same voltage class, so no scheme that sorts by class
separates them, and **a short between them makes the readback follow the command,
which is precisely and only the failure G-09 exists to detect.** It removes weld
detection at the same time. The schedule states it as a jacket rule - separate
jackets or provably non-adjacent - **and an entry order is where that rule either
survives or quietly dies, because two jackets entering side by side are adjacent
whatever their jackets say.** RUN-007 and RUN-008 sit between them. Neither may be
moved out of that gap: each carries a G-27 complementary pair from one changeover
pole and may not be split, so they are two entries and not four.

**One consequence reported rather than solved, and it is INTERCONNECT's to close.**
Ordering by susceptibility puts the LINE entry at an end, which gives it the fewest
neighbours available on this face, but its one neighbour is a 24 V sense run.
**Every candidate neighbour for a LINE entry on this face has a stated unsafe short
case:** an optocoupler sense loop shorted to an energised neighbour lights the LED
and reads the wrong way, D-049, and the coil drive shorted to something live is
F-019's shorted output device against G-07. **There is no order of these entries that
removes that. The remedy that does exist is spacing on the face, which is
INTERCONNECT's under D-146.** So: **the gap between entry 7 and entry 8 is the one
gap on this face that carries a named failure**, and it is flagged here so it is
spaced deliberately rather than evenly.

**Also carried, not resolved here:** RUN-009's provision is OPEN in the schedule and
P-07 reads CLOSED in the interface table while display-box.md still carries its form
as open. **The face above is stated for the Pi's supply however it is provided.** If
it lands as a cord and cap under D-046's precedent rather than as a glanded cable,
the face does not change and the entry does not disappear, because the supply still
has to get inside the box.

**Splits:** as with the pump boxes, the rule is not keyed to an id. **Everything to
the drivers enters in the signal band, everything to and from the panel's poles
enters in the 24 V band with RUN-005 and RUN-006 kept apart, probes at one end, LINE
at the other.** That places whatever RUN-003 and RUN-004 become.

---

## 4. CBL-04, THE FIELD DEVICES. WHAT IS WATER'S

**Almost all of it. Named here so nobody reads this document as having covered it.**

**What is already decided and is neither WATER's nor mine to restate as new:** cords
run UP the standpipe and leave through a grip with a DRIP LOOP OUTSIDE the box,
D-126, which is D-047's shed principle applied to a cord. **That is the entry rule at
the field end and it is on file.** D-156 adds that float cords and pump cords get
separate tie groups on the pipe.

**What is WATER's, per device:**

| Run | The field end | Why it is not mine |
|---|---|---|
| RUN-012, RUN-013 | Day tank and storage tank floats, on the standpipes | The float, its cord and its position are WATER's, and the float pass restarts from requirements under D-118 |
| RUN-011 | Fill solenoid coil | The valve is WATER's under P-02 and D-136; the entry is that device's own housing |
| RUN-014 | Leak detection sensor | S-04, and its position is open under F-104 |

**And one observation offered as a question rather than an answer, because it may
mean the schedule's cell has no valid value rather than an unfilled one.** RUN-012
and RUN-013 are provisioned "Supplied" and D-131 makes the cord uncuttable at the
tank. **A float is not an enclosure and has no faces.** What exists at that end is a
cord leaving a standpipe, already ruled by D-126. **So "A face" for those two rows may
be the CBL- shape of F-097 again: a column asking for a kind of value the thing at
that end does not have.** INTERCONNECT and WATER between them, not decided here.

---

## 5. THE D-146 ESCAPE CLAUSE. NEITHER BOX USED IT

**D-146 says that if an enclosure owner cannot state a face without knowing the run,
that is a FINDING, because it would mean the box's contents are being decided by its
cabling rather than the other way round.**

**Neither box is in that position and no such finding is raised.** Both faces above
came out of what is inside the box and out of D-047, and neither needed a wall layout,
an approach direction or a run. **M-02 and Z5 are open and this document did not
touch them.**

**What was reported instead is in 3.3: an adjacency on the display box's face whose
remedy is spacing, which is INTERCONNECT's half of the same allocation.** That is the
allocation working, not failing.

---

## 6. STATUS

**The pass is complete and it is not self-declared finished, per rule 7.** BOSS
declares that after another agent builds against it and finds nothing, and the agent
that will is INTERCONNECT, filling the face cells of CBL-02 and CBL-03 and then
placing glands within the stated faces.

**Nothing here is a dimension, a gland size, a gland count, a position, a spacing or a
part number.** Faces and orders only.
