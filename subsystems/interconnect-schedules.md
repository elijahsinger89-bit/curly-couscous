# INTERCONNECT: the cable schedule and the terminal schedule

Second pass, 2026-09-04, against D-142's acceptance and the routing appended to
subsystems/interconnect.md. **Two documents, not two shapes.** Blocked rows carry
real IDs and say what blocks them.

**Re-read before writing, as instructed:** subsystems/interconnect.md including the
appended routing; interface-table.md in full, including the reserved namespace table
at the top and the gland-boundary allocation at the bottom; **every FL- row, because
they were renamed**; decisions.md D-140 through D-147; findings.md F-096 through
F-104; subsystems/main-panel-ladder.md, which landed in the same pass and touches
seven of my rows; order.md's envelope map; parts.md; channel-token.md;
channel-register.md; wire-table-row-zero.md; traps.md T-008 to T-013 and T-020.

**No length, gauge, core count, terminal count or part number is stated from memory
or by derivation.** Where a value is needed there is a requirement and a search term.
**Nothing is built against an OPEN row.** Every absence names what was read.

---

## PART A. THE CABLE SCHEDULE

### A.1 What a RUN- id is, and the one thing it must be pinned to first

D-145 defines RUN-nnn as **one physical cable run**. Filling the schedule in showed
that phrase carries two readings and the difference is load-bearing:

| Reading | Consequence |
|---|---|
| **RUN- is a ROUTE** - panel to display box, one id | Wire-table column 2 becomes unusable again for the same reason CBL- was: **a conductor travels in a jacket, not in a route** |
| **RUN- is a JACKET** - one id per cable | Column 2 works, and **the id count is not knowable until the wire table exists**, because F-029 and F-030 split some routes |

**I take RUN- to mean ONE JACKET, because that is the only reading that makes
wire-table column 2 point at something a conductor can be inside.** I am recording
it as a reading and not as a decision, because the prefix is BOSS's.

**And the consequence has to be stated before any id is used, not after:** several
of the twenty ids below will SPLIT when F-029's non-adjacency requirement and
F-030's per-signal return requirement are settled. **Nothing in the tree says what
happens to an id that splits.** channel-token.md forbids renumbering and forbids
closing a gap; applied here that means **a split parent is RETIRED and the children
take new numbers, never a suffix** - but that is a namespace rule and it is BOSS's
to make. **I have not invented it and I have not used a suffix anywhere below.**

### A.2 The assignment rule

**The number in a RUN- id carries no meaning.** Not a route order, not a class, not
a priority, not a build sequence. No rule may be keyed to it, and a gap is never
closed. T-013 and channel-token.md forbidden items 2, 9 and 11.

Ids RUN-001 to RUN-020 are assigned in the order the runs were enumerated in
interconnect-first-pass.md, so that the two documents can be read against each other.
**That the three cord routes landed on the last three numbers is an accident of that
order and is NOT a rule. A future cord route takes the next free number.**

### A.3 The schedule, table 1 of 2: identity, endpoints and entries

**Table 1 and table 2 are ONE SCHEDULE keyed by RUN-, split for width.** Reading
either alone gives a wrong answer about a run. G-41's recognition test applies to
this file too.

Device names are post-D-144: **the manifold pump** is the device formerly called the
circulation submersible or circulation pump.

Entry face is filled where the enclosure owner has already stated it, per D-146.
**parts.md states the main panel's: every cord grip is on the BOTTOM face, and
nothing but the five 22 mm devices penetrates the top.** That is the enclosure
owner's decision already on file, so twelve entry cells fill in today.

| RUN | End A | A entry face | End B | B entry face | Interface rows realised |
|---|---|---|---|---|---|
| **RUN-001** | MAIN-PANEL: permissive contactor load side | **BOTTOM**, parts.md | PUMP-BOXES: driver motor supply, box A | OPEN, CBL-02 | P-06 |
| **RUN-002** | MAIN-PANEL: permissive contactor load side | **BOTTOM**, parts.md | PUMP-BOXES: driver motor supply, box B | OPEN, CBL-02 | P-06 |
| **RUN-003** | DISPLAY-BOX: logic board step and direction outputs | OPEN, CBL-03 | PUMP-BOXES: the driver STEP and DIR screw terminals, box A | OPEN, CBL-02 | S-10, and P-09 if one jacket |
| **RUN-004** | DISPLAY-BOX: logic board step and direction outputs | OPEN, CBL-03 | PUMP-BOXES: the driver STEP and DIR screw terminals, box B | OPEN, CBL-02 | S-10, and P-09 if one jacket |
| **RUN-005** | DISPLAY-BOX: logic board permissive coil drive | OPEN, CBL-03 | MAIN-PANEL: the driver permissive contactor coil | **BOTTOM**, parts.md | S-07, **and S-09, unmerged** |
| **RUN-006** | MAIN-PANEL: pole 2 of the driver permissive contactor | **BOTTOM**, parts.md | DISPLAY-BOX: optocoupler input | OPEN, CBL-03 | S-08 |
| **RUN-007** | MAIN-PANEL: the normally closed contact of the day tank fill relay's quiet envelope | **BOTTOM**, parts.md | DISPLAY-BOX: isolated Pi input | OPEN, CBL-03 | S-03, **and the D-042 second leg, which has no row - ?27** |
| **RUN-008** | MAIN-PANEL: second pole of the dry-run relay | **BOTTOM**, parts.md | DISPLAY-BOX: isolated Pi input | OPEN, CBL-03 | S-20, **and order.md's complementary pair, which the row does not describe - ?28** |
| **RUN-009** | MAIN-PANEL: fused, NOT relay switched receptacle | **BOTTOM**, parts.md | DISPLAY-BOX: Pi power | OPEN, CBL-03 | P-07 |
| **RUN-010** | Building branch circuit | **BOTTOM**, parts.md | MAIN-PANEL: line input | n/a, this is End B | P-01 |
| **RUN-011** | MAIN-PANEL: fill solenoid relay output | **BOTTOM**, parts.md | WATER: fill solenoid coil | OPEN, CBL-04 | **P-02** |
| **RUN-012** | WATER: day tank floats, on the day tank standpipe | OPEN, CBL-04 | MAIN-PANEL: transfer relay seal-in chain, and possibly the permissive string | **BOTTOM**, parts.md | S-02, and possibly the permissive string per ?13 and ?14 |
| **RUN-013** | WATER: storage tank floats, on the storage standpipe | OPEN, CBL-04 | MAIN-PANEL: fill relay seal-in chain, and possibly the permissive string | **BOTTOM**, parts.md | S-01, and possibly the permissive string per ?13, ?14 and ?15 |
| **RUN-014** | WATER: leak detection sensor placement | OPEN, CBL-04 | MAIN-PANEL: leak console | **UNPLACEABLE** - the console's position is stated nowhere | S-04 |
| **RUN-015** | MAIN-PANEL: leak console, 24 V in and Form C out | **UNPLACEABLE**, as RUN-014 | MAIN-PANEL: permissive string | **BOTTOM**, parts.md | **CBL-06** |
| **RUN-016** | DOSING: pH, EC and PT-1000 probes in the manifold probe section | n/a, a wet fitting | DISPLAY-BOX: the EZO circuits and their carriers | OPEN, CBL-03 | S-11 |
| **RUN-017** | MAIN-PANEL: ground bar | **BOTTOM**, parts.md | **SEE A.6 - this is not one run and the id is provisional** | OPEN | **CBL-07** |
| **RUN-018** | MAIN-PANEL: relay-switched receptacle, panel mounted | **FACE, not a gland**, D-046 | WATER: transfer pump cord cap | n/a, a cord cap | P-03 |
| **RUN-019** | MAIN-PANEL: relay-switched receptacle, panel mounted | **FACE, not a gland**, D-046 | WATER: manifold pump cord cap | n/a, a cord cap | P-04 |
| **RUN-020** | MAIN-PANEL: **the row's End A names a device D-108 says does not exist** | **FACE, not a gland**, D-046 | WATER: chiller cord cap AND chiller loop pump cord cap | n/a, two cord caps | P-05, as amended by D-137 |

**Where on the face, and the spacing between glands, is INTERCONNECT's under D-146
and is OPEN in every row**, because it follows from the wall layout and M-02 is open.
**BOSS states no gland count, no spacing and no position, and neither do I.**

### A.4 The schedule, table 2 of 2: class, provisioning, segregation and status

Class vocabulary is wire-table column 8's four values. **Filling this column found a
fifth duty the four do not cover - see A.7, finding 3.**

| RUN | Class | Cut / supplied / cord | Segregation group | Wall run | Status and what blocks it |
|---|---|---|---|---|---|
| RUN-001 | **24 V, POWER duty** - see A.7 finding 3 | Cut | SEG-B | Measured, parts.md, **and see F-099** | **BLOCKED: P-06 OPEN.** Both ends must agree voltage, conductor and gland first, and PUMP-BOXES owes the driver supply range from the datasheet. Also CBL-02 |
| RUN-002 | As RUN-001 | Cut | SEG-B | Measured, parts.md, F-099 | **BLOCKED: P-06 OPEN.** Note parts.md: one pole for motor-supply distribution, not two, both feeds off one terminal downstream of it - **two jackets from one terminal** |
| RUN-003 | SELV signal | Cut | **SEG-C** | Measured, parts.md, F-099 | **BLOCKED: S-10 OPEN.** P-09's source is closed by D-031. **Whether S-10 and P-09 share this jacket is mine and cannot be settled before F-030's per-signal returns are** |
| RUN-004 | SELV signal | Cut | **SEG-C** | Measured, parts.md, F-099 | **BLOCKED: S-10 OPEN**, plus PUMP-BOXES' open item on how the eight channels divide between boxes, which it is told to coordinate with INTERCONNECT and not decide alone |
| RUN-005 | 24 V control | Cut | SEG-B | Measured, parts.md, F-099 | **BLOCKED: S-07 OPEN, and the conductor has TWO interface rows.** S-09's own status says it should close as "no relay drive outputs" or merge into S-07, which is the same conductor, and the resolution cell reads BOSS to merge or close. **Wire-table column 10 admits one row per conductor** |
| RUN-006 | 24 V control | Cut | SEG-B | Measured, parts.md, F-099 | **BLOCKED: CBL-03, DISPLAY-BOX's input side, no TRM- values.** The circuit itself is closed and recorded as given in parts.md. **F-029 forbids this jacket being adjacent to RUN-005** |
| RUN-007 | 24 V control | Cut | SEG-B | Measured, parts.md, F-099 | **BLOCKED: CBL-03, DISPLAY-BOX's input side, no TRM- values, and ?27** - the D-042 dose-inhibit leg reaches the Pi in this jacket and has no interface row at all |
| RUN-008 | 24 V control | Cut | SEG-B | Measured, parts.md, F-099 | **BLOCKED: S-20 OPEN**, and ?28 - the row describes one pole and one input while order.md builds a complementary pair. **Its fail direction is established, never inherited, per F-017** |
| RUN-009 | **120 VAC, contested** | **OPEN** - see status | SEG-A | Measured, parts.md, F-099 | **BLOCKED on a contradiction, F-098's shape: P-07 reads CLOSED in the interface table while display-box.md still carries "Power into this box, P-07, and whether the Pi is fed from the NDR-240-24 or separately" as OPEN.** The principle is closed; the conductor is not, and its class follows the answer |
| RUN-010 | 120 VAC | Cut | SEG-A | **Not measured. It leaves the 8 by 8 envelope** | **BLOCKED: P-01 OPEN.** And ?1 and ?2: no disconnecting means is named anywhere, and the branch-circuit arrangement is unstated. **D-137's dedicated chiller circuit may make this two runs and nothing says** |
| RUN-011 | **120 VAC** | Cut | SEG-A | **Not measured** | **BLOCKED: P-02 OPEN, and its text is stale - F-098.** The device is fully specified by D-136. **The conductor is sized on the make-and-break event, not the holding figure**, and that is wire-table column 9's business, not this schedule's |
| RUN-012 | **CONTESTED: 24 V control per F-089, or 120 V class per ?12** | **SUPPLIED, NOT CUT - F-100** | **CONTESTED, SEG-B or SEG-A** | **Not measured** | **BLOCKED: S-02 OPEN; ?12, ?13, ?14 on whether any float in this jacket sits in the permissive string; F-100 on the cord; CBL-04.** See A.7 finding 4 |
| RUN-013 | As RUN-012 | **SUPPLIED, NOT CUT - F-100** | As RUN-012 | **Not measured** | **BLOCKED: S-01 OPEN; ?12, ?13, ?14, ?15; F-100; CBL-04** |
| RUN-014 | **OPEN.** Nothing states the sensor's cable class | **Supplied with the sensor** | OPEN | **Not measured** | **BLOCKED: S-04 OPEN; the console has no position; and F-104 - a floor built to move water to a track drain hides a leak from a floor sensor, which changes where the sensor goes and therefore where this run goes** |
| RUN-015 | **Every conductor at the higher insulation rating, CBL-06 as frozen. CONTESTED by ?12** | Cut | **SEG-A, on the frozen text** | **Not measured** | **BLOCKED: CBL-06 OPEN; console position unstated; and ?12 - MAIN-PANEL says one sentence on the string's voltage class decides a cable purchase, and this is the cable** |
| RUN-016 | SELV signal | **SUPPLIED with the probes** | **SEG-D, its own** | parts.md: within the same run as the tank | **BLOCKED: S-11 OPEN, and the three-way circular wait is unbroken** - my file says get the length limit from DISPLAY-BOX, display-box.md waits on DOSING, S-11 gives me the run |
| RUN-017 | EGC | Cut | **Rides with the run it protects** | n/a | **BLOCKED: CBL-07 OPEN, and the id is provisional - see A.6** |
| RUN-018 | 120 VAC | **CORD** | SEG-A | **Not measured** | **BLOCKED: P-03's circuit and rating open; route blocked on the wall layout.** Mounting closed by D-046 |
| RUN-019 | 120 VAC | **CORD** | SEG-A | **Not measured** | **BLOCKED as RUN-018. This cord runs on the day tank standpipe** under D-121 - see A.7 finding 4 |
| RUN-020 | 120 VAC | **CORD, two of them** | SEG-A | **Not measured** | **BLOCKED: P-05 OPEN, and ?10 - its End A names a chiller contactor D-108 says does not exist, so the cell cannot be written as the row writes it.** Also ?8: nothing names the device that switches this receptacle. **The loop pump's cord is also on the day tank standpipe** |

### A.5 The segregation groups

**A local list, keyed to this document, per G-43.** It is a grouping of runs, not a
separation distance, and I state no distance.

| Group | Holds | Why it is its own group |
|---|---|---|
| **SEG-A** | 120 VAC runs and cords | The class the tree already treats as needing its own insulation ruling, CBL-06 |
| **SEG-B** | 24 V runs, both control duty and the driver motor supply | See A.7 finding 3: two duties are in here and one bucket may be wrong |
| **SEG-C** | SELV signal to the drivers | F-030: eight step conductors in one jacket is the single most probable short in the build, and the fix is per-signal returns |
| **SEG-D** | Probe runs, alone | INTERCONNECT's standing open item names probe cables separately from step and direction. **The tree has no separation rule yet and I am not inventing one** |
| **EGC** | Not a group. It rides with the run it protects | CBL-07: no bonding path through any plastic box, every ground lands on the bar |

**Two constraints that cut across the groups and are not satisfied by them:**

- **F-029: RUN-005 and RUN-006 are the same class as each other**, so no scheme that
  sorts by class separates them, and a short between them makes the readback follow
  the command - the one failure G-09 exists to detect. **They must be separate
  jackets or provably non-adjacent, and that is a construction requirement on top of
  the grouping.**
- **The day tank standpipe puts SEG-A and SEG-B in one tie bundle, in the water**,
  by D-121 and D-131. **No group membership fixes that** - see A.7 finding 4.

### A.6 Why the cord routes are in this schedule, and where RUN-017 is provisional

**RUN-018, RUN-019 and RUN-020 stay in the cable schedule** rather than in a document
of their own. D-046 removed the cable and left a physical route across the wall that
only INTERCONNECT arbitrates, and in two cases that route is a standpipe. **If they
are not here nothing owns them.**

**What is structurally different about them, stated so nobody reads it as an error:
they have NO CDR- children.** A cord's conductors are inside a manufactured assembly
and nothing lands them on a terminal, so wire-table column 2 will never name
RUN-018, RUN-019 or RUN-020. **A RUN- with no conductors is correct here and only
here.**

**RUN-017 is a provisional id and I say so rather than pretending otherwise.**
CBL-07 is one crossing covering all four enclosures. Writing it as one run made the
question visible: **an equipment grounding conductor is either a conductor inside
each of the other runs, or a separate bonding run to each plastic box.** Those are a
different number of ids. **The choice is mine and I cannot take it until CBL-01 to
CBL-04 return faces**, because a separate bonding run needs its own entry at each
box. **RUN-017 is therefore one id standing in for a set whose size is unknown, and
it is the only row in this schedule that is not one physical thing.**

### A.7 What assigning real ids revealed that the shape work did not

**FINDING 1. The FL- rename left one row behind, and it is the one row where the
collision is live in the same table.**

D-145 renames "F-01 through F-09" to FL-01 through FL-09, 72 references in one pass,
so that F- means only a finding. **The fluid crossings table has a tenth row and it
still reads FL-10.** I read the table top to bottom: FL-01, FL-02, FL-03, FL-04,
FL-05, FL-06, **FL-10**, FL-07, FL-08, FL-09.

**And it is not a cosmetic leftover. Two rows below it, P-06's status text cites
F-010** - the finding about the 24 V rail trim. **So FL-10 and F-010 now sit in the
same table, one keystroke apart, meaning a fluid interface row and a finding.** That
is F-097's exact defect, in the exact place D-145 closed it.

I cited that row in my first pass, as part of "FL-01 to FL-10: fluid, no run", which
is why re-reading the FL- rows as instructed caught it. **Not fixed. BOSS owns the
namespace.**

**FINDING 2. The device the terminal schedule has to anchor on has no name, only a
part number and an ordinal.**

TRM- part 2 requires a device named per G-28, which says a relay is labelled BY NAME
and never by position, because relays are not interchangeable once bought.

order.md's envelope map gives six real names: K-PERM, K-FILL-D-Q, K-DRY-Q, K-FILL-S,
K-FILL-D-P, K-DRY-P. **The driver permissive contactor has none.** parts.md,
interface-table.md S-08 and the ladder all call it by its part family, and the ladder
distinguishes two of them as **"22.32 #1" and "22.32 #2"**.

**That is a part number plus an ordinal, which is precisely the two things G-28 and
T-013 forbid a device identity from being.** S-08's terminal is on it. **So the
single most-cited terminal in the tree cannot be given a stable TRM- id, and the
reason is not missing data - it is that the device was never named.**

Two smaller instances of the same shape: **interface-table.md S-20 says "second pole
of K-DRY" while order.md has K-DRY-Q and K-DRY-P**, so one relay has a pre-split
name and a post-split name and a terminal id built on either is unstable; and
**?8 records that nothing in any file names the device that switches the chiller
receptacle**, so RUN-020's End A has no device to anchor a terminal on.

**FINDING 3. The class vocabulary has four buckets and the schedule needs five.**

Wire-table column 8 is "120 VAC / 24 V control / SELV signal / EGC", and it exists to
drive segregation and insulation rating. **RUN-001 and RUN-002 carry the driver motor
supply. It is at a control voltage and it is a POWER duty** - it is the conductor the
permissive removes, and F-047 establishes that four motor phase conductors chopping
current in one small sealed volume is where the coupled-noise premise is truest.

**Putting it in "24 V control" alongside RUN-005 to RUN-008 says those five may share
a duct, and G-30's whole reasoning is that duty separates, not voltage.** The bucket
sorts by voltage and the rule sorts by duty.

**Grade: CURRENT.** What would change it: one more class value, which is BOSS's since
column 8 is the wire table's. **I have marked the cells "24 V, POWER duty" rather
than choosing a bucket, so the disagreement is visible instead of resolved wrongly.**

**FINDING 4. Two runs in this schedule are SUPPLIED, and one of them is supplied into
a bundle the other class is already in.**

F-100 is with WATER and is not mine to solve. **What assigning ids added: the
"Cut / supplied / cord" column, filled in, shows that seven of twenty runs are not
cut by INTERCONNECT** - RUN-012, RUN-013, RUN-014, RUN-016 supplied, RUN-018,
RUN-019, RUN-020 cords. **D-090's cut rule reaches thirteen of twenty rows.** A cut
rule presented as covering the cable schedule covers under two thirds of it.

And the two facts land on one object: **RUN-012 is supplied cord that cannot be cut,
and RUN-019 and part of RUN-020 are 120 VAC cords, and D-121 puts all of them on the
same standpipe, tied at intervals, in the water.** The class column and the
provisioning column disagree about the same bundle - one says these are different
segregation groups, the other says neither can be re-terminated to separate them.

**FINDING 5. A run can be more valid than its own contents.**

RUN-007 and RUN-008 have interface rows and therefore exist. **Two conductors inside
them do not:** the D-042 dose-inhibit leg, which the ladder records at ?27 as having
no interface row while reaching the Pi, and S-20's second leg, which ?28 records as
built by order.md as a complementary pair while the row describes one pole and one
input.

**Wire-table column 10 says a conductor with no interface row does not exist.** So
these jackets are buildable in principle while some of their conductors cannot be
written down. **The shape work could not produce this because it never had to put a
conductor inside a named cable.**

**FINDING 6. Six of the twenty rows have no measured wall run, and they are the ones
that leave the wall.**

Filling the wall-run column: the five measured runs in parts.md are all
enclosure-to-enclosure. **RUN-010 to RUN-015 and RUN-018 to RUN-020 have no measured
figure**, and they are the runs that go to a tank, to a floor, to a console with no
position, or to the building supply - **that is, everything that leaves the 8 by 8
envelope.** The cut rule has a measurement basis for inter-enclosure runs and none
for field runs. **I state no length and none can be derived.**

---

## PART B. THE TERMINAL SCHEDULE

### B.1 The TRM- shape

**A terminal is identified by WHERE it is, ON WHAT it is, and WHICH one it is - three
parts, always three, in that order, joined by dots.**

```
TRM-<where>.<on what>.<which>
```

| Part | What it is | The rule it satisfies |
|---|---|---|
| **where** | The enclosure or field device the terminal is inside or on. **A closed set, written out, never computed** | channel-token.md forbidden item 4: sets are written out explicitly. Also item 7: no box-local numbering, because the box is IN the id rather than being the origin of a count |
| **on what** | The device or block the terminal belongs to, **BY NAME** | **G-28**: which relay goes in which socket is a build fact, labelled by name and never by position. **T-013**: names, never positions |
| **which** | **The marking as printed on the part.** Where nothing is printed, a descriptor in braces | **F-051**: the terminal block silk is a circled plus and a circled minus, not the words and not VM. A build sheet cannot quote a symbol, so that terminal is named by position and by what it does |

**The closed set for part one**, written out here and computed nowhere:
`MAIN-PANEL`, `PUMP-BOX-A`, `PUMP-BOX-B`, `DISPLAY-BOX`, and `FIELD` followed by the
device as the tree names it.

### B.2 The five rules the shape carries

**TRM-R1. Three parts, always. A two-part id is not a short form, it is a different
identity and is rejected.** channel-token.md forbidden item 10's shape: a carrier
that cannot hold the canonical form is a carrier defect, never solved by inventing a
short form at the wall. **If a wire marker cannot hold this, that is a carrier
question I return, and I have not pre-solved it by shortening the id.**

**TRM-R2. No part is a position, an index or an ordinal.** Not "the third terminal",
not "pole 2" where pole 2 is a count rather than a printed mark, not a socket number.
**Finding 2 in A.7 is what happens when this rule meets the tree as it stands.**

**TRM-R3. Part three is what is PRINTED. If nothing is printed, part three is a
descriptor in braces and the schedule's marking-source column says so.** A braced
descriptor never becomes a printed marking by being written down.

**TRM-R4. A digit may appear INSIDE part three and never as a whole part.**
channel-token.md forbidden item 5 forbids a bare digit that could be a channel, a
core or a terminal. **The tension is real: if a block's silk is literally "1", F-051
requires that mark and item 5 forbids a bare digit. The three-part form resolves it -
the digit never stands alone, because it always arrives with its enclosure and its
device.** `TRM-MAIN-PANEL.K-FILL-S.1` contains a digit; it is not a bare digit.

**TRM-R5. A TRM- id changes only when the PART changes.** It survives a relay moving
sockets, a cable being rerouted, a run splitting, and a channel being reassigned.
**It is never derived from a RUN- id and no RUN- id is derived from it.** No
arithmetic on either.

### B.3 The marking-source column, and why it is not optional

**F-051 is the whole reason this column exists.** Every file in the tree said VM; the
part carries a circled symbol. **So a marking quoted from a document is not a marking
read off a part, and the schedule must say which it has.**

| Value | Means |
|---|---|
| `PART` | Read off the physical part |
| `FILE` | Quoted from a tree document. **Provisional until somebody looks at the part** |
| `DESCRIBED` | Nothing is printed. Part three is a braced descriptor of position and function |

**Every row below is FILE or OPEN. Not one is PART, because no agent has been asked
to look at a terminal and report what is on it.**

### B.4 The schedule, applied as far as the tree allows

**This is short and it is supposed to be.** MAIN-PANEL's own file says terminal
numbers are assigned late, not now, and the ladder states it has no terminal number
in it anywhere. **I state none from memory or by derivation. What follows is what the
tree has already written down, carried into the shape.**

| TRM | Enclosure | Device, by name | Marking | Source | Conductors landed | Interface row | Status |
|---|---|---|---|---|---|---|---|
| `TRM-MAIN-PANEL.{driver permissive contactor}.{pole 1, motor supply out}` | MAIN-PANEL | **UNNAMED - A.7 finding 2** | `{pole 1}` | DESCRIBED | RUN-001 and RUN-002 both, **from one terminal downstream, parts.md** | P-06 | **BLOCKED: the device has no name.** And T-010 applies the moment two feeds come off one terminal - count clamps against conductors |
| `TRM-MAIN-PANEL.{driver permissive contactor}.{pole 2, readback}` | MAIN-PANEL | **UNNAMED - A.7 finding 2** | `{pole 2}` | DESCRIBED | RUN-006 | S-08 | **BLOCKED: the device has no name.** Also ?26 - if that contactor's poles share one contact volume, S-08 violates G-30 and has nowhere to move |
| `TRM-MAIN-PANEL.K-FILL-S.{solenoid pole}` | MAIN-PANEL | **K-FILL-S**, order.md envelope map | `{solenoid pole}` | DESCRIBED | RUN-011 | **P-02** | **BLOCKED: P-02 OPEN and stale, F-098.** The pole is sized on the make-and-break event, ?5 |
| `TRM-MAIN-PANEL.K-FILL-D-Q.{S-03 changeover}` | MAIN-PANEL | **K-FILL-D-Q**, order.md | `{S-03 / D-042 changeover pair}` | DESCRIBED | RUN-007 | S-03, **and ?27's rowless leg** | **BLOCKED: no marking, and one landed conductor has no interface row** |
| `TRM-MAIN-PANEL.K-DRY-Q.{Pi pair}` | MAIN-PANEL | **K-DRY-Q**, order.md - **but S-20 calls the relay K-DRY**, A.7 finding 2 | `{G-27 complementary pair}` | DESCRIBED | RUN-008 | S-20, **and ?28** | **BLOCKED: S-20 OPEN, name unstable, row and order.md disagree on how many legs** |
| `TRM-MAIN-PANEL.{ground bar}.{...}` | MAIN-PANEL | **{ground bar}** - order.md lists it as not covered | OPEN | OPEN | RUN-017, provisionally | **CBL-07** | **BLOCKED: CBL-07 OPEN, the bar is not bought, and RUN-017 is one id for an unknown number of runs** |
| `TRM-FIELD.{fill solenoid}.{coil lead}` | FIELD | The fill solenoid, specified by D-136 | OPEN | **OPEN** | RUN-011 | **P-02** | **BLOCKED: coil lead identification has never been looked up.** wire-table-row-zero.md's CDR-001 says the same and names the standard: per F-051 it is named by what is printed on the part, and nobody has looked |
| `TRM-PUMP-BOX-A.{driver}.{...}` | PUMP-BOX-A | OPEN | OPEN | OPEN | RUN-001, RUN-003 | P-06, S-10, P-09 | **BLOCKED: S-10 and P-06 OPEN. The pin list is known and the terminal MARKINGS are not** - parts.md warns the flat pin list is a list of NAMES read as an order, F-058, and the board is two connectors |
| `TRM-DISPLAY-BOX.{logic board}.{...}` | DISPLAY-BOX | OPEN - the logic board is hand built and has no terminals yet | OPEN | OPEN | RUN-003 to RUN-009, RUN-016 | S-07, S-08, S-03, S-20, S-10, S-11, P-07 | **BLOCKED: S-12 is not frozen and the board does not exist** |

**Nine rows, none buildable.** That is the honest state and it is the same shape as
the cable schedule: **the identities can be written today and not one value can.**

### B.5 What the terminal schedule can already do that nothing else can

Even blocked, it holds two checks nothing else in the tree can hold:

1. **T-009 and T-010.** The first row above already shows two runs coming off one
   terminal downstream of the contactor pole. **A terminal carrying exactly one
   conductor is an open circuit, not a spare; and clamps are counted against
   conductors, not assumed.** Neither question is answerable from a cable schedule or
   a wire table, because both of those are organised by a conductor's journey and
   this one is organised by its destination.
2. **F-051 in force.** The marking-source column makes "the file said so" visibly
   different from "the part says so", which is the exact distinction that made VM
   wrong in every file in the tree.

---

## PART C. WHAT IS DUPLICATED BETWEEN THE TWO SCHEDULES, AND WHAT MUST NEVER BE

There are **three** artifacts, not two. The wire table already exists in schema form
in wire-table-row-zero.md and both schedules join to it.

| Artifact | Row unit | Key |
|---|---|---|
| Cable schedule, this file | one jacket | **RUN-nnn** |
| Wire table, wire-table-row-zero.md | one conductor | **CDR-nnn** |
| Terminal schedule, this file | one landing point | **TRM-** |

### C.1 Duplicated ON PURPOSE, because it is the join

**Every one of these is an EQUALITY a check can fail, not a copy that can drift.**
T-012: derive it, or make the check an identity rather than a bound - a bound passes
while the number drifts, an identity fails the moment two sides disagree.

- Every wire-table row's **Cable** value **is** a RUN- id in the cable schedule.
- Every wire-table row's **From: terminal** and **To: terminal** **are** TRM- ids in
  the terminal schedule.
- Every terminal-schedule row's **Conductors landed** **are** CDR- ids in the wire
  table, and their count **is** the clamp count. T-010.
- Every cable-schedule row's **Interface rows realised** **is** the union of the
  interface rows of its conductors. **Computed, never typed.**
- Endpoint device names appear in both schedules and **are** the same string, taken
  from the interface table.

**The four exceptions to the last rule, and they are the reason it is checkable at
all:** RUN-018 to RUN-020 have no CDR- children by construction, A.6; and RUN-017's
child set has an unknown size until CBL-07 resolves.

### C.2 MUST NEVER be duplicated

| What | Where it lives, once | Why duplicating it is the defect |
|---|---|---|
| **Length and cut length** | Nowhere as a stored value. Computed at the cut step from D-090 | **T-020, and F-099 is the live instance**: parts.md already carries the same five figures under two contradictory allowance rules. A cut cable cannot be un-cut |
| **Gauge, core count, colour, part number** | The owner's lookup. The cable schedule's core requirement is DERIVED by counting CDR- rows | **T-008: count landings, never the jacket.** wire-table-row-zero.md excludes these for the same reason |
| **The per-channel core identity** | **channel-register.md, once, under D-057.** Its Cable core column is empty and waiting for INTERCONNECT | channel-token.md forbidden item 1. **"CH3's core is Y" is the correct shape; "core 7 = CH3" is forbidden**, because its existence proves the core has an identity of its own. Neither schedule restates it |
| **Fail behaviour on a severed conductor** | **Wire table column 11, per conductor** | **F-017.** It is a conductor property. A cable-level fail behaviour is an average of several, and averaging is how S-03 inherited its direction from S-08 once already |
| **Design current and which event** | **Wire table column 9, per conductor** | D-136: a relay contact makes and breaks the inrush. **A cable-level current has no event attached to it, and the event is the whole point** |
| **The class** | **Wire table column 8, derived from the interface row.** The cable schedule's class column is the ROLL-UP and is computed | If both are typed they can disagree, and the thing that disagrees is what decides insulation and segregation |
| **What a signal MEANS** | The interface row | INTERCONNECT's out-of-scope line. Applying an identity is not interpreting a meaning; restating a meaning is |
| **A terminal's marking** | **The terminal schedule, once, with its source** | F-051. A marking copied into a cable schedule loses the PART / FILE / DESCRIBED distinction, and that distinction is the finding |

---

## PART D. REQUIREMENTS AND SEARCH TERMS

No value below is stated. Each is a lookup the owner runs under G-15.

| For | Requirement | Search term |
|---|---|---|
| RUN-011, RUN-015, RUN-018 to RUN-020 | A flexible 120 VAC cable for a wall route in a room where water moves tank to tank, with an equipment grounding conductor, rated for the make-and-break event of an inductive coil load | `flexible power cable 600 V oil resistant wet location`; `tray cable TC-ER exposed run wall` |
| RUN-012, RUN-013 | A control cable for a dry-contact pilot circuit at whichever voltage class ?12 settles, on a route that includes a wet zone | `instrumentation control cable 300 V vs 600 V dry contact multiconductor` |
| RUN-015 | Confirmation that every conductor in one jacket may share the higher insulation rating CBL-06 requires | `600 V insulated conductor mixed circuit same raceway control cable` |
| RUN-016 | The maximum probe cable length the EZO circuits tolerate. **Not from any file in this tree** | `Atlas Scientific EZO pH EC probe cable length limit extension` |
| Every entry | A cord grip per entry, sized to the cable actually chosen, sealed at least to the enclosure's own rating and suitable for the face it lands on under F-088 | `liquid tight cord grip strain relief NPT cable range chart` |
| The segregation rule | A stated rule for which classes may share a duct, a jacket, a clip run or a tie bundle, what an unavoidable crossing requires, and what the standpipe bundle requires | `control panel power and signal circuit segregation separation barrier`; `Class 1 Class 2 circuits same raceway` |
| Labelling | A marker carrier that holds the canonical three-part TRM- form and the channel token in addition, without merging them | `wire marker sleeve character capacity heat shrink printable` |

---

## PART E. STATUS

**Stopped part way and I do not declare myself finished**, rule 7.

**Returned:** 20 RUN- ids assigned and both schedules written as documents; the TRM-
shape with five rules; nine terminal rows applied as far as the tree allows; the
duplication contract across three artifacts; six findings that only appeared once the
ids were real.

**NOT returned, so the absence is not read as an answer:**

- **No wall layout.** M-02 is open and Z5 is undefined, F-067. Every "where on the
  face" cell and every unmeasured wall run waits on it.
- **No answer to the monotone CH1 to CH8 question** in channel-token.md. Not a no, an
  unanswered, for the same reason.
- **No gland count, spacing, position, cable selection, core count, cut length or
  terminal number.** Rule 3 and G-15. Each is a requirement in Part D.
- **No enclosure owner has yet been asked for faces under D-146.** MAIN-PANEL's are
  on file in parts.md and I have used them. **PUMP-BOXES and DISPLAY-BOX have stated
  none, and I am not reporting the D-146 escape-clause finding against either of
  them, because neither has been asked and refused.** Assert nothing from absence.

**What unblocks the most, in order:** PUMP-BOXES and DISPLAY-BOX stating faces and
order under D-146, which fills sixteen cells and costs them nothing; BOSS ruling
whether RUN- means a jacket and what happens to an id that splits, A.1; the one
sentence ?12 asks for on the permissive string's voltage class, which decides
RUN-012, RUN-013 and RUN-015 together; and the S-07 / S-09 merge, without which
RUN-005 cannot have a wire-table row at all.
