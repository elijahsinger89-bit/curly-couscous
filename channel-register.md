# D11 - THE CHANNEL REGISTER

**The ONE record per token. D-057, settling AUDIT run 2's B11.**

`channel-token.md` declares what a channel IS. **This file holds what each channel
HAS.** An attribute is recorded once, here. A subsystem file may reference it and may
not restate it. Four files holding four attributes was close to the thing the
declaration's forbidden list calls a table in any medium.

Each subsystem returns its own attribute to BOSS, who writes it here. **No subsystem
edits this file**, on the same rule as the interface table.

## WHY D11 IS THIS FILE AND NOT A DOCUMENT BUILT FROM IT

**Every other document in this set is a VIEW of a source. D11 is the exception, and the
declaration's own forbidden list is the reason.**

D8 is a view of `commissioning.md`; D4 is a view of D5. **A second file carrying this
table would be a second place a channel's attributes are written, which is forbidden
item 1 - a translation table in any medium - and D-057 put the one record here.**

**So D11 IS this file, promoted to document form.** It gained everything a reader needs
to use and update it. **It gained no new table, and that is the point.**

**G-54 still binds and is satisfied differently here: a fact enters at the subsystem
that owns the attribute and reaches this file only through BOSS.** The register is
where an attribute is WRITTEN, not where it is DECIDED.

---

## 1. HOW TO READ THIS DOCUMENT

| Section | What it is for |
|---|---|
| 2 | **The register.** The table itself. Everything else exists to keep it correct |
| 3 | **The three quantities that are not one column**, G-33. Read before touching any volume |
| 4 | **Column by column**: who returns it, what it waits on, when it is written |
| 5 | **What C-09 writes**, which is most of the empty half of the table |
| 6 | **The four constraints that bind at assignment**, and they are free to honour then and expensive afterwards |
| 7 | **When a channel changes.** The procedure, and what must be re-run |
| 8 | **What may never be written here**, and it is a shorter list than the declaration's because most of it cannot be expressed in a table keyed by token |
| 9 | **The counts**, per G-46 |

**A row is never deleted.** A channel is retired by marking the row retired, because
the logs still name it, **and the token is never reassigned.**

---

## 2. THE REGISTER

| Token | Role | Colour | Box | STEP pin | DIR pin | Cable core | Product | Jug seed | Nominal capacity | Microstep, C-17 | Steps per ml, C-01 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| CH1 | nutrient | white | **A** | | | | UNASSIGNED | 4000 mL | | | |
| CH2 | nutrient | brown | **A** | | | | UNASSIGNED | 4000 mL | | | |
| CH3 | nutrient | grey | **A** | | | | UNASSIGNED | 4000 mL | | | |
| CH4 | nutrient | red | **A** | | | | UNASSIGNED | 4000 mL | | | |
| CH5 | **pH DOWN** | **blue** | **B** | | | | pH down | **1000 mL** | | | |
| CH6 | **pH** | **yellow** | **B** | | | | **NOT STATED.** pH up by elimination | **1000 mL** | | | |
| CH7 | nutrient | black | **B** | | | | UNASSIGNED | 3785 mL | | | |
| CH8 | nutrient | violet | **B** | | | | UNASSIGNED | 3785 mL | | | |

**Filled volume is NOT a column here.** It is entered per fill, per G-05, and it
changes every time a jug is topped up. **A column would hold one value and the
arithmetic needs the current one.** Section 3 says why it is not the same quantity as
either of the two volume columns above.

**Role and Product as shown are the CONTROLLER'S CURRENT CONFIG, not an assignment.**
D-105: role is a per-channel SETTING and any channel may carry nutrient, pH-up or
pH-down. **CH5's pH-down mark has a real origin - the controller's blocked-channels
path, D-086. CH6's is elimination from that mark and is marked as an inference wherever
it appears.** Neither is binding. **Both are rewritten at C-09.**

**Colour is bound, D-099, and the markers are NOT MADE YET.** F-080's gate: the
channel markers are not manufactured until C-09 has bound both product and role.
**Before C-09 the gate is free. After the markers exist it is eight relabels.**

**Box is PUMP-BOXES' decision and is returned, D-178.** CH1 to CH4 in box A, CH5 to
CH8 in box B. **The low four and the high four, so a builder holding a box can tell
which channels are in it without consulting a table.**

---

## 3. THREE DIFFERENT QUANTITIES, AND THEY ARE NEVER ONE COLUMN

**G-33, frozen 2026-09-02. Corrected by the owner at D-086 after all three had been one
column.**

| Quantity | What it is | Where it lives | Status |
|---|---|---|---|
| **Jug seed** | **A SEED VALUE in config.yaml. NOT a container.** Every one is a default that gets overwritten per channel on the Pumps screen. **CH7 and CH8 carry 3785 because that was the closest seed to a US gallon and nothing more** | The register, section 2 | **A default. It is not a measurement of the world** |
| **Nominal capacity** | What the vessel actually holds | The register, section 2, **empty** | **NOT DECIDED.** The owner states it when he buys the containers |
| **Filled volume** | **What was actually poured**, which is what G-05's arithmetic decrements against | Entered at fill time, not a column | Entered per fill, for the life of the machine |

**A seed is what a file had to contain. A capacity is what a vessel holds. A poured
volume is what the arithmetic runs on. None of the three is the same number.** T-018.

### Three conclusions on file rest on an INFERENCE FROM A DEFAULT

**Marked as such and not removed, because each is probably right and none is stated:**

1. **That the two 1000 mL channels are the pH adjusters**, and therefore that the size
   axis separates the pH pair from the six nutrients for free. F-064's narrowing of
   F-063 rested on this. **Probably right - pH adjusters are concentrated and used in
   small volumes - and the config does not say it.**
2. **F-066**, that the two smallest containers are handled most often.
3. **DOSING's three depth classes for the suction pickup**, derived from numbers that
   are not container sizes.

**What does NOT rest on it: CH5's pH-down mark**, which comes through the controller's
blocked-channels path and is a ROLE marking rather than a default.

---

## 4. COLUMN BY COLUMN

| Column | Who returns it | Waits on | Written when |
|---|---|---|---|
| **Token** | CONTROL-SOFTWARE | Nothing. Declared and complete | Done |
| **Role** | Owner, at C-09 | C-09 | **At assignment.** The current marks are config, not assignment |
| **Colour** | CONTROL-SOFTWARE, bound at D-099 | Nothing for the binding. **The CARRIER waits on the owner's lookup** - whether eight colours exist in a colour-through, non-printed material surviving acid, base and nutrient-concentrate duty, D-084 | Bound. **Markers not made until C-09** |
| **Box** | PUMP-BOXES, D-178 | Nothing | Done |
| **STEP pin, DIR pin** | DISPLAY-BOX | **S-12, an OPEN interface row, and the Pi 5 header lookup.** Rule 9: nothing is built against it | When S-12 closes |
| **Cable core** | INTERCONNECT | D6. **The eight tokens applied as conductor identity at BOTH ends of every core** | When the cores are labelled |
| **Product** | Owner, at C-09 | C-09. **Five of eight are unnamed in any file in this tree** | At assignment |
| **Jug seed** | CONTROL-SOFTWARE, from config | Nothing | Done. **And it is a seed** |
| **Nominal capacity** | Owner | The containers being bought | When bought |
| **Microstep, C-17** | PUMP-BOXES sets by pins, owner records | **Drivers wired.** Set by PINS and never over UART, D-075 | C-17, before C-01 |
| **Steps per ml, C-01** | Owner measures | **C-17 recorded first, AND F-075 settled**, D-102 | C-01 |

**Filled volume, per G-05: the owner, AT FILL TIME.** Not the same quantity as the jug
seed. **DOSING caught BOSS recording the first as though it settled the second.**

---

## 5. WHAT C-09 WRITES

**C-09 is the end-to-end channel trace: command one channel alone, confirm BY EYE which
head turns, which tube moves, which jug's level drops, and which product.**

**It is the only check that catches a build-time labelling error or a numbering
disagreement between software, wiring, head and jug, and those pass every other check
in the system.** Free, needs no hardware, and with translucent tubing needs no
disassembly. **Possible only because G-06 serialises the heads.**

**Per channel, C-09 asks three questions and writes two columns:**

| Asked | Why it is asked | Writes |
|---|---|---|
| Which product is this? | D-077 makes assignment time BE commissioning. **This row is that moment** | **Product** |
| **Is this product an ACID, a BASE, or a SALT SOLUTION?** | D-084 specifies the token carrier against exactly those three duty classes, **and its residual said nothing would detect a product outside them at assignment time.** F-077 | Nothing in the table. **It validates the carrier choice** |
| **Is this channel's ROLE SETTING the role this product actually has?** | **A wrong role is worse than a wrong product: it makes the signed check expect the wrong direction, so the check CONFIRMS the error.** G-32 as amended by D-105 | **Role** |

**AND, D-178: are pH-up and pH-down assigned to two channels in the same pump box?
They should not be.**

**C-09 IS RE-RUN FOR ALL EIGHT CHANNELS, NEVER FOR THE ONE THAT CHANGED.** A crossing
always involves at least two channels and a partial trace cannot see the half it did
not trace. **A partial C-09 is not a cheaper C-09. It is a different and much weaker
test.**

**WHAT MUST NEVER HAPPEN: discovering a disagreement at C-09 and fixing it by
relabelling the carrier that disagrees.** That converts a detected crossing into a
permanent silent one, and every later check confirms it. **The fix is to determine
which end departed from the declaration, correct THAT end, and re-run all eight.**

---

## 6. THE FOUR CONSTRAINTS THAT BIND AT ASSIGNMENT

**All four are free to honour at C-09 and expensive or impossible afterwards. That is
the whole reason they are listed here rather than left in their source files.**

| # | Constraint | Source | What it costs to honour at C-09 | What it costs afterwards |
|---|---|---|---|---|
| 1 | **pH-up and pH-down shall not be assigned to ADJACENT tokens** | channel-token.md, from S-16 | **A choice of which jug goes where** | **Unfixable without renumbering**, which forbidden item 2 forbids and G-17 and G-18 make impossible |
| 2 | **pH-up and pH-down shall not receive NEIGHBOURING colours** | Same | The same choice | **Eight relabels** |
| 3 | **pH-up and pH-down shall not be assigned to two channels in the SAME PUMP BOX** | D-178 | **A sentence typed at commissioning** | **Moving a head from one plate to another** |
| 4 | **The product must be an acid, a base or a salt solution** | D-084, F-077 | A question asked once per channel | **A carrier that does not survive its duty, discovered later** |

**Why 1 and 2 exist and are not legibility rules: the movements of pH-up and pH-down
CANCEL, and S-16 attributes to the COMMANDED channel, so a swap between them is
invisible to the only check that looks at them.**

**Why 3 exists: CH5 and CH6 are both in box B.** If the pH roles land there, **an acid
and a base share one sealed enclosure and one lid.** The box division is not changed
for it - **the cheaper place to fix it is the role assignment, and this is where that
happens.**

**F-063 is DISSOLVED, not shrunk, and this is where the dissolution lands.** D-105 made
role a per-channel setting, so **there is no fixed pH pair to separate. Any two channels
could be the pair.** The adjacency problem stopped being a property of the token
numbering and became **a constraint on a choice made at commissioning** - which is
strictly better, because it was previously unsatisfiable.

---

## 7. WHEN A CHANNEL HAS TO CHANGE

**Universal, every case:**

- **The change is made in ONE place first, this register, and every carrier is brought
  into agreement IN THE SAME WORKING SESSION.** No overnight partial state.
- **While software and the wall may disagree, the channel is OUT OF SERVICE: THE
  SEQUENCER SKIPS IT.** D-056. **This is not a hardware disable and does not rely on
  one** - G-21 says software has no per-driver disable, permanently. **Skipping is the
  sequencer declining to issue steps, which needs no hardware at all.**
- **A batch that requires the channel STOPS and tells the operator.** It does not
  substitute, skip or reorder. G-16: **the only safe direction of error is the loud one.**
- **C-09 is re-run for all eight.**

| Case | The token | What else must be re-run |
|---|---|---|
| **A head is moved between boxes** | **Goes with the channel.** The vacated location carries NO token and never inherits a neighbour's. Box, core and possibly pin update as attributes. **Nothing renumbers** | C-09 all eight. **C-01 for the moved channel if its tubing or head orientation changed** |
| **A driver is replaced** | **Unchanged.** The replacement inherits the token of the position and wiring it lands in. **A driver is a consumable attribute** | C-09, all eight if anything was unlanded and relanded. **AND: steps per ml for that channel is VOID until re-measured**, because the driver's step configuration is part of what PUMP-BOXES sets. **No figure is carried across a driver change on the assumption the configuration was reproduced** |
| **A product is retired, channel kept** | **Unchanged.** G-17: the jug is retired with its product, since that jug can only ever have held it. **A new jug at the same station, same token, new product name and fill date** | **Full-jug volume re-entered per G-05.** C-03 or C-04 for that channel. C-09 all eight if any wet-path item was disconnected. **F-002's residual is unchanged: a correctly stationed, correctly tokened jug filled from the wrong drum is caught by nothing here** |
| **A channel is retired outright** | **The token is retired with it and is NEVER REASSIGNED.** G-17 retires a vessel too: the jug is dedicated for life and cannot be re-stationed. **The live set becomes a subset of the eight WITH A GAP IN IT, and the gap stays** | **C-09 for the seven that remain.** The retired one has nothing to trace, **and the point of re-running is that its neighbours' wiring was disturbed** |

---

## 8. WHAT MAY NEVER BE WRITTEN IN THIS FILE

**The declaration's forbidden list is in `channel-token.md` and is not restated here.
These are the items that could actually be written INTO this table, which is a shorter
list, and it is short because the table's shape prevents most of them.**

| # | Never | Why the table alone does not prevent it |
|---|---|---|
| 1 | **A column that is an identity of its own** | Every column here is an ATTRIBUTE keyed by the token. **"CH3's core is Y" is correct. "core 7 = CH3" is the same fact written as a mapping and it is the defect** |
| 2 | **A second row for one token, or one row for two** | Nothing in a markdown table stops it |
| 3 | **Closing a gap after a retirement** | **The remaining tokens do not shift down to make the set contiguous.** Tidiness is the generator here |
| 4 | **A ninth row**, or a spare labelled as a channel | There is no ninth channel |
| 5 | **An index column**, zero-based or otherwise | **No array position is ever a channel identity.** A positional list is an off-by-one waiting for an editor to insert a line, **and G-04 and G-05 guarantee nobody will ever see the result** |
| 6 | **A product name used as the row key** | **Retiring or swapping a product does not rename a channel** |
| 7 | **A local abbreviation of the token** | If a carrier cannot hold `CH3`, that is a carrier defect reported to CONTROL-SOFTWARE. **It is never solved by inventing a short form** |
| 8 | **Filled volume as a column** | It changes every fill. **A column holds one value and the arithmetic needs the current one** |

**The test for any proposed column: could its value be replaced without the channel
becoming a different channel?** If yes it is an attribute and belongs here. **If no,
something has gone wrong, because a channel has no attributes that are not replaceable.**

---

## 9. THE COUNTS, PER G-46

**Eight rows, twelve columns, 96 cells.**

| | Cells | Which |
|---|---|---|
| **Carry text** | **48** | Token 8, Role 8, Colour 8, Box 8, Jug seed 8, Product 8 |
| **Empty, with a named blocker** | **48** | STEP pin 8 and DIR pin 8 on S-12; Cable core 8 on D6; Nominal capacity 8 on the containers being bought; Microstep 8 on C-17; Steps per ml 8 on C-01 |
| **Empty with no blocker** | **0** | |
| **Cells that can never be filled** | **0** | **Filled volume was the only candidate and it is not a column.** G-46 |

**AND OF THE 48 THAT CARRY TEXT, ONLY 32 CARRY A FACT.** The distinction is G-46's and
it matters more here than the empty count does, **because a cell reading "nutrient"
looks settled and is not.**

| | Cells | |
|---|---|---|
| **A fact** | **32** | Token 8, Colour 8, Box 8, Jug seed 8. **Jug seed is a fact about a config file, not about a vessel** |
| **Config, not assignment** | **8** | **Role, all eight. Rewritten at C-09** |
| **A stated decision NOT MADE** | **6** | Product, CH1 to CH4 and CH7 to CH8. **"UNASSIGNED" is a value. It is not a gap** |
| **A real config mark** | **1** | **Product, CH5.** The controller's blocked-channels path, D-086 |
| **An inference, marked as one** | **1** | **Product, CH6.** Elimination from CH5's mark. **It is not a statement and nothing may be built on it** |

**Not one of the 48 empty cells is blocked on anything BOSS owns.** Two of the five
blocked columns wait on the build existing, one on another agent, one on an open
interface row, one on a purchase.

---

## 10. STATUS

**D11 EXISTS. It is this file and it always was; what it gained is everything around
the table.**

| | |
|---|---|
| **The register** | **Live. 40 of 96 cells carry a value** |
| **Gated on** | **C-09 for the half that matters**, and C-09 is gated on the build existing |
| **The colour markers** | **Bound, D-099, and DELIBERATELY NOT MADE.** F-080's gate |
| **The five unassigned products** | **A DECISION NOT MADE, not a missing record.** Every channel in the controller config is named "Channel 1" through "Channel 8". **NOTHING THERE KNOWS WHAT IS PLUGGED INTO WHICH CHANNEL**, and the config says so on its own line |
| **Searched** | BOSS searched every markdown file for a channel-to-product list on 2026-09-01. **There is none.** The only product-like names are in `channel-token.md`'s own FORBIDDEN examples - "the Grow A line is not a channel name" - **which are illustrations of what is banned, not an assignment. Nothing to strike** |

**So the five unassigned are deliberately unassigned until commissioning.** No subsystem
holds a row open waiting for them, and no subsystem assumes a product to get on with its
own work. **The channel token exists precisely so identity can be carried without the
product being known.**
