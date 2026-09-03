# AUDIT run 4: every impossibility claim in decisions.md, graded under G-36, with a cost column

Target: decisions.md, the whole file. The G-rule table at the top and every D-nnn
entry, D-001 to D-102.

This run repeats the Part 2 grading of `audit/2026-09-03-doc12-vs-frozen.md` on a
harder target, and adds the column that run did not have: **what somebody would
decline to buy or decline to build on the strength of each claim.** The owner's
reason, verbatim: "That is where a false impossibility turns into a real loss, and
it is not visible from the claim itself."

## What I read, in full

- `agents.md`, all of it, including rules 1 to 11 and the AUDIT section.
- `decisions.md`, all 1685 lines. The G-rule table, the parts-in-hand table, the
  site conditions table and every D-nnn entry.
- `interface-table.md`, all 103 lines. Every fluid, power, signal, cable and
  placement row.
- `commissioning.md`, all 90 lines. Every C-nn row, the ordering note, the
  re-measure triggers and the chiller-state section.
- `audit/2026-09-03-doc12-vs-frozen.md` from Part 2 to the end: the 24-claim table,
  "The three that are dressed as structural", the two claims document 12 got right,
  "What I could NOT settle" and the agreement section. I read the heading outline of
  Part 1 and did not read Part 1's 126-row table or its expanded entries.
- `traps.md` T-023 in full, plus the heading list for T-003, T-012, T-014, T-016
  and T-017.
- `findings.md` rows F-001, F-003, F-015, F-019, F-033, F-035, F-045, F-053, F-057,
  F-059, F-060, F-061, F-062, F-063, F-070, F-072, F-073, F-074 and F-075.
- `parts.md`, the section "DIAG and INDEX, and why the ruling cannot rest on the
  datasheet", in full, plus the lines matching INDEX elsewhere in that file.

## What I did NOT read, named so nothing here rests on it

Under agents.md rule 8, these are named because several of my gradings would move if
they contain something I have not seen, and I say where in the text that matters.

- Every file in `subsystems/`. All nineteen: control-software.md, -f004.md, -p09.md,
  display-box.md, -sweep.md, -short-column.md, dosing.md, -f002-proposal.md,
  -f004-wet-side.md, -verification-options.md, interconnect.md, main-panel.md,
  -buy.md, -poles.md, pump-boxes.md, -p09.md, -pulldowns.md, water.md,
  water-s18-f003.md.
- `software-spec.md` (document 12). I graded decisions.md's restatements of it, not
  the document.
- `channel-token.md`, `channel-register.md`, `colour-map-proposal.md`, `order.md`.
- `parts.md` other than the section named above, and `findings.md` other than the
  rows named above, and `traps.md` other than T-023 and the headings.
- Any datasheet. Every figure quoted below is quoted from the file that carries it.

**I state no part number, count, size, resistance or pin number.** Where a figure is
load-bearing I name the file that holds it and stop. Where a claim needs a lookup I
name the requirement and a search term.

## What I did

I swept decisions.md for claims of the form: impossible, cannot, can never, no way
to, forecloses, permanently, nothing can, is not possible, has no source, will never,
unexecutable, not enforceable, removed, dissolved, foreclosed, invisible, nobody
solves, off the table, deleted, irreversible, unmeasurable, nothing measures, nothing
notices - and claims with none of those words that assert a capability is GONE.
I graded each under G-36, which is frozen in this same file.

**Prohibitions are included.** G-16, G-19, G-25 and G-99-style rules do not say a
thing is impossible; they say it may not be done. Under G-36 that still follows from
a frozen rule, so it grades STRUCTURAL, and the cost column still applies: somebody
declines something on the strength of a prohibition exactly as they do on the
strength of an impossibility. Each such row is marked *(prohibition)* so the owner
can see the composition of the count rather than only its size.

## Counts

| | Count |
|---|---|
| Claims graded | **60** |
| **STRUCTURAL** | **37** |
| **CURRENT** | **19** |
| **MIXED** - one sentence running a structural half and a current half together | **4** |
| Of the current and mixed, **correctly graded in place** by their own entry | 7 |
| **FLAGGED**: would stop a purchase, a measurement or a capability | **8** |
| Of the flagged, **retroactively self-making** if declined | **4** |
| Could not settle from the tree | 6 |

The seven correctly graded in place are the model and are marked **MODEL** in the
table. They matter because they prove the discipline is available in this file
rather than only asked for by it.

---

# The grading table

Cost column: what somebody would decline to buy or decline to build on the strength
of the claim. "Nothing" means no purchase, no commissioning row and no capability is
declined because of it - the claim being wrong would cost the project nothing.

## STRUCTURAL

| # | Where | The claim | Grade | Cost when wrong |
|---|---|---|---|---|
| 1 | G-01 | Float switches are hardwired to relays and **invisible to the Pi** | STRUCTURAL, frozen owner rule | Nothing. The capability it removes is one the panel provides in hardware under G-26 |
| 2 | G-02 | The Pi gets **exactly one** level signal | STRUCTURAL, frozen owner rule | Nothing on its own. It is the ground of the tank-level claims, and the rule is explicit rather than inferred |
| 3 | G-04 | **No flow meters on the dosing lines. Nothing measures what a peristaltic pump actually delivered** | STRUCTURAL **by rule, not by physics** | The per-channel dose verification of F-001. Already declined knowingly by D-014, which is what D-010 asked for. See flag 5: the rule's own column says "Deliberate" and D-014 says "unless something changes", which is current language sitting under a structural label |
| 4 | G-05 | **No level sensors on the nutrient jugs.** Remaining volume is arithmetic | STRUCTURAL, frozen owner rule | Jug floats. Explicitly declined ("Do not add jug floats") |
| 5 | G-07, G-08, G-13 | A leak, an E-stop or a lost interlock **drops everything independent of the Pi.** Safety is not in software | STRUCTURAL, frozen owner rule *(prohibition)* | Nothing. It buys hardware rather than declining it |
| 6 | G-09 as amended by D-031 | The permissive removes **motor supply from every driver at once** and does **not** remove the logic supply | STRUCTURAL, frozen rule as amended | A second switched supply to both pump boxes. D-031 gives three reasons and D-070 records that reason 2 is now a different question, so the decline is on file with its own reopening condition |
| 7 | G-16, G-16a | **No automatic re-dose, ever.** No retry, no threshold, no resume button, **no crash exemption** | STRUCTURAL, frozen rule *(prohibition)* | A whole class of software. Correctly declined, and D-017 records that the rule is what makes every settle-window timing bug produce a false stop instead of a silent overdose. G-16a's demand that the corrective path be "structurally incapable" is a **requirement not yet satisfied by anything**: the UI is HELD by the owner, so nothing in the tree yet delivers it |
| 8 | G-17, G-18, D-018, D-020 | A jug is refilled with the same product **forever** or retired; the tube is **never** moved between channels | STRUCTURAL, frozen rule *(prohibition)* | The keyed coupling. D-019 holds rather than declines it, and names the reason (a bad seal on a suction line draws air rather than dripping). Correctly held, not closed |
| 9 | G-19 | **No progress bar on an interrupted dose and no delivered-fraction percentage anywhere** | STRUCTURAL, frozen rule *(prohibition)* | A UI feature. Declined for a stated reason. Nothing |
| 10 | G-21, D-032 | **Software has no per-driver disable, permanently, and never will.** The drop handler abstains rather than acts, permanently | STRUCTURAL **by frozen rule G-21**, which only the owner can unfreeze | Wiring EN, which PUMP-BOXES argued for and D-032 overruled on F-015. The cost is recorded rather than argued away, and C-06 still records both energised and de-energised numbers, so **the measurement survives the decline.** D-074 carves out the only software-reachable action on a driver and grades it "currently", which is the right shape |
| 11 | G-23, G-31, D-068 | A minimum switching load **belongs to a contact, not to a circuit**; the published V/mA pair **cannot be a legal operating point** | STRUCTURAL, arithmetic against a published figure | Nothing. It forced independent sizing rather than a carried figure |
| 12 | G-25, D-038 | A circulation **verification failure may not** drop the pump in hardware | STRUCTURAL, frozen rule *(prohibition)* | Nothing. D-038's reason is that a hardware drop is silent, and the same entry creates S-20 as the route that keeps the judgement in software |
| 13 | G-26, D-052 | The Pi **does not command** the transfer pump, the circulation pump or the chiller. It commands a permissive that gates them | STRUCTURAL for the **DRIVES** half, frozen rule | The F-003 exercise run's command path. D-091 grades the consequence correctly. **D-101 has already recorded that G-26 says nothing about what the Pi READS**, so this row is structural only as far as its own words go |
| 14 | G-28, D-065, D-073, D-082 | Relay type is **irreversible once bought**; a gold relay used as a power envelope has its gold consumed and **reverts**, so you pay for a property and destroy it | STRUCTURAL, rule plus the consumption mechanism recorded in D-073 | It stopped the order pending two lookups (D-065), which is a deferral not a decline, and then drove a purchase. Correct use of a stop |
| 15 | G-29, D-061 | **In a random-lay bundle you cannot guarantee which core ends up against which** | STRUCTURAL, property of random lay | Nothing. It bought pairing rather than declining it |
| 16 | G-30, D-067, D-072 | **No contact material and no burden value addresses** the debris path, and **a sealed or wash-tight relay does not solve it** - the debris is generated inside the shared volume | STRUCTURAL given the shared-volume premise D-067 records. See "could not settle" item 1 | **This is the only claim in the file whose being wrong costs money SPENT rather than capability lost.** It declined the contact-material remedy and the sealed-relay option and bought duty-split relays instead (D-082). If it is wrong the loss is relays and sockets, and spares are useful. **It forecloses nothing, so it fails the retroactive test in the safe direction** |
| 17 | G-32, D-083 | **A swap present at commissioning is baked into the reference and confirms itself forever** | STRUCTURAL **within S-16** - the reference is C-03's measured step, so a swap present when C-03 runs is in the reference | Nothing, and arguably negative: the claim is the argument FOR C-09, which is free, first in the order (D-022) and acts before C-03. A reader who takes it as an argument for giving up on labelling has read it backwards |
| 18 | D-011, S-16 constraint 1 | **pH up and pH down cannot be attributed at the same time.** The movements cancel and pH shows the net | STRUCTURAL, one probe reading a net | Nothing. The mitigation taken (a batch firing both is a fault condition that must not read as passing) is free |
| 19 | D-017 | On the two pH channels **the excess leaves through V3 and is gone. The tank and the books diverge in a direction nobody can ever see** | STRUCTURAL for the **books**, under G-04, G-05 and D-001's scope boundary | Nothing is declined. But the words are stronger than the tree supports for the **tank**: S-15 reads a net EC rise and C-04 measures the step, so a nutrient overdose is not invisible to the tank, only to the books. Worth one line rather than a flag, because nothing is bought or measured differently either way |
| 20 | D-017 | With G-16 in place a timing error **cannot produce a silent overdose**, only a false stop | STRUCTURAL, follows from the frozen rule | Nothing. It is the reason to freeze the rule before the code, and it is stated as such |
| 21 | D-024 | The old S-15 wording defined **a window in which its own evidence cannot exist** | STRUCTURAL, the check is delayed by construction | Nothing. It corrected a frozen row rather than declining anything |
| 22 | D-042, T-016 | **Software cannot make a severed cable safe. Contact selection can** | STRUCTURAL, physics of a two-state loop | Nothing. It bought the normally-closed contact |
| 23 | D-043, D-055, F-033, F-035 | **No resistor at the driver end can close both of G-22's questions on DIR.** Severed and shorted define opposite levels, so exactly one of the two gives the backwards head | STRUCTURAL for a single-ended pull at one end | Nothing directly. But see flag 2: D-061 claims this limit was **dissolved**, and D-096 reversed that without annotating D-061 |
| 24 | D-058 | **K-DRY cannot fold into K-PERM** (T-017's deadlock) and **K-PERM cannot fold into anything** because it is the only thing RESET re-arms. K-CIRC is deleted | STRUCTURAL, the deadlock plus the reset topology | It cut the definite additional relay count to zero. Then contact duty moved the constraint and the order grew anyway, so nothing was lost by it |
| 25 | D-060 | A latched dry-run trip stops circulation until a human presses RESET and **the Pi cannot restart it.** It can log and alert but cannot recover | STRUCTURAL under G-26's drives half | Nothing. It is made visible rather than discovered, and the entry says so |
| 26 | D-061 | On the driver terminal block DIR's neighbours are fixed by the board: **nothing needs doing there and nothing can be done - the order is the board's** | STRUCTURAL, a bought board's terminal order | Nothing. It is good news correctly reported as good news |
| 27 | D-070, D-076, D-097 | **P-09 cannot be closed from documentation.** The datasheet neither allows, forbids, sequences nor characterises the state, and **UART does not rescue it** because logic is sourced from VS | STRUCTURAL relative to that datasheet, grounded in the owner's lookup recorded in parts.md. **MODEL**: D-070 names both exits (measure it, or remove the state) rather than one | Nothing declined - it **created** a commissioning row (C-18) rather than removing one. This is the model for how a documentary absence should read |
| 28 | D-083 | **A magnitude-only pH check is a duplicate of S-15 wearing S-16's name** and attributes nothing | STRUCTURAL, from what the check is for | Nothing. It bought direction-awareness before any code existed |
| 29 | D-083 | The signed check **generalises nowhere else**: for the six nutrient channels EC moves the same way for all of them and a crossed pair still confirms itself | STRUCTURAL, one EC reading over one stream, given that no per-channel sensor exists | The per-channel sensor, already declined by D-010 and D-014. Nothing new |
| 30 | D-083 | A wrong-direction dose is already partly downstream of V3, **unmeasurable and irreversible** | STRUCTURAL, D-001's scope boundary plus G-04 | Nothing. It is the argument for the loud stop, not against a remedy |
| 31 | D-092 | Five upward-facing penetrations and unsealed cord caps mean **the assembly's rating is set by its worst penetration regardless of what is fitted above** | STRUCTURAL, physics of an enclosure | Gasketed devices, which D-047 had routed to MAIN-PANEL as possibly changing the parts. The substitute remedy (shed, do not seal) addresses the same hazard, so the decline is sound. **D-047 is not annotated as answered**, which is D-051's own shape |
| 32 | D-098 | The two pins D-098 names as held strongly high **cannot be used for anything whose safe power-on state is low, and that is a hard exclusion, not a preference** | STRUCTURAL by the design rule in the same entry (every pin whose power-on level matters gets an external pull) | Two pins on the S-12 map. Whether that binds depends on the pin budget, which is OPEN and in a file I did not read. **D-098 itself flags that the underlying figure's provenance is forum statements, the weakest of anything load-bearing in the tree**, which is the right way to carry it |
| 33 | D-099 | The colour lives on the marker and **nothing is permitted to compute from it** | STRUCTURAL, frozen rule *(prohibition)* | Nothing |
| 34 | D-022, D-102, S-19 | A crossed pair **confirms itself and passes every check**; after C-01 runs the wrong number **is indistinguishable from data** and G-05 decrements against it forever | STRUCTURAL under G-04, G-05 and S-19. **MODEL**: it produced a gate with a deadline rather than a shrug | Nothing declined. It promoted C-09 to first and attached a deadline to F-075. This is the cost column being used correctly by BOSS |
| 35 | D-030 | An apparent weld **latches on a single sample and is never cleared**, and **software may not lengthen the filter** to stop nuisance trips | STRUCTURAL, frozen discipline *(prohibition)* | Nothing. The guard names the fix (at the contact) rather than only forbidding the workaround |
| 36 | D-034, G-20 | A truncated calibration recorded as complete corrupts the figure every dose divides by, and **G-04 guarantees nothing notices** | STRUCTURAL under G-04 | Nothing. It bought a free recording requirement |
| 37 | D-082, G-28 | A swapped relay pair is **a defect that passes every check** | STRUCTURAL - nothing in service measures contact material | Nothing. It bought a labelling requirement, sharpened to apply at delivery |

## CURRENT

Every row here names what would change it. Where the entry already names it, the row
is marked **MODEL**.

| # | Where | The claim | Grade | What would change it | Cost when wrong |
|---|---|---|---|---|---|
| 38 | D-007, S-13 | **There is no flow signal into the Pi.** The flow cell is a fitting, not an instrument. S-13 is closed **as a signal** | CURRENT | S-13's own row says the reason is that **"Nobody has ever specified a sensor in it"** - an absence of a proposal, not a rule. G-04 bans meters on the **dosing lines**; nothing I read bans an element in the circulation loop. S-05's flow-proving fork and S-20 are the route already on the table | See **flag 1**. This is the same door D-060 prices, seen from the instrument end |
| 39 | D-014 | O-19, a flow meter on every dosing line, is **off the table. Not to be brought back unless something changes** | CURRENT half, correctly conditioned. **MODEL** for the wording | The entry says it: something changing. The structural half is G-04 | Nothing. This is the owner declining knowingly, which is exactly what D-010 asked to be recorded |
| 40 | G-06 | Only one dosing pump turns at a time, mandatory in software. **Holds until a thermal measurement says otherwise** | CURRENT, correctly conditioned in the rule's own reason column. **MODEL** | C-15, the sealed-box temperature rise, which commissioning.md calls "the only thing that could ever relax G-06" | Nothing. The condition is named and the measurement is scheduled |
| 41 | D-016, F-003 | **Nothing verifies anything at rest** | CURRENT | S-05's sense element, and C-12's W-1 transient, which C-12 calls "the only F-003 option that costs nothing and adds nothing". Both are on the table | Nothing today - F-003 is assigned to WATER and MAIN-PANEL by D-016 rather than left in the gap |
| 42 | D-038 | A hardware drop is **SILENT**, and the Pi **still believes the loop is turning** | CURRENT | S-20, which the same entry creates in the next sentence | Nothing. The entry states the problem and creates the fix together |
| 43 | D-060 | On the level fork, **circulation verification is foreclosed permanently** | CURRENT, and the word "permanently" is not supported by the row D-060 cites | See **flag 1**, in full | **The highest cost in this file** |
| 44 | D-061 | **F-033's limit was correct for sixteen conductors in a common jacket and is dissolved by construction** | CURRENT, and now **FALSE** | It has already changed. D-096 item 4 and F-072: severed goes high, shorted to a return-paired neighbour goes low, opposite once more. **D-061 is not annotated** | See **flag 2**. A purchase with a deadline |
| 45 | D-063, D-091, F-045, F-057 | **The exercise run still has no command path.** It cannot happen as designed **until one exists or the design changes** | CURRENT, correctly conditioned. **MODEL** | The entry says it, and D-091 calls it "a closed question with an open consequence, which is a different thing from an open question" | Nothing. This is what the settle-window claim should have looked like |
| 46 | D-064 | **D-027's sample tagging cannot be implemented as written, because there is no chiller state to tag with** | CURRENT | S-18's row names three exits, the first being **a Pi READ of a contact on the chiller contactor, which G-26 permits**; and the owner settling what energises the coil, which D-064 routes as an open question | See **flag 7**. A measurement condition for C-02 and C-08 |
| 47 | D-074 | The Pi **currently** has no recovery action on a driver at all | CURRENT, labelled "currently", with the candidate named in the same entry. **MODEL** | The VCC_IO cycle, recorded as a candidate and deliberately **not built**, with its three objections stated | Nothing. This is the second model entry, alongside D-070 and D-091 |
| 48 | D-075, D-080 | A UART-set microstep factor reverting mid-batch is **invisible by construction** | CURRENT on the **observation** half | G-04 and G-05 make **delivered volume** invisible. They do not make **rotation** invisible. parts.md records INDEX as pulsing once per electrical rotation, unwired, on a board already bought; a revert changes the ratio of commanded steps to INDEX pulses. Landing it is the change | Low. The decision it justifies (pins, never UART) stands on D-075's other reason - a reset restores the same configuration, so pins are idempotent - regardless of how this half grades. Prior audit item 2.8 named the same pin for the same reason |
| 49 | D-083 | **Small trim doses stay below the band and a swap discovered only through them stays invisible** | CURRENT | It compares two numbers **neither of which exists yet**: C-03's measured step and C-08's measured band. Either measurement lands and the claim becomes checkable | Low, but it is T-019's shape inside the entry that generalised T-019: a term refused for want of evidence elsewhere in the same argument, accepted here |
| 50 | D-084 | **The union cannot be computed** because five products are unassigned | CURRENT, correctly conditioned | The owner assigning the products, which D-077 places at C-09 with the jugs physically present | Nothing. Waiting is the right answer and the entry says why |
| 51 | D-084 | A product outside the three duty classes arriving on any channel invalidates the carrier specification, and **NOTHING WILL DETECT THAT AT ASSIGNMENT TIME** | CURRENT | **C-09 is assignment time** (D-077), it is first in the order (D-022), it is free and needs no hardware. One question added to its script detects it | See **flag 4** |
| 52 | D-093 | The datasheet is silent, C-18 is the decision to accept an uncharacterised state once under observation, **and that is the only path** | CURRENT relative to **D-070's own second exit** | D-070 states two exits, not one: measure it, or **remove the state**. D-070 also records that reopening D-031 is "now a different question, because the board's own pulldowns and the chip's internal pull change what those pins do" | Modest. D-093 drops one of the two exits its own source names, three entries later, with no reason given for dropping it. It commits the build to entering a hazardous state without re-stating that the alternative exists |
| 53 | D-097 | DIAG is not a specified detector for VM absent, **and C-18 is now the only route** | **MIXED** - see flag 3 | Split below | See **flag 3** |
| 54 | D-019 | On a suction line a bad seal **does not drip, it draws air**, the head turns, the books decrement and nothing is delivered | CURRENT | O-03 (translucent tubing) and O-04 (jug end in the sightline), both free, both taken in the same entry | Nothing. Problem and fix in one entry |
| 55 | D-085 | The wall-length gap was justified when a swap was **permanently invisible**; the signed check made it a bounded one-dose error. **IF THE SIGNED CHECK IS EVER REMOVED, THIS REOPENS** | CURRENT, correctly conditioned. **MODEL** for naming its own reversal condition | The signed check being removed, or its premises failing at C-03 and C-08 | **This entry declines a physical purchase (wall length) on the strength of a capability claim.** The reopening condition is named, but reopening after the manifold and raceway are built is not free - T-020's shape, since a wall run cannot be un-run. Worth carrying as a known asymmetry, not a defect |
| 56 | D-013, S-17 | **Nobody solves it** / **Do not solve it** (fulvic) | **MIXED** - see flag 6 | Split below | See **flag 6** |

## MIXED - one sentence carrying a structural half and a current half

| # | Where | The claim | The structural half | The current half | Cost |
|---|---|---|---|---|---|
| 57 | D-095 | Three things are **STRUCTURALLY IMPOSSIBLE rather than pending**: settle-window validity, attribution for six of eight channels, any measurement of delivered volume | The first is already superseded by D-101. The second and third are structural **by frozen rule** (G-04, G-05) | D-014's own words for that rule are "not to be brought back **unless something changes**", and the prior audit's item 11.16, banked by D-101, records that the **floor** on delivered volume is current on this build | See **flag 5** |
| 58 | D-049, G-22 as amended | **You can choose which is safe. You cannot make both safe.** No two-state sense line can report three states | True for a **single** two-state line. Information, not opinion | G-27, frozen in the very next entry (D-053), adds a second leg and converts fail-safe into fail-detected, and D-053 says it is **free wherever two legs of one changeover are already bought** | See **flag 8** |
| 59 | D-013, S-17 | Fulvic **moves neither EC nor pH meaningfully**, therefore nobody solves it | The **decision** to accept one unattributed channel is structural: a frozen owner decision, D-013, S-17 closed on it | The **premise** is a physical claim about this build with no measurement named behind it in anything I read | See **flag 6** |
| 60 | D-097 | DIAG is not a specified detector for VM absent, and **C-18 is now the only route** | What a driver does with VM absent is a chip-behaviour question the datasheet does not answer. Only measurement answers it | "The only route to **permissive-drop detection**" is a different claim, and S-08 already gives the Pi a contactor readback under D-029 | See **flag 3** |

---

# FLAGGED, worst first

Eight claims would stop a purchase, a commissioning measurement or a capability.
For each: what specifically would not get bought or built, and whether declining it
makes the claim true retroactively the way D-060 and F-074 describe.

---

## FLAG 1. D-060: "circulation verification is foreclosed permanently"

**The claim.** D-060, verbatim: "flow-proving means a timing element is definite and
circulation verification stays possible; level-based means no timing element and
**circulation verification is foreclosed permanently.**"

**Why this is the worst one in the file.** D-060 is the frozen text that F-074, D-101,
C-23's correction and the prior audit's ruling all cite as the authority that
document 12 was wrong. It is the terminating source in that chain. **Under G-37 that
means nothing above it re-derives it, and under T-023 nobody was ever given an
occasion to test it, because its own content removes the occasion.** The sentence
that corrected the tree's worst impossibility claim contains an ungraded
impossibility claim of its own, in the same breath, about the same door.

**The grade, and what settles it.** S-05's frozen row, which is what D-060 is reading,
says: a level element "senses the supply and **can NEVER subsume circulation
verification**, because it reads healthy through a fouled impeller, an air-locked
volute, a blocked intake and a shut valve. **Choosing a level-based answer here
forecloses the shared solution.**"

The row's word is **the shared solution.** D-060's word is **circulation
verification, permanently.** Those are not the same claim, and the second does not
follow from the first.

- **STRUCTURAL:** a level element cannot subsume circulation verification. That is
  S-05's frozen sentence and it is physics - a supply reading is healthy through four
  named failures.
- **CURRENT:** that circulation verification is foreclosed **permanently**. Nothing
  frozen says the circulation loop's instrumentation question closes when S-05 closes.

**What would change it - three things, all already on the table:**

1. **F-003 is a separate assignment with a separate route.** S-05's own row says
   "S-05 must not be answered before F-003 is", and D-016 assigns F-003 to WATER
   primary with MAIN-PANEL at the other end. **S-05 settles the dry-run element. It
   does not settle whether the loop is ever instrumented.** A flow element added
   later as its own device is a purchase nothing forbids.
2. **C-12's W-1 transient is a free, scheduled witness that does not depend on S-05
   at all.** D-063 consequence 2: "WATER's free witness survives and gets BETTER."
   C-12's row: "It is also the only F-003 option that **costs nothing and adds
   nothing**." It witnesses that the loop started moving after a rest. It is a
   partial verification, not a window-long one, and I state that limit rather than
   overselling it - but a partial capability is not a foreclosed one.
3. **S-20 survives a level-based fork.** S-20 is a second pole of **K-DRY**, and
   K-DRY exists on either fork; circulation is a pole on it under D-058. C-23's
   corrected text says "a read of S-20 through the window is a read of whether the
   pump was **energised** across it" and "the correct statement is that NOTHING
   BUILT TODAY catches it, **and S-20 would**." With a level element that read is
   much weaker - it says the pump was permitted and supply was present, not that the
   loop moved - **but window INVALIDATION survives, and D-060's sentence gives back
   nothing.**

**What would not get bought or built.** The timing element D-060 prices. The flow
element itself. And, further out, the S-20 build, since WATER reads this entry and
S-20's row is blocked on WATER returning the S-05 element.

**Does declining make it true retroactively? YES, and in the strongest form present
in this file.** If WATER answers S-05 level-based on the strength of "foreclosed
permanently", then: the timing element is never bought; nobody prices C-12's witness
as circulation verification, because the decision file says the door is shut; nobody
proposes a separate element later, for the same reason; and the tree records
circulation verification as gone. **There is no step between the decision and the
sentence becoming true that anyone would notice.** That is T-023's mechanism running
on T-023's own cited authority.

**The fix is one word and it is not mine to make.** "Forecloses the shared solution",
which is what S-05's frozen row says, is defensible. "Foreclosed permanently" is not,
and G-36 now requires the grade to be named.

---

## FLAG 2. D-061: "F-033's limit ... is dissolved by construction", reversed and not annotated

**The claim.** D-061: "With DIR paired to its own return, the two G-22 failures stop
being opposite and converge on one state. **F-033's limit was correct for sixteen
conductors in a common jacket and is dissolved by construction.**"

**It has already been reversed, in this same file, and D-061 does not say so.**
D-096 item 4: "**G-29's convergence on DIR is broken again.** Severed goes HIGH,
shorted to a return-paired neighbour goes LOW. **Opposite once more.**" F-072 puts it
in terms: "That convergence is now BROKEN AGAIN ... which is precisely the condition
D-049 and G-22 called unsafe-in-both-directions."

**The asymmetry that makes this a question rather than a note.** The tree annotates
reversals in place when it notices them. D-069's closing sentence was corrected in
place. D-095 carries "SUPERSEDED IN PART 2026-09-03 BY D-101" as its second line.
F-053's row carries its correction. **D-061 carries nothing.** A reader arriving at
D-061 - which is the entry that freezes G-29 and reads as good news throughout - is
told the DIR problem is dissolved, and nothing on that page points forward.

**What would not get bought or built.** This is **the flagged claim with a clock on
it**, and the clock is D-062's gate: links (a) and (b) are settled "**BEFORE the S-10
cable is bought and before any resistor is fitted**". Specifically at risk:

- **D-043's external pull-down at each driver input.** F-072: with DIR floating high,
  the pull-down "is the ONLY thing that defines the level at all, so it is
  load-bearing for the LEVEL and not merely for noise immunity", and it can no longer
  be sized against leakage. A reader of D-061 alone reads it as belt-and-braces.
- **C-21**, the per-driver lift-and-meter check that D-043's pull-downs actually hold
  the driver terminal below its low threshold. C-21's own reason: the pull-downs are
  "a safety component whose failure is silent and self-confirming".
- **The pairing itself in the S-10 cable**, which D-062 records F-030 as saying is
  cheaper before the cable is bought.

**And what sits on the other side of it:** S-10's row calls a severed DIR producing a
head that runs backwards while the books decrement forward **the worst outcome in the
whole fail-safe sweep**, and D-062 records that pairing is an amplifier - it makes
both failures give one level, "which is a win only if that level is safe".

**Does declining make it true retroactively? YES, in T-020's form.** Buy and lay the
S-10 cable on the strength of "dissolved by construction" and a cut cable cannot be
un-cut. The pairing that would restore convergence is precisely the thing that is
cheaper before the cable is bought, so the decline closes the cheap route and leaves
only the expensive one.

**What I am asking for, not doing.** D-061 is annotated the way D-095 was, pointing
forward to D-096 item 4 and F-072. I fix nothing.

---

## FLAG 3. D-097: "C-18 is now the only route" - two claims in one sentence

**The claim.** D-097: "**No agent may build a permissive-drop detection on DIAG on
the strength of the word 'diagnostic'.** C-18 is now the only route, and C-18 already
carries the ruling that running it IS the decision."

**Two readings, and only one of them is structural.**

- **Reading A, what a driver does when VM is absent, and whether DIAG says anything
  about it.** STRUCTURAL relative to the datasheet, and well grounded: parts.md's
  quoted paragraph says the datasheet "does NOT say whether DIAG or INDEX is high, low
  or Hi-Z, does not say whether the pad remains a driven output while the core is held
  in reset, and does not offer DIAG as a VS-present detector." Only measurement
  answers that. C-18 genuinely is the only route.
- **Reading B, detection of a permissive drop at all.** CURRENT, and **partly false
  today.** The sentence it follows is about permissive-drop detection, so this is the
  natural reading. But **the Pi already reads the permissive contactor back**: S-08 is
  closed by D-029, the readback is a pole of the contactor, the sense is inverted, and
  D-030's asymmetric discipline runs on it - a weld latches on a single sample. So the
  Pi is not blind to a permissive drop. **It is blind to VM at the driver terminal**,
  which is a different and narrower thing. And no frozen row I read forbids a VM sense
  landed at the Pi; the prior audit's item 2.23 says the same about the same gap.

**This is exactly the shape D-101 item 2 caught in document 12's section 6.4** - a
structural half and a current half run together in one sentence, where the structural
half is real and does the work of licensing the other. It is now on file in
decisions.md, four entries after D-101 recorded it as a defect.

**What would not get bought or built.** A VM sense at the driver end - conductors and
a Pi input, no new instrument - never gets priced, because the sentence says there is
only one route. And in the other direction it **commits the build to C-18**, which
D-070 and D-093 both record as the decision to deliberately enter an uncharacterised
state, once, under observation. **The cost here runs both ways: it forecloses an
unpriced alternative and it commits to a hazard as though there were no alternative
to price.**

**Does declining make it true retroactively? NO.** Nothing is consumed. The VM sense
stays available and C-18 stays runnable. **Expensive, but recoverable** - which is the
distinction the retroactive test exists to draw.

**The fix under G-36 is to split the sentence**, and the split is CONTROL-SOFTWARE's
and DISPLAY-BOX's to make, not mine.

---

## FLAG 4. D-084: "NOTHING WILL DETECT THAT AT ASSIGNMENT TIME"

**The claim.** D-084, quoting the owner: "a product outside those three classes
arriving on any channel invalidates the carrier specification, and **NOTHING WILL
DETECT THAT AT ASSIGNMENT TIME.**"

**Grade: CURRENT.** Assignment time is a scheduled, named, free event in this tree.
D-077: "**C-09 is where a token is bound to a product, with the jugs physically
present.**" D-022 puts C-09 first in the commissioning order. C-09's own row: "Free,
needs no hardware, and with translucent tubing needs no disassembly", and it is
already a re-measure trigger for any rewiring or renumbering.

**What would change it.** One question added to C-09's script: is this product acid,
base, or generic nutrient concentrate - and if it is none of the three, the carrier
specification is invalid and D-084's residual has fired. The operator has the jug in
hand at that moment by construction. **No hardware, no purchase, no new row - a line
in a row that already exists and already runs first.**

**What would not get bought or built.** That line. And with it, the only moment at
which the residual D-084 explicitly accepts could ever be caught.

**Does declining make it true retroactively? YES.** The residual is accepted, the
check is never added because the entry says nothing can detect it, the fourth-class
product arrives at a C-09 that does not ask, and the carrier specification is invalid
with nothing having recorded the moment it became so. **The claim's own content
removes the occasion to add the check that would falsify it** - T-023 in one sentence.

**One caution against my own finding.** D-084 accepts the residual deliberately and
in the owner's words, which is the correct handling of a residual under this tree's
rules. I am not arguing the residual should be closed. **I am reporting that
"nothing will detect that" is stated where "nothing detects that today, and the free
place to detect it is C-09" is what the tree supports.**

---

## FLAG 5. D-095's two surviving "STRUCTURALLY IMPOSSIBLE" items

**The claim.** D-095 banks three things as "**STRUCTURALLY IMPOSSIBLE rather than
pending, so nobody reads it later as a gap waiting to close**": settle-window
validity, attribution for six of the eight channels, and **any measurement of
delivered volume**. D-101 superseded the first. **The other two still stand under that
heading, and the heading is the whole point of the sentence.**

**Grade: MIXED, and the mix is not marked.**

- Both surviving items are structural **by frozen rule** - G-04 and G-05 - and **not
  by physics.** The prior audit made the same call at its item 2.7. D-014's own
  wording for that rule is "**not to be brought back unless something changes**",
  which is the language G-36 reserves for a current claim.
- More sharply: **the FLOOR on how wrong the book can be is current on this build,
  and D-101 has already banked the sentence that says so.** The prior audit's item
  11.16, which D-101 accepts and names as the model, reads: "Nothing on **this build**
  can narrow it. If a per-driver indication that requires actual commutation ever
  lands at the Pi it becomes the only candidate, and even then the book decrements the
  ceiling." parts.md's printed pin list carries **INDEX**, unwired, on a board already
  bought.

So decisions.md today contains, in D-095, a stronger claim than D-101 banks four
entries later, under a heading whose stated purpose is to stop readers treating it as
a gap.

**What would not get bought or built.** Landing INDEX at the Pi: conductors, a Pi
input, an S-12 row, a software counter. No instrument, no new part. And the
commissioning row that would use it, which nobody has proposed - because D-095 says
the category is closed.

**Does declining make it true retroactively? WEAKLY, and I say weakly deliberately.**
The pin stays on the board and the conductor can be run at any time. Nothing is
consumed by declining. **This is an expensive wrong claim that is not a
self-fulfilling one**, which is a different and lesser problem than flags 1, 2, 4 and
6 - and drawing that line is what the retroactive test is for.

**What I am not saying.** I am not saying INDEX gives a measurement of delivered
volume. It does not - parts.md records what it pulses on, and rotations are not
millilitres. **I am saying the two are different claims and D-095 states the stronger
one.**

---

## FLAG 6. D-013 and S-17: "Nobody solves it" resting on an unmeasured premise

**The claim.** D-013: "**Fulvic stays unattributed.** It moves neither EC nor pH
meaningfully. One unattributed channel out of eight, recorded, is acceptable.
**Nobody solves it.**" S-17's row closes on the same words and adds: "**Do not solve
it.**"

**Grade: MIXED, and the halves have very different standing.**

- **The DECISION is STRUCTURAL.** D-013 is an owner decision, S-17 is closed on it,
  and one unattributed channel out of eight is accepted with the count stated. That is
  the tree working correctly.
- **The PREMISE is a physical claim about this build with no measurement named behind
  it in anything I read.** "It moves neither EC nor pH meaningfully" is a statement
  about a product on a channel, on a loop, against a band. I read D-013, S-17's row,
  C-03, C-04, C-08 and F-001. **None of them names a measurement behind it.** Under
  agents.md rule 8 I say what I read to say that, and I name the file I did not read
  that may carry it: `subsystems/dosing-verification-options.md`, which D-010 records
  as holding the returned options.

**What would not get measured.** **C-04's scope is "EC step per single dose, per
EC-moving channel."** Fulvic is excluded from C-04 by the same assumption the claim
rests on. So the measurement that would test the premise is the one the premise
removes from the schedule.

**Does declining make it true retroactively? YES, in its epistemic form.** If C-04
never includes fulvic, nobody ever learns whether it moves EC on this build against
C-08's measured band, so the claim can never be falsified. It is not a purchase being
foreclosed - it is a **column in a measurement that is already scheduled, already
being run on seven other channels, by the same person, on the same trace.** The cost
of testing it is close to zero and the cost of not testing it is one channel of
attribution out of eight, forever.

**What I am not claiming.** I am not claiming fulvic moves EC. I have no measurement
and I will not estimate one. **I am reporting that "nobody solves it" and "do not
solve it" are written where the tree's own evidence for the premise is an assertion,
and that the cheapest possible test of it was scheduled and then scoped out by the
assertion itself.**

---

## FLAG 7. D-064: "the sample tagging cannot be implemented as written"

**The claim.** D-064: "Until it is settled, S-18 stays OPEN and **D-027's sample
tagging cannot be implemented as written, because there is no chiller state to tag
with.**"

**Grade: CURRENT**, and the entry's own qualifier "as written" is doing real work
that a hurried reader will drop.

**What would change it.** S-18's row names three exits, none of them BOSS's: "the Pi
**READS** a contact on the chiller contactor, **which G-26 permits since it restricts
what the Pi drives and not what it reads**"; or accept untagged samples; or the Pi
drives the chiller, which contradicts G-26. D-101 item 2 has since made the
drives-versus-reads boundary an explicit ruling. Plus D-064's own open question: what
energises the coil, with three candidates named and none chosen.

**What would not get built or measured.** commissioning.md's closing section is
categorical: C-02 and C-08 "are measured in normal service **with the commanded
chiller state logged alongside each reading**", and "a measurement whose conditions
are unrecorded is not a measurement". **Two commissioning rows depend on a condition
this entry says cannot be implemented.**

**The bound on the cost, stated so this is not over-flagged.** C-02 and C-08 are
measured **by the owner**, by hand, with a stopwatch and a trace. **A person can
record chiller state by looking at it.** What "cannot be implemented as written" is
D-027's *automatic* tagging by the Pi. The measurement is not blocked; the software
feature is. A reader who drops "as written" concludes the measurements are blocked,
which they are not.

**Does declining make it true retroactively? NO.** C-02 and C-08 are re-measurable -
commissioning.md's own re-measure trigger table exists for exactly that. Data taken
without the tag is worth less, not worthless, and it can be retaken. **Expensive,
recoverable.**

---

## FLAG 8. D-049 and G-22: "You cannot make both safe"

**The claim.** D-049: "for an optocoupler sense loop severed and
shorted-to-an-energised-neighbour fail in opposite directions, always ... **You can
choose which is safe. You cannot make both safe.** No two-state sense line can report
three states."

**Grade: MIXED.** The information-theoretic half is unarguable: a line with two states
cannot report three. **But the scope is a SINGLE line, and the very next decision
frozen the same day adds a second one.** D-053 freezes G-27: "**A COMPLEMENTARY PAIR
IS A FAIL-DETECT** ... both legs at the same potential, on the same cable. Then a
severed conductor makes them contradict, and **any state where both agree is a broken
sense path**." D-053 adds: "**Free wherever two legs of one changeover are already
bought.**"

So the correct statement is: **a single two-state line cannot make both failures safe.
A signal can, by being carried on two.**

**What would not get built.** D-073's envelope list gives K-DRY-Q "the seal-in and
**the G-27 complementary pair to the Pi**", so S-20 is planned with one. **S-03's row,
which I read in full, describes a single series branch through an optocoupler LED and
does not mention a complementary pair** - and S-03 is the fill-in-progress contact
that D-042 makes the interlock against dosing during a fill, and F-011 stands against
it unresolved per D-029's closing sentence. The cost of adding one is a pole and a
conductor on a changeover that is already bought.

**The measurement it touches.** C-19, the fail-direction test - "**G-22 was a design
claim with NO CHECK BEHIND IT**" - disconnects each sense conductor in turn and
records what the Pi reports. A complementary pair changes what that row can conclude,
from "the chosen direction happened" to "a broken path is distinguishable from a real
state".

**Does declining make it true retroactively? NO.** A second leg can be added later,
though D-073's envelope split and the socket are the practical constraint and G-28
makes the relay type irreversible once bought, so the window is not open forever.
**Expensive, mostly recoverable, with a soft deadline at the order.**

**Stated as a question, not an assertion.** I read S-03's row, D-042, D-035, D-029 and
D-073's envelope list. **I did not read `subsystems/display-box.md`,
`display-box-sweep.md`, `main-panel.md`, `main-panel-poles.md` or `main-panel-buy.md`,
any of which may already carry a pair on S-03.** I am asking whether it does. I am not
saying it does not.

---

# What I could NOT settle from the tree

**1. Whether G-30's "no contact material and no burden value addresses it" is physics
or a reading of one part.** D-067 states the debris mechanism as given: all four poles
share one volume, the plug-in is dust protected and not wash tight, a power break
throws silver vapour, oxide and carbon onto the quiet pole. **I read D-067, D-072,
G-30's row and D-073.** None of them names the datasheet page or the measurement the
shared-volume premise comes from, and I did not open a datasheet. If the premise
holds, the conclusion is structural. **I graded it structural on the premise as
recorded, and I am naming the premise rather than the conclusion as the thing nobody
sourced.** The cost of being wrong here is money already committed, not capability, so
this is the lowest-urgency of the six.

**2. Whether fulvic moves EC on this build.** Flag 6. No measurement is named in
D-013, S-17, C-03, C-04, C-08 or F-001. `subsystems/dosing-verification-options.md`
may carry one and I did not read it. **I will not estimate it and no agent should.**
The requirement is: fulvic's EC step per single dose against C-08's measured band.
Search term for the owner: the product's conductivity contribution at dose
concentration, from the supplier's data.

**3. Whether S-03 carries a G-27 complementary pair.** Flag 8. S-03's row describes a
single series branch. Five subsystem files I did not read could settle it in a line.

**4. Whether D-098's exclusion of two Pi pins actually binds.** It binds only if the
pin budget is tight, and S-12 is OPEN. `subsystems/display-box.md` and
`display-box-sweep.md` hold the sweep. **D-098 itself flags that the figure behind the
exclusion is forum-sourced, which is the correct handling, and I am not questioning
the exclusion - only whether it costs anything.**

**5. What a level-based S-20 would actually deliver.** Flag 1 establishes that
D-060's "permanently" is not supported by S-05's row. **It does not establish what the
level fork leaves you with.** I read S-20's row, D-038, D-058 and C-23's corrected
text, all of which describe K-DRY as the relay and circulation as a pole on it on
either fork, and none of which says S-20 dies with a level answer. But S-20 is OPEN
and blocked on WATER returning the S-05 element, `subsystems/water-s18-f003.md` and
`main-panel-poles.md` may bear on it, and I read neither. **What I can say is that
"forecloses the shared solution" and "foreclosed permanently" are different claims and
only the first is on file as frozen.**

**6. Whether landing INDEX would narrow the delivered-volume floor, and what it would
cost.** Flag 5. parts.md records what INDEX pulses on and that it is unwired. **Nothing
I read prices the conductor, the Pi input, the S-12 row or the software.** The prior
audit's item 11.16 is the record and I am not extending it. This is a requirement and
a routing question for DISPLAY-BOX and CONTROL-SOFTWARE, not a conclusion.

---

# A note on the shape of this file, offered because it runs the other way

**Seven of the current and mixed claims are graded correctly in place**, by the entry
that makes them, before G-36 existed to require it: D-014's "unless something
changes"; G-06's "holds until a thermal measurement says otherwise" with C-15 named;
D-070's two exits rather than one; D-074's "currently" with the candidate named;
D-085's "IF THE SIGNED CHECK IS EVER REMOVED, THIS REOPENS"; D-091's "a closed
question with an open consequence, which is a different thing from an open question";
and D-102, which turned an impossibility into a gate with a deadline instead of a
shrug.

That matters for the same reason the prior audit recorded items 11.16 and 11.12:
**it establishes the standard as something this tree already does, rather than
something an audit is asking it to start doing.** The eight flagged claims are
departures from a practice that is visibly present in the same file.

And one asymmetry worth carrying: **of the eight flagged, exactly four make
themselves true if declined** - flags 1, 2, 4 and 6. The other four are expensive and
recoverable. **The tree has no marking that distinguishes those two kinds**, and
G-36 as frozen does not require one. That is an observation, not a proposal.
