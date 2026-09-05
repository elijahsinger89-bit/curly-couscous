# D1. Build book

**How the machine is arranged and assembled, from an empty wall to a machine, in the
order the work is done.**

| | |
|---|---|
| Document | **D1**, per document-plan.md section 1.2 |
| Owner | BOSS, assembled from the returns of WATER, DOSING, PUMP-BOXES, DISPLAY-BOX, MAIN-PANEL and INTERCONNECT |
| Issue | 1, 2026-09-05 |
| Read by | The builder, from the first fixing to the last lid |
| Read when | Throughout. It is the book you are holding while you work |
| Written to | G-49 for every step and G-50 for every section |

---

## 1. HOW TO READ THIS BOOK

**MUST BE TRUE BEFORE THIS SECTION STARTS:** nothing. You are holding this book and
no work has been done.

**TRUE AFTER IT ENDS:**
- **BB-01.** The builder knows this book's conventions, knows which document owns
  what, and knows that a blocked step is stepped over and never substituted.

### 1.1 What this book is

**You need to know how to use tools. You do not need to know anything about this
machine. If it is not on the page it does not happen.**

This book carries **two things and nothing else: the ORDER things happen in, and how
a thing is physically assembled.** That is D-183, and it is absolute. Every other
kind of fact lives in another document and this book points at it.

| What you need | Where it is | What this book does |
|---|---|---|
| Any conductor, terminal or landing | **D4** wiring-instructions.md, **D5** wiring-schedule.md | Points at the page. Never restates a joint |
| Any part, quantity, count or price | **D7** | Points. G-41: quantities are deltas and must never repeat |
| Any measurement or acceptance test for service | **D8** and commissioning.md | Points |
| Any rung, coil, contact or device function | **D2** electrical-schematic.md | Points |
| Any cable route, jacket or gland position | **D6** cable-and-terminal-schedule.md | Points |
| Where a device sits on a plate, a rail or a face | **D3** | Points |
| Why anything is the way it is | The tree: decisions.md, findings.md, traps.md, the subsystem files | Points |

**There is no parts table in this book.** Not on any section, not at the end. D7 is
the only document in this set where a quantity appears, and a second place a quantity
can live is the one defect in the 1st Edition set that cost money.

### 1.2 How to read a step

**Every step is numbered and the numbers are section-scoped.** 7-03 is section 7,
step 3. **Numbers are never silently changed. If a step is ever inserted it takes a
letter, 7-03a, and a REVISION line appears at the head of that section saying so.**
There are no revision lines yet.

**Every step ends with ACCEPT: how you know it is right, checked at that moment.** If
you cannot see the accept condition, the step is not done.

**Some steps carry WHY.** Those are the steps that exist to prevent something, where
a builder would reasonably do it differently. A builder who knows why will not undo
it, and a builder who does not will improve it.

**A step marked BLOCKED has no accept condition yet.** It says what is missing and
who owns it. **Do not substitute, do not pick a likely value, do not skip ahead.**
Leave that item and go to the next step. A blocked step stays in its place so you
know you are stepping over it, rather than reaching the end and discovering something
in the middle was left out. This is D4's convention and this book uses the same one.

**Every allowance, correction and precondition is folded into the step it modifies.**
Nothing in this book corrects a step after it. T-020: a builder running in order cuts
at step 7 and reads step 8 too late, and a cut cable cannot be un-cut.

### 1.3 How to read a section

**Every section states what must be TRUE BEFORE it starts and what is TRUE AFTER it
ends.** That is G-50, and it is why this book is written this way: **sequence defects
are invisible to every per-page check, because each page is internally consistent and
the defect is in the order.**

Postconditions carry ids of the form **BB-nn**. The prefix is reserved by this
document for its own pre- and postconditions, per G-43, and means nothing outside it.

**If you reach a section whose preconditions are not all true, stop.** Do not start
it. Something earlier was skipped or is blocked, and the section that produces the
missing condition is named beside it.

### 1.4 Names

**Every device is named as D2's roster names it, and G-42 binds: one device, one
name, everywhere.** This book states no device's function, no contact and no rung.
It states which device, where it goes, and when.

Float POSITIONS are LS-1 to LS-8 and they are positions, not parts, per D-127 and
D-145. Channels are CH1 to CH8 per channel-token.md.

### 1.5 Where this book differs from the sheet list in document-plan.md, and why

The plan lists D1's sheets in the 1st Edition's sheet order. Six differences, each
stated so nobody reads a missing sheet as an oversight.

| Plan's sheet | What this book does | Why |
|---|---|---|
| "The interior of each enclosure" | Sections 7 to 15 carry the ORDER an enclosure is built up in and the mechanical method. **Where anything sits is D3** | document-plan section 3.2 gives device position, rail, duct, face and penetration to D3. A second place for a plate layout is a second place it can drift |
| "Probe cable routing" | Pointed at D6 | A cable route is one RUN- row's fact |
| "Chiller loop routing" | **Kept**, section 27 | It is pipe, not cable. No other document owns a pipe run |
| "Legend" | Section 1 carries the conventions instead | A legend belongs on a drawing sheet. This book is prose and numbered steps |
| "Overview" | Section 2, written as a precondition list rather than as a picture | G-50. An overview a builder cannot check against is decoration |
| "The dosing wall", old sheet 13 | Absorbed into sections 6, 10, 12 and 29 | **There is one wall in this build, not a separate dosing wall.** parts.md's "The wall" section puts the four enclosures, the manifold, the tubing raceway and the jug stations on one wall |
| "Float standpipe assembly" and "Storage standpipe", old sheets 14 and 19 | Absorbed into sections 17 to 23, one set of steps covering both tanks with every difference named at the step | D-121's method is one method. Two sheets for one method is where a difference gets stated once and missed once |

**Three sections are in this book and in no sheet list**, because they are build work
nothing else in the set schedules and two of them are the open gates: **section 3**,
labelling every device as it is unpacked; **section 4**, reading every terminal;
**section 5**, measuring the wall.

### 1.6 The two things that block every dimension in this book

**Said here once and then said again in every section where a builder would need
them.** They are not collected at the end, because a builder who reaches the end and
discovers something in the middle was skipped has found out at the worst possible
moment.

**F-106. Nobody in this project has looked at a terminal and written down what is
printed on it.** Section 4 is the work that closes it. Until it is closed, every
joint in D4 is blocked, so section 31 cannot be worked.

**M-02. The wall is not measured and there is no wall layout.** Section 5 produces
the measurement and section 6 is the layout that is blocked on it. **Until it exists,
every dimension in this book is blocked**: every mounting position, every gland
position, every tank position, every cable length, and the float cord length that
gates the float purchase under F-100.

**Everything else in this book is complete.** The order is complete and the method is
complete. What is missing is where things go and what is printed on them.

---

## 2. WHAT MUST BE TRUE BEFORE STEP 1

**MUST BE TRUE BEFORE THIS SECTION STARTS:**
- BB-01, section 1.

**TRUE AFTER IT ENDS:**
- **BB-02.** The document set is at the bench.
- **BB-03.** Every part this book uses is present, or its absence is recorded.
- **BB-04.** The four fixed features of the room are located: the wall, the floor
  drain track, the cold water supply point, and the building branch circuit.

**2-01. Put the document set on the bench: D2, D3, D4, D5, D6, D7 and this book.**
ACCEPT: seven documents, each with its own name at the top of its first page.
WHY: D4's pages and D5's rows are used in section 31 and are useless without D6, and
D3 is the only place a position is stated. **A build worked from this book alone will
reach section 7 and stop.**

**2-02. Confirm D7 has been worked and the buy is done.**
ACCEPT: D7 exists and every line on it is marked bought, ordered or open.
WHY: **D7 comes before this book, not after it.** If you are reading this step with
parts missing, the buy was not finished, and the sections below will stop at the part
rather than at a decision.

**2-03. Lay out the parts D7 lists for the mechanical build and check each one
against its line.**
ACCEPT: every line is either matched to a part in front of you or marked absent on
D7, and no line is unaccounted for.

**2-04. Record every part that is absent.**
ACCEPT: D7 carries the absence against the line, dated.
WHY: **a recorded absence is worth more than a guess.** It tells sections 3, 4 and 31
which rows stay blocked, and it stops a substitution being made at the bench where
nobody will see it again.

**2-05. Find the wall this build mounts on and confirm it is clear.**
ACCEPT: the wall named in parts.md's "The wall" section is empty and reachable along
its whole width.

**2-06. Find the floor drain track.**
ACCEPT: you can see the track and walk its length.
WHY: D-147 makes the track's entry point free, which is why no section below fixes
one. **You need to know where it runs before section 6 places a tank.**

**2-07. Find the cold water supply point that FL-01 connects to.**
ACCEPT: you can put a hand on the supply stub.
BLOCKED for anything beyond finding it. Missing: FL-01 is an OPEN interface row.
Owner: WATER returns the connection, BOSS freezes the row.

**2-08. Find the building branch circuit that P-01 connects to.**
ACCEPT: you can put a hand on the outlet or the disconnect.
BLOCKED for anything beyond finding it. Missing: P-01 is an OPEN interface row, and
D-137's dedicated chiller circuit is unaccounted for in it. Owner: MAIN-PANEL and
BOSS.

---

## 3. LABEL EVERY DEVICE AS IT IS UNPACKED

**MUST BE TRUE BEFORE THIS SECTION STARTS:**
- BB-03, section 2.

**TRUE AFTER IT ENDS:**
- **BB-05.** Every device carries the name D2's roster gives it, written on the
  device, before it is installed.

**This section is short and it is the cheapest insurance in the book.**

**3-01. Open D2 section 1 at the device roster.**
ACCEPT: you are looking at a list of names.

**3-02. Write its roster name on each device as you unpack it.**
ACCEPT: the name on the device reads exactly as D2 spells it, character for
character.
WHY: **G-28. Which device goes in which position is a build fact, and the two relay
contact types look alike.** A swapped pair passes every check in this build and
destroys the property one of them was bought for. **Label at unpack, not at
installation** - once four identical envelopes are on a bench, the information that
told them apart is in the packaging you have thrown away.

**3-03. Write the roster name on the socket a plug-in device goes into, as well as on
the device.**
ACCEPT: the socket and the device that belongs in it read the same.
WHY: **the socket is what a conductor lands on, not the relay.** A device pulled for
service leaves a socket with no name on it, and the next person puts back whatever
fits.

**3-04. Set aside any device whose roster name you cannot find in D2.**
ACCEPT: it is on the bench, unlabelled, and written down.
BLOCKED beyond setting it aside. Missing: a device with no name in D2 has no identity
in this build. Owner: BOSS, and G-42 governs the naming.

---

## 4. READ EVERY TERMINAL

**MUST BE TRUE BEFORE THIS SECTION STARTS:**
- BB-03, section 2.
- BB-05, section 3.

**TRUE AFTER IT ENDS:**
- **BB-06.** terminal-survey.md is filled in for every device on the shelf, and every
  device not on the shelf is recorded as NOT ON SHELF.

**THIS SECTION CLOSES F-106 AND IT IS THE ONLY THING BLOCKING ALL 125 JOINTS IN D4.**
No decision, no lookup, no money: the parts in front of you and something to write
with. It is one evening and everything downstream reads it.

**4-01. Open terminal-survey.md.**
ACCEPT: you are looking at the form and the device list.

**4-02. Work terminal-survey.md through, device by device, in the group order it
gives.**
ACCEPT: every device in its list has either a completed set of rows or the words NOT
ON SHELF against it.
WHY: **the survey is grouped so that a partial pass still unblocks something.** This
book does not restate the form, the datum rule or the legend convention: they are
terminal-survey.md's and a terminal fact copied into a second document is a terminal
fact that can drift.

**4-03. Put the completed survey with the document set.**
ACCEPT: it is on the bench with D2 to D7.
WHY: **it is read once and cited forever.** That is the whole point of doing it once,
and it is why a photograph is not a substitute.

---

## 5. MEASURE THE WALL AND THE FLOOR

**MUST BE TRUE BEFORE THIS SECTION STARTS:**
- BB-04, section 2.

**TRUE AFTER IT ENDS:**
- **BB-07.** The wall, its fixing points, and the positions of the supply stub, the
  branch circuit and the drain track relative to it are measured, recorded, and
  handed to whoever holds M-02.

**5-01. Measure the wall and write the figures down.**
ACCEPT: a written record exists, dated, with the units on it.
WHY: **M-02 is OPEN and this measurement is its missing input.** parts.md states the
layout envelope; nothing in this tree states what is actually on that wall. **This
book states no dimension of its own and never will** - it records that the
measurement is taken and hands it on.

**5-02. Find and record every fixing point the wall offers.**
ACCEPT: each stud, rail, block course or fixing you found is on the record with its
position relative to one corner you name as the datum.
WHY: **name the datum and the direction you measured in.** A set of positions with no
datum is the defect the terminal survey exists to prevent, one level up, and the 1st
Edition's height contradictions were exactly this.

**5-03. Record the supply stub's position relative to the same datum.**
ACCEPT: it is on the record and the datum is the one named in 5-02.

**5-04. Record the branch circuit's position relative to the same datum.**
ACCEPT: as 5-03.

**5-05. Record the drain track's run relative to the same datum.**
ACCEPT: the track's two ends and its side of the room are on the record.
WHY: every overflow in section 24 has to fall continuously to this track and cannot
rise anywhere. **The track's position is a constraint on where a tank may stand, and
that constraint has to be in the layout before a tank is placed and not after.**

**5-06. Hand the record to whoever holds M-02.**
ACCEPT: the record has left your hands and section 6's precondition is somebody
else's work.

---

## 6. THE LAYOUT

**MUST BE TRUE BEFORE THIS SECTION STARTS:**
- BB-02, section 2.
- BB-07, section 5.

**TRUE AFTER IT ENDS:**
- **BB-08.** A mounting position exists for the main panel, pump box A, pump box B,
  the display box, the manifold and every jug station; a floor position exists for
  each tank; and a standing position exists for a jug change.
- **BB-09.** Each enclosure's entry positions and the spacing between them are
  stated.

### THIS WHOLE SECTION IS BLOCKED. HERE IS WHAT IS MISSING AND WHO OWNS IT.

**BLOCKED. Missing: M-02 is an OPEN interface row and there is no wall layout.**
Owner: DOSING and PUMP-BOXES claim the wall space jointly, **INTERCONNECT
arbitrates**, BOSS freezes the row.

**BLOCKED. Missing: CBL-01, CBL-02, CBL-03 and CBL-04 are all OPEN.** The FACE half
of each is answered - parts.md for the main panel, subsystems/entry-faces.md for the
pump boxes and the display box, D-126 and D-156 for the field devices - **and the
position-and-spacing half is INTERCONNECT's and needs the wall layout.** Owner:
INTERCONNECT, then BOSS freezes.

**BLOCKED. Missing: D3 does not exist.** Owner: each enclosure owner for its own
sheet, with INTERCONNECT placing glands within a stated face under D-146.

**Nothing below this line may be started until BB-08 and BB-09 exist.** Sections 7,
8, 9, 10, 12 and 16 each require one of them.

### What the layout must resolve, so that whoever writes it knows what is waiting

Stated as constraints, not as positions. **No position, no spacing and no dimension
is proposed here.**

**6-01. Give every wall-mounted item a position.**
BLOCKED. Missing: as above.

**6-02. Give each tank a floor position that leaves a continuous fall from its
overflow bulkhead to the drain track, with no trap, no low point and no rise
anywhere.**
BLOCKED. Missing: as above.
WHY THIS IS A LAYOUT CONSTRAINT AND NOT A PLUMBING ONE: WATER's return records that
an overflow line is a permanent wet-side object on the wall that four enclosures and
the cable runs are competing for, **and that it cannot go over or under anything.**
If it is not in the arbitration it will be routed last, against everything already
fixed.

**6-03. Give each tank a floor position that leaves the far side of its rim
reachable.**
BLOCKED. Missing: as above.
WHY: sections 18, 21, 22 and 23 all put a person's hands on the standpipe over the
rim, and D-131 puts them there again at every level adjustment for the life of the
machine.

**6-04. Give the jug stations positions that put the jug end of every dose line in
the operator's sightline from the standing position.**
BLOCKED. Missing: as above, plus DOSING's open jug placement item.
WHY: D-019 took translucent tubing and the sightline INSTEAD of the keyed coupling,
and both were named by DOSING as the conditions without which the coupling trades a
visible failure for an invisible one. **A station placed out of sight spends a
decision that was already made.**

**6-05. Give the display box a position that satisfies operator reach and sightline.**
BLOCKED. Missing: M-03 is an OPEN interface row. Owner: DISPLAY-BOX.

**6-06. State each enclosure's entry positions within the face its owner has already
stated, and the spacing between them.**
BLOCKED. Missing: as above.
**ONE SPACING ON ONE FACE IS NOT FREE AND MUST NOT BE SPACED EVENLY.** The display
box's bottom face carries a gap between its entry 7 and its entry 8 that
subsystems/entry-faces.md section 3.3 flags as **the one gap on that face carrying a
named failure.** It is called out here because a builder handed a face with no
spacings marked will space them evenly, and even spacing is the one answer that is
wrong. The reasoning is in entry-faces.md and D6 and is not repeated.

**6-07. Produce the float cord span terms.**
BLOCKED. Missing: the wall layout. Owner: INTERCONNECT.
WHY THIS ONE GATES A PURCHASE AND NOT A STEP: **F-100.** D-131 makes the float cord
the strain member, the trip-height datum and the signal path at once, so it cannot be
cut at the tank and cannot be joined there. **A float whose supplied cord does not
reach is disqualified, and the only remedies D-131 leaves are a splice in the wet
zone or moving a mounted panel, both of which it forbids.** So the cord length has to
exist before the float search, which means this section gates section 22 through D7.
The terms of the sum are set out in subsystems/water-float-requirement.md section
1.4 and are not repeated here.

---

## 7. PREPARE THE MAIN PANEL ENCLOSURE

**MUST BE TRUE BEFORE THIS SECTION STARTS:**
- BB-05, section 3.
- BB-09, section 6.

**TRUE AFTER IT ENDS:**
- **BB-10.** The main panel body has every penetration it will ever have, cut,
  deburred and fitted, and the enclosure is clean.

**EVERY CUT IN THIS SECTION IS MADE WITH THE ENCLOSURE EMPTY AND ITS BACKPLATE OUT,
AND THAT IS THE WHOLE REASON THE SECTION SITS HERE.** Section 13 populates the plate.
**A hole cut over a populated plate puts swarf under a relay socket and on a gold
contact, and neither is recoverable by cleaning.**

**7-01. Take the backplate out of the enclosure and set it aside.**
ACCEPT: the enclosure is empty and you can see through it.

**7-02. Mark the five top-face device holes at the positions D3 states.**
BLOCKED. Missing: D3 does not exist. Owner: MAIN-PANEL, and the face itself is
already decided in parts.md: the door-mounted devices are all on the TOP FACE,
nothing else penetrates that face, and every cord grip is on the bottom. **The hole
size and the count are parts.md's and D3's and are not repeated here.**

**7-03. Step drill each of the five top-face holes.**
BLOCKED. Missing: as 7-02.
WHY IT IS STEP DRILLED AND NOT TWIST DRILLED: parts.md records the method with the
face. A twist drill grabs sheet and tears a hole that a gasketed device cannot seal
against, and D-047 treats every one of these five as needing a gasketed device.

**7-04. Mark the bottom-face cable entries at the positions and spacings D6 states.**
BLOCKED. Missing: CBL-01 is OPEN and its position half needs the wall layout, M-02.
Owner: INTERCONNECT places them within the face; MAIN-PANEL owns the face, which is
already stated: **every cord grip is on the BOTTOM face.**

**7-05. Cut each bottom-face entry.**
BLOCKED. Missing: as 7-04.

**7-06. Mark and cut the receptacle openings in the face D3 states.**
BLOCKED. Missing: D3 does not exist and no file read for this book states which face
carries them. Owner: MAIN-PANEL. **What is decided is D-046: the receptacles are
panel mounted in the enclosure face and cords plug into them from outside, so no
receptacle cord is fed through a grip.**

**7-07. Deburr every hole you have cut.**
ACCEPT: run a finger round each edge and feel nothing that catches.
WHY: a burr on a device hole cuts the gasket of the device that seals it, and the cut
is on the underside where nobody will look again.

**7-08. Turn the enclosure over and shake every particle of swarf out of it.**
ACCEPT: hold it to the light, run a hand over the inside, and find nothing.
WHY: **this is the last moment the box is empty.** Swarf that stays in now ends up on
a contact face or across a terminal, and a short between two clamps built by a metal
chip passes every visual check.

**7-09. Fit a cord grip to each bottom-face entry, sized to the cable D6 selects for
that entry.**
BLOCKED. Missing: the cable selections in D6 section 5 are requirements and search
terms, not parts, and the entry positions are 7-04's blocker. Owner: the owner runs
the lookups under G-15; INTERCONNECT selects.

**7-10. Fit the top-face devices' gaskets and blanks so that no top-face hole is left
open.**
BLOCKED. Missing: as 7-02, and F-025's top-face half is live - D-110 closes the
enclosure's own rating and **explicitly does not close the question of each top-face
device's rating in an upward-facing orientation.** Owner: MAIN-PANEL.
WHY THE TOP FACE IS TREATED DIFFERENTLY FROM EVERY OTHER FACE: D-092 and D-110. **The
assembly's rating is set by its worst penetration regardless of what the box is
rated**, and five upward-facing holes are the worst penetration. The design sheds
rather than seals, so anything that lands on that face has to run off it.

---

## 8. PREPARE THE TWO PUMP BOXES

**MUST BE TRUE BEFORE THIS SECTION STARTS:**
- BB-05, section 3.
- BB-09, section 6.

**TRUE AFTER IT ENDS:**
- **BB-11.** Both pump box bodies have every penetration they will ever have, cut,
  deburred and fitted; both lids have their head penetrations; both are clean.

**Do both boxes together, one operation at a time across the pair.** They are one
build and not a mirrored pair: **left and right are the same on both boxes**, per
subsystems/entry-faces.md section 2.3. A mirrored pair is two builds of one thing.

**8-01. Take the lid off each box and set both lids aside.**
ACCEPT: two open box bodies and two lids, each lid marked with the box it came off.

**8-02. Mark the bottom-face entries on each box body, at the positions and spacings
D6 states.**
BLOCKED. Missing: CBL-02 is OPEN and its position half needs the wall layout, M-02.
Owner: INTERCONNECT places them within the face.
**THE FACE AND THE ORDER ARE ALREADY DECIDED AND ARE NOT OPEN:** bottom face, both
boxes, every cable, and reading the bottom face left to right as you stand at the box
facing the lid, the motor supply entry is at the left end and the step-and-direction
entry is at the right end. That is subsystems/entry-faces.md section 2.3 and this
book does not restate its reasoning.

**8-03. Cut each bottom-face entry.**
BLOCKED. Missing: as 8-02.

**8-04. Mark the head penetrations on each lid.**
BLOCKED. Missing: CBL-05 is an OPEN interface row. Owner: PUMP-BOXES owns the
penetration, DOSING owns the tubing through it.

**8-05. Cut each head penetration.**
BLOCKED. Missing: as 8-04.

**8-06. Deburr every hole in both bodies and both lids.**
ACCEPT: run a finger round each edge and feel nothing that catches.

**8-07. Clean every particle out of both bodies and off both lids.**
ACCEPT: hold each to the light and find nothing.

**8-08. Fit a cord grip to each bottom-face entry, sized to the cable D6 selects.**
BLOCKED. Missing: as 7-09.

**NOTHING ENTERS A PUMP BOX LID EXCEPT A HEAD, AND NOTHING IS FITTED TO THE TOP OR
THE SIDES OF EITHER BOX.** subsystems/entry-faces.md section 2.2 gives two reasons
and either is sufficient: **the lid is a heavy serviceable assembly that is removed as
a unit, so a cable entering it tethers the one part of the box that has to come off**;
and the lid is already committed as the head penetration and a sealing face. The top
is D-047's shed rule. **If you find yourself wanting a hole in a lid or a top, stop:
that is a decision, not a step.**

---

## 9. PREPARE THE DISPLAY BOX

**MUST BE TRUE BEFORE THIS SECTION STARTS:**
- BB-05, section 3.
- BB-09, section 6.

**TRUE AFTER IT ENDS:**
- **BB-12.** The display box body has every penetration it will ever have, cut,
  deburred and fitted, including the USB-C bulkhead; the box is clean.

**9-01. Open the box and take out the back plate.**
ACCEPT: the box is empty and the display cutout's gasket is undisturbed.
WHY: **the gasketed display cutout is the youngest part in this assembly** under
D-092's own argument, and every operation below throws particles.

**9-02. Mark the bottom-face entries at the positions and spacings D6 states.**
BLOCKED. Missing: CBL-03 is OPEN and its position half needs the wall layout, M-02.
Owner: INTERCONNECT places them within the face.
**THE FACE AND THE ORDER ARE DECIDED:** bottom face, every cable, and the order
reading left to right as you stand at the box facing the display is in
subsystems/entry-faces.md section 3.3. **Two of those entries must not become
adjacent and one gap between two of them is deliberate and is not even.** The rule
and the failure it prevents are in that file and in D6 and are not restated here.

**9-03. Cut each bottom-face entry.**
BLOCKED. Missing: as 9-02.

**9-04. Cut the opening for the panel-mount USB-C bulkhead at the position D6 gives
it, at the right-hand end of the bottom face.**
BLOCKED. Missing: as 9-02, and the bulkhead itself is a requirement and a search term
in D6 section 5, not a part. Owner: the owner runs the lookup under G-15.
WHY IT IS A BULKHEAD AND NOT A GRIP: D-162. **A USB-C connector will not pass a grip
bore, and cutting and re-terminating a USB-C cable is not a thing anyone should do.**
If you are holding a grip and a USB-C cable, you are about to solve this the
expensive way.

**9-05. Deburr every hole.**
ACCEPT: run a finger round each edge and feel nothing that catches.

**9-06. Clean every particle out of the box and off the back plate.**
ACCEPT: hold both to the light and find nothing.

**9-07. Fit a cord grip to each bottom-face entry and the bulkhead to its opening.**
BLOCKED. Missing: as 9-02 and 9-04.

---

## 10. MOUNT THE FOUR ENCLOSURES

**MUST BE TRUE BEFORE THIS SECTION STARTS:**
- BB-08, section 6.
- BB-10, section 7.
- BB-11, section 8.
- BB-12, section 9.

**TRUE AFTER IT ENDS:**
- **BB-13.** The main panel, pump box A, pump box B and the display box are mounted
  on the wall, empty, with backplates out and lids off.

**THE ENCLOSURES GO UP EMPTY AND THEY GO UP BEFORE THE TANKS COME INTO THE ROOM.**
Sections 13, 14 and 15 populate them afterwards.
WHY BOTH: **a populated plate is heavy and is lifted at height**, and a tank standing
in its final position is between you and the wall for every remaining wall operation.

**10-01. Transfer each mounting position from the layout onto the wall and mark it.**
BLOCKED. Missing: BB-08, section 6. Owner: as section 6.

**10-02. Fix the main panel to the wall.**
BLOCKED. Missing: the mounting position, and the fixings, which are a D7 line.
**REQUIREMENT AND SEARCH TERM, since no file read for this book states one:** a
fixing suited to the wall construction recorded in 5-02, rated for the enclosure's
loaded weight in shear, in a room where water moves tank to tank. Search:
`enclosure wall mounting bracket load rating`; `fastener corrosion resistance damp
location`. **The line belongs in D7 and the lookup is the owner's under G-15.**

**10-03. Fix pump box A to the wall with its back to the wall and its lid facing the
room.**
BLOCKED. Missing: as 10-02.
WHY THE LID FACES THE ROOM AND NOT UP: subsystems/entry-faces.md section 2.1. **The
head is outside the box and the motor body is inside it, so every tubing joint sits
on the lid. A lid facing up puts the whole wet assembly directly above the box's own
sealing face and its head penetrations, and puts a tube change over them.** It also
puts the head at hand height for the tube change, which is a thing that happens for
the life of the machine.

**10-04. Fix pump box B to the wall the same way round as box A.**
BLOCKED. Missing: as 10-02.
WHY THE SAME WAY ROUND: they are one build, not a mirrored pair.

**10-05. Fix the display box to the wall with its display facing the operator.**
BLOCKED. Missing: as 10-02, and M-03 is an OPEN interface row on reach and sightline.
Owner: DISPLAY-BOX.

**10-06. Confirm each enclosure sits true and is not pulled out of square by its
fixings.**
BLOCKED. Missing: nothing to check until 10-02 to 10-05 are done.
WHY IT IS ITS OWN STEP: a box racked by an over-tightened fixing will not seal on its
own gasket, and the gasket is the part that gets blamed.

---

## 11. ASSEMBLE THE MANIFOLD

**MUST BE TRUE BEFORE THIS SECTION STARTS:**
- BB-03, section 2.

**TRUE AFTER IT ENDS:**
- **BB-14.** The manifold is assembled between its two unions, its probe section
  vertical and ahead of every injection port, its solvent joints cured, and it is off
  the wall.

**THIS IS BENCH WORK AND IT ENDS AT A CURE.** Section 12 does not start until the
cure is finished, and it says so as its own precondition. **Do not carry on working
this assembly while a joint is curing.**

**11-01. Lay the manifold out dry, end to end, before any cement is opened.**
ACCEPT: the probe section is vertical when the assembly is held in its mounting
orientation, and every injection port is downstream of every probe position.
WHY: **G-10.** Probes sit first in line in a vertical section, ahead of every
injection point, **so a bubble cannot corrupt a reading and no injectate reaches a
probe before mixing.** A dry lay-up is the last moment this is free to correct.

**11-02. Mark each joint's alignment across the joint line while the assembly is
still dry.**
ACCEPT: every joint carries a mark on both sides that lines up.
WHY: solvent cement gives you seconds, not minutes. A joint made a quarter turn out
puts an injection port or a probe boss facing a wall, and it cannot be taken apart.

**11-03. Take the dry assembly apart.**
ACCEPT: every piece is loose and every alignment mark is still readable.

**11-04. Make each solvent-welded joint in turn, to the alignment marks.**
BLOCKED for the port arrangement. Missing: **DOSING's injection port arrangement is
an open item** - how a port is made in PVC, and whether ports need a check to stop
backflow into a dose line when its head is idle. Owner: DOSING returns the
requirement.
ACCEPT for the joints that are not blocked: the marks line up and the joint is home
to its stop.

**11-05. Fit the union at each end of the manifold body.**
BLOCKED. Missing: **FL-03 and FL-04 are OPEN interface rows** and the union type is
not settled. Owner: WATER and DOSING jointly, BOSS freezes.
WHY THE UNIONS ARE NOT OPTIONAL: they are the manifold's scope boundary at both ends.
DOSING owns everything between them and WATER owns everything outside them, and a
manifold solvent-welded into the loop cannot be taken out for service without cutting
somebody else's pipe.

**11-06. Fit the probe wet fittings to the probe section.**
BLOCKED. Missing: **DOSING's probe wet fitting requirement is an open item**, one per
EZO probe body, and S-11 is an OPEN interface row. Owner: DOSING returns the
requirement and the search term; the owner runs the lookup under G-15.

**11-07. Leave the assembly undisturbed until the cement's own instruction says the
cure is complete.**
ACCEPT: the time the cement's label states has elapsed and nothing has been moved.
WHY THIS SECTION ENDS HERE: **a cure is a wait, and a wait in the middle of a section
is where a builder is sent away and the next steps quietly assume he did not go.**
Section 12 restates the cure as a precondition so that coming back to the book puts
you in the right place.

---

## 12. MOUNT THE MANIFOLD AND THE JUG STATIONS

**MUST BE TRUE BEFORE THIS SECTION STARTS:**
- BB-08, section 6.
- BB-14, section 11, **including its cure.**

**TRUE AFTER IT ENDS:**
- **BB-15.** The manifold is mounted on the wall in its layout position, probe
  section vertical.
- **BB-16.** Every jug station is fixed in its layout position and carries its
  permanent channel token.

**12-01. Fix the manifold to the wall at its layout position.**
BLOCKED. Missing: BB-08, section 6. The manifold's position is half of M-02 and DOSING
and PUMP-BOXES claim the same wall space, with the tubing between them setting the
spacing. Owner: as section 6.

**12-02. Confirm the probe section is vertical as mounted.**
BLOCKED. Missing: nothing to check until 12-01 is done.
WHY IT IS CHECKED AGAIN AFTER MOUNTING: G-10's whole point is that a bubble cannot sit
against a probe. **A probe section that was vertical on the bench and is not vertical
on the wall satisfies nothing**, and the assembly is heavy enough to pull a bracket
out of true as it is tightened.

**12-03. Fix each jug station in its layout position.**
BLOCKED. Missing: BB-08, and DOSING's jug placement item is open - height relative to
the head, so a head is not asked to lift more than it can and so a jug change is
possible without a tool. Owner: DOSING.

**12-04. Apply the permanent channel token to each jug station.**
BLOCKED. Missing: the token's carrier is a requirement and a search term in D6 section
5 and is not a part yet, and **which product and which role a channel carries is bound
at C-09 and is not knowable before commissioning.** Owner: CONTROL-SOFTWARE declares
the token per S-19 and D-021; DOSING carries it on the station.
WHY THE STATION IS TOKENED AND NOT THE JUG ALONE: G-17 makes a jug dedicated to its
channel for life, and G-18 puts the change break point at the jug. **A station with no
token is a station where the right jug can be put in the wrong place**, and S-19's own
row says a crossed pair confirms itself and passes every check in this build.

---

## 13. THE MAIN PANEL BACKPLATE

**MUST BE TRUE BEFORE THIS SECTION STARTS:**
- BB-05, section 3.
- BB-13, section 10.

**TRUE AFTER IT ENDS:**
- **BB-17.** The main panel backplate is populated and installed in the mounted
  enclosure, with the ground bar fitted and nothing landed on it.

**EVERY CUT IN THIS SECTION HAPPENS ON A BARE PLATE.** Rail and duct are cut to
length before a single device goes on.
WHY, AND IT IS ONE OF THE FIVE DEFECTS THIS BOOK IS WRITTEN AGAINST: **a duct cut
over a populated plate showers a plate full of open terminals with plastic swarf and
metal filings.** A builder who has already fitted the devices will reasonably decide
to cut the duct in place rather than strip the plate back, because stripping it back
looks like the wasteful option. It is not.

**13-01. Put the bare backplate on the bench.**
ACCEPT: it is off the wall, empty, and you can reach both ends of it.

**13-02. Mark the rail runs and the duct runs on the bare plate at the positions D3
states.**
BLOCKED. Missing: D3 does not exist. **The plate layout - which device on which rail,
in what order - has not been returned by any subsystem.** Owner: MAIN-PANEL.

**13-03. Cut each rail to length on the bare plate.**
BLOCKED. Missing: as 13-02.

**13-04. Cut each duct to length on the bare plate.**
BLOCKED. Missing: as 13-02.

**13-05. Clean every particle off the plate before anything is fixed to it.**
ACCEPT: hold the plate to the light and find nothing.

**13-06. Fix each rail to the plate.**
BLOCKED. Missing: as 13-02.

**13-07. Fix each duct to the plate.**
BLOCKED. Missing: as 13-02.

**13-08. Fix the copper ground bar to the plate.**
BLOCKED. Missing: the bar is a requirement and a search term in D6 section 5 and has
not been bought. Owner: MAIN-PANEL provides the bar; the owner runs the lookup under
G-15.
WHY IT GOES ON EARLY AND EMPTY: **CBL-07, closed by D-165. The bar is the SINGLE
BONDING POINT in this panel and nothing bonds anywhere else.** It is written down
because a builder who finds a convenient screw will use it. Fitting the bar now means
that when section 31 lands a green conductor there is somewhere for it to go, and
D4's page 1 lands the whole bar last and all together.

**13-09. Fit each device to its rail, by the name written on it in section 3.**
BLOCKED. Missing: as 13-02.
WHY BY NAME AND NEVER BY POSITION: **G-28 and T-013.** Relays that look alike have
different contact duties, and a step that names a device by its place in a list
follows the index and not the meaning as soon as the list changes. **D2's roster is
the only source of which device this is.**

**13-10. Lift the populated plate into the mounted enclosure and fix it.**
BLOCKED. Missing: nothing to lift until 13-06 to 13-09 are done.

**13-11. Confirm nothing on the plate fouls a face device or a cable entry.**
BLOCKED. Missing: as 13-10.
WHY IT IS CHECKED NOW: this is the last moment before conductors are in the way. A
device that fouls a gland is moved with one screwdriver today and with a stripped
panel in section 31.

---

## 14. THE PUMP BOXES: LIDS, MOTORS, HEADS AND DRIVERS

**MUST BE TRUE BEFORE THIS SECTION STARTS:**
- BB-05, section 3.
- BB-11, section 8.
- BB-13, section 10.

**TRUE AFTER IT ENDS:**
- **BB-18.** Each pump box carries its motors and heads on its lid and its drivers on
  its box body, every driver in a box set the same way round, with the lids not yet
  fitted.

**Do both boxes together, one operation at a time across the pair.** Box A carries
CH1 to CH4 and box B carries CH5 to CH8, per D-178.

**14-01. Put each lid on the bench with its outside face up.**
ACCEPT: two lids, each still marked with the box it came off in 8-01.

**14-02. Fit each motor body to the inside of its lid.**
BLOCKED. Missing: D3 does not exist and no file read for this book states the motor
positions on the lid. Owner: PUMP-BOXES.

**14-03. Fit each head to its motor on the outside of the lid.**
BLOCKED. Missing: as 14-02, and CBL-05's penetration is 8-04's blocker.

**14-04. Apply the permanent channel token to the lid at each head's penetration.**
BLOCKED. Missing: the token carrier, as 12-04, and the channel assignment is bound at
C-09. Owner: PUMP-BOXES owns the carrier, DOSING owns the scheme, CONTROL-SOFTWARE
declares the token.
WHY IT GOES ON THE LID FACE AND NOT INSIDE: it has to be readable with the box closed,
from the operator's standing position, and not obscured by the tubing it identifies.

**14-05. Fit each driver to the BOX BODY, not to the lid.**
BLOCKED. Missing: D3 does not exist and the driver positions in the box are not
stated. Owner: PUMP-BOXES.
WHY THE BODY AND NOT THE LID: **the lid is a heavy serviceable assembly carrying four
motor bodies and it is removed as a unit.** Anything landed on it moves with it and
drags wiring, which is already on file as the reason the pull-down landing mounts to
the body.

**14-06. Set every driver in a box the same way round, so that every power block
faces one end of the box and every logic header faces the other.**
BLOCKED. Missing: as 14-05.
WHY, AND IT IS THE REASON THE ENTRY ORDER IN SECTION 8 IS WHAT IT IS: the motor supply
enters at the power-block end and the step and direction enter at the logic end, so
**nothing crosses the box.** An arcing break into drivers with bulk capacitors and
the logic pins of drivers whose severed direction input is the worst outcome in the
whole fail-safe sweep are the two most different things in this box, and separation
inside the box is the only adjacency remedy PUMP-BOXES has that costs nothing. **One
driver turned round undoes it silently.**

**14-07. Fit each driver's heatsink.**
BLOCKED. Missing: the heatsink is a D7 line and no file read for this book states it
as bought. Owner: PUMP-BOXES states the requirement; the owner runs the lookup under
G-15.
WHY IT IS NOT OPTIONAL AND WHY IT CANNOT BE ADDED LATER: **the motor bodies and the
drivers sit in one sealed plastic box and nothing has measured the temperature
rise.**
C-15 is the measurement and its own precondition is boxes populated and closed with
heatsinks fitted, **so a box built without them cannot even be measured.** G-06, one
pump at a time, is a thermal constraint and stays mandatory until C-15 exists.

**14-08. Fit the pull-down landing to the box body.**
BLOCKED. Missing: the landing is not a stated part and S-10 is an OPEN interface row.
Owner: PUMP-BOXES, per D-043.
WHY THE LANDING IS FITTED HERE AND THE PULL-DOWNS THEMSELVES ARE LANDED IN SECTION
31: **a pull at the display end does nothing once the conductor is cut**, so the
component has to be at the driver end, inside this box. Landing it is a conductor
fact and belongs to D4. **Fitting the thing it lands on is this section's, because a
conductor cannot be landed on a part a later step installs.**

**14-09. Leave both lids off.**
ACCEPT: both boxes are open and both lids are on the bench, each marked with its box.
WHY: section 31 lands conductors inside these boxes and section 32 closes them. **A
lid fitted now is a lid taken off again, and every removal is a chance to trap a
conductor in a sealing face.**

---

## 15. THE DISPLAY BOX BACK PLATE

**MUST BE TRUE BEFORE THIS SECTION STARTS:**
- BB-05, section 3.
- BB-13, section 10.

**TRUE AFTER IT ENDS:**
- **BB-19.** The display box back plate is populated and installed, the three EZO
  circuits have been set and recorded per C-14, and the cover is not fitted.

**15-01. Put the bare back plate on the bench.**
ACCEPT: it is out of the box and empty.

**15-02. Fit the Pi to the back plate at the position D3 states.**
BLOCKED. Missing: D3 does not exist. Owner: DISPLAY-BOX.

**15-03. Fit each EZO carrier board to the back plate.**
BLOCKED. Missing: as 15-02.

**15-04. Fit the pH circuit and the EC circuit each to a carrier, and the RTD circuit
to the back plate on no carrier.**
BLOCKED. Missing: as 15-02.
**S-11 is an OPEN interface row.** DOSING owns the wet fitting and the probe
placement, DISPLAY-BOX owns the carriers and the I2C side, INTERCONNECT owns the cable
run.

**15-05. Fit the logic board to the back plate.**
BLOCKED. Missing: **the logic board does not exist yet.** Owner: DISPLAY-BOX. D4
records it as the blocker behind a group of its steps.

**15-06. Set each of the three EZO circuits from UART to I2C, and record which pin and
which procedure was used for each one, per C-14.**
BLOCKED. Missing: C-14 is the procedure and it is D8's to stage. **This book states
only when it happens.** Owner: the owner, with the circuits in hand.
**WHEN IT HAPPENS IS THE POINT AND IT IS THIS BOOK'S FACT: BEFORE THE DISPLAY BOX IS
CLOSED.** C-14's own note says so, and until it is done the Pi cannot read any probe.
It is three different procedures, not one repeated three times, and **without a
per-circuit record nobody can repeat it after a board swap.** The procedure and the
record are C-14's and are not restated here.

**15-07. Lift the populated back plate into the mounted box and fix it.**
BLOCKED. Missing: nothing to lift until 15-02 to 15-05 are done.

**15-08. Leave the cover off.**
ACCEPT: the box is open and the cover is set aside with its gasket undisturbed.
WHY: section 31 lands conductors on this plate and section 32 closes the box. **The
gasketed display cutout is the youngest part in the assembly and every fitting and
removal of the cover is a chance to damage it.**

---

## 16. SET THE TANKS IN POSITION

**MUST BE TRUE BEFORE THIS SECTION STARTS:**
- BB-03, section 2.
- BB-08, section 6.
- BB-13, section 10.

**TRUE AFTER IT ENDS:**
- **BB-20.** Both tanks stand in their layout positions, empty, dry and level, with
  the far side of each rim reachable.

**THE TANKS COME INTO THE ROOM AFTER THE WALL IS MOUNTED AND BEFORE ANYTHING IS CUT
IN THEM.** Sections 18 to 23 all work over the rim of a tank standing where it will
stand for the life of the machine.

**16-01. Stand the storage tank on its support at its layout position.**
BLOCKED. Missing: BB-08, section 6, and the support is a D7 line.
**REQUIREMENT AND SEARCH TERM, because no file read for this book states one:** the
storage tank is cone bottom and open top, so **it cannot stand on its own bottom** and
needs a support that carries it full, leaves its outlet reachable, and stands on the
floor the drain track runs across. Search: `cone bottom tank stand`; `conical tank
stand load rating`. **The line belongs in D7 and the lookup is the owner's under
G-15.**

**16-02. Stand the day tank at its layout position.**
BLOCKED. Missing: BB-08, section 6.

**16-03. Confirm each tank is level.**
BLOCKED. Missing: nothing to check until 16-01 and 16-02 are done.
WHY LEVEL MATTERS MORE HERE THAN IT LOOKS: **every trip height in section 19 is
measured up a standpipe from an end cap face, and every one of them is a height in
the water.** A tank standing out of level puts every float mark at a different depth
on one side of the tank from the other, and nothing in this system measures a level to
tell you.

**16-04. Confirm the far side of each tank's rim can be reached.**
BLOCKED. Missing: as 16-03.
WHY: D-131 puts a person's hands on a standpipe tie over the rim at commissioning and
at every level adjustment afterwards, **with both day tank pumps running.** A rim you
cannot reach turns a routine adjustment into a two-person job forever.

**16-05. Confirm each tank is empty and dry inside.**
BLOCKED. Missing: as 16-03.
WHY: sections 18 and 20 cut and drill on and around these tanks, and section 23 hangs
a standpipe in them. **Water in a tank you are about to cut into is water you will be
lifting out.**

---

## 17. BUILD ONE STANDPIPE PER TANK

**MUST BE TRUE BEFORE THIS SECTION STARTS:**
- BB-03, section 2.
- BB-20, section 16.

**TRUE AFTER IT ENDS:**
- **BB-21.** One standpipe exists per tank, each with a solvent-welded end cap at its
  bottom, cured.

**THIS IS D-121'S METHOD AND SECTIONS 17 TO 23 ARE THE WHOLE OF IT.** One rigid pipe
per tank carrying every float and every cord, hung off the rim, **with nothing hanging
off a float body.**

**WHY THE METHOD EXISTS AT ALL, because a builder will otherwise hang a float from its
own cord and it will look fine:** nothing in this system measures a level. **A float
that has moved is invisible**, and under D-114 the fill-stop float is the only thing
stopping the fill. A cord-hung float is a float whose position is a suggestion.

**THE PIPE IS PVC.** D-121 as confirmed by the owner on 2026-09-05: the same material
as everything else in the wet path.
WHY IT IS WRITTEN DOWN RATHER THAN LEFT TO THE BUILDER: **a metal standpipe would be
an unbonded conductive part in a tank with line-voltage cords tied to it.** The material
choice removes that failure instead of managing it. The alternative was a bonding
conductor, a landing on the local bar, a step, a check that it is still bonded, and a
failure mode where it is not. **If you are holding a metal pipe because it is stiffer,
that is what you are buying.**

**17-01. Cut one pipe per tank.**
BLOCKED for the length. Missing: **this book states no dimension.** The length is set
by the tank in front of you and by the trip heights, which do not exist until section
19.
**THE RULE THAT SURVIVES EVERY NUMBER BEING WRONG, so the cut can be made when the
heights arrive:** the pipe stands at the bottom of the tank and its top clears the rim
by enough to take the U-bolt and to turn the cords over the rim without a sharp bend.
**Cut long and cut again if you must. A pipe cut short is a pipe bought twice.**

**17-02. Deburr the cut end of each pipe.**
ACCEPT: run a finger round the bore and the outside and feel nothing that catches.
WHY: every cord in section 22 is drawn past this end at some point, and a burr on a
pipe is a cut in a cord jacket that nobody sees until it is in the water.

**17-03. Dry-fit an end cap to the bottom of each pipe.**
ACCEPT: the cap seats to its stop and the pipe stands square on the cap face.
WHY THE CAP IS AT THE BOTTOM AND WHY IT IS FLAT: **every trip height in this build is
measured from the end cap face**, D-131. The cap is the datum for the whole tank.

**17-04. Solvent-weld the end cap to each pipe.**
ACCEPT: the cap is home to its stop and the joint has an unbroken bead all round.

**17-05. Leave both pipes undisturbed until the cement's own instruction says the cure
is complete.**
ACCEPT: the time the cement's label states has elapsed and neither pipe has been
moved.
WHY THIS SECTION ENDS HERE: as section 11. **A wait in the middle of a section is
where a builder is sent away and the next steps assume he did not go.** Section 18
restates the cure as its own precondition.

---

## 18. HANG EACH PIPE ONCE AND TAKE ITS DATUM

**MUST BE TRUE BEFORE THIS SECTION STARTS:**
- BB-20, section 16.
- BB-21, section 17, **including its cure.**

**TRUE AFTER IT ENDS:**
- **BB-22.** Each pipe's U-bolt is fitted and its hang position on the rim is set;
  the offset between the pipe's end cap face and the tank floor is measured once per
  tank and recorded; and each pipe is back out of its tank.

**THIS SECTION EXISTS TO PRODUCE ONE MEASUREMENT AND IT IS THE CHEAPEST ITEM IN THE
WHOLE BUILD.** It costs one dry hang per tank. **What it prevents is the defect D-129
found in the 1st Edition set: the same numbers stated against two different datums.**

**THE DEFECT IN PLAIN TERMS, because it is about to become live in this build for the
first time:** D-131 fixes every float mark to **the standpipe's end cap face.** A
bulkhead is a hole in a **tank wall.** An air gap is measured from the **tank's flood
rim.** Those are three different datums on two different objects, and the offsets
between them are whatever they happen to be.

**18-01. Fit a U-bolt with a backing plate over the tank's drum lip, to each pipe.**
BLOCKED. Missing: the U-bolt and the backing plate are D7 lines and no file read for
this book states them as bought. Owner: WATER states the requirement; the owner runs
the lookup under G-15.
**REQUIREMENT AND SEARCH TERM:** a U-bolt and a backing plate that clamp over the
tank's lip without crushing it, in a material that will stand in a fertiliser solution
atmosphere. Search: `U-bolt with backing plate pipe clamp`; `tank rim pipe mounting
bracket`.

**18-02. Tighten the U-bolt nuts underneath the lip, snug and not crushed.**
BLOCKED. Missing: as 18-01.
WHY IT IS WRITTEN AS ONE STEP WITH THE ALLOWANCE IN IT: D-131 states the whole of it
in one breath - **a U-bolt with a backing plate over the drum lip, nuts underneath,
snug and not crushed.** A crushed lip on a bought tank is not recoverable, and a
builder tightening to feel will keep going until something stops moving.

**18-03. Stand each pipe in its tank and hang it on its U-bolt.**
BLOCKED. Missing: as 18-01.
ACCEPT when unblocked: the pipe stands at the bottom of the tank, hangs from the rim,
and nothing else in the tank carries any part of its weight.

**18-04. Measure the offset between the end cap face and the tank floor, once, for
this tank.**
BLOCKED. Missing: nothing to measure until 18-03 is done.
WHY THIS ONE MEASUREMENT IS ITS OWN STEP: **it is the only thing that ties the
standpipe's datum to the tank's datum**, and every height in section 19 is written
against one or the other. **It is measured once per tank and recorded before any
height in this build is written down.** WATER's return names it as the cheapest item
in that entire pass.
WHY IT MAY NOT BE ZERO: the storage tank is cone bottom. A pipe standing in it may sit
on a boss, on the cone, or clear of the floor entirely, **and the same tether length
gives a very different volume band at different heights in that vessel.**

**18-05. Record the offset against the tank it belongs to.**
BLOCKED. Missing: as 18-04.
ACCEPT when unblocked: the record names the tank, the offset, the units, and the two
faces it was taken between.
WHY THE TWO FACES ARE NAMED IN THE RECORD: a figure with no datum is the defect this
section exists to prevent. Writing the number without writing what it was measured
between reproduces it exactly.

**18-06. Lift each pipe back out of its tank and put it on the bench.**
BLOCKED. Missing: as 18-03.
WHY THE PIPE COMES BACK OUT: section 20 cuts a hole in each tank wall and section 21
marks the pipes. **Cutting a tank wall with a standpipe in the tank puts swarf down
the tank and onto a pipe that will carry floats**, and marking a pipe is bench work
that is done badly leaning over a rim. **The cost is one lift per tank and it is
paid here on purpose.**

---

## 19. SET THE LEVELS

**MUST BE TRUE BEFORE THIS SECTION STARTS:**
- BB-22, section 18.

**TRUE AFTER IT ENDS:**
- **BB-23.** Every height in each tank's freeboard stack is decided and recorded: the
  fill band, the four trip heights, the high-high mark, the overflow invert, the rim,
  and the air gap.

### THIS SECTION IS A DECISION AND NOT A STEP, AND IT IS BLOCKED.

**Nothing is cut and nothing is marked until it is finished.** Sections 20, 21 and 25
each restate BB-23 as their own precondition, and each of them is irreversible.

**BLOCKED. Missing: C-11, the day tank working volume and the actual fill band, both
ends with the reason for each.** Owner: the owner measures, WATER states what sets
each end. **The figure on the parts list is nominal vessel capacity and must not be
used as a working volume.**

**BLOCKED. Missing: the differential each position needs.** Owner: WATER. **D-131:
the differential is set by tether length, so it is a thing this build chooses rather
than a thing the part provides, and no float datasheet can supply it.** The
requirement per position is in subsystems/water-float-requirement.md section 1.0(e)
and is not restated here.

**BLOCKED. Missing: the surface disturbance amplitude at each position.** Owner: the
owner, as an observation taken while filling slowly. It is caused by things WATER
places - the return drop's landing point, the transfer discharge, and two
continuously running submersibles in the day tank - **and nothing has measured it and
no datasheet contains it.**

**BLOCKED. Missing: whether the freeboard stack closes at all.** Owner: WATER, and it
cannot be added up until the differentials are chosen. **Everything from the top of
the fill band upward has to fit inside a tank height that is already bought.**

**BLOCKED. Missing: the overflow's capacity requirement, which sets its size.** Owner:
WATER states it, the owner measures the two flows it depends on. **It must swallow the
full inflow with the fill-stop failed**, which for storage is the solenoid's flow at
the actual supply pressure and for the day tank is the transfer pump's delivered flow
into a full tank. **Neither number is on file and neither may be inherited from the
manifold's diameter**, which is a different duty.

### The order the decisions are made in, which is this book's fact and is not blocked

**Taken from subsystems/water-float-requirement.md section 2.2, which is where the
ordering was worked out. The order stands whatever the numbers turn out to be.**

**19-01. Decide the working volume and the fill band, both ends, with the reason for
each.**
BLOCKED. Missing: C-11, as above.
WHY THIS IS FIRST AND WHY IT IS NOT CIRCULAR: C-11's own blocked-on column says
"floats chosen and set", which reads as though the band waits on the floats. **It does
not. The band is a decision about the water and the float marks follow it.**

**19-02. Decide the four trip heights for this tank, with the differential of each,
measured from the end cap face.**
BLOCKED. Missing: as above.
**ONE POSITION IS A CONFLICT AND NOT A REQUIREMENT, and it must be recognised before a
mark is chosen and not after:** the day tank low-low needs the largest differential of
the eight, **because low level is when the two submersibles are nearest the surface
and vortexing is worst, and it is the position with the least depth available to spend
on a tether.** It may force the low-low trip higher than the pump's bare submergence
limit. That is resolved by geometry and not by a part.

**19-03. Decide the high-high mark, which is the topmost of item 19-02's marks.**
BLOCKED. Missing: as above.

**19-04. Decide the overflow's landing height, above the high-high mark.**
BLOCKED. Missing: as above.
WHY ABOVE AND NOT BELOW, AND THIS IS THE ONE THAT WILL BE ARGUED WITH WHILE SOMEBODY
IS HOLDING A HOLE SAW: **the high-high is the instrumented protection and the overflow
is the uninstrumented one.** D-134. Above, the high-high trips first and the machine
finds out, and the overflow is the second line for when the high-high fails too.
Below, **the overflow silently absorbs the failure and the high-high never trips - the
protection works and nobody is told, every time, forever.** If the freeboard stack
does not close, **the tempting fix is to drop the overflow below the high-high and
recover the height, and that is exactly the trade D-134 forbids.** The thing that
gives is the working volume.

**19-05. Decide the tank rim and the fill air gap above it.**
BLOCKED. Missing: as above, and one question the owner has not been asked.
**THE QUESTION, and it doubles or halves this half of the work:** D-138's stated reason
for the air gap is backflow protection of the municipal supply, **and only the storage
tank is connected to municipal supply.** On that reason the air gap attaches to the
storage fill only. There is a separate reason to air-gap the transfer discharge into
the day tank - it prevents back-siphoning the day tank into storage when the transfer
pump stops - **but that is a different requirement with a different justification and
WATER declined to merge them.** Owner: the owner.

**19-06. Record every decided height against the tank it belongs to, and against the
datum it was measured from.**
BLOCKED. Missing: as above.
ACCEPT when unblocked: every height on the record names its tank, its datum face, and
its units.
WHY THE DATUM IS RECORDED WITH EVERY SINGLE HEIGHT AND NOT ONCE AT THE TOP OF THE
SHEET: a height that travels without its datum is the 1st Edition's defect. **Three
datums are in play in one tank** and section 18 measured the offset between two of
them precisely so that this record can be unambiguous.

---

## 20. CUT THE OVERFLOW BULKHEADS

**MUST BE TRUE BEFORE THIS SECTION STARTS:**
- BB-20, section 16.
- BB-23, section 19.

**TRUE AFTER IT ENDS:**
- **BB-24.** Each tank carries one overflow bulkhead at its decided invert, sealed,
  and each tank is clean of swarf.

**THIS IS THE MOST IRREVERSIBLE OPERATION IN THE BUILD.** Two holes in two bought
tanks. **A bulkhead sited before the heights are settled is a scrapped tank**, which
is why BB-23 is this section's precondition and why section 19 is a section rather
than a note.

**20-01. Confirm the standpipe is out of this tank before anything is cut.**
ACCEPT: the tank is empty of everything.
WHY: section 18 took it out for this reason. **Swarf in a tank is swarf on a float.**

**20-02. Find a flat land on the tank wall at the decided invert height.**
BLOCKED. Missing: **whether either tank has a flat moulded boss near the top is a
question for the owner with the tanks in front of him.** Owner: the owner.
WHY IT IS A STEP AND NOT AN ASSUMPTION: **a gasket needs a flat land, and the upper
wall of a cylindrical tank is a curve.** A bulkhead gasket seating on a curve is a
leak that appears later. It changes the fitting class and it may change the landing
height, **which is why it is asked before the hole and not after.**

**20-03. Mark the hole centre at the decided invert height, on the flat land.**
BLOCKED. Missing: BB-23 and 20-02.

**20-04. Confirm the marked position is clear of the standpipe's hang point, the
return drop's landing, the transfer discharge, the submersible cords and every
penetration and hanger M-01 carries.**
BLOCKED. Missing: BB-08, section 6, and M-01's contents.
WHY THIS CHECK IS HERE AND NOT LATER: **the same upper wall and rim carry all of
those**, and M-01 grows by one item with this bulkhead. **The overflow must not sit
under the return drop's splash and must not sit where the standpipe or its cord run
is.** A hole in the wrong place on a bought tank is the whole tank.

**20-05. Cut the hole.**
BLOCKED. Missing: BB-23, 20-02, 20-03 and 20-04.

**20-06. Clean every particle of swarf out of the tank.**
BLOCKED. Missing: nothing to clean until 20-05 is done.

**20-07. Fit the bulkhead and seal it.**
BLOCKED. Missing: the bulkhead is a requirement and a search term, not a part.
**REQUIREMENT AND SEARCH TERM, per WATER's return:** a bulkhead fitting for the tank
wall it lands in, sized to swallow the full inflow with the fill-stop failed, seating
on the land found in 20-02, **and large relative to the debris it will meet and
inspectable without disassembly.** Search: `bulkhead tank fitting flat mounting surface
curved tank wall gasket`; `polyethylene tank overflow bulkhead fitting installation`.
**The line belongs in D7 and the lookup is the owner's under G-15.**
WHY LARGE AND INSPECTABLE, AND WHY NOT A SCREEN: **an open port in an open-top tank
collects debris and grows biofilm at the waterline, which is exactly where it sits.**
It fouls silently and it is the last line, with nothing behind it. **A screen makes a
visible failure into an invisible one**, which is the same trade WATER already refused
on the return drop.

**20-08. Confirm the bulkhead does not leak, dry, by hand.**
BLOCKED. Missing: as 20-07.
ACCEPT when unblocked: the fitting is home, the gasket is seated all round with no
witness of a lip or a curve under it, and nothing moves when you pull on it.
WHY IT IS CHECKED DRY AND NOW: a wet test belongs to D8. **What is checked here is
that the gasket is seated on the land, because that is only visible before the tank is
full and only correctable before the run is plumbed to it.**

---

## 21. MARK THE STANDPIPES

**MUST BE TRUE BEFORE THIS SECTION STARTS:**
- BB-22, section 18.
- BB-23, section 19.

**TRUE AFTER IT ENDS:**
- **BB-25.** Each pipe carries a permanent mark at every one of its trip heights,
  measured from its end cap face.

**THE PIPE IS MARKED BEFORE ANYTHING GOES IN THE TANK.** D-131 states it as an
assembly step. **It is more than that here, and the reason is worth carrying: nothing
in this system measures a level, so an unmarked float that slips is invisible and a
marked one is not.** The 1st Edition knew to do it. It did not know why it mattered.

**21-01. Put each pipe on the bench with its end cap face against a stop.**
ACCEPT: the cap face is square to the stop and the pipe cannot slide.
WHY THE STOP: every mark on this pipe is measured from that face and from nothing
else. Measuring from a tape held against a free end reproduces the datum error section
18 exists to prevent.

**21-02. Mark the day tank pipe at LS-1's trip height.**
BLOCKED. Missing: BB-23, section 19.

**21-03. Mark the day tank pipe at LS-5's trip height.**
BLOCKED. Missing: as 21-02.

**21-04. Mark the day tank pipe at LS-4's trip height.**
BLOCKED. Missing: as 21-02.

**21-05. Mark the day tank pipe at LS-2's trip height.**
BLOCKED. Missing: as 21-02.

**21-06. Mark the storage pipe at LS-6's trip height.**
BLOCKED. Missing: as 21-02.

**21-07. Mark the storage pipe at LS-7's trip height.**
BLOCKED. Missing: as 21-02.

**21-08. Mark the storage pipe at LS-3's trip height.**
BLOCKED. Missing: as 21-02.

**21-09. Mark the storage pipe at LS-8's trip height.**
BLOCKED. Missing: as 21-02.

**21-10. Write the position name beside each mark.**
BLOCKED. Missing: nothing to write beside until 21-02 to 21-09 are done.
ACCEPT when unblocked: every mark on both pipes carries its LS- name, and no two marks
on one pipe carry the same name.
WHY THE NAME AND NOT THE ORDER: **T-013.** A mark identified as "the second one up"
follows the count and not the meaning as soon as one mark moves, and D-131 expects
marks to be adjusted for the life of the machine. **The positions in one tank look
alike on a pipe.**

**21-11. Make every mark permanent with a paint pen.**
BLOCKED. Missing: the paint pen is a D7 line and no file read for this book states it
as bought. Owner: the owner runs the lookup under G-15.
**REQUIREMENT AND SEARCH TERM:** a marker that survives permanent immersion in a
fertiliser solution on PVC. Search: `paint marker permanent immersion PVC chemical
resistant`.
WHY PERMANENT AND WHY IT IS ITS OWN STEP: **the mark is the only record of where a
float is supposed to be.** A pencil line under water for a season is a mark that
disappears exactly when somebody comes to check whether a float has slipped.

---

## 22. FIT THE FLOATS AND THEIR CORDS

**MUST BE TRUE BEFORE THIS SECTION STARTS:**
- BB-25, section 21.

**TRUE AFTER IT ENDS:**
- **BB-26.** Every float is clamped at its mark, every float cord is run up its pipe
  in the float tie group, and every float cord leaves through its tank's cord grip
  with the drip loop outside.

### THE WHOLE OF THIS SECTION IS BLOCKED ON THE FLOAT, AND HERE IS WHY

**BLOCKED. Missing: the float part is not chosen. S-01 and S-02 are OPEN interface
rows and D-118 struck the inherited roster - the float pass restarts from
requirements.** Owner: WATER returns the requirement and the search terms; the owner
runs the lookup under G-15; BOSS freezes the rows.

**AND THE FLOAT CANNOT BE BOUGHT UNTIL SECTION 6 EXISTS.** F-100. **The cord is the
strain member, the trip-height datum and the signal path at once**, so it cannot be
cut at the tank and cannot be joined there, **and a float whose supplied cord does not
reach the panel gland is disqualified.** The span's terms are in
subsystems/water-float-requirement.md section 1.4. **This is the one place in the book
where a layout gates a purchase, and it is why section 6 is early.**

**ONE REQUIREMENT ON THE PART THAT IS FREE NOW AND MONEY LATER, D-156:** the float
cord's insulation is rated for the highest voltage in the bundle, **because the
standpipe puts the float cords and the pump cords up one pipe by construction and
they are not in the same voltage class.** D6 carries the class of each.
It is a purchasing attribute and not a build step, and it is free only while the
requirement is open.

**22-01. Clamp LS-1's external weight on its mark on the day tank pipe with a cable
tie.**
BLOCKED. Missing: the float part, as above.
**THE TIE IS THE TRIP HEIGHT AND THE WEIGHT IS THE PIVOT.** D-131. The float hangs
below its weight on a tether and swings from the weight, **so a trip level is set by
where a clamp is and by nothing else.**

**22-02. Clamp LS-5's external weight on its mark.**
BLOCKED. Missing: as 22-01.

**22-03. Clamp LS-4's external weight on its mark.**
BLOCKED. Missing: as 22-01.

**22-04. Clamp LS-2's external weight on its mark.**
BLOCKED. Missing: as 22-01.

**22-05. Clamp LS-6's external weight on its mark on the storage pipe.**
BLOCKED. Missing: as 22-01.

**22-06. Clamp LS-7's external weight on its mark.**
BLOCKED. Missing: as 22-01.

**22-07. Clamp LS-3's external weight on its mark.**
BLOCKED. Missing: as 22-01.

**22-08. Clamp LS-8's external weight on its mark.**
BLOCKED. Missing: as 22-01.

**22-09. Confirm every float on each pipe is fitted the same way up.**
BLOCKED. Missing: as 22-01.
**READ THIS BEFORE YOU FIT ANY OF THEM, BECAUSE IT CANNOT BE CHECKED AFTERWARDS BY
LOOKING.** **The float requirement records that most positions in this build are
closed on low water and that some are the inverse of the rest.** Which are which is
that document's fact and is not repeated here. **The inverted ones sit on the same
standpipes, in the same tanks as the others, and if the parts are identical they are
indistinguishable by eye once installed.** A float installed the wrong way up silently
inverts the fail direction, and it does so at the positions where an inverted fail
direction is most dangerous.
**WHAT THE REQUIREMENT DOES ABOUT IT, so that this step is a confirmation and not a
judgement:** WATER's requirement asks for a changeover contact **so that both senses
are available at the panel from one physical installation.** Eight floats installed
identically, two of them wired to the other leg. **The fail direction becomes a wiring
choice at a terminal a person can see, instead of an orientation choice in a tank a
person cannot.** If the float that arrives is not a changeover, this step becomes a
judgement made in a tank and it should be reported rather than made.

**22-10. Lay the four float cords along the day tank pipe.**
BLOCKED. Missing: as 22-01.

**22-11. Tie the four day tank float cords to the pipe at intervals, as one group.**
BLOCKED. Missing: as 22-01.
**FLOAT CORDS AND PUMP CORDS GET SEPARATE TIE GROUPS.** D-121 as extended by D-156.
The pump cords join this pipe in section 27 and they go in their own group.
WHY IT IS THE ONLY ADJACENCY REMEDY TAKEN, AND WHY NOTHING ELSE IS ADDED: it costs
nothing, changes no part, and is one instruction. **Shields, conduits and barriers
cost a part per pipe, a buy line and an assembly step, they obstruct the tie a person
has to reach at every level adjustment, and none of them touches the expensive failure
- which is float to float, inside one class.** That failure is already paid for by the
overflow.

**22-12. Lay the four storage float cords along the storage pipe.**
BLOCKED. Missing: as 22-01.

**22-13. Tie the four storage float cords to the pipe at intervals, as one group.**
BLOCKED. Missing: as 22-01.

**22-14. Leave slack in each cord at its weight clamp, enough for that position's full
plausible adjustment range in the direction that lengthens the span.**
BLOCKED. Missing: as 22-01, and the adjustment range is not a number until BB-23
exists.
WHY THE ALLOWANCE IS FOLDED INTO THIS STEP AND NOT STATED AFTER IT: **D-131 requires
that commissioning adjust the tie and never the wiring.** The clamp has to travel up
and down its mark with the far end of the cord not moving, **and a clamp moving DOWN
the pipe pulls cord into the tank.** A cord run tight and then adjusted is a cord that
has to be re-run from the panel, and the only remedies left are the two D-131 forbids.
**This allowance has no analogue in any other cable in this build and nobody but WATER
can give it.**

**22-15. Take each tank's float cords out through that tank's cord grip.**
BLOCKED. Missing: as 22-01, and the grip is a D7 line.

**22-16. Form the drip loop in the cords outside the grip.**
BLOCKED. Missing: as 22-15.
ACCEPT when unblocked: the lowest point of the cord run is outside the grip and not
inside it.
WHY: D-126 and D-047. **Water runs to the lowest point. If that point is inside the
grip, it runs into the entry.** A loop formed on the inside is not a drip loop, it is
a funnel.

**22-17. Confirm no float body carries the weight of anything.**
BLOCKED. Missing: as 22-01.
WHY IT IS THE LAST STEP OF THE SECTION: **D-121's whole method is that nothing hangs
off a float body.** A cord tied to a float instead of to the pipe is the failure the
standpipe was adopted to remove, and it is easy to do while tidying.

---

## 23. HANG THE STANDPIPES FOR THE LAST TIME

**MUST BE TRUE BEFORE THIS SECTION STARTS:**
- BB-24, section 20.
- BB-26, section 22.

**TRUE AFTER IT ENDS:**
- **BB-27.** Both standpipes are hung in their tanks, floats at their marks, cords out
  through the grips.

**23-01. Confirm each tank is clean and dry before the pipe goes back in.**
ACCEPT: nothing in either tank.
WHY: section 20 cut a hole in each of them. This is the check that section 20's
cleaning actually happened, made at the last moment it is free.

**23-02. Lower the day tank pipe into its tank and hang it on its U-bolt.**
BLOCKED. Missing: BB-26, section 22.

**23-03. Lower the storage pipe into its tank and hang it on its U-bolt.**
BLOCKED. Missing: as 23-02.

**23-04. Confirm each pipe hangs where section 18 set it and nothing else in the tank
carries its weight.**
BLOCKED. Missing: as 23-02.

**23-05. Confirm every float hangs clear of the tank wall, the bulkhead and the pipe
through its full swing.**
BLOCKED. Missing: as 23-02.
WHY IT IS CHECKED WITH THE TANK EMPTY: a float that fouls something swings short, and
a float that swings short trips at a height that is not its mark. **With the tank
empty you can see the whole swing. With water in it you cannot see any of it**, and
nothing in this system measures a level to tell you.

---

## 24. THE OVERFLOW RUNS TO THE TRACK

**MUST BE TRUE BEFORE THIS SECTION STARTS:**
- BB-20, section 16.
- BB-24, section 20.

**TRUE AFTER IT ENDS:**
- **BB-28.** Each overflow falls continuously from its bulkhead to the drain track and
  discharges through an air gap above it, and a provision for a tell-tale is left in
  each run.

**24-01. Set out each run dry from its bulkhead to the track, with continuous fall.**
BLOCKED. Missing: BB-08, section 6, for where the tank stands relative to the track.
ACCEPT when unblocked: water poured in at the bulkhead end would run the whole way
without standing anywhere.
**NO TRAP, NO LOW POINT, NO RISE ANYWHERE.** Gravity is the only thing moving water in
this line. **The entry point into the track is free under D-147**, which removes the
constraint rather than satisfying it, so the route has the whole track to aim at.

**24-02. Confirm the run does not pass over or under anything it would have to be cut
to service.**
BLOCKED. Missing: as 24-01.
WHY: **an overflow line is a permanent wet-side object on a wall that four enclosures
and the cable runs are competing for, and it cannot go over or under anything.** It
has to have been in the layout. If it was not, this step is where that is discovered,
and it is discovered against everything already fixed.

**24-03. Choose the run's entry into the track away from where the leak sensor sits.**
BLOCKED. Missing: as 24-01, and the sensor's position is the owner's under F-104,
which he has closed.
WHY: D-133. **If normal overflow discharge can splash or pool on the sensor, every
overflow reads as a leak and the alarm stops meaning anything.** The entry point is
free, so this is satisfied by choosing rather than by paying for anything.

**24-04. Build the run in from the bulkhead to the track.**
BLOCKED. Missing: BB-08 and the pipe size, which is 19-05's blocked capacity
requirement. **The overflow's size must not be inherited from the manifold's
diameter** - it is a different question with a different driver.

**24-05. Leave a provision in the run for a tell-tale device.**
BLOCKED. Missing: **there is no decision.** WATER recommended the provision and named
no mechanism and no part. Owner: the owner.
WHY IT IS RAISED HERE AND NOT LEFT FOR LATER, WHICH IS THE WHOLE OF ITS ARGUMENT: **a
successful overflow is indistinguishable from nothing happening.** F-095. Water gone,
floor dry, machine fine, nobody knows, **and a fill-stop float can have been failing
for weeks with the only evidence down a drain.**
**COST, PER G-48:** adding a branch or a boss to this run while it is being assembled
is one fitting and one step. **Adding either afterwards means cutting a line that is
already routed and sloped**, which is the run and the fall done twice. **What it buys
is a place to put a witness, not a witness.** The device decision stays open and the
requirement WATER stated is a persistent, human-readable mark that clearing requires a
deliberate human act - which needs no panel resource, no interface row, no conductor
and no relay envelope, **because the reader is the person doing the walk-round.**
**WHAT IS NOT ADDED, and why:** an alarm. It needs somewhere to land, and the panel's
inventory of destinations is closed - G-01 and G-02 bar a Pi input, every top-face
hole is spoken for, the envelope map has no spare coil, and breaking an existing
chain turns a successful protection into a plant stop **at precisely the moment the
tank has just been saved.**

**24-06. Terminate the run above the track with an air gap.**
BLOCKED. Missing: as 24-04.
ACCEPT when unblocked: the end of the pipe is clear of anything the track can ever
hold, and the pipe is not connected to the drain.
**THIS IS A SECOND AIR GAP AND IT PROTECTS THE OPPOSITE SIDE FROM THE FIRST ONE.**
WATER's return records that **D-138 names only the fill air gap and that nothing on
file names this one.** The fill air gap protects the municipal supply from the tank.
**This one protects the tank from the drain**: a pipe that terminates below the
track's water surface, or that is connected to it, is a back-siphon path from the
drain into a tank of nutrient solution.
Owner: WATER stated the requirement in its return and no D- entry carries it. BOSS.

**24-07. Confirm the run is supported along its whole length.**
BLOCKED. Missing: as 24-04.
WHY IT IS ITS OWN STEP: a gravity line that sags has a low point, **and a low point is
the one thing 24-01 forbids.** A run set out correctly and then hung on too few
supports fails 24-01 without anybody repeating 24-01.

---

## 25. THE STORAGE FILL LINE AND ITS AIR GAP

**MUST BE TRUE BEFORE THIS SECTION STARTS:**
- BB-20, section 16.
- BB-23, section 19.

**TRUE AFTER IT ENDS:**
- **BB-29.** The fill line runs from the building supply through FV-1 to a fixed
  outlet that discharges into the storage tank through an air gap above its flood
  rim.

**25-01. Run the line from the supply stub toward the storage tank.**
BLOCKED. Missing: **FL-01 is an OPEN interface row.** Owner: WATER, and the crossing
carries the air gap as a property of itself under D-138 and D-153.

**25-02. Install FV-1 in the line between unions.**
BLOCKED. Missing: FL-01, as 25-01.
ACCEPT when unblocked: FV-1 is between two unions and can be taken out of the line
without cutting pipe.
**FV-1 IS ORIENTATION-TOLERANT AND FLOW-DIRECTIONAL.** parts.md records the valve as
mountable in any orientation with coil-up preferred for long life. **Fit it the way
round its own body arrow says.** A directional valve fitted backwards is a valve that
never opens, and it looks correctly installed.
WHY UNIONS AND NOT SOLVENT WELD: parts.md records it as the installation method for
this valve. **A coil is a serviceable item on a line that is otherwise permanent.**

**25-03. Bring the line over the storage tank rim and turn its outlet downward into
open air.**
BLOCKED. Missing: BB-23's air gap height, and 19-05's open question about whether the
air gap is required on both tanks or only on the storage fill. Owner: the owner.

**25-04. Fix the outlet to a bracket.**
BLOCKED. Missing: the bracket is a D7 line and its position depends on BB-08.
**REQUIREMENT AND SEARCH TERM:** a rigid fixture holding the fill line's discharge end
over the storage tank, **clear of the standpipe, the transfer suction and the
overflow.** Search: `pipe support bracket tank rim`; `rigid pipe stand-off bracket`.
WHY IT NEEDS A FIXTURE AT ALL: **with an air gap the discharge end is unsupported by
definition.** There is nothing at the end of the pipe holding it, and a fill line that
has swung out of position discharges onto a floor or onto the rim.

**25-05. Confirm the outlet is clear of the flood rim by the decided air gap.**
BLOCKED. Missing: BB-23.
**THE GAP IS MEASURED FROM THE FLOOD-LEVEL RIM, AND ON A TANK WITH AN OVERFLOW THE
FLOOD LEVEL IS SET BY THE OVERFLOW AND NOT BY THE RIM.** So this dimension is
referenced to the overflow, which is referenced to the high-high, which is referenced
to a float mark on a standpipe. **D-130 and D-138 are one dimension chain, not two
requirements**, and that is why section 19 decides all of it in one pass.

**25-06. Note the splash the gap discharge will make, and confirm it does not land on
the storage standpipe or its cords.**
BLOCKED. Missing: as 25-03.
WHY IT IS WORTH A STEP: **a gap discharge into an open tank splashes and entrains
air.** It lands in storage, not in the day tank, so it is one transfer away from the
probes, **but it disturbs the storage surface that LS-6, LS-7 and LS-8 read**, and
that disturbance is an input to the differential each of them needs.

**25-07. Report FL-02's wording to BOSS rather than correcting it.**
ACCEPT: the report is written and sent.
**WHAT TO REPORT:** with an air gap the fill line does not connect to the tank, and
FL-02's End B reads "WATER: storage tank inlet", which describes a fitting. **The row
is wrong in wording.** WATER found it and reported it rather than fixing it, and BOSS
owns the table. **Nothing in this section is blocked by it.** It is here so that a
builder reading FL-02 and looking for an inlet fitting stops looking.

---

## 26. THE TRANSFER LINE

**MUST BE TRUE BEFORE THIS SECTION STARTS:**
- BB-20, section 16.

**TRUE AFTER IT ENDS:**
- **BB-30.** The transfer line runs from the storage tank to the day tank with its
  discharge fixed.

**26-01. Place the transfer pump at its layout position.**
BLOCKED. Missing: BB-08, section 6.
**IT IS A CORDED PUMP AND ITS CORD PLUGS INTO A PANEL-MOUNTED RECEPTACLE FROM
OUTSIDE**, per D-046. **Nothing about its cord is fed through a grip and nothing about
it is cut.** The cord cap and the receptacle are D6's RUN-018 and are not this book's.

**26-02. Run the suction from the storage tank to the pump.**
BLOCKED. Missing: BB-08, and WATER's transfer plumbing is an open item.

**26-03. Run the discharge from the pump to the day tank.**
BLOCKED. Missing: as 26-02.

**26-04. Fix the discharge end over the day tank.**
BLOCKED. Missing: as 26-02.
WHY IT IS FIXED AND NOT LEFT HANGING: **the transfer discharge disturbs the surface
the day tank floats read**, and that disturbance is an input to every day tank
differential in section 19. **A discharge that moves changes a number that was
measured once.**

**26-05. Confirm the discharge does not land on the day tank standpipe, its floats or
its cords.**
BLOCKED. Missing: as 26-04.

**26-06. Confirm the discharge is not under the overflow bulkhead's splash path and
does not sit where the return drop lands.**
BLOCKED. Missing: as 26-04.
WHY THESE ARE CHECKED TOGETHER: the same rim carries the standpipe's U-bolt, the
standpipe and its cord bundle, the return drop's landing, two submersible cords, the
overflow bulkhead and M-01's penetrations and hangers. **This is the tightest piece of
real estate in the build and every item on it was placed by a different section.**

---

## 27. THE DAY TANK SUBMERSIBLES AND THE CHILLER LOOP

**MUST BE TRUE BEFORE THIS SECTION STARTS:**
- BB-20, section 16.
- BB-27, section 23.

**TRUE AFTER IT ENDS:**
- **BB-31.** Both submersibles are held by cradle in the day tank, their cords are
  tied on the standpipe in their own group, and the chiller loop is plumbed and its
  joints are cured.

**TWO SUBMERSIBLES SIT IN THE DAY TANK AND BOTH RUN CONTINUOUSLY**, per D-137 and
D-143: the manifold pump and the chiller loop pump.

**27-01. Set the manifold pump in a cradle at the day tank bottom.**
BLOCKED. Missing: the cradle is a D7 line and no file read for this book states it as
bought.
**REQUIREMENT AND SEARCH TERM:** a fixture that holds a submersible pump at a fixed
position and depth in the day tank, taking no load through the cord. Search:
`submersible pump mounting bracket tank`; `pump cradle stand aquarium sump`.
WHY A CRADLE AND NOT THE CORD: water.md's own rule. **Position held by fixture, not by
cord. A cord-hung pump is a pump whose position is a suggestion**, and G-11 puts this
pump's suction at the day tank bottom so the tank mixes.

**27-02. Set the chiller loop pump in a cradle in the day tank.**
BLOCKED. Missing: as 27-01.

**27-03. Confirm neither pump is set where a float swings.**
BLOCKED. Missing: as 27-01.

**27-04. Confirm neither pump's intake is where the low-low trip will leave it drawing
air.**
BLOCKED. Missing: as 27-01, and BB-23.
WHY: C-11 names the vortex explicitly and it is worst at low level, when both
submersibles are nearest the surface. **Air past a probe makes the spike that looks
like an early arrival**, which corrupts the measurement the whole dosing model rests
on. The conflict this creates for the low-low trip is named in 19-02 and is resolved
by geometry.

**27-05. Lay both pump cords along the day tank standpipe.**
BLOCKED. Missing: as 27-01.

**27-06. Tie both pump cords to the pipe at intervals, as a group separate from the
float cords.**
BLOCKED. Missing: as 27-05, and BB-26 must already have put the float cords in their
own group.
WHY THE GROUPS ARE SEPARATE AND WHY THIS SECTION IS WHERE THE PUMP GROUP IS MADE:
D-121 as extended by D-156. **These cords and the float cords are not in the same
voltage class**, and D6 carries the class of each.
The pump cords cannot be tied before the pumps are in the tank, so section 22 tied the
float group and left this one, **and this step must not be done by adding the pump
cords to the float bundle because that is exactly the adjacency the two groups exist
to keep apart.**

**27-07. Run the chiller loop pump's discharge to the chiller's inlet port.**
BLOCKED. Missing: BB-08 for where the chiller stands, and FL-08 is internal to WATER
and its plumbing is an open item.

**27-08. Run the chiller's outlet port back to the day tank.**
BLOCKED. Missing: as 27-07.

**27-09. Fix the loop's return end over the day tank.**
BLOCKED. Missing: as 27-07.

**27-10. Leave the loop undisturbed until the cement's own instruction says any
solvent joint in it is cured.**
BLOCKED. Missing: as 27-07.
WHY THIS SECTION ENDS AT A CURE: as sections 11 and 17.

**ONE THING TO KNOW WHILE YOU ARE PLACING THESE TWO PUMPS, because it changes nothing
you do here and it changes what somebody measures later:** both of them put their
entire electrical input into the water as heat, continuously, in a tank that is being
chilled. **That was invisible while the manifold pump was believed intermittent.**
F-103 is the arithmetic and it is WATER's. Nothing in this system reports a tank that
never reaches temperature.

---

## 28. THE LOOP: MANIFOLD SUCTION AND RETURN DROP

**MUST BE TRUE BEFORE THIS SECTION STARTS:**
- BB-15, section 12.
- BB-31, section 27.

**TRUE AFTER IT ENDS:**
- **BB-32.** The circulation loop is closed: day tank, manifold pump, manifold, return
  drop, day tank.

**28-01. Run the manifold pump's discharge to the manifold's inlet union.**
BLOCKED. Missing: **FL-03 is an OPEN interface row.** Owner: WATER and DOSING jointly,
BOSS freezes.

**28-02. Make the inlet union.**
BLOCKED. Missing: as 28-01.

**28-03. Run the line from the manifold's outlet union toward the day tank.**
BLOCKED. Missing: **FL-04 is an OPEN interface row.** Owner: as 28-01.

**28-04. Make the outlet union.**
BLOCKED. Missing: as 28-03.

**28-05. Terminate the return as an open drop into the day tank.**
BLOCKED. Missing: as 28-03.
ACCEPT when unblocked: the end of the line discharges into open air above the water
and is not submerged.
WHY AN OPEN DROP AND NOT A SUBMERGED RETURN WITH A VENT HOLE: **the siphon break has
to be the geometry, not a hole.** WATER refused the submerged return with an
anti-siphon vent on the ground that the break then depends on a small hole staying
clear, **and that hole fouls shut silently.** Trading a visible failure for an
invisible one is the wrong trade. **If you are about to submerge this for the sake of
splash, that is what you are trading.**

**28-06. Fix the return drop's landing point.**
BLOCKED. Missing: as 28-03.
WHY THE LANDING POINT IS FIXED AND RECORDED RATHER THAN LEFT WHERE IT FALLS:
commissioning.md's re-measure triggers list the return drop's landing point by name,
and it records that **the return-versus-suction geometry changes short-circuiting more
than anything else, and that it can be changed by someone tidying a cord.** A landing
point that moves voids a measurement nobody will know to re-take.

**28-07. Confirm the drop does not land on the standpipe, a float, a cord or the
overflow bulkhead.**
BLOCKED. Missing: as 28-06.

**28-08. Confirm the drop's splash does not land where the day tank floats read.**
BLOCKED. Missing: as 28-06.
WHY: as 26-04. It is an input to every day tank differential in section 19.

---

## 29. THE DOSE AND SUCTION TUBING

**MUST BE TRUE BEFORE THIS SECTION STARTS:**
- BB-15, section 12.
- BB-16, section 12.
- BB-18, section 14.

**TRUE AFTER IT ENDS:**
- **BB-33.** Every channel has an unbroken suction line from its jug to its head and
  an unbroken delivery line from its head to its injection port, dry and unprimed.

**THE WET PATH FROM MANIFOLD TO HEAD TO JUG IS ONE PATH AND ONE OWNER'S**, D-006.
PUMP-BOXES stops at the barb.

**29-01. Run the suction line for CH1 from its jug station to its head's suction barb,
through the lid penetration.**
BLOCKED. Missing: **CBL-05 is an OPEN interface row** and DOSING's tubing selection is
an open item - chemical compatibility per product, and translucency under D-019.
Owner: PUMP-BOXES owns the penetration, DOSING owns the tubing through it.
**THE TUBE IS TRANSLUCENT.** D-019 took translucent tubing and the jug end in the
operator's sightline **instead of** the keyed coupling, and both were named by DOSING
as the conditions without which the coupling trades a detectable failure for an
undetectable one. **An opaque tube spends a decision that was already made.**
WHY IT MATTERS ON THE SUCTION SIDE SPECIFICALLY: **on a suction line a bad seal does
not drip, it draws air. The head turns, the books decrement, and nothing is
delivered.** Nothing in this system measures what a head actually delivered.

**29-02. Run the suction line for CH2 from its jug station to its head's suction barb, through the lid penetration.**
BLOCKED. Missing: as 29-01.

**29-03. Run the suction line for CH3 from its jug station to its head's suction barb, through the lid penetration.**
BLOCKED. Missing: as 29-01.

**29-04. Run the suction line for CH4 from its jug station to its head's suction barb, through the lid penetration.**
BLOCKED. Missing: as 29-01.

**29-05. Run the suction line for CH5 from its jug station to its head's suction barb, through the lid penetration.**
BLOCKED. Missing: as 29-01.

**29-06. Run the suction line for CH6 from its jug station to its head's suction barb, through the lid penetration.**
BLOCKED. Missing: as 29-01.

**29-07. Run the suction line for CH7 from its jug station to its head's suction barb, through the lid penetration.**
BLOCKED. Missing: as 29-01.

**29-08. Run the suction line for CH8 from its jug station to its head's suction barb, through the lid penetration.**
BLOCKED. Missing: as 29-01.
**CH1 to CH4 are in box A and CH5 to CH8 are in box B, per D-178. One step per
channel, eight ticks, because a step covering several channels can be half done and
look finished.**

**29-09. Run the delivery line for CH1 from its head's discharge barb, through the lid
penetration, to its injection port.**
BLOCKED. Missing: as 29-01, and DOSING's injection port arrangement is an open item.

**29-10. Run the delivery line for CH2 from its head's discharge barb, through the lid penetration, to its injection port.**
BLOCKED. Missing: as 29-09.

**29-11. Run the delivery line for CH3 from its head's discharge barb, through the lid penetration, to its injection port.**
BLOCKED. Missing: as 29-09.

**29-12. Run the delivery line for CH4 from its head's discharge barb, through the lid penetration, to its injection port.**
BLOCKED. Missing: as 29-09.

**29-13. Run the delivery line for CH5 from its head's discharge barb, through the lid penetration, to its injection port.**
BLOCKED. Missing: as 29-09.

**29-14. Run the delivery line for CH6 from its head's discharge barb, through the lid penetration, to its injection port.**
BLOCKED. Missing: as 29-09.

**29-15. Run the delivery line for CH7 from its head's discharge barb, through the lid penetration, to its injection port.**
BLOCKED. Missing: as 29-09.

**29-16. Run the delivery line for CH8 from its head's discharge barb, through the lid penetration, to its injection port.**
BLOCKED. Missing: as 29-09.
**Eight steps, one per channel, as 29-01 to 29-08.**

**29-17. Confirm every tube joins external tubing at the ends of the head's own short
tube piece, and that no external tube is joined onto the pump tube itself.**
BLOCKED. Missing: as 29-01.
WHY: **the pump tube is a consumable that gets changed**, and DOSING owns the change.
A joint made onto the pump tube is a joint that has to be remade at every change, in
place, over an open manifold.

**29-18. Confirm the jug end of every line is visible from the operator's standing
position.**
BLOCKED. Missing: BB-08, section 6, and 29-01.
WHY IT IS CHECKED AFTER THE TUBES ARE RUN AND NOT ONLY WHEN THE STATIONS WERE PLACED:
a station in the sightline with a tube routed behind something is a sightline that was
paid for and not delivered.

**29-19. Leave every line dry and unprimed.**
BLOCKED. Missing: as 29-01.
WHY: priming is commissioning's, and **a primed line is a line with product in it
standing against a head that has not been proved to hold.** Whether a head holds
against back-siphon with the jug above the inlet is C-06 and it is not answered.

**ONE THING NOT DECIDED HERE AND NOT TO BE DECIDED AT THE BENCH: how high a jug
stands.** DOSING's jug placement item is open - height relative to the head, so a head
is not asked to lift more than it can and so a jug change is possible without a tool -
and **whether a dose line can siphon when the head is idle depends on it.** Owner:
DOSING, and C-06 measures it in both energised and de-energised states.

---

## 30. THE LEAK CONSOLE AND ITS SENSOR

**MUST BE TRUE BEFORE THIS SECTION STARTS:**
- BB-13, section 10.
- BB-28, section 24.

**TRUE AFTER IT ENDS:**
- **BB-34.** WB200 is mounted at the position the owner set and its sensor is placed
  on the floor clear of every overflow discharge point.

**WB200 IS REMOTE AND IS IN NO ENCLOSURE.** D-163. It sits outside the main panel, fed
through its own cord grip, with its sensor on the floor.

**30-01. Mount WB200 at the position the owner has set.**
BLOCKED. Missing: **the console's position on the wall is the owner's and is not
fixed.** Owner: the owner. CBL-06 is an OPEN interface row.

**30-02. Place the sensor on the floor.**
BLOCKED. Missing: the placement is the owner's under F-104, which he has closed, and
S-04 is an OPEN interface row.
**WHAT MAKES THE PLACEMENT HARD, so that a builder does not put it somewhere
convenient:** the floor drain is a track, and **a floor with a track drain is a floor
built to move water to the track.** A leak reaching that floor goes to the track, not
to a sensor sitting elsewhere on it. **The console's job is water where water should
not be, on a floor whose entire design is to have no standing water anywhere.**

**30-03. Confirm the sensor is not where normal overflow discharge can splash or pool
on it.**
BLOCKED. Missing: as 30-02, and BB-28.
WHY IT IS CHECKED AFTER THE OVERFLOW RUNS EXIST AND NOT BEFORE: **the splash path is
not knowable until the runs are built.** D-133: if the sensor sits in it, every
overflow reads as a leak and the alarm stops meaning anything.
**AND THE THING THAT IS GAINED BY GETTING THIS RIGHT, which is easy to miss: a working
overflow produces no floor water and no alarm. The sensor does not see the overflow -
it sees the overflow FAILING.** Blocked track, discharge that misses, line that comes
apart. That is a better signal than an overflow alarm would have been, and it only
exists if the sensor is out of the normal splash.

**30-04. Leave the sensor lead unlanded.**
BLOCKED. Missing: **RUN-014's voltage and segregation cells in D6 are empty and both
wait on one lookup, the WB200's sensing-circuit class.** Owner: the owner runs the
lookup under G-15.
WHY IT IS CALLED OUT: D6 records that D-163, CBL-06 and parts.md's WB200 entry all
describe the console's supply and its output contact, **and that none of them
describes the sensor lead.**

---

## 31. WIRING

**MUST BE TRUE BEFORE THIS SECTION STARTS:**
- BB-05, section 3. Every device carries its name.
- BB-06, section 4. Every terminal has been read.
- BB-09, section 6. Every entry position is stated.
- BB-17, section 13. The main panel plate is populated and installed.
- BB-18, section 14. The pump boxes are populated.
- BB-19, section 15. The display box plate is populated.
- BB-26, section 22. Every float cord is out through its grip.
- BB-27, section 23. Both standpipes are hung.
- BB-29, section 25. FV-1 is installed.
- BB-34, section 30. WB200 is mounted.

**TRUE AFTER IT ENDS:**
- **BB-35.** Every conductor in D5 is cut, routed, labelled at both ends, landed and
  ticked.

### THIS SECTION OWNS THE ORDER AND NOTHING ELSE

**Not one conductor, terminal, landing, label or route is stated in this book.** They
are D5's rows, D4's pages and D6's runs. **What is here is when the wiring happens,
what has to be true before it starts, and the one ordering rule that is not on any of
those three documents.**

**THE ORDERING RULE, and it is why this section is the second-to-last piece of work:
NO CONDUCTOR IS LANDED ON A PART A LATER SECTION INSTALLS.** Every precondition above
is a part that a conductor lands on. **A build that wires before it mounts produces
joints that have to be broken to finish the mounting, and a broken and remade joint is
not the joint that was checked.**

**31-01. Confirm F-099 is closed before any cable is cut.**
BLOCKED. Missing: **F-099 is open against parts.md's two cable-run tables, which carry
the same five figures under contradictory allowance rules.** Owner: BOSS; parts.md is
authoritative under D-026 and is not silently rewritten.
WHY IT IS THE FIRST STEP IN THIS SECTION: **T-020, and it is worse for where it sits.
It is an ambiguous quantity in the authoritative file, on a table a person reads
immediately before cutting cable.** A cut cable cannot be un-cut. **Do not cut from
either table until it closes.**

**31-02. Confirm every joint in the wet path has cured.**
ACCEPT: every solvent joint made in sections 11, 17, 24, 25, 26, 27 and 28 has had the
time its cement's label states.
WHY IT IS CHECKED HERE: it is one of D8's prerequisites and this is the last moment
before the machine stops being a plumbing job. **Finding an uncured joint after the
panel is live is finding it in the worst order.**

**31-03. Take D6 and cut each jacket.**
BLOCKED. Missing: 31-01, and **no row in D6 is buildable: CBL-01 through CBL-04 are
all OPEN and every jacket lands at a gland or a bulkhead they govern.** Owner:
INTERCONNECT for position and spacing, BOSS to freeze the rows.
**THE ALLOWANCE IS IN D6'S CUT STEP AND IS NOT STATED ANYWHERE ELSE.** Do not add
anything to it and do not take anything off it.

**31-04. Route each jacket on the wall per D6.**
BLOCKED. Missing: as 31-03. **No page in this set says which way a cable runs on the
wall, because the wall layout does not exist.** That is an open cell in D6 and it
stays open while M-02 is open.

**31-05. Pull every jacket through its glands before any conductor is landed.**
BLOCKED. Missing: as 31-03.
WHY EVERY JACKET IS PULLED BEFORE ANY END IS LANDED: **a conductor spans the gland and
is one row, D-171.** Landing one end of a spanning conductor before its jacket is
pulled means pulling a landed conductor, and a jacket pulled past a populated gland
plate disturbs the ones already there.

**31-06. Take the D4 page for the box in front of you and work it in order.**
BLOCKED. Missing: **every joint in D4 is blocked on F-106, and section 4 is what
closes it.** If section 4 was worked, this is not blocked by F-106 and the remaining
blockers are the ones D4 names on each page.
**THE PAGES MAY BE WORKED IN ANY ORDER AND THIS BOOK IMPOSES NONE.** Each page is
complete for the end you are holding, and a conductor that spans a gland appears on
both pages with its far end named, **so you never hold two documents to land one
wire.** Each page carries its own step order and this book does not repeat it.

**31-07. Tick each conductor on D5 as D4's page tells you to.**
BLOCKED. Missing: as 31-06.
WHY THE TICK IS ON D4'S PAGE AND THE RECORD IS D5: **the tick is on the page in your
hand. D5 is the record of what the build is, not the worksheet for what you have
done.**

**31-08. Land the ground bars last, per D4.**
BLOCKED. Missing: as 31-06, and **the ground bars are not bought.** Owner: MAIN-PANEL.
**THE BARS ARE THE ONLY BONDING POINTS IN THIS BUILD AND NOTHING BONDS ANYWHERE
ELSE.** D-165. **A builder who finds a convenient screw will use it**, which is why it
is written down. Each remote enclosure has its own local bar and a green conductor
inside the cross-box cable joins it home. **There is no separate bonding cable** -
RUN-017 was retired for exactly that reason.

---

## 32. CLOSING UP

**MUST BE TRUE BEFORE THIS SECTION STARTS:**
- BB-35, section 31.

**TRUE AFTER IT ENDS:**
- **BB-36.** All four enclosures are closed, and no bond exists outside a bar.

**32-01. Confirm nothing in any enclosure is bonded to anything but its bar.**
ACCEPT: you have looked at every green conductor in every box and every one of them
ends at a bar.
WHY IT IS CHECKED BEFORE THE LIDS GO ON: it is the last moment any of them is visible,
and **a bond made to a convenient screw during wiring looks exactly like a bond made
to a bar until you look at where it ends.**

**32-02. Confirm no conductor lies where a lid or a cover will trap it.**
ACCEPT: you have run a hand round every sealing face and found nothing crossing it.

**32-03. Fit pump box A's lid.**
ACCEPT: the lid seats all round and no tubing or conductor is pinched at the sealing
face.

**32-04. Fit pump box B's lid.**
ACCEPT: as 32-03.

**32-05. Fit the display box cover.**
ACCEPT: the cover seats all round and the display cutout's gasket is undamaged and
seated.
WHY IT IS CHECKED RATHER THAN ASSUMED: the gasketed cutout is the youngest part in the
assembly and it has been off and on since section 9.

**32-06. Close the main panel.**
ACCEPT: the door closes on its own seal without being forced.

**32-07. Confirm every top-face device on the main panel is fitted and no top-face
hole is open.**
BLOCKED. Missing: 7-10's blocker. Owner: MAIN-PANEL.
WHY IT IS CHECKED AGAIN HERE: **the assembly's rating is set by its worst
penetration**, and an unfitted device hole in an upward-facing face is a hole in the
roof of the panel. The design sheds rather than seals, so anything that lands on that
face has to run off it and not into it.

---

## 33. WHAT COMES NEXT, AND WHAT HAD TO COME FIRST

**MUST BE TRUE BEFORE THIS SECTION STARTS:**
- BB-28, section 24. The overflows run to the track.
- BB-30, section 26. The transfer line is in.
- BB-32, section 28. The circulation loop is closed.
- BB-33, section 29. Every dose and suction line is run.
- BB-36, section 32. Every enclosure is closed.

**TRUE AFTER IT ENDS:**
- **BB-37.** The mechanical build is complete, and the next book and its own
  prerequisites are named.

### What had to come first, and it is not this book

**D7, the purchase package, comes before section 2 and is used once.** If you reached
section 2 with parts missing, D7 was not finished. **The cart audit says what to
change in each cart before checkout, which is a thing that only helps before money is
spent.**

**D2, D3, D5, D6 and D4 were in your hands throughout and none of them comes after
this book.** D2 and D3 are what the panel is and where things sit in it. D6 must be
complete for any jacket a conductor travels in, **because a conductor cannot be cut,
routed or landed without a jacket and a landing point.** D5 is generated before D4,
and D4 is its view.

**This is said here because a book that ends by naming the next book, without naming
the one that had to come first, sends a builder forward past a gap he cannot see.**

### What comes next

**D8, the commissioning checklist.** It opens with prerequisites - every wire landed
and both ends labelled, every joint cured - then runs staged, **each stage ending in a
gate, with no stage started until every box in the one before it is ticked.**

**Three things about D8's order that belong here, because they are order and this book
owns order:**

**1. C-09 IS FIRST.** D-022. Nothing below it is worth measuring until the channel the
wall says it is, is the channel software means. **A measurement taken against a
mislabelled channel is not a wrong number, it is a right number filed against the
wrong thing, and every later check confirms it.**

**2. THE FLOAT TESTS COME BEFORE WATER IS IN THE TANKS.** C-24 lifts each float's
conductor at the panel terminal in turn and confirms the chain does what it is
supposed to. Its own row says to do it before water is in the tanks, **because the
test is about conductors and coils and a wet tank adds nothing to it and makes the
lifting worse.** WATER's return adds a second one of the same shape, on the plant
rather than on the meter, and returns it as a required row that BOSS has not yet put
in commissioning.md. **Owner: BOSS.**

**3. THE FIRST FILL IS SLOW AND IT IS WHERE THE MARKS ARE PROVED.** D-131: fill
slowly, confirm each float trips at its mark, **and adjust the tie and never the
wiring.** That is the whole point of sections 21 and 22 and of the re-clamp allowance
in 22-14.

**D9's form is written with D8 and its content cannot exist until D8 has run.**
Everything that later wants one of D8's figures cites D9 and never a datasheet.

**D11, the channel register, is filled at C-09 and updated for the life of the
machine.**

### The two gates, said for the last time

**F-106.** Section 4 is the work that closes it. Until it is closed, **every joint in
D4 is blocked and section 31 cannot be worked.** It is one evening with the parts and
a pen. It is not a decision, a purchase or a design.

**M-02.** Section 5 produces the measurement and section 6 is the layout. Until it
exists, **every dimension in this book is blocked** and so is D3, the balance of D6,
and the float purchase that section 22 waits on.

**Everything else in this book is complete. What is missing is where things go and
what is printed on them.**

---

## 34. THE SEQUENCE CHECK, RUN ON THIS BOOK

**Run as G-50 and D-183 require, after the book was written and against the book as
written.** It does not replace an end-to-end read as a builder. **It gives that read
something to check against.**

### 34.1 Every precondition, matched

**Thirty-three sections. Thirty-seven postconditions, BB-01 to BB-37. Every
precondition below is matched by a postcondition of an EARLIER section, or by
something true before the build starts.**

| Section | Requires | Produced by |
|---|---|---|
| 1 | nothing | true before the build starts |
| 2 | BB-01 | 1 |
| 3 | BB-03 | 2 |
| 4 | BB-03, BB-05 | 2, 3 |
| 5 | BB-04 | 2 |
| 6 | BB-02, BB-07 | 2, 5 |
| 7 | BB-05, BB-09 | 3, 6 |
| 8 | BB-05, BB-09 | 3, 6 |
| 9 | BB-05, BB-09 | 3, 6 |
| 10 | BB-08, BB-10, BB-11, BB-12 | 6, 7, 8, 9 |
| 11 | BB-03 | 2 |
| 12 | BB-08, BB-14 | 6, 11 |
| 13 | BB-05, BB-13 | 3, 10 |
| 14 | BB-05, BB-11, BB-13 | 3, 8, 10 |
| 15 | BB-05, BB-13 | 3, 10 |
| 16 | BB-03, BB-08, BB-13 | 2, 6, 10 |
| 17 | BB-03, BB-20 | 2, 16 |
| 18 | BB-20, BB-21 | 16, 17 |
| 19 | BB-22 | 18 |
| 20 | BB-20, BB-23 | 16, 19 |
| 21 | BB-22, BB-23 | 18, 19 |
| 22 | BB-25 | 21 |
| 23 | BB-24, BB-26 | 20, 22 |
| 24 | BB-20, BB-24 | 16, 20 |
| 25 | BB-20, BB-23 | 16, 19 |
| 26 | BB-20 | 16 |
| 27 | BB-20, BB-27 | 16, 23 |
| 28 | BB-15, BB-31 | 12, 27 |
| 29 | BB-15, BB-16, BB-18 | 12, 12, 14 |
| 30 | BB-13, BB-28 | 10, 24 |
| 31 | BB-05, BB-06, BB-09, BB-17, BB-18, BB-19, BB-26, BB-27, BB-29, BB-34 | 3, 4, 6, 13, 14, 15, 22, 23, 25, 30 |
| 32 | BB-35 | 31 |
| 33 | BB-28, BB-30, BB-32, BB-33, BB-36 | 24, 26, 28, 29, 32 |

**RESULT: no precondition is unmatched. Every producing section number is lower than
the section that requires it.**

### 34.2 Cycles

**RESULT: none.** Every precondition in 34.1 is produced by a strictly earlier
section, so the dependency graph is acyclic by inspection of the table.

**Two candidate cycles existed while the book was being written and both were broken
deliberately. They are recorded because a reader will otherwise re-derive them.**

**Candidate 1. The wall layout needs the tank positions and the tank positions need
the wall layout.** Broken by making section 6 produce BOTH: it is one arbitration
under M-02 and not two decisions that wait on each other. **Nothing else in the book
places a tank or a wall item.**

**Candidate 2. C-11's fill band is blocked on "floats chosen and set", and the float
marks are blocked on the fill band.** Broken by WATER's reading, adopted in 19-01:
**the band is a decision about the water and the float marks follow it.** Section 19
decides the band before section 21 marks anything.

### 34.3 Postconditions nothing later requires

**Every postcondition BB-01 to BB-36 is required by at least one later section.**

**BB-37 is required by nothing, and it is the only one.** That is correct rather than
a defect: it is section 33's postcondition and section 33 is the last section. **It is
this book's output, and what consumes it is D8.**

### 34.4 The five defects this book was written against, checked one at a time

**1. A section that sends a builder away and then continues assuming he has not
gone.** Four sections end at a wait and each names its wait as the last step: 11 at
the manifold cure, 17 at the standpipe cure, 27 at the chiller loop cure, and 19 at a
decision that is somebody else's. **Sections 12, 18, 28 and 20 restate the wait as
their own precondition**, so returning to the book puts you in the right place.
**Section 5 ends by handing the measurement to somebody else and section 6 is that
person's work.**

**2. A step that lands a conductor on a part a later step installs.** Section 31's
preconditions name every part a conductor lands on: the populated main panel plate,
both populated pump boxes, the populated display box plate, the float cords out
through their grips, the standpipes hung, FV-1 installed, and WB200 mounted. **Nothing
is wired before it is mounted.** The single case inside a section is 14-08, which
fits the pull-down landing to the box body **because a conductor cannot be landed on a
part a later step installs**, and leaves the landing itself to D4.

**3. A book that ends by sending the builder to the next book without mentioning the
one that had to come first.** Section 33 names D7 as the book before this one, names
D2, D3, D5, D6 and D4 as in hand throughout, and then names D8 as next. **It says why
in terms.**

**4. Two sections each depending on the other's output.** 34.2. None, and the two
candidates are recorded with how each was broken.

**5. A duct cut over a populated plate.** Sections 7, 8 and 9 cut every penetration
with the enclosure empty and its plate out. **Section 13 cuts rail and duct on a bare
plate and says why a builder would reasonably do it the other way.** Sections 18 and
20 apply the same rule to a tank: the standpipe comes out before the bulkhead is cut,
**because swarf in a tank is swarf on a float.**

### 34.5 What this check does not do

**It does not find a step that is wrong.** Every precondition here is a statement the
writer made about his own section, and a section that names the wrong precondition
passes this check. **The end-to-end read as a builder is still owed, and it is the
thing this check exists to serve.**

---

## 35. STATUS

**Stopped part way, and this book is finished only when somebody has tried to build
from it.** Rule 7: BOSS declares it finished after another agent builds against it and
finds nothing.

**Thirty-three build sections, one check section and this one. 237 numbered steps.**
**185 of the 237 are blocked and 52 are ready to work today.** The order is complete,
the method is complete, and **the sequence check above passes with no unmatched
precondition, no cycle, and no unconsumed postcondition except the book's own
output.**

**Counts of this document's own sections and steps appear because this section is
about the document.** No count of anything the build contains appears anywhere in this
book, per G-41 and D-183: D7 is the only document in this set where a quantity lives.

**What is not complete is every dimension and every marking, and both have one cause
each: M-02 and F-106.** Neither is a design problem. One is an evening with a tape
measure and one is an evening with a pen.
