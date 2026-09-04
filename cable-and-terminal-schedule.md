# D6. Cable and terminal schedule

**Owner: INTERCONNECT. Issued 2026-09-04, revised the same day** against the duty
vocabulary, the contactor names, the S-03 and S-20 amendments, D-156, and the entry
faces returned by PUMP-BOXES and DISPLAY-BOX in subsystems/entry-faces.md.

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

---

## 1. HOW TO READ A RUN- ROW

**RUN-nnn is ONE JACKET, not a route.** D-149. A conductor travels in a jacket, so
D5's cable column names one of these.

**The number carries no meaning.** Not a route order, not a class, not a build
sequence. No rule is keyed to it and a gap is never closed.

**If a jacket splits, its id is RETIRED and new ids are issued.** D-149. Never a
suffix: RUN-007a is arithmetic on an identifier and is the off-by-one generator
channel-token.md's forbidden list exists to prevent. **Rows expected to split are
marked in the Blocked on column.**

### 1.0 A cell has THREE states, not two

**A cell that can never be filled must not look like one that has not been filled
yet.** Schema rule, applied throughout:

| State | Written as | Means |
|---|---|---|
| **Filled** | The value | |
| **No valid value** | **n/a**, with the reason | The thing at that end has no such property. **It is not waiting on anybody and it is counted out of the empty total** |
| **Empty** | **OPEN**, with the blocker in the last column | Genuinely not yet answered |

**Applying it cost twelve cells that had been counted as filled.** Seven duty cells on
jackets that leave no pole, and five face cells on things that are not enclosures: a
building branch circuit, a wet fitting, and three cord caps. **A float, a solenoid
coil, a floor sensor, a cord cap and a probe fitting have no faces.** Asking them for
one is the CBL- shape of F-097 again - a column asking for a kind of value the thing
at that end does not have - and DISPLAY-BOX raised it in entry-faces.md section 4
before this document had a way to record it.

**Where a face is n/a, the entry rule is not missing.** At the tank it is D-126: cords
run up the standpipe and leave through a grip with a drip loop OUTSIDE the box, with
separate tie groups for float and pump cords under D-156. At a cord cap it is D-046:
the cap plugs into a panel-mounted receptacle and is not fed through a grip.

### 1.1 Faces and entry order

**Which face, and the order of entries on it, is the enclosure owner's under D-146.
Where on that face, and the spacing, is INTERCONNECT's.**

**All three enclosures enter on the BOTTOM face.** MAIN-PANEL's is on file in
parts.md - every cord grip on the bottom, nothing but the five 22 mm devices on top.
PUMP-BOXES' and DISPLAY-BOX's are in entry-faces.md, decided from what is inside each
box and from D-047, with neither box using D-146's escape clause. **The face cells
below carry the entry's position in the stated order; the order's reasoning is not
restated here.**

**Position on the face and spacing remain OPEN in every row**, because they follow
from a wall layout that does not exist while M-02 is open - **with one exception that
is a decision rather than a measurement, section 2.3.**

### 1.2 Voltage class. INTERCONNECT's vocabulary, per D-150

| Value | Means | No number defines it |
|---|---|---|
| **LINE** | At building supply potential | Membership of the 120 VAC system, not a threshold |
| **24 V** | The panel's 24 V system, whatever the duty | Membership of that system |
| **SIGNAL** | Below the 24 V system: the driver logic supply, the step and direction conductors, the probe conductors | Membership |

**EGC is not a voltage class.** A bonding conductor takes the voltage class of the
circuit it protects, and "grounding" is a duty. Accepted 2026-09-04.

### 1.3 Duty. MAIN-PANEL's vocabulary, and the cell is a roll-up

**ARC, COIL, SENSE.** Stated by MAIN-PANEL from D-072's three tiers, defined in D2
section 4, which is its single source. **Duty is a property of the POLE, not of the
conductor** - D2's own sentence. D5 derives each conductor's duty from the pole it
leaves; the cell below is that roll-up, generated rather than typed. G-45.

**A jacket that leaves no pole has no duty**, and that cell is n/a under 1.0. Seven
are, and none is a G-30 subject: G-30 separates poles inside a relay, and these leave
no relay.

### 1.4 Segregation groups

A local list keyed to this document, per G-43. **It groups runs. It states no
distance, and no separation distance exists anywhere in this tree yet.**

| Group | Holds | What it prevents, and what it costs - G-44 |
|---|---|---|
| **SEG-A** | LINE runs and cords | Prevents a line conductor being the realistic neighbour of a sense conductor, which is the short D-049 handed to the wiring plan. Costs nothing: it is a routing rule, not a part |
| **SEG-B** | 24 V runs | As SEG-A. **It does not separate ARC duty from SENSE duty inside itself** - the duty column does that, and RUN-001, RUN-002 and RUN-012 show why one column could not |
| **SEG-C** | SIGNAL runs to the drivers | F-030: eight step conductors in one jacket is the single most probable short in the build, and a step shorted to another step steps two heads together, violating G-06 in hardware where software cannot prevent it |
| **SEG-D** | Probe runs, alone | INTERCONNECT's standing open item names probes separately, and entry-faces.md puts them alone at one end of the display box face. **No rule exists yet for what SEG-D requires and I state none** |

**Three constraints no group satisfies:**

- **RUN-005 and RUN-006 are the same voltage class**, so no scheme that sorts by class
  separates them. F-029: a short between them makes the readback follow the command,
  which is precisely and only the failure G-09 exists to detect, and it removes weld
  detection too. **The jacket rule is separate jackets or provably non-adjacent, and
  entry-faces.md now enforces it at the entry as well, with RUN-007 and RUN-008
  between them.**
- **RUN-007 and RUN-008 each carry a G-27 complementary pair from one changeover
  pole.** G-27's rule is both legs at the same potential **on the same cable**, so
  **neither pair may be split across jackets**, and neither may be moved out of the
  gap it holds.
- **RUN-012, RUN-013, RUN-019 and part of RUN-020 are tied to one pipe by D-121 and
  cannot be separated by any group.** Section 4, and D-156 is what was done about it.

---

## 2. THE CABLE SCHEDULE

Device names are current: the **manifold pump**, D-144; **KM-DRV** the driver
permissive contactor and **KM-CHIL** the chiller and loop-pump receptacle switching
element, both named 2026-09-04.

| RUN | End A | A face | End B | B face | Rows | Voltage | Duty | Provision | Seg | Blocked on |
|---|---|---|---|---|---|---|---|---|---|---|
| **RUN-001** | MAIN-PANEL: KM-DRV load side | BOTTOM | PUMP-BOX-A: driver motor supply | **BOTTOM, entry 1 of 2, power-block end** | P-06 | 24 V | **ARC** | Cut | SEG-B | P-06. **D-150's own case: 24 V voltage, ARC duty. A DC break with no zero crossing into eight drivers with bulk capacitors** |
| **RUN-002** | MAIN-PANEL: KM-DRV load side | BOTTOM | PUMP-BOX-B: driver motor supply | **BOTTOM, entry 1 of 2, power-block end** | P-06 | 24 V | **ARC** | Cut | SEG-B | P-06. **Both feeds leave one terminal downstream, parts.md - T-010 applies there, not here.** Same hand as box A: the two boxes are one build, not a mirrored pair |
| **RUN-003** | DISPLAY-BOX: logic board step and direction outputs | **BOTTOM, entry 2 of 8** | PUMP-BOX-A: driver STEP and DIR terminals | **BOTTOM, entry 2 of 2, logic-header end** | S-10; P-09 | SIGNAL | **n/a, no pole** | Cut | SEG-C | S-10. **Expect a split: F-030's per-signal returns. The entry rule is keyed to the board's geometry, not to this id, so it survives the split** |
| **RUN-004** | DISPLAY-BOX: logic board step and direction outputs | **BOTTOM, entry 3 of 8** | PUMP-BOX-B: driver STEP and DIR terminals | **BOTTOM, entry 2 of 2, logic-header end** | S-10; P-09 | SIGNAL | **n/a, no pole** | Cut | SEG-C | S-10, plus PUMP-BOXES' open division of the eight channels between boxes |
| **RUN-005** | DISPLAY-BOX: logic board permissive coil drive | **BOTTOM, entry 4 of 8** | MAIN-PANEL: KM-DRV coil | BOTTOM | S-07; **S-09 unmerged** | 24 V | **COIL** | Cut | SEG-B | S-07. **One conductor, two interface rows - S-09's own status says merge into S-07 or close, and D5 admits one row per conductor.** Duty is D-072 tier 2, a slave-coil drive |
| **RUN-006** | MAIN-PANEL: KM-DRV pole 2 | BOTTOM | DISPLAY-BOX: optocoupler input | **BOTTOM, entry 7 of 8** | S-08 | 24 V | **SENSE** | Cut | SEG-B | DISPLAY-BOX's input side. **Not adjacent to RUN-005 at either end, F-029.** Also open: whether KM-DRV's poles share one contact volume, which would put S-08 against G-30 with nowhere to move |
| **RUN-007** | MAIN-PANEL: K-FILL-D-Q changeover pole | BOTTOM | DISPLAY-BOX: two isolated Pi inputs | **BOTTOM, entry 5 of 8** | **S-03, both legs** | 24 V | **SENSE** | Cut | SEG-B | DISPLAY-BOX's input side. **Carries a G-27 pair, may not be split, and may not be moved out of the F-029 gap it holds** |
| **RUN-008** | MAIN-PANEL: K-DRY-Q changeover pole | BOTTOM | DISPLAY-BOX: two isolated Pi inputs | **BOTTOM, entry 6 of 8** | **S-20, both legs** | 24 V | **SENSE** | Cut | SEG-B | S-20. **As RUN-007** |
| **RUN-009** | MAIN-PANEL: fused, NOT relay switched receptacle | BOTTOM | DISPLAY-BOX: Pi power | **BOTTOM, entry 8 of 8, far end** | P-07 | LINE, **contested** | **n/a, no pole** | **OPEN** | SEG-A | **P-07 reads CLOSED in the interface table while display-box.md still carries its form as open.** The face holds however the supply is provided; the provision cell does not. **Section 2.3 is about this entry** |
| **RUN-010** | Building branch circuit | **n/a, not an enclosure** | MAIN-PANEL: line input | BOTTOM | P-01 | LINE | **n/a, no pole** | Cut | SEG-A | P-01. **May be two jackets: D-137's dedicated chiller circuit is unaccounted for in P-01. If a disconnecting means is chosen it becomes this jacket's pole and the duty cell fills** |
| **RUN-011** | MAIN-PANEL: K-FILL-S solenoid pole | BOTTOM | FIELD: fill solenoid coil | **n/a, a coil housing has no faces** | **P-02** | LINE | **ARC** | Cut | SEG-A | P-02, whose text is stale per F-098: it says the coil voltage is undecided and D-136 specified the valve. **D-072 puts the solenoid on the arcing side whatever its coil voltage** |
| **RUN-012** | FIELD: day tank floats, on the day tank standpipe | **n/a, a float has no faces.** Entry rule is D-126 | MAIN-PANEL: K-FILL-D and K-DRY coil chains | BOTTOM | S-02 | **24 V**, D-154 | **COIL** | **Supplied** | SEG-B | S-02; **F-100** cord length. **D2: every float conductor is COIL duty, being a series element in a coil chain.** Section 4 |
| **RUN-013** | FIELD: storage tank floats, on the storage standpipe | **n/a, as RUN-012** | MAIN-PANEL: K-FILL-S and permissive coil chains | BOTTOM | S-01 | **24 V**, D-154 | **COIL** | **Supplied** | SEG-B | S-01; F-100 |
| **RUN-014** | FIELD: leak detection sensor | **n/a, a floor sensor has no faces** | MAIN-PANEL: leak console | **OPEN** | S-04 | **OPEN** | **n/a, no pole** | Supplied | **OPEN** | S-04; **the console's position is stated in no file**; **F-104** - a floor built to move water to a track drain hides a leak from a floor sensor, so the sensor's position and this jacket's class are both open |
| **RUN-015** | MAIN-PANEL: leak console, 24 V in and Form C out | **OPEN** | MAIN-PANEL: permissive string | BOTTOM | **CBL-06** | **LINE-rated**, CBL-06 | **COIL or ARC, contested** | Cut | SEG-A | CBL-06; the console's position. **The permissive string's voltage class decides the duty cell and it is the G-30 line itself: as a 24 V coil string these legs are COIL; as a 120 V bus they are ARC under D-072 tier 1, and ARC may not share a relay with SENSE** |
| **RUN-016** | DOSING: probes in the manifold probe section | **n/a, a wet fitting has no faces** | DISPLAY-BOX: the EZO circuits and their carriers | **BOTTOM, entry 1 of 8, alone at one end** | S-11 | SIGNAL | **n/a, no pole** | **Supplied** | SEG-D | S-11. **The EZO length limit is a lookup nobody has run** - section 5 |
| **RUN-017** | MAIN-PANEL: ground bar | BOTTOM | **OPEN. A SET, not one end** | **OPEN** | **CBL-07** | Takes the class it protects | **n/a, no pole** | Cut | Rides its circuit | CBL-07. **PROVISIONAL ID.** An EGC is either a conductor inside each other jacket or a separate bonding run to each plastic box, and those are different id counts. **A separate bonding run takes the face and position of the circuit it protects and adds no new entry rule.** This row retires under D-149 when CBL-07 returns |
| **RUN-018** | MAIN-PANEL: K-FILL-D-P pole, to a panel-mounted receptacle | **FACE**, D-046 | FIELD: transfer pump cord cap | **n/a, a cord cap has no face** | P-03 | LINE | **ARC** | **Cord** | SEG-A | P-03's circuit and rating |
| **RUN-019** | MAIN-PANEL: K-DRY-P pole, to a panel-mounted receptacle | **FACE**, D-046 | FIELD: manifold pump cord cap | **n/a, as RUN-018** | P-04 | LINE | **ARC** | **Cord** | SEG-A | P-04's circuit and rating. **On the day tank standpipe** - section 4 |
| **RUN-020** | MAIN-PANEL: **KM-CHIL**, to a panel-mounted receptacle | **FACE**, D-046 | FIELD: chiller cord cap and chiller loop pump cord cap | **n/a, as RUN-018** | P-05, as amended by D-137 | LINE | **ARC** | **Cord**, two | SEG-A | P-05, whose End A still names a chiller contactor D-108 removed. **KM-CHIL names the FUNCTION and no device performs it yet.** The loop pump's cord is on the day tank standpipe |

### 2.1 What is filled, honestly

**Twenty jackets, 180 content cells: 157 FILLED, 16 with NO VALID VALUE, 7 still
EMPTY.**

**The filled total did not move when twelve face cells were filled, and that is the
finding rather than a coincidence.** Twelve cells that had been counted as filled were
never fillable - seven duty cells on jackets that leave no pole, five face cells on
things that are not enclosures - so twelve arrived and twelve were reclassified.
**Under the old two-state count this document would have reported 169 of 180 and
been wrong by twelve in the flattering direction.**

**Sixteen of the twenty rows now have no empty cell at all**, up from four. **A row
with no empty cell is not a buildable row**: all sixteen are still blocked on their
interface rows, and that is the document working as intended.

**The seven remaining empties reduce to three causes:**

| Cause | Cells |
|---|---|
| **P-07's form** - closed in principle, open as a conductor | RUN-009's provision |
| **The leak console's position, stated in no file** | RUN-014's B face, voltage and segregation; RUN-015's A face |
| **CBL-07's shape** - one conductor per jacket, or a bonding run per box | RUN-017's End B and its face |

### 2.2 Three rows that are not one physical thing

- **RUN-017** is one id standing in for a set of unknown size. It retires under D-149.
- **RUN-003 and RUN-004** are expected to split on F-030's per-signal returns. **Do
  not order or label against these two ids.** Their entry rule survives the split
  because entry-faces.md keyed it to the driver board's geometry rather than to an id.
- **RUN-018, RUN-019 and RUN-020 have no CDR- children and no TRM- landing point.** A
  cord's conductors are inside a manufactured assembly and nothing lands them. **D5
  will never name these three ids, and that is correct rather than an error to fix.**

### 2.3 THE ONE GAP ON THE DISPLAY BOX FACE THAT CARRIES A NAMED FAILURE

**Routed to INTERCONNECT by entry-faces.md 3.3 and answered here.**

Ordering by susceptibility puts the LINE entry, RUN-009, at the far end, which gives
it the fewest neighbours the face allows. Its one neighbour is RUN-006, a 24 V SENSE
run. **Every candidate neighbour for a LINE entry on this face has a stated unsafe
short case** - an optocoupler sense loop shorted to an energised neighbour lights the
LED and reads the wrong way, D-049; the coil drive shorted to something live is
F-019's shorted output device against G-07. **No order removes it. The remedy is
spacing and spacing is mine.**

**What spacing costs, and it is not nothing.**

**1. Face width is zero-sum.** Eight entries share one bottom face. Widening the gap
between entries 7 and 8 narrows another gap or pushes entries toward the ends.
**Which gaps can afford to give is answerable today: 2 to 3, and 5 to 6.** Both are
same-class, same-duty neighbours - two step-and-direction jackets to two identical
boxes, and two SENSE jackets each carrying a G-27 pair. **Which gaps cannot: 4 to 5
and 6 to 7, because those are the two holding RUN-005 and RUN-006 apart, and
narrowing them attacks the rule the whole order exists to enforce.** And 1 to 2, which
is SEG-D keeping the probes alone. **So the cost is paid out of the two cheapest gaps
on the face, and the expensive ones are identified rather than eroded by an even
spread.**

**2. The usable band is narrower than the face.** A grip needs flat, unobstructed
material on both sides of the wall for its nut, so corners and any reinforced or
radiused region are not available. **I state no dimension. What I state is that the
count of entries the face can carry is a D3 question and is not derivable from the
order.**

**3. And the real cost is a prior claim: RUN-003 and RUN-004 are expected to split.**
When they do, the signal band needs more entries on this same face. **Width spent now
on gap 7 to 8 is width the split has a prior claim on**, and F-030 is not settled.
**Spacing decided before the split is spacing decided against an unknown entry
count.** Grade: **CURRENT.** What would change it: F-030 settling, which fixes the
entry count in the signal band and makes the remaining width knowable.

**4. The cheapest resolution may be that the LINE entry stops being an entry.**
RUN-009's provision is OPEN. D-046's precedent is that a panel-mounted receptacle
takes a cord cap from outside and no grip is involved. **If the Pi's supply lands that
way, the LINE entry leaves this face and the named failure leaves with it, at zero
cost and with no width spent.** That is P-07's form and it is DISPLAY-BOX's, not
mine. **Under G-44 the burden is on the addition, and spacing is the addition here:
it is worth knowing which way P-07 falls before paying for it.**

**What I am doing about it now: nothing, deliberately, and the reason is in item 3.**
Spending face width against an unsettled entry count is the T-020 shape - an
allowance committed before the step that consumes it is known. **The gap is recorded
as the one gap on this face that is spaced deliberately rather than evenly, and the
number waits on F-030 and on P-07.**

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

**If a wire marker cannot hold the canonical form, that is a carrier defect to
report, never solved by inventing a short form at the wall.**

### 3.2 The marking source column

**F-051 is the entire reason.** Every file in this tree said VM; the part carries a
circled plus and a circled minus. **A marking quoted from a document is not a marking
read off a part.**

| Source | Means |
|---|---|
| `PART` | Read off the physical part |
| `FILE` | Quoted from a tree document. **Provisional until somebody looks** |
| `DESCRIBED` | Nothing is printed. `which` is a braced descriptor |

**G-44 test: what failure does it prevent, and what does it cost?** It prevents a
build sheet naming a terminal that is not on the part, which is T-013 and is the
failure that once told a builder to verify a short across a 5 V supply and tick the
box. One word per row to build, nothing to operate, nothing to repair. **It goes in.**

**Not one row below is marked PART. F-106: nobody in this project has ever been asked
to look at a terminal and report what is printed on it.**

### 3.3 The schedule

| TRM | Device, by name | Which | Source | Runs landed | Row | Blocked on |
|---|---|---|---|---|---|---|
| `TRM-MAIN-PANEL.KM-DRV.{pole 1, motor supply}` | **KM-DRV** | `{pole 1}` | DESCRIBED | RUN-001, RUN-002 | P-06 | **The marking has not been read, F-106.** **T-010 applies here: two jackets leave one terminal** |
| `TRM-MAIN-PANEL.KM-DRV.{pole 2, readback}` | **KM-DRV** | `{pole 2}` | DESCRIBED | RUN-006 | S-08 | Marking not read. Also open: whether KM-DRV's poles share one contact volume, which would put S-08 against G-30 with nowhere to move |
| `TRM-MAIN-PANEL.KM-DRV.{coil}` | **KM-DRV** | `{coil}` | DESCRIBED | RUN-005 | S-07 | S-07, which must state where the coil positive is taken from; marking not read |
| `TRM-MAIN-PANEL.K-FILL-S.{solenoid pole}` | **K-FILL-S**, order.md | `{solenoid pole}` | DESCRIBED | RUN-011 | P-02 | P-02; marking not read. **The pole is sized on the make-and-break event, not the holding figure** |
| `TRM-MAIN-PANEL.K-FILL-D-Q.{S-03 changeover pole}` | **K-FILL-D-Q**, order.md | `{changeover pole}` | DESCRIBED | RUN-007 | S-03 | Marking not read. **Both legs of one pole land here and G-27 requires both on RUN-007** |
| `TRM-MAIN-PANEL.K-DRY-Q.{S-20 changeover pole}` | **K-DRY-Q**, order.md | `{changeover pole}` | DESCRIBED | RUN-008 | S-20 | S-20; marking not read. **The relay is called K-DRY in the interface table and K-DRY-Q in order.md, so the id is unstable until one name wins** |
| `TRM-MAIN-PANEL.{ground bar}.{...}` | **{ground bar}**, not a bought part | OPEN | OPEN | RUN-017 | CBL-07 | CBL-07; the bar is not bought; RUN-017 is provisional |
| `TRM-FIELD.{fill solenoid}.{coil lead}` | The fill solenoid specified by D-136 | OPEN | **OPEN** | RUN-011 | P-02 | **Coil lead identification has never been looked up.** Per F-051 it is named by what is printed on the part, and nobody has looked |
| `TRM-PUMP-BOX-A.{driver}.{...}` | OPEN | OPEN | OPEN | RUN-001, RUN-003 | P-06, S-10, P-09 | S-10; P-06. **The pin list is known and the MARKINGS are not** - parts.md records that the flat pin list is a list of names that was read as an order, and the board is two connectors |
| `TRM-PUMP-BOX-B.{driver}.{...}` | OPEN | OPEN | OPEN | RUN-002, RUN-004 | P-06, S-10, P-09 | As PUMP-BOX-A |
| `TRM-DISPLAY-BOX.{logic board}.{...}` | OPEN. The board is hand built and does not exist | OPEN | OPEN | RUN-003 to RUN-009, RUN-016 | S-07, S-08, S-03, S-20, S-10, S-11, P-07 | S-12 is not frozen and the board does not exist |

**Eleven landing points. Six name their device. None is buildable, and every one of
the six is blocked on the same thing: nobody has looked at the part.** F-106.

### 3.4 The check this table holds that no other document can

**T-009 and T-010: a terminal carrying exactly one conductor is an open circuit, not
a spare, and clamps are counted against conductors rather than assumed.** The first
row shows two jackets leaving one terminal. Neither question is answerable from D5 or
from section 2, because both are organised by a conductor's journey and this table is
organised by its destination.

---

## 4. THE STANDPIPE ADJACENCY. F-113, ANSWERED AND ACTED ON

**The method is not reopened: D-121 answers a float that has moved, and nothing here
measures a level, so an unmarked float that slips is invisible. That is the worse
failure and the method stays.**

D-049 amended G-22 so the severed case is answered by the circuit and the short case
by **adjacency - the wiring plan.** That escape assumes a route with choices in it.
**D-121 fixes the adjacency at worst case by construction, so on RUN-012, RUN-013,
RUN-019 and part of RUN-020 there is no wiring plan left to answer with.** Grade:
**STRUCTURAL** while D-121 stands.

**The expensive failure is float-to-float, not the cross-class one.** Under D-154
every float is a series element in a coil chain, so a bridge between pairs on one
pipe **shorts out the elements between the bridge points and closes the chain around
an open float.** Severed is safe; this is not. **And it is already paid for**: D-130's
overflow, FL-11 and FL-12, was made a requirement for exactly that failure and lands
above the high-high per D-134, so the instrumented protection trips first.

| | Status |
|---|---|
| **Float cord insulation rated for the highest voltage in the bundle** | **TAKEN**, D-156, into WATER's float requirement. A purchasing attribute, free while the requirement is open |
| **Separate tie groups for float and pump cords on the standpipe** | **TAKEN**, D-156, into D-121's method. Costs nothing, and it makes a cord identifiable by its group |
| **Shields, conduits, barriers or dividers on the pipe** | **REJECTED under G-44.** Each costs money and build time, each obstructs the tie a person must reach under D-131, and **none touches the expensive failure, which is float-to-float and inside one class** |
| **Removing the pump cords from the pipe** | **LOGGED, NOT PURSUED.** D-121's sentence is the owner's. The observation stands: the pipe was adopted so a float that has moved is visible, and a pump gets no positioning benefit from it, since water.md holds the submersibles by cradle |

**Two residuals recorded rather than solved**, both logged in D-156: a tie is a
compression point and D-131 puts a person's hands on it with both pumps running under
D-143; and adjacency stops being a recorded fact, so a fault on the pipe cannot be
localised by knowing what lies next to what. **A repair cost paid every time.**

---

## 5. REQUIREMENTS AND SEARCH TERMS

No value is stated. Each is a lookup the owner runs under G-15. **The float cord's
insulation rating has left this list: it is in WATER's float requirement, D-156.**

| For | Requirement | Search term |
|---|---|---|
| RUN-011, RUN-015, RUN-018 to RUN-020 | A flexible LINE-class cable for a wall route in a room where water moves tank to tank, with an equipment grounding conductor | `flexible power cable 600 V oil resistant wet location`; `tray cable TC-ER exposed run wall` |
| RUN-015 | Confirmation that every conductor in one jacket may share the higher rating CBL-06 requires | `600 V insulated conductor mixed circuit same raceway control cable` |
| RUN-016 | The maximum probe cable length the EZO circuits tolerate. **Not from any file in this tree** | `Atlas Scientific EZO pH EC probe cable length limit extension` |
| Every gland entry | A cord grip per entry, sized to the cable chosen, sealed at least to the enclosure's rating and suitable for a bottom face | `liquid tight cord grip strain relief NPT cable range chart` |
| The display box bottom face | **How many entries the stated face can carry, which is D3's geometry and is not derivable from the entry order.** Section 2.3 | D3, not a lookup |
| The segregation rule | A stated rule for which classes may share a duct, a jacket, a clip run or a tie bundle, and what an unavoidable crossing requires | `control panel power and signal circuit segregation separation`; `Class 1 Class 2 circuits same raceway` |
| Labelling | A marker carrier that holds the canonical three-part TRM- form and, on a per-channel core, the channel token in addition without merging them | `wire marker sleeve character capacity heat shrink printable` |

---

## 6. WHY THERE IS NO DUPLICATION CONTRACT IN THIS DOCUMENT

**G-45. D5 and D6 are generated from one source, so they cannot disagree, and a
schedule is never hand-transcribed.** The rule that said they must agree was deleted
rather than restated: **a contract needs a reader who obeys it; a mechanism does
not.** The face cells are the newest instance: entry-faces.md states face and order
once, and this document carries the resulting cell without restating the reasoning.

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

**Deliverable as it stands:** every jacket and every landing point has a real id, an
owner, a duty, a voltage class, a segregation group, an entry face where one can
exist, and a named blocker. **Sixteen of twenty rows have no empty cell.** Nobody may
cut, order or land against it yet, and the reasons are in the Blocked on column.

**Four things would move the most, in order:**

1. **P-07's form**, DISPLAY-BOX's. It fills RUN-009's last cell and it may remove the
   LINE entry from the display box face entirely, which would settle section 2.3 at
   zero cost.
2. **F-030's per-signal returns.** RUN-003 and RUN-004 retire and are reissued under
   D-149, and only then is the display box face's remaining width knowable.
3. **The leak console's position**, which is four of the seven remaining empty cells
   and belongs to nobody on file.
4. **CBL-07's shape**, which decides whether RUN-017 is one id or several.

**Not returned, so no absence is read as an answer:** no wall layout, because M-02 is
open and Z5 is undefined; **no answer to channel-token.md's monotone CH1 to CH8
question, which is unanswered rather than no**, for the same reason; **no spacing on
the display box face, deliberately, per section 2.3**; and no gland count, position,
cable selection, core count, cut length or terminal number, all of which are
requirements in section 5.
