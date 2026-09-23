# D7. The purchase package

INTEGRATOR, 2026-09-23. Written in one pass per BOSS's invocation discipline.

**THIS IS THE DOCUMENT WHERE A MISTAKE COSTS MONEY RATHER THAN TIME.** Every other
document in this set can be corrected in a pass. This one gets acted on with a
credit card.

---

# READ ME

## 1. What this document is, and what reads it

**Every part this build needs, once, on one line, with a state and - where a state
allows one - a quantity.** It is read by the buyer, once, before anything is bought.
`build-book.md` step 2-02 requires it worked and the buy done before section 2 of the
build starts.

**IT IS THE ONLY DOCUMENT IN THIS SET WHERE A QUANTITY APPEARS AT ALL.**
`document-plan.md` section 3.2 reserves every quantity, count, total and price to
this document and states that no drawing sheet carries a parts table. That is the old
set's one defect that cost money, and the structural fix is that a supplement has
exactly one document it can contradict and one place to look.

**Structure follows the 1st Edition's purchase workbook under G-40b**: a read-me
stating how it is organised and what is still open, a buy list, and a cart audit
saying what to change in each cart before checkout. Its column set - ID, System,
Item, Status, part or search term, Qty, Unit, Notes - is adopted rather than
re-derived. **Its figures and its parts are observed in the 1st Edition set,
unverified, per G-40**, and nothing of its content is carried across without being
named as an import.

## 2. G-41, AND THIS IS THE DOCUMENT IT WAS FROZEN FOR

**ASSEMBLY STEPS ARE ABSOLUTE AND SHOULD REPEAT. QUANTITIES, COUNTS AND TOTALS ARE
DELTAS AND MUST NEVER REPEAT.** If a table can be read either way it will be read as
ABSOLUTE by whoever is holding a credit card.

G-41 was frozen against a real cost: the parallel build's add-on sheet listed four
float switches where its own text said three arrive, **and buying per both sheets
gives nine floats for eight positions.**

Three rules follow, and they govern every number below.

**a. A QUANTITY IN SECTION B IS WHAT TO BUY. IT IS NOT A TOTAL.** Where a part is
partly on the shelf, the shelf holding is a separate line in section A and the two
are never added. The clearest case is the relays: four Finder 55.34 standard are held
at A-13 and four Finder 55.34 gold are bought at B-01. **They are eight relays in
total and the buy line is four.**

**b. NO QUANTITY IS EVER STATED AS A RANGE ON A BUY LINE.** Where the tree gives a
minimum and a contingency, the buy line carries the minimum and the contingency is
written as an explicit ADD, with the decision it waits on named. A cell reading
"3 or 4" is a cell that gets bought as 4 and stocked as 3, or the reverse.

**c. A COUNT IS DERIVED ONLY FROM A NAMED ROW, AND THE ROW IS ON THE LINE.** Where no
row supports a count, the Qty cell reads **not stated** and the line stays a
requirement. It does not get a guess to look finished.

## 3. THE FOUR STATES, AND WHY THEY ARE KEPT APART

| State | Section | Meaning | Qty means |
|---|---|---|---|
| **ALREADY OWNED** | A | On the shelf, delivered or ordered. **Nothing to buy** | What is held. **Never added to a section B line** |
| **SPECIFIED AND NOT BOUGHT** | B | A part is named and must be purchased | **What to buy** |
| **REQUIREMENT ONLY** | C | Nothing is chosen. The line carries a requirement and a search term | What to buy **once the lookup returns**, or **not stated** |
| **N/A WITH REASON** | D | **The line can never be filled here.** It belongs to another document, or the part was removed, or the requirement is met by something that is not a part | **Nothing. Ever** |

**Section C IS NOT AN OMISSION.** Under G-15 the owner does all lookups and every
agent returns a requirement and a search term and stops. **A requirement line is
finished work.** No agent may state a part number or a spec from memory, and nothing
in this document does.

**Section D EXISTS BECAUSE OF G-46.** A cell that can never be filled must not look
like one that has not been filled yet. Two blank cells that mean opposite things is
one line of work outstanding and one line of work that will never exist, **and a
completion count that mixes them is wrong in both directions.** Section D is counted
separately and never rolls into a percentage.

## 4. TWO LIVE PURCHASE WARNINGS. BOTH HAVE ALREADY BEEN PAID FOR BY SOMEONE

### 4.1 DO NOT BUY A DIN-RAIL GROUNDING TERMINAL BLOCK

**The parallel build bought seven before the ground bar decision and is returning
them.** D-166's record of it: a grounding terminal block bonds to the rail, the rail
bonds to the plate, **and the plate is plastic. They bond to nothing.**

**Nothing in this tree assumes one.** BOSS searched `parts.md`, `order.md`,
`electrical-schematic.md`, both schedules and `interface-table.md`, and every one
already says ground bar. It is marked n/a at D-03 so that it stays that way when this
package is worked, rather than left as an absence a buyer fills in helpfully.

**This crossing is IN, from the parallel build, per G-53.**

### 4.2 UL 489, NOT UL 1077, IS A REQUIREMENT ON THE LINE FOR BOTH OVERCURRENT DEVICES

**A supplementary protector is not legal branch protection under the NEC.** D-200
records it as a requirement on the line and not a preference. **The common IEC parts
- ABB S201-C15, Schneider M9F11115, Eaton FAZ-C15/1 without the NA suffix - are all
UL 1077**, many fully rated only two-pole at 240 or 415 V with the single-pole 120 V
interrupt weaker or unlisted.

**The owner's two shelf breakers are CANDIDATES pending that check, not the
specification.** D-202: whether the Control Gear CGMB1C15 and CGMB1D15 are UL 489 or
UL 1077 is unknown, **and by the requirement above that decides whether they are
usable at all.** They sit at A-23 and A-24 marked as candidates. The specification is
B-03 and B-04.

## 5. ONE LINE IS BLOCKED ON A MEASUREMENT RATHER THAN A LOOKUP

**B-04, BUS-B's breaker, is correct only if the compressor's measured locked-rotor
current is under about 120 to 150 A.**

`parts.md` states outright that the JBJ Arctica DBE-200's locked rotor current is NOT
PUBLISHED anywhere, and that any inrush figure is an estimate and must be labelled as
one everywhere it appears. **The D curve does not solve the unknown LRA - it moves the
magnetic wall from 5-10x to 10-20x**, which on 15 A is 150 to 300 A.

| Fault current | What happens |
|---|---|
| 7.5 A continuous, 0.5x In | The thermal element never moves |
| Under 150 A | Will not instantaneous trip |
| 150 to 240 A | May or may not. **Nuisance trip on a sticky start is possible** |
| Over 240 A | Clears under 100 ms, which is a stall rather than a start |

**If the measured LRA is over 120 to 150 A the answer is a larger breaker sized to
the wire, or a motor-rated protector.** D-200's own words: a margin row became a
measurement.

**And the reason it must be got right the first time is that its failure is silent.**
D-108 leaves nothing in the panel wired to the chiller, so a nuisance trip on BUS-B
stops the compressor and nothing reports it.

## 6. WHAT THIS PACKAGE CANNOT FINISH, AND IT IS NOT AN OVERSIGHT

**The float line, C-21, cannot close before the build starts, and `build-book.md`
step 2-02 says so on its own page rather than leaving a builder to find it at section
22.**

The chain is: D-131 makes the float cord the strain member, the trip-height datum and
the signal path at once, **so it cannot be cut at the tank and cannot be joined
there.** A float whose supplied cord does not reach is disqualified. The cord span is
produced by build-book step 6-07, which is blocked on the wall arrangement, M-02.
**So the purchase is gated by a step inside the book the purchase is supposed to
precede.** F-100, graded CURRENT and SELF-FULFILLING under G-36: unstated, floats get
bought against positions and contact duty alone, and the only remedies left are a
splice in the wet zone or moving a mounted panel, both of which D-131 forbids.

**What would unblock it without the arrangement:** build-book 6-07 records that a
worst-case BOUND on the span follows from D-090's 8 ft by 8 ft envelope and the cut
rule, with no arrangement at all, **and that the requirement 6-07 feeds is a
DISQUALIFICATION test rather than a cut length.** A bound is enough to disqualify.

**Twelve other lines are in the same shape** and are marked in section C with the
build-book step that gates them: the wall fixings at 10-02, the device marker at
3-02, the local ground bars at 13-08 and 14-08a, the heatsinks at 14-07, the tank
support at 16-01, the U-bolts at 18-01, the cable ties in section 22, the paint pen
at 21-11, the solvent cement at 11-01, the tank cord grips at 20-07b, the fill outlet
bracket at 25-04 and the pump cradles at 27-01.

## 7. WHAT THIS PACKAGE DOES NOT COVER, NAMED RATHER THAN LEFT ABSENT

**Tools.** No step's tooling is on this list. `parts.md` requires five 22 mm top-face
holes **step drilled**, and build-book section 8 cuts cord grip holes and head
penetrations. The 1st Edition's cart audit carried a step drill line. **Nothing in
this tree states a tool as a buy line and no tool is invented here.**

**Consumables a step names but no file states as bought** are in section C, not
omitted. That is deliberate: build-book's own words at 22, a consumable that a step
names is a consumable that has to be bought.

**Prices.** No price appears anywhere in this document. No file read for it states
one, and G-47 applies in the other direction as well - **an unpriced line is not a
cheap line, it is an unpriced line.**

## 8. PROVENANCE DISCIPLINE ON THIS PAGE

- **No part number, price, quantity or spec appears here that is not already in the
  tree or returned by a subsystem.** Nothing is invented.
- **Where a count is derived, the row it is derived from is on the line.**
- **Nothing is asserted from absence.** Where this document says a part is not
  recorded as bought, it names the files that were read: `decisions.md`'s "Parts the
  owner already has" table, `parts.md` in full, `terminal-survey.md`, and `order.md`.
- **A citation is not a source, G-37.** Where the 1st Edition is the only thing on the
  page, the line says so and stays unverified.
- **D-118 removes the 1st Edition's priority on ONE subject specifically: the
  floats.** The LS-1 to LS-8 roster came from the same body of work as the 1st Edition
  set and was sitting inside `parts.md` under "established facts", so checking it
  against the 1st Edition drawings would have been checking a document against itself.
  **G-40b does not apply to the float line. The float pass restarts from requirements
  and the old roster is one candidate among others.**

---

# SECTION A. ALREADY OWNED. NOTHING ON THIS SECTION IS BOUGHT

**Qty here is WHAT IS HELD. It is never added to a section B quantity.**

Verified against `parts.md`, `decisions.md`'s "Parts the owner already has" table and
`terminal-survey.md`'s held counts. **That table's own preamble binds: quantities
beyond what is stated there are not decided and no agent may assume one.**

| ID | System | Item | Status | Qty | Unit | Source and note |
|---|---|---|---|---|---|---|
| A-01 | Water | 100 gal cone bottom storage tank, open top | OWNED | 1 | ea | decisions.md owned table. **F-111: it is already bought, so a bulkhead sited before the trip heights are settled is a scrapped tank** |
| A-02 | Water | 40 gal food-grade day tank, open top | OWNED | 1 | ea | decisions.md owned table. As A-01 |
| A-03 | Transfer | Anbull transfer pump, 120 V corded | OWNED | 1 | ea | decisions.md owned table. **Its electrical input is not on file** - main-panel-ladder mark ?6 |
| A-04 | Water | Hi-flow submersible, 120 V corded | OWNED | 2 | ea | decisions.md owned table, "one circulation and one chiller loop". **CONFLICTS WITH B-10. See cart audit CA-03 before ordering a loop pump** |
| A-05 | Chiller | JBJ Arctica DBE-200, 115 V, 6 A, 3000 BTU/h, R-134a, no internal pump | OWNED | 1 | ea | decisions.md owned table and parts.md. **Its locked rotor current is NOT PUBLISHED. B-04 waits on the nameplate reading** |
| A-06 | Wet path | PVC, 3/4 in Schedule 80 | OWNED | **not stated** | - | decisions.md owned table, "All the PVC". D-109 sets 3/4 in Sch 80. **No quantity is stated anywhere and none may be assumed.** The two standpipes are cut from it, D-121 and D-166: PVC, confirmed by the owner |
| A-07 | Dosing | Kamoer KPHM400-ST peristaltic pump head, motor and stepper as one unit | OWNED | 8 | ea | decisions.md owned table, "Eight peristaltic pump heads". parts.md holds the figures |
| A-08 | Pump boxes | Adafruit 6121 TMC2209 breakout | OWNED | 8 | ea | decisions.md owned table. **JP4 ships as bare pads with the header strip loose and unsoldered** - see D-14 |
| A-09 | Display box | Raspberry Pi 5 | OWNED | 1 | ea | decisions.md owned table |
| A-10 | Display box | 7 inch touch display | OWNED | 1 | ea | decisions.md owned table |
| A-11 | Display box | Atlas Scientific EZO circuits: pH, EC, RTD with PT-1000 | OWNED | 3 | ea | decisions.md owned table. **They ship in UART mode and each must be jumpered to I2C before the Pi can see it, and the mode pin differs by circuit type.** C-14, a build step nobody had |
| A-12 | Display box | Atlas Scientific ISCCB-2 isolation carrier | OWNED | 2 | ea | decisions.md owned table. **pH and EC only. The RTD gets NO carrier** - a resistance measurement has no solution ground path |
| A-13 | Main panel | Finder 55.34 4PDT relay, **STANDARD contact** | OWNED | 4 | ea | decisions.md owned table; order.md confirms the four in hand are STANDARD. **order.md item 2 is therefore ZERO.** Three are drawn for the power envelopes, one is the standard spare. **If K-PERM splits, all four are drawn and there is no standard spare** |
| A-14 | Main panel | Finder 22.32 modular contactor, 24 Vdc coil, 2 NO, 25 A | OWNED | 2 | ea | decisions.md owned table. **One is KM-DRV and keeps its job. The other was KM-CHIL and is FREED by D-201** - the 22.32's 25 A is AC-1 resistive and its AC-3 rating is typically 8 A or less. **It is a spare, not a part with a position** |
| A-15 | Main panel | Mean Well NDR-240-24, 24 Vdc, 10 A, 240 W | OWNED | 1 | ea | decisions.md owned table. **VERTICAL MOUNTING ONLY, AC in at the bottom, DC out at the top. Any other orientation voids the cooling figures** |
| A-16 | Main panel | Main panel enclosure | OWNED | 1 | ea | decisions.md owned table, 20.7 x 16.6 in. **D-199 closes the enclosure study on this box and withdraws D-196's 16 x 14 verdict: no further enclosure is specified.** See cart audit CA-08 - `parts.md` lookup 2 and D-199 describe two different boxes and only one is on the shelf |
| A-17 | Pump boxes | Pump box enclosure, 16 x 8 x 6 in, sealed | OWNED | 2 | ea | decisions.md owned table; parts.md enclosures. **The heads mount THROUGH the lids** |
| A-18 | Display box | Display box enclosure, **300 x 300 x 150 mm, plate 260 x 260**, NEMA 4X polycarbonate, gasketed display cutout. **CORRECTED 2026-09-23, D-226: this line read "roughly 300 x 250 x 130 mm" and the middle and depth figures were both wrong** | OWNED | 1 | ea | decisions.md owned table; parts.md enclosures |
| A-19 | Display box | ULN2003 | OWNED | 12 | ea | terminal-survey.md, "12 held, fewer used". **One drives the single Pi-driven coil, S-09** |
| A-20 | Display box | 74AHCT125 | OWNED | 4 | ea | terminal-survey.md, "4 held" |
| A-21 | Main panel | Inrush current limiter | OWNED | 2 | ea | terminal-survey.md Group 3. **No position is assigned in anything read for this document** |
| A-22 | Main panel | McMaster 2450K14 ground bar block, tin-plated copper, 5.75 x 0.50 x 0.50 in, twelve 1/4-28 tapped holes, 14 to 6 AWG | OWNED | 2 | ea | F-117 closed 2026-09-23: **the owner bought two 12-way bars rather than one.** D-192: two bonded bars are ONE ground point. **NO INSULATORS AND NO MOUNTING HARDWARE.** D-195: drill through, holes at least 5.0 in apart to miss the taps, both bars side by side, **jumper first per C-25**. Both go in the main panel; see C-16 for the remote boxes |
| A-23 | Main panel | Control Gear CGMB1C15, 1P 15 A C curve | **DELIVERED, CANDIDATE ONLY** | 1 | ea | parts.md, on the shelf. **CANDIDATE for BUS-A pending the UL 489 check. Whether it is UL 489 or UL 1077 is UNKNOWN, and that decides whether it is usable.** The specification is B-03 |
| A-24 | Main panel | Control Gear CGMB1D15, 1P 15 A D curve | **DELIVERED, CANDIDATE ONLY** | 1 | ea | parts.md, on the shelf. **CANDIDATE for BUS-B, pending BOTH the UL 489 check AND the LRA measurement.** The specification is B-04 |
| A-25 | Main panel | Control Gear CGMB1D06, 1P 6 A D curve | DELIVERED | 1 | ea | parts.md, on the shelf. **No position in this build is assigned to it in anything read for this document.** Recorded so it is not bought against and not assumed into a position |
| A-26 | Main panel | Conta-Clip 2190.2 DIN fuse holder, 5 x 20 mm, with 2046.2 end plate and five 3 A glass fuses | DELIVERED | 1 | ea | parts.md, on the shelf. **NO INDICATOR, so it does NOT meet the R-PI requirement.** D-204: nothing in the panel can power-cycle the Pi, so a blown fuse presents as a dead Pi with no cause. **It is the part the parallel build specified before anyone asked for one.** The specification is B-05 |
| A-27 | Water | ASCO 8210G095AC120/60 fill solenoid, 3/4 NPT, brass, NBR, 2-way normally closed, 120 VAC 60 Hz Class F 10.1 W | **ORDERED** | 1 | ea | D-136, fully specified. **Inrush 0.58 A, holding 0.21 A, Cv 5, minimum operating pressure differential 0 psi, DIRECT-LIFT hung diaphragm.** Spring returns closed on power loss. Installed between unions. **THE NUMBER THAT SIZES A CONTACT IS THE INRUSH, 0.58 A** |
| A-28 | Main panel | Finder 94.74SMA socket | OWNED, **CONFIRM** | 4 | ea | **DERIVED, and the derivation is order.md item 3**: six envelopes built needs six sockets and order.md's buy count is 2, or seven and 3 if K-PERM splits. Both arithmetics resolve to four in hand. terminal-survey.md Group 1 also lists relay-and-socket as 4. **`decisions.md`'s owned table names only the relays.** See cart audit CA-05 |

**28 lines already owned.**

---

# SECTION B. SPECIFIED AND NOT BOUGHT

**Qty here is WHAT TO BUY.** Under G-41 it is a delta against section A and is never
a total.

| ID | System | Item and exact search term | Qty | Unit | Notes |
|---|---|---|---|---|---|
| B-01 | Main panel | **Finder 55.34 4PDT, AgNi PLUS HARD GOLD, option 5.** Search: `Finder 55.34 contact material options AgNi hard gold ordering code`; `Finder 55.34 DC coil operating range must release voltage` | **4** | ea | **order.md item 1 gives 3 minimum and 4 if K-PERM splits. MAIN-PANEL's recommendation is BUY THE FOURTH GOLD, and its reason is not the split.** At the minimum there is one standard spare and ZERO gold spares, and under G-30 a standard relay cannot substitute for a gold one. **The fourth gold is used either way: as K-PERM-Q if the split happens, or as the only gold spare if it does not, and the envelopes with no spare are exactly the ones carrying every Pi-facing signal and both contact-driven lamps.** **G-48: it costs one relay and no step. What it buys is that resolving the split later does not mean a second order, a second delivery and rewiring an envelope already built and labelled.** **NEVER CARRIES A POWER POLE: the gold is consumed above roughly 30 V and 100 mA and reverts to AgNi.** **Coil requirement: a DC coil whose permitted continuous range covers the WHOLE 23.76 to 28.28 V trim band per F-010, not a coil nominally matched to 24 V, with the must-release voltage stated** |
| B-02 | Main panel | **Finder 94.74SMA socket, 4PDT, DIN rail, with the 094.71 metal retaining clip.** Search: `Finder 94.74 socket technical data retaining clip DIN rail`; `relay socket rated insulation voltage between poles`; `relay socket terminal two conductors per clamp permitted` | **3** | ea | **order.md item 3, at MAIN-PANEL's recommendation of three. One per envelope BUILT: a spare relay reuses the socket of the one it replaces, so no spare socket is needed.** If K-PERM does not split, the third is spare. **The SMA ships with the 094.71 metal clip and the coil-side slot takes the 99.01 suppression module - both fit, neither is sacrificed, and the module sits INSIDE the socket envelope so it adds no height.** **Do NOT use a 99.02, that is the box-clamp family. The plastic 094.91.3 clip is INSTEAD OF the metal one, not in addition.** Rail occupancy 30 mm, height above rail 71 mm with clip. **Two open requirements on the line: rated insulation BETWEEN POLES, which is the mixed-voltage gate G-30 does not answer; and clamp capacity per conductor, T-009 and T-010 - any terminal expected to take two conductors must be rated for two, and if it is not, the second conductor goes to a terminal block** |
| B-03 | Main panel | **Altech 1C15UL. 1P, C curve, 15 A, UL 489, 10 kA at 120 V, 17.5 mm rail.** Search: `Altech 1C15UL UL 489 branch circuit breaker 120 V` | **1** | ea | BUS-A: the NDR primary, FV-1, and the transfer, manifold and R-PI feeds. **Requirement on the line: UL 489, not UL 1077. Selectivity with the building breaker.** **A-23 may satisfy this line and may not. Check its listing before buying either** |
| B-04 | Main panel | **Altech 1D15UL. Same family, D curve, 15 A, UL 489, 10 kA, 17.5 mm rail.** Search: `Altech 1D15UL UL 489 D curve`; `JBJ Arctica DBE-200 locked rotor amperage nameplate` | **1** | ea | **BLOCKED ON A MEASUREMENT, NOT A LOOKUP. This breaker is correct only if the compressor's MEASURED locked-rotor current is under about 120 to 150 A.** BUS-B carries 7.5 A continuous, 6 A chiller plus 1.5 A pump. **Read the compressor nameplate before ordering.** Over 120 to 150 A the answer is a larger breaker sized to the wire, or a motor-rated protector. **A nuisance trip here is SILENT - D-108 leaves nothing in the panel wired to the chiller.** **A-24 may satisfy this line, pending the same UL 489 check** |
| B-05 | Main panel | **Phoenix Contact PT 4-HESILED 250, 5 x 20 mm, screw; or spring-cage ST 4-HESILED 250, order 3036563. 6.2 mm rail.** Search: `Phoenix Contact PT 4-HESILED 250 DIN fuse holder blown fuse indicator` | **1** | ea | R-PI feed. **USE THE 250 V VERSION. A 24 V LED version dies on 120 V.** **The indicator has NO minimum load current, because the lamp sits ACROSS the fuse and not in series with the load** - fuse good, LED shorted out, dark; fuse open, full 120 V across the LED and its resistor, lamp lights. The datasheet's 0.4 to 0.95 mA is leakage through the indicator while the fuse is open, not a lighting threshold. **G-48: one part, no extra step. What it prevents is the one failure in this panel that presents as "the Pi is dead and nothing says why", because nothing in the panel can power-cycle the Pi.** **A-26 does NOT satisfy this line - it has no indicator.** The fuse element itself is C-18 |
| B-06 | Main panel | **ABB AF09-30-10-13, 45 mm rail. Alternative Schneider LC1D09G7, same width.** Search: `ABB AF09-30-10-13 electronic coil 100 250 V`; `modular contactor AC-3 rating single phase hermetic compressor` | **1** | ea | **DO NOT ORDER YET. KM-CHIL STAYS BLOCKED on the open rung that decides its coil's bus, and a coil voltage follows from which bus it is on.** That rung decides whether the Pi can stop the water system, which G-26 forbids, so **no part may be chosen first, rule 9.** Load 8.7 A: 7.2 A compressor FLA at 1/3 HP 115 V plus 1.5 A pump. AF09: AC-3 9 A, AC-1 25 A, UL 3/4 HP at 120 V, **coil 100 to 250 V AC or DC.** LC1D09G7: AC-3 9 A, AC-1 25 A, 1/3 HP at 115 V, 120 V coil. **COIL DROP-OUT DECIDES IT AND IT FAVOURS THE ABB. A standard AC magnet coil chatters and can WELD on a brown-out** - TeSys D pulls in at 0.85 to 1.1x Un and drops out at 0.3 to 0.6x Un. **The ABB electronic coil stays sealed to about 100 V then opens cleanly: it REMOVES the failure mode rather than tolerating it.** **The -13 coil code is 100 to 250 V and a 24 V bus is not inside that band, which is exactly why the rung must close first** |
| B-07 | Field | **Winland WaterBug WB200 leak console, with its floor sensor.** Search: `Winland WaterBug WB200 leak detection module`; `Winland WaterBug WB200 sensor lead circuit voltage` | **1** | ea | **The part is named in parts.md. It is not in `decisions.md`'s owned table and `parts.md` does not record it as bought.** D-163: **remote, in no enclosure, fed 24 V through its own cord grip, sensor ON THE FLOOR rather than in the drain.** Its Form C legs sit in the 120 V permissive chain, **so every conductor in its cable is insulated for 600 V.** **CHECK ITS SUPPLY VOLTAGE BEFORE BUYING - see cart audit CA-02.** Its sensing-circuit class is an open lookup and is D6's last two empty cells. **G-39 as extended by D-170: what its contact does when its own 24 V supply dies is on file nowhere, and that contact sits in a permissive chain** |
| B-08 | Main panel | **Bell 5320-0 weatherproof device box.** Search: `Bell 5320-0 weatherproof outlet box` | **4** | ea | **D-197 and parts.md lookup 11: a standard 15 A duplex DOES NOT PANEL-MOUNT. It screws to a DEVICE BOX by the yoke, strap holes 3.281 in apart, and the body sits in the box rather than in the panel.** So the boxes mount **to the wall BESIDE the panel** and are fed by cord grips. **Count is four and it is derived from main-panel-plate-area section 2.1: the four receptacle feeds are the transfer pump P-03, the manifold pump P-04, the chiller and loop pump P-05, and the R-PI brick P-07.** The receptacle devices themselves are C-49 |
| B-09 | Main panel | **TayMac in-use weatherproof cover, to suit the 5320-0.** Search: `TayMac in use weatherproof cover 5320` | **4** | ea | As B-08. One per box |
| B-10 | Chiller | **Danner Supreme Aqua-Mag 12, item 02712.** 1200 GPH, about 840 to 940 GPH at 4 to 6 ft head, 110 W, 1.5 A at 120 V, 3/4 in FPT inlet, 3/4 in MPT outlet, continuous duty, oil-free magnetic drive. Search: `Danner Supreme Aqua-Mag 12 02712` | **1** | ea | **D-137: "the chiller loop pump is a separate submersible and IS BEING BOUGHT."** **DO NOT BUY BEFORE CHECKING CA-03 - `decisions.md`'s owned table of 2026-08-30 says two hi-flow submersibles are already held, one circulation and one chiller loop, and D-137 of 2026-09-04 says this one is being bought. Buying per both records gives three submersibles for two positions, which is G-41's exact shape.** **DO NOT BUY THE VENTURI OR AIR-FRACTIONATING VERSION. Air in a heat exchanger is the opposite of what a chiller loop wants.** **Chiller required flow is 420 to 1920 gph** |

**10 lines specified and not bought.**

---

# SECTION C. REQUIREMENT ONLY

**Nothing here is chosen. Each line is a requirement plus a search term, and the
owner runs every lookup under G-15.** A line in this section is finished work, not an
omission.

**Qty reads `not stated` wherever no row in the tree supports a count.** It is not a
gap to fill with a plausible number.

## C.1 The main panel

| ID | Requirement | Search term | Qty | Notes |
|---|---|---|---|---|
| C-01 | **Five gasketed 22 mm top-face devices AS ONE FAMILY**: E-STOP momentary NC mushroom, RESET momentary NO, PL-G green, PL-R red, PL-Y yellow | `22 mm pilot device IP66 gasketed panel thickness range`; `emergency stop rating actuated position sealed` | **5** | Derived from `parts.md`, "The main panel face, as decided": five door-mounted devices, five 22 mm holes, step drilled, and nothing else penetrates that face. **ONE SERIES FOR ALL FIVE - three families is three gasket systems, three thickness ranges and three torque procedures on one face, validated by nobody.** **The hole diameter is not the seal. The sleeper is the range of PANEL THICKNESS the device accepts, so measure the face and check it against every candidate.** **The E-stop's rating must be stated IN THE ACTUATED POSITION** - D-048 makes this the only E-stop there is, so it does not get to be marginal. **PL-Y is a lamp across the outgoing 24 V rail downstream of KM-DRV, D-045, so it is 24 V class specifically and is exempt from G-24** |
| C-02 | **RESET contact blocks: at least one NO and one NC** | `22 mm push button contact block NO NC stack depth` | **not stated** | The NC block sits in series with K-DRY's seal-in. **K-DRY latches and cannot be cleared by a normally open button and cannot be cleared from the permissive bus, because a dry tank does not drop the permissive under G-25, so the bus never interrupts.** **Three blocks if it also proves the lamps.** Stack depth per parts.md lookup 10, Schneider XB5A with ZBE blocks measured from the front face with the gasket compressed: 1 row 43 mm, 2 rows 55 mm, 3 rows 68 mm. **A DOUBLE BLOCK IS TWO ROWS. Side-by-side blocks add no depth; only stacked rows do** |
| C-03 | **In-panel parallel burden for PL-G and PL-R** | `pilot lamp burden resistor minimum contact load` | **not stated** | G-24 and F-056. **The 300 mW floor must be met at the BOTTOM of the trim range, 23.76 V, not at 24 V** - through a fixed series resistance, delivered power falls as the SQUARE of the rail voltage. **PL-Y is exempt, being across a supply rather than on a contact.** **Keep the lamp elements low-current and long-lived and put the burden inside the panel**: on a gasketed upward-facing face a higher-current element is a maintenance cycle on the one face where the seal matters most, and every element replacement there is a RE-SEAL EVENT |
| C-04 | **S-03 sense branch: one optocoupler with its series resistor, sized for about 12.5 mA at 24 V against the 55.34's 300 mW floor, evaluated at 23.76 V** | `optocoupler forward current series resistor 24 V dry contact sense` | **not stated** | **DO NOT COPY S-08. Same shape, different numbers, and that is why it is not a copy.** At 12.5 mA a single series branch carries the whole loop and the LED sits in its normal band. **Copying S-08's two-branch arrangement onto it would add a part for nothing.** **The burden sits in the MAIN PANEL**, so the contact stays wetted even if the cable is unplugged. **Sense reads INVERTED.** F-056: S-03 was specified as a POINT ON THE FLOOR and does not survive the trim's low end |
| C-05 | **S-08 sense branches: one optocoupler with a series resistor AND one bare burden resistor in parallel, sized together so the contact sees 45 to 55 mA against the 22.32's 1000 mW floor** | `optocoupler continuous forward current rating 40 mA`; `burden resistor power rating 24 V 50 mA` | **not stated** | parts.md records this circuit as GIVEN by the owner. **Do not re-derive it.** At 42 mA an optocoupler LED is near its continuous rating, which is why it splits into two branches. **The burden is in the MAIN PANEL: a power contact left switching 14 mA oxidises, and the failure of the cable must not degrade the contact it senses.** **The 45 to 55 mA WINDOW carries headroom and survives the trim's low end** |
| C-06 | **Coil suppression, FAST RELEASE grade, located AT THE COIL** | `coil suppression diode versus diode zener versus RC snubber release time`; `DIN rail relay socket coil suppression module compatibility retaining clip` | **3** | **order.md item 4.** Covers K-PERM, K-DRY-Q and K-DRY-P. **ADD ONE, to four, ONLY IF K-PERM SPLITS. That decision has not been taken. Do not buy four because B-01 buys four gold relays - see cart audit CA-04.** **The usual freewheel diode lengthens drop-out, and these are safety-chain devices where a slower drop is a real cost.** **Placement at the coil rather than at the driving contact is load-bearing under G-30.** The 99.01 module fits the SMA socket alongside the metal clip; **if a chosen element does not, it lands on terminal blocks and becomes terminal-plan work** |
| C-07 | **Coil suppression, ORDINARY grade, located AT THE COIL** | `relay coil freewheel diode DC`; `contactor DC coil surge suppression module` | **3** | **order.md item 5 states FOUR. THREE OF THEM ARE THIS LINE - K-FILL-S, K-FILL-D-Q and K-FILL-D-P. THE FOURTH IS C-08 AND IT IS BLOCKED. Three plus one is order.md's four. DO NOT ADD THIS LINE TO C-08 AND THEN TO order.md AGAIN** |
| C-08 | **Coil suppression for KM-CHIL's coil** | as C-07, **plus** `AC coil suppression electronic coil contactor` | **1** | **BLOCKED, and the blocker changed since order.md was written.** order.md held this element on 2026-09-01 because the element choice depends on what switches it, D-064, and it recorded the coil as a 24 Vdc contactor coil. **D-201 has since made KM-CHIL a motor-rated contactor whose coil is 100 to 250 V AC or DC, so the coil order.md assumed is no longer the coil.** Blocked with B-06 on the same rung |
| C-09 | **Timing element, if one is needed at all. MUST FAIL TO PROTECTION ACTIVE, NEVER TO BYPASSED** | `timing relay behaviour on power up and power interruption fail safe` | **0**, conditionally | **order.md item 6 reads "0 or 1" and names its own condition: only if the S-05 fork lands FLOW-PROVING. D-119 closed S-05 LEVEL-BASED - "everything in this system is level switches, there is no flow element anywhere and there is not going to be one" - so the condition order.md names did not happen and the count is zero.** **What is NOT settled by that, and must be confirmed rather than assumed: F-040's dry-run BYPASS timer is a separate demand from order.md item 6, and a timer stuck in the bypassed state defeats dry-run protection permanently and silently.** Cart audit CA-06 |
| C-10 | **DIN terminal blocks, 6.2 mm per way** | `DIN rail terminal block 6 mm pitch screw clamp 600 V` | **not stated. 57 clamps is a FLOOR** | main-panel-plate-area section 9: **57 clamps is a floor and the panel-internal conductor list is still unwritten.** parts.md lookup 7: 6.2 mm per way, **70 mm vertical envelope including the DIN clip, 44 mm above the rail, 56 mm off the rail face.** **The parallel build carries 129 conductors on 51 terminal footprints, which says the floor is close to final rather than about to double - that is an IMPORT under G-53 and not this build's number.** **DOUBLE-DECK BLOCKS ARE OUT, D-190: on a series interlock chain a tier slip does not short like to like, IT BYPASSES THE PROTECTION and makes a float permanently MADE** |
| C-11 | **Terminal end plates and end stops** | `DIN terminal block end plate end stop` | **not stated** | parts.md lookup 7: **end plates add 1 to 2 mm outside the pitch** |
| C-12 | **DIN rail** | `DIN rail 35 mm slotted steel` | **not stated** | D-199 gives the box's available rail as 814 mm, two rails at 407 mm usable, against 584.2 mm of demand. **That is what the box HAS, not what to buy** |
| C-13 | **Wire duct, two vertical runs dedicated by class** | `wire duct fill 50 percent NFPA 79`; `slotted wiring duct sizes` | **not stated** | main-panel-poles: two vertical wireways, one per side, **120 V down one and 24 V plus signal down the other, never sharing a duct and crossing once at right angles at a defined point.** parts.md lookup 3: inch widths 0.5, 0.75, 1, 1.5, 2, 2.5, 3, 4, 6. **FILL IS 50 PERCENT OF INTERIOR CROSS-SECTION, from NFPA 79 section 13.5.2, NOT NEC.** Knock nominal W x H down to about 90 percent for wall thickness, then fill 50 percent of that. **Shop practice designs to 30 to 40 percent so the cover still snaps on. The LIMIT is 50.** **Size it for fill before placing rails, not after** |
| C-14 | **Panel hook-up wire, by class and colour** | `MTW hook up wire 600 V panel`; `control panel wire colour code function` | **not stated** | **Insulation carries FUNCTION, which is what an electrician reads. The MARKER carries CHANNEL.** colour-map-proposal.md, not frozen. **BOSS states no standard from memory and asserts no reservation as fact: which colours are reserved, and by what document, is a lookup** |
| C-15 | **Cord grip, one per entry, sized to the cable actually chosen, sealed at least to the enclosure's own rating and suitable for the face it lands on** | `liquid tight cord grip strain relief NPT cable range chart` | **15 for the MAIN PANEL bottom face. Not stated elsewhere** | **The fifteen is main-panel-plate-area section 2.1 and is a returned count: eleven became fifteen when lookup 11 moved the four receptacle feeds off the face and onto grips.** **INTERCONNECT returns NO gland count, position or spacing for any other enclosure** - those wait on M-02. Also needed: one per tank cord exit at build-book 20-07b and 30-01, and one for the WB200 at D-163. **parts.md lookup 1: USE 1.10 IN CENTRE-TO-CENTRE FOR 3/8 NPT AND 1.30 IN FOR 1/2 NPT; mixed pair 1.15 to 1.20 in.** **G-52: the geometric floor is NOT the flat width. Across-corners is about 1.15x flats and that is what collides first WHEN A NUT ROTATES. A spacing that fits two nuts sitting still does not fit two being tightened** |
| C-16 | **Local ground bar, one per REMOTE enclosure, mountable in a plastic box. NOT a DIN-rail grounding block** | `copper ground bar kit enclosure mount insulated standoff`; `equipment grounding bar screw terminal copper` | **3** | **DERIVED, and the rows are D-165 and `parts.md`'s enclosures table.** D-165: a copper bar in the main panel, and **each remote enclosure has its own LOCAL BAR**, with a green conductor inside the cross-box cable joining it home. parts.md names four enclosures: main panel, two pump boxes, display box. **Main panel is covered by A-22's two bars, so three remain: pump box A, pump box B and the display box.** Build-book 14-08a: **the boxes are plastic and offer no bonding path at all, so a green conductor arriving has nowhere to go unless a bar is here.** **See warning 4.1: NOT a DIN-rail grounding terminal block** |
| C-17 | **Inter-bar jumper for the two main-panel bars** | `ground bar bonding jumper 6 AWG` | **1** | D-192 condition 1: **the inter-bar jumper is NOT a landing. It is fitted first, it is never removed to free a way, and it is not a terminal anything else may share.** If it is treated as a landing, somebody eventually removes it to make room, **and at that moment half the equipment grounds in the build are floating.** **Fitted before anything else lands, and C-25 measures continuity across it with a meter** |
| C-18 | **Fuse element for B-05, 5 x 20 mm, TIME DELAY, sized against a 27 W USB-C brick's plug-in surge** | `time delay fuse switch mode power supply inrush`; `5 x 20 mm slow blow fuse rating` | **not stated** | main-panel-plate-area 8.3: **a switch-mode supply charges its input capacitor on connection, so a fast-acting element sized on running current will nuisance-blow.** The brick's running current is 0.23 A. **The five 3 A glass fuses at A-26 are a holding, not a specification - nothing states the rating this line needs** |
| C-19 | **A hood, shield or sloped cap for the top face** | `enclosure rain hood drip shield`; `sloped enclosure cap` | **not stated** | D-110 closes F-025 **on the enclosure** at IP65 and explicitly leaves the top-face half live as its own item under G-35. main-panel-buy: **five gasketed devices on an upward-facing surface give five compliant seals and one non-compliant system.** An upward face COLLECTS AND HOLDS INDEFINITELY; a vertical face sheds. **The gasket is the youngest part of the assembly and it ages, and what is directly inside is the permissive-chain relays.** **Every requirement is a constraint rather than a part:** must not compromise E-stop reachability or the force an operator can apply; must not hide the three lamps from the normal sightline; must shed away from the box and not onto the bottom face where every cord grip lives; must be removable without breaking any device seal. **G-48: SLOPING THE SURFACE IS WORTH MORE THAN COVERING IT. A surface that sheds needs no hood, and that is zero parts and zero steps against one part, one fixing and one removal procedure** |
| C-20 | **Wall fixings for the four enclosures, suited to the wall construction recorded at build-book 5-02, rated for each enclosure's loaded weight in shear** | `enclosure wall mounting bracket load rating`; `fastener corrosion resistance damp location` | **not stated** | Build-book 10-02, blocked on the mounting position. **Four enclosures, but no file read for this document states a fixing count per enclosure** |

## C.2 The wet side and the field

| ID | Requirement | Search term | Qty | Notes |
|---|---|---|---|---|
| C-21 | **Float switch.** SPDT changeover, cord length reaching from its trip mark to the panel gland without a splice, contact duty against a 24 V DC INDUCTIVE load, body and cord materials compatible with permanent immersion in a pH-adjusted nutrient solution | `float switch minimum switching load milliwatts low level dry circuit`; `pilot duty float switch DC contact rating inductive relay coil`; `AC pilot duty rating versus DC rating same contact float switch`; `SPDT changeover tethered float switch normally open normally closed both legs`; `float switch available supplied cord lengths options`; `float switch cable jacket voltage rating 600 V submersible`; `external cable weight tethered float switch differential versus tether length`; `float switch float body material compatibility fertiliser solution long immersion` | **8** | **DERIVED, and the row is D-127: the roster accounts for EIGHT POSITIONS with no gaps and no spares, four on the day tank and four on storage. D-127 is a ROSTER OF POSITIONS, not a parts list.** **THE FLOAT PASS RESTARTS FROM REQUIREMENTS, D-118. The LS-1 to LS-8 part roster was struck: it came from the same body of work as the 1st Edition set, so checking it against those drawings would have been checking a document against itself, G-37 inside the authoritative file. G-40b does NOT apply here and the old roster carries no priority for having been here first.** **F-089: the 1st Edition floats switch a 120 VAC coil and this build's control voltage is 24 V - under G-31 that is a fifth of the contact power at the same current.** **F-112: it is also AC to DC, and the load is INDUCTIVE. A DC inductive break is a different contact problem from an AC one at the same power.** **BLOCKED ON THE CORD SPAN, F-100 and build-book 6-07. See read-me section 6.** **Each float's cord is insulated for 600 V because it shares the standpipe with pump cords, D-156** |
| C-22 | **Overflow bulkhead fitting, one per tank**, seating on the flat land found at build-book 20-02, sized to swallow the full inflow with the fill-stop failed, **large relative to the debris it will meet and inspectable without disassembly** | `bulkhead tank fitting flat mounting surface curved tank wall gasket`; `polyethylene tank overflow bulkhead fitting installation`; `tank overflow line sizing gravity full inflow rate` | **2** | D-130, both tanks. **The single largest cost is not the fitting: it is that the hole CANNOT BE MOVED, and both tanks are already bought.** **A gasket needs a flat land and one of the two tanks is a cone bottom - a bulkhead gasket seating on a curve is a leak that appears later.** **Do not fit a screen: an open port in an open-top tank collects debris and grows biofilm at the waterline, it fouls silently, it is the last line with nothing behind it, and a screen makes a visible failure into an invisible one.** **SIZING IS NOT INHERITED FROM D-109's 3/4 in** - the overflow's capacity requirement has a different driver |
| C-23 | **U-bolt and backing plate that clamp the standpipe over the tank's lip without crushing the lip, in a material that will stand in a fertiliser solution atmosphere** | `U-bolt with backing plate pipe clamp`; `tank rim pipe mounting bracket` | **2** | Build-book 18-01. **One per standpipe, two standpipes** |
| C-24 | **Storage tank support that carries the tank FULL, suits the tank's form, leaves its outlet reachable, and stands on the floor the drain track runs across** | `tank stand load rating`; `conical tank stand` | **1** | Build-book 16-01. **Read the tank's form in parts.md before looking for a flat place to stand it. A tank that cannot stand on its own bottom and is stood on one is a tank standing on its outlet** |
| C-25 | **Pump cradle holding a submersible at a fixed position and depth, taking NO load through the cord** | `submersible pump mounting bracket tank`; `pump cradle stand sump` | **2** | Build-book 27-01 and 27-02. **Both in the day tank: the manifold pump and the chiller loop pump, and D-137 records that both run continuously.** **Position held by fixture, not by cord. A cord-hung pump is a pump whose position is a suggestion**, and G-11 puts the manifold pump's suction at the day tank bottom so the tank mixes |
| C-26 | **Rigid fixture holding the fill line's discharge end over the storage tank, clear of the standpipe, the transfer suction and the overflow** | `pipe support bracket tank rim`; `rigid pipe stand-off bracket` | **1** | Build-book 25-04. **With an air gap the discharge end is unsupported by definition. A fill line that has swung out of position discharges onto a floor or onto the rim** |
| C-27 | **Solvent cement and primer for the pipe material D-121 and D-109 settle, rated for the products this loop carries, with a STATED CURE TIME at the room's temperature** | `PVC solvent cement cure time chart temperature`; `solvent cement chemical resistance fertiliser solution` | **not stated** | Build-book 11-01. **Every cure step in that book reads a time off that label, so without it nothing in sections 11, 17, 24, 25, 26, 27 or 28 can be cured or confirmed** |
| C-28 | **Cable tie that holds a clamped weight in position under permanent immersion in a fertiliser solution, and that a person can cut and replace at a level adjustment for the life of the machine** | `cable tie chemical resistant permanent immersion`; `UV and chemical resistant cable tie material selection` | **not stated** | Build-book 22-01 to 22-08 clamp with one; 22-11, 22-13 and 27-06 tie with one. **The tie IS the trip height - commissioning adjusts the tie and never the wiring.** **A consumable that a step names is a consumable that has to be bought** |
| C-29 | **Paint pen whose mark survives PERMANENT IMMERSION in a fertiliser solution on the pipe's material** | `paint marker permanent immersion chemical resistant` | **not stated** | Build-book 21-11. **The mark is the only record of where a float is supposed to be. A pencil line under water for a season is a mark that disappears exactly when somebody comes to check whether a float has slipped** |
| C-30 | **Marker whose mark stays legible on the device it is written on for the life of the machine, inside a warm enclosure** | `permanent marker plastic metal smear resistant`; `industrial equipment marking pen` | **not stated** | Build-book 3-02. **G-28 applies AT DELIVERY, not at installation: label each relay BY NAME to its envelope the moment it is unpacked, never by position.** **The two types look alike and a swapped pair is a defect that passes every check** - the gold relay silently degrades in a power envelope and the standard one carries the Pi-facing signals with the 300 mW floor and no gold. **The step is not blocked on this line: its acceptance condition tests the requirement at the bench. If it smears, stop - that is a purchase** |
| C-31 | **Wire marker carrier holding the canonical three-part TRM- form AND, on a per-channel core, the channel token in addition, WITHOUT merging them** | `wire marker sleeve character capacity heat shrink printable` | **not stated** | D6 section 5. **The channel colour is carried on the MARKER, not on the conductor insulation** - the insulation carries function, which is what an electrician reads; the marker carries channel, which is what an operator reads. colour-map-proposal.md asks for **colour-through or otherwise non-printed carriers**, which is a marker technology and not an insulation one |

## C.3 Cables and crossings

| ID | Requirement | Search term | Qty | Notes |
|---|---|---|---|---|
| C-32 | **RUN-001 to RUN-008, the cross-box jackets: a multiconductor control cable CARRYING A GROUNDING CONDUCTOR in addition to its circuit conductors, insulation rated for the highest voltage anywhere on the bar it lands at rather than for its own circuit** | `multiconductor control cable with green ground conductor 600 V`; `control cable 600 V insulation rating low voltage circuit` | **not stated** | D6 section 5. **D-165: one green conductor per CABLE rather than one per DEVICE, which is why the cross-box cords are three-conductor rather than two.** **A ground bar is ALWAYS IN THE 120 V CHAIN even in a box holding only 24 V, because the ground is common.** **No cut length is stated. The five cross-box wall runs in parts.md are an IMPORT from the parallel build's wall under D-206, order-of-magnitude only, and NOTHING IS CUT TO THEM.** D-090 freezes the cut rule for this build: wall run plus 3 ft, made of 6 in drip loop per grip and 12 in service per end. **T-020: the allowance is folded into the cut step and never stated after it** |
| C-33 | **RUN-010, RUN-011, RUN-015, RUN-018 to RUN-020: a flexible LINE-class cable for a wall route in a room where water moves tank to tank, with an equipment grounding conductor, rated for the make-and-break event of an inductive coil load** | `flexible power cable 600 V oil resistant wet location`; `tray cable TC-ER exposed run wall` | **not stated** | D6 section 5 |
| C-34 | **RUN-012 and RUN-013: a control cable for a dry-contact pilot circuit at whichever voltage class the permissive string settles at, on a route that includes a wet zone** | `instrumentation control cable 300 V vs 600 V dry contact multiconductor` | **not stated** | D6 section 5. **Blocked on one sentence: the permissive string's voltage class, which decides RUN-012, RUN-013 and RUN-015 together** |
| C-35 | **RUN-016: the MAXIMUM PROBE CABLE LENGTH the EZO circuits tolerate. NOT FROM ANY FILE IN THIS TREE** | `Atlas Scientific EZO pH EC probe cable length limit extension` | **not stated** | D6 section 5. **The probe run is within 6 ft of the display box, the same run as the tank** |
| C-36 | **RUN-009: a panel-mount USB-C bulkhead for the display box face, sealed to at least the box's own rating in a bottom-face orientation** | `panel mount USB-C bulkhead pass-through IP67 waterproof` | **1** | D6 section 5 and D-162. **A BULKHEAD, NOT A GRIP, and the reason is physical: a USB-C connector will not pass a grip bore, and cutting and re-terminating a USB-C cable is not a thing anyone should do** |
| C-37 | **USB-C cable, main panel face to display box bulkhead** | `USB-C cable 5 V 27 W length` | **1** | D-162: what crosses to the display box is 5 V DC over a USB-C cable, NOT LINE. **Its length follows the wall run and M-02 is open** |
| C-38 | **27 W USB-C power supply for the Pi** | `27 W USB-C power supply Raspberry Pi 5` | **1** | D-162: **the AC-DC conversion is OUTSIDE BOTH ENCLOSURES - a brick hanging outside the main panel, in neither box.** It plugs into the UNSWITCHED receptacle at B-08/B-09. **Its running current is 0.23 A, which is irrelevant to B-05's indicator and relevant to C-18's fuse rating** |
| C-39 | **A segregation RULE: which classes may share a duct, a jacket, a clip run or a tie bundle, what an unavoidable crossing requires, and what the standpipe bundle requires** | `control panel power and signal circuit segregation separation barrier`; `Class 1 Class 2 circuits same raceway` | **n/a, not a part** | D6 section 5. **Listed here because it is a lookup the owner runs and it changes what cable is bought at C-32, C-33 and C-34.** It buys nothing itself |

## C.4 Pump boxes and dosing

| ID | Requirement | Search term | Qty | Notes |
|---|---|---|---|---|
| C-40 | **Stick-on heatsink for the Adafruit 6121** | `TMC2209 stepper driver heatsink adhesive`; `stick on heatsink 9 mm TO-package` | **8** | **DERIVED: parts.md states "Each driver needs a stick-on heatsink" and A-08 holds eight drivers.** Build-book 14-07: **NOT OPTIONAL AND CANNOT BE ADDED LATER. The motor bodies and the drivers sit in one sealed plastic box and nothing has measured the temperature rise.** C-15's own precondition is boxes populated and closed WITH heatsinks fitted, **so a box built without them cannot even be measured**, and G-06's one-pump-at-a-time thermal constraint stays mandatory until C-15 exists |
| C-41 | **The S-10 pull-down landing and its pull-down components, at the DRIVER end** | requirement returned by PUMP-BOXES; **no search term is stated in anything read for this document** | **not stated** | **BLOCKED. S-10 is an OPEN interface row and nothing may be built against it, rule 9.** Build-book 14-08: **a pull at the display end does nothing once the conductor is cut**, so the component has to be at the driver end, inside the box. **D-096 reverses the direction the tree first recorded: A FLOATING DIR FLOATS HIGH, via the board's green LED branch pulling up to VDD through 20 k, which beats the chip's 166 k typical internal pulldown by an order of magnitude.** **F-049 makes this a GATE and it has a deadline: DIR level to rotation, and rotation to flow through the head AS MOUNTED, are settled BEFORE the S-10 cable is bought and before any resistor is fitted** |
| C-42 | **PharMed BPT tube, code B25 / 25#, 4.8 mm ID x 8.0 mm OD, 1.6 mm wall - a SPARE set** | `PharMed BPT tubing 25# peristaltic pump` | **not stated** | parts.md: **the tube is a consumable, about 1000 h.** A worn tube delivers less per revolution while every instrument reads healthy. **The re-measure trigger is a TUBE CHANGE, not a date.** **The head ships with its fixed tube installed; nothing read for this document states a spare set as bought or states how many** |
| C-43 | **3/16 in straight barb connector, to mate the 4.8 mm ID tube** | `3/16 inch straight barb connector chemical resistant` | **not stated** | parts.md manufacturer figures. **DOSING's tubing selection is an OPEN item and the count follows from it** |
| C-44 | **Dose delivery and head suction tubing**, selected against the head barb and against nutrient chemical compatibility | `peristaltic dosing tube chemical compatibility fertiliser`; `tubing 3/16 ID chemical resistant` | **not stated** | dosing.md open item. **The fixed-tube null head means external tubing joins at the ends of a SHORT installed BPT loop, so the jug-change break point sits on EXTERNAL TUBING and never on the pump tube**, G-18 |
| C-45 | **Nutrient jug, one per channel, DEDICATED FOR LIFE** | `chemical resistant jug HDPE narrow mouth` | **8** | **DERIVED from the eight channels CONTROL-SOFTWARE declares under S-19.** G-17: jugs are dedicated per channel for life, not interchangeable vessels; **a jug is refilled with the same product forever or it is retired.** **The channel token goes on the JUG BODY permanently as well as on the station.** **No size is stated: D-105 made product-to-channel an ASSIGNMENT rather than a design-time fact, so any size argument keyed to a fixed pH pair is moot, F-063 dissolved** |
| C-46 | **Probe wet fitting, one per EZO probe, per the probe body** | `Atlas Scientific probe compression gland PVC`; `pH probe 3/4 NPT wet mount fitting` | **3** | **DERIVED: A-11 holds three EZO circuits and G-10 puts all three in the vertical manifold section ahead of every injection point.** dosing.md open item, requirement and search term only |
| C-47 | **Injection port in PVC, downstream of every probe**, and whether a port needs a check to stop backflow into a dose line when its head is idle | `PVC injection quill port fitting`; `dosing line check valve siphon prevention` | **not stated** | dosing.md open item. **Report the requirement, do not pick a part.** G-10 is the constraint: no injectate reaches a probe before mixing |
| C-48 | **Flow cell body: a PVC body that holds the probes in the moving stream** | `PVC inline probe flow cell 3/4 inch` | **not stated** | D-007 and S-13. **IT IS A FITTING, NOT AN INSTRUMENT. No output, no contact, no wire. Do not build a sensor pocket, a tapping or a wire route for it** |
| C-49 | **Receptacle device for each of the four wall boxes**, to suit the Bell 5320-0 yoke, strap holes 3.281 in apart | `15 A duplex receptacle weatherproof box mount` | **4** | Follows B-08. **P-03 transfer pump, P-04 manifold pump, P-05 chiller and loop pump, P-07 the Pi brick. P-07's is UNSWITCHED and fused; the other three are switched.** **P-05 is an OPEN interface row** |
| C-50 | **Eight fixed, ordered, tokened jug stations**: the mounting that holds each jug at its assigned position and height relative to its head | `jug rack shelf chemical storage`; `carboy stand adjustable height` | **8** | DOSING owns the jug station. **Height relative to the head decides whether a head is asked to lift more than it can and whether a dose line can siphon when the head is idle, and both are DOSING open items.** F-064: the ordering rule constrains the SEQUENCE of the eight tokens and says nothing about the SPACING between them, **so spacing is free and what may NOT go in a gap is another channel** |

**50 lines requirement only.**

---

# SECTION D. N/A WITH REASON. G-46

**These lines can never be filled here.** Each is recorded so that a blank does not
read as work outstanding, and so that a helpful buyer does not fill one in.

| ID | Line | Why it can never be filled | Grade |
|---|---|---|---|
| D-01 | **Main disconnect** | **NO PART, AND ZERO RAIL MILLIMETRES.** D-200: a lockable 2-pole building breaker upstream opens both incoming legs together and can be locked OFF. **OSHA and NFPA 79 care that the source is isolated and locked, not that a second isolator sits on the plate. G-48's question, asked first, returned the best possible answer: the requirement was already satisfied by something already there.** **What would revive it, recorded rather than bought against: a DIN isolator earns its place ONLY IF a local VISIBLE open point is needed without walking to the building panel, or if the two entering circuits are not on the same 2-pole breaker. Neither holds.** If that changes: ABB SD202/25, 2P 25 A load-break, 35 mm, padlock adapter 2CDD282001R0001 | **CURRENT.** Named what would change it |
| D-02 | **Panel-mount receptacle in the enclosure face** | **THE PART DOES NOT EXIST AND THE ARRANGEMENT WAS REMOVED.** parts.md lookup 11: a standard 15 A duplex does not panel-mount at all. **D-197: D-046 is CORRECTED rather than annotated, because a frozen decision that a part cannot obey is not a decision, it is an error.** **The four receptacles left the plate entirely** and became wall-mounted device boxes fed by cord grips, which is B-08 and B-09. order.md's closing list carries "the two panel-mount receptacles per D-046" as not covered; **it can never be covered.** **A single snap-in 5-15R does panel-mount, cutout 26 x 22 mm - and this build does not use one** | **STRUCTURAL.** No addition makes a duplex panel-mount |
| D-03 | **DIN-rail grounding terminal block** | **THEY BOND TO NOTHING.** The block bonds to the rail, the rail bonds to the plate, **and the plate is plastic** - D-195 confirms the mounting plate is PC/ABS and the box polycarbonate. **The parallel build bought seven before the ground bar decision and is returning them, D-166.** **Nothing in this tree assumes them: parts.md, order.md, electrical-schematic.md, both schedules and interface-table.md were searched and every one already says ground bar.** **An IMPORT under G-53** | **STRUCTURAL** while the plate is plastic; **D-195 records it as a DEPENDENCY: if the plate were steel the same part would create exactly the split D-192 forbids, and nobody would see it because the block looks identical either way** |
| D-04 | **Interposer relay** | **ZERO.** order.md: G-26 leaves one Pi-driven coil and the browser package already drives it. **Correction A from main-panel-buy stands and is why the count is zero rather than one: both contactor coils were the same part with the same coil, so the answer was 0 or 2 and never 1 - recording them as two independently contingent relays invites buying one, and there is no world in which one is right** | **CURRENT.** G-26 and D-052 would have to move |
| D-05 | **Suppression across KM-DRV's coil** | **ZERO.** order.md: **SUP-1 is already across it in the corrected package, taken as given and not respecified.** parts.md: the Pi drives ONE coil, BCM 18, through a ULN2003 sinking the coil return, **with SUP-1 across the coil** | **CURRENT.** S-09 would have to move |
| D-06 | **Auxiliary contact block for the Finder 22.32** | **THERE IS NO AUXILIARY CONTACT BLOCK ON THE 22.32. NONE IS IN THE PARTS LIST AND NONE WAS EVER BOUGHT**, D-029, given by the owner. **A 25 A power pole IS the readback contact: pole 1 carries the 24 V rail out to both pump boxes, pole 2 was unwired and free and the readback was granted onto it.** **F-051's shape: five files plus parts.md call it an "auxiliary contact", which is a name not on the part** | **STRUCTURAL** for this part |
| D-07 | **Flow meter per channel, and any flow element anywhere** | **D-014 put O-19 off the table and said do not bring it back unless something changes. D-119 is stronger: "everything in this system is level switches. THERE IS NO FLOW ELEMENT ANYWHERE AND THERE IS NOT GOING TO BE ONE."** **F-095's overflow-detection question was LOGGED AND NOT PURSUED on the same grounds: a flow switch is the obvious device and D-119 forecloses it, and under G-44 nothing is added** | **CURRENT**, and the owner's decision is what would change it. **The residual is recorded rather than solved: a fill-stop failure is caught by the overflow and reported by nobody** |
| D-08 | **Jug level sensor** | **G-05 forbids it outright: no level sensors on the nutrient jugs, remaining volume is arithmetic against a user-entered full-jug volume, per channel. "Do not add jug floats"** | **STRUCTURAL.** A frozen rule |
| D-09 | **A second Finder 22.32 for KM-CHIL** | **THE 22.32 IS THE WRONG PART, D-201.** Its 25 A is AC-1 RESISTIVE, its AC-3 motor rating is typically 8 A or less, and it is not built for compressor make and break. **KM-CHIL becomes a motor-rated contactor, B-06. The 22.32 that was KM-CHIL is FREED and is a spare - one unit, not the pair. KM-DRV is unaffected and keeps its job** | **STRUCTURAL** on the ratings |
| D-10 | **A replacement or additional main panel enclosure** | **D-199: the enclosure study is CLOSED, the box is the one on the shelf, D-196's 16 by 14 verdict is WITHDRAWN and no further enclosure is specified.** It clears on every axis: plate 468 x 379 mm against 374.65 x 327.15 called for, rail 814 mm available against 584.2 mm of demand | **CURRENT.** The demand figure moving would change it, and D-199 records why it will not: the parallel build carries 129 conductors on 51 terminal footprints, **which says the 57-way floor is close to final rather than about to double** |
| D-11 | **RUN-017, a separate bonding cable** | **RETIRED under D-149. D-165 removed it from the schedule rather than filling its cells: the EGC is a conductor INSIDE each run, not a separate cable.** The parent id goes and the conductors appear inside the runs they protect. **Nothing is renumbered around it and no suffix is issued** | **STRUCTURAL** under D-149 |
| D-12 | **The storage auto-fill add-on package: its own parts table, its own buy list, its own added floats** | **THERE IS NO SUPPLEMENT, SO THERE IS NO SUPPLEMENT'S PARTS TABLE.** document-plan 1.3: the old set built the storage fill as an add-on because it was decided after the base package shipped. **This build has the storage fill in scope from the beginning** - A-27 records the solenoid as ordered and fully specified, and D-127 puts float positions in both tanks. **That is the cheapest possible way to satisfy G-41 and T-028: the defect they were frozen against is a property of SUPPLEMENTS, and this set has none.** **The parallel build's add-on sheet listed four float switches where its own text said three arrive, and buying per both sheets gives nine floats for eight positions. C-21 carries all eight, once** | **STRUCTURAL** for this document set |
| D-13 | **A 12 VDC DIN-rail supply for the leak console** | **THIS BUILD FEEDS THE WB200 AT 24 V, D-163.** The 1st Edition carried a MEAN WELL HDR-15-12 as its one placeholder, shaded yellow, because its WB-200 needed 12 VDC and its panel had none. **That is observed in the 1st Edition set, UNVERIFIED under G-40, and where it disagrees with a frozen row the tree wins.** **It is nevertheless the sharpest thing in that workbook for this build and it is raised at cart audit CA-02 rather than dismissed, because if the module really needs 12 V then D-163's 24 V feed is wrong and this line comes back** | **CURRENT, and it is the one n/a line that could reopen.** What would change it: the WB200's actual supply range |
| D-14 | **A logic-side connector for the Adafruit 6121** | **IT SHIPS WITH THE BOARD.** parts.md, board in hand: **JP4 ships as BARE PADS with a 10-pin header strip supplied LOOSE and UNSOLDERED.** So the choice is soldered flying leads or a soldered connector, **not a plug-on assembly out of the box.** **Soldering it is a build step nobody had** - a step, not a purchase. **And it removed a landing argument rather than creating one: PUMP-BOXES ruled out putting a resistor lead into the driver's own screw terminal on T-009 and T-010 grounds, but there is no screw terminal on the logic side to rule out** | **CURRENT.** A different connector choice would create a part |

**14 lines n/a with reason.**

---

# CART AUDIT. WHAT TO CHANGE BEFORE YOU CHECK OUT

**The 1st Edition's workbook had this tab and it is the one thing in a purchase
package that only helps BEFORE money is spent.** Under G-40b it is adopted. This
build has no placed carts, so every item below is a check rather than an edit to an
order.

| # | Line | Check | Why it costs money if skipped |
|---|---|---|---|
| **CA-01** | **B-03, B-04, A-23, A-24** | **Read the LISTING on the two shelf breakers. UL 489 or UL 1077.** | **UL 1077 is a supplementary protector and is not legal branch protection under the NEC.** If they are UL 1077 you buy B-03 and B-04 and the shelf parts have no position. If they are UL 489 you buy neither. **Buying both ways is two breakers for one slot; buying neither leaves the panel unprotected** |
| **CA-02** | **B-07** | **Read the WB200's supply voltage range before ordering.** | D-163 feeds it 24 V. **The 1st Edition workbook carries its ONE placeholder for exactly this: its WB-200 needed 12 VDC and its panel had none, so it added a DIN 12 V supply. That is unverified under G-40 and a citation is not a source under G-37 - but it is a live contradiction with a frozen row in this tree, on a device neither build has confirmed here.** If it needs 12 V, D-13 comes back as a real line and RUN-014's class changes with it |
| **CA-03** | **B-10 against A-04** | **Count the submersibles on the shelf and confirm which one is the chiller loop pump before ordering the Aqua-Mag.** | **`decisions.md`'s owned table of 2026-08-30 says TWO hi-flow submersibles are held, one circulation and one chiller loop. D-137 of 2026-09-04 says the chiller loop pump is a separate submersible and IS BEING BOUGHT, and names the Danner Supreme Aqua-Mag 12 item 02712.** **Buying per both records gives three submersibles for two positions. That is G-41's exact shape, on a line where both records are the owner's.** **And if you do buy: NOT the venturi or air-fractionating version** |
| **CA-04** | **C-06 against B-01 and B-02** | **Buying four gold relays and three sockets does NOT mean K-PERM has split. Leave fast-release suppression at THREE.** | order.md gives 3 fast-release for K-PERM, K-DRY-Q and K-DRY-P, and 4 only if K-PERM splits. **MAIN-PANEL's four-gold recommendation is a spares argument, not a split decision: the fourth gold is used either way, as K-PERM-Q if the split happens or as the only gold spare if it does not.** **If the split is later decided, ADD ONE fast-release element and no relay and no socket, because both are already bought.** Write the add on this line when it happens; do not restate the total |
| **CA-05** | **A-28** | **Count the 94.74SMA sockets on the shelf before buying B-02.** | **Four in hand is DERIVED from order.md item 3's arithmetic, not recorded in `decisions.md`'s owned table.** If fewer are held, B-02's three is short by the difference and you find out with a relay in your hand and no socket |
| **CA-06** | **C-09** | **Confirm with MAIN-PANEL that F-040's dry-run BYPASS timer is not a separate demand from order.md item 6 before closing the timing line at zero.** | order.md item 6 is conditioned on the S-05 fork landing flow-proving and D-119 closed S-05 level-based, so item 6 is zero. **F-040 is a different element with a different job, and a timer stuck in the bypassed state defeats dry-run protection permanently and silently.** **Requirement if it is real: it must fail to PROTECTION ACTIVE, never to BYPASSED, and its behaviour on power-up, on interruption mid-bypass and on component failure must be stated BEFORE it is bought** |
| **CA-07** | **C-21** | **Do not buy floats until a BOUND on the cord span exists.** | **A float whose supplied cord does not reach is disqualified, and D-131's only remaining remedies are a splice in the wet zone or moving a mounted panel, both of which it forbids.** Build-book 6-07 records that a worst-case bound follows from D-090's 8 ft by 8 ft envelope and the cut rule with **no wall arrangement needed at all**, and that the test is a disqualification rather than a cut length. **That is one afternoon against eight floats bought against the wrong requirement** |
| **CA-08** | **A-16** | **Measure the box on the shelf before anything is cut or laid out.** | **`parts.md` lookup 2 describes a QILISU at overall 425 x 340 x 183 mm with a 359 x 271 mm plate. D-199 describes a Qilipsu at 508 x 419 x 201 mm with a 468 x 379 mm plate and says THAT is the box on the shelf.** Those are two different boxes. **Nothing is bought either way - D-199 specifies no further enclosure - but every rail, duct and gland position downstream reads one of the two figures** |
| **CA-09** | **A-22, C-16, C-17** | **Two bars are bought and both go in the MAIN PANEL. Three more are needed, one per remote enclosure.** | D-192 makes two bonded bars ONE ground point, on two conditions: **the inter-bar jumper is NOT a landing and is never removed to free a way, and the bars are NEVER split by class.** **Splitting 24 V grounds onto one bar and 120 V onto the other is the single-point rule defeated by tidiness.** **Both failures are SILENT - a missing or backed-out jumper leaves everything looking correctly built and nothing measures it**, which is why C-25 puts a meter across it before anything else lands |
| **CA-10** | **B-06, C-08** | **Do not order KM-CHIL or its suppression until the rung that decides its coil's bus is closed.** | **The AF09-30-10-13's coil code is 100 to 250 V AC or DC, and a 24 V bus is not inside that band.** The rung decides whether the Pi can stop the water system, which G-26 forbids, **so no part may be chosen first, rule 9.** Ordering against the wrong bus is a contactor with an unusable coil |
| **CA-11** | **Every relay line** | **Label each relay BY NAME to its envelope THE MOMENT IT IS UNPACKED.** | **G-28 applies AT DELIVERY, not at installation. The two types look alike.** A swapped pair is a defect that passes every check: **the gold relay silently degrades in a power envelope, and the standard one carries the Pi-facing signals with the 300 mW floor and no gold.** The marker for it is C-30 and it is not on this list as bought |
| **CA-12** | **All of section C** | **Run the terminal survey, `terminal-survey.md`, on every part as it arrives.** | **No decision, no lookup, no money - parts in front of you and something to write with. It closes the one thing that blocks all 111 rows of D4.** **Do not survey a part you have not got: a blank row that says NOT ON SHELF is worth more than a guess, and it tells the schedule which rows stay blocked** |

---

# THE COUNT

**Counted under G-46, which means the four states are counted separately and the n/a
lines never roll into a completion percentage.**

| State | Lines |
|---|---|
| **A. Already owned** | **28** |
| **B. Specified and not bought** | **10** |
| **C. Requirement only** | **50** |
| **D. N/A with reason** | **14** |
| **Total lines** | **102** |

**How to read that, and it is the thing G-46 exists to stop being read wrong:**

**38 lines carry a part** - 28 held and 10 to buy. **50 carry a requirement and a
search term, which under G-15 is finished work and not an omission.** **14 will never
carry a part at all.**

**A completion figure that mixes the states is wrong in both directions.** Against the
88 lines that could ever carry a part, 38 do. **Against all 102 it reads 37 percent
and flatters nothing, because 14 of those 102 are not work.** That is the same
arithmetic D6 met on first application of G-46: twelve cells previously counted as
filled were never fillable, and under the old two-state count it would have reported
169 of 180 and been wrong by twelve **in the flattering direction.**

**Of the 10 buy lines, 4 carry a hold that must clear before the money goes:**
B-03 and B-04 on the UL 489 check, B-04 additionally on the compressor nameplate
reading, B-06 on the open coil-bus rung, and B-10 on the submersible count.
**B-07 carries a check rather than a hold.**

**Of the 50 requirement lines, 13 are gated by a build-book step rather than by a
lookup**, which is the defect build-book section 33 reports against itself: D7 is
supposed to precede the book and cannot be finished before it starts. **C-21, the
floats, is the one that matters, and CA-07 names the cheapest way out of it.**

---

# WHAT THIS DOCUMENT DOES NOT CLAIM

**Not finished. INTEGRATOR does not declare itself finished, rule 7.** BOSS declares
that after another agent has built against this and found nothing.

**What is returned:** 102 lines in four states, every count carrying the row it was
derived from, both live purchase warnings on the face of the document, the
measurement-blocked line marked as such, and a cart audit with twelve checks.

**What is NOT returned, so no absence is read as an answer:**

- **No price anywhere.** No file read for this document states one.
- **No part number that is not already in the tree.** Every part named in sections A
  and B appears in `parts.md`, `order.md` or a `decisions.md` entry and is cited to it.
- **No quantity that is not either recorded or derived from a named row.** Every
  derived count says which row: D-127 for the eight floats, D-165 and the enclosures
  table for the three local bars, main-panel-plate-area 2.1 for the four receptacle
  feeds and the fifteen main-panel grips, order.md items 1 to 6 for the relay buy,
  parts.md for the eight heatsinks, S-19 for the eight jugs and stations.
- **No gland count, position or spacing for the pump boxes or the display box.**
  INTERCONNECT returns none and every one waits on M-02.
- **No cut length for any cable.** The five cross-box runs in `parts.md` are an import
  from the parallel build's wall under D-206 and nothing is cut to them.
- **No tool line.** Named in read-me section 7 rather than omitted.
- **No judgement on whether the shelf breakers are usable.** That is CA-01 and it is
  the owner's lookup.
