# MAIN-PANEL: what 16 by 12 actually costs

Returned 2026-09-11 against D-188 and G-51. **This is arithmetic and a verdict. It is
not a layout and it proposes no placement.**

Read: agents.md; G-51 and D-188; electrical-schematic.md for the roster; order.md;
parts.md in full; G-30, D-072 and F-055 for the duty separation; and, because the
counts live there, cable-and-terminal-schedule.md, wiring-schedule.md and
subsystems/entry-faces.md.

**No file was edited.**

---

## 1. THE SHORT VERSION

**The area arithmetic cannot be completed today, and the reason is not coyness.
parts.md carries no footprint, width, height or depth for any panel component** - not
the 55.34, not the 94.74SMA socket, not the 22.32, not the NDR-240-24, not a terminal
block, not a duct, not the ground bar. Searched: parts.md in full, order.md,
electrical-schematic.md, both schedules. **Nothing states a dimension of anything that
goes on the plate.** Under rule 3 the output is therefore the lookup list, in
section 9.

**But the interesting result does not need a single one of those lookups.**

**The cost of 16 by 12 is not spread over an area. It falls almost entirely on the
WIDTH, and width is the dimension that carries both the rails and all eleven glands.**

| | Landscape, box on file | Portrait, box on file, G-51 | Target 16 by 12 |
|---|---|---|---|
| Width, which sets rail length and the gland face | **20.7 in** | **16.6 in** | **12 in** |
| Height | 16.6 in | 20.7 in | 16 in |
| Gross area | 343.6 sq in | 343.6 sq in | **192 sq in** |

**Width: 20.7 to 12, a 42 percent loss. Height: 16.6 to 16, a 4 percent loss. Area:
44 percent.** The area figure reads as an even squeeze and it is not one. Arithmetic
on given numbers only: 16, 12, 20.7 and 16.6.

**So the question to put to the owner is not "does 192 square inches hold it". It is
"do eleven cord grips in a mandated order fit across twelve inches, and does a rail
twelve inches long minus two class-separated wireways hold what has to go on it".**
The first of those is one lookup. The second is six.

**One piece of arithmetic did complete, and it is a finding rather than an answer to
the question asked. The 12-way ground bar is exactly full at 12 of 12, with zero
spare ways, before three named unknowns.** Section 5.5.

---

## 2. WHAT IS BEING MEASURED AGAINST WHAT

**Available.** 16 by 12 is **two numbers, and an enclosure has three.** The main panel
is the only box in parts.md with no depth on file: the pump boxes are 16 by 8 by 6 and
the display box is 300 by 250 by 130 mm, both with three figures; the main panel is
"roughly 20.7 by 16.6 in" with none. **Depth is what a receptacle body, a gasketed
22 mm device carrying up to three stacked contact blocks, and a relay plus a
suppression module on a rail all consume**, and main-panel-buy.md already stated that
the top rail cannot be fixed until the deepest stack behind the face is measured.

**Gross area is not plate area either.** A back plate is inset from the box on all
four sides and the inset is a property of the enclosure, not a figure anyone here may
state. Then the plate loses two vertical wireways to class separation and a gutter at
top and bottom.

**So "available" today is one number - 192 square inches gross - and three unknowns
between it and a usable plate: the depth, the plate inset, and the duct width.**

**Needed.** The sum of the footprints in section 3, none of which exists in the tree.

---

## 3. THE ROSTER, WITH EACH FOOTPRINT AS A REQUIREMENT AND A SEARCH TERM

Devices from electrical-schematic.md section 1 and order.md's envelope map. **No
number below is stated from memory.**

| # | On the plate | Requirement | Search term |
|---|---|---|---|
| 1-6 | **K-PERM, K-FILL-D-Q, K-DRY-Q, K-FILL-S, K-FILL-D-P, K-DRY-P** - six 55.34 relays, each in a 94.74SMA socket | Rail length consumed per socket, and height over the rail with the relay and the retaining clip fitted | `Finder 94.74 socket dimensions DIN rail`; `Finder 55.34 relay overall dimensions in socket` |
| 7 | **KM-DRV**, Finder 22.32 | Rail length and depth. It is a modular device and its width is a module count | `Finder 22.32 modular contactor dimensions DIN` |
| 8 | **K-PERM-P**, only if K-PERM splits, ?16 | As 1-6 | as above |
| 9 | **KM-CHIL** | **No device is chosen, ?8, so no footprint exists to look up.** It must carry 7.5 A continuous plus an unpublished compressor inrush, ?3 | `Finder 22.32 modular contactor dimensions DIN`, if the orphaned second 22.32 is used |
| 10 | **Main disconnect**, ?1 | **No device is named anywhere in the tree.** Nothing to look up until one is | `enclosure main disconnect switch DIN rail single phase dimensions` |
| 11-12 | **Two overcurrent devices**, one per branch circuit, ?2 and ?3 | **Not chosen.** BUS-A and BUS-B are separate circuits under D-137 | `DIN rail circuit breaker dimensions single pole` |
| 13 | **Fuse holder for R-PI** - P-07 says the Pi receptacle is fused | Rail length and depth | `DIN rail fuse holder dimensions` |
| 14 | **NDR-240-24** | Footprint, mounting method, **and the convection clearance it requires above and below.** That clearance is a clearance, and G-51 says the owner will not spend one | `Mean Well NDR-240-24 dimensions mounting`; `NDR-240 recommended clearance convection cooling` |
| 15 | **Terminal bank**, at least 56 clamps, section 5.2 | Width per way at the conductor size, single tier and double tier, and the end-stop and separator allowance | `DIN terminal block width per pole`; `double deck terminal block dimensions` |
| 16 | **Ground bar, 12-way copper**, owner-given | Footprint including insulated standoffs. **Not a DIN-rail grounding block: the plate is plastic and it would bond to nothing**, D-165 | `copper ground bar 12 position dimensions insulated standoff` |
| 17 | **Five sense-circuit burdens** - S-08, S-03, the D-042 leg, S-20 and its complement | **NOBODY HAS EVER GIVEN THESE A MOUNTING.** parts.md puts the burden in the main panel for both circuits and no file says what holds it. Section 5.1 | `component terminal block resistor DIN rail`; `fuse-style terminal block with component` |
| 18 | **Seven coil suppression modules**, order.md items 4 and 5 | **Zero extra positions if the socket accepts a module and the retaining clip at once, seven if it does not.** main-panel-buy.md raised this and it is unresolved | `Finder 94.74 socket module slot compatibility retaining clip` |
| 19 | **Two vertical wireways**, one per voltage class | Width, and the fill ratio a duct is sized at | `PVC wiring duct sizes fill capacity` |

**Not on the plate and not counted above, but consuming the box:** the four
panel-mounted receptacles on a face, D-046; the five 22 mm devices on the top face;
and the eleven cord grips on the bottom face. Each needs a face lookup, section 9.

---

## 4. WHAT DOES NOT DEPEND ON A LOOKUP

Four counts and one rule. All of them are answerable today and all of them bear on
whether a small box is legal.

### 4.1 Rail positions

**Between 16 and 24 discrete rail-mounted positions**, of which one is a terminal bank
and one is the ground bar.

| Certainty | Count | What |
|---|---|---|
| Certain, device known | **7** | Six relay envelopes and KM-DRV |
| Contingent on ?16 | 0 or 1 | K-PERM-P |
| Certain in FUNCTION, device not chosen | **5** | KM-CHIL, the disconnect, two overcurrent devices, the R-PI fuse holder |
| Certain, footprint unknown | **3** | NDR-240-24, the terminal bank, the ground bar |
| Never placed by anybody | **1 to 8** | The five burdens as one carrier or five; suppression as zero or seven |

**The count is orientation-independent. What orientation changes is how many rails
those positions need**, because a rail spans the width: narrower rails mean more
rails, and more rails means more of the height spent on rail pitch and on the
horizontal duct between them. **That is the mechanism by which portrait costs plate
area at a constant device count.**

### 4.2 Terminal count: 56 to 57 clamps is a FLOOR, not the number

Counted as landings, never as jackets, per T-009 and T-010.

| Group | Clamps | Source |
|---|---|---|
| Conductors entering through a gland, less the eight that land on the bar | **34 to 35** | wiring-schedule.md, the MAIN-PANEL end of RUN-001, 002, 005, 006, 007, 008, 010, 011, 012, 013, 015. The range is the leak console's Form C legs, two or three, which **MAIN-PANEL owes and has not returned** |
| Top-face device conductors | **14** | E-STOP one block, RESET up to three blocks, three lamps, two conductors each |
| Receptacle feeds, hot and neutral | **8** | R-PI, R-XFER, R-MAN, R-CHIL. Their grounds go to the bar |
| **Floor** | **56 to 57** | |

**And the number that would actually decide the box does not exist.**
wiring-schedule.md section 7 says so in terms: **every conductor internal to the main
panel is unwritten, and they are MAIN-PANEL's to fill.** The rails, the permissive
string, the seal-in poles, the coil buses, node PB, BUS-A and BUS-AP, the lamps and
their burdens, and the burden branches of all four sense circuits are all on top of
the 56.

**So the honest statement about terminals is: the floor is 56, the real number is
unknown, and it is unknown because of work MAIN-PANEL owes rather than because of a
lookup.** Nothing about box size should be concluded from 56.

### 4.3 The bottom face is the binding constraint, and it is decidable before anything else

**Eleven jackets enter the main panel's bottom face.** parts.md fixes it: every cord
grip on the bottom, nothing but the five 22 mm devices on top. Owner-given.

RUN-001, RUN-002, RUN-005, RUN-006, RUN-007, RUN-008, RUN-010, RUN-011, RUN-012,
RUN-013, RUN-015.

**They are not free to be placed in any order, and the order at the panel end has
never been decided.** subsystems/entry-faces.md covers CBL-02 and CBL-03 only - the
pump boxes and the display box. **CBL-01, the main panel's own face, has no order, and
under D-146 it is MAIN-PANEL's.**

Three constraints already bind it, all from cable-and-terminal-schedule.md:

- **RUN-005 and RUN-006 must be provably non-adjacent AT EITHER END.** F-029: a short
  between them makes the readback follow the command, which is precisely and only the
  failure G-09 exists to detect, and it removes weld detection at the same time.
- **RUN-007 and RUN-008 each carry a G-27 complementary pair, may not be split, and
  may not leave the F-029 gap they hold.** At the display box they sit between 005 and
  006. The same gap has to exist here.
- **SEG-A - RUN-010, RUN-011, RUN-015 - must not be the realistic neighbour of the
  sense runs.** That is D-049's short case handed to the wiring plan, and G-51 names
  this exact thing as the separation the owner will not spend.

**So the bottom face must hold eleven grips, in a constrained order, with at least one
deliberate gap, across twelve inches.** In landscape on the box already on file that
face is 20.7 inches; G-51's portrait rule alone takes it to 16.6; the target takes it
to 12.

**This is the arithmetic to run first.** It needs one lookup - grip bore and required
panel spacing for the cable outside diameters D6 already carries - against a count
that is already final. **Every other question in this study needs six lookups or a
piece of work MAIN-PANEL has not done.**

### 4.4 What must stay separated, and what a small box threatens

**G-30 is not threatened by a small box.** It separates poles inside a relay, and the
separation is bought by the six-envelope split in order.md - three gold quiet
envelopes and three standard power ones. **A smaller enclosure cannot undo that**,
because it is a purchase and not a placement. The one live G-30 problem in this panel,
F-055, is KM-DRV carrying an ARC pole and a SENSE pole, and **it is unaffected by box
size: S-08 has nowhere to move whatever the box is.**

**What a small box threatens is the CONDUCTOR separation, and that is a different
rule.** D-150 splits class into VOLTAGE and DUTY; voltage drives insulation and
segregation, duty drives G-30. The panel carries three voltage classes - LINE, 24 V
and SIGNAL - and main-panel-poles.md's plan is **two vertical wireways, LINE down one
and 24 V plus signal down the other.** That pairing is legitimate on D-072's stated
condition, suppression at the coil, and it is the minimum: **two ducts is already the
answer with the separation spent down to its floor, not a comfortable arrangement
with room to give back.**

**So under G-51 the test is simple and it is a yes-or-no: does a 12-inch width hold
two ducts plus a rail long enough for the positions in 4.1.** If it holds them only by
deleting a duct or by putting a sense conductor in the LINE duct, **the box is too
small and that is the answer, per G-51's own words.**

### 4.5 The ground bar: the one piece of arithmetic that completed, and it fails

**The bar is 12-way, owner-given. Twelve conductors land on it. There is no spare
way.**

| # | Conductor | Source |
|---|---|---|
| 1-2 | Pump box A and pump box B local bars, daisied home | CDR-004, CDR-007 |
| 3-6 | **The display box local bar, four times** - one grounding conductor per jacket, and four jackets run to it | CDR-032, CDR-035, CDR-038, CDR-041 |
| 7 | The building branch circuit's equipment ground | CDR-044 |
| 8 | FV-1's ground | CDR-046 |
| 9-12 | The four panel-mounted receptacles' grounds | D-046, panel-internal, not yet in D5 |

**Three named things each need a thirteenth way and none of them is speculative.**

1. **The leak console's equipment ground.** The WB200 is a powered device, remote,
   with its own cord grip under D-163. RUN-015 enumerates a 24 V supply pair and
   states that its contact legs are not enumerated. **No grounding conductor appears
   for it anywhere.** I looked at RUN-015, CBL-06, D-163 and parts.md's leak console
   section. Not present, and whether it needs one is a question about a bought device.
2. **The enclosure's own bonding, if it is metal.** **parts.md states no material for
   the main panel.** The pump boxes are plastic and the display box is polycarbonate,
   both stated; the main panel's row carries a size and nothing else. D-165's
   "the plate is plastic" is recorded of the parallel build. **If this box or its plate
   is metal, each needs a bonding conductor and the bar overflows by two.**
3. **A spare way.** A bar with no spare is a bar where the first addition is a new
   part and a new landing, and G-51 is explicit that a margin is not the thing to
   spend.

**Under G-51 this is exactly the report the owner asked for: a bar chosen at 12 ways
is at 12 of 12 before three known questions, and that is a margin being spent by
arithmetic rather than by choice.** It is independent of the box size and it would be
true in a 20 by 16 enclosure.

---

## 5. DOES PORTRAIT CHANGE ANYTHING

**Yes, and it changes one thing in three places, all of them the width.**

**A DIN rail spans the width.** Portrait makes the width the small dimension, so every
rail is shorter, so more rails are needed for the same 16 to 24 positions, so more of
the height goes to rail pitch and to the horizontal duct between rails. The device
count does not change and the area it needs does.

**The two vertical wireways are subtracted from the width.** They cost the same
absolute inches in either orientation, so in portrait they take a larger fraction of a
smaller number. On the box already on file that is two ducts out of 16.6 rather than
out of 20.7; at the target it is two ducts out of 12.

**The gland face is the bottom face, owner-given, and the bottom face is the width.**
Eleven grips in a constrained order. Portrait alone takes that face from 20.7 to 16.6
with the count unchanged.

**What portrait does NOT change:** the rail position count, the terminal count, the
gland count, the envelope split that satisfies G-30, or the ground bar's twelve
landings. **Four of the five things this study could count are orientation-independent,
and the fifth - rail length - is the one that decides the box.**

**Stated plainly so it is not mistaken for an objection to G-51: the rule is frozen
and this study does not reopen it. What is reported is that on THIS panel the rule's
whole cost lands on the one dimension that is also the target's whole reduction, and
the two compound rather than being independent.**

---

## 6. THE DOUBLE-DECK TRADE, PRICED

G-51 says take them if the box needs it and say so on the face, and do not take them
for tidiness. **The verdict is DO NOT TAKE THEM, and the reason is not tidiness - it
is that the place they would save the most is the place they are unsafe.**

### 6.1 Where they would save the most: the sixteen float conductors

RUN-012 and RUN-013 bring **sixteen conductors home, two per float, eight identical
pairs.** No series link is made in the wet zone - INTERCONNECT's decision, so that
C-24 can test each float's fail direction at the panel with a meter. Sixteen clamps is
over a quarter of the whole terminal floor and it is the single largest homogeneous
block in the panel. **It is the obvious double-deck candidate and it is the wrong
one.**

**G-51's safety argument for a double-deck block is that tier pairing is like with
like: hot with hot, neutral with neutral, so a slip between tiers shorts like to like.
THAT ARGUMENT DOES NOT HOLD ON A SERIES INTERLOCK CHAIN, and the float terminals are
exactly a series interlock chain.**

Every float conductor is a series element in a 24 V coil chain, D-154. **Every
terminal in a series chain is at a DIFFERENT point of the chain. There is no pair of
them that is like to like.** A slip between tiers does not short two equals; it
**bridges across whatever sits between them**, and what sits between them is the
protection.

| Slip | What it does |
|---|---|
| Between the two tiers of one float's own pair | **The float is bypassed.** It reads permanently closed |
| Between the tiers of two different floats' conductors | **Every element between them is bypassed** |

**And the direction is the dangerous one.** D-154's whole achievement is that every
float fails safe by topology: severed equals open equals coil drops equals the action
stops. **A tier slip is the exact inverse - it makes a float permanently made.** On
LS-5 that is a fill that never stops, which D-130 says has no second line but the
overflow. On LS-4 that is the dry-run interlock silently gone.

**So on the sixteen conductors where double-decking pays, it converts the one failure
mode this panel has made structurally safe into the one it has no defence against.**

### 6.2 Where they are safe: the common-potential banks, and there they buy little

The neutral bank, the 24 V minus-V bank and the 24 V plus-V bank are genuinely like
with like, and a slip between tiers there is a short between two conductors already at
the same potential, which is nothing. **That is G-51's argument working, and those are
the only banks in this panel where it does.**

**But a common-potential bank is the one thing that does not need a second tier**, because
it can be collapsed with a bridge comb into one block with many ways - fewer parts,
fewer steps, no tier to get wrong. **The simpler part already solves the case where the
riskier part is safe.**

### 6.3 The cost, per G-48

| | |
|---|---|
| **What it buys** | Roughly half the rail length of whatever bank it is applied to. On the float bank that is sixteen ways down to eight positions |
| **Parts** | A second block type in the panel, and G-28's labelling problem arrives with it: two block types that look alike |
| **Steps** | Every landing step in D4 gains a tier, and under G-49 a step that says "land it on the block" becomes a step that says which tier, with an acceptance condition that can distinguish them |
| **Operate and repair** | **A tier is invisible once wired.** At 2am with a meter, two conductors in one footprint are two conductors you cannot tell apart by looking |
| **The new failure mode** | A tier slip. **Safe on a common-potential bank. On the float chain it bypasses a protection, section 6.1** |

**Verdict: no. The trade does not decide whether 16 by 12 fits, it is unsafe on the
only bank large enough to matter, and on the banks where it is safe a bridge comb is
the simpler part.** If the owner nevertheless wants them, **the constraint to write on
the face is: never on a series chain - not the float terminals, not the permissive
string, not either G-27 pair.**

---

## 7. THE VERDICT ON 16 BY 12

**Not answerable as stated, and there are three separate reasons. Two are work, one is
that the target is not a complete specification.**

**1. It is two numbers and an enclosure has three.** No depth is on file for this box
and depth is what the RESET's stacked contact blocks behind a gasketed face, the
receptacle bodies and a relay-plus-module on a rail consume. **16 by 12 can be neither
accepted nor rejected until a depth is named.**

**2. Zero component footprints exist in the tree.** Nineteen lookups, section 9.

**3. The terminal count that would settle it is MAIN-PANEL's own unwritten work**, not
a lookup. 56 clamps is the floor and excludes every panel-internal conductor.

**What I will say without any of them, because the counts are already final:**

**The failure mode of this target is WIDTH, not area.** Height goes 16.6 to 16, four
percent. Width goes 20.7 to 12, forty-two percent, and width carries the rails, both
wireways and all eleven glands. **If 16 by 12 fails, it will not fail by a little bit
everywhere. It will fail on the bottom face and on rail length, and the answer will be
a wider box at about the same height rather than a uniformly larger one.**

**I will not name a size.** 18 by 14 is not the shape of the answer this arithmetic
points at - it adds two inches of height that is not short and two of width that may
not be enough. **The right next number comes from one measurement: eleven grips at
their required spacing, plus one deliberate gap, across a face.** That single lookup
converts this from a guess into a decision, and it is the cheapest question in the
list.

**And one thing that fails today regardless of the box: the 12-way ground bar is at 12
of 12 with three named unknowns outstanding.** Section 4.5. That is not a consequence
of 16 by 12 and it should not wait for it.

---

## 8. WHAT THIS STUDY FOUND THAT NO FILE PREVIOUSLY SAID

Three, each with what I read.

**a. The five sense-circuit burdens have never been given a mounting.** parts.md says
the burden sits in the main panel for both S-08 and S-03, and repeats the two reasons.
**No file says what holds it.** I read parts.md's two readback sections,
electrical-schematic.md section 2 rungs 24 to 28, order.md's list and its
not-covered section, and main-panel-buy.md. **Five components with a stated location
and no carrier**, and they are the one item on the plate that is not a bought device
with a datasheet.

**b. The main panel's bottom-face entry ORDER has never been decided, and it is
MAIN-PANEL's under D-146.** entry-faces.md decides CBL-02 and CBL-03 and says so on
its title line. **F-029's non-adjacency and the two G-27 pairs' gap are enforced at the
display box end and at no other.** The same four jackets land here.

**c. The main panel's material and depth are both absent from parts.md**, where every
other enclosure has three dimensions and the two plastic ones have their material
stated. It matters twice: depth is half of whether any target fits, and material
decides whether the ground bar needs two more ways than it has.

---

## 9. THE LOOKUPS THE OWNER MUST RUN

**In the order that makes them worth running.** The first one alone converts the
verdict from "not answerable" to a decision.

| # | The measurement | Search term |
|---|---|---|
| **1** | **Cord grip bore and required panel spacing**, for the cable outside diameters D6 carries. Against eleven grips plus one separation gap on a 12 in face | `cord grip panel mounting hole spacing wrench flat`; `liquid tight cord grip dimensions clearance` |
| 2 | The enclosure's **DEPTH** and its back-plate dimensions inside a 16 by 12 box, and its **material** | `16 x 12 enclosure back panel dimensions`; `NEMA 4X enclosure 16x12 depth options` |
| 3 | Wiring duct width and the fill ratio it is sized at | `PVC wiring duct sizes fill capacity` |
| 4 | 94.74SMA socket rail length; 55.34 height in socket with clip | `Finder 94.74 socket dimensions DIN rail`; `Finder 55.34 relay dimensions in socket` |
| 5 | 22.32 rail length and depth | `Finder 22.32 modular contactor dimensions` |
| 6 | NDR-240-24 footprint, mounting, **and its convection clearance** | `Mean Well NDR-240-24 dimensions mounting clearance` |
| 7 | Terminal block width per way, single tier, at the conductor size | `DIN rail terminal block width per pole` |
| 8 | 12-way copper ground bar footprint with standoffs | `copper ground bar 12 position dimensions insulated standoff` |
| 9 | Whether the 94.74SMA socket takes a suppression module and the retaining clip together | `Finder 94.74 socket module slot retaining clip compatibility` |
| 10 | 22 mm device stack depth behind a gasketed face at two and three blocks | `22 mm pushbutton contact block stacking depth` |
| 11 | Panel-mount receptacle cutout and body depth | `panel mount duplex receptacle cutout dimensions depth` |

**Not lookups, because no device is chosen:** the main disconnect, the two overcurrent
devices, the R-PI fuse holder, and KM-CHIL. **Four rail positions whose footprint
cannot be looked up because nobody has said what they are.** They are ?1, ?2, ?3 and
?8 on the schematic and they were open before this study.

---

## 10. STATUS

**Stopped part-way.** MAIN-PANEL does not declare itself finished, rule 7.

**Delivered:** the arithmetic that given numbers support, the four counts that need no
lookup, the double-deck trade priced under G-48 with a verdict, the eleven lookups,
and the verdict on 16 by 12 with its three reasons.

**Not delivered, and deliberately: no layout, no placement, no rail order, and no
recommended enclosure size.** D-188 asked for the arithmetic and the verdict.

**What would let MAIN-PANEL finish this:** lookup 1 for the face, lookups 2 to 8 for
the plate, and MAIN-PANEL's own panel-internal conductor list, which
wiring-schedule.md section 7 correctly assigns here and which nobody has started.
**That list is the largest single unknown in the arithmetic and it is not blocked on
anybody.**
