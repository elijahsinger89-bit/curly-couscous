# D6. Cable and terminal schedule

**Owner: INTERCONNECT. Issued 2026-09-04, revised 2026-09-05** against the duty
vocabulary, the contactor names, the S-03 and S-20 amendments, D-156, the entry faces
in subsystems/entry-faces.md, and D-162 to D-165.

**Who reads this and when.** The person routing, cutting and landing cable, before
wiring starts. D5 gives them the conductor; this gives them the jacket it travels in
and the landing point at each end. Per document-plan.md section 4.1, **D6 must be
complete for any jacket a conductor travels in, because a conductor cannot be cut,
routed or landed without both.**

**What is NOT here, and where it is instead.** Per document-plan.md section 3.2, one
fact has one place:

| Not here | There |
|---|---|
| Any conductor fact: endpoints, colour, fail direction, design current and its event | **D5**, one CDR- row |
| Rung logic, device identity, and each pole's DUTY | **D2**, the electrical schematic |
| Which face a cable enters and the order of entries on it | **subsystems/entry-faces.md** for CBL-02 and CBL-03. This document carries the resulting cell and does not restate the reasoning |
| What a crossing IS and its status | **interface-table.md**, one FL-, P-, S-, CBL- or M- row |
| Face geometry, penetration and rail positions | **D3** |
| Any quantity, count, total or price | **D7, once** |
| Per-channel product, role, jug and cable core | **D11**, the channel register |
| Reasoning and provenance | The tree. No delivered document carries it |

**No length, gauge, core count, terminal count, spacing or part number appears in
this document.** Length is not stored anywhere: D-090's allowance is folded into the
cut step, per T-020. **Note before cutting: F-099 is open against parts.md's two
cable-run tables, which carry the same five figures under contradictory allowance
rules. Do not cut from either until F-099 closes.**

**Every cost claimed below is stated in PARTS and STEPS, per G-48**, and where a cost
belongs to a box INTERCONNECT does not own it is named as the owner's rather than
called cheap, per G-47. **Section 2.3 records where this document got that wrong
once.**

---

## 1. HOW TO READ A RUN- ROW

**RUN-nnn is ONE JACKET, not a route.** D-149. A conductor travels in a jacket, so
D5's cable column names one of these.

**The number carries no meaning.** Not a route order, not a class, not a build
sequence. No rule is keyed to it and a gap is never closed.

**If a jacket splits, its id is RETIRED and new ids are issued.** D-149. Never a
suffix: RUN-007a is arithmetic on an identifier and is the off-by-one generator
channel-token.md's forbidden list exists to prevent. **A retired id stays visible in
the table saying why, and its number is never reused. RUN-017 is the first.**

### 1.0 A cell has THREE states, not two

**A cell that can never be filled must not look like one that has not been filled
yet.**

| State | Written as | Means |
|---|---|---|
| **Filled** | The value | |
| **No valid value** | **n/a**, with the reason | The thing at that end has no such property. **It waits on nobody and is counted out of the empty total** |
| **Empty** | **OPEN**, with the blocker in the last column | Genuinely not yet answered |

**A float, a solenoid coil, a floor sensor, a cord cap, a probe fitting, a building
branch circuit and a USB-C brick have no faces.** Asking them for one is the CBL-
shape of F-097 - a column asking for a kind of value the thing at that end does not
have. **Where a face is n/a the entry rule is not missing:** at the tank it is D-126,
cords up the standpipe and out through a grip with the drip loop OUTSIDE, with
separate tie groups for float and pump cords under D-156; at a cord cap it is D-046,
the cap plugs into a panel-mounted receptacle and is not fed through a grip.

### 1.1 Faces and entry order

**Which face, and the order of entries on it, is the enclosure owner's under D-146.
Where on that face, and the spacing, is INTERCONNECT's.**

**All three enclosures enter on the BOTTOM face.** MAIN-PANEL's is in parts.md - every
cord grip on the bottom, nothing but the five 22 mm devices on top. PUMP-BOXES' and
DISPLAY-BOX's are in entry-faces.md, decided from what is inside each box and from
D-047, with neither box using D-146's escape clause.

**One entry is not a gland at all.** RUN-009 crosses at a **panel-mount USB-C
BULKHEAD**, D-162, because a USB-C connector will not pass a grip bore and
re-terminating a USB-C cable is not a thing anyone should do. **The face and the order
are unchanged by that; the entry hardware is not.**

**Position on the face and spacing remain OPEN in every row**, because they follow
from a wall layout that does not exist while M-02 is open. **No allowance is being
held against any particular gap - see 2.3.**

### 1.2 Voltage class. INTERCONNECT's vocabulary, per D-150

| Value | Means | No number defines it |
|---|---|---|
| **LINE** | At building supply potential | Membership of the 120 VAC system, not a threshold |
| **24 V** | The panel's 24 V system, whatever the duty | Membership of that system |
| **SIGNAL** | Below the 24 V system: the driver logic supply, the step and direction conductors, the probe conductors, and the Pi's 5 V supply | Membership |

**EGC is not a voltage class.** A bonding conductor takes the voltage class of the
circuit it protects, and "grounding" is a duty. **Section 2.4 is what that decided.**

**AND ONE RULE THAT IS GENERAL RATHER THAN LOCAL, because it has now arrived from
three directions: A CONDUCTOR IS INSULATED FOR THE HIGHEST VOLTAGE PRESENT WHEREVER
IT GOES, NOT FOR ITS OWN CIRCUIT.**

| Arrival | The case |
|---|---|
| **F-113 and D-156**, from the standpipe | A 24 V float cord tied against a 120 V pump cord up one pipe. Rated for the bundle |
| **CBL-06 and D-163**, from the leak console | A 24 V supply pair sharing a jacket with contact legs in the 120 V chain. Rated for the jacket |
| **D-165**, from the ground bar | **A bar is a terminal that is ALWAYS IN THE 120 V CHAIN even in a box that holds only 24 V, because the ground is common.** Rated for the highest voltage anywhere on the bar |

**So the voltage class of a conductor is a property of its worst company, not of its
own duty**, and the three cases above are one rule with three addresses rather than
three exceptions. **It reaches every 24 V and SIGNAL jacket that carries a grounding
conductor under 2.4**, which is all of them.

### 1.3 Duty. MAIN-PANEL's vocabulary, per D-150

**ARC, COIL, SENSE**, from D-072's three tiers, defined in D2 section 4, which is its
single source. **Duty is a property of the POLE, not of the conductor** - D2's own
sentence. D5 derives each conductor's duty from the pole it leaves; the cell below is
that roll-up, generated rather than typed. G-45.

**A jacket that leaves no pole has no duty**, and that cell is n/a under 1.0. None is
a G-30 subject: G-30 separates poles inside a relay, and these leave no relay.

### 1.4 Segregation groups

A local list keyed to this document, per G-43. **It groups runs and states no
distance.** Cost of the whole scheme, per G-48: **no parts. One line in the routing
step of D4 per group.** It is not free and it is close to it.

| Group | Holds | What it prevents |
|---|---|---|
| **SEG-A** | LINE runs and cords | A line conductor being the realistic neighbour of a sense conductor, which is the short D-049 handed to the wiring plan |
| **SEG-B** | 24 V runs | As SEG-A. **It does not separate ARC duty from SENSE duty inside itself** - the duty column does that, and RUN-001, RUN-002 and RUN-012 show why one column could not |
| **SEG-C** | SIGNAL runs. **Widened 2026-09-05 from "SIGNAL runs to the drivers" to take RUN-009, rather than adding a group for one jacket** - G-48 | F-030 on the driver jackets specifically: eight step conductors in one jacket is the single most probable short in the build, and a step shorted to another step steps two heads together, violating G-06 in hardware where software cannot prevent it |
| **SEG-D** | Probe runs, alone | Kept separate by INTERCONNECT's standing open item and by entry-faces.md, which puts them alone at one end. **No rule exists yet for what SEG-D requires and I state none** |

**Three constraints no group satisfies:**

- **RUN-005 and RUN-006 are the same voltage class**, so no scheme that sorts by class
  separates them. F-029: a short between them makes the readback follow the command,
  which is precisely and only the failure G-09 exists to detect, and it removes weld
  detection too. **Separate jackets or provably non-adjacent, and entry-faces.md now
  enforces it at the entry too, with RUN-007 and RUN-008 between them.**
- **RUN-007 and RUN-008 each carry a G-27 complementary pair from one changeover
  pole**, both legs at the same potential on the same cable. **Neither pair may be
  split across jackets and neither may be moved out of the gap it holds.**
- **RUN-012, RUN-013, RUN-019 and part of RUN-020 are tied to one pipe by D-121 and
  cannot be separated by any group.** Section 4.

---

## 2. THE CABLE SCHEDULE

**Nineteen active jackets. Twenty-one ids issued, one retired.** Device names are
current: the **manifold pump**, D-144; **KM-DRV** the driver permissive contactor and
**KM-CHIL** the chiller and loop-pump receptacle switching element.

| RUN | End A | A face | End B | B face | Rows | Voltage | Duty | Provision | Seg | Blocked on |
|---|---|---|---|---|---|---|---|---|---|---|
| **RUN-001** | MAIN-PANEL: KM-DRV load side | BOTTOM | PUMP-BOX-A: driver motor supply | **BOTTOM, entry 1 of 2, power-block end** | P-06 | 24 V | **ARC** | Cut | SEG-B | P-06; CBL-01; CBL-02. **D-150's own case: 24 V voltage, ARC duty. A DC break with no zero crossing into eight drivers with bulk capacitors** |
| **RUN-002** | MAIN-PANEL: KM-DRV load side | BOTTOM | PUMP-BOX-B: driver motor supply | **BOTTOM, entry 1 of 2, power-block end** | P-06 | 24 V | **ARC** | Cut | SEG-B | P-06; CBL-01; CBL-02. **Both feeds leave one terminal downstream, parts.md - T-010 applies there, not here.** Same hand as box A: the two boxes are one build, not a mirrored pair |
| **RUN-003** | DISPLAY-BOX: logic board step and direction outputs | **BOTTOM, entry 2 of 8** | PUMP-BOX-A: driver STEP and DIR terminals | **BOTTOM, entry 2 of 2, logic-header end** | S-10; P-09 | SIGNAL | **n/a, no pole** | Cut | SEG-C | S-10; CBL-02; CBL-03. **Expect a split on F-030's per-signal returns. The entry rule is keyed to the board's geometry, not to this id, so it survives** |
| **RUN-004** | DISPLAY-BOX: logic board step and direction outputs | **BOTTOM, entry 3 of 8** | PUMP-BOX-B: driver STEP and DIR terminals | **BOTTOM, entry 2 of 2, logic-header end** | S-10; P-09 | SIGNAL | **n/a, no pole** | Cut | SEG-C | S-10; CBL-02; CBL-03, plus PUMP-BOXES' open division of the eight channels |
| **RUN-005** | DISPLAY-BOX: logic board permissive coil drive | **BOTTOM, entry 4 of 8** | MAIN-PANEL: KM-DRV coil | BOTTOM | S-07; **S-09 unmerged** | 24 V | **COIL** | Cut | SEG-B | S-07; CBL-01; CBL-03. **One conductor, two interface rows - S-09's own status says merge into S-07 or close, and D5 admits one row per conductor.** Duty is D-072 tier 2, a slave-coil drive |
| **RUN-006** | MAIN-PANEL: KM-DRV pole 2 | BOTTOM | DISPLAY-BOX: optocoupler input | **BOTTOM, entry 7 of 8** | S-08 | 24 V | **SENSE** | Cut | SEG-B | CBL-01; CBL-03; DISPLAY-BOX's input side. **Not adjacent to RUN-005 at either end, F-029.** Also open: whether KM-DRV's poles share one contact volume, which would put S-08 against G-30 with nowhere to move |
| **RUN-007** | MAIN-PANEL: K-FILL-D-Q changeover pole | BOTTOM | DISPLAY-BOX: two isolated Pi inputs | **BOTTOM, entry 5 of 8** | **S-03, both legs** | 24 V | **SENSE** | Cut | SEG-B | CBL-01; CBL-03; DISPLAY-BOX's input side. **Carries a G-27 pair, may not be split, may not leave the F-029 gap it holds** |
| **RUN-008** | MAIN-PANEL: K-DRY-Q changeover pole | BOTTOM | DISPLAY-BOX: two isolated Pi inputs | **BOTTOM, entry 6 of 8** | **S-20, both legs** | 24 V | **SENSE** | Cut | SEG-B | S-20; CBL-01; CBL-03. **As RUN-007** |
| **RUN-009** | **The 27 W USB-C brick**, on an unswitched receptacle on the main panel FACE, in neither enclosure | **n/a, a brick is not an enclosure.** The cable plugs into it | DISPLAY-BOX: Pi power | **BOTTOM, entry 8 of 8 - a panel-mount USB-C BULKHEAD, not a grip**, D-162 | P-07, **CLOSED** | **SIGNAL**, 5 V DC. **Not LINE** | **n/a, no pole** | **Supplied, and not cuttable** | SEG-C | **CBL-03 only.** P-07 is closed and every other cell is answered. **See 2.3 and 2.5** |
| **RUN-010** | Building branch circuit | **n/a, not an enclosure** | MAIN-PANEL: line input | BOTTOM | P-01 | LINE | **n/a, no pole** | Cut | SEG-A | P-01; CBL-01. **May be two jackets: D-137's dedicated chiller circuit is unaccounted for in P-01. If a disconnecting means is chosen it becomes this jacket's pole and the duty cell fills** |
| **RUN-011** | MAIN-PANEL: K-FILL-S solenoid pole | BOTTOM | FIELD: fill solenoid coil | **n/a, a coil housing has no faces** | **P-02** | LINE | **ARC** | Cut | SEG-A | P-02, whose text is stale per F-098; CBL-01; CBL-04. **D-072 puts the solenoid on the arcing side whatever its coil voltage** |
| **RUN-012** | FIELD: day tank floats, on the day tank standpipe | **n/a, a float has no faces.** Entry rule is D-126 | MAIN-PANEL: K-FILL-D and K-DRY coil chains | BOTTOM | S-02 | **24 V**, D-154 | **COIL** | **Supplied** | SEG-B | S-02; CBL-01; CBL-04; **F-100** cord length. **D2: every float conductor is COIL duty, being a series element in a coil chain.** Section 4 |
| **RUN-013** | FIELD: storage tank floats, on the storage standpipe | **n/a, as RUN-012** | MAIN-PANEL: K-FILL-S and permissive coil chains | BOTTOM | S-01 | **24 V**, D-154 | **COIL** | **Supplied** | SEG-B | S-01; CBL-01; CBL-04; F-100 |
| **RUN-014** | FIELD: leak detection sensor, on the floor | **n/a, a floor sensor has no faces** | The leak console, **remote and in no enclosure**, D-163 | **Its own housing entry, the manufacturer's** - not allocated under D-146 | S-04 | **OPEN** | **n/a, no pole** | Supplied | **OPEN** | S-04; CBL-04. **Voltage and segregation both wait on one lookup: the WaterBug's sensing-circuit class, which is stated in no file I read** - D-163, CBL-06 and parts.md's WaterBug entry all describe the 24 V supply and the Form C output and none describes the sensor lead. Section 5. **F-104 still governs where the sensor may sit** |
| **RUN-015** | The leak console, remote, 24 V in and Form C out | **Its own cord grip**, D-163 | MAIN-PANEL: permissive string | BOTTOM | **CBL-06** | **LINE-rated**, CBL-06 | **COIL or ARC, contested** | Cut | SEG-A | CBL-06; CBL-01. **The console's POSITION is the owner's and not fixed, so this jacket's route and length terms stay open while everything else about it closes.** The duty contest is unresolved: D-163 restates CBL-06's "legs in the 120 V chain" and does not adjudicate it against order.md's 24 Vdc coil, so under G-37 that is one claim in two places rather than two sources |
| **RUN-016** | DOSING: probes in the manifold probe section | **n/a, a wet fitting has no faces** | DISPLAY-BOX: the EZO circuits and their carriers | **BOTTOM, entry 1 of 8, alone at one end** | S-11 | SIGNAL | **n/a, no pole** | **Supplied** | SEG-D | S-11; CBL-03. **The EZO length limit is a lookup nobody has run** - section 5 |
| ~~RUN-017~~ | **RETIRED 2026-09-05 under D-149, and the number is never reused.** CBL-07 closed by D-165 and the grounding conductor turned out to live inside the jackets it protects, so this was never a jacket. Section 2.4 | | | | CBL-07, **closed** | | | | | |
| **RUN-018** | MAIN-PANEL: K-FILL-D-P pole, to a panel-mounted receptacle | **FACE**, D-046 | FIELD: transfer pump cord cap | **n/a, a cord cap has no face** | P-03 | LINE | **ARC** | **Cord** | SEG-A | P-03's circuit and rating |
| **RUN-019** | MAIN-PANEL: K-DRY-P pole, to a panel-mounted receptacle | **FACE**, D-046 | FIELD: manifold pump cord cap | **n/a, as RUN-018** | P-04 | LINE | **ARC** | **Cord** | SEG-A | P-04's circuit and rating. **On the day tank standpipe** - section 4 |
| **RUN-020** | MAIN-PANEL: **KM-CHIL**, to a panel-mounted receptacle | **FACE**, D-046 | FIELD: chiller cord cap and chiller loop pump cord cap | **n/a, as RUN-018** | P-05, as amended by D-137 | LINE | **ARC** | **Cord**, two | SEG-A | P-05, whose End A still names a chiller contactor D-108 removed. **KM-CHIL names the FUNCTION and no device performs it yet** |

### 2.1 What is filled, honestly

**Nineteen active jackets, 171 content cells: 153 FILLED, 16 with NO VALID VALUE, 2
still EMPTY.**

**Eighteen of the nineteen rows have no empty cell.** The two empties are RUN-014's
voltage and segregation and they share **one cause: the WaterBug's sensing-circuit
class, a lookup on a bought device.**

**No row is buildable, and the reason is unchanged: CBL-01 through CBL-04 are all
still OPEN.** The face half of those rows is now answered - parts.md for CBL-01,
entry-faces.md for CBL-02 and CBL-03, D-126 and D-156 for CBL-04 - and **my half,
position and spacing, needs the wall layout, which is M-02.** So the four rows close
when the wall layout exists and not before. **RUN-009 is the first jacket in this
build whose own interface row is CLOSED**, and it is still blocked by CBL-03 alone.

### 2.2 Rows that are not one physical thing

- **RUN-003 and RUN-004** are expected to split on F-030's per-signal returns. **Do
  not order or label against these two ids.** Their entry rule survives the split
  because entry-faces.md keyed it to the driver board's geometry rather than to an id.
- **RUN-009, RUN-018, RUN-019 and RUN-020 have no CDR- children and no TRM- landing
  point.** Each is a manufactured assembly - a USB-C cable, three cord caps - whose
  conductors nothing lands. **D5 will never name these four ids, and that is correct
  rather than an error to fix.**
- **RUN-017 is retired**, section 2.4.

### 2.3 THE DISPLAY BOX FACE: THE NAMED FAILURE IS GONE AND THE ALLOWANCE IS RELEASED

**The gap between entries 7 and 8 no longer carries a named failure, and I am no
longer holding face width for it.**

The failure was specific: **a LINE entry adjacent to a 24 V sense loop**, where a
short to an energised neighbour lights the optocoupler LED and reads the wrong way,
D-049. **D-162 removed the LINE entry rather than moving it.** With the AC-DC
conversion in a brick outside both enclosures, what crosses is 5 V DC over a USB-C
cable. **There is now no LINE entry anywhere on the display box face.**

**What releasing costs, per G-48: no parts, and it removes one instruction from D4's
routing step.** The width returns to the pool that F-030's split has a prior claim
on, which was the reason I declined to spend it.

**One consequence for DISPLAY-BOX, reported and not acted on.** entry-faces.md's rule
A orders the face by susceptibility and justified RUN-009's position at the far end
as putting LINE as far from the probes as the face allows. **RUN-009 is not LINE any
more, so that justification is void even though the position may still be right** - a
5 V supply is nearer the susceptible end of a ramp than the immune end. **The order is
the enclosure owner's under D-146 and I do not reorder it.** Cost of a review, per
G-48: no parts, one pass over a table that already exists.

**AND A CORRECTION AGAINST THIS DOCUMENT, recorded because G-47 was frozen out of
it.** The previous revision proposed that the LINE entry might leave the face "at zero
cost and with no width spent" if the Pi's supply landed as a cord under D-046's
precedent. **That was a cost claimed for a box INTERCONNECT does not own.**
DISPLAY-BOX owned it and found the remedy removed nothing: LINE still had to reach
the rail, so the same conductors sat in the same band behind the face. **The remedy
was not free, it was invisible.** The answer that did work came from outside both
boxes and from the owner. **G-47 is the rule and this document is one of its two
exhibits.**

### 2.4 CBL-07. CLOSED BY D-165, AND THE EGC IS NOT A JACKET

**CBL-07 is CLOSED. The shape is the owner's, not mine, and it corrects what the
previous revision of this section reasoned to.**

**A copper ground bar in the main panel is THE SINGLE POINT. Each remote enclosure has
its OWN LOCAL BAR. A green conductor inside the cross-box cable joins the local bar to
the main one, so THE BARS ARE DAISIED HOME rather than every device running back to
the main panel. One green conductor PER CABLE, not one per DEVICE.**

**RUN-017 retires under D-149.** The parent id goes, the conductors appear inside the
runs they protect, **nothing is renumbered around it and no suffix is issued.** It was
one of this document's three remaining causes and it is gone rather than filled.

**Which jackets carry one, derived from the rule rather than listed twice:**

| Jackets | Carry a grounding conductor? |
|---|---|
| **RUN-001 to RUN-008**, the cross-box cables | **Yes, one each.** This is what daisies the three local bars home |
| **RUN-010, RUN-011, RUN-015**, the LINE field jackets | **Yes.** A LINE circuit's equipment ground goes home in its own jacket |
| **RUN-009, RUN-018, RUN-019, RUN-020** | Whatever the manufactured assembly carries. **Not selectable and not landed by anyone here** |
| **RUN-012, RUN-013, RUN-014, RUN-016**, supplied field leads | Whatever the supplied part carries |

**Two properties of the bar that belong in a schedule a person reads, both the
owner's:**

**1. THE BAR IS THE SINGLE POINT AND NOTHING BONDS ANYWHERE ELSE.** It is written down
for a reason a builder will recognise: **a builder who finds a convenient screw will
use it.** A second bonding point is not a spare, it is a second path.

**2. A BAR IS ALWAYS IN THE 120 V CHAIN, even in a box that holds only 24 V**, because
the ground is common. **So whatever insulates a conductor landing there is rated for
the highest voltage anywhere on the bar** - which is section 1.2's general rule, and
this is its third arrival.

**What it costs, per G-48, and it is not zero, per G-47:** no new cable and no new
gland, because the conductor rides a jacket that already exists - **but it is a
cable-SELECTION requirement that D7 buys and D5 counts**, and it adds three local bars
as parts with three buy lines and three mounting steps. **What it buys against the
alternative of every device running home separately: one conductor per cable instead
of one per device**, which is fewer conductors in every cross-box jacket and fewer
landings at the main bar.

**AND ONE THING DECIDING THE SHAPE REVEALED, routed and not solved.** CBL-07 names
the four enclosures. **D-121 adopted the standpipe as a method and deliberately
adopted NO MATERIAL** - "no dimension, no material, no attachment detail, no count",
in terms. **If a standpipe is metal, it is a conductive part standing in a tank with
120 V pump cords tied to it under D-121, and nothing in this tree bonds it.** Under
D-156 those cords are now in their own tie group and their insulation is rated for the
bundle, which is the mitigation for a fault; it is not a bond.

**I state nothing about whether it needs one and I raise it before the material is
chosen, because that is when it is free to decide.** Priced both ways, per G-48: if
the pipe is non-conductive the question does not arise and costs nothing; if it is
metal, a bond costs one conductor, one landing at the bar, and one line in the buy
list. **WATER owns the material and MAIN-PANEL owns the bar. Not mine to answer, and
cheap only while unbought.**

### 2.5 One question the brick raises, one line, no new id

**A 27 W brick hangs on a panel-face receptacle in a room where water moves tank to
tank.** D-046 covers a cord cap plugging in from outside; **a brick is heavier than a
cord cap and its only support is its own plug.** If it has a separate mains cord
rather than integral pins, that cord is a cord route of the RUN-018 family and needs
an id. **I have issued none, because inventing a jacket that may not exist is exactly
what D-149 and rule 3 forbid.** Routed to MAIN-PANEL, which owns the face: **which is
it, and what holds the brick.**

---

## 3. THE TERMINAL SCHEDULE

### 3.1 How a TRM- id is formed

```
TRM-<where>.<on what>.<which>
```

**Three parts, always three.** `where` is the enclosure or field device, from a
closed set written out and computed nowhere: `MAIN-PANEL`, `PUMP-BOX-A`,
`PUMP-BOX-B`, `DISPLAY-BOX`, `FIELD`. `on what` is the device or block **BY NAME**,
per G-28, never a socket position. `which` is **the marking as printed on the part**,
per F-051; where nothing is printed it is a descriptor in braces.

**No part is a position, an index or an ordinal.** A digit may appear inside `which`
and never as a whole part. **An id changes only when the PART changes**, so it
survives a relay moving sockets, a jacket splitting and a channel being reassigned.
**It is never derived from a RUN- id and no RUN- id is derived from it.**

**A mated connector is not a landing point.** RUN-009's bulkhead, and the three cord
caps, land no conductor on a clamp and carry no TRM- id.

### 3.2 The marking source column

**F-051 is the entire reason.** Every file in this tree said VM; the part carries a
circled plus and a circled minus. **A marking quoted from a document is not a marking
read off a part.**

| Source | Means |
|---|---|
| `PART` | Read off the physical part |
| `FILE` | Quoted from a tree document. **Provisional until somebody looks** |
| `DESCRIBED` | Nothing is printed. `which` is a braced descriptor |

**G-48 on this column: it costs one word per row and no parts, and it prevents a
build sheet naming a terminal that is not on the part** - T-013, the failure that
once told a builder to verify a short across a 5 V supply and tick the box. **It goes
in.**

**Not one row below is marked PART. F-106: nobody in this project has ever been asked
to look at a terminal and report what is printed on it.**

### 3.3 The schedule

| TRM | Device, by name | Which | Source | Runs landed | Row | Blocked on |
|---|---|---|---|---|---|---|
| `TRM-MAIN-PANEL.KM-DRV.{pole 1, motor supply}` | **KM-DRV** | `{pole 1}` | DESCRIBED | RUN-001, RUN-002 | P-06 | **Marking not read, F-106.** **T-010 applies: two jackets leave one terminal** |
| `TRM-MAIN-PANEL.KM-DRV.{pole 2, readback}` | **KM-DRV** | `{pole 2}` | DESCRIBED | RUN-006 | S-08 | Marking not read. Also open: whether KM-DRV's poles share one contact volume, which would put S-08 against G-30 with nowhere to move |
| `TRM-MAIN-PANEL.KM-DRV.{coil}` | **KM-DRV** | `{coil}` | DESCRIBED | RUN-005 | S-07 | S-07, which must state where the coil positive is taken from; marking not read |
| `TRM-MAIN-PANEL.K-FILL-S.{solenoid pole}` | **K-FILL-S**, order.md | `{solenoid pole}` | DESCRIBED | RUN-011 | P-02 | P-02; marking not read. **The pole is sized on the make-and-break event, not the holding figure** |
| `TRM-MAIN-PANEL.K-FILL-D-Q.{S-03 changeover pole}` | **K-FILL-D-Q**, order.md | `{changeover pole}` | DESCRIBED | RUN-007 | S-03 | Marking not read. **Both legs of one pole land here and G-27 requires both on RUN-007** |
| `TRM-MAIN-PANEL.K-DRY-Q.{S-20 changeover pole}` | **K-DRY-Q**, order.md | `{changeover pole}` | DESCRIBED | RUN-008 | S-20 | S-20; marking not read. **The relay is called K-DRY in the interface table and K-DRY-Q in order.md, so the id is unstable until one name wins** |
| `TRM-MAIN-PANEL.{ground bar}.{...}` | **{ground bar}**, copper, not a bought part | OPEN | OPEN | The grounding conductor of every jacket landing in this panel | **CBL-07**, closed | The bar is not bought. **It is THE SINGLE POINT: nothing bonds anywhere else, D-165** |
| `TRM-PUMP-BOX-A.{local ground bar}.{...}` | **{local ground bar}**, not a bought part | OPEN | OPEN | RUN-001, RUN-003 | **CBL-07**, closed | Not bought. **Daisied to the main bar by the green conductor in RUN-001** |
| `TRM-PUMP-BOX-B.{local ground bar}.{...}` | **{local ground bar}**, not a bought part | OPEN | OPEN | RUN-002, RUN-004 | **CBL-07**, closed | Not bought. **Daisied by RUN-002** |
| `TRM-DISPLAY-BOX.{local ground bar}.{...}` | **{local ground bar}**, not a bought part | OPEN | OPEN | RUN-005 to RUN-008 | **CBL-07**, closed | Not bought. **Daisied by the panel-to-display jackets** |
| `TRM-FIELD.{fill solenoid}.{coil lead}` | The fill solenoid specified by D-136 | OPEN | **OPEN** | RUN-011 | P-02 | **Coil lead identification has never been looked up.** Per F-051 it is named by what is printed on the part, and nobody has looked |
| `TRM-FIELD.{leak console}.{...}` | Winland WaterBug WB200, remote, D-163 | OPEN | OPEN | RUN-014, RUN-015 | CBL-06, S-04 | **A bought device: its terminals are the manufacturer's and nobody has looked.** MAIN-PANEL states which legs it uses |
| `TRM-PUMP-BOX-A.{driver}.{...}` | OPEN | OPEN | OPEN | RUN-001, RUN-003 | P-06, S-10, P-09 | S-10; P-06. **The pin list is known and the MARKINGS are not** - parts.md records that the flat pin list is a list of names that was read as an order, and the board is two connectors |
| `TRM-PUMP-BOX-B.{driver}.{...}` | OPEN | OPEN | OPEN | RUN-002, RUN-004 | P-06, S-10, P-09 | As PUMP-BOX-A |
| `TRM-DISPLAY-BOX.{logic board}.{...}` | OPEN. The board is hand built and does not exist | OPEN | OPEN | RUN-003 to RUN-008, RUN-016 | S-07, S-08, S-03, S-20, S-10, S-11 | S-12 is not frozen and the board does not exist. **RUN-009 no longer lands here: it terminates at a bulkhead connector** |

**Fifteen landing points. Six name their device. None is buildable, and every one of
the six is blocked on the same thing: nobody has looked at the part.** F-106.

**ONE PART THAT MUST NOT APPEAR ON ANY OF THESE ROWS, recorded here because a
terminal schedule is where someone would reach for it: a DIN-rail grounding terminal
block.** It bonds to the rail, the rail bonds to the plate, **and the plate is
plastic, so it bonds to nothing.** The parallel build bought seven before the bar
decision and is returning them. **Nothing in this tree assumes one, BOSS has checked,
and none is introduced here.** A local bar is a bar, not a rail block.

### 3.4 The check this table holds that no other document can

**T-009 and T-010: a terminal carrying exactly one conductor is an open circuit, not
a spare, and clamps are counted against conductors rather than assumed.** The first
row shows two jackets leaving one terminal. Neither question is answerable from D5 or
from section 2, because both are organised by a conductor's journey and this table is
organised by its destination.

---

## 4. THE STANDPIPE ADJACENCY. F-113, ANSWERED AND ACTED ON

**The method is not reopened: D-121 answers a float that has moved, and nothing here
measures a level, so an unmarked float that slips is invisible.**

D-049 amended G-22 so the severed case is answered by the circuit and the short case
by **adjacency - the wiring plan.** That escape assumes a route with choices in it.
**D-121 fixes the adjacency at worst case by construction**, so on RUN-012, RUN-013,
RUN-019 and part of RUN-020 there is no wiring plan left to answer with. Grade:
**STRUCTURAL** while D-121 stands.

**The expensive failure is float-to-float, not the cross-class one.** Under D-154
every float is a series element in a coil chain, so a bridge between pairs on one pipe
**shorts out the elements between the bridge points and closes the chain around an
open float.** Severed is safe; this is not. **And it is already paid for**: D-130's
overflow, FL-11 and FL-12, was made a requirement for exactly that failure and lands
above the high-high per D-134.

| | Parts and steps, per G-48 | Status |
|---|---|---|
| **Float cord insulation rated for the highest voltage in the bundle** | No extra part and no extra step. It is an attribute of a part not yet bought, so it is free only while the requirement is open | **TAKEN**, D-156 |
| **Separate tie groups for float and pump cords** | No extra part - the same ties. One instruction in the standpipe assembly step | **TAKEN**, D-156 |
| **Shields, conduits, barriers or dividers on the pipe** | A part per pipe, a buy line, an assembly step, and an obstruction at the tie a person must reach under D-131 | **REJECTED under G-48.** It is thorough, and **none of it touches the expensive failure, which is float-to-float and inside one class** |
| **Removing the pump cords from the pipe** | Would cost a separate cord fixture per pump. Not priced by anyone who owns it | **LOGGED, NOT PURSUED.** D-121's sentence is the owner's, and per G-47 I do not call it cheap from outside |

**Two residuals recorded rather than solved**, both in D-156: a tie is a compression
point and D-131 puts a person's hands on it with both pumps running under D-143; and
adjacency stops being a recorded fact, so a fault on the pipe cannot be localised by
knowing what lies next to what.

---

## 5. REQUIREMENTS AND SEARCH TERMS

No value is stated. Each is a lookup the owner runs under G-15.

| For | Requirement | Search term |
|---|---|---|
| RUN-010, RUN-011, RUN-015, RUN-018 to RUN-020 | A flexible LINE-class cable for a wall route in a room where water moves tank to tank, **carrying a grounding conductor**, section 2.4 | `flexible power cable 600 V oil resistant wet location`; `tray cable TC-ER exposed run wall` |
| **RUN-001 to RUN-008**, the cross-box jackets | **A cable carrying a grounding conductor in addition to its circuit conductors**, since each one daisies a local bar home, D-165. **And its insulation rated for the highest voltage anywhere on the bar it lands at, not for its own circuit** - section 1.2 | `multiconductor control cable with green ground conductor 600 V`; `control cable 600 V insulation rating low voltage circuit` |
| **The four ground bars** | A copper bar for the main panel and one local bar for each remote enclosure, mountable in a plastic-plated box. **Not a DIN-rail grounding block** - section 3.3 | `copper ground bar kit enclosure mount insulated standoff`; `equipment grounding bar screw terminal copper` |
| **RUN-014** | **The WaterBug's sensing-circuit class, so this jacket's voltage and segregation can be filled.** The two remaining empty cells in this document | `Winland WaterBug WB200 sensor lead circuit voltage`; `WaterBug water sensor extension cable specification` |
| RUN-015 | Confirmation that every conductor in one jacket may share the higher rating CBL-06 requires | `600 V insulated conductor mixed circuit same raceway control cable` |
| RUN-016 | The maximum probe cable length the EZO circuits tolerate. **Not from any file in this tree** | `Atlas Scientific EZO pH EC probe cable length limit extension` |
| **RUN-009** | **A panel-mount USB-C bulkhead** for the display box face, sealed to at least the box's own rating in a bottom-face orientation | `panel mount USB-C bulkhead pass-through IP67 waterproof` |
| Every gland entry | A cord grip per entry, sized to the cable chosen, sealed at least to the enclosure's rating and suitable for a bottom face | `liquid tight cord grip strain relief NPT cable range chart` |
| The display box bottom face | **How many entries the stated face can carry, which is D3's geometry and is not derivable from the entry order** | D3, not a lookup |
| The segregation rule | A stated rule for which classes may share a duct, a jacket, a clip run or a tie bundle, and what an unavoidable crossing requires | `control panel power and signal circuit segregation separation`; `Class 1 Class 2 circuits same raceway` |
| Labelling | A marker carrier that holds the canonical three-part TRM- form and, on a per-channel core, the channel token in addition without merging them | `wire marker sleeve character capacity heat shrink printable` |

---

## 6. WHY THERE IS NO DUPLICATION CONTRACT IN THIS DOCUMENT

**G-45. D5 and D6 are generated from one source, so they cannot disagree, and a
schedule is never hand-transcribed.** The rule that said they must agree was deleted
rather than restated: **a contract needs a reader who obeys it; a mechanism does
not.**

**Two facts do not survive generation and are therefore stated here and nowhere
else:**

1. **The terminal marking source, section 3.2.** A generator can make two documents
   carry the same marking. **It cannot make anyone have looked at the part.**
2. **The per-conductor fail direction, which lives in D5 and appears nowhere in this
   document.** Established per conductor and never inherited, F-017. **A jacket-level
   roll-up would average several directions into one**, which is the inheritance that
   put S-03's fail direction on file as S-08's before anyone checked.

---

## 7. STATUS

**Stopped part way. INTERCONNECT does not declare this finished** - rule 7.

**Eighteen of nineteen rows have no empty cell, and no row is buildable.** Both are
true at once and that is the document working: the schedule is finished for those
jackets and the crossings behind them are not. **CBL-01 through CBL-04 are still OPEN
and every jacket lands at a gland or bulkhead they govern.**

**Of the three causes that held this document's empty cells, two are gone and one
remains.** P-07's form closed by D-162 and filled RUN-009. **CBL-07 closed by D-165
and did not fill a cell at all - it removed RUN-017 from the schedule**, which is the
better outcome and the one a shape argument could not have produced. The leak console
closed by D-163 on everything except one lookup.

**What actually closes them now, and it is one thing.** Their face half is answered -
parts.md, entry-faces.md, D-126 and D-156. **My half is position and spacing, and
that needs the wall layout, M-02**, which is open with DOSING and PUMP-BOXES claiming
the same wall and the tubing between them setting the spacing. **The whole schedule
is now downstream of one mechanical arbitration.**

**Three smaller things, in order:** the WaterBug sensing-circuit lookup, which is the
last two empty cells; **F-030's per-signal returns**, after which RUN-003 and RUN-004
retire and are reissued under D-149 and the display box face's remaining width becomes
knowable; and **the S-07 and S-09 merge**, because RUN-005 carries one conductor with
two interface rows and D5 admits one.

**Not returned, so no absence is read as an answer:** no wall layout, because M-02 is
open and Z5 is undefined; **no answer to channel-token.md's monotone CH1 to CH8
question, which is unanswered rather than no**, for the same reason; **no spacing
anywhere, and no allowance held against any gap** - section 2.3; and no gland count,
position, cable selection, core count, cut length or terminal number, all of which are
requirements in section 5.
