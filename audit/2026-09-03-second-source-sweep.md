# AUDIT: the second-source sweep, G-37's shape across the whole tree

> **RUN NUMBER NOT CLAIMED, AND BOSS SHOULD ASSIGN ONE.** While this sweep was
> running, `audit/2026-09-03-decisions-impossibility-grading.md` landed in the
> same directory, timestamped minutes before this file, and **it calls itself
> "AUDIT run 4".** This sweep was invoked separately, under D-102, and would also
> have been the fourth. **Two audit returns in one namespace both numbered by
> their authors is F-026's defect exactly, T-013's shape: a thing named by an
> index in a namespace that is not its own.** I have removed the number from this
> file rather than pick one, because the numbering is BOSS's. I did not read that
> file and nothing here rests on it.

Returned 2026-09-03, under D-102's routing: BOSS asked whether the F-074 shape
appears anywhere else, and instructed that the answer come from looking rather
than from recall. Questions and classifications only. **AUDIT changed nothing and
edited no file but this one.**

Scope difference from run 3, stated so the two are not confused. Run 3 compared
ONE document against the frozen rows. **This run compares FILES AGAINST EACH
OTHER on provenance, everywhere in the tree, and asks one question of every
cross-file attribution: does the cited text originate the claim, or only repeat
it.**

---

## What I read, in full

Root: `agents.md`, `interface-table.md`, `decisions.md` (all 1685 lines),
`findings.md` (all 338), `traps.md` (all 455), `commissioning.md` (all 90),
`parts.md` (all 620), `channel-token.md` (all 214), `channel-register.md` (all
97), `software-spec.md` (all 1154), `order.md` (all 121),
`colour-map-proposal.md` (all 93).

`subsystems/`, all nineteen files, complete: `control-software.md`,
`control-software-f004.md`, `control-software-p09.md`, `display-box.md`,
`display-box-sweep.md`, `display-box-short-column.md`, `dosing.md`,
`dosing-f002-proposal.md`, `dosing-f004-wet-side.md`,
`dosing-verification-options.md`, `interconnect.md`, `main-panel.md`,
`main-panel-buy.md`, `main-panel-poles.md`, `pump-boxes.md`,
`pump-boxes-p09.md`, `pump-boxes-pulldowns.md`, `water.md`,
`water-s18-f003.md`.

`audit/`: `2026-08-30-channel-token.md` (all 148), `2026-08-30-displaybox-vs-mainpanel.md`
(all 159), `2026-09-03-doc12-vs-frozen.md` (headings, the Part 1 table, Part 2
entire, and the closing sections; **I did not read its 16 expanded entries line
by line**, only their titles and the four I cite below).

That is every markdown file in the working directory, `subsystems/` and
`audit/`. Thirty-three files.

## What I did NOT read, named so nothing here rests on it

**No datasheet, no schematic, no photograph, no board and no code.** Every
external fact in this report is a fact as the tree records it. Where I say a
claim is false I mean another file in this tree contradicts it, never that I
checked the world.

**I state no part number and no specification.** Every figure named below is
attributed to the file I read it in.

I did not read the git history. A claim's date is the date the file gives it.

---

## The method as actually executed

1. **I built the graph by grepping for attributions, not by reading for the
   phrase.** For each of the load-bearing identifiers - G-nn, D-nnn, F-nnn, C-nn,
   T-nnn, the S-/P-/F-/CBL-/M- rows, and the filenames `parts.md`,
   `channel-token.md`, `channel-register.md`, `software-spec.md`,
   `commissioning.md` and each `subsystems/` file - I listed every place in
   another file that cites it. Same-file citations were dropped: a file citing
   its own IDs is not this shape.

2. **For each cross-file citation I opened the cited text and asked whether it
   originates the claim.** An origin is a measurement, a datasheet the owner
   pasted, a physical fact, an owner's ruling, or a decision that is itself the
   origin of what it decides. A decision that RECORDS a claim it got from
   somewhere else is not an origin, and neither is a frozen row that describes
   something nobody established.

3. **I followed each chain until it reached an origin or looped.** Where a chain
   terminated in a file that had itself been corrected, I checked whether the
   correction is visible from the citing end. **That is where most of the hits
   are: the correction exists, and it exists only at the far end of a link
   nobody following the chain would take.**

4. **Separately I looked for the same claim stated in two or more files with no
   citation between them**, by grepping distinctive phrasings and the key
   figures, then comparing wording. Verbatim agreement with no link is the tell.

5. **I classified the file before choosing the question, per T-021.** A frozen
   row, a decision, a finding row, a subsystem return and a specification fail
   differently. Subsystem returns are the highest-yield population in this tree
   and they are the population run 3 did not read: **they are dated returns that
   stay on disk, they are cited by name from the load-bearing files, and D-051
   and F-032 already record that a return keeps arguing for something after it
   has been decided.** Every CONFIRMED hit below except one lives in that
   population.

**What the method cost me.** It finds a chain that terminates wrongly. It does
not find a claim nobody ever cited, and it does not find a claim whose only
source is a conversation. Where a chain terminates in "the owner said so" I
recorded it as an origin and stopped, because I cannot check the owner.

---

## The citation graph: every cross-file chain I followed

42 chains. "Terminus" is where the chain actually stops, not where it appears to
stop.

| # | Citing file and place | Claim carried | Cited as authority | Terminus reached | Verdict |
|---|---|---|---|---|---|
| 1 | `commissioning.md` C-23, as first written | Window validity is unconfirmable, "the Pi neither commands nor observes" | `software-spec.md` | `software-spec.md`, banked into D-095, cited back by C-23 | **LOOP.** The known instance, F-074. C-23's text is corrected in place; the loop is recorded, not live |
| 2 | `software-spec.md` 2.17, 11.6, section 12 | Same claim, called STRUCTURAL | F-001 limit 1, F-003, D-007, D-091, G-26 | F-001 limit 1 and F-003 are about the pump AT REST; G-26 is about what the Pi DRIVES | **NON-ORIGIN.** F-074, still unfixed in the document |
| 3 | `subsystems/control-software-f004.md` line 45 | "The Pi commands the circulation relay, so it can require circulation commanded on" | **S-09** | Interface S-09 as first written, which D-052 records came from the owner's project description and "was loose" | **NON-ORIGIN.** F-070 covers this one instance |
| 4 | `subsystems/control-software-f004.md` line 218 | "The software commands the circulation relay so it knows what it asked for" | nothing | same withdrawn premise | **NON-ORIGIN, AND UNFLAGGED.** Not covered by F-070 |
| 5 | `subsystems/control-software-p09.md` step 6 | "Commanded circulation and chiller states alongside, per D-027" | **D-027** | D-027's mechanism, "the Pi commands the contactor, so it knows", withdrawn by G-26 and D-052 | **NON-ORIGIN, AND UNFLAGGED** |
| 6 | `subsystems/dosing-f004-wet-side.md` line 34 | "The timer must be gated on the manifold pump being commanded on" | F-003, for the weakness only; the capability is uncited | same withdrawn premise | **NON-ORIGIN, AND UNFLAGGED.** This file is cited live by C-02 and by N-4 |
| 7 | `subsystems/control-software.md` "Settled" bullet | "The Pi commands relays for the fill solenoid, transfer pump, manifold pump and chiller contactor" | nothing | the project description D-052 corrected | **NON-ORIGIN, AND UNFLAGGED** |
| 8 | `subsystems/water-s18-f003.md` F-003 half one | "The manifold pump is commanded on for a short exercise run ... CONTROL-SOFTWARE schedules it, MAIN-PANEL's relay switches it" | nothing | same | **NON-ORIGIN.** Consequence flagged by F-045, F-057 and D-091; the file itself is unannotated |
| 9 | `subsystems/main-panel-poles.md` state 4 and the F-003 ruling | K-CIRC is an independently commanded state, "commanded by the Pi", and the exercise needs it to stay its own relay | nothing | same, plus K-CIRC which D-058 deleted | **NON-ORIGIN.** Unannotated |
| 10 | `subsystems/display-box-sweep.md` sweep row | "S-09, four relay coil drives" | S-09 | same | **NON-ORIGIN.** Unannotated |
| 11 | `subsystems/display-box.md` scope | "relay coil drives" (plural) | nothing | same | **NON-ORIGIN.** S-09's own row says DISPLAY-BOX "must be told" and it has not been |
| 12 | `subsystems/display-box-short-column.md`, "One adjacency stated as fact rather than guess" | VDD and VM are two positions apart on one screw terminal block, the closest approach in the build | **`parts.md`, the printed pin list** | `parts.md`'s flat list, which F-058 establishes was a list of NAMES read as an ORDER and the order read as ADJACENCY | **NON-ORIGIN.** `parts.md` never stated an adjacency |
| 13 | `findings.md` F-031 | Same claim | `parts.md` pin list, P-09, F-020 | same | **NON-ORIGIN.** F-031's row is unannotated |
| 14 | `decisions.md` D-061, segment 5 | DIR's neighbours are STEP and EN, "neither is an energised rail"; VDD and VM at the far end of the part | PUMP-BOXES' segment-5 answer | same flat list | **NON-ORIGIN.** F-058 calls this conclusion "WRONG IN THE UNSAFE DIRECTION". D-061 is unannotated |
| 15 | `colour-map-proposal.md` constraint 1 | "CH5 and CH6 ... They are the pH pair" | F-063 | F-063 states it flatly and cites nothing for the identification | **NON-ORIGIN** |
| 16 | `findings.md` F-063 | "THE TWO pH CHANNELS ARE CH5 AND CH6. They are adjacent" | `channel-token.md`, S-16 (for the RULE) | The rule traces cleanly to S-16. **The identification traces to `channel-register.md`, which calls it an inference by elimination** | **SPLIT.** Rule clean, identification non-origin |
| 17 | `channel-register.md` "What the software does know" | "The two 1000 mL channels are the pH adjusters" (flat) | D-077 | D-077 to the controller config for the count and CH5's role, **and to the Jug column for the pairing** - which the same file's own header calls a SEED | **NON-ORIGIN.** T-018: a seed is not evidence about the world |
| 18 | `decisions.md` D-099 and its colour table | CH5 and CH6 bound blue and yellow because they are the pH pair | `colour-map-proposal.md` | chain 15 to chain 17 | **NON-ORIGIN, AND FROZEN ON IT** |
| 19 | `decisions.md` D-085 | "the CH5 and CH6 gap" | F-063, F-064 | F-064 is clean and volume-independent per D-088. The pair identification is chain 16 | **SPLIT** |
| 20 | `decisions.md` D-083 closing note | "CH5-versus-CH6 is the ONE confusion where direction is a discriminator" | F-064 | chain 16 | **SPLIT** |
| 21 | `software-spec.md` 3.2 | The register holds "one role marking and one inference that is marked as an inference" | `channel-register.md` | the register's own marking | **CLEAN.** The one downstream file that carries the qualification |
| 22 | `subsystems/pump-boxes.md` line 45 | "Vref pot set with a meter before power" | `parts.md` ("read parts.md before anything else") | `parts.md`'s Vref line, since corrected there as UNEXECUTABLE per F-061 | **STALE COPY of a corrected origin** |
| 23 | `commissioning.md` C-22 | The Vref hazard | F-061 | F-061 to the Adafruit schematic and `parts.md` | **CLEAN** |
| 24 | `commissioning.md` C-02, blocked-on column | "chiller in NORMAL SERVICE, its state recorded against every sample, per D-027" | **D-027** | D-027's mechanism, withdrawn by G-26 and D-052; D-064 says the tagging "cannot be implemented as written" | **NON-ORIGIN** |
| 25 | `commissioning.md` C-08 | Same instruction, same citation | **D-027** | same | **NON-ORIGIN** |
| 26 | `commissioning.md` "Chiller state is part of the measurement condition" | Same instruction, third time in one file | **D-027** | same | **NON-ORIGIN** |
| 27 | `software-spec.md` 6.4 item 4 and 11.5 | D-027's tagging is specified and unimplementable | D-027, S-18, D-064 | correct | **CLEAN.** The document says what commissioning.md does not |
| 28 | `order.md` K-DRY-Q envelope | "G-27 complementary pair to the Pi" on K-DRY | D-073 | D-073's envelope list, which cites MAIN-PANEL's return. **G-27 and D-053 were frozen out of the S-03 and D-042 pair on K-FILL-D, not out of K-DRY** | **NON-ORIGIN for K-DRY.** S-20's frozen row says "single series branch" and is not cited |
| 29 | `findings.md` F-056 | "the K-DRY pair" among five affected circuits | MAIN-PANEL, G-31, F-010 | same | **NON-ORIGIN for the word "pair"** |
| 30 | `subsystems/display-box.md` frozen slice, G-09 row | The Pi "reads back an auxiliary contact" | **G-09** | G-09's text says "reads back a contact on the contactor". **D-029 and `parts.md` establish there is no auxiliary block and the readback is pole 2, a 25 A power pole** | **NON-ORIGIN for the word "auxiliary"** |
| 31 | `subsystems/control-software.md` frozen slice, G-09 row | Same wording | **G-09** | same | **NON-ORIGIN** |
| 32 | `subsystems/main-panel.md` frozen slice, G-09 row | "provides an auxiliary contact for readback", and G-09 in its pre-D-031 wording | **G-09** | same, and G-09 as amended by D-031 says MOTOR supply | **NON-ORIGIN and STALE.** The same file carries the D-031 amendment further down |
| 33 | `subsystems/pump-boxes.md` frozen slice, G-09 row | "Driver power ... removed for all eight drivers at once" | **G-09** | G-09 as amended by D-031 | **STALE COPY** |
| 34 | `subsystems/control-software-p09.md`, "what it cannot tell you" | The readback is "the position of an auxiliary contact" | S-08 | D-029 | **NON-ORIGIN** |
| 35 | `parts.md` "The permissive readback" heading | "reads back a real auxiliary contact on that contactor" | the owner | **contradicted ten lines later in the same file: "There is no auxiliary contact block on the 22.32"** | **THE AUTHORITATIVE FILE STATES BOTH** |
| 36 | `software-spec.md` 4.2 | "The position of an auxiliary contact" | D-029, S-08 | D-029 | **NON-ORIGIN.** Already reported by run 3 as 1.6 DRIFT |
| 37 | Everything citing D-063 - C-23, C-02's blocked-on note, `software-spec.md` 6.4 item 3, F-045, F-046, F-057, D-091 | The manifold pump is intermittent and is OFF between batches | **D-063** | **D-063, which cites nothing.** D-091 then establishes that nothing commands it | **TERMINUS CITES NOTHING** |
| 38 | `software-spec.md` 2.4.5, `subsystems/control-software.md` frozen slice, `subsystems/display-box.md` | "A watchdog is the only recovery path" | P-07, `parts.md` | The owner's fact that the Pi's receptacle is fused and not relay switched. **A real origin** | **CLEAN, but see chain 39** |
| 39 | `subsystems/display-box-sweep.md` watchdog section | "If no external reset input is available on a Pi 5 ... P-07's 'watchdog is the only recovery path' becomes an open item rather than a plan" | its own search | the unchecked lookup, also named at C-20 and N-16 | **The condition on chain 38, carried in ONE file** |
| 40 | `software-spec.md` 11.12 | No Pi application source in reach | `subsystems/control-software.md` search record | the search record, which is present and enumerates what was searched including the searches that returned nothing | **CLEAN.** T-003 observed |
| 41 | Every DIR statement in the tree - D-069, D-096, F-053, F-059, F-072, `subsystems/pump-boxes.md`, `subsystems/pump-boxes-pulldowns.md` | Which way a floating DIR goes | **`parts.md`** | **`parts.md` board-pulls table: "a floating DIR goes LOW". `parts.md` four sub-sections later: "A FLOATING DIR FLOATS HIGH, NOT LOW. THIS REVERSES WHAT parts.md SAID BEFORE"** | **THE SINGLE TERMINUS STATES BOTH DIRECTIONS** |
| 42 | The figure family - the 55.34 and 22.32 minimum switching loads, the loop currents, the rail trim range, the tube life, the millilitres per revolution - restated across `decisions.md`, `findings.md`, `interface-table.md`, `order.md`, `commissioning.md`, `main-panel.md`, `main-panel-buy.md`, `main-panel-poles.md`, `display-box-sweep.md`, `pump-boxes.md`, `dosing.md` | every one | `parts.md`, by name, in almost every instance | `parts.md`, with the owner or a datasheet behind each | **CLEAN.** This is the tree's largest citation population and it does not have the shape |

---

## Hits, by classification

**CONFIRMED 6. SUSPECTED 2. CLEAN-BUT-FRAGILE 3.**

---

### CONFIRMED 1. "The Pi commands the circulation relay", live in five subsystem files

**Chains 3 to 11.** The claim's origin is interface row S-09 as first written,
and D-052 records where S-09 got it: "the owner's original project description
said the Pi commands relays for the transfer pump, the manifold pump and the
chiller. **That was loose.**" So the chain terminates in a description, which is
not an origin, and F-027 and D-052 closed it on 2026-08-30.

**What is still on disk and reads as live:**

| File | The sentence | Covered by an existing finding? |
|---|---|---|
| `subsystems/control-software-f004.md` line 45 | "The Pi commands the circulation relay, S-09, so it can require circulation commanded on for the whole window" | **Yes.** F-070, and `software-spec.md` 1.3 and 6.4 withdraw it |
| `subsystems/control-software-f004.md` line 218 | "The software commands the circulation relay so it knows what it asked for" | **NO** |
| `subsystems/control-software-p09.md` step 6 | "Commanded circulation and chiller states alongside, per D-027" | **NO** |
| `subsystems/dosing-f004-wet-side.md` line 34 | "The timer must be gated on the manifold pump being commanded on" | **NO** |
| `subsystems/control-software.md` "Settled" | "The Pi commands relays for the fill solenoid, transfer pump, manifold pump and chiller contactor" | **NO** |
| `subsystems/water-s18-f003.md`, `subsystems/main-panel-poles.md`, `subsystems/display-box-sweep.md`, `subsystems/display-box.md` | the exercise run, K-CIRC, four coil drives, "relay coil drives" | **Consequence** flagged by F-045, F-057, D-091 and by S-09's own row; **the files are unannotated** |

**Why this is the F-074 shape and not just staleness.** Two of these files are
CITED LIVE by rows nobody would re-derive. `commissioning.md` C-02 names
`subsystems/dosing-f004-wet-side.md` as its full procedure, and
`software-spec.md` N-4 names it again. A reader who goes to that procedure for
C-02 is told the settling clock must be gated on circulation-commanded-on. **The
gate does not exist.** And the corroboration is real: DOSING wrote the constraint
from wet-side physics and handed it to CONTROL-SOFTWARE, which wrote it back
citing S-09. **Two subsystems, two files, one claim, and the half that has an
origin is not the half that is being relied on.**

**What the claim rests on.** The physics half - settling counts circulating time,
so if the loop stops, settling stops - is DOSING's and stands on its own. **The
capability half rests on nothing.**

**TRUE regardless?** **NO.** G-26 and D-052 are frozen and say the opposite.
**This is F-074's class, not a documentation defect.**

**This answers AUDIT run 3's unsettled item 3 directly.** It asked someone to
check whether the two control-software returns carry any OTHER claim resting on
the withdrawn premise. **They do: `control-software-f004.md` line 218 and
`control-software-p09.md` step 6.** T-022's shape, as run 3 predicted.

---

### CONFIRMED 2. The VDD-to-VM adjacency, and it is the cleanest instance of the shape in the tree

**Chains 12 to 14.**

The claim: VDD and VM are two screw terminals apart on every driver, separated
only by GND, the closest approach between the two rails anywhere in this build,
and it is a screw terminal rather than a trace.

**Three places carry it and none is annotated:** `findings.md` F-031;
`subsystems/display-box-short-column.md` in two places, one of them headed **"One
adjacency stated as fact rather than guess"**; and `decisions.md` D-061's segment-5
paragraph, which adds that DIR's neighbours are STEP and EN and "neither is an
energised rail".

**The terminus.** Both DISPLAY-BOX and PUMP-BOXES cite `parts.md`'s printed pin
list. **F-058 establishes that the list was a list of NAMES, that it was read as
an ORDER and the order read as ADJACENCY, and that the part is two connectors.**
`parts.md`'s own board-in-hand section then records the header silk and states
that VDD and DIR are physically adjacent. **So the cited file never contained the
claim.**

**Why it is the illusion and not one error.** DISPLAY-BOX reached it in the short
column and PUMP-BOXES reached it in segment 5, on different days, in different
subsystems, and the tree records them as two lines of evidence. **They are one
misreading of one list.** F-058 says so in terms: "T-013's disease committed at
the DOCUMENT level rather than in a procedure step. Three conclusions rest on
it."

**What it rests on now.** Nothing. F-058 withdraws the premise and `parts.md`'s
photograph section contradicts it.

**TRUE regardless?** **NO.** F-058 calls PUMP-BOXES' half "WRONG IN THE UNSAFE
DIRECTION". **F-074's class.**

**The residual, which is the reportable part.** The withdrawal lives only in
F-058's row. **D-061 is a frozen decision - G-29 was frozen out of it - and its
segment-5 paragraph still reads as good news.** F-031 still reads as live and is
what F-020's over-voltage requirement is written against. A reader arriving at
either does not pass F-058.

---

### CONFIRMED 3. "CH5 and CH6 are the pH pair", and D-099 is frozen on it

**Chains 15 to 21.**

Six places state it flat, with no mark: `findings.md` F-063 ("THE TWO pH CHANNELS
ARE CH5 AND CH6"); `colour-map-proposal.md` constraint 1 ("They are the pH
pair"); `decisions.md` D-085, D-083 and D-099's colour table;
`channel-register.md`'s "What the software does know" section.

Two places mark it: `channel-register.md`'s header ("**CH6 is the other pH
channel by elimination. That is an inference, not a statement, and it is marked
as one**") and `software-spec.md` 3.2, which tells an implementer not to promote
the inference to a fact.

**The terminus.** CH5's role marking has a real origin, the controller's
blocked-channels path, and D-086 says so explicitly. **CH6's does not.** The
elimination runs through "the two 1000 mL channels are the pH adjusters", and
that pairing is the Jug column, which `channel-register.md`, D-086 and T-018 all
say is **a SEED in a configuration file and not a measurement of the world.**

**What it rests on.** For CH5, the controller config. **For CH6, a retracted
seed.**

**TRUE regardless?** **UNSETTLED.** D-086 says the inference "is probably right,
because pH adjusters are concentrated and used in small volumes, but the config
does not say it." Nothing binds a token to a product before C-09.

**Why it is not tidy-up, and this is the expensive part.** **D-099 is frozen and
it bound the colour axis with CH5 and CH6 maximally separated as its hardest
constraint.** `channel-token.md` says the S-16 non-adjacency rule is "Declared
now, applied once the products are assigned." **D-099 applied it before
assignment, against an inferred assignment.** And T-022 has already run on this
label once: F-071 was split out of F-064 and withdrawn, while **F-063 itself was
qualified only on the size axis** - the pair identification inside it was never
qualified, and D-085 and D-099 both spend it.

If CH6 is not the second pH channel, what fails is not the colour map's
legibility but its reason: the strongest separation in the set has been spent on
the wrong pair, and the pair that needed it did not get it.

---

### CONFIRMED 4. "auxiliary contact" for what D-029 established is a power pole

**Chains 30 to 36.**

D-029 and `parts.md` are unambiguous: there is no auxiliary block on the 22.32,
none was ever bought, pole 2 was free, and **a 25 A power pole is the readback
contact.**

**Five files outside document 12 still call it an auxiliary contact**, each
citing G-09: `subsystems/display-box.md` frozen slice,
`subsystems/control-software.md` frozen slice, `subsystems/main-panel.md` frozen
slice, `subsystems/control-software-p09.md`, and - the terminus itself -
**`parts.md`'s own "The permissive readback" heading, ten lines above the section
that says no auxiliary block exists.**

G-09's text says "reads back a contact on the contactor". **The word "auxiliary"
was added by the copies, and the authoritative file is on both sides of it.**

**TRUE regardless?** **Substantively yes, mechanically no.** The readback exists.
**It is a power pole, and that is the entire subject of F-055**, which run 3
found absent from document 12 and which I find is also not reflected in any of
the four subsystem frozen slices. A reader who believes the readback is an
auxiliary block has no reason to read F-055.

Also live: `subsystems/main-panel.md`'s Open list still asks "whether the
auxiliary contact needed for S-08 exists on the part the owner has", which D-029
answered on 2026-08-30.

**Documentation defect around a claim that is true in substance and false in
mechanism**, and the false half is load-bearing on an open finding.

---

### CONFIRMED 5. `commissioning.md` instructs a tagging D-064 says cannot be done

**Chains 24 to 27.**

Three places in `commissioning.md` - C-02's blocked-on column, C-08's measurement
column, and the standing section "Chiller state is part of the measurement
condition" - instruct that chiller state be **recorded against every sample, per
D-027**.

**D-027's stated mechanism is "The Pi commands the contactor, so it knows."**
G-26 and D-052 removed it. F-043 says S-18 "was closed against a capability that
no longer exists". D-059 reopened S-18. **D-064 says in terms: "D-027's sample
tagging cannot be implemented as written, because there is no chiller state to
tag with."**

`software-spec.md` 6.4 item 4 and 11.5 say the same. **`commissioning.md` does
not, in any of the three places, and it is the file the owner reads while
measuring.**

**What it rests on.** D-027 is the origin of the instruction and not the origin
of the capability. The capability was withdrawn.

**TRUE regardless?** **No, as written.** "Every sample" is a Pi sample -
`subsystems/dosing-f004-wet-side.md` step 1 has the trace logged at the fastest
rate the Pi will read. The Pi has no chiller state, commanded or measured. **A
person could annotate the trace by eye and no file says so.**

**Documentation defect if a human is meant to write it down. F-074's class if a
field is meant to be populated.** Nothing on file distinguishes them, and that
is what makes it reportable rather than obvious.

---

### CONFIRMED 6. The Vref instruction copied past its own correction

**Chain 22.**

`parts.md` carried "set the pot with a meter before any power is applied" from
2026-08-30. F-061 established it is unexecutable as written, and `parts.md` now
says so at that line, with D-081 and C-22 carrying the consequence.

**`subsystems/pump-boxes.md` line 45 still states it flat**, inside the section
headed "Facts arrived 2026-08-30, **read parts.md before anything else**". The
same file carries the retraction at lines 105 to 108. **One file, both states,
and the uncorrected copy is in the section that tells the reader to trust it.**

**What it rests on.** Nothing. F-061 is unopposed in the tree.

**TRUE regardless?** **No.** And C-22 is a hazard row, so the cost of the copy is
that someone reads the wrong procedure at the moment F-061 says a person has a
screwdriver on a pot beside four motors.

**This is the exact failure the CLEAN-BUT-FRAGILE category predicts: one file
carried the origin, the origin changed, and nothing flagged the copy.** It is
CONFIRMED rather than fragile because the change has already happened.

---

### SUSPECTED 1. "The manifold pump is off between batches" - the terminus cites nothing

**Chain 37.**

D-063 states it: "It runs when the system needs the tank mixed or moving: during
a batch, during dosing, and through a settle window. **Between batches it is
off.**" **D-063 gives no source.** It is written as a decision, but it describes
how the panel behaves, which is not something a decision can settle.

Seven places build on it: C-23 (a hazard row instructing the owner to confirm the
pump is running across the window), C-02's blocked-on note, `software-spec.md`
6.4 item 3 and 4.3, F-045's resolution ("it does NOT dissolve"), F-046's
resolution ("CLOSED in the favourable direction. Circulation is intermittent, so
both survive"), F-057's resolution, and D-091.

**And D-091, answering F-057, says: "there is no command path".** Circulation is
a pole on K-DRY; K-DRY is a permission; **nothing in any file I read says what
de-energises K-DRY between batches.** I checked `interface-table.md` S-05 and
S-20, `subsystems/main-panel-poles.md`, `subsystems/main-panel-buy.md`,
`order.md`, `parts.md`'s permissive-chain section and D-038, D-058, D-060 and
D-091. **I did not find it. I am not asserting it is absent - I am naming what I
read.**

**Why SUSPECTED and not CONFIRMED.** The owner may simply have said it, and
D-063 may be the faithful record of that. **But two findings were closed in the
favourable direction on the strength of it (F-046) and one commissioning hazard
row is written against it (C-23), and the file that would carry the origin says
nothing.** The owner is the only one who can say which came first.

---

### SUSPECTED 2. A complementary pair on K-DRY that S-20 does not provide for

**Chains 28 and 29.**

`decisions.md` D-073's envelope list and `order.md`'s envelope map both give
K-DRY-Q "the G-27 complementary pair to the Pi", and `findings.md` F-056 lists
"the K-DRY pair" among the five circuits affected by the trim-range sizing.

**G-27 and D-053 were frozen out of the S-03 and D-042 changeover on K-FILL-D**,
per `subsystems/main-panel-buy.md`. **The frozen S-20 row describes one isolated
Pi input, "single series branch", and is cited by none of the three.**
`subsystems/display-box-short-column.md` requirement 3 asks for a polarity on
S-20, not a pair.

Three files agree and all three descend from MAIN-PANEL's returns, so the
agreement is not corroboration. **The pole arithmetic in `order.md` is consistent
with the pair being the two legs of ONE changeover**, which is how K-FILL-D's was
done, so this may be entirely sound and simply never written back to S-20.

**Which it is decides whether S-20's row or the order's envelope map is the one
that moves.** MAIN-PANEL and the owner, not me.

---

### CLEAN-BUT-FRAGILE 1. `parts.md` is the sole terminus for DIR and it states both directions

**Chain 41.**

Every statement in the tree about which way a floating DIR goes terminates in
`parts.md`. **`parts.md`'s board-pulls table says "So a floating DIR goes LOW,
via the CHIP's internal pulldown".** Four sub-sections later `parts.md` says **"A
FLOATING DIR FLOATS HIGH, NOT LOW. THIS REVERSES WHAT parts.md SAID BEFORE."**

D-026 makes this file authoritative and says no agent may contradict a line in
it. **Two of its lines contradict each other and only the second is marked.**

Correctly sourced today - D-096, F-059 and F-072 all carry the reversal, and
D-096 routed it to PUMP-BOXES. **Fragile because the whole tree's DIR reasoning
hangs on one file and that file answers the question twice.** D-062's gate has
flipped its question on the strength of the second answer, and the first answer
sits above it under a heading that says "THIS IS THE D-062 ANSWER".

---

### CLEAN-BUT-FRAGILE 2. "A watchdog is the only recovery path" carries a condition only one file states

**Chains 38 and 39.**

The claim has a real origin: the Pi's receptacle is fused and not relay switched,
recorded in `parts.md` from the owner. It is restated in P-07, in
`subsystems/control-software.md`'s frozen slice, in `subsystems/display-box.md`
and at `software-spec.md` 2.4.5, each citing P-07 or `parts.md`. **That is a
correct chain.**

**One file names the condition.** `subsystems/display-box-sweep.md`: "If no
external reset input is available on a Pi 5, the watchdog as specified cannot be
built and **P-07's 'watchdog is the only recovery path' becomes an open item
rather than a plan**." N-16 and C-20 both carry "whether an external reset input
exists at all".

**If that lookup comes back badly, four restatements of a closed row go with it
and nothing links them to the file that predicted it.**

---

### CLEAN-BUT-FRAGILE 3. G-09's superseded wording in two frozen slices

**Chains 32 and 33.**

`subsystems/main-panel.md` and `subsystems/pump-boxes.md` both restate G-09 in
its pre-D-031 wording - power removed from every driver, no supply named. G-09
itself was amended by D-031 and `decisions.md` carries the amendment.
`subsystems/main-panel.md` also carries it, lower in the same file, under "Open,
added or sharpened".

Correctly sourced when written. **Fragile because a frozen slice is the thing a
subsystem builds against, and the amendment is the whole subject of P-09 and
F-014.**

---

## The weaker shape: the same claim in two files with no citation between them

I looked for this separately, per the brief. Three populations, and only one of
them is a problem.

**1. The withdrawn coil-drive picture.** `subsystems/display-box.md`'s scope says
"relay coil drives" plural; `subsystems/control-software.md`'s "Settled" section
names four. **Neither cites the other and neither cites anything.** They are not
independent: D-052 records that both descend from the owner's original project
description. **This is the weaker shape resolving into CONFIRMED 1 once the
common ancestor is found**, and it is worth saying that the ancestor was only
findable because D-052 wrote down where the error came from. Provenance recorded
once made a whole family traceable.

**2. The F-004 settle-window prohibitions.** `subsystems/control-software-f004.md`
and `software-spec.md` sections 5.6 and 6.4 carry near-identical lists, and
`software-spec.md` 1.3 declares the relationship explicitly - superseded as a
deliverable, standing as reasoning. **Declared, not hidden. Not a hit.**

**3. The figure family.** Chain 42. Every minimum switching load, loop current,
rail figure, tube life and delivery figure I traced resolves to `parts.md` by
name, and `parts.md` states where each came from. **I could not find a figure in
this tree that is restated in two files without `parts.md` behind it.** The
searches were: the two Finder minimum switching loads, the two loop currents, the
readback current window, the rail trim range, the millilitres per revolution, the
tube life, and the wall dimension, grepped across all thirty-three files. That is
what I read to establish it.

---

## Where the tree does this correctly, stated so the counts mean something

- **`software-spec.md` 3.2** is the only downstream file that carries
  `channel-register.md`'s inference marking rather than the inference. It tells
  an implementer not to promote it. **That is G-37 observed before G-37 existed.**
- **`software-spec.md` 6.4 splits Claim A from Claim B before qualifying
  either**, and says which rests on which row. It is the only place in the tree
  where a document pre-splits its own claims by provenance.
- **`software-spec.md` 11.12 and `subsystems/control-software.md`'s search
  record** are a citation and a source, and the source is a real enumeration
  including the searches that returned nothing.
- **`decisions.md` D-052 recorded where an error came from**, which is the only
  reason CONFIRMED 1 could be traced at all.
- **`findings.md` F-058 caught the document-level version of this shape
  unprompted**, and named all three conclusions resting on it. Its only failure
  is that the three were not annotated where they live.
- **`parts.md` names its own weakest provenance** at the Pi header section -
  forum statements, not a datasheet - and D-098 carries that forward.
- **`decisions.md` D-088 and T-022** are this shape caught in advance, on a
  label rather than on a citation.

---

## What I could not settle

**1. Whether D-063 has an origin.** SUSPECTED 1. If the owner stated the
intermittent duty cycle, D-063 is a faithful record and everything downstream is
sound. If D-063 inferred it, then F-046's favourable closure and C-23's hazard
instruction rest on an inference and D-091 is the file that says so. **I cannot
tell from the tree and I did not look outside it.**

**2. Whether the K-DRY complementary pair is real.** SUSPECTED 2. Either S-20's
row is short a leg or `order.md`'s envelope map has a leg S-20 never granted.
`subsystems/main-panel-poles.md` and `subsystems/main-panel-buy.md` both predate
D-072's envelope split and neither settles it.

**3. Whether `commissioning.md`'s chiller-state instruction is meant for the Pi
or for a person.** CONFIRMED 5 turns on it. C-02 and C-08 say "against every
sample" and the samples are the Pi's, which points at the software reading. **If
the intent is that the owner writes it on the trace, the rows are executable and
what is wrong is only the D-027 citation.**

**4. Whether CH6 is the second pH channel.** CONFIRMED 3 establishes that the
tree's own record calls it an inference and that six files state it flat. **It
does not establish that the inference is wrong.** C-09 settles it, and D-099 is
frozen before C-09.

**5. Whether `subsystems/control-software-f004.md` and
`-p09.md` contain any FURTHER claim on the withdrawn premise beyond the two I
found.** I read both in full and found two. **I searched for the premise by its
wording, not by its consequences**, so a claim that relies on commanded
circulation without using those words would not have surfaced. Run 3 asked this
question; I have narrowed it, not closed it.

**6. Anything that was never cited.** The method finds chains. **A claim that
sits in one file, cited by nobody, and rests on nothing has no chain and does not
appear in this report.** Audit 7 in D-094's set - tracing every figure to the
world or to a file that had to contain something - is the run that would find
those, and it is not this run.

**7. The operator interface.** HELD by the owner. I asked no question about it.
