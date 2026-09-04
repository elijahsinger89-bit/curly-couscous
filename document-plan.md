# The document plan

BOSS, 2026-09-04. Written against G-44 and G-40b.

**What this file is.** A plan for the set of documents this build delivers, mapped
onto the set the 1st Edition delivered. It is not a document, it is a list of them.

**What it states.** No part number, no figure, no dimension, no quantity, no
terminal number, no page count. Counts of DOCUMENTS appear because the plan is
about documents.

**Provenance.** Everything about the old set below is **observed in the 1st
Edition set, unverified**, per G-40. What was read: `handoff/DRAWING-METHODOLOGY.md`
and `handoff/STATE-OF-PROJECT.md` in full; the build book's front matter and
contents sheet; the purchase workbook's Read me, Buy list header and Cart audit
header; sample pages of both wiring instruction sets; both one-page wiring
schedules; the commissioning checklist's procedure and first stage; the
maintenance log's baseline page; the headers of the schematic, the plate sheet,
the receptacle schematic and the dosing wall sheet; both standpipe sheets; and the
add-on's one-page sheet and its buy-list-and-commissioning sheet.

**Tree side, read in full or in the part named:** `agents.md`; the G-rule table in
`decisions.md` and D-094, D-095, D-135, D-148 to D-152; `interface-table.md`
including the reserved namespace and the gland allocation; `commissioning.md`;
`parts.md` section headings and the named sections; `order.md`; `traps.md` T-028
and T-029; `wire-table-row-zero.md`; `channel-register.md`; `channel-token.md`;
`colour-map-proposal.md`; `subsystems/interconnect.md`,
`subsystems/interconnect-first-pass.md` sections 2.3 to 2.5 and
`subsystems/interconnect-schedules.md` Parts C, D and E;
`subsystems/main-panel-ladder.md`; and the section headings of every other
subsystem file.

---

## 1. THE DOCUMENT LIST

### 1.1 What the 1st Edition set contains

Nineteen documents in three groups. Observed in the 1st Edition set, unverified.

| # | Document | What it is | Who reads it | When | Needed here |
|---|---|---|---|---|---|
| 1 | Build book | The drawing set. Overview, legend, tank and loop sheets, manifold and probes, the electrical ladder, a schedule-and-parts sheet, the dosing wall, the wall allocation, and detail sheets for floats, fill, chiller hoses, probe cables and receptacles | The builder | Throughout, from first plumbing to last | **YES, reshaped** |
| 2 | Purchase package workbook | Read me tab, Buy list tab, Cart audit tab. Every part, one line each, with a search term and a status | The buyer, once | Before anything is bought | **YES** |
| 3 | Panel wiring instructions | One page per wire. From, to, clamp, route, six identical connection steps | The person with strippers in hand | During panel wiring, page by page | **YES** |
| 4 | Panel wiring schedule, one page | Every panel wire on one sheet. Generated from the same wire list as #3 | The same person, to tick off and to check | During and after panel wiring | **YES** |
| 5 | Panel wiring schematic | The ladder, large format, with a wire schedule table on the sheet | The builder and anyone diagnosing later | Before and during wiring, and forever after | **YES, narrowed** |
| 6 | Panel physical wiring | The backplate face-on, every wire drawn as a route on the plate | The builder, for orientation | Before wiring, to see where things sit | **YES, narrowed** |
| 7 | Receptacle wiring instructions | One page per receptacle conductor | The builder | After panel wiring | **NO, dropped** |
| 8 | Receptacle wiring schedule, one page | Same conductors, one sheet | The builder | Same | **NO, dropped** |
| 9 | Receptacle schematic | One box detailed, then the boxes as installed | The builder | Same | **NO, dropped** |
| 10 | Commissioning checklist | Staged procedure, each stage ending in a gate, with prerequisites and a fault-finding table | The commissioner, on paper, pen in hand | After the build, before service | **YES** |
| 11 | Maintenance log | A baseline page filled once at commissioning, then periodic pages | The operator | At commissioning and forever after | **YES** |
| 12 | Plotter sheet | Single-sheet general arrangement: the P&ID and the ladder on one large sheet | Anyone wanting the whole machine at a glance | Any time | **NO, dropped** |
| 13 | Dosing wall | Wall elevation plus the relay box interior, as a standalone sheet | The builder | While building the wall | **YES, folded** |
| 14 | Float standpipe assembly | How the day tank standpipe is built, hung and clamped, with its own parts table | The builder | Before floats go in a tank | **YES, folded** |
| 15 | Storage auto-fill sheet | The add-on's plumbing, its ladder rungs, its new terminals and wires, and a parts table | The builder of the add-on | After the main build | **NO, dropped as a package** |
| 16 | Storage auto-fill wiring | One page per new wire, numbered so it cannot collide with the base set | The builder | During add-on wiring | **NO, dropped as a package** |
| 17 | Storage auto-fill wiring schedule, one page | Same wires, one sheet | The builder | Same | **NO, dropped as a package** |
| 18 | Storage auto-fill buy list and commissioning | Add-on lines to buy, what changes in the base package, what does not, and add-on commissioning steps | The buyer and the commissioner | Before and after the add-on build | **NO, dropped as a package** |
| 19 | Storage standpipe | The second standpipe, for the add-on floats, with its own parts table | The builder | Before add-on floats go in | **YES, folded** |

### 1.2 This build's set

**Eleven documents.**

| # | Document | Status against the old set |
|---|---|---|
| D1 | **Build book** | From old #1, absorbing #13, #14 and #19 as sheets |
| D2 | **Electrical schematic** | From old #5, narrowed: logic only, no wire schedule on the sheet |
| D3 | **Enclosure layout sheets** | From old #6, narrowed to geometry, and extended to all four enclosures |
| D4 | **Wiring instructions** | From old #3, covering every conductor in the build, not only the panel's |
| D5 | **Wiring schedule** | From old #4, one sheet, generated from the same list as D4 |
| D6 | **Cable and terminal schedule** | **NEW** |
| D7 | **Purchase package** | From old #2 |
| D8 | **Commissioning checklist** | From old #10 |
| D9 | **Baseline and maintenance record** | From old #11 |
| D10 | **Software specification** | **NEW** |
| D11 | **Channel register** | **NEW** |

### 1.3 Dropped, each with its reason

**The whole storage auto-fill package, old #15 to #18.** Not dropped as content,
dropped as a SEPARATE PACKAGE. The old set built the storage fill as an add-on
because it was decided after the base package shipped. This build has the storage
fill in scope from the beginning: `parts.md` "The fill solenoid" records it as
ordered and fully specified under D-136, and D-127 puts float positions in both
tanks. **There is no base set for it to supplement, so there is no supplement.**
That is the cheapest possible way to satisfy G-41 and T-028: the defect they were
frozen against is a property of supplements, and this set has none.

**The receptacle documents, old #7 to #9.** D-046 panel-mounts the receptacles in
the enclosure face and stops cords being fed through grips. Their conductors are
therefore panel conductors: they are rows in D5 and pages in D4, and there is no
external box to detail. **The old set needed three documents for them because they
were four separate boxes on the end of four cables.** This build has none of that.

**The plotter sheet, old #12.** It restates the build book's overview sheet and the
ladder on one large sheet. Under G-44 a document that states no fact of its own
must justify itself, and this one cannot: everything on it is on D1 or D2.
**Recorded as an owner call rather than a closed question** - if the owner wants a
wall plot, it is GENERATED from D1's and D2's sources, states nothing of its own,
and never becomes a place a fact can drift to.

### 1.4 New, each with its reason

**D6, the cable and terminal schedule.** The old set had one enclosure and its
inter-enclosure cabling was a cut list on the purchase workbook's Read me tab,
observed in the 1st Edition set, unverified. This build has four enclosures with
conductors running between all of them, and INTERCONNECT owns every crossing.
A cut list on a workbook tab cannot hold a segregation group, a class, an entry
face or a landing point.

**D10, the software specification.** The old set had no computer. Its dosing was a
bought appliance with fixed ports. This build has a Pi application that commands
step counts, books volumes, runs the verification model and holds the fault model.
Nothing in a drawing set can carry that.

**D11, the channel register.** Follows from D10. The old set had no per-channel
product, role or jug arithmetic to record. This build does, and G-05 decrements a
jug against it for the life of the machine.

---

## 2. THE DOCUMENTS, ONE BY ONE

Material status is against the tree TODAY: **EXISTS**, **PARTLY EXISTS**, or
**DOES NOT EXIST**, with the files named.

### D1. Build book

**Purpose.** How the machine is arranged and assembled, from tap to the scope
boundary, in sheet order.

**Owner.** BOSS, assembling returns from WATER, DOSING, PUMP-BOXES, DISPLAY-BOX
and INTERCONNECT. No single subsystem owns a book that crosses all of them.

**Depends on.** Every FROZEN FL- and M- row in `interface-table.md`; INTERCONNECT's
wall arbitration of M-02; D-121's standpipe method; D-146's face-and-order
allocation.

**Sheets, following the old set's sheet order.** Overview; legend; storage tank and
transfer; day tank and chiller loop; dosing manifold and probe glands; the dosing
wall carrying the manifold, the two pump boxes and the display box; the standpipe
assembly, one sheet covering both tanks; the interior of each enclosure; storage
fill and backflow break; chiller loop routing; probe cable routing.

**Material: PARTLY EXISTS.**
- Wet path, vessels, standpipe, overflow, drain, air gap, leak sensor:
  `subsystems/water.md`, especially the standpipe, overflow, drain and air gap
  sections dated 2026-09-03 and 2026-09-04.
- Manifold, injection, probe placement, jugs and jug change: `subsystems/dosing.md`,
  `subsystems/dosing-f002-proposal.md`, `subsystems/dosing-f004-wet-side.md`.
- Enclosures and the panel face: `parts.md` "Enclosures" and "The main panel face,
  as decided".
- The wall and the measured runs: `parts.md` "The wall" and the two cable-run
  sections - **note F-099, which is that those two sections carry the same figures
  under contradictory allowance rules.**
- **Does not exist: the wall layout itself.** `subsystems/interconnect.md` lists it
  under "Open, owned by INTERCONNECT" and M-02 is OPEN. That sheet is a blocked
  sheet with the blocker named, per D-142's precedent.

### D2. Electrical schematic

**Purpose.** The rungs, in order, from supply through the permissive chain to every
load and every sense circuit.

**Owner.** MAIN-PANEL.

**Depends on.** Every P- and S- row; G-07, G-13, G-25, G-26, G-28, G-30; the
envelope map in `order.md`.

**Material: EXISTS.** `subsystems/main-panel-ladder.md` is the ladder, returned
2026-09-04, drawn as the machine stands with its holes marked OPEN on the drawing
rather than held back. `order.md` supplies the envelope names. `parts.md` supplies
the two sense circuits that are given rather than derived.

**Narrowed against the old set.** The old set's schematic sheet carried a wire
schedule table in addition to the ladder, and `handoff/STATE-OF-PROJECT.md` records
that this table disagreed with the receptacle sheet on terminal assignments, with
the receptacle sheet correct. **A wire schedule on the schematic sheet is a second
place a conductor fact can live.** D5 is the only place. Observed in the 1st
Edition set, unverified.

### D3. Enclosure layout sheets

**Purpose.** Where each device physically sits, per enclosure: rails, ducts, faces,
penetrations and gland positions.

**Owner.** Each enclosure owner for its own sheet - MAIN-PANEL, PUMP-BOXES,
DISPLAY-BOX - with INTERCONNECT placing glands within a stated face under D-146.

**Depends on.** D-146; D-110 and F-088 on the top face; `parts.md`'s panel face;
the device roster from D2.

**Material: PARTLY EXISTS.** The main panel's faces and what is on them are in
`parts.md` "The main panel face, as decided". The decision rights are allocated in
`interface-table.md`'s gland boundary section. **The plate layout itself - which
device on which rail, in what order - has not been returned by any subsystem.**

**Narrowed against the old set.** The old set's plate sheet drew every wire as a
route on the plate and labelled it OVERVIEW ONLY, pointing at the instruction set
for the detail. `handoff/DRAWING-METHODOLOGY.md` shows both were generated from one
geometry file, so they could not disagree about a route - **but the sheet also
carried a device label that was wrong, recorded as known-wrong-but-cosmetic in
`handoff/STATE-OF-PROJECT.md`, because that label was typed on the sheet rather
than computed.** D3 carries geometry. Device identity comes from D2. Observed in
the 1st Edition set, unverified.

### D4. Wiring instructions

**Purpose.** One page per conductor: from, to, which clamp, the route, and the same
connection steps every time.

**Owner.** MAIN-PANEL for panel conductors, each box owner for conductors inside
its box, INTERCONNECT for conductors in a jacket between boxes. **Generated as one
set from one list, so the set has one shape and no seam.**

**Depends on.** D5 entirely. It is a VIEW of D5, never a transcription of it.

**Material: DOES NOT EXIST.** Nothing has been generated. Its input, D5, holds one
row.

**Note on G-41 inside this document.** Every page repeats the same assembly steps.
That is correct and it is what the old set did: steps are ABSOLUTE and should
repeat. No page states a quantity, so there is nothing on a page that could be
read as a total.

### D5. Wiring schedule

**Purpose.** Every conductor in the build on one sheet, one row each, keyed CDR-.
**The single source for every conductor fact.**

**Owner.** BOSS holds the list; each conductor's row is filled by the subsystem
that owns the crossing it realises.

**Depends on.** D2 for what a conductor is for; D6 for the jacket it travels in and
the terminals it lands on; every FROZEN interface row.

**Material: PARTLY EXISTS.** `wire-table-row-zero.md` holds the twelve-column
schema and one row filled in for a real conductor, plus its own record of what
filling that row cost and what it found. Zero conductors are enumerated.

### D6. Cable and terminal schedule

**Purpose.** One row per jacket, keyed RUN-. One row per landing point, keyed TRM-.
Two tables, one document, because a jacket and a landing are read together and
apart from a conductor.

**Owner.** INTERCONNECT.

**Depends on.** CBL-01 to CBL-07; D-146's allocation; D-149's ruling that RUN-
means a jacket and that a split id is retired rather than suffixed; D5 for the
conductors inside each jacket.

**Material: EXISTS as a returned draft.** `subsystems/interconnect-schedules.md`
carries both schedules with real ids, the TRM- shape and its rules, and every
blocked row saying what blocks it. `subsystems/interconnect-first-pass.md` is its
predecessor and holds the cable inventory at row level and the constraints found.
**Its own Part E says it is stopped part way and does not declare itself finished.**

### D7. Purchase package

**Purpose.** Every part to buy, once, with a search term, a status and a quantity.
**The only document in the set where a quantity appears.**

**Owner.** BOSS assembles; the owner does every lookup under G-15.

**Depends on.** Every subsystem's requirement-and-search-term returns; `order.md`;
`parts.md` for what is already specified or already bought.

**Tabs, following the old set.** A read-me stating how the workbook is organised and
what is still open; the buy list; a cart audit stating what to change in each cart
before checkout. Observed in the 1st Edition set, unverified.

**Material: PARTLY EXISTS.** `order.md` holds MAIN-PANEL's list as requirements
plus search terms with the envelope map behind it. `parts.md` holds the parts the
owner has already specified or bought. `subsystems/interconnect-schedules.md` Part D
holds its requirements and search terms. **There is no consolidated list and most
quantities do not exist, correctly: rule 4 says a count comes back once you know
what you need and can say why.**

### D8. Commissioning checklist

**Purpose.** The staged procedure, on paper, each stage ending in a gate, with
prerequisites and a fault-finding table.

**Owner.** BOSS.

**Depends on.** `commissioning.md`, which is its source register; D4 and D5, because
the first stage checks landed conductors against the schedule; D2, because ringing
out a series string is reading the ladder with a meter.

**Material: PARTLY EXISTS.** `commissioning.md` holds every measurement as a C- row
with its reason, its measurer and its blocker, plus the ordering note that fixes
the sequence of the tank-reading rows and the re-measure triggers. **What does not
exist is the staging: which rows are one stage, where the gates fall, what the
prerequisites are, and the fault-finding table.** The old set's answer to staging is
in section 4 below.

**The register and the document are two things.** `commissioning.md` carries the
reasoning, the corrections and the struck rows, and it should - it is tree state.
D8 carries the tick box and the one line that says how you know. The reasoning's
single source is the tree, not the delivered document.

### D9. Baseline and maintenance record

**Purpose.** A form. The numbers measured at commissioning are written into it once,
and later readings are compared against them.

**Owner.** BOSS writes the form. The owner fills it.

**Depends on.** D8, entirely. Its content cannot exist before commissioning runs.

**Material: PARTLY EXISTS.** `commissioning.md` already names what must be recorded
and, in several rows, says why a figure nobody recorded is a figure nobody can
check later. Its re-measure triggers section names what voids a recorded figure.
**The form does not exist.**

### D10. Software specification

**Purpose.** What the application does, what it may never do, and what it cannot
specify yet with the blocker for each.

**Owner.** CONTROL-SOFTWARE.

**Depends on.** S-12's pin and address map; the whole G-rule set, restated as
implementation constraints; `channel-token.md`.

**Material: EXISTS.** `software-spec.md`, twelve sections, written in one pass per
D-095. `audit/2026-09-03-doc12-vs-frozen.md` is a pairwise audit of it against the
frozen rows. `subsystems/control-software.md` carries four instruction blocks
issued since it was written, so **it exists and is behind the tree.**

### D11. Channel register

**Purpose.** The live per-channel record: product, role, jug, and the cable core the
channel travels in. Written at commissioning and updated for the life of the build.

**Owner.** CONTROL-SOFTWARE declares what a channel is, per S-19 and D-021.
INTERCONNECT fills the cable core column.

**Depends on.** C-09, which binds product and role to a channel and is first in the
commissioning order; D6 for the core.

**Material: EXISTS as a live record with empty columns.** `channel-register.md`,
with G-33's three different quantities kept in three columns, and a Cable core
column that is empty and waiting. `channel-token.md` holds the token's canonical
form and its forbidden list.

**Why it is not folded into D9.** D9 is filled once. D11 is written at every jug
change and every rewire. Different lifetimes, different reader moments. **This is
the one document in the set I would fold if the owner wants ten rather than eleven,
and the cost of folding it is that a jug refill would edit a commissioning
baseline.**

---

## 3. THE REFERENCE DISCIPLINE

### 3.1 How the old set's documents cite each other

Observed in the 1st Edition set, unverified.

- The wiring instruction pages carry "built from Sheet 6", naming the build book's
  ladder sheet as the source of the logic.
- The plate sheet carries "OVERVIEW ONLY - wire from the instruction set", and names
  the instruction set and the ladder it was built from.
- The schematic carries "see the instruction set for routing".
- The one-page schedules each carry "companion to the routing set".
- The add-on sheets carry "add-on to the base set", plus a "what does not change in
  the main package" block and a "shared with the existing package" block.
- `handoff/DRAWING-METHODOLOGY.md` states the mechanism behind all of it: **the
  one-page schedules read the SAME wire lists as the routing sheets, so they update
  automatically and cannot disagree, and a schedule is never hand-transcribed.**

**Where it worked and where it did not.** Where a document was a computed VIEW of
one list, the citations were decoration and nothing could drift. Where a fact was
TYPED onto a second sheet, it drifted:
`handoff/STATE-OF-PROJECT.md` records two live instances, a device label on the
plate sheet and a terminal assignment on the schematic, and names which sheet is
authoritative in each case. And `traps.md` T-028 records the third and only
expensive one: a parts table on an add-on sheet stating its whole scope where the
base set already covered part of it.

**The lesson, stated as a rule this set follows: a citation is decoration. What
stops drift is that the second document is computed from the first.** G-37 says the
same thing about sources.

### 3.2 Single source per kind of fact

Every prefix below is reserved and tree-global per G-43 and the namespace table at
the top of `interface-table.md`. **No document invents a local list under a bare
letter.**

| Kind of fact | Its single source | What every other document does |
|---|---|---|
| What a crossing IS, both ends named, and its status | `interface-table.md`, one FL-, P-, S-, CBL- or M- row | Cites the row id. Never restates the meaning |
| A frozen rule | `decisions.md`, one G- row | Cites G-nn |
| A dated decision | `decisions.md`, one D- entry | Cites D-nnn |
| A trap | `traps.md`, one T- entry | Cites T-nnn |
| A finding | `findings.md`, one F- entry | Cites F-nnn |
| Rung logic, contacts, what energises what, device identity | **D2** | D4's pages carry "built from D2", as the old set's pages carried "built from Sheet 6" |
| Device position, rail, duct, face, penetration, gland position | **D3** | D4 shows the route on a plate drawn from D3's geometry, computed |
| Every conductor fact: endpoints, class, colour, fail behaviour on a severed conductor, design current and the event that sets it | **D5**, one CDR- row | D4 is a generated view of D5. Nothing else states a conductor fact |
| One jacket: its route, its entries, its segregation group, its class roll-up | **D6**, one RUN- row | D5 column 2 holds the RUN- id and nothing else about the jacket |
| One landing point: its clamp count, its marking, and the source of that marking | **D6**, one TRM- row | D5 holds the TRM- id at each end. A marking is never copied |
| **Every quantity, count, total and price** | **D7, once** | **No drawing sheet carries a parts table.** This is the old set's one defect that cost money |
| A float POSITION and what it must do there | The float requirement WATER is writing, against S-01 and S-02 | Drawings label the position. No drawing states a height |
| Channel identity | `channel-token.md`, declared by CONTROL-SOFTWARE per S-19 | Applied at both ends of every per-channel core. No translation table in any medium |
| Per-channel product, role, jug quantities and cable core | **D11** | D10 and D6 reference it. Neither restates it |
| A measurement that must be made, and what blocks it | `commissioning.md`, one C- row | **D8** is its staged view |
| A measured RESULT | **D9**, once | Everything that consumes a figure cites D9, not the datasheet it replaced |
| Software behaviour, the fault model, the verification model | **D10** | |
| Reasoning, provenance, why a thing is the way it is | The tree - `decisions.md`, `findings.md`, `traps.md`, the subsystem files | **No delivered document carries it.** The old set's construction sheets carry none, and its reasoning lived in two handoff files |

### 3.3 G-41 inside this set

**The set has no supplement, so the delta problem does not arise.** That is the
plan's answer and it is the reason the add-on package is dropped rather than
rebuilt.

**If one is ever issued** - a revision, or a second-edition addendum - G-41 binds
exactly as frozen: assembly steps are ABSOLUTE and repeat in full, because the
reader may not be holding the base set. Quantities, counts and totals are DELTAS and
must never repeat. The recognition test is applied section by section, and any table
that can be read either way is read as absolute by whoever is holding a credit card.

**And the structural version of the same rule, which is stronger than the test:** the
only document in this set where a quantity appears at all is D7. A supplement
therefore has exactly one document it can contradict, and one place to look.

### 3.4 The three joins that must be identities

Taken from `subsystems/interconnect-schedules.md` Part C, which is correct and which
this plan adopts rather than restates. Per T-012, these are equalities a check can
fail, not copies that can drift:

- Every D5 row's cable value **is** a RUN- id in D6.
- Every D5 row's endpoint terminals **are** TRM- ids in D6.
- Every D6 terminal row's landed conductors **are** CDR- ids in D5, and their count
  **is** the clamp count.

---

## 4. THE BUILD ORDER

**Found in the old set rather than derived.** Observed in the 1st Edition set,
unverified. Its answer is distributed across four documents and is consistent:

- The purchase workbook's read-me says to filter the buy list and work a section at
  a time, and the cart audit says what to change in each cart **before checkout**.
  So the buy documents come first and are used once.
- The wiring instruction pages are numbered as steps in a sequence, each ending with
  an instruction to tick the wire off on the schedule. **So the instruction set and
  the schedule are both in hand before wiring starts, and both are built from the
  ladder, so the ladder precedes both.**
- The schematic says to build left to right, top to bottom, inside the panel.
- The commissioning checklist opens with prerequisites - every wire landed and both
  ends labelled, every joint cured - then runs staged, each stage ending in a gate,
  with the instruction not to start a stage until every box in the one before it is
  ticked.
- The maintenance log's baseline page says to copy the numbers off the commissioning
  checklist when the last stage finishes. **So its form exists early and its content
  cannot exist until commissioning has run.**
- The add-on's commissioning block says to run it after the last stage of the main
  checklist, and its buy list says to build it alongside the main package.

### 4.1 Mapped onto this set

**Before a person can BUY:** D7.

**Before a person can START BUILDING:** D1, D2, D3. D1 is the wet build and the
mechanical build; D2 and D3 are what the panel is and where things sit in it.

**Before a person can START WIRING, and generated from D2, D3 and D6:** D5 first,
then D4 as its view. D6 must be complete for any jacket a conductor travels in,
because a conductor cannot be cut, routed or landed without a jacket and a landing
point.

**Can lag the build.** D10 and D11.
**The tree's own reason, not an assumption:** G-26 says the panel runs without the
Pi - fills, transfer, circulation and chiller all operate on float and interlock
logic. So the water system can be built and brought into service while D10 is still
being written. D11 cannot be filled before C-09 runs.

**Can only be written after commissioning:** D9's CONTENT. Its form is written with
D8. And every figure `commissioning.md` schedules - the per-channel volume, the two
settling times, the noise and drift band, the rail as left, the microstep
configuration as set - exists only after D8 has run, so any document that wants one
cites D9 and never a datasheet.

**D8 itself** sits between: written after D4 and D5, because its first stage checks
landed conductors against the schedule; needed before anything is energised.

### 4.2 The rule that governs every one of them

Rule 9 and D-142's precedent. **A document is written with its blocked rows carrying
real ids and saying what blocks them.** A schedule of blocked rows with real ids is a
document. A schedule waiting for everything to close is not. Nothing is built against
an OPEN row, and no document waits for one.

---

## 5. WHAT WE HAVE BEEN OVER-COMPLICATING

Each item names our file against theirs. G-44: the burden of proof is on complexity.

### 5.1 The apparatus has outgrown the deliverable, and that is the whole of it

**The old set carried everything that could not be reconstructed from its source in
two markdown files:** `handoff/DRAWING-METHODOLOGY.md`, which is how to draw, and
`handoff/STATE-OF-PROJECT.md`, which is what is verified, what is known-wrong and
cosmetic, and what breaks if you touch it. **Against those two files it delivered
nineteen documents.**

This tree carries `decisions.md`, `findings.md`, `traps.md`, `interface-table.md`,
`parts.md`, `commissioning.md`, `order.md`, `software-spec.md`, `channel-token.md`,
`channel-register.md`, `wire-table-row-zero.md`, `colour-map-proposal.md`, nine
files under `audit/` and twenty-three under `subsystems/`. **Against all of that it
has delivered one builder-facing document, `software-spec.md`, and D-095 records it
as the first.**

**The ratio is inverted and it is the single clearest thing on this list.** It is
not an argument for deleting the tree - the tree is what caught the DIR level
reversal, the C-08 gap and the second-source illusion, and `handoff/STATE-OF-PROJECT.md`
shows the old set carrying its own known-wrong items with no mechanism that would
ever close them. **It is an argument that the tree is now large enough and the
output is not, and that the next work is documents rather than more apparatus.**
The two handoff files are the proof that the reasoning a build actually needs to
survive is small.

### 5.2 A written duplication contract where the old set had a mechanism

`handoff/DRAWING-METHODOLOGY.md` disposes of the whole question in one line: the
one-page schedules read the same wire lists as the routing sheets, so they update
automatically and cannot disagree, and a schedule is never hand-transcribed.

Against that we have `wire-table-row-zero.md` proving a twelve-column schema on one
row, `subsystems/interconnect-first-pass.md` sections 2.3 to 2.5 stating the
identities, the never-duplicate table and the namespace requirements, and
`subsystems/interconnect-schedules.md` Part C stating the identities and the
never-duplicate table again with the real prefixes. **Two files, both correct, both
saying the same thing, and the second exists because the first was written before
the prefixes were assigned.**

**The contract is not wrong. It is a written substitute for a mechanism.** The parts
of it that survive generation are the two facts a generator cannot compute: the
source of a terminal's marking, and a conductor's fail behaviour on being severed.
Everything else in those tables is a consequence of generating the views from one
list, which is what the old set did.

### 5.3 Eighty-nine kilobytes of shape work to produce two tables with no buildable rows

`subsystems/interconnect-first-pass.md` proposes the shapes. `subsystems/interconnect-schedules.md`
re-expresses the same shapes with real prefixes. Both are good work and D-142
accepted the first correctly - zero buildable of twenty is rule 9 working. **But the
old set's equivalent artefact is one page, and it exists because it was generated
rather than designed.** The lesson is not that INTERCONNECT was wrong; it is that a
schedule whose rows are all blocked is cheaper to produce as a generated view with
blank cells than as a document that argues for its own shape twice.

### 5.4 A colour axis the printed token may already cover

The old set used a small fixed set of wire colours, each meaning a FUNCTION, stated
in one key block that repeats on the sheets that need it. Observed in the 1st
Edition set, unverified.

`colour-map-proposal.md` proposes a channel colour per token on a marker carrier,
with a colour-vision constraint, an adjacency constraint for the pH pair and a
neutral-run constraint. Its own closing section says CH5 against CH6 is the binding
that matters and that three of the rest are weaker than they look.

**Under G-44 the question to put to it is: what failure does the colour axis prevent
that the printed token does not, and what does it cost to build, operate and
repair?** The token is already applied at both ends of every per-channel core under
`channel-token.md`, it is unambiguous to a colour-blind operator with no palette at
all, and `colour-map-proposal.md` is explicitly not frozen. **The honest reduced form
may be: function on the insulation as the old set did it, the token on the marker,
and colour on the pH pair only, where the proposal says the binding is strongest.**
That is a question for the owner, not a change.

### 5.5 Reasoning inside a row that a builder will read

`commissioning.md` C-23 carries, inside one table cell, an original statement, a
same-day correction, a struck-through paragraph, a reduction dated the following
day, and a note on why the row is reduced rather than deleted. C-01, C-04 and C-12
have the same shape. **All of that is correct as tree state and it is why the tree
works.**

The old set's commissioning row is a tick box and a line saying how you know.
Observed in the 1st Edition set, unverified.

**The over-complication is not in `commissioning.md`. It is in expecting one file to
be both the register and the document.** D8 is the checklist; `commissioning.md`
stays as it is. Naming this now is what stops the checklist inheriting the register's
shape when it is written.

### 5.6 One rule that has already done its job

G-41 and T-028 were frozen against a supplement this build had not written. **On this
plan it never writes one**, because the storage fill is in scope from the start.
The rule stands and binds on any future revision. **It should not be carried as a
standing obligation on every document in this set, because only one document in this
set states a quantity at all.**

---

## 6. WHAT THIS PLAN DOES NOT DECIDE

- **The staging of D8.** Which C- rows fall in which stage and where the gates go is
  a pass of its own, against `commissioning.md` in full.
- **Whether the plotter sheet is wanted.** Dropped here as stating no fact of its
  own. The owner may want a wall plot and that is his call.
- **Whether D11 folds into D9.** Named as the one fold available if the set must be
  smaller by one, with its cost stated.
- **The colour axis.** 5.4 is a question put to the owner, not a change to
  `colour-map-proposal.md`, which is not frozen and which BOSS does not freeze here.
- **Any sheet count, page count, row count or format.** No document below the level
  of the eleven is specified, and no template, style or tool is proposed.
