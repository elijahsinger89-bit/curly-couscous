# INTERCONNECT, first pass

First invocation, 2026-09-04, per D-140. This is a FIRST PASS on the shape of two
schedules and an inventory of the runs they will hold. It is not a schedule.

Read before writing: agents.md rules 1 to 11; subsystems/interconnect.md; the whole
of interface-table.md including every CBL- row; decisions.md's G-rule table, D-046,
D-047, D-090, D-092, D-108 to D-111, D-114 to D-140; parts.md in full;
wire-table-row-zero.md; channel-token.md; channel-register.md; findings.md rows
F-017, F-022 to F-025, F-028 to F-036, F-047, F-051, F-058, F-060, F-067, F-088 to
F-097; traps.md T-006 to T-013, T-015, T-016, T-020, T-021, T-028; order.md;
commissioning.md rows C-08, C-09, C-12, C-21; subsystems/main-panel.md,
pump-boxes.md, display-box.md, water.md; audit/2026-09-04-standpipe-extraction.md;
audit/2026-09-03-1st-edition-floats-and-wall.md sections B.5 and 2.3.

**Nothing below states a part number, a gauge, a core count, a length, a terminal
number or a colour.** Where a value is needed the requirement and a search term are
given and the pass stops there, per rule 3 and G-15.

**Every impossibility claim below is graded, per rule 10 and G-36.**

---

## 0. THE ONE THING TO READ IF YOU READ NOTHING ELSE

**A float's cord is not a cable INTERCONNECT cuts. It is a part property, and its
required length is set by a wall layout that does not exist yet.** Section 4,
constraint K-01. It is the constraint nobody has written down and it lands on a
purchase that is being specified right now.

---

## 1. THE SHAPE OF THE CABLE SCHEDULE

One row per CABLE. Derived from the crossings that actually exist in
interface-table.md, not from a template. Every column names the frozen row or rule
that requires it, because a column nobody can name a reason for is a column that
gets filled in with a guess - wire-table-row-zero.md's own standard, adopted here.

**This schedule is the third of three artifacts and it must not duplicate the other
two.** See section 2.5.

| # | Column | What it is for, and which row or rule requires it | Who owns the value |
|---|---|---|---|
| 1 | **Cable ID** | The one identity of a jacket. **It is NOT a CBL- number** - see defect BD-02. Own namespace, no bare digit, per channel-token.md forbidden item 5 | BOSS assigns the prefix, INTERCONNECT assigns within it |
| 2 | **End A: enclosure or field device** | Named exactly as the tree names it, never invented. Required because F-05, F-06, S-01, S-02 and S-04 are all rows that existed with an end nobody owned | The subsystem owning that end |
| 3 | **End A: entry** | Which FACE, and which gland or grip. CBL-01 to CBL-04 are open on precisely this and nothing else in the tree carries it. **The drip-loop rule makes this a face decision, not a position decision** - constraint K-03 | The enclosure owner, through CBL-01 to CBL-04 |
| 4 | **End B: enclosure or field device** | As column 2 | The subsystem owning that end |
| 5 | **End B: entry** | As column 3 | As column 3 |
| 6 | **Interface rows realised** | A SET, not one row. **This is where the cable schedule differs from the wire table**: wire-table column 10 carries one row per conductor, but a single jacket can realise several crossings - the display box to pump box run carries S-10 and P-09 together. **A cable realising no interface row does not exist; a cable realising rows of two different classes is a flag, not a row** | BOSS |
| 7 | **Class or classes carried** | 120 VAC / 24 V control / SELV signal / EGC, the same four as wire-table column 8. **Derived from the interface rows, never chosen.** It drives segregation and insulation rating. CBL-06 is the precedent already frozen: where a 120 V chain leg shares a jacket, every conductor in that jacket takes the higher insulation rating | Derived from column 6 |
| 8 | **Cut, supplied, or cord** | **This column does not exist anywhere in the tree and three frozen decisions create it.** D-046 makes P-03, P-04 and P-05 into cords that plug in from outside, so those crossings have no cable to cut. D-131 makes every float cord a supplied part that must never be cut. S-11's probe cables arrive with the probes. **The D-090 cut rule silently assumes every run is a cut cable and a third of them are not** | The device owner |
| 9 | **Wall run and route** | The measured wall run and which route or duct the cable takes. **The wall run is recorded here. THE CUT LENGTH IS NOT** - see column 10 | INTERCONNECT, after the wall layout exists |
| 10 | **Cut length** | **Deliberately ABSENT as a stored value, per T-020.** D-090's allowance is folded into the cut STEP of the build procedure and computed there. A stored cut length is a second table of lengths that can disagree with the first, **and parts.md already has two such tables that do disagree** - defect BD-04 | Nobody. It is computed at the cut step |
| 11 | **Core requirement** | **Derived by counting the wire-table conductors assigned to this Cable ID, never asserted.** T-008: count landings, never the jacket. T-012: derive it, or make the check an identity rather than a bound. **The value is OPEN until the wire table exists and no agent may state a number here** | Derived from the wire table |
| 12 | **Segregation group** | Which cables may share a duct, a clip or a bundle, and which may not. **Load-bearing rather than tidy**: D-049 amended G-22 so the SEVERED case is answered by the circuit and the SHORT case is answered by the wiring plan, and F-028's resolution says in terms that this makes INTERCONNECT's cable schedule load-bearing on G-22. F-029 and F-030 are the two named constraints that land here | INTERCONNECT, derived from column 7 and from F-029, F-030, F-033 |
| 13 | **Label at both ends** | The conductor-labelling scheme applied at BOTH ends. A conductor labelled at one end only is worse than one labelled at neither, because it looks done. **Where the cable carries a per-channel signal the CHANNEL TOKEN appears IN ADDITION and the two are never merged or abbreviated** - channel-token.md's INTERCONNECT row | INTERCONNECT applies; CONTROL-SOFTWARE declares the token, S-19 and D-021 |
| 14 | **Status** | BUILDABLE, or BLOCKED ON (named row). Rule 9 | BOSS |

**Columns deliberately NOT present**, for the same reason wire-table-row-zero.md
excludes them: gauge, colour, part number, and per-channel core identity. The first
three are outputs of a lookup the owner runs. The fourth belongs to
channel-register.md and section 2.5 explains why restating it here is forbidden.

---

## 2. THE SHAPE OF THE TERMINAL SCHEDULE

One row per TERMINAL, meaning one landing point on a real part. **Not one row per
conductor** - that is the wire table, and the difference is the whole reason both
exist. F-097 routed the terminal namespace to INTERCONNECT explicitly, "while it is
deciding the schedule's shape, which is now". Section 2.4 is that proposal.

### 2.1 The columns

| # | Column | What it is for, and which row or rule requires it | Who owns the value |
|---|---|---|---|
| 1 | **Terminal ID** | The identity wire-table columns 4 and 6 point at. **Those two columns currently have nowhere to point** - wire-table-row-zero.md defect 2, and CDR-001 has OPEN in both | BOSS assigns the prefix, the enclosure owner assigns within it |
| 2 | **Enclosure or field device** | Which of the four boxes, or which field device. **A terminal has no identity outside the thing it is on** | The enclosure owner |
| 3 | **Device or block, BY NAME** | G-28: which relay goes in which socket is a build fact, labelled BY NAME and never by position. The terminal schedule is where that rule is enforced or lost | The enclosure owner |
| 4 | **Marking, as printed on the part** | **Never a name that is not printed.** F-051 is the frozen case: the terminal block silk carries a circled plus and a circled minus, not the words and not VM, so that terminal is named by position and by what it does. **A build sheet cannot quote a symbol, and naming by list index is T-013** | The enclosure owner, from the part in hand |
| 5 | **Conductors landed** | By Conductor ID, from the wire table. **T-009: a terminal carrying exactly one conductor is an open circuit, not a spare. T-010: count clamps against conductors** - two bus terminals landed twelve conductors on eight clamps for months | Derived from the wire table |
| 6 | **Clamp face** | Internal wire on one face, field cable from the gland on the other, and every wire descriptor names which. **Observed in the 1st Edition set at B-23, unverified, confirm or replace** - it is a labelling convention and carries no figure, which is the class D-121 was adopted under | INTERCONNECT proposes, enclosure owner confirms |
| 7 | **Class at this terminal** | Must agree with the class of every cable landing on it. **A terminal where two classes meet is a flag, and G-30's reasoning is why**: duty is separated by the device, not by the material | Derived, must agree with cable schedule column 7 |
| 8 | **Interface row** | The crossing this landing realises. A landing that realises none does not exist | BOSS |
| 9 | **Status** | BUILDABLE, or BLOCKED ON (named row) | BOSS |

**No terminal number appears in this pass.** MAIN-PANEL's own file says terminal
numbers are assigned late, not now, and rule 3 forbids me stating one regardless.

### 2.2 What the terminal schedule is FOR, that the other two cannot do

It is the only artifact that can answer "how many conductors land on this clamp",
which is the T-010 failure, and "does this terminal exist on the part", which is the
F-051 and T-013 failure. **Neither question is answerable from a cable schedule or
from a wire table, because both of those are organised by the conductor's journey
and this one is organised by its destination.**

### 2.3 The relationship between the three artifacts, stated as identities

There are THREE, not two, and the wire table already exists in schema form:

| Artifact | Row unit | Exists? |
|---|---|---|
| Cable schedule | one jacket | This pass proposes the shape |
| Wire table | one conductor | Schema frozen in wire-table-row-zero.md, twelve columns, one row filled |
| Terminal schedule | one landing point | This pass proposes the shape, and its namespace |

**The joins must be IDENTITIES, not lookups, per T-012** - a bound passes while the
data drifts, an identity fails the moment two sides disagree:

- Every wire-table row's **Cable** value exists in the cable schedule. Exactly.
- Every wire-table row's **From: terminal** and **To: terminal** exist in the
  terminal schedule. Exactly.
- Every terminal-schedule row's **Conductors landed** exist in the wire table.
  Exactly, and the count is the clamp count check.
- Every cable-schedule row's **Interface rows realised** is the union of the
  interface rows of its conductors. **Computed, never typed.**

### 2.4 WHAT IS DUPLICATED, AND WHAT MUST NEVER BE

**Duplicated on purpose, because it is the join and it must be checkable:** the
Cable ID, the Terminal ID, the device names at both ends, and the interface row
references. These appear in more than one artifact by design and every one of them
is an equality that a check can fail.

**MUST NEVER be duplicated, and each has a named reason:**

| What | Where it lives, once | Why duplicating it is the defect |
|---|---|---|
| **Length and cut length** | Nowhere as a stored value. Computed at the cut step from D-090 | **T-020. A cut cable cannot be un-cut, and parts.md already carries two tables of the same five figures under two different allowance rules** - BD-04 |
| **Gauge, core count, colour, part number** | The owner's lookup, and the cable schedule's core requirement is DERIVED | wire-table-row-zero.md's own exclusion: they are outputs of a rule and a lookup, and putting them in a table is what makes a wire table disagree with a cable schedule |
| **The per-channel core identity** | **channel-register.md, once, under D-057** - it has a Cable core column and that column is empty and waiting for INTERCONNECT | channel-token.md forbidden item 1: any translation table, in any medium. **"CH3's core is Y" is the correct shape. "core 7 = CH3" is forbidden**, because its existence proves the core has an identity of its own. A subsystem file may reference the register and may not restate it |
| **Fail behaviour on a severed conductor** | Wire table column 11, per conductor, established by the subsystem that established it | **F-017 and G-22's amendment. It is a per-conductor property and restating it per-cable is exactly how an inherited fail direction happens** - BOSS asserted S-03's from S-08 once already |
| **Design current and which event** | Wire table column 9, per conductor | D-136: the number that sizes a contact is the make and break event, not the holding figure. **A cable-level current is a summed abstraction that has no event attached to it** |
| **What a signal MEANS** | The interface row | INTERCONNECT's own out-of-scope line. Applying an identity is not interpreting a meaning; restating a meaning is |

### 2.5 THE TERMINAL NAMESPACE, proposed as a shape and not as values

F-097 routes this to INTERCONNECT. **The proposal is a shape. BOSS assigns the
prefix, because F-097 also records that the F- collision is BOSS's and is not fixed
unilaterally mid-pass.**

**Requirement on the shape, in order of what it must survive:**

1. **A terminal is identified by the thing it is on, then by what is printed on it.**
   Enclosure or device, then block BY NAME per G-28, then the marking as printed per
   F-051. Where nothing is printed, position plus function, and the schedule says
   which of the two it is using.
2. **No bare digit anywhere in the identity.** channel-token.md forbidden item 5: no
   bare digit that could be a channel, a core or a terminal. A terminal ID that
   reads as an integer will eventually be read as a channel.
3. **No box-local, cable-local or connector-local numbering** - forbidden item 7. A
   terminal's identity is not "terminal 3 of the field block".
4. **The prefix must not collide with anything already in the tree.** Prefixes I
   read and found in use: D- decisions, G- rules, T- traps, F- BOTH fluid interface
   rows and findings, S- signal rows, P- power rows, M- BOTH mechanical interface
   rows and the standpipe extraction's method rules, C- BOTH commissioning rows and
   two different audit files' correction and contradiction lists, B- the wall
   audit's proposals, E- the standpipe audit's electrical observations, CBL- cable
   and enclosure crossings, CDR- conductors, W- the C-12 witness, K- relay
   envelopes, PL- pilot lamps, LS- float positions, SUP- suppression, V3 the scope
   boundary valve, Z5 the operator standing position. **CDR- was chosen for
   conductors precisely to avoid guessing into this. The terminal prefix needs the
   same care and I am not assigning it.**
5. **It must be stable under a relay being moved between sockets**, because G-28
   says relays are not interchangeable once bought and are labelled by name. A
   terminal named through a socket position is not stable; one named through the
   relay's name is.

**And a namespace finding that strengthens F-097, found by reading rather than
assumed - defect BD-03 in section 6.**

---

## 3. THE CABLE INVENTORY, AT ROW LEVEL

**Derived only from rows that exist in interface-table.md.** No run below is
invented and no run is stated with a length, a gauge, a core count or a part number.
Endpoints are named as the interface table names them.

**Twenty rows: seventeen cable runs and three cord routes.** The three cord routes
are listed because D-046 removed their cable while leaving a physical route across
the wall that INTERCONNECT arbitrates, and no artifact in the tree owns a cord route.

### 3.1 Inter-enclosure cable runs

| # | End A | End B | Carries | Interface row | Status |
|---|---|---|---|---|---|
| R-01 | MAIN-PANEL: permissive contactor load side | PUMP-BOXES: stepper driver VM distribution, box A | The conductor the permissive removes | P-06 | **BLOCKED on P-06 OPEN.** Both ends must agree voltage, conductor and gland before either box is built, and PUMP-BOXES must return the driver supply range from the datasheet first. Also blocked on CBL-01 and CBL-02 |
| R-02 | MAIN-PANEL: permissive contactor load side | PUMP-BOXES: stepper driver VM distribution, box B | As R-01 | P-06 | **BLOCKED, as R-01.** Note parts.md: one pole for VM distribution, not two, both box feeds off one terminal downstream of it - so this is two cables from one terminal, not two poles |
| R-03 | DISPLAY-BOX: logic board step and direction outputs | PUMP-BOXES: the driver STEP and DIR screw terminals, box A | Per-channel step and direction, and the logic supply | S-10, and P-09 if they share a jacket | **BLOCKED on S-10 OPEN.** P-09's source is closed by D-031. **Whether S-10 and P-09 share a jacket is a cable-schedule decision I own and cannot take** - see constraint K-06 |
| R-04 | DISPLAY-BOX: logic board step and direction outputs | PUMP-BOXES: the driver STEP and DIR screw terminals, box B | As R-03 | S-10, and P-09 if they share a jacket | **BLOCKED, as R-03.** Additionally blocked on PUMP-BOXES' open item: how the two boxes divide the eight channels, and whether both boxes take one cable each or share one, which it is told to coordinate with INTERCONNECT and not decide alone |
| R-05 | DISPLAY-BOX: logic board permissive coil drive | MAIN-PANEL: the driver permissive contactor coil | The one coil the Pi drives | S-07, and S-09 | **BLOCKED on S-07 OPEN, and on an unresolved namespace: S-09's own status says it should close as "no relay drive outputs" or MERGE INTO S-07, which is the same conductor, and the resolution cell says BOSS to merge or close. I cannot write one cable row for a conductor that has two interface rows** |
| R-06 | MAIN-PANEL: pole 2 of the 22.32, the readback | DISPLAY-BOX: optocoupler input | Permissive readback, sense inverted | S-08 | **BLOCKED, but the least blocked run in the build.** The circuit is closed and recorded as given in parts.md, with the burden in the main panel. Blocked on CBL-01 and CBL-03 for gland position, on DISPLAY-BOX's input side which S-08 says is still open, and on the terminal namespace |
| R-07 | MAIN-PANEL: the normally closed contact of a 55.34 | DISPLAY-BOX: isolated Pi input | Day tank fill in progress, sense inverted | S-03 | **BLOCKED, as R-06.** Circuit closed by D-042 and its numbers are different from S-08's and must not be copied from it |
| R-08 | MAIN-PANEL: second pole of K-DRY | DISPLAY-BOX: isolated Pi input | Dry-run relay state, for the software verification judgement | S-20 | **BLOCKED on S-20 OPEN AND NEW.** Its fail direction must be established rather than inherited, per F-017 |
| R-09 | MAIN-PANEL: fused, NOT relay switched receptacle | DISPLAY-BOX: Pi power | The Pi's independent supply | P-07 | **BLOCKED on a contradiction, defect BD-05.** P-07 is marked CLOSED in the interface table, and display-box.md still carries "Power into this box, P-07, and whether the Pi is fed from the NDR-240-24 or separately" as an OPEN item. **The principle is closed; the conductor is not** |

### 3.2 Field cable runs

| # | End A | End B | Carries | Interface row | Status |
|---|---|---|---|---|---|
| R-10 | Building branch circuit | MAIN-PANEL: line input | Supply | P-01 | **BLOCKED on P-01 OPEN.** And see defect BD-06: P-01 names one branch circuit while D-137 requires a dedicated circuit for the chiller and loop pump. Whether that is a second feed into the panel is unstated and it changes this row's count |
| R-11 | MAIN-PANEL: fill solenoid relay output | WATER: fill solenoid coil | Switched 120 VAC to the coil | **P-02** | **BLOCKED on P-02 OPEN** - and P-02 EXISTS, which contradicts F-096 and wire-table-row-zero.md. See defect BD-01, which is the most important thing in section 6. The device itself is fully specified by D-136 and the run is still blocked, because P-02's own text is stale rather than absent |
| R-12 | WATER: day tank floats, on the day tank standpipe | MAIN-PANEL: transfer relay seal-in chain | Pilot-duty dry contacts at the control voltage | S-02 | **BLOCKED on S-02 OPEN.** The mounting method is adopted, D-121 and D-131; which floats, their type and their positions are not, D-118. **And see constraint K-01: this run may not be a cut cable at all** |
| R-13 | WATER: storage tank floats, on the storage standpipe | MAIN-PANEL: fill relay seal-in chain | As R-12 | S-01 | **BLOCKED, as R-12** |
| R-14 | WATER: leak detection sensor placement | MAIN-PANEL: leak console | Sensor to console | S-04 | **BLOCKED on S-04 OPEN, and on defect BD-07: nothing states where the console physically sits**, so the run has one end with no position |
| R-15 | MAIN-PANEL: leak console, 24 V in and Form C out | MAIN-PANEL: permissive chain | Console supply and its contact legs, in one jacket | **CBL-06** | **BLOCKED on CBL-06 OPEN and on BD-07.** The one class rule already frozen in the tree: the console is POWERED, its contact legs sit in the 120 V chain, so every conductor in this cable takes the higher insulation rating including the supply pair sharing the jacket |
| R-16 | DOSING: pH, EC and PT-1000 probes in the manifold probe section | DISPLAY-BOX: the EZO circuits and their carriers | Probe signals | S-11 | **BLOCKED on S-11 OPEN, and on a three-way circular wait** - blocker B-03 in section 5. Also: the probe cables arrive with the probes, so cable-schedule column 8 reads "supplied", not "cut" |
| R-17 | MAIN-PANEL: ground bar | Each of the other three enclosures, and each 120 V field device | Equipment grounding | **CBL-07** | **BLOCKED on CBL-07 OPEN.** The display box is polycarbonate and the pump boxes are plastic, so there is no bonding path through any of them and every equipment ground lands on the bar. **Whether the EGC is a conductor inside each run or a separate cable is a cable-schedule decision I own and cannot take until CBL-01 to CBL-04 return** |

### 3.3 Cord routes, which have no cable and still have a route

**D-046 closed the mounting: receptacles are panel mounted in the enclosure face and
cords plug in from outside, not fed through grips. So these crossings have no cable
for me to cut and they do have a physical route across the wall that only
INTERCONNECT arbitrates.** No artifact in the tree owns a cord route - defect BD-08.

| # | End A | End B | Carries | Interface row | Status |
|---|---|---|---|---|---|
| R-18 | MAIN-PANEL: relay-switched receptacle, panel mounted | WATER: transfer pump cord, plugged in from outside | 120 VAC | P-03 | **BLOCKED.** Mounting closed by D-046; circuit and rating still open. Route blocked on the wall layout |
| R-19 | MAIN-PANEL: relay-switched receptacle, panel mounted | WATER: circulation submersible cord | 120 VAC | P-04 | **BLOCKED, as R-18.** **This cord runs on the day tank standpipe** under D-121 - see constraint K-02 |
| R-20 | MAIN-PANEL: switched receptacle on a dedicated circuit | WATER: chiller cord AND chiller loop pump cord, switched together | 120 VAC, two cord caps | P-05, as amended by D-137 | **BLOCKED on P-05 OPEN.** G-12 was right that a loop pump exists and wrong about what switches it: not a contactor, one switched receptacle. **Two cord caps at one receptacle is a MAIN-PANEL question that constrains where I route two cords to one point.** The loop pump is a submersible in the day tank, so **its cord is also on the standpipe** - constraint K-02 |

### 3.4 Rows that imply NO cable, checked and named rather than assumed

- **S-06**, E-stop and manual reset: closed by D-048, both devices are on the panel's
  top face per parts.md, and the row says in terms that INTERCONNECT does not place
  them on the wall. **No run.**
- **S-12**, the Pi GPIO and I2C map: a map, not a crossing of the wall. **No run.**
- **S-13**, the flow cell: closed as a signal. It is a fitting, not an instrument -
  no output, no contact, no wire. **No run.**
- **S-14, S-15, S-16, S-17, S-19**: software and attribution rows. **No run.**
- **S-18**: reopened, and D-108 removed the chiller contactor entirely, so there is
  no contact to read and no conductor. **No run.**
- **P-08**: internal to MAIN-PANEL. **No run.**
- **F-01 to F-10**: fluid. **No run** - with the exception recorded at BD-01.
- **CBL-05**: a lid penetration for a head and the tubing through it. Not a cable.
- **M-01, M-02, M-03**: placement. M-02 is mine to arbitrate and is not a cable.

### 3.5 The count

**Twenty rows. Zero buildable now. Twenty blocked.**

That is not pessimism, it is rule 9 applied honestly: **CBL-01, CBL-02, CBL-03 and
CBL-04 are all OPEN, and every one of the seventeen cable runs terminates at a gland
those four rows govern.** Even a run whose electrical definition is fully closed
cannot be built, because nothing states which face it enters or which grip it uses.

**Two runs are blocked on less than the others and are the right place to start when
the four CBL- rows return: R-06 and R-07.** Both circuits are closed and recorded as
given in parts.md, both have their fail direction chosen rather than inherited, and
what remains on each is a gland position, DISPLAY-BOX's input side, and the terminal
namespace.

---

## 4. CONSTRAINTS FOUND, REPORTED AND NOT FIXED

Each is graded per rule 10 and G-36. **A CURRENT claim names what would change it.**

### K-01. THE FLOAT CORD IS A PART PROPERTY, NOT A CUT LENGTH, AND ITS REQUIRED LENGTH IS SET BY A WALL LAYOUT THAT DOES NOT EXIST

**This is the constraint nobody has written down.**

D-131 confirms the method in the owner's order, and two of its clauses collide with
the cut rule: **"a cable tie clamps each float's external weight on its mark and THE
TIE IS THE TRIP HEIGHT"**, and **"fill slowly, confirm each float trips at its mark,
ADJUST THE TIE AND NEVER THE WIRING."**

So the float's own cord is the strain member, the trip-height datum, and the signal
path at once. **It cannot be cut to fit, cannot be shortened at the tank, and must
carry slack above the weight so the tie can be moved at commissioning.** Its total
required length spans: the trip mark on the standpipe, up the pipe with ties at
intervals, over the rim, the wall route, the panel gland, a drip loop outside the
box, and service at the landing.

**Every term after "over the rim" is INTERCONNECT's wall layout, which does not
exist. So the float cord length is a purchasing requirement on a part, set by a
layout owned by an agent who is not in the float pass.**

I read the requirement the float pass is being restarted against - D-118's restart
from requirements, F-089's control-voltage contact power under G-31, D-127's eight
positions, D-131's chosen differential, and D-132's candidate family recorded as one
entry with no priority. **Cord length is not among them.** D-132 records a candidate
described as having "a long cord" and long is not a requirement.

**Grade: CURRENT.** What would change it: the wall layout returning with the panel's
position relative to each tank, at which point the cord length becomes a stated
requirement rather than an unknown. **And it is the SELF-FULFILLING kind under
D-103's amendment to G-36**: if nobody states it, floats get bought against
positions and contact duty alone, a short cord arrives, and the only remedies are a
splice in the wet zone or a junction box neither of which any row owns - or moving
the panel, after it is mounted.

**REQUIREMENT to return:** each float's supplied cord must reach from its trip mark
on the standpipe to its landing in the main panel, uncut and unspliced, with tie
slack for commissioning adjustment and a drip loop outside the entry.
**SEARCH TERM:** "float switch cord length options SPDT pilot duty control voltage".
**I state no length.**

### K-02. THE STANDPIPE MANDATES A MIXED-CLASS BUNDLE, IN THE WATER, AND THE TREE HAS NO RULE FOR IT

D-121 adopts, in the owner's words and as the whole scope of the adoption: **one
rigid pipe per tank carrying every float AND EVERY CORD.** D-131 adds that cords run
up the pipe, tied at intervals, and leave through a grip with a drip loop outside
the box.

D-137 then put a second submersible in the day tank. water.md records the count -
"two cords, not one, on the standpipe's cord run" - **and nobody has recorded the
CLASS consequence.** On the day tank standpipe, the SELV float cords and **two
continuously-running 120 VAC pump cords** are tied into one bundle, along the full
length of a pipe standing in the solution, and they leave through the same cord
entry.

**INTERCONNECT's own file carries "separation of the 120 V pump and chiller runs
from step and direction and from probe cables" as an OPEN item, and the tree has no
rule yet** - the wall audit's B-20 says the same at the point where it records the
old set's prohibition as observed and unverified. **So the one place in the build
where mixed classes are already mandated to touch is the one place no separation
rule reaches.**

The tree has ruled on this shape exactly once, at CBL-06, and the ruling does not
reach here: **CBL-06 requires the higher insulation rating for every conductor
sharing a JACKET with a 120 V chain leg. The standpipe cords share a TIE BUNDLE, not
a jacket, and no row covers that case.**

**Grade: STRUCTURAL as to the adjacency** - D-121 is adopted and its whole content is
that one pipe carries every float and every cord, so no addition removes the
adjacency without unmaking the mounting method. **CURRENT as to the consequence**:
what would change it is a separation rule that says what a mixed bundle requires,
which is mine to propose and which I will not propose without the classes settled by
S-01, S-02, P-04 and P-05.

**Reported, not fixed.** It is also a commissioning observable rather than only a
wiring rule if B-21 is confirmed - a reading that jumps when a pump starts - and the
tree currently has no named symptom for it.

### K-03. THE DRIP-LOOP REQUIREMENT IS A GLAND-FACE DECISION AT EVERY ENCLOSURE, NOT ONLY AT THE STANDPIPE

D-131 puts a drip loop outside the box at the tank cord entry. D-090's cut rule
already spends an allowance on a drip loop **per grip**, which means the rule assumes
a drip loop at every grip in the build and not only at the tank. D-092 and D-110
keep design-to-shed as the principle.

**The implication nobody has written: a drip loop only sheds if the entry is at or
below the cable's lowest approach. So the drip-loop requirement DECIDES THE GLAND
FACE, and it decides it at all four enclosures.**

parts.md settles this for one box only: every cord grip on the main panel is on the
BOTTOM face and nothing but the five 22 mm devices penetrates the top. **CBL-02 and
CBL-03 have no face decision at all**, and the pump box lids are already penetrated
for the heads under CBL-05, so a lid that is also a cable face is a second question
on the same surface.

**Grade: STRUCTURAL.** A drip loop on an upward-facing entry is not a drip loop, and
no addition changes that. What is open is which face each enclosure offers, and that
is CBL-02 and CBL-03.

### K-04. THE IP65 TOP FACE IS A ROUTING PROHIBITION, AND IT IS THE NEGATIVE KIND

D-110 closed the box at IP65 and kept design-to-shed for the top face; F-088 keeps
the top-face half open under G-35, and what is still owed is each 22 mm device's
rating IN THE UPWARD-FACING ORIENTATION.

**Nothing of mine enters that face** - parts.md says nothing else penetrates it. So
my constraint is entirely negative and it has not been written down:

- **No cable of mine may be routed above, over, or across the main panel's top
  face**, because anything routed above it drips onto five upward-facing gasketed
  devices whose orientation rating is still owed, and D-092's reasoning is that the
  assembly's rating is set by its worst penetration regardless of the box.
- **A common horizontal run, if one is adopted, sits below that face**, not above it.
- **G-13 makes the same volume a safety matter for a second reason**: the E-stop and
  the manual reset are on that face and an operator must reach them. A tray, a clip
  run or a cable loop above the panel fouls the reach as well as the shedding.

**Grade: STRUCTURAL** for the reach half, since G-13 is frozen. **CURRENT** for the
shedding half: what would change it is F-088 returning device ratings in that
orientation, or a drip shield, which D-092 already anticipates.

### K-05. F-029'S REQUIREMENT MEANS THE MAIN PANEL TO DISPLAY BOX ROUTE IS NOT ONE CABLE, AND THE FIVE MEASURED RUNS ARE FIVE ROUTES

F-029 states the requirement and calls it the one conductor pair in this build whose
independence is the deliverable: **the permissive coil drive and its own readback
shall not share a pair, shall not be adjacent in a bundle, preferably not share a
jacket**, because a short between them makes the readback follow the command, which
is precisely and only the failure G-09 exists to detect, and it removes weld
detection too. And it records that class separation cannot catch it, because command
and readback are the same class as each other.

**Five interface crossings ride the main panel to display box route: S-07 with S-09
pending merge, S-08, S-03, S-20 and P-07.** They span at least three classes, and
F-029 forbids two of them from being adjacent.

**So the measured run named "panel to display box" is one ROUTE carrying several
cables, and the same is true of every other row in that table.** The cut rule
applies per cable. **The number of cables in this build is therefore not five and
cannot be derived from that table.**

**Grade: CURRENT.** What would change it: a construction that guarantees
non-adjacency inside one jacket, which F-029 permits only as a second preference,
and which I will not choose without the wire table.

**This is a purchasing hazard of exactly the class G-41 was just frozen for**: a
table that can be read either way will be read as absolute by whoever is holding a
credit card. See also defect BD-04.

### K-06. THE DUTY BOUNDARY G-30 WOULD OBJECT TO, ASKED HONESTLY

G-30 is a rule about RELAYS - a power pole and a sense pole never share a relay,
because all four poles share one volume and a break throws vapour onto the quiet
pole. **I do not extend a frozen rule to cables by analogy.** What I did is ask
G-30's REASONING of every run and report where a power duty and a sense duty share
one enclosure of my own making, which is a jacket or a bundle.

**Three places, and only three:**

1. **CBL-06**, already ruled and correctly: the console supply pair and the Form C
   legs in one jacket, all conductors at the higher insulation rating. **The tree got
   this one right and it is the precedent for the other two.**
2. **The day tank standpipe bundle**, K-02. Unruled.
3. **The pump box runs, and this one is currently SAFE and could stop being so.**
   Today the motor supply arrives on R-01 or R-02 from the main panel and the step,
   direction and logic supply arrive on R-03 or R-04 from the display box - two
   cables, two glands, duty separated at the gland. **PUMP-BOXES has an open item
   asking whether both boxes take one cable each or share one, and it is told to
   coordinate with INTERCONNECT rather than decide alone.** Combining the motor
   supply with step and direction into one jacket to one box is where the G-30-shaped
   mistake would be made, and F-047 already establishes that the coupled-noise premise
   is truest inside the box, with four motor phase conductors chopping current in the
   same small sealed volume as every logic jumper.

**Grade for item 3: CURRENT, and recoverable.** What would change it is the cable
schedule fixing two cables per box before anyone buys one, which costs nothing now.

### K-07. SEGREGATION BETWEEN THE 120 VAC SOLENOID RUN AND THE SELV SIGNAL RUNS

R-11 carries switched 120 VAC to a coil whose contact-sizing event is the **make and
break inrush and not the holding figure**, per D-136 and wire-table column 9. R-12
and R-13 carry SELV pilot-duty dry contacts. **All three run from the main panel to a
tank, so they share a wall, probably a route, and possibly a clip run.**

Why this is load-bearing rather than tidy: **D-049 amended G-22 so that the severed
case is answered by the circuit and the SHORT case is answered by the wiring plan.**
F-028's resolution says so in terms - it makes MAIN-PANEL's duct plan and
INTERCONNECT's cable schedule load-bearing on G-22. **The realistic short is the
adjacent conductor in a duct or a jacket, not ground in the abstract.**

And the direction it fails matters: **F-093 is live on the same conductors.** The
dry-run element is now a float, D-119, and the old set draws both low-level stops
normally open, on which a severed conductor reads as "level is fine", the unsafe
direction. **BOSS states no fail direction and inherits none and neither do I.** What
I record is that the adjacency question and the fail-direction question land on the
same cable and are owned by different agents.

**REQUIREMENT to return:** a stated separation rule giving which classes may share a
duct, a jacket, a clip run or a tie bundle; what an unavoidable crossing requires;
and what the standpipe bundle of K-02 requires, since it is the one case already
mandated. **SEARCH TERM:** "control panel power and signal circuit segregation
separation barrier Class 1 Class 2 wiring". **I state no separation distance.**

### K-08. THE CHANNEL TOKEN AT THE CORE, AND THE QUESTION channel-token.md PUTS TO ME

channel-token.md hands me the eight tokens as the conductor identity at both ends of
every core carrying a per-channel signal, and forbids a per-cable restart if the
eight are split across more than one cable, a renumbering to match a connector's pin
order or a core's position in a bundle, and a token for a spare core.

**The per-cable restart prohibition is live and not hypothetical**, because R-03 and
R-04 split the eight channels across two cables to two boxes, and PUMP-BOXES has not
yet returned which tokens go in which box. **The tokens do not restart at CH1 in box
B.**

The question routed to me and to nobody else: **whether a monotone ascending run of
CH1 to CH8, read from the operator's standing position, is achievable across the
wall I arbitrate.**

**I cannot answer it, and the reason is nameable rather than vague: Z5, the operator
standing position, is undefined.** F-067 records that it is DOSING's coinage and
DOSING's to define, that it is load-bearing in three places, that it was flagged by
AUDIT on 2026-08-30 and has not closed, and that where it physically is depends on
the wall layout INTERCONNECT arbitrates. **The wall layout does not exist and M-02 is
open.** Per channel-token.md this answer blocks nothing unless it is no, and I am not
returning a no I have not established.

---

## 5. WHAT BLOCKS ME, PRECISELY

### B-01. CBL-01, CBL-02, CBL-03 and CBL-04 are all OPEN, and they block everything

Every one of the seventeen cable runs terminates at a gland those four rows govern.
Rule 9 is unambiguous. **This is the whole blocker and the other entries are refinements of it.**

### B-02. And those four rows are DEADLOCKED, both sides waiting on the other

Read and named rather than assumed:

| File | Its "Waiting on" says |
|---|---|
| subsystems/interconnect.md | All four enclosure owners: gland positions and entry sides, CBL-01 to CBL-04 |
| subsystems/main-panel.md | INTERCONNECT: gland positions and cable entry side |
| subsystems/pump-boxes.md | INTERCONNECT: cable entry side and gland positions |
| subsystems/water.md | INTERCONNECT: how field cables leave the wet area |

**Four files, one fact, every arrow pointing at somebody else.** This is why CBL-01
to CBL-04 have been open since the table was written and why no amount of further
analysis moves them.

**What breaks it, and it is cheap:** the dependency is not actually circular. **The
enclosure owner owns which FACES its box can offer and what is behind each one.
INTERCONNECT owns which face each cable arrives at.** If each enclosure owner returns
the faces available and what is inside them, I can arbitrate. **I am not making that
change myself: it costs nothing but it is an allocation of a boundary and rule 5 says
stop and ask when it is a choice rather than a defect.**

### B-03. The probe run is a three-way circular wait

- subsystems/interconnect.md: get the EZO length limit from DISPLAY-BOX, do not
  assume one.
- subsystems/display-box.md "Waiting on": DOSING, probe cable length and routing,
  S-11.
- interface-table.md S-11: DOSING owns the wet fitting and probe placement,
  DISPLAY-BOX owns the carriers and the I2C side, **INTERCONNECT owns the cable run.**

**Three agents, each waiting on one of the other two.** And the limit itself is a
datasheet question the owner runs under G-15.

**REQUIREMENT:** the maximum probe cable length the EZO circuits tolerate, from the
manufacturer rather than from any file in this tree. **SEARCH TERM:** "Atlas
Scientific EZO pH EC probe cable length limit extension". **I state no limit.**

### B-04. S-07 and S-09 are two interface rows for one conductor

S-09's own status says it should close as "no relay drive outputs" or MERGE INTO
S-07, which is the same conductor, and its resolution cell reads "BOSS to merge or
close". **Wire-table column 10 and cable-schedule column 6 both require exactly one
interface row per conductor. I cannot write R-05 while the conductor has two.**

### B-05. No terminal namespace exists

Wire-table columns 4 and 6 have nowhere to point and CDR-001 has OPEN in both.
Section 2.5 proposes the shape. **BOSS assigns the prefix, per F-097.**

### B-06. Every remaining OPEN row a run depends on

P-01, P-02, P-05, P-06, S-01, S-02, S-04, S-07, S-10, S-11, S-20, CBL-01, CBL-02,
CBL-03, CBL-04, CBL-06, CBL-07. **Seventeen rows.** Nothing is built against any of
them.

### B-07. The wall layout is mine and it is blocked on M-02 and on Z5

M-02 is OPEN with DOSING and PUMP-BOXES jointly claiming the same wall space and the
tubing between them setting the spacing, and I arbitrate. **I cannot arbitrate a
spacing I have not been given, and I will not invent one.** Z5 is undefined, F-067,
and it is what the channel-token question in K-08 is measured from.

---

## 6. BOUNDARY DEFECTS, REPORTED THROUGH BOSS AND NOT FIXED

Rule 2. I fixed none of these and edited no file but this one.

### BD-01. P-02 EXISTS. F-096 and wire-table-row-zero.md say it does not

**This is the most important item in this pass.**

F-096 reads: "THE SOLENOID HAS FLUID ROWS AND NO POWER ROW. F-01 and F-02 carry the
water into and out of it. NOTHING IN THE INTERFACE TABLE CARRIES THE ELECTRICITY."
CDR-001's Interface row cell reads "OPEN - and this is defect 1 below. The solenoid's
power feed has no P- row." D-140 then records F-096 as one of two defects "the
analysis could not see" and offers it as the argument for the whole change of mode.

**interface-table.md's power crossings section contains:**

> P-02 | MAIN-PANEL: fill solenoid relay output | WATER: fill solenoid coil | OPEN.
> Solenoid coil voltage is undecided and the relay contact rating depends on it |
> WATER returns the solenoid requirement, MAIN-PANEL sizes the contact

**That is the solenoid's electrical crossing, with both ends named, in the P- table,
and it has been there.** CDR-001 column 10 should read **P-02**, and its Status
should not carry "no P- row for the solenoid feed".

**What IS true, and it is a smaller and different defect:** P-02's status text is
**stale**. It says the coil voltage is undecided and that WATER must return the
solenoid requirement. **D-136 ordered and fully specified the valve, and parts.md
carries its coil rating and both current figures.** So the row exists, names both
ends, and describes a question that is closed.

**Why I am confident rather than merely disagreeing:** I read the interface table in
full, as instructed, and the row is in the power crossings table between P-01 and
P-03. This is rule 8 in the other direction - an absence was asserted, and naming
what I read is how it gets checked.

**Routed, not fixed.** The correction is BOSS's: P-02's status is rewritten against
D-136, and F-096 and wire-table-row-zero.md are corrected. **I flag one consequence
because it is the expensive kind: D-140 uses F-096 as evidence for a direction. The
direction is right and this particular piece of evidence is not, and a wrong exhibit
attached to a right conclusion is the shape G-37 exists for.**

### BD-02. CBL- cannot serve as a cable identity, so wire-table column 2 has no valid values

Wire-table column 2 is "Cable: which CBL- run it travels in", and CDR-001 fills it
with **CBL-04**.

**CBL-04 is "WATER: field devices, floats, solenoid, leak sensors, pump cords |
INTERCONNECT: field cable runs".** That is a whole CLASS of runs. **It cannot
distinguish the solenoid cable from the day tank float cable from the storage float
cable from the leak sensor run** - my rows R-11, R-12, R-13, R-14 and R-18 to R-20
all live inside it.

Same for CBL-01, CBL-02 and CBL-03: each names one enclosure's glands against all of
my runs, and several of my cables land at each.

**So the cable schedule needs its own ID namespace and wire-table column 2 points at
it, with the CBL- row kept as the interface reference in column 10.** That is the
shape I proposed in section 1 column 1. **BOSS assigns the prefix.**

### BD-03. F-097's namespace collision is not the only one, and two more are already in the tree

F-097 found that F-nn means a fluid interface row and F-nnn means a finding,
separated by zero padding alone, and correctly calls it F-026 fixed in one place and
left standing in another. **Reading for the terminal namespace, I found two more of
the same shape:**

| Prefix | Meaning 1 | Meaning 2 |
|---|---|---|
| **M-0n** | **Mechanical interface rows** - M-01 day tank penetrations, M-02 the wall space arbitration, M-03 the display box on the wall | **The standpipe extraction's method rules**, M-01 to M-07, where M-01 is the trip-height rule and M-02 is the tether rule |
| **C-0n** | **Commissioning rows**, C-01 upward, which is the namespace F-026 already fought over once | **Two audit files' own lists**: the wall audit's contradiction table C-01 to C-07, and the standpipe extraction's corrections C-01 and C-02 |

**M-02 is the sharpest: it means "the wall space arbitration INTERCONNECT owns" in
one file and "the tether length sets the differential" in another, and both are live
this week.** A cable schedule citing interface rows and a terminal schedule citing
commissioning rows will both have to cite across these.

**Not fixed. It is BOSS's, and it is the same fix F-026 already made once.**

### BD-04. parts.md carries TWO cable-run tables with contradictory allowance rules for the same five figures

Under "Cable runs, measured on the wall, and the CUT LENGTHS", parts.md states the
cut rule as the wall run plus a stated allowance made of a drip loop per grip and
service per end, and gives a Cut column.

Immediately below, under "Cable runs, measured on the wall and already doubled for
slack", **the same five endpoint pairs appear with the same wall-run figures**, and
the text says these already include the slack.

**The same number is described in one table as a bare wall run that must be extended
and in the other as a figure that already contains its allowance.** A builder reading
the second table cuts short.

**This is T-020 exactly, in the authoritative file, on a table that reaches a cut
step - and T-020 is the trap the tree records as having cost STOCK rather than
rework, because a cut cable cannot be un-cut.** It is also G-41's recognition test
one week after G-41 was frozen: a table that can be read either way will be read as
absolute by whoever is holding a credit card.

**Not fixed. It is parts.md and it is the owner's, per D-026 and F-051.** The fix
T-020 prescribes is not to delete one table or reorder them: **it is to fold the
allowance into the cut step so there is only ever one number and one place it comes
from.** Section 1 column 10 is that shape.

### BD-05. P-07 is CLOSED in the interface table and open in display-box.md

The interface row reads CLOSED by parts.md and closes the PRINCIPLE - the Pi is
powered independently, stays alive through a permissive drop, nothing in the panel
can power cycle it. **display-box.md's own open list still carries "Power into this
box, P-07, and whether the Pi is fed from the NDR-240-24 or separately."**

**A closed row with an open conductor inside it.** R-09 cannot be written until the
form is settled and rule 9's protection does not apply, because the row reads closed.

### BD-06. P-01 names one branch circuit; D-137 requires a dedicated one

P-01 is "Building branch circuit | MAIN-PANEL: line input", singular. D-137 says the
chiller and the loop pump **share one switched receptacle on a DEDICATED CIRCUIT**.
**Whether that dedicated circuit is a second feed from the building into the panel or
is derived inside the panel is stated nowhere I read.** It changes whether R-10 is one
run or two, and it is MAIN-PANEL's to answer.

### BD-07. Nothing states where the leak console physically sits

CBL-06 names its End A as "MAIN-PANEL: leak console" and hands the cable to
INTERCONNECT. S-04 makes the sensor placement WATER's. **So a cable is owned, a
sensor position is owned, and the position of the thing between them is owned by
nobody I could find.** R-14 and R-15 both have one end with no position.

And D-133 adds a placement constraint on the sensor end that is easy to lose: **the
sensor must not sit where normal overflow discharge can splash or pool on it**, or
every overflow reads as a leak.

### BD-08. Three crossings have a route and no artifact that owns a route

D-046 removed the cable from P-03, P-04 and P-05. **The cord still crosses the wall.**
It has a path, a length that is a part property, a place where it must not be walked
on or pulled, and in two cases it runs on a standpipe. **A cable schedule row cannot
hold it and nothing else in the tree tries.** Section 1 column 8 is my proposal for
where it goes.

---

## 7. STATUS OF THIS PASS

**Stopped part way, deliberately, and I do not declare myself finished** - rule 7,
and BOSS declares that only after another agent has built against this and found
nothing.

**What is returnable now and does not wait on anything:** the shape of both
schedules, the terminal namespace requirement, the twenty-row inventory, and the
eight constraints.

**What I did NOT return, and why, so the absence is not read as an answer:**

- **No wall layout.** M-02 is open and Z5 is undefined. B-07.
- **No answer to the monotone CH1 to CH8 question.** K-08. Not a no, an unanswered.
- **No separation distances, no gland sizes, no cable selections, no core counts, no
  cut lengths, no terminal numbers.** Rule 3 and G-15. Each appears above as a
  requirement and a search term.
- **No cable schedule and no terminal schedule with rows in them.** Twenty rows are
  identified and zero are buildable, so a schedule written now would be a table of
  BLOCKED, which is what section 3 already is in a more honest form.

**What I would do next, in the order that unblocks the most:** B-02, the four-way
gland deadlock, because it is one allocation decision and it is upstream of all
seventeen runs; then BD-01 and BD-04, because both are corrections to documents that
production is now being written from; then B-05, the terminal namespace, because
MAIN-PANEL is drawing the ladder in this same pass and will need somewhere for its
terminals to point.
