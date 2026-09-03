# AUDIT: the D-105 role reach sweep

Run 2026-09-03. AUDIT designs nothing, owns nothing and fixes nothing. Every item
below is a question or an observation with the file it came from named. No part
number, count, size or pin number in this file is stated from memory: every figure
and every count quoted is quoted from a named file and attributed there.

**The decision being swept: D-105.** Role becomes a PER-CHANNEL SETTING. Any
channel may carry nutrient, pH-up or pH-down, assigned per channel and changeable
by the owner. Previously role was keyed to the channel NUMBER.

**The owner's question:** he expects four things - the plan builder, the signed pH
attribution check, the register schema, and commissioning row C-09 - and asks
whether it reaches further. This sweep answers by looking, not by reasoning from
the four.

---

## 1. What I read, and how

Under rule 8, an absence claim is worth nothing unless the search is named. This
section is that naming, and it distinguishes what was read in full from what was
searched.

### Read in full

| File | Note |
|---|---|
| `agents.md` | Rules 1-11 first, as instructed |
| `software-spec.md` | Document 12, all twelve sections. The thickest source of hits |
| `channel-token.md` | The declaration. CONTROL-SOFTWARE's, definitional end of the token |
| `channel-register.md` | The one record per token, D-057 |
| `commissioning.md` | All rows, the ordering note, the re-measure trigger table, the chiller condition note |
| `interface-table.md` | Every crossing, all five sections |
| `traps.md` | All entries T-001 to T-025 including the un-numbered "What survived the seed retraction" section |
| `findings.md` | The whole table F-001 to F-080 and every "in full" section below it |
| `colour-map-proposal.md` | |
| `order.md` | |
| `subsystems/dosing.md` | |
| `subsystems/dosing-f002-proposal.md` | |
| `subsystems/control-software.md` | Including its own D-105 routing section |
| `subsystems/control-software-f004.md` | The plan-admission and exclusion-domain reasoning |
| `subsystems/interconnect.md` | |
| `subsystems/display-box.md` | |
| `subsystems/pump-boxes.md` | |

### Read in part, plus a full-file search

`decisions.md` is 1935 lines. I read lines 1-120 (the G-rule block), 1120-1150
(D-077, D-078), 1225-1400 (D-083 through D-090), 1560-1600 (D-098, D-099, D-100)
and 1855-1935 (D-104, D-105, D-106, D-107) in full. Across the WHOLE file I
searched for: `CH5`, `CH6`, `six nutrient`, `two pH`, `pH pair`, `nutrient
channel`, `eight channels`, `six of the eight`, `by elimination`, `adjacent
token`, `neighbouring colour`, `station`, `injection plan`, `injection group`,
`runs last`, `excluded from`, `exclusion`, `role`, `duty class`, `forearm`,
`D-084`, `D-085`, `D-10[0-9]`.

`parts.md` was read at lines 20-60 and 300-360 and searched in full for `pH`,
`acid`, `role`, `channel`.

### Searched, not read in full

`subsystems/water.md`, `subsystems/water-s18-f003.md`, `subsystems/main-panel.md`,
`subsystems/main-panel-buy.md`, `subsystems/main-panel-poles.md`,
`subsystems/pump-boxes-pulldowns.md`, `subsystems/pump-boxes-p09.md`,
`subsystems/display-box-sweep.md`, `subsystems/display-box-short-column.md`,
`subsystems/control-software-p09.md`, `subsystems/dosing-verification-options.md`,
`subsystems/dosing-f004-wet-side.md`.

Searched for: `pH up`, `pH-up`, `pH down`, `pH-down`, `pH channel`, `pH pair`,
`pH probe`, `pH runs`, `acid`, `base`, `role`, `nutrient`, `injection group`,
`blocked`, `channel`, `CH5`, `CH6`. Where a search hit, the surrounding passage
was read: `dosing-f004-wet-side.md` lines 125-200, `display-box-sweep.md` lines
52-65 and 175-250, `dosing-verification-options.md` around its option table.

**Four of these returned NO occurrence of the word `channel` at all**, which is why
they carry no hit below: `water.md`, `water-s18-f003.md`, `main-panel.md`,
`main-panel-buy.md`, `main-panel-poles.md`, `pump-boxes-pulldowns.md`. That is a
search result, not an inspection.

### Not read

`audit/2026-08-30-channel-token.md`, `audit/2026-08-30-displaybox-vs-mainpanel.md`,
`audit/2026-09-03-decisions-impossibility-grading.md`,
`audit/2026-09-03-doc12-vs-frozen.md`, `audit/2026-09-03-second-source-sweep.md`.
These are AUDIT's own prior outputs. Under G-37 a citation is not a source, and
every claim they carry is a claim about a document listed above. Reading them would
have produced corroboration of the second-source shape rather than evidence. Named
here so their exclusion is a decision and not an oversight.

---

## 2. Hits, by category, with the verdict

**Verdicts used, per the instruction:**

- **BREAKS** - the item becomes wrong or uncheckable under D-105 and nothing in the
  tree currently notices.
- **CHANGE** - the item survives but its wording, its key or its trigger has to
  move from the number to the setting.
- **DISSOLVES** - the item stops existing, because the thing it worried about is no
  longer a fixed property.
- **SURVIVES** - listed because it was checked and is clean. Reported so the clean
  result is a named search rather than a silence.

### Category 1. A channel NUMBER determines what a channel does, or what may be done to it

| # | File and what it says | Verdict |
|---|---|---|
| H-01 | `channel-register.md`, the register table. The Role column carries `pH DOWN` against CH5 and `pH` against CH6, and `nutrient` against the other six, as fixed cell values in the one record per token | **CHANGE.** This is the owner's item 3, the register schema. Naming it here because the Role column already EXISTS and `software-spec.md` 3.2 already reads the pH set from it. What changes is not that the column appears; it is that its values become settable and dated, and the file's surrounding prose has to stop asserting them |
| H-02 | `channel-register.md`, "What the software does know, and it is all it knows": "The controller independently marks CH5 as pH-down through its blocked-channels path, which is a ROLE rather than a product. pH channels are excluded from every injection plan by construction." | **CHANGE.** Three separate things keyed to a number in one paragraph: the CH5 marking, the exclusion, and "by construction" - which is exactly the fixed-list wording D-105 replaces. Also category 3 and 4 |
| H-03 | `channel-token.md`, "One binding rule that comes from S-16, not from legibility": "pH up and pH down shall not receive adjacent tokens and shall not receive neighbouring colours. Far apart on every axis at once. Declared now, applied once the products are assigned" | **DISSOLVES** as a constraint on the numbering, exactly as D-105 and F-063 record. **But it leaves a tail that is a CHANGE and is not yet written anywhere:** the rule becomes a constraint on the ASSIGNMENT, and the moment it applies moves. The file says "applied once the PRODUCTS are assigned". Under D-105 the binding moment is once the ROLES are assigned, and roles are changeable after that moment while products under G-17 are not. Those are two different clocks and the file names the wrong one |
| H-04 | `colour-map-proposal.md`, constraint 1: "CH5 and CH6 maximally separated. They are the pH pair and they are adjacent tokens, F-063." And the CH5 and CH6 rows, whose entire justification is "pH" | **DISSOLVES** as a rationale. The proposal's hardest constraint was a claim about two named numbers and there is no fixed pair to bind |
| H-05 | `decisions.md` D-099, the frozen colour table with CH5 blue and CH6 yellow | **DISSOLVES** as to its reason; the BINDING itself is untouched and must not be reopened. D-099 says the colour is an identity axis on the token and "nothing is permitted to compute from it", so no behaviour is keyed to it and the table is harmless as it stands. What is gone is the argument for why those two colours sit where they sit |
| H-06 | `decisions.md` D-085, "NO EXTRA WALL LENGTH for the CH5 and CH6 gap. The free axes only", taking instead "non-neighbouring colours on the two tokens... and whatever spacing the existing station run gives" | **DISSOLVES** in the form it is written. Its CONTENT survives - spend no wall length, use the free axes - but its subject changes from two named tokens to whichever two carry the pH roles. D-085's own closing line, "IF THE SIGNED CHECK IS EVER REMOVED, THIS REOPENS", is unaffected and still stands |
| H-07 | `decisions.md` D-077's recital, which states the CH5 marking and the CH6 elimination as what the software knows | **CHANGE**, by annotation. The reversal rule keeps entries whole, so this is an annotation and not a rewrite |
| H-08 | `decisions.md` D-078 and D-086, and the chain that reads "the two 1000 mL channels are the pH adjusters" | **DISSOLVES.** Already withdrawn as F-071 and marked in D-086 as an inference from a seed. D-105 removes even the need for the inference |

### Category 2. A fixed count assumed, or written as a property

| # | File and what it says | Verdict |
|---|---|---|
| H-09 | `software-spec.md` 2.5.2: "The pH probe attributes the two pH channels and nothing else" | **CHANGE.** Must read: the channels whose role is pH-up or pH-down |
| H-10 | `software-spec.md` 2.5.3: "The two pH channels cannot be attributed at the same time" | **CHANGE.** Same reason. Note that 5.2.3, the admission rule, is already worded "At most one pH-moving channel", which is robust; 2.5.3 is the count-worded restatement of it |
| H-11 | `software-spec.md` 6.3: "For the six nutrient channels EC moves the same way for all of them, so a crossed pair still confirms itself completely" | **CHANGE.** The claim survives keyed to role. The count does not |
| H-12 | `software-spec.md` 6.6, the attribution table: "Which of the two pH channels moved the tank"; "Anything about the six nutrient channels" | **CHANGE** |
| H-13 | `software-spec.md` section 12, Status: "Structurally impossible rather than pending, and it should not be read as a gap waiting to close: ... attribution for six of the eight channels (6.6)" | **CHANGE, and it is a GRADING error that D-105 has just created.** Under G-36 as amended by D-103, structural means no addition could change it. The number of unattributed channels is now a function of the assignment: an owner who sets a third channel to a pH role changes it, and setting a pH channel to nutrient changes it the other way. What is structural is that attribution exists only for channels carrying a pH role. The COUNT is CURRENT, and what would change it is a role setting. This is the first instance of G-36's own question landing on a change rather than on an old claim |
| H-14 | `software-spec.md` 7.3, the fault name and definition: "F-PH-ATTRIBUTION: both pH-moving channels in one window" | **CHANGE.** "Both" is a count word. See section 5: whether more than two channels may carry a pH role is not settled anywhere, and the fault's shape depends on the answer |
| H-15 | `channel-register.md`: "Six nutrient channels and two pH" | **CHANGE** |
| H-16 | `findings.md` F-050: "The dosing failure of a backwards head is caught on seven of eight channels ... and is silent on fulvic" | **CHANGE.** The seven-of-eight count is a consequence of the current assignment, not a property of the build |
| H-17 | `interface-table.md` rows S-15, S-16, S-17, S-19 | **SURVIVES.** Checked deliberately because they are FROZEN and a frozen row that needed changing would be the most expensive hit in this sweep. S-16 as frozen names "the pH up and pH down channels" and never CH5 or CH6; its constraint 1 is worded by role; constraint 3 anchors the sign to C-03's measurement. S-15, S-17 and S-19 are role-blind or role-worded. **Not one frozen interface row keys behaviour to a channel number.** That is the single best piece of news in this sweep and it is why D-105 costs what it costs rather than more |

### Category 3. Role derived rather than read

| # | File and what it says | Verdict |
|---|---|---|
| H-18 | `channel-register.md`: "CH6 is the other pH channel by elimination. That is an inference, not a statement, and it is marked as one", and the Product cell "pH up by elimination, NOT stated" | **DISSOLVES.** D-105 says so in terms. The register still carries the words |
| H-19 | `channel-register.md`, the three conclusions resting on an inference from a default. Conclusion 1 is that the two 1000 mL channels are the pH adjusters and therefore that the size axis separates the pair for free | **DISSOLVES** for conclusion 1. Conclusions 2 and 3 - F-066, and DOSING's three depth classes - are volume-derived and were already qualified by D-086; D-105 does not touch their volume half. It does touch F-066's SUBJECT, below |
| H-20 | `findings.md` F-066: "The two smallest containers are the two pH channels. Smaller vessel means more frequent change... So the pair the system most wants left alone is the pair that gets handled most often" | **DISSOLVES.** Its subject was a role read off a container size. No role comes from a size any more. Note that F-066 is recorded as "the strongest argument on DOSING's path for spending effort on the pH stations rather than distributing it evenly across eight" - with the pair unfixed, the argument now points the other way, toward distributing evenly, because any station may become a pH station |
| H-21 | `software-spec.md` 3.2: "The set of pH-moving tokens is read from the register's role column. It is never computed, never hard-coded as a pair, and never derived from 'the other pH channel'." Then: "Today the register carries one role marking and one inference that is marked as an inference; code must treat both as data it was given" | **CHANGE**, and the first sentence deserves saying out loud: **it is already written the D-105 way and was before D-105 existed.** The second sentence is what changes, and it is moot in the right direction. This is the one place in the tree where role was already an attribute read from a record rather than a property of a number |
| H-22 | `decisions.md` D-105 itself: "What BOSS cannot confirm from the tree is whether the config carries a role marking for CH6 the way it does for CH5 - channel-register.md states the CH5 marking and calls CH6 an inference, and nothing in the tree shows the blocked list itself" | **CHANGE, and it is a fifth thing.** D-057 and `software-spec.md` 2.6.5 say an attribute is recorded ONCE, in the register, and 3.2 says the application reads it "from one record per token and never from a second place". But the only role marking anybody has actually SEEN lives in a controller config's blocked-channels path that no file in this tree shows. So role now has two candidate homes, the register and that config, and the tree does not say which is definitional or how they are kept in agreement. Before D-105 that was an archaeology question about CH5. After D-105 it is the provenance of the field the signed check reads |
| H-23 | `interface-table.md` S-17, "Fulvic channel \| any attribution mechanism \| CLOSED as unattributed"; `commissioning.md` C-04 scoped "per EC-moving channel"; `subsystems/display-box-sweep.md` twice, "nothing else catches it on the fulvic channel" and "A severed STEP on the fulvic channel is a silent no-delivery"; `findings.md` F-050 | **CHANGE, and this is a fifth thing.** D-105's role set is nutrient, pH-up, pH-down. **Fulvic is not a value in it.** So "the fulvic channel" is not derivable from the role setting at all: it is derivable only from the product binding at C-09. Four files speak of "the fulvic channel" as a settled singular identity while no file says which channel it is, and D-107 has just put the untestability of D-013's premise on C-04's row, whose scope is the derivation in question. A role setting that reads `nutrient` on a fulvic channel is correct and tells nobody that S-17 applies to it |

### Category 4. Something ORDERED or GROUPED using role

| # | File and what it says | Verdict |
|---|---|---|
| H-24 | `channel-register.md` and `decisions.md` D-077's recital: "pH channels are excluded from every injection plan by construction" | **CHANGE.** This is the owner's item 1, the plan builder. Named here because the wording lives in two files OUTSIDE the software specification, and a plan builder corrected in code while the register still says "by construction" leaves the fixed-list claim standing in the file every other subsystem reads |
| H-25 | `software-spec.md` 5.6.6: "No opposing pH dose while a pH attribution window is open"; 2.2.5 and G-16a: the corrective path must be structurally incapable of offering "the opposing pH channel"; 9.1.5: "If a pH attribution window was open at the cut, refuse the opposing pH channel until an operator resolves it" | **CHANGE, and it is a fifth thing with a sharp edge.** "Opposing" is computed from role. With role settable, the opposing set can change while a window is open. A guard that resolves "opposing" at the moment it is evaluated, against a setting that changed since the window opened, refuses the wrong channel and permits the right one to be violated. The prohibition is correct; its subject is now time-varying and no file says which instant the set is taken at |
| H-26 | `software-spec.md` 8.1, durable state: "The settle window state: open or closed, which channel, baseline value and spread, when taken, earliest valid read" | **CHANGE.** The window records WHICH CHANNEL and not what role that channel had when the window opened. That is the field H-25's guard needs. 8.1 does separately require "The channel register's attributes as the application read them", which may already cover it, but it covers them as a set and not as a stamp on the open window |
| H-27 | `software-spec.md` 5.2.3, plan admission: "At most one pH-moving channel carries a nonzero commanded volume"; and 5.2's "what counts as fired" note | **SURVIVES.** Worded by role, quantified as "at most one", and robust to any number of pH-role channels. It is the correct shape and D-105 does not touch it |
| H-28 | `subsystems/control-software-f004.md`, "Enforcing S-16 constraint 1", including the exclusion-domain argument and the overshoot-correction row | **CHANGE.** Same derivation as H-25. Note this file is superseded as a deliverable by document 12 but stands as reasoning, per `software-spec.md` 1.3, so its wording is still read |

### Category 5. Wrong, ambiguous or uncheckable if the owner changes a role after commissioning

This is the category the instruction calls the important one, and it is where the
sweep found what the owner did not name.

| # | File and what it says | Verdict |
|---|---|---|
| H-29 | `commissioning.md` C-03: "pH step per single dose, pH up and pH down separately, AND SIGNED: the measured step IS the reference sign for S-16's direction check, per D-083 and G-32. The sign comes from this measurement and never from a product name." Also `software-spec.md` 6.3 and N-6 | **BREAKS, and it is the sharpest hit in the sweep.** A recorded C-03 value is a signed magnitude bound to a token AND to the role that token held when it was measured. Change a role after C-03 and one of two things is true: the channel now carries a pH role and has no C-03 reference at all, or it carries a C-03 reference measured against the opposite product. Nothing in the tree marks a C-03 figure with the role it was taken under, and nothing voids it |
| H-30 | `commissioning.md` C-04, scoped "per EC-moving channel", with D-107's scope note now promoted onto the row | **BREAKS.** The scope is derived from what a channel does. A channel moved from nutrient to a pH role keeps a C-04 figure filed against a channel that is no longer expected to move EC; a channel moved the other way has no C-04 figure and the EC check has nothing to turn a movement into a verdict with. D-107 has just recorded that this scope protects D-013's premise from measurement. D-105 makes the same scope a function of a settable field, which is a second and different way for the scope to be wrong |
| H-31 | `commissioning.md`, the re-measure trigger table. Its rows are: any plumbing change; pump or impeller service; probe replacement, recalibration or cleaning; a product or recipe change; anything added to the loop; any rewiring or renumbering of channels; anyone touching the supply trimmer; a pump tube change; any change to MS1 or MS2; periodically; a driver replaced | **BREAKS. A ROLE CHANGE IS NOT ON THIS LIST.** A role change accompanied by a product change is caught by "A product or recipe change - C-03, C-04". A role change WITHOUT a product change is caught by nothing, and D-105 makes role a SETTING the owner changes rather than a wet-path event. The list is an event list by design, and this is a new event with no row |
| H-32 | `channel-token.md`, "When a channel has to change", whose four cases are: a head moved between boxes; a driver replaced; a product retired with the channel kept; a channel retired outright | **BREAKS. A ROLE CHANGE IS NOT ONE OF THE FOUR CASES.** So there is no universal-rules paragraph applied to it, no OUT OF SERVICE entry, and no "C-09 is re-run for all eight channels" instruction, which is the instruction every other case carries |
| H-33 | `software-spec.md` 3.4: "While software and the wall may disagree about a channel - during a rewire, a relabel, a move, a driver change that voids C-01 - the channel is OUT OF SERVICE and the sequencer skips it" | **CHANGE.** A role change is a disagreement between software and the physical product of exactly the kind 3.4 exists for, and it is not in 3.4's list of causes. And F-075 already records that 3.4 has an entry and no exit and that 5.2's admission does not check C-09, with D-102's deadline attached. **A role change would enter a state that has no exit, and the state it needs to gate on is C-09, which admission does not read.** D-105 lands directly on top of an already-open defect |
| H-34 | `software-spec.md` 2.1.8 and 2.1.9: a driver replacement and a pump tube change each VOID C-01 for that channel, and a voided figure BLOCKS COMMANDING that channel | **BREAKS, by omission, and the omission is visible because the mechanism exists.** The specification has a working pattern for "this event invalidates that measurement and blocks the channel until it is re-taken". It is applied to C-01 twice. **There is no equivalent that voids C-03 on a role change.** So the one figure whose wrongness makes the signed check confirm an error is the one figure with no voiding rule |
| H-35 | `subsystems/dosing-f004-wet-side.md`, C-02's named procedure, step 7: "Repeat for the pH channels separately, on the pH probe. Different probe, different response... pH up and pH down separately, never together"; and its "One number or many" table: "The pH channels settle differently because both probe and response differ, and a buffered solution moves non-linearly" | **CHANGE.** The C-02 measurement set is role-scoped: which channels get pH-probe settling numbers follows the assignment. Less sharp than C-03 because the dominant leg is a loop property, but the file states the pH channels settle differently, so the per-channel half is role-dependent |
| H-36 | `decisions.md` D-088 and `traps.md`, "What survived the seed retraction": DOSING's hazard rule, "no acid or base container stationed where breaking or lifting it puts it above the operator's forearms", survived the retraction precisely because it is keyed to ROLE. Frozen out of that as **G-34**: "A rule keyed to what a thing IS outlives a rule keyed to how big it is. Sizes are provisional until something is bought. **Roles are decided earlier and change less**" | **CHANGE, and it is a fifth thing that nobody has looked at.** G-34's RULE is unaffected: a role is still a better key than a dimension. **Its stated REASON is now false.** Under D-105 role is the most changeable attribute in the register, and it is changeable by a setting rather than by a purchase. The consequence is physical: the hazard rule's subject is a station, `dosing-f002-proposal.md` fixes the station as "The FIXED spot in Z4", and G-17 and G-18 fix the jug and the tube to the channel for life. **So a role change moves which fixed stations must satisfy an acid-and-base hazard rule, and the station cannot move.** Nobody has said whether a role assignment is constrained by where the station physically sits |
| H-37 | `subsystems/dosing-f002-proposal.md`: step 3 of the jug change, "park the jug-side half at its own channel's point, never the floor, never a shared tray with acid or base"; failure mode 5, "Seals and springs are wear items in acid and base. A seal in the pH-down line is a scheduled replacement nobody has scheduled"; failure mode 10, "acid and base halves must not share a drip catch or a rag" | **CHANGE.** Three physical and maintenance items keyed to role on a named line. They follow the assignment and nothing in the file says they do. Most of failure mode 5 and 10 is recorded as "no longer required by this proposal" under the owner's rulings, so the live one is the parking and shared-tray rule, and the fact that "the pH-down line" is now a line the owner can nominate |
| H-38 | `software-spec.md` 11.15: "Which product sits on which token, and the token colours ... The application carries product as an attribute it is given, never as identity, and never as the source of an expected sign" | **CHANGE.** Role is now a second attribute the application is given, and unlike product it IS a source of an expected direction. The sentence that protects the tree from deriving a sign from a label has no counterpart for deriving a direction from a setting. G-32 as amended says the rule binds on role; 11.15 has not been told |
| H-39 | `findings.md` F-080 as amended, and D-105: "THE MARKER GATE SURVIVES AND TIGHTENS: markers are not made until C-09 has bound both PRODUCT and ROLE. Still free before C-09, still eight relabels after" | **CHANGE, and it is a fifth thing.** The gate protects the FIRST assignment. Under D-105 a role change AFTER C-09 is permitted, the markers are already made, and the constraint the gate exists to protect - the pH pair on non-neighbouring colours, per H-03 and D-099 - is exactly what a later role change can violate. The gate as written has no second firing. Nothing in the tree prices a post-C-09 role change against the relabel cost the gate was created to avoid |
| H-40 | `decisions.md` D-084 and `findings.md` F-068: the token carrier specified against three duty classes, acid, base and generic nutrient-concentrate, as a UNION over the wall rather than per channel | **SURVIVES, and D-105 strengthens it.** Because any channel may now become acid or base, the union is the only defensible specification and per-channel carrier specialisation is foreclosed rather than merely unattractive. DOSING's carrier requirement, "chemical duty is the union of everything on the wall, not each channel's own product", was written for drips and one rag and is now load-bearing for a second reason |

### Category 6. Anything keyed to the pH pair being ADJACENT or maximally separated

The design-time items are H-03, H-04, H-05 and H-06 above and all four DISSOLVE or
carry an assignment-time tail. What remains is the physical half of the question
the owner asked - cable cores, colours, layout, marker positions, wall positions.

| # | What was searched | Verdict |
|---|---|---|
| H-41 | `subsystems/interconnect.md`, `subsystems/display-box.md`, `subsystems/display-box-sweep.md`, `subsystems/display-box-short-column.md`, `subsystems/pump-boxes.md`, `subsystems/pump-boxes-p09.md`, `subsystems/pump-boxes-pulldowns.md`, `subsystems/main-panel.md`, `subsystems/main-panel-buy.md`, `subsystems/main-panel-poles.md`, `order.md`, `parts.md` | **SURVIVES. Nothing keys a cable core, an insulation colour, a duct, a gland, a wall position or a bundle adjacency to pH or to any role.** Every adjacency rule in the wiring is role-blind: F-029 separates the permissive coil drive from its own readback, F-030 pairs every STEP and DIR with its own return, G-29 pairs a signal with its pull's destination, D-098 excludes two Pi pins from signals whose safe power-on state is low. **The only channel-keyed thing on the physical side is the token itself**, and `colour-map-proposal.md` moved the channel colour onto the marker rather than the insulation, so no conductor carries a channel colour at all. **This is a search, not an inspection**, and the search terms are listed in section 1 |

---

## 3. The owner's question, answered directly

Beyond the plan builder, the signed attribution check, the register schema and
C-09, **it reaches eight further places.** Ordered by how much they cost if nobody
touches them.

**1. C-03's signed reference and C-04's scope are recorded, role-dependent data
with no re-measure trigger for a role change.** H-29, H-30, H-31, H-34. This is the
one that turns the owner's own named risk into a permanent condition rather than a
moment. The tree already has the exact mechanism it needs - a driver change VOIDS
C-01 and blocks commanding - and applies it to the figure whose wrongness is
loudly detectable while leaving it unapplied to the figure whose wrongness makes
the check confirm the error.

**2. A role change is not a case in any change procedure.** H-31, H-32, H-33.
`channel-token.md`'s change procedure has four cases and this is not one;
`commissioning.md`'s re-measure trigger table has eleven rows and this is not one;
`software-spec.md` 3.4's OUT OF SERVICE causes do not include it. And F-075,
already open with D-102's deadline, is that 3.4 has an entry and no exit and that
admission does not check C-09. D-105 lands on top of that.

**3. The physical, wet-side items keyed to acid and base.** H-36, H-37. DOSING's
forearm hazard rule, the parking points, the shared drip catch and rag, and the
scheduled seal wear on a pH line all follow the ROLE and the stations are FIXED.
And G-34, the rule frozen out of what survived the seed retraction, gives as its
reason that "roles are decided earlier and change less". **D-105 makes that
sentence false.** The rule is still right; the argument printed under it is not.

**4. Where role definitionally LIVES.** H-22. D-057 and `software-spec.md` 2.6.5
and 3.2 say an attribute is recorded once, in the register, read from one record
and never from a second place. The only role marking anyone has actually seen is in
a controller config's blocked-channels path that no file in this tree shows. Two
homes for one attribute is D-057's own defect, and it is now the provenance of the
field the signed check reads.

**5. "The fulvic channel" is a fixed identity in four files and fulvic is not a
value in D-105's role set.** H-23. Role cannot tell anyone which channel S-17
applies to. That derivation now runs through the product binding alone, at the same
moment D-107 put the untestability of D-013's premise onto C-04's row.

**6. The count claims read as properties, in six places, one of which is graded
STRUCTURALLY IMPOSSIBLE.** H-09 to H-16. `software-spec.md` section 12 lists
"attribution for six of the eight channels" among the things that are structural
rather than pending. Under G-36 as amended by D-103 that count is CURRENT and what
would change it is a role setting. This is a new grading error created by the
decision itself, not an old one found.

**7. "Opposing" is now a time-varying set, and the open window does not record the
role it was opened under.** H-25, H-26, H-28. The prohibition on dosing the
opposing pH channel into an open window is correct and its subject can change while
the window is open.

**8. The marker gate fires once.** H-39. It protects the first assignment. A role
change after C-09 can violate the colour separation the gate exists to protect,
with the markers already made and the cost already at eight relabels.

**And the thing that did NOT reach, stated because the owner asked about it
specifically.** Nothing on the physical side is keyed to the pH pair being
adjacent, separated or anywhere in particular: not a cable core, not an insulation
colour, not a duct, not a gland, not a wall position. H-41, with the twelve files
named. And no FROZEN interface row keys behaviour to a channel number: H-17, with
S-15, S-16, S-17 and S-19 each checked. D-105 is cheap in the hardware and
expensive in the paperwork, and that asymmetry is what the sweep found.

---

## 4. Is C-09 sufficient? The risk the owner named himself

The owner's own statement of the risk, from D-105: **a role that can change is a
role someone can change wrongly, and a wrong role makes the signed check expect the
wrong direction, so the check confirms the error.** G-32 as amended by D-105 binds
on role for that reason, and D-106 puts the role question on C-09's script.

**C-09 as a TEST is sufficient. C-09 as a SCHEDULE is not.**

### Why the test is sufficient

C-09's new question (b), as `commissioning.md` now carries it, is: is this
channel's role setting - nutrient, pH-up or pH-down - the role this product
actually has. That is a comparison between a setting and a physical product, made
by eye, with the jugs present, per channel, for all eight. It does not depend on
any measurement, any instrument, or any other row. **Run at any moment, it catches a
wrong role.** Nothing about a role change after commissioning degrades the test
itself. AUDIT has no criticism of question (b) as written.

### Why the schedule is not

Take the case the owner asked about: a role is changed AFTER C-09 has been run.

**Nothing in the tree would notice.** Named, with what was read to establish it:

- **`commissioning.md`, the re-measure trigger table.** Eleven event rows, read in
  full. The only row that could catch it is "A product or recipe change - C-03,
  C-04", which fires on a product event and does not name a role, and which
  schedules C-03 and C-04 and not C-09. The row that schedules C-09 is "Any
  rewiring or renumbering of channels". A role change is neither a rewiring nor a
  renumbering, and D-105's whole point is that it requires neither.
- **`channel-token.md`, "When a channel has to change".** Four cases, read in full.
  Every one of them carries "C-09 is re-run for all eight channels, never for the
  one that changed". A role change is not one of the four, so it inherits no
  instruction, including that one.
- **`commissioning.md` C-09's own Blocked-on cell:** "Repeat after ANY rewiring or
  renumbering." Same two events. Not a setting.
- **`software-spec.md` 5.2, plan admission.** Seven conditions, read in full. A
  live token, a non-void C-01 and a recorded C-17, at most one pH-moving channel
  fired, no open opposing window, no fill, no latched weld, command and readback
  agreeing. **C-09 is not among them - which is F-075, already open - and neither
  is anything about role provenance or role age.**
- **`software-spec.md` 2.1.8 and 2.1.9.** The voiding mechanism exists and covers a
  driver change and a tube change, both against C-01. There is no rule that voids
  C-03 on a role change, so a stale signed reference is not blocked, not flagged,
  and not distinguishable from a fresh one.
- **`software-spec.md` 8.1.** Durable state records the register's attributes as
  the application read them. That could hold a role, but nothing states that a
  CHANGE in that value is an event with a consequence.
- **The check itself.** By G-32 as amended, the signed check cannot notice: a wrong
  role makes it expect the wrong direction, so a wrong-role dose scores PASS. The
  fifth outcome, WRONG DIRECTION, fires when the movement opposes the prediction -
  and after a role change the prediction has moved with the error, so the two agree
  and the outcome is a pass.

### The shape of the gap, stated and not solved

It is three separate absences and they are not interchangeable:

1. **No trigger.** No file names a role change as an event, so no file can schedule
   anything against it.
2. **No invalidation.** C-03's signed reference is not voided by a role change the
   way C-01 is voided by a driver change. The mechanism exists elsewhere in the
   same document and is not applied here.
3. **No detection.** The only check that catches a wrong role is C-09, and the only
   thing that runs C-09 is a person following a trigger list that does not contain
   this event.

**And the shape has a name already in the tree.** `commissioning.md`'s own opening
line says a measurement taken against a mislabelled channel "is not a wrong number,
it is a right number filed against the wrong thing, and every later check confirms
it". D-102 attached a deadline to F-075 on exactly that reasoning: before C-01 runs
a wrong channel is a mistake, after C-01 runs it is a dated entry with a procedure
behind it and looks like data. **A role changed after C-09 has the same shape one
level up: before the change, C-03's sign is a measurement; after it, the same
number is a dated entry that the check divides its direction by, and nothing
downstream can tell which it is holding.**

**AUDIT designs no mechanism and proposes no row.** What is reported is that the
gap is real, that it is a scheduling gap rather than a capability gap, and that the
three absences above are the shape of it.

---

## 5. What I could not settle

Named rather than left, per rule 8 and G-35.

1. **How many channels may carry a pH role.** D-105 says any channel may carry
   nutrient, pH-up or pH-down. It does not say at most one may carry pH-up, or that
   at most two may carry a pH role at all. `software-spec.md` 5.2.3 is robust to
   any number; 2.5.3, 6.6, 7.3 and S-16's own constraint 1 are all written for
   exactly two, one of each. If three channels may carry pH roles, or two may carry
   the same one, F-PH-ATTRIBUTION's definition and 6.6's attribution claim both
   change shape. Nothing in the tree answers this and I am not inferring it from
   the old fixed pair.

2. **Whether fulvic is a role, a product, or neither.** H-23. D-105's role set has
   three values and fulvic is not one. S-17 is frozen against "Fulvic channel".
   Unresolvable from what I read.

3. **Where role is definitionally held**, the register or the controller's
   blocked-channels path. H-22. D-105 calls the CH6 half of this an owner lookup
   and marks it optional. The general question - which of the two is the one record
   under D-057 - is not the same question and is not marked anywhere.

4. **Whether a role change is permitted while a pH attribution window is open**, or
   between C-03 and the next dose. H-25, H-26. Nothing in the tree contemplates the
   setting moving under a running mechanism.

5. **Whether a role assignment is constrained by physical station position.** H-36.
   DOSING's forearm hazard rule is keyed to acid and base, stations are fixed, and
   nobody has said whether the owner may assign a pH role to a station that fails
   the hazard rule.

6. **Whether the assignment-time restatement of the non-adjacency rule has been
   made.** H-03. D-105 and F-063 both say the restatement is CONTROL-SOFTWARE's,
   and `subsystems/control-software.md` records the instruction along with "Write in
   ONE pass at the end, and not before the reach sweep reports". So as of this
   sweep the rule stands in `channel-token.md` in its old numbering form, and under
   agents.md rule 9 nothing should be built against it in either form until it is
   restated. That is a state, not a defect.

7. **I did not read the five files in `audit/`.** Reason given in section 1. If any
   of them carries a role-keyed claim not traceable to a file I did read, this
   sweep did not see it.
