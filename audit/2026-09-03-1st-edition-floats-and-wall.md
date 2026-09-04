# 1st Edition set: float selection and placement, and the wall arrangement

**QUESTIONS FORMED FROM A PREVIOUS BUILD. NOT A SOURCE. NOT EVIDENCE. NOT A RECOMMENDATION.**

---

## The owner's caveat, verbatim, and it governs every line below

> "NOTHING IN IT IS AUTHORITATIVE. Not one figure, not one part, not one decision.
> It is a previous attempt at the same problem, built before most of what you and
> the parallel effort have established, and it contains errors that took thirty
> sessions to find in the other build. Treat it as LOOSE GUIDELINE ONLY. Every
> figure in it is a candidate for T-018 - assume seeded until traced. Every part
> in it may have been superseded, returned, or never bought. Every impossibility
> claim in it is ungraded. Where it disagrees with your tree, YOUR TREE WINS
> unless I say otherwise. Do not cite it as a source for anything. If it
> contradicts a frozen row, that is a finding about the old set, not about the
> row."

And the owner's instruction on what this file is for:

> "Use it to form the QUESTIONS, not the answers. [...] I will answer against the
> current design rather than against the old one. That is the right use of it: it
> turns two blank questions into two questions with a starting proposal, and I am
> a much faster confirmer than I am an originator. Do not treat anything you find
> there about floats or layout as decided."

**Nothing in this file may be cited by any subsystem. It is a question list. No
row here becomes a fact until the owner marks it CONFIRMED, and a CONFIRMED row
is then owned by WATER or INTERCONNECT and re-derived by them, not inherited from
here.**

---

## What was read, and what was skipped

**Read in full:**

| Document | Why |
|---|---|
| `handoff/STATE-OF-PROJECT.md` | Carries the old set's own float map and its own list of what it knew was wrong |
| `handoff/DRAWING-METHODOLOGY.md` | Carries the panel plate coordinate system and the clamp convention |
| `main/float-standpipe-assembly-1st-edition.pdf` (1 p) | The primary float mounting document |
| `addon/storage-standpipe-1st-edition.pdf` (1 p) | The storage tank float set |
| `main/dosing-wall-1st-edition.pdf` (1 p) | The primary wall document |
| `main/plotter-sheet-1st-edition.pdf` (1 p) | General arrangement plus the whole ladder and the float wiring table |
| `addon/storage-autofill-1st-edition.pdf` (1 p) | The storage fill logic and the fill valve |
| `addon/storage-autofill-buylist-1st-edition.pdf` (1 p) | Add-on parts and the fill commissioning sequence |
| `main/fertigation-build-book-1st-edition.pdf` (15 pp, all) | Sheets 8, 9, 10, 11, 13 and 14 are the wall and float content; 1-7 read for context |

**Skipped deliberately, with the reason:**

- `panel-wiring-instructions` (67 pp), `storage-autofill-wiring` (16 pp),
  `receptacle-wiring-instructions` (12 pp) and the three one-page wire schedules.
  These are one-wire-per-page routing sheets for an enclosure the current tree
  does not have. They carry no float placement and no wall arrangement.
- `panel-wiring-schematic`, `panel-physical-wiring`, `receptacle-schematic`.
  Same reason. The ladder they draw is fully readable off the plotter sheet and
  build book sheet 6, which were read.
- `commissioning-checklist` (9 pp), `maintenance-log` (5 pp),
  `fertigation-purchase-package.xlsx`. Out of the two assigned areas.
- `handoff/1st-edition-generators.zip`. Not opened.

**Read in the current tree first, to have something to disagree with:**
`agents.md` (rules 1-11), `decisions.md` (the G-rule table, D-090, D-108 to
D-114), `interface-table.md` (all rows), `subsystems/water.md`,
`subsystems/interconnect.md`, `parts.md` (the wall and float sections), `traps.md`
T-018.

---

## How to read every numbered item

Each item is a PROPOSAL TO CONFIRM OR REPLACE. None is a finding about the
current design. The shape is fixed:

> **A-nn.** The old set appears to show X. *Observed in the 1st Edition set,
> unverified. Confirm or replace.*

Reply per item with CONFIRM, REPLACE-WITH, or NO POSITION YET. A CONFIRM is the
owner making a decision, not the old set being promoted.

**Counts: 24 proposals on floats (A-01 to A-24). 26 proposals on the wall (B-01
to B-26).**

---

# A. FLOATS

## A.1 What a standpipe assembly is, and why it exists

**A-01.** The old set appears to show that every float in a tank is carried on ONE
RIGID PIPE per tank, called a standpipe, and not hung from its own cord. The pipe
is 3/4 in Sch 80 PVC with a solvent-welded end cap on the bottom. Its stated
purpose: *"The bracket carries the pipe, the floats and every cord. Nothing hangs
off a float body and nothing rests on the tank floor."* *Observed in the 1st
Edition set, unverified. Confirm or replace.*

**A-02.** The old set appears to show the standpipe hung from the tank's rim by a
2 in ID U-bolt with a backing plate, 316 stainless, nuts underneath, two nyloc
nuts hand tight plus a quarter turn, with the instruction *"Do not crush the lip.
Snug is enough."* The pipe sits inside the U-bolt and is set so the end cap hangs
clear of the tank floor. *Observed in the 1st Edition set, unverified. Confirm or
replace.*

**A-03.** The old set appears to show the build order as: fit the bracket FIRST,
then set float heights against the standpipe. Mark every trip height on the pipe
with a paint pen BEFORE anything goes in the tank. *Observed in the 1st Edition
set, unverified. Confirm or replace.*

**A-04.** The old set appears to show every float cord running UP the pipe, tied
every 6 in, over the rim, and out through a cord grip with the drip loop OUTSIDE
the enclosure, with *"No slack loops inside the tank."* *Observed in the 1st
Edition set, unverified. Confirm or replace.*

## A.2 Float type and how one is mounted

**A-05.** The old set appears to use ONE float type for every position in the
system: a tethered SPDT float switch on a 20 ft cord, pilot duty, rated at the
control voltage, with an EXTERNAL CABLE WEIGHT clamped on the cord. *Observed in
the 1st Edition set, unverified. Confirm or replace.*

**A-06.** The old set appears to hold, as a build rule, that **NOTHING GETS
FLIPPED. All floats mount the same way. NO or NC is chosen at the terminal strip,
not by inverting the float.** *Observed in the 1st Edition set, unverified.
Confirm or replace.*

**A-07.** The old set appears to show the trip height as **the position of the
WEIGHT, not the position of the float body**: *"The trip height is where the
WEIGHT sits, not where the float sits. [...] The weight is the pivot. The float
swings from it."* The weight is clamped on its paint-pen mark with a cable tie,
and that tie IS the trip height. *Observed in the 1st Edition set, unverified.
Confirm or replace.*

**A-08.** The old set appears to set the SWITCHING DIFFERENTIAL by tether length:
a stated 3 in of tether below the weight gives a narrow angle and a stated 1.5 in
differential, with one float shortened to 2 in of tether because it has only 1 in
of freeboard above it. *Observed in the 1st Edition set, unverified. Confirm or
replace.*

**A-09.** The old set appears to hold that adjustment after install is made at the
CABLE TIE and never at the wiring: *"Fill the tank slowly and confirm each one
trips. Adjust the tie, never the wiring."* *Observed in the 1st Edition set,
unverified. Confirm or replace.*

## A.3 How many floats, which tank, and what each one switches

**A-10.** The old set appears to run EIGHT floats total, FOUR per tank, in two
packages: five in the main package (four day tank plus one storage) and three
added by a storage auto-fill add-on. *Observed in the 1st Edition set, unverified.
Confirm or replace.*

**A-11.** DAY TANK, four floats on a 30 in standpipe. The old set appears to show:

| Tag | Role | Trip | Wired | What it does |
|---|---|---|---|---|
| LS-2 | high-high / overfill fault | 32 in | NC | Drops the master permissive latch. Hardware backstop |
| LS-5 | fill stop | 30 in | NC | Opens at level, drops the fill latch, ends the fill |
| LS-1 | fill start | 11 in | NC | Closes below level, calls for a fill |
| LS-4 | low-low / dry-run stop | 8 in | NO | Closed above level. Drops the dry-run interlock relay |

*Observed in the 1st Edition set, unverified. Confirm or replace, per row.*

**A-12.** STORAGE TANK, four floats on an 80 in standpipe. The old set appears to
show:

| Tag | Role | Trip | Wired | What it does |
|---|---|---|---|---|
| LS-8 | storage high-high | 72 in | NC | Drops the master permissive. In series with LS-2 |
| LS-7 | storage fill stop | 66 in | NC | Opens at level, drops the storage fill latch |
| LS-6 | storage fill start | 30 in | NC | Closes at level, pulls in the storage fill latch |
| LS-3 | storage low | 20 in **or** 27 in | NO | Closed while storage has water. Stops the transfer pump running dry |

**LS-3's trip height appears TWICE in the old set at two different values.** See
flag 2 and the internal-contradiction list. *Observed in the 1st Edition set,
unverified. Confirm or replace, per row.*

**A-13.** The old set appears to hold that floats switch RELAY COILS ONLY and
never a pump load directly. *Observed in the 1st Edition set, unverified. Confirm
or replace.*

## A.4 The level bands, as bands rather than as heights

**A-14.** The old set appears to define the DAY TANK working band as fill start to
fill stop, a stated 19 in, described as one refill. The high-high sits a stated
2 in above the fill stop and is called the hardware backup: *"If it ever gets wet,
LS-5 or its wiring has failed."* *Observed in the 1st Edition set, unverified.
Confirm or replace.*

**A-15.** The old set appears to place the day tank low-low at the **pump-top
minimum** - the height of the top of the pump intakes - rather than at a chosen
volume, and states the residual volume left below it as a consequence, not as the
target. *Observed in the 1st Edition set, unverified. Confirm or replace.*

**A-16.** The old set appears to define the STORAGE working band as fill start to
fill stop, a stated 36 in, and calls it *"the long clear run"* between them, with
the high-high a stated 6 in above the fill stop. *Observed in the 1st Edition set,
unverified. Confirm or replace.*

**A-17.** The old set appears to order the storage floats top to bottom as
high-high, fill stop, [long clear run], fill start, storage low. *Observed in the
1st Edition set, unverified. Confirm or replace.*

## A.5 The fill and transfer logic the floats drive

**A-18.** DAY TANK FILL. The old set appears to run: master permissive latched →
fill start (closes) → fill stop (NC, opens at the top) → fill latch relay, with a
SEAL-IN contact of the fill latch bridged ACROSS the fill start float, so once the
fill starts the seal holds it until the fill stop opens. A pole of that same fill
latch relay switches the transfer pump. *Observed in the 1st Edition set,
unverified. Confirm or replace.*

**A-19.** STORAGE FILL. The old set appears to run the identical shape one level
up: master permissive tap → fill start (NC, low) → fill stop (NC, opens when full)
→ a second fill latch relay, sealed across the fill start, with a pole of that
relay energising the fill valve. Its own words: *"mirrors the day tank fill."*
*Observed in the 1st Edition set, unverified. Confirm or replace.*

**A-20.** THE MASTER PERMISSIVE STRING. The old set appears to put, in one series
string: E-stop (NC) → leak detector dry contact (NC) → day tank high-high (NC) →
storage high-high (NC) → storage low (NO) → reset button → master latch relay,
with the master relay sealing itself in through its own contact so *"any fault
drops it and it STAYS down"* and a manual reset is required. *Observed in the 1st
Edition set, unverified. Confirm or replace.*

**A-21.** The old set appears to put **STORAGE LOW into the MASTER PERMISSIVE
STRING**, so an empty storage tank drops everything, not only the transfer pump.
Its stated reason: *"It drops the master permissive so the transfer pump cannot
run the storage tank dry."* *Observed in the 1st Edition set, unverified. Confirm
or replace.* **The current tree has no position on whether storage-low is a local
interlock or a master fault.**

**A-22.** DRY-RUN. The old set appears to use the day tank LOW-LOW FLOAT - a LEVEL
element - as the dry-run interlock, driving a dedicated relay whose poles switch
the manifold pump and the chiller loop. Its stated reason for keeping that
relay out of the master latch: *"Dry-run protection must work whether or not
anyone has pressed reset."* *Observed in the 1st Edition set, unverified. Confirm
or replace.* **See flag 1, item C-06: this is the exact choice S-05 is being held
open to avoid foreclosing.**

**A-23.** The old set appears to run the fill commissioning as: lift each float by
hand and confirm the relay picks up or drops; then fill the tank slowly with a
hose and watch each float trip at its mark; then adjust the clamp. It also appears
to require a POWER-KILL TEST on the fill valve - *"Power the panel, then kill it.
The valve must spring shut on its own"* - before the first unattended fill.
*Observed in the 1st Edition set, unverified. Confirm or replace.*

**A-24.** The old set appears to state a MEASUREMENT DATUM for every float height,
and appears to state two different ones in two places: *"heights off the END CAP
FACE, not the pipe end"* on the standpipe sheets, and *"all dimensions off the
TANK FLOOR"* on the build book float sheet, with the same numbers under both. The
two datums are separated by the end cap's stated clearance above the floor.
*Observed in the 1st Edition set, unverified.* **The proposal to confirm or
replace is not a number: it is that THERE MUST BE ONE NAMED DATUM and every level
figure in the tree carries it.**

---

# B. THE WALL

## B.1 The board itself

**B-01.** The old set appears to mount everything on ONE sheet of 1/2 in HDPE
board, stated as 72 in (6 ft) wide by 44 in tall, with its bottom edge a stated
40 in off the floor. *Observed in the 1st Edition set, unverified. Confirm or
replace.* **This disagrees with D-090. See flag 1, item C-01.**

**B-02.** The old set appears to divide that board into two named horizontal
zones: a DOSING ZONE occupying the left ~72% of the width and a CONTROL ZONE
occupying the right ~28%, with the enclosure and the receptacles in the control
zone and the pumps, manifold, raceway and containers in the dosing zone. *Observed
in the 1st Edition set, unverified. Confirm or replace.* **The current tree has no
zoning concept for the wall at all.**

**B-03.** The old set appears to hold that the board is the mounting substrate for
BOTH the enclosure and the field devices, fixed with pan head screws directly into
the HDPE, with the caution *"Do not over-torque; HDPE strips easily."* *Observed
in the 1st Edition set, unverified. Confirm or replace.*

## B.2 What is above what: the vertical stack

**B-04.** The old set appears to stack the dosing zone in five bands, top to
bottom, in this order:

1. **Pump modules**, surface mounted, daisy-chained, along the top edge
2. **Tubing raceway** - one slotted duct with a lid, immediately below the pumps
3. **Injection manifold** - horizontal, ports tapping the TOP of the run
4. **Container shelf** for the small bottles
5. **Containers and drip tray** at the bottom, on a floor rack

*Observed in the 1st Edition set, unverified. Confirm or replace.* **The order is
the proposal. The distances between the bands are separate figures - see flag 2.**

**B-05.** The old set appears to state a reason for the pump row being at the top
and a clearance under it: *"Leave 4 in clear below each head to change tubing."*
*Observed in the 1st Edition set, unverified. Confirm or replace.*

**B-06.** The old set appears to state THE governing vertical rule of the whole
wall: **every liquid level in every container stays BELOW the manifold**, with the
stated reason *"A failed tube then cannot siphon a container into the tank."*
*Observed in the 1st Edition set, unverified. Confirm or replace.* **This is a
rule keyed to a ROLE and a RELATION, not to a dimension, which is the shape G-34
prefers.**

**B-07.** The old set appears to treat SUCTION LIFT - the vertical distance from
each container's liquid surface up to the pump heads - as a wall-layout output,
and tabulates it per shelf position, measured to the heads at a stated height off
the floor. *Observed in the 1st Edition set, unverified. Confirm or replace.*
**The current tree has no position on suction lift as a placement driver.**

## B.3 The tubing route

**B-08.** The old set appears to route ALL dosing tubes into ONE raceway, and to
forbid point-to-point runs: *"Tubing routed in a raceway, not point to point."*
Every tube drops into the raceway, runs to one end into a single bundle, then back
across, and *"Tubes only leave at their own port or container."* *Observed in the
1st Edition set, unverified. Confirm or replace.*

**B-09.** The old set appears to run the discharge branches and the suction
branches in the SAME raceway, distinguished only by which direction they leave it.
*Observed in the 1st Edition set, unverified. Confirm or replace.*

**B-10.** The old set appears to hold the manifold port ORDER as fixed by
chemistry and not by layout convenience, with an explicit prohibition on
rearranging it. *Observed in the 1st Edition set, unverified. Confirm or replace.*
**Under the current tree the port-to-channel relation is S-19's, CONTROL-SOFTWARE
declares it, and the old set's port order was built for six channels, not eight.**

**B-11.** The old set appears to run the wet loop as a rectangle on the board: up
the right side through the probe glands, across the top through the injectors,
down the left side, and back to the tank - a stated loop span, a stated left leg,
a stated right leg, and injector tees on even centres. *Observed in the 1st
Edition set, unverified. Confirm or replace.*

**B-12.** The old set appears to place BOTH probes on the right-hand riser, one
above the other, upstream of every injection port, with a bypass leg outboard of
them and isolation valves either side so the whole gland section lifts out as one
piece. *Observed in the 1st Edition set, unverified. Confirm or replace.*
**The upstream-of-every-port half agrees with G-10; the vertical-section half
agrees with G-10's wording. This is not corroboration of G-10 - G-10 is the
source and this document is not.**

## B.4 The enclosure and the operator's face

**B-13.** The old set appears to mount ONE enclosure, portrait, in the control
zone at the top right of the board, with its interior drawn to scale against a
real backplate. *Observed in the 1st Edition set, unverified. Confirm or replace.*
**The current tree has FOUR enclosures. See flag 1, item C-02.**

**B-14.** The old set appears to put the E-STOP, the RESET button and three pilot
lights on the enclosure's TOP FACE, and nothing else. *Observed in the 1st Edition
set, unverified. Confirm or replace.* **This is the same arrangement D-048 and
S-06 already closed. It is NOT a second source for D-048 under G-37 - D-048 stands
on its own and this document adds nothing to it.**

**B-15.** The old set appears to mount three pilot lights - filling, fault, ready
- driven from relay poles, on that top face. *Observed in the 1st Edition set,
unverified. Confirm or replace.* **decisions.md already routes "three lamps driven
from relay poles is a claim on the pole budget" to MAIN-PANEL as an open item.
This is not an answer to it.**

## B.5 Cable routes on the wall

**B-16.** The old set appears to hold that ALL cord grips are on the enclosure's
BOTTOM FACE ONLY - *"never the top or the sides"* - with a drip loop OUTSIDE the
box on every one. *Observed in the 1st Edition set, unverified. Confirm or
replace.* **CBL-01 to CBL-04 are open on exactly this and the current tree has no
position on which face.**

**B-17.** The old set appears to route power cables in one shape: each cable
leaves its grip on the bottom face, drops to a COMMON HORIZONTAL RUN at a stated
height, goes level to the device's position, then drops in. Not point to point.
*Observed in the 1st Edition set, unverified. Confirm or replace.*

**B-18.** The old set appears to fix cables with nylon P-clips at stated spacings,
one spacing for vertical drops and a wider one for level runs. *Observed in the
1st Edition set, unverified. Confirm or replace.*

**B-19.** The old set appears to leave a SERVICE LOOP at every termination, sized
by what the loop has to let you do: a short loop at each receptacle *"so the box
can be pulled off the board without disturbing the cable"*, and a longer one at
each probe gland *"so the probe backs out to a sink without unplugging"* the
controller. *Observed in the 1st Edition set, unverified. Confirm or replace.*
**parts.md's cut-length rule already adds a fixed allowance per end; the old set
sizes the loop by the SERVICE ACTION instead. Those are different rules and both
are stated as figures.**

**B-20.** The old set appears to run PROBE CABLES IN THEIR OWN DUCT with an
explicit prohibition: *"Probe cables never share a duct or a conduit with 120 V.
Not the float cable either."* Where a crossing is unavoidable it appears to
require crossing at 90 degrees. *Observed in the 1st Edition set, unverified.
Confirm or replace.* **INTERCONNECT owns "separation of the 120 V pump and chiller
runs from step and direction and from probe cables" as an OPEN item and the tree
has no rule yet.**

**B-21.** The old set appears to state the FAILURE MODE that separation rule
exists to prevent, in observable terms: *"a pH number that jumps when a pump
starts, or a reading that drifts with no chemistry change."* *Observed in the 1st
Edition set, unverified. Confirm or replace.* **The current tree has no named
symptom for probe cable noise. If confirmed this is a commissioning observable,
not a wiring rule.**

**B-22.** The old set appears to hold that the enclosure body is NOT a bonding
path and that every ground lands on a dedicated ground terminal group inside it.
*Observed in the 1st Edition set, unverified. Confirm or replace.* **CBL-07 says
the same thing about the display box and the pump boxes, and CBL-07 is the source.
This is not corroboration.**

**B-23.** The old set appears to hold a clamp convention as a labelling rule on
every wire: internal panel wires land on one clamp face of a terminal, field
cables coming up from the grips land on the other, and every wire descriptor names
which. *Observed in the 1st Edition set, unverified. Confirm or replace.*

## B.6 The floor in front of the wall

**B-24.** The old set appears to allocate FLOOR footprint as part of the wall
drawing, not separately: a container rack of stated width and depth, the day tank
of stated diameter beside it, and a stated clear gap. *Observed in the 1st Edition
set, unverified. Confirm or replace.* **The current tree treats the wall as an 8 x
8 envelope and has no position on the floor in front of it.**

**B-25.** The old set appears to state that the tank, the manifold pump and the
probe glands *"sit on the floor below this board"*, so the wall carries no wet
vessel weight. *Observed in the 1st Edition set, unverified. Confirm or replace.*

**B-26.** The old set appears to place the CHILLER outside the room entirely, with
a stated reason: *"It rejects heat into the room"*, and a stated wattage.
*Observed in the 1st Edition set, unverified. Confirm or replace.* **The current
tree's site conditions state a room temperature band and D-108 makes the chiller
self-contained, but nothing states where it physically stands.**

---

# FLAG 1. WHERE THE OLD SET CONTRADICTS THE CURRENT TREE

**In every row below, THE TREE WINS. Each row is a finding about the old set, not
about the row it disagrees with.** These are listed so that no proposal above is
read as a challenge.

| # | The old set appears to say | The tree says | Verdict |
|---|---|---|---|
| **C-01** | The wall is a 72 in x 44 in board, bottom edge 40 in off the floor | **D-090: the wall is 8 ft by 8 ft.** That is the layout envelope and Z5, M-02 and the station run are consequences of placement inside it | **D-090 wins.** The old set's board is smaller than the current envelope in both directions. Any spacing figure derived from a 72 in width does not transfer |
| **C-02** | One enclosure, plus four separate receptacle boxes cabled to it | **INTERCONNECT's frozen "Physical shape" row: four enclosures - main panel, two pump boxes on the dosing wall, one display box.** Enclosure is 20.7 x 16.6 in per decisions.md | **The tree wins.** The old set's wall arrangement is an arrangement of a different set of objects. Its band order (B-04) may survive; its object placement cannot |
| **C-03** | Receptacles are separate weatherproof boxes on the wall, on their own cables from the enclosure, at stated left-edge positions | **D-046: receptacles are PANEL MOUNTED in the enclosure face and cords plug in from OUTSIDE. Cords are not fed through grips.** P-03 and P-04 | **D-046 wins.** The old set's entire receptacle mounting sheet - positions, spacing, cable cut list, P-clip run - describes a topology D-046 removed |
| **C-04** | The fill valve is a motorized ball valve, 2-wire, claimed spring return, claimed fails closed | **D-114 / G-39: THE FILL VALVE IS A SOLENOID. Energise to open, spring closed on power loss.** D-111 is reversed and everything it said about a motorized valve is WITHDRAWN | **D-114 wins, and it is not close.** See the note below this table - the old set's variant is worth one sentence to the owner and no more |
| **C-05** | All relay coils are 120 VAC and the floats are chosen and rated to switch a 120 VAC coil at a stated amperage | **The panel's control voltage is 24 V.** P-08 (24 V supply to relay and contactor coils), S-03 (wetted at 24 V), S-08 (wetted from 24 V) | **The tree wins, and this is the one that bites on FLOATS.** A float chosen for a 120 VAC coil is a different duty from a float switching 24 V. **G-31 applies: a minimum switching load is one POWER requirement, and dropping from 120 V to 24 V drops the power at the contact by a factor of five at the same current.** Any float part inherited from the old set arrives sized against the wrong coil |
| **C-06** | Dry-run protection is a LEVEL element - the day tank low-low float - driving a dedicated interlock relay | **S-05 is OPEN AND DELIBERATELY HELD.** WATER holds it open because *"a LEVEL element can NEVER subsume circulation verification"* and *"choosing a level-based answer here forecloses the shared solution"* | **The tree wins and this is the most dangerous single item in the old set.** A-22 above states what the old set did. **It must not be read as a proposal to close S-05.** If the owner confirms A-22 he is spending D-060's real price knowingly; if it slides through as "the old set already did it" the door closes with nobody deciding to close it. T-023 |
| **C-07** | Six live dosing channels plus two spare, six injector ports on the manifold | **Eight channels, CH1 to CH8, eight heads, eight drivers.** S-19, D-021, D-105 | **The tree wins.** Every port spacing, every raceway tube count and the whole "12 tubes" figure in the old set is built on six |
| **C-08** | The chiller ships with an external submersible pump and both are switched together by a relay pole feeding one receptacle | **D-108: the chiller is entirely self-contained, there is no chiller contactor. F-086 is OPEN: nothing on file states what switches the loop pump, and BOSS has NOT chosen between four possibilities** | **The tree wins, and F-086 stays open.** The old set contains something that looks like an answer to F-086. **It is not one.** water.md says explicitly: *"Do not design around any of the four."* Recording it here as an observation is the limit of what may be done with it |
| **C-09** | The storage tank has ONE float in the base package; the start/stop pair is an add-on bolted on later | **G-03: storage AND day tank fill use a start float and a stop float with relay seal-in between them** | **G-03 wins.** The storage start/stop pair is a baseline requirement here, not an add-on. This is a difference in STATUS, not in arrangement - the old set's storage pair, once added, matches G-03's shape |
| **C-10** | The transfer pump load and a pilot lamp share one relay; the manifold pump and the chiller share another | **G-30: DUTY IS SEPARATED BY RELAY, NOT BY CONTACT MATERIAL. A power pole and a sense pole never share a relay.** G-24 asks the minimum-switching-load question of lamp poles too | **G-30 wins.** Noted only because the float chains land on these relays; the relay allocation itself is MAIN-PANEL's and outside this pass |

### The one nuance worth one sentence, and no more

The old set's motorized ball valve is specified as **spring return, normally
closed, fails closed on power loss** - so the old set did not choose a hold-last
valve. **This changes nothing.** D-114 also rejected the motorized valve on
TRAVEL TIME, and that half stands independently: *"the float that stops the fill
is the only thing stopping it, so several seconds of travel puts an unmeasured
volume past the switching point every time."* **The valve is a solenoid. The only
reason to mention the old set's variant at all is so the owner is not later
surprised to find the word "motorized" attached to a fail-closed claim and wonder
whether D-114 examined the right part.**

---

# FLAG 2. EVERY FIGURE IS A T-018 CANDIDATE

**Blanket marking, and it applies to every number in this file without exception:
ASSUME SEEDED UNTIL TRACED.** T-018's test is *"did this come from the world, or
from a file that had to contain something."* Not one figure below has been traced
to a measurement, a datasheet or a tank in a room.

## 2.1 Why the float figures in particular are suspect

Three independent reasons, before any single number is examined:

1. **The old set's own handoff notes admit a recurring failure of exactly this
   class**: *"Cross-document stale values [...] several sheets still carried the
   old scheme in their prose and tables [...] 'four float switches', the old
   terminal count [...] This class recurs whenever a design value changes."*
2. **Two of its float figures disagree with themselves inside the same set.** See
   2.3.
3. **The two documents that state float heights state two different DATUMS for
   them.** A-24.

## 2.2 The float figure register

Every cell is a T-018 candidate. **Assume seeded until traced.**

| Quantity | Value as it appears | Note |
|---|---|---|
| Day tank standpipe length | 30 in | **Two of the four day tank floats are placed at or above this length measured from the end cap face.** See 2.3 |
| Day tank end cap clearance off floor | 3 in | Also the datum offset between the two datums in A-24 |
| Day tank high-high | 32 in | |
| Day tank fill stop | 30 in | |
| Day tank fill start | 11 in | |
| Day tank low-low | 8 in | Stated as "the pump-top minimum", so it is a consequence of a pump dimension nobody here has |
| Day tank fill band | 19 in | Derived from two of the above |
| Day tank volume per refill | 25.8 gal | **Derived from a band, a diameter and a depth - G-33's three-quantity confusion is exactly what produces a number like this** |
| Refill time | 6.5 min at 4 GPM | Derived from a derived volume and a pump rating |
| Volume below low-low | 10.9 gal | Derived |
| Day tank max volume | 40.8 gal at 30 in | **The tree's part list says "40 gal day tank." 40.8 is a computed number, not the tank's rating** |
| Day tank inside depth / diameter | 33 in / 20 in | Stated as "modelled on a standard open head drum". **Modelled, not measured** |
| Storage standpipe length | 80 in | |
| Storage high-high | 72 in | |
| Storage fill stop | 66 in | |
| Storage fill start | 30 in | |
| Storage low | **20 in in two documents, 27 in in three others** | See 2.3. **One float, two heights, five documents** |
| Storage fill band | 36 in | |
| Storage max level | **78 in in one document, 81.5 in in another** | See 2.3 |
| Storage cone start | **18 in in one document, 12 in in another** | See 2.3 |
| Tether length | 3 in, one float at 2 in | |
| Switching differential | 1.5 in | **A float property, quoted without a datasheet.** Rule 3 territory |
| Float cord length | 20 ft | A part property |
| Float contact rating | 5 A, 120 V | **A part property quoted at the WRONG COIL VOLTAGE.** See C-05 |
| Cord tie spacing | every 6 in | |
| U-bolt size | 2 in ID | |
| Cable tie | 8 in, 120 lb | |

## 2.3 Figures that disagree with THEMSELVES inside the old set

These are the highest-value items in flag 2, because a figure that contradicts
itself cannot be a measurement in both places.

| Figure | Value A | Value B | Where each appears |
|---|---|---|---|
| **Storage low trip height** | **20 in** | **27 in** | 20 in on the storage standpipe sheet and in the handoff's own float map. 27 in on the build book electrical ladder float table, on the build book float mounting detail's trip-height table, and in the plotter sheet notes. **The document dedicated to placing that float and the document dedicated to wiring it do not agree** |
| **Storage max level** | 78 in | 81.5 in | 78 in on the storage standpipe elevation. 81.5 in on the float mounting detail |
| **Storage cone start** | 18 in | 12 in | 18 in on the storage standpipe sheet. 12 in on the float mounting detail |
| **Float height datum** | End cap face | Tank floor | Standpipe sheets say end cap face and repeat it in red. Build book float sheet says *"all dimensions off the TANK FLOOR"*. **The same numbers appear under both** |
| **Day tank standpipe vs float heights** | 30 in pipe | Floats at 30 in and 32 in | The pipe is 30 in long and hangs 3 in off the floor. Two floats are placed at 30 in and 32 in from the end cap face. **The upper float is above the top of the pipe carrying it** unless the datum is silently the tank floor for those two |
| **Float count on one sheet** | "four floats" | "all five floats" | The day tank standpipe elevation names four floats and its parts table lists four of each. The clamp detail on the same sheet says *"Identical for all five floats"* |

**None of these is a defect in the current tree. All six are the reason the caveat
exists.**

## 2.4 The wall figure register

Same blanket marking. **Assume seeded until traced.** Listed by group rather than
cell by cell, because the whole set is downstream of a board size that C-01
already contradicts:

- **Board**: width 72 in, height 44 in, thickness 1/2 in, bottom edge 40 in off
  the floor, zone split at 52 in.
- **Manifold and loop**: manifold 17 in down from the board top; injector centres
  6 in apart at 9, 15, 21, 27, 33 and 39 in; loop span 40 in; left leg 4 in; right
  leg 44 in; leg bottoms 40 in down; EC gland tee 26 in down the right riser; pH
  gland tee 34 in down; bypass leg outboard at 51 in; valves at 22, 30 and 38 in;
  service unions at 23-3/5 in and 36-2/5 in.
- **Shelf and containers**: bottle shelf 36 in down and 19 in below the manifold;
  container rack 26 in wide x 16 in deep x 20-3/4 in tall, two shelves; 42 lb per
  container when full; floor footprint 26 in rack + 20 in tank + 18 in clear.
- **Suction lifts**: 32 in / 2.7 ft, 52 in / 4.3 ft, 72 in / 6.0 ft, all measured
  to heads at 80 in off the floor; container liquid heights 48 in, 28 in and 8 in.
- **Enclosure**: 16.4 x 12.4 x 7.1 in; backplate 359 x 259 x 4.5 mm; three DIN
  rails at 18-63, 107-152 and 196-241 mm; two ducts at 70-100 and 159-189 mm;
  gland holes 7/8 in and 11/16 in; M4 x 0.7 tapped, 3.3 mm tap drill.
- **Cable runs**: receptacle row 30 in down from the board top; left edges at 16,
  26, 36 and 46 in; 10 in centres; common horizontal run at 27 in; P-clips every
  12 in vertical and 16 in level; 4 in service loop at receptacles; 12 in at probe
  glands; cut lengths 9, 9, 10 and 11 ft, total 39 ft, buy 50 ft; probe runs 7 ft
  and 6 ft off 3 m cables; probe cable clips every 12 in.
- **Clearances and rules-as-figures**: 4 in clear below each pump head; 6 in
  minimum air gap at both tanks; 1-1/2 in overflow bore; 12 tubes; 12 cord grips;
  chiller 600 W of rejected heat.

**One structural note about this register, offered as an observation and not as a
correction: several of these figures are DERIVED from the 72 in board width and
from the six-channel port count.** Both of those are contradicted at C-01 and
C-07. A derived figure whose input has moved is not a figure at all. **G-38's
shape, arriving on a dimension instead of on an impossibility claim.**

---

# FLAG 3. EVERY PART NAMED

**Blanket marking: MAY HAVE BEEN SUPERSEDED, RETURNED, OR NEVER BOUGHT.** The old
set's own ordering notes make this concrete rather than theoretical: it records a
part that its own cart audit said to DELETE being ordered anyway, and it records
another part corrected on a sheet after ordering to match what actually arrived.
**Under G-15 no agent states a part number, and this file is not doing so - it is
recording what the old set printed so the owner can rule on each.**

## Parts touching FLOATS

| Named | Role in the old set | Marking |
|---|---|---|
| SJE Rhombus SignalMaster SPDT, 20 ft cord | Every float, all eight positions | **May have been superseded, returned, or never bought.** And see C-05: rated in the old set against a 120 VAC coil, and the current control voltage is 24 V. **The tree's parts.md already carries "LS-1 through LS-8, pilot duty. NOBODY HAS TRACED THAT CHAIN AGAINST THE ACTUAL SJE PART" - see the provenance question below** |
| SJE Rhombus external cable weight | The pivot that sets every trip height | As above |
| 2 in U-bolt with backing plate, 316 stainless | The rim bracket carrying each standpipe | As above. **Assumes the tank has a rolled lip a U-bolt can wrap** |
| 1/4-20 nyloc nut, 316 stainless | Bracket fixing | As above |
| 3/4 in Sch 80 PVC pipe and socket cap | The standpipe itself | **D-109 makes all PVC 3/4 in Sch 80 in the current tree. That is not corroboration - D-109 is the source and it says derive nothing from it** |
| 8 in UV black nylon cable tie, 120 lb | Clamps each weight at its trip height | As above |
| White paint marker, fine tip | Marks the trip heights before install | As above |
| Winland WB-200, dry contact | Leak detector into the permissive string | **parts.md already names the Winland WaterBug WB200 as the leak console. Same part in two lineages. Under G-37 that is NOT a second source - establish which one the tree got it from before treating it as confirmed twice** |
| Finder 55.34 4PDT, 120 VAC coil, 94.74SMA socket | Every relay a float drives | **The tree has four Finder 55.34 relays and two 22.32 contactors on a 24 V control system. The relay family matches; the coil voltage does not. See C-05** |
| U.S. Solid 1/2 in motorized ball valve, 2-wire, NC, spring return, 110 V | The storage fill valve | **Superseded by D-114.** The current valve is a solenoid and voltage, pipe size and normally-closed are still open with the owner under F-087 |
| Watts 7 dual-check backflow preventer / Watts 0792091 LF8A vacuum breaker | Two different backflow devices for the same line in two documents | **May have been superseded, returned, or never bought.** The old set changed its own mind here and flags the change as an open code question |

## Parts touching THE WALL

| Named | Role | Marking |
|---|---|---|
| 1/2 in HDPE board | The wall substrate | **May have been superseded, returned, or never bought** |
| Growee Expert Combo modules: Hydro Master, pH Balancer, Doser 1-3 | The dosing controller and pumps | **Structurally superseded.** The current build is a Pi plus eight Kamoer heads and eight ADA6121 drivers. **Every wall band position downstream of a five-module row is downstream of a part that is gone** |
| McMaster 7578K14 wire duct, 1-1/2 x 1 in | Panel internal duct | As above |
| Panduit F1X1LG6 slotted duct, 1 x 1 in | The probe signal duct on the wall | As above |
| WAGO 4036N21 / 4036N19 / 4036N302 / 4036N204 / 4036N203 | Terminals, grounds, jumpers, end covers | As above |
| 69915K53 1/2 NPT and 69915K51 3/8 NPT cord grips | All wall and enclosure penetrations | As above |
| NEIKO 10185A step bit | Drilling the gland holes | As above |
| Sensorex FC75P 3/4 NPT gland | Probe wet fitting | As above. **S-11 is open and DOSING owns the wet fitting** |
| 835-101 adapter + John Guest PP011222W | Injection ports | As above. **DOSING's, and the port count was six** |
| TayMac MM420C boxes / ENERLITES TWR receptacles | The four wall receptacle boxes | **Superseded by D-046** - the current receptacles are panel mounted |
| 14/3 SJOOW cord, nylon P-clips, #10 x 3/4 pan head screws | Wall cable runs and fixings | **May have been superseded, returned, or never bought.** INTERCONNECT states cable requirements and search terms, never part numbers |

## A provenance question the owner should settle before anything else here

`parts.md` line 520 already reads: **"the float switches are LS-1 through LS-8,
pilot duty. NOBODY HAS TRACED THAT CHAIN AGAINST THE ACTUAL SJE PART."**

The 1st Edition set has exactly an LS-1 through LS-8 roster on exactly an SJE
part. **Two possibilities and they are not the same:**

1. The tree's roster came from the browser package independently, and the two
   efforts converged. Then it is real corroboration.
2. The tree's roster is inherited from this same 1st Edition lineage. **Then it is
   ONE claim wearing two hats, and G-37's second-source illusion is already
   sitting inside `parts.md` under the heading "Established facts about real
   parts."**

**Nothing in this pass can settle which. It needs the owner, and it should be
settled before any float proposal above is confirmed**, because if it is (2) then
confirming A-10 and A-11 against the tree's own roster is confirming the old set
against itself.

---

# FLAG 4. EVERY IMPOSSIBILITY AND EVERY PROHIBITION IN THE OLD SET IS UNGRADED

**Under G-36 an ungraded impossibility is not a claim anyone can check.** None of
the statements below names a grade. None of the CURRENT-shaped ones names what
would change it. Under the G-36 amendment from D-103, none says whether declining
to pay makes it true.

**They are reproduced so the owner can see the shape, not so anyone can act on
them. No agent may cite any of them.**

## Claims of impossibility

| The old set's claim | Shape, on its face | What is missing |
|---|---|---|
| *"A narrow angle float cannot hold a 19 in band on its own"* | Reads STRUCTURAL - a float property against a band. **This is the load-bearing one: it is the entire justification for the relay seal-in, which is G-03** | Ungraded. The differential figure behind it (1.5 in) is itself an untraced part property. **If it is wrong the seal-in is unnecessary; if it is right it is the reason G-03 exists** |
| *"Every liquid level stays BELOW the manifold. A failed tube then CANNOT siphon a container into the tank"* | Reads STRUCTURAL - it follows from geometry | Ungraded, and it is a claim about a whole failure class from one relation |
| *"Nothing may bridge that gap. No hose stuck down into the water, no elbow turned to reach the surface, no float valve on the end"* | A prohibition dressed as an impossibility | Ungraded |
| *"The feed bulkhead sits higher than the drain, so it CANNOT empty the tank on its own"* | STRUCTURAL-shaped | Ungraded |
| *"The plastic box is NOT a bonding path"* | STRUCTURAL-shaped, and materially the same thing CBL-07 says | Ungraded here. **CBL-07 is the tree's source and CBL-07 stands on its own** |
| *"Gravity will not push through a fine cartridge"* | STRUCTURAL-shaped | Ungraded, and no head figure behind it |
| *"An always-on faucet holds [a hose-bib vacuum breaker] under pressure permanently and it FAILS"* | CURRENT-shaped - it depends on a duty rating | Ungraded. It NAMES what would change it in passing (a continuous-pressure device) which is closer than the others get |
| *"No chlorine anywhere in this procedure, so an accidental mix CANNOT produce toxic gas"* | STRUCTURAL-shaped | Ungraded. Chemistry, and out of scope for this pass |
| *"You physically CANNOT install the wrong part"* (the handoff, on a relay whose buy list orders only one type) | CURRENT, explicitly - it depends on what was ordered | Ungraded, and **self-fulfilling in D-103's sense: it removes the reason to check the label** |

## Prohibitions

These are not impossibility claims, but each one forecloses something and each is
stated without a grade:

- *"Do not rearrange the ports."*
- *"NOTHING GETS FLIPPED. All five mount the same way."*
- *"Adjust the cable tie. NEVER adjust the wiring."*
- *"Probe cables NEVER share a duct or a conduit with 120 V. Not the float cable
  either."*
- *"Cord grips on the bottom face only, NEVER the top or sides."*
- *"NO ferrules anywhere in this panel."*
- *"Never restrict suction on a diaphragm pump."*
- *"Do not keep tightening. The thread root is the thinnest section in the whole
  system and it splits before it seals."*
- *"Never use a `for` loop to place geometry"* and *"Do not merge the add-on into
  the main package"* - both drawing-process rules, not build rules, listed only
  so the owner sees the full inventory.

**Two of these - the port order and the no-flip rule - are the only prohibitions
in the whole set that would change what a CURRENT subsystem builds. Both are in
the proposal list above (B-10, A-06) and both need the owner, not this file.**

---

# FLAG 5. WHAT THE OLD SET COVERS THAT THE CURRENT TREE HAS NO POSITION ON

**This is the category with the most value in it, because these are blanks rather
than disagreements.** Each row is a place where the current tree is silent and the
old set has something - so the owner's answer converts a blank into a decision
rather than adjudicating a conflict.

| # | The blank in the current tree | What the old set has |
|---|---|---|
| **1** | **HOW A FLOAT IS PHYSICALLY HELD IN A TANK.** `water.md` owns *"which floats, their pilot duty rating, and their placement in both tanks"* and *"day tank penetrations and hangers"*. Nothing in the tree says whether a float hangs on its own cord, clamps to a wall, or rides a fixture | **The standpipe, entire: one rigid pipe per tank carrying every float and every cord, hung off the rim on a U-bolt, end cap clear of the floor, nothing resting on the tank bottom and nothing hanging off a float body.** A-01 to A-04 |
| **2** | **WHAT SETS A TRIP HEIGHT, mechanically.** Nothing in the tree names the adjustable element | **The external cable weight is the pivot and its clamp position IS the trip height, marked with a paint pen before install and adjusted at the tie afterwards.** A-07, A-09 |
| **3** | **WHAT SETS THE SWITCHING DIFFERENTIAL.** Nothing in the tree names it | **Tether length below the weight.** A-08 |
| **4** | **THE DATUM FOR EVERY LEVEL FIGURE.** The tree has no datum rule at all. Every level number anywhere in it is currently a bare number | **A named datum, stated in red on the sheets - and the old set states TWO of them and uses the same figures under both.** A-24. **The proposal is the RULE, not either datum** |
| **5** | **WHETHER ONE FLOAT PART SERVES EVERY POSITION.** The tree has G-28 for relays - not interchangeable once bought, labelled by name - and nothing at all for floats | **One part everywhere, never flipped, NO or NC chosen at the terminal strip.** A-05, A-06. **Note this is the OPPOSITE property from G-28: relays are position-bound, floats would be freely interchangeable. Whether that asymmetry is right is a question, not a finding** |
| **6** | **HOW MANY FLOATS AND WHAT THE EXTRA ONES DO.** G-03 requires a start and a stop per tank, so four. Nothing in the tree says whether there is a high-high, a low-low or a storage-low, or what they drop | **Eight: four per tank. The extra four are two high-highs into the master permissive, one low-low as the dry-run interlock, and one storage-low also into the master permissive.** A-10 to A-12, A-20 to A-22 |
| **7** | **WHETHER STORAGE-LOW IS A LOCAL INTERLOCK OR A MASTER FAULT** | **A master fault. It sits in the permissive string and drops everything.** A-21 |
| **8** | **THE ORDER AND SPACING OF THINGS ON THE WALL, TOP TO BOTTOM.** D-090 fixes the envelope at 8 x 8 ft and says Z5, M-02 and the station run are consequences of placement inside it. **Nothing states the placement.** M-02 and M-03 are OPEN. F-067 records that Z5 is undefined and load-bearing in three places and that *"nothing can be drawn until it exists"* | **A five-band vertical stack with a stated reason for the top band and a stated relation governing the bottom one.** B-04 to B-07 |
| **9** | **WHICH FACE OF AN ENCLOSURE THE GLANDS ARE ON.** CBL-01 to CBL-04 are all open on gland positions | **Bottom face only, never top or sides, drip loop outside.** B-16 |
| **10** | **THE SEPARATION RULE FOR PROBE CABLES.** `interconnect.md` owns it as an open item and there is no rule yet | **Own duct, never shared with 120 V or with float cable, cross at 90 degrees, with a named observable symptom.** B-20, B-21 |
| **11** | **CABLE ROUTE SHAPE ON THE WALL.** The tree has cut lengths in `parts.md` and no routing rule | **Grip → drop → common horizontal run → level → drop in. Not point to point.** B-17, B-18 |
| **12** | **SERVICE LOOPS SIZED BY THE SERVICE ACTION.** `parts.md` adds a flat 3 ft per cable (6 in drip loop per grip, 12 in service per end) | **A loop sized by what it must let you do - pull a box off the board, back a probe out to a sink.** B-19. **The two rules coexist; the old set's is a reason, the tree's is an allowance** |
| **13** | **SUCTION LIFT AS A LAYOUT DRIVER.** Nothing in the tree connects container shelf height to pump performance | **A per-shelf lift table measured to the head height.** B-07 |
| **14** | **THE FLOOR IN FRONT OF THE WALL.** The tree's envelope is a wall, not a room | **A floor footprint drawn on the same sheet: rack, tank, and a stated clear gap.** B-24, B-25 |
| **15** | **WHERE THE CHILLER PHYSICALLY STANDS.** D-108 makes it self-contained; nothing says where it is | **Outside the room, on a heat-rejection argument.** B-26 |
| **16** | **A ZONED BOARD.** No zoning concept exists in the tree | **A dosing zone and a control zone with a stated split.** B-02 |

## The single most valuable one

**Row 1: how a float is physically held.**

It is the most valuable for four reasons that compound:

1. **It is a true blank.** `water.md` lists float placement as OPEN and owned; the
   interface table's S-01 and S-02 both say WATER owns *"which floats, their type
   and where they sit"*; and there is no answer anywhere in the tree to the
   mechanical question of what a float is attached to. **Nothing has to be
   unpicked to answer it.**

2. **It is keyed to a ROLE, not a dimension, which is what G-34 prefers.** The
   standpipe concept survives every figure in flag 2 being wrong. *"The bracket
   carries the pipe, the floats and every cord. Nothing hangs off a float body and
   nothing rests on the tank floor"* is a statement about what things ARE and what
   they carry. **It contains no number.** Confirm or replace it and the heights
   remain a separate, later, tracable question.

3. **It unblocks three other rows at once.** S-01 and S-02 are both split rows
   held by BOSS until WATER returns *"the device requirement, the search term and
   the physical location"* - and the physical location is the half that has no
   candidate answer at all today. CBL-04, field cable runs to the floats, cannot
   be routed until it is known where a float cord starts and where it leaves the
   tank. And `water.md`'s own standing note - **"Position held by fixture, not by
   cord. [...] A cord-hung pump is a pump whose position is a suggestion"** -
   already states the exact principle for the submersibles and the return drop.
   **WATER has the rule and has not applied it to the floats.** The old set
   applies the same rule to the floats and calls it a standpipe.

4. **It is the failure that is invisible.** A float on its own cord in an open-top
   tank has a position that drifts, and there is no reading anywhere in this
   system that would show it. G-01 and G-02 make level control hardware and give
   software exactly one dry contact. **Nothing measures a level, so nothing detects
   a float that has moved.** The fill stop is the only thing stopping the fill -
   D-114 says so in as many words - and if its position is held by a cord, its
   position is a suggestion.

**It is offered as a question. It is not decided, it is not recommended, and
neither the pipe, the bracket, the material nor any height in it is a choice this
file is making.**

---

# WHAT THIS FILE IS NOT

- It is **not a source.** No subsystem may cite it. No decision may be built on it.
- It **names no part as a choice** and **sizes nothing.** Every part in flag 3 is
  recorded as printed, marked as possibly superseded, and offered for the owner's
  ruling under G-15.
- It **recommends nothing.** Every A and B item is a question with a starting
  proposal attached.
- Where it disagrees with the tree, **the tree wins**, and the disagreement is
  recorded in flag 1 as a finding about the old set.
- **The two rows the owner should answer first, because answering them wrong is
  cheap and answering them by default is expensive: C-06 (the old set closes S-05
  with a level element, and S-05 is being held open on purpose) and the provenance
  question at the end of flag 3 (whether `parts.md`'s LS-1 to LS-8 roster is
  independent of this set or inherited from it).**

*Written 2026-09-03. One pass, at the end, per the invocation discipline in
agents.md.*
