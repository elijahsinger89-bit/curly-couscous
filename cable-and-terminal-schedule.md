# D6. Cable and terminal schedule

**Owner: INTERCONNECT. Issued 2026-09-04.**

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
| What a crossing IS and its status | **interface-table.md**, one FL-, P-, S-, CBL- or M- row. This document cites the id and never restates the meaning |
| Rung logic and device identity | **D2** |
| Face geometry, penetration and rail positions | **D3** |
| Any quantity, count, total or price | **D7, once** |
| Per-channel product, role, jug and cable core | **D11**, the channel register |
| Reasoning and provenance | The tree. No delivered document carries it |

**No length, gauge, core count, terminal count or part number appears in this
document.** Length is not stored anywhere: D-090's allowance is folded into the cut
step, per T-020. **Note before cutting: F-099 is open against parts.md's two
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
channel-token.md's forbidden list exists to prevent. **Rows that are expected to
split are marked in the Blocked on column.**

**Stated once here rather than twenty times in the table:** where on a face a gland
sits, and the spacing between glands, is INTERCONNECT's under D-146 and is OPEN in
every row, because it follows from a wall layout that does not exist while M-02 is
open. **Which face, and the order of entries on it, is the enclosure owner's under
the same allocation.** MAIN-PANEL's is on file in parts.md - every cord grip on the
bottom face, nothing but the five 22 mm devices on top - and is used below.
PUMP-BOXES and DISPLAY-BOX have not been asked and have refused nothing.

### 1.1 Voltage class. INTERCONNECT's vocabulary, per D-150

Three values. It drives insulation and segregation and nothing else.

| Value | Means | No number defines it |
|---|---|---|
| **LINE** | At building supply potential | Membership of the 120 VAC system, not a threshold |
| **24 V** | The panel's 24 V system, whatever the duty | Membership of that system |
| **SIGNAL** | Below the 24 V system: the driver logic supply, the step and direction conductors, the probe conductors | Membership |

**EGC is not a voltage class and has been removed from this vocabulary.** An
equipment grounding conductor takes the voltage class of the circuit it protects, and
"grounding" is a DUTY. **Simpler by one value, per G-44, and it stops a bonding
conductor being sorted away from the circuit it belongs to.**

### 1.2 Duty. MAIN-PANEL's vocabulary, per D-150

**Every duty cell below is OPEN and there is one reason: the vocabulary does not
exist yet.** D-150 gave voltage to INTERCONNECT and duty to MAIN-PANEL, because the
driver motor supply is a power duty at a control voltage and one column was carrying
two facts. **I do not invent MAIN-PANEL's half.** Duty drives G-30's separation of
power from sense; voltage drives insulation. They are not the same sort.

### 1.3 Segregation groups

A local list keyed to this document, per G-43. **It groups runs. It states no
distance, and no separation distance exists anywhere in this tree yet.**

| Group | Holds | What it prevents, and what it costs - G-44 |
|---|---|---|
| **SEG-A** | LINE runs and cords | Prevents a line conductor being the realistic neighbour of a sense conductor, which is the short D-049 handed to the wiring plan. Costs nothing to build, operate or repair: it is a routing rule, not a part |
| **SEG-B** | 24 V runs | As SEG-A. **It does NOT separate power duty from sense duty inside itself** - that is what the duty column is for, and it is open |
| **SEG-C** | SIGNAL runs to the drivers | F-030: eight step conductors in one jacket is the single most probable short in the build, and a step shorted to another step steps two heads together, which violates G-06 in hardware where software cannot prevent it. Costs nothing beyond the return conductors D5 already requires |
| **SEG-D** | Probe runs, alone | INTERCONNECT's standing open item names probe cables separately. Costs nothing. **No rule exists yet for what SEG-D requires, and I state none** |

**Two constraints no group satisfies, carried here because a person routing cable
must see them:**

- **RUN-005 and RUN-006 are the same class as each other**, so no scheme that sorts
  by class separates them. A short between them makes the readback follow the
  command, which is precisely and only the failure G-09 exists to detect, and it
  removes weld detection too. **F-029. They must be separate jackets or provably
  non-adjacent.**
- **RUN-012, RUN-013, RUN-019 and part of RUN-020 are tied to one pipe by D-121 and
  cannot be separated by any group.** Section 4.

---

## 2. THE CABLE SCHEDULE

Device names are post-D-144: the **manifold pump** is the device formerly called the
circulation submersible or circulation pump.

| RUN | End A | A face | End B | B face | Rows | Voltage | Duty | Provision | Seg | Blocked on |
|---|---|---|---|---|---|---|---|---|---|---|
| **RUN-001** | MAIN-PANEL: permissive contactor load side | BOTTOM | PUMP-BOX-A: driver motor supply | OPEN | P-06 | 24 V | OPEN | Cut | SEG-B | P-06; CBL-02; D-150 |
| **RUN-002** | MAIN-PANEL: permissive contactor load side | BOTTOM | PUMP-BOX-B: driver motor supply | OPEN | P-06 | 24 V | OPEN | Cut | SEG-B | P-06; CBL-02; D-150. **Both feeds leave one terminal downstream, parts.md - T-010 applies there, not here** |
| **RUN-003** | DISPLAY-BOX: logic board step and direction outputs | OPEN | PUMP-BOX-A: driver STEP and DIR terminals | OPEN | S-10; P-09 | SIGNAL | OPEN | Cut | SEG-C | S-10; CBL-02; CBL-03; D-150. **Expect a split: F-030's per-signal returns** |
| **RUN-004** | DISPLAY-BOX: logic board step and direction outputs | OPEN | PUMP-BOX-B: driver STEP and DIR terminals | OPEN | S-10; P-09 | SIGNAL | OPEN | Cut | SEG-C | As RUN-003, plus PUMP-BOXES' open division of the eight channels between boxes |
| **RUN-005** | DISPLAY-BOX: logic board permissive coil drive | OPEN | MAIN-PANEL: driver permissive contactor coil | BOTTOM | S-07; **S-09 unmerged** | 24 V | OPEN | Cut | SEG-B | S-07; CBL-03; D-150. **One conductor, two interface rows - S-09's own status says merge into S-07 or close, and D5 admits one row per conductor** |
| **RUN-006** | MAIN-PANEL: second pole of the driver permissive contactor | BOTTOM | DISPLAY-BOX: optocoupler input | OPEN | S-08 | 24 V | OPEN | Cut | SEG-B | CBL-03; DISPLAY-BOX's input side; D-150; **F-029 against RUN-005** |
| **RUN-007** | MAIN-PANEL: K-FILL-D-Q, the normally closed contact | BOTTOM | DISPLAY-BOX: isolated Pi input | OPEN | S-03; **F-107** | 24 V | OPEN | Cut | SEG-B | CBL-03; DISPLAY-BOX's input side; D-150; **F-107 - it carries a conductor with no interface row** |
| **RUN-008** | MAIN-PANEL: K-DRY-Q, second pole | BOTTOM | DISPLAY-BOX: isolated Pi input | OPEN | S-20; **F-107** | 24 V | OPEN | Cut | SEG-B | S-20; CBL-03; D-150; F-107 |
| **RUN-009** | MAIN-PANEL: fused, NOT relay switched receptacle | BOTTOM | DISPLAY-BOX: Pi power | OPEN | P-07 | LINE, **contested** | OPEN | OPEN | SEG-A | CBL-03; D-150. **P-07 reads CLOSED in the interface table while display-box.md still carries its form as open. The principle is closed; the conductor is not, and provision and voltage both follow the answer** |
| **RUN-010** | Building branch circuit | n/a | MAIN-PANEL: line input | BOTTOM | P-01 | LINE | OPEN | Cut | SEG-A | P-01; D-150. **May be two jackets: D-137's dedicated chiller circuit is unaccounted for in P-01, and no disconnecting means is named** |
| **RUN-011** | MAIN-PANEL: K-FILL-S, solenoid pole | BOTTOM | FIELD: fill solenoid coil | OPEN | **P-02** | LINE | OPEN | Cut | SEG-A | P-02; CBL-04; D-150. **P-02's text is stale, F-098: it says the coil voltage is undecided and D-136 specified the valve** |
| **RUN-012** | FIELD: day tank floats, on the day tank standpipe | OPEN | MAIN-PANEL: coil chains, per D-154 | BOTTOM | S-02 | **24 V**, D-154 | OPEN | **Supplied** | SEG-B | S-02; CBL-04; D-150; **F-100** cord length; **F-113** section 4 |
| **RUN-013** | FIELD: storage tank floats, on the storage standpipe | OPEN | MAIN-PANEL: coil chains, per D-154 | BOTTOM | S-01 | **24 V**, D-154 | OPEN | **Supplied** | SEG-B | As RUN-012, on S-01 |
| **RUN-014** | FIELD: leak detection sensor | OPEN | MAIN-PANEL: leak console | **UNPLACEABLE** | S-04 | OPEN | OPEN | Supplied | OPEN | S-04; D-150; **the console's position is stated in no file**; **F-104** - a floor built to move water to a track drain hides a leak from a floor sensor, so the sensor's position and therefore this jacket's are both open |
| **RUN-015** | MAIN-PANEL: leak console, 24 V in and Form C out | **UNPLACEABLE** | MAIN-PANEL: permissive string | BOTTOM | **CBL-06** | **LINE-rated**, CBL-06 | OPEN | Cut | SEG-A | CBL-06; D-150; the console's position. **CBL-06 requires every conductor in this jacket at the higher rating including the 24 V pair. The float requirement's finding 5 records the string's class stated two ways** |
| **RUN-016** | DOSING: probes in the manifold probe section | n/a, a wet fitting | DISPLAY-BOX: the EZO circuits and their carriers | OPEN | S-11 | SIGNAL | OPEN | **Supplied** | SEG-D | S-11; CBL-03; D-150. **The EZO length limit is a lookup nobody has run** - section 5 |
| **RUN-017** | MAIN-PANEL: ground bar | BOTTOM | **A SET, not one end** | OPEN | **CBL-07** | Takes the class it protects | OPEN | Cut | Rides its circuit | CBL-07; D-150. **PROVISIONAL ID.** CBL-07 is one crossing over four enclosures, and an EGC is either a conductor inside each other jacket or a separate bonding run to each plastic box. Those are different id counts. **This row will retire under D-149 when CBL-07 returns** |
| **RUN-018** | MAIN-PANEL: relay-switched receptacle, panel mounted | **FACE**, D-046 | FIELD: transfer pump cord cap | n/a | P-03 | LINE | OPEN | **Cord** | SEG-A | P-03's circuit and rating; D-150 |
| **RUN-019** | MAIN-PANEL: relay-switched receptacle, panel mounted | **FACE**, D-046 | FIELD: manifold pump cord cap | n/a | P-04 | LINE | OPEN | **Cord** | SEG-A | P-04's circuit and rating; D-150. **On the day tank standpipe** - section 4 |
| **RUN-020** | MAIN-PANEL: **the row's End A names a device D-108 says does not exist** | **FACE**, D-046 | FIELD: chiller cord cap and chiller loop pump cord cap | n/a | P-05, as amended by D-137 | LINE | OPEN | **Cord**, two | SEG-A | P-05; D-150. **End A is unwritable as the row writes it, and no file names the device that switches this receptacle.** The loop pump's cord is on the day tank standpipe - section 4 |

### 2.1 What is filled, honestly

**Twenty jackets. 137 of the 180 content cells filled. ZERO rows complete.**

**Twenty of the forty-three gaps are one column: duty.** Three rows - RUN-010,
RUN-018 and RUN-019 - are **one word from complete, and that word is MAIN-PANEL's
under D-150.** Under document-plan.md 4.1 nothing can be wired until D6 is complete
for the jacket in question, so **a vocabulary nobody has written is currently on the
build's critical path.** Stated, not solved.

### 2.2 Three rows that are not one physical thing, flagged so nobody builds them

- **RUN-017** is one id standing in for a set of unknown size. Section 2, and it
  retires under D-149.
- **RUN-003 and RUN-004** are expected to split when F-030's per-signal returns
  settle. **Do not order or label against these two ids.**
- **RUN-018, RUN-019 and RUN-020 have no CDR- children**, because a cord's
  conductors are inside a manufactured assembly and nothing lands them. **D5 will
  never name these three ids. That is correct and is not an error to fix.**

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
and never as a whole part, so a block silked "1" is carried without ever becoming a
bare digit. **An id changes only when the PART changes**, so it survives a relay
moving sockets, a jacket splitting and a channel being reassigned. **It is never
derived from a RUN- id and no RUN- id is derived from it.**

**If a wire marker cannot hold the canonical form, that is a carrier defect to
report, never solved by inventing a short form at the wall.** No short form is
defined here.

### 3.2 The marking source column, and why it is not optional

**F-051 is the entire reason.** Every file in this tree said VM; the part carries a
circled plus and a circled minus. **A marking quoted from a document is not a marking
read off a part.**

| Source | Means |
|---|---|
| `PART` | Read off the physical part |
| `FILE` | Quoted from a tree document. **Provisional until somebody looks** |
| `DESCRIBED` | Nothing is printed. `which` is a braced descriptor |

**G-44 test on this column: what failure does it prevent, and what does it cost?** It
prevents a build sheet naming a terminal that is not on the part, which is T-013 and
is the failure that once told a builder to verify a short across a 5 V supply and
tick the box. It costs one word per row to build, nothing to operate, and nothing to
repair. **It goes in.**

**Not one row below is marked PART. F-106: nobody in this project has ever been asked
to look at a terminal and report what is printed on it.**

### 3.3 The schedule

| TRM | Device, by name | Which | Source | Runs landed | Row | Blocked on |
|---|---|---|---|---|---|---|
| `TRM-MAIN-PANEL.{unnamed}.{motor supply pole}` | **UNNAMED**, F-105 | `{motor supply pole}` | DESCRIBED | RUN-001, RUN-002 | P-06 | **F-105 and D-151: the device has no name, only a part number and an ordinal.** MAIN-PANEL owns naming it. **T-010 applies here: two jackets leave one terminal** |
| `TRM-MAIN-PANEL.{unnamed}.{readback pole}` | **UNNAMED**, F-105 | `{readback pole}` | DESCRIBED | RUN-006 | S-08 | F-105. Also the open question of whether that contactor's poles share one contact volume, which would put S-08 against G-30 with nowhere to move |
| `TRM-MAIN-PANEL.K-FILL-S.{solenoid pole}` | **K-FILL-S**, order.md | `{solenoid pole}` | DESCRIBED | RUN-011 | P-02 | P-02; no marking has been read. **The pole is sized on the make-and-break event, not the holding figure** |
| `TRM-MAIN-PANEL.K-FILL-D-Q.{S-03 changeover}` | **K-FILL-D-Q**, order.md | `{S-03 changeover pair}` | DESCRIBED | RUN-007 | S-03 | No marking read; **F-107 - one conductor landing here has no interface row** |
| `TRM-MAIN-PANEL.K-DRY-Q.{Pi pair}` | **K-DRY-Q**, order.md | `{complementary pair}` | DESCRIBED | RUN-008 | S-20 | S-20; **the relay is called K-DRY in the interface table and K-DRY-Q in order.md, so the id is unstable until one name wins** |
| `TRM-MAIN-PANEL.{ground bar}.{...}` | **{ground bar}**, not yet a bought part | OPEN | OPEN | RUN-017 | CBL-07 | CBL-07; the bar is not bought; RUN-017 is provisional |
| `TRM-FIELD.{fill solenoid}.{coil lead}` | The fill solenoid specified by D-136 | OPEN | **OPEN** | RUN-011 | P-02 | **Coil lead identification has never been looked up.** Per F-051 it is named by what is printed on the part, and nobody has looked |
| `TRM-PUMP-BOX-A.{driver}.{...}` | OPEN | OPEN | OPEN | RUN-001, RUN-003 | P-06, S-10, P-09 | S-10; P-06. **The pin list is known and the MARKINGS are not** - parts.md records that the flat pin list is a list of names that was read as an order, and the board is two connectors |
| `TRM-PUMP-BOX-B.{driver}.{...}` | OPEN | OPEN | OPEN | RUN-002, RUN-004 | P-06, S-10, P-09 | As PUMP-BOX-A |
| `TRM-DISPLAY-BOX.{logic board}.{...}` | OPEN. The board is hand built and does not exist | OPEN | OPEN | RUN-003 to RUN-009, RUN-016 | S-07, S-08, S-03, S-20, S-10, S-11, P-07 | S-12 is not frozen and the board does not exist |

**Ten landing points. None buildable. Two blocked on a device that has no name.**

### 3.4 The check this table holds that no other document can

**T-009 and T-010: a terminal carrying exactly one conductor is an open circuit, not
a spare, and clamps are counted against conductors rather than assumed.** The first
row already shows two jackets leaving one terminal. Neither question is answerable
from D5 or from section 2, because both are organised by a conductor's journey and
this table is organised by its destination.

---

## 4. F-113. WHAT THE STANDPIPE ADJACENCY COSTS

**Asked of INTERCONNECT. The method is not reopened: D-121 answers a float that has
moved, and nothing in this system measures a level, so an unmarked float that slips
is invisible. That is the worse failure and the method stays.**

**What D-049 gave up.** G-22 asks two questions of every sense path. D-049 amended
it: the severed case is chosen safe on frequency, and **the short case is answered by
ADJACENCY - the wiring plan - and not by circuit design.** That escape assumes a
route with choices in it. **D-121 fixes the adjacency at worst case by construction,
so on RUN-012, RUN-013, RUN-019 and part of RUN-020 there is no wiring plan left to
answer with.** Grade: **STRUCTURAL** while D-121 stands. Nothing added to the wiring
plan changes it, because the wiring plan is what was removed.

### The cost, in four parts

**COST 1, and it is the expensive one, and it is NOT the 120 V one.** WATER's float
requirement states it: a short between two float pairs on one standpipe can bridge a
high-high to a fill float and produce "level is fine" on a chain that is not fine.
Under D-154 every float is a series element in a coil chain, so **a bridge does not
report a wrong level - it shorts out the elements between the bridge points and
closes the chain around an open float.** Severed is safe; this is not.

**And it is already paid for.** D-130 made the overflow bulkhead a requirement on
both tanks precisely because a fill that does not stop has no second line, and FL-11
and FL-12 now carry it. **The mitigation exists, was bought for a different reason,
and lands above the high-high per D-134 so the instrumented protection trips first.**
Under G-44 nothing is added, because the thing that would be added is already there.

**COST 2. The cross-class short is less probable and more severe, and its whole cost
is a purchasing attribute.** A 120 VAC conductor faulting to a 24 V float conductor
does not flip a level; it injects line potential into a coil chain that runs to the
panel and to three optocoupled inputs. **CBL-06 already sets this tree's precedent:
where a 120 V leg shares a jacket, every conductor takes the higher rating.** These
share a tie bundle rather than a jacket and no row covers that case. **The cost is
that the float cord's insulation rating is set by the highest voltage in the bundle
rather than by its own use** - which is free to state now, while WATER's float
requirement is open and no float is bought, and costs money after. **Same window and
same shape as F-100.**

**COST 3. A tie is a compression point, and D-131 puts a person's hands on it.** The
commissioning step is fill slowly, confirm each float trips at its mark, adjust the
tie and never the wiring - with both pumps running continuously under D-143, in
water, on cords tied to the same pipe. **G-22 asks what a severed conductor does and
G-39 asks what a dead panel does. Nothing in this tree asks what a wet hand does**,
and this is the one place in the build where that question has an address.

**COST 4. It removes a diagnostic, not just a margin.** Off the pipe, a conductor's
neighbour is a choice and therefore a recorded fact. On the pipe every float
conductor's realistic neighbour is every other cord on that tank, **so a fault cannot
be localised by knowing what lies next to what.** That is a repair cost, paid every
time, forever.

### What is worth doing, each with what it prevents and what it costs - G-44

| | What it prevents | Build | Operate | Repair |
|---|---|---|---|---|
| **M1. Float cords and pump cords are never under the same tie.** Separate tie groups on the pipe | The compression contact between two classes at the one point insulation is stressed for the life of the build. Does not touch cost 1 | **Nothing. It is a tie position, not a part** | Nothing | **Negative cost: a cord is identifiable by which group it is in** |
| **M2. The float cord's insulation rating is set by the highest voltage in the bundle.** Into WATER's float requirement, which is open | Cost 2 entirely | **Nothing now. Money if stated after a float is bought** | Nothing | Nothing |
| **M3. A question, not a change: do the pump cords need the pipe at all?** | Cost 2 and most of cost 4, at zero cost | - | - | - |

**M3 is routed to the owner and I am not making it.** D-121 says one pipe carries
every float **and every cord**, and that sentence is the owner's. **What is worth his
eye: the pipe was adopted so a float that has moved is visible, and a pump gets no
positioning benefit from it** - water.md holds the submersibles by cradle, with both
cords strain-relieved so they carry no positioning duty. **So the pump cords are on
the pipe for tidiness, and under G-44 the burden of proof is on the addition.**
Removing them removes cost 2 and most of cost 4 and buys nothing back that the
mounting method was adopted for.

**REJECTED under G-44, and named so nobody proposes them later:** a shield, a
separate conduit, a barrier or a divider on the pipe. Each costs money and build
time, each obstructs the tie a person must reach under D-131, **and none of them
touches cost 1, which is float-to-float and inside one class.** An addition that
misses the expensive failure and charges for the cheap one does not go in.

---

## 5. REQUIREMENTS AND SEARCH TERMS

No value is stated. Each is a lookup the owner runs under G-15.

| For | Requirement | Search term |
|---|---|---|
| RUN-011, RUN-015, RUN-018 to RUN-020 | A flexible LINE-class cable for a wall route in a room where water moves tank to tank, with an equipment grounding conductor | `flexible power cable 600 V oil resistant wet location`; `tray cable TC-ER exposed run wall` |
| RUN-012, RUN-013 | **The float cord's insulation rated for the highest voltage in the standpipe bundle, not for its own 24 V use.** Section 4, M2 | `float switch cord insulation voltage rating 600 V`; `submersible level switch cable water resistant rating` |
| RUN-015 | Confirmation that every conductor in one jacket may share the higher rating CBL-06 requires | `600 V insulated conductor mixed circuit same raceway control cable` |
| RUN-016 | The maximum probe cable length the EZO circuits tolerate. **Not from any file in this tree** | `Atlas Scientific EZO pH EC probe cable length limit extension` |
| Every gland entry | A cord grip per entry, sized to the cable chosen, sealed at least to the enclosure's rating and suitable for the face it lands on under F-088 | `liquid tight cord grip strain relief NPT cable range chart` |
| The segregation rule | A stated rule for which classes may share a duct, a jacket, a clip run or a tie bundle, and what an unavoidable crossing requires | `control panel power and signal circuit segregation separation`; `Class 1 Class 2 circuits same raceway` |
| Labelling | A marker carrier that holds the canonical three-part TRM- form and, on a per-channel core, the channel token in addition without merging them | `wire marker sleeve character capacity heat shrink printable` |

---

## 6. WHY THERE IS NO DUPLICATION CONTRACT IN THIS DOCUMENT

**G-45. D5 and D6 are generated from one source, so they cannot disagree, and a
schedule is never hand-transcribed.** The rule that said they must agree has been
deleted rather than restated: **a contract needs a reader who obeys it; a mechanism
does not.**

**Two facts do not survive generation and are therefore stated here and nowhere
else:**

1. **The terminal marking source, section 3.2.** A generator can make two documents
   carry the same marking. **It cannot make anyone have looked at the part.** Copying
   a FILE-sourced marking forward renders it indistinguishable from a PART-sourced
   one, and F-051 exists because that difference was once wrong in every file in the
   tree at once.
2. **The per-conductor fail direction, which lives in D5 and appears nowhere in this
   document.** It is established per conductor and never inherited, F-017. **A
   jacket-level roll-up would average several directions into one**, which is exactly
   the inheritance that put S-03's fail direction on file as S-08's before anyone
   checked.

---

## 7. STATUS

**Stopped part way. INTERCONNECT does not declare this finished** - rule 7, and that
waits until another agent builds against it and finds nothing.

**Deliverable as it stands:** every jacket and every landing point in the build has a
real id, an owner, and a named blocker. A person can route, group and plan against
it. **Nobody may cut, order or land against it yet**, and the reasons are in the
Blocked on column of every row.

**Four things would move the most, in order:**

1. **MAIN-PANEL's duty vocabulary, D-150.** One column, twenty cells, and three rows
   go from one-word-short to complete.
2. **PUMP-BOXES and DISPLAY-BOX stating faces and order under D-146.** Sixteen cells,
   and it costs them nothing: a face follows from what is inside the box.
3. **Naming the driver permissive contactor, F-105 and D-151.** Two landing points
   cannot exist until it has a name.
4. **The S-07 and S-09 merge.** RUN-005 carries one conductor with two interface rows
   and D5 admits one.

**Not returned, so no absence is read as an answer:** no wall layout, because M-02 is
open and Z5 is undefined; **no answer to channel-token.md's monotone CH1 to CH8
question, which is unanswered rather than no**, for the same reason; no gland count,
spacing, position, cable selection, core count, cut length or terminal number, all of
which are requirements in section 5.
