# D8. Commissioning checklist

**The staged procedure, on paper, pen in hand. Written 2026-09-23 by INTEGRATOR.**

**THIS DOCUMENT IS A VIEW OF `commissioning.md` AND STATES NO MEASUREMENT OF ITS OWN.**
Every measurement, every condition, every re-measure trigger and every prerequisite is
a C- row there. **What is here is the tick box, the stage gating, and the one line that
says how you know.** D4 is a view of D5 in exactly this way, and for the same reason:
G-45, two documents that must agree are generated from one source rather than told to
agree.

**IF A STEP BELOW AND A C- ROW DISAGREE, THE C- ROW WINS AND THE DISAGREEMENT IS A
DEFECT IN `commissioning.md`.** G-54: a fact enters at the source, never at the view.
Section 13 lists the ones found while writing this, reported and not resolved here.

**The reasoning is not here and should not be.** `commissioning.md` carries the
corrections, the struck rows and the reasons, and it is tree state. This page carries
the work.

**THIS DOCUMENT ADDS NO PART TO THE BUILD.** G-48. What it costs is time with a meter
and a pen; two steps in it can generate a part, and each says so on the step.

---

## 1. HOW TO READ A STEP

**Every step is numbered D8-01 upward, once through the whole document, and the numbers
are never silently changed.** If one is ever inserted it takes a letter, D8-09a, and a
REVISION line appears at the head of its stage. There are no revision lines yet.

**No step refers to another by its number.** Where one depends on another, the other is
named by its C- row, because a step number is a position in a list and a position moves
when the list does. T-013.

Every step has the same five lines:

| Line | What it is |
|---|---|
| **The step** | **ONE ACTION.** A tick box beside the number. G-49 |
| **SOURCE** | The C- row this step runs. **The method is there and is not repeated here** |
| **BEFORE** | What must be true at the moment you start, folded into this step and never stated after it. **T-020: a correction after the step it modifies is read too late** |
| **ACCEPT** | **How you know it is right, observable at that moment.** Where the C- row states no success criterion the line says **NO ACCEPTANCE CRITERION IN THE ROW** and names who owns it. **It is never invented here** |
| **RECORD** | Where the figure goes: a row in D9, `maintenance-record.md` |

**A step that says BLOCKED has no accept condition yet.** It names what is missing and
who owns it. **Do not substitute, do not pick a likely value, do not skip ahead.** Leave
it and go to the next step, so that you are stepping over it rather than finding out
later that something was left out. This is D4's rule and it is the same rule.

**NO STAGE IS STARTED UNTIL EVERY BOX IN THE ONE BEFORE IT IS TICKED**, except where a
stage carries its own explicit note saying otherwise.

---

## 2. STAGE 1. THE CHECKS THAT CANNOT WAIT FOR COMMISSIONING

**THIS STAGE RUNS INSIDE D1, NOT AFTER IT.** Both rows in it have a precondition that
the build destroys as it proceeds, so a stage that waits for a finished machine cannot
run them. **They are listed here because a checklist that leaves them out reads as
though they were not commissioning, and then nobody ticks them at all.**

**MUST BE TRUE BEFORE THIS STAGE STARTS:**
- D1 section 13 has mounted both main panel ground bars and fitted the inter-bar jumper,
  and nothing else has landed on either bar. C-25's own blocked-on cell.
  **PRODUCER: PRODUCED, BB-17.** Its wording says "the ground bar" singular where D-192
  put two bonded bars. Listed in 12.4.
- D1 section 15 has the display box plate populated and the three EZO circuits in hand,
  **with the box still open.** C-14's own blocked-on cell.
  **PRODUCER: PRODUCED, BB-19.**

**TRUE AFTER THIS STAGE ENDS:**
- The inter-bar jumper's continuity is proved and recorded.
- The mode pin and the procedure used are recorded for each of the three EZO circuits,
  individually.

**D8-01. Run C-25 on the two main panel ground bars.**
SOURCE: `commissioning.md` C-25. One measurement.
BEFORE: **the panel plate has been confirmed non-conductive from the part in your hands
and against D-195, not from the block's appearance** - C-25 says the block looks
identical either way. And nothing but the jumper is on either bar: C-25's whole value is
that it is made when it is one wire.
ACCEPT: a meter reads continuity across the jumper. **The criterion is in the row and in
D3 sheet 3.7.3 step 4, which already carries C-25 as its acceptance condition.**
RECORD: D9 row **MR-01**.
COST AND WHAT IT BUYS, G-48: **no part, one meter reading.** It buys the only detection
of a missing or backed-out jumper, whose failure is otherwise silent with every ground
landed and everything looking correctly built. **Done later it means lifting landings to
prove what could have been proved on one wire.**

**D8-02. Confirm C-14 has been run and recorded on the EZO pH circuit.**
SOURCE: C-14. The procedure is D1 step 15-06 and the record is 15-06a.
BEFORE: the display box is still open.
ACCEPT: the Pi sees that circuit, **and** D9 carries the pin and the procedure used for
it.
RECORD: D9 row **MR-02**.

**D8-03. Confirm C-14 has been run and recorded on the EZO EC circuit.**
SOURCE: C-14.
BEFORE: as D8-02.
ACCEPT: as D8-02.
RECORD: D9 row **MR-03**.

**D8-04. Confirm C-14 has been run and recorded on the EZO RTD circuit.**
SOURCE: C-14.
BEFORE: as D8-02.
ACCEPT: as D8-02.
RECORD: D9 row **MR-04**.
WHY THESE ARE THREE STEPS AND NOT ONE REPEATED THREE TIMES: **C-14 says the mode pin
differs by circuit type, so this is THREE DIFFERENT PROCEDURES.** Without a per-circuit
record nobody can repeat it after a board swap, and the next person applies the pH
procedure to the RTD circuit.

**GATE 1. Do not start stage 2 until D8-01 to D8-04 are ticked.**

---

## 3. STAGE 2. LANDINGS, WITH NOTHING ENERGISED

**This is the stage the document plan names: the first stage checks landed conductors
against the schedule, and ringing out a series string is reading the ladder with a
meter.** It consumes no C- row. **It states no conductor fact: every fact it checks
against is a CDR- row in D5 or a rung in D2.**

**IT CAN BE WRITTEN NOW AND IT CANNOT BE RUN YET.** F-106 is open: nobody has read a
terminal, `terminal-survey.md` is the form, and every one of D4's 127 joints is blocked
on it. **A conductor that has not been landed cannot be checked as landed.**

**MUST BE TRUE BEFORE THIS STAGE STARTS:**
- **F-106 closed.** `terminal-survey.md` filled, per D1 section 4.
- **BB-35**, D1 section 31. Every conductor in D5 is cut, routed, labelled at both ends,
  landed and ticked.
- **D1 step 31-02.** Every wet joint's cure has been confirmed against the joint-time
  records, not against anybody's memory.
  **PRODUCER: PRODUCED, D1 step 31-02 - and NOT by BB-35, which covers conductors only.**
  BB-35 is extended to carry it. Listed in 12.4.
- Nothing in the build is energised.
  **PRODUCER: INVARIANT.** True from the first step and produced by nothing. **Ended by
  stage 4, which energises the supply.** It is not a missing arc and must not be
  reported as one.

**TRUE AFTER THIS STAGE ENDS:**
- Every CDR- row D5 lists as landing in an enclosure is ticked as landed and labelled.
- Every grounding conductor lands on one of the four bars and nowhere else.
- Every series string reads as D2 draws it, with the panel dead.

**D8-05. Confirm every joint step on every D4 page carries a tick or still carries its
original blocker.**
SOURCE: D4, `wiring-instructions.md`. **This is not a C- row.**
BEFORE: nothing energised.
ACCEPT: no joint step is unticked without a blocker, **and no blocked joint has been
substituted, guessed at or skipped ahead of.**
RECORD: no figure. Tick only.

**D8-06. Confirm the count of ticked CDR- rows equals the count of CDR- rows D5 lists
as landing in an enclosure.**
SOURCE: D5, `wiring-schedule.md`.
BEFORE: D8-05 ticked.
ACCEPT: **the two counts are equal.** T-012: make the check an identity rather than a
bound, because a bound passes while the number drifts.
RECORD: no figure. Tick only.
WHY A COUNT AND NOT A READ-THROUGH: **T-008 and T-010. A cable declared as N conductors
is not N landed conductors, and two bus terminals once carried twelve conductors on
eight clamps for months.**

**D8-07. Confirm every grounding conductor lands on one of the four ground bars and
nowhere else.**
SOURCE: D5's grounding rows; D1 step 31-08; D-165.
BEFORE: D8-06 ticked.
ACCEPT: the count of conductors on the four bars equals the count of grounding
conductors D5 lists, **and no conductor is bonded to any other point.**
RECORD: no figure. Tick only.
WHY IT IS ITS OWN STEP: **a builder who finds a convenient screw will use it**, and the
four bars are the only bonding points in this build.

**D8-08. Ring out each series string against D2, with the panel dead.**
SOURCE: D2, `electrical-schematic.md`. **This step states no rung, no contact and no
device: read them off D2.**
BEFORE: D8-07 ticked. Nothing energised, and it stays that way through this step.
ACCEPT: each string reads as D2 draws it, rung by rung.
RECORD: no figure. Tick only.

**GATE 2. NOTHING IS ENERGISED UNTIL EVERY BOX IN STAGE 2 IS TICKED.**

---

## 4. STAGE 3. PROVING WHAT A BROKEN CONDUCTOR DOES, STILL DEAD AND STILL DRY

**Both rows here prove a CLAIM that nothing else in the build reaches. T-014: a claim
nobody tested is a claim nobody has.**

**MUST BE TRUE BEFORE THIS STAGE STARTS:**
- Stage 2 closed.
- **The tanks are empty and dry.** C-24 says to run it before water is in the tanks: the
  test is about conductors and coils, and a wet tank adds nothing to it and makes the
  lifting worse.
  **PRODUCER: PRODUCED, BB-20, then INVARIANT. Ended by stage 7**, which fills the day
  tank.
- **The pull-down resistors are fitted at the DRIVER end.** C-21's blocked-on. **BLOCKED
  TODAY: D5 records them as an owed fix and not as a fitted part, PUMP-BOXES' under
  D-043.**
  **PRODUCER: PRODUCED, BB-35.** D1 14-08 fits the pull-down LANDING; the pull-downs
  themselves are landed in section 31. **The producer existed and the precondition did
  not name it, which is the whole reason this one read as a gap.**
- **V_IL is known from the datasheet.** C-21's blocked-on. **BLOCKED TODAY.**
  **PRODUCER: LOOKUP.** A fact from outside the build. No section can produce it and none
  should be asked to. Owner's, under G-15.

**TRUE AFTER THIS STAGE ENDS:**
- Every float position's fail direction is proved.
- Every STEP and DIR conductor's level at the driver terminal is proved.

**D8-09. Run C-24 on one float position: lift that float's conductor at the panel
terminal and observe the chain.**
SOURCE: C-24. One lift.
BEFORE: tanks empty and dry, the chain complete, and the float's conductor landed.
**Write the position's name beside the tick.** How many float positions there are is
D2's roster's fact and the float requirement's, and is not stated here.
ACCEPT: **LIFT IT, THE PERMISSIVE DROPS, TICK.** With the conductor lifted the chain
OPENS and the permissive drops, observable at the panel: **the master permissive relay
releases and STAYS released until the conductor is landed again.**
**IF THE PERMISSIVE HOLDS, STOP AND DO NOT PROCEED.** A lifted conductor that leaves
the permissive MADE means that position is not in the series path it is supposed to be
in.
**ORIGIN: ELIJAH, 2026-09-23.** **SUPPLIED, not derived from a part figure.** The eight fail directions
in D-154 are what the chain is supposed to do; **this step tests one thing about each -
that the position is actually in the series path - because that is the only thing
observable at that moment, and it has never been verified.**
RECORD: D9 group **MR-G1**, one row per float position.
COST AND WHAT IT BUYS: **no part and no instrument added.** It buys the only test of the
float fail directions that exists, because C-19 records what the Pi reports and G-01
makes all eight floats invisible to the Pi. **F-109.**

**D8-10. Repeat D8-09 for the next float position, and start none until the one before
it is ticked.**
SOURCE: C-24.
BEFORE: as D8-09.
ACCEPT: as D8-09. **Lift it, the permissive drops, tick. Same criterion for every
position, because every float is in series.** **ORIGIN: ELIJAH, 2026-09-23.**
RECORD: D9 group **MR-G1**.

**D8-11. Confirm every float position in D2's roster carries a tick.**
SOURCE: C-24, against D2's roster.
BEFORE: D8-10 exhausted.
ACCEPT: the count of ticks equals the count of positions in the roster.
RECORD: no figure. Tick only.

**D8-12. Run C-21 on one STEP or DIR conductor: lift it at the display end and measure
the driver terminal.**
SOURCE: C-21.
BEFORE: the pull-down fitted at the driver end. **Write the conductor's CDR- id beside
the tick.** How many STEP and DIR conductors there are is D5's fact.
ACCEPT: **NO ACCEPTANCE CRITERION USABLE AT THAT MOMENT.** The row says the terminal
must sit below V_IL and **V_IL is not in the row**; its own blocked-on cell says V_IL
comes from the datasheet. **The row also does not say whether VDD is present for the
measurement.** Owner: **the owner's lookup under G-15, with PUMP-BOXES stating the
requirement**, per rule 3 and per F-059's precedent.
RECORD: D9 group **MR-G2**, one row per conductor.
COST AND WHAT IT BUYS: **cheap, and per-driver because the part is per-driver.** It
buys detection of a backed-out pull-down lead, which leaves a floating input on an
enabled driver with the box looking correctly built and nothing downstream measuring
direction or delivery.

**D8-13. Repeat D8-12 for the next STEP or DIR conductor, and start none until the one
before it is ticked.**
SOURCE: C-21.
BEFORE: as D8-12.
ACCEPT: as D8-12. **NO ACCEPTANCE CRITERION USABLE AT THAT MOMENT.** Owner: as D8-12.
RECORD: D9 group **MR-G2**.

**D8-14. Confirm every STEP and DIR conductor D5 lists carries a tick.**
SOURCE: C-21, against D5.
BEFORE: D8-13 exhausted.
ACCEPT: the count of ticks equals D5's count.
RECORD: no figure. Tick only.

**GATE 3. Water does not go in a tank until D8-11 is ticked.** That gate is C-24's own
and D1 section 33 restates it.

---

## 5. STAGE 4. THE RAIL, AND THE ONE HAZARD ROW ON IT

**READ C-22 BEFORE YOU POWER ANYTHING IN THIS STAGE. It is a hazard row and not a
measurement:** setting Vref requires the permissive CLOSED and 24 V LIVE in the box
while a person has a screwdriver on a pot beside four motors. **F-061.**

**MUST BE TRUE BEFORE THIS STAGE STARTS:**
- Stage 2 closed and stage 3 closed.
- **C-16's own precondition: the supply powered, before anything else is connected to
  the rail. THIS PRECONDITION IS UNMATCHED BY ANY STATE THE BUILD PRODUCES.** See
  section 12, check result 1. It is not resolved here.
  **PRODUCER: UNPRODUCED, and F-125 says the requirement is wrong rather than
  unachievable** - a rail with nothing on it is not the rail the devices see. Routed to
  the owner.

**TRUE AFTER THIS STAGE ENDS:**
- The NDR-240-24 trim position as actually left is measured at the rail and recorded.
- Every driver's Vref has been set with VS present, under C-22's stated conditions.

**D8-15. Confirm BOSS has ruled on whether C-22's two-step reconciliation is the
procedure, before the supply is powered for the first time.**
SOURCE: C-22.
BEFORE: nothing powered.
ACCEPT: a dated ruling exists in `decisions.md`.
**BLOCKED TODAY. Missing: C-22 offers the two-step reconciliation - pre-set the pot to
minimum before power, then set VREF with VS present - explicitly AS A READING, and
nothing has adopted it.** Owner: **BOSS.** **Do not read the reading as the procedure.**
RECORD: no figure. Tick only.

**D8-16. Run C-16: measure the NDR-240-24 trim position as actually left, at the rail.**
SOURCE: C-16.
BEFORE, AND IT IS FOLDED IN HERE BECAUSE IT CHANGES HOW YOU TAKE THE READING: **the trim
reading is NOT the number that matters.** F-052 and D-071: the board's ceiling and the
rail's OVP trip are the same number, and stray inductance can ring a DC reading upward.
**Keep VS and its return short and paired; the local bulk cap absorbs the ring.**
ACCEPT: **NO ACCEPTANCE CRITERION IN THE ROW.** C-16 names no target and no tolerance.
It says only that a rail nobody recorded is a rail nobody can check later. Owner:
**PUMP-BOXES owes the 6121's VM range per F-010, and the owner runs every other device
rating on the rail under G-15.**
RECORD: D9 row **MR-05**.

**D8-17. Set Vref on one driver with VS present, per C-22, and tick, writing that
driver's identifier beside the tick.**
SOURCE: C-22.
BEFORE: **the permissive is CLOSED and 24 V is LIVE in the box, with four motors beside
your hand. C-22 exists because that is the condition the work requires and nobody had
written it down.** Instruction "set the pot before any power is applied" is unexecutable:
with no power there is nothing to measure.
ACCEPT: **NO ACCEPTANCE CRITERION IN THE ROW.** C-22 names no Vref target. Owner:
**PUMP-BOXES to state the requirement, the owner to run the lookup under G-15.**
RECORD: **NO D9 ROW EXISTS FOR THE AS-SET VREF, AND THAT IS DELIBERATE.** See section
13, defect 6: no C- row schedules recording it, and a D9 row for a figure the register
does not schedule would put the view ahead of its source. G-54.

**GATE 4. Do not start stage 5 until D8-16 is ticked and recorded.**

---

## 6. STAGE 5. LOGIC AND SENSE

**MUST BE TRUE BEFORE THIS STAGE STARTS:**
- Stage 4 closed.
- Sense circuits built and the Pi reading them. C-19's blocked-on.
  **PRODUCER: PRODUCED, BB-19 and BB-35.**
- **The watchdog daemon is ENABLED AND PETTING, verifiable by reading its state.**
  **REWRITTEN 2026-09-23, D-233. It read "the watchdog fitted, and confirmation that an
  external reset input exists at all", and "FITTED" WAS THE WHOLE DEFECT: it reads as a
  part, and everything on file describes software.** The owner has chosen the Pi 5 SoC's
  own internal watchdog - **no part, no pin, no panel device, and the external reset
  input answered NO by decision.** Nothing gets installed because there is nothing to
  install.
  **PRODUCER: SOFTWARE STATE, not a build state, D-233.** No section produces it and
  none should: **the SoC watchdog is enabled by the application at start-up and is
  verified by reading its state.** It leaves the build's dependency graph entirely.
- **S-12 is an OPEN interface row.** Rule 9: nothing is built against it. **Every step in
  this stage needs the Pi reading a pin, so this stage cannot run while S-12 is open.**
  **PRODUCER: OPEN ROW.** Closed by DISPLAY-BOX and CONTROL-SOFTWARE agreeing the pin
  map, not by any build step. **It belongs in the interface table's graph, not this
  one.**

**TRUE AFTER THIS STAGE ENDS:**
- Every sense conductor's fail behaviour is recorded as the Pi reports it.
- The watchdog has been seen to fire and seen not to loop silently.

**D8-18. Run C-19 on one sense conductor: disconnect it at the gland and record what
the Pi reports.**
SOURCE: C-19. No instruments needed.
BEFORE: **at the gland, not at a terminal.** Write the conductor's CDR- id beside the
tick. How many sense conductors there are is D5's fact.
ACCEPT: **THE PI REPORTS THE SIGNAL IN ITS SAFE DIRECTION WITHIN ONE READ INTERVAL,
AND THE REPORT PERSISTS WHILE THE CONDUCTOR IS DISCONNECTED.**

**THE CRITERION IS A DIRECTION, NOT A VALUE, and the person decides it standing there:
disconnect it, and THE MACHINE BECOMES MORE CAUTIOUS RATHER THAN LESS. If it becomes
less cautious, that conductor fails.** G-22: a severed conductor must produce the report
that INHIBITS action, not the one that permits it. **Fill sense severed reads as
FILLING and dosing is inhibited. Readback severed reads as NOT PULLED IN.**

**The tick is on the direction. The CDR- id and the actual report go in the record.**

**AND IF A CONDUCTOR'S SAFE DIRECTION IS NOT STATED, IT IS NOT GUESSED AT THE BENCH.**
It is a gap and it goes to the owner. **Section 12.8 carries the table, and every entry
in it is now answered, 2026-09-23.**

**START WITH A PROBE CONDUCTOR AND KNOW WHAT YOU ARE LOOKING FOR, D-233.** The step
disconnects AT THE GLAND, **and the probe cable is what is at the gland, so S-11 is the
first conductor this step meets.** Its answer is not a direction: **an unreadable probe
raises a LATCHING fault and no batch may start or continue while it is raised.**

**SO IF THE SOFTWARE DOES NOTHING VISIBLE WHEN A PROBE CONDUCTOR IS PULLED, THE STEP HAS
FOUND SOMETHING RATHER THAN PASSING.** Silence is the failure here, not the pass.
**ORIGIN: ELIJAH, 2026-09-23.** **SUPPLIED, and its content is derived from G-22 rather than chosen.**
RECORD: D9 group **MR-G3**, one row per sense conductor.
COST AND WHAT IT BUYS: **no instrument and no part.** It is the only thing that converts
G-22 from an intention into a fact.

**D8-19. Repeat D8-18 for the next sense conductor, and start none until the one before
it is ticked.**
SOURCE: C-19.
BEFORE: as D8-18.
ACCEPT: as D8-18. **Disconnect it and the machine becomes more cautious, not less.**
**ORIGIN: ELIJAH, 2026-09-23.**
RECORD: D9 group **MR-G3**.

**D8-20. Confirm every sense conductor D5 lists carries a tick.**
SOURCE: C-19, against D5.
BEFORE: D8-19 exhausted.
ACCEPT: the count of ticks equals D5's count.
RECORD: no figure. Tick only.

**D8-21. Run C-20: watch the watchdog fire.**
SOURCE: C-20.
BEFORE: the watchdog fitted and an external reset input confirmed to exist.
ACCEPT: **it fires, and it does not loop silently.** The row states both and states no
time bound. **If a bound is wanted, it is BOSS's to add to the row.**
RECORD: D9 row **MR-06**.
WHY IT IS HERE AT ALL: **it is the only recovery path P-07 leaves, and a watchdog nobody
has watched fire is the silent reboot-hang-reboot case waiting to happen.**

**GATE 5. Do not start stage 6 until every box in stage 5 is ticked.**

---

## 7. STAGE 6. DRIVERS, HEADS AND THE SEALED BOXES

**MUST BE TRUE BEFORE THIS STAGE STARTS:**
- Stage 4 closed. The rail is set and recorded.
- Drivers wired. Boxes populated and closed, heatsinks fitted. C-13's and C-15's
  blocked-on cells.
  **PRODUCER: PRODUCED, BB-18, BB-35 and BB-36.** Heatsinks are D1 step 14-07 and **are
  not named in BB-18**, which is extended to carry them. Listed in 12.4.
- Jug placement made, and an EN policy at least provisionally chosen. C-06's blocked-on.
  **SEE SECTION 13, DEFECT 4: G-21 froze EN unwired with the drivers defaulting enabled,
  permanently, and three rows still read as though the policy were open.**
  **PRODUCER: jug placement is PRODUCED, BB-16. The EN policy is a DECISION ALREADY
  MADE**, G-21 and D-032, permanently. **Not a state and not open.**
- **P-09's remaining open half** - what a 6121 does with STEP asserted and VM absent -
  **is what C-18 observes.** Rule 9 bars building against an open row. **C-18 builds
  nothing; it is the observation the row says will settle it.**
  **PRODUCER: OPEN ROW, and deliberately so.** This is the one precondition in the
  document that is satisfied by the step rather than before it.

**TRUE AFTER THIS STAGE ENDS:**
- MS1 and MS2 are recorded per driver, as set by pins.
- The standstill current is measured with the EN state it was measured in.
- The rise inside a sealed pump box is measured with the EN state of the idle drivers.
- The permissive-drop state has been entered once, deliberately, under observation.
- The back-siphon question is answered in both energised and de-energised states.

**D8-22. Run C-17 on one driver: record MS1 and MS2 as set by pins, and tick, writing
that driver's identifier beside the tick.**
SOURCE: C-17. **Set by pins and never over UART, per D-075.**
BEFORE: the driver wired, and its configuration already set by PUMP-BOXES. **It must be
set, then recorded, then used, in that order.** How many drivers there are is D5's fact
and `terminal-survey.md`'s.
ACCEPT: the recorded MS1 and MS2 match the pins as they physically sit on that driver.
**Criterion present: it is an identity between what is written and what is set.**
RECORD: D9 group **MR-G4**, one row per driver.

**D8-23. Repeat D8-22 for the next driver, and start none until the one before it is
ticked.**
SOURCE: C-17.
BEFORE: as D8-22.
ACCEPT: as D8-22.
RECORD: D9 group **MR-G4**.

**D8-24. Confirm every driver carries a tick.**
SOURCE: C-17.
BEFORE: D8-23 exhausted.
ACCEPT: the count of ticks equals the driver count in `terminal-survey.md`.
RECORD: no figure. Tick only.

**D8-25. Run C-13: measure the driver standstill current, and record the EN state it was
measured in.**
SOURCE: C-13.
BEFORE: drivers wired, rail set and recorded at D8-16, **and VDD present per whatever
P-09 decides. C-13's own row says this presumes VDD exists while P-09 has not said where
it comes from, and says not to read that as settled.**
ACCEPT: **THE MEASURED TOTAL FOR EIGHT DRIVERS AT STANDSTILL IS AT OR BELOW 2.4 A.**
0.3 A per driver, STANDSTILL_FRACTION at 0.30 against the 1.0 A rated winding current -
**the figure the package assumes.** `parts.md`: "Standstill current has never been
measured and is currently assumed at 30 percent."

**THIS IS A CHECK ON AN ASSUMPTION, NOT A DESIGN LIMIT.** Measure, compare, tick at or
below. **Above 2.4 A: STOP and report the figure rather than continuing.**

**AND THE CONSEQUENCE HAS NOWHERE TO LAND TODAY, WHICH THE OWNER SHOULD SEE BEFORE HE
RUNS IT.** The instruction was to cite MAIN-PANEL's loading model rather than the
owner. **SEARCHED: there is no loading model and no assembled 24 V budget anywhere in
this tree.** What exists is `parts.md` lines 241 to 248 - 1.0 A per driver, 8.0 A worst
case with all eight connected, and a 10 A supply - **which is a worst case nobody will
ever see, because G-06 runs one head at a time. The figure this step measures is the
term that would turn that into a real number, and nothing assembles it.** Section 12.8.
**ORIGIN: ELIJAH, 2026-09-23.** **DERIVED FROM A PART FIGURE: the 1.0 A rated winding current
and the package's own 30 percent assumption.**
consumer is the rail's real load, **and no document read for this checklist holds a rail
load budget for the figure to be judged against.** Owner: **BOSS to say where that
budget lives; MAIN-PANEL owns the rail.**
RECORD: D9 row **MR-07**.
WHY IT MATTERS THAT IT IS MEASURED: `parts.md` records it as never measured and
currently assumed. **T-012: an assumption in that position is correct until the data
moves, with nothing to say when it stopped.**

**D8-26. Run C-15: measure the temperature rise inside a sealed pump box with one motor
running and three idle at standstill current, and record the EN state of the three idle
ones.**
SOURCE: C-15.
BEFORE: boxes populated and closed, heatsinks fitted, lids on.
ACCEPT: **INTERNAL AIR STABILISES AT OR BELOW 60 C**, one motor running and three idle,
**in a room at 18 C. A 42 C rise.**

**The number comes from the components rather than from a preference: the TMC2209's
operating range, the electrolytics beside it, and the PharMed tubing, WHICH SOFTENS
WITH HEAT AND CHANGES DELIVERED VOLUME.**

**Stabilises below 60: tick, and the figure is what PUMP-BOXES judges G-06 against.
Does not stabilise, or exceeds 60: SEQUENTIAL DOSING STAYS MANDATORY, AND THAT IS THE
RESULT RATHER THAN A FAILURE.**

**PUMP-BOXES OWNS THE REAL RATING and supersedes 60 C if it has a tighter one from a
part datasheet. This is a pass mark supplied so the step is runnable. It is not a
specification.**
**ORIGIN: ELIJAH, 2026-09-23.** **DERIVED FROM PART FIGURES, and the softening tubing is the
term that is easy to forget because it is not electrical.**
Owner: **BOSS, with PUMP-BOXES stating the rating the rise is judged against.**
RECORD: D9 row **MR-08**.
COST AND WHAT IT BUYS: **no part.** It is the only measurement that could ever relax
G-06, one pump at a time, which is a THERMAL constraint and not a control preference.
**Sequential dosing is mandatory until this figure exists.**

**D8-27. Run C-18: command STEP with VM removed, and observe the manual-reset
re-application transient.**
SOURCE: C-18.
BEFORE: **read C-18's blocked-on cell first.** P-09 cannot be closed from documentation,
D-070: the datasheet neither allows, forbids nor characterises the state.
ACCEPT: **NO PASS MARK. OBSERVE AND RECORD. THE ONLY FAILURE IS A PART THAT DOES NOT
WORK AFTERWARDS.**

**Running it IS the decision to accept an uncharacterised state on purpose, once, under
observation. THE OWNER HAS TAKEN THAT DECISION, 2026-09-23, and it is recorded as
taken.** The alternative was to remove the state, which reopens D-031.

**What the step produces is an OBSERVATION RECORD rather than a pass or a fail:** what
the drivers do, what DIAG does if anything, whether anything gets warm, **and what the
re-application transient does that is visible.**

**If a driver is dead afterwards, that is the answer and D-031 REOPENS.**
**ORIGIN: ELIJAH, 2026-09-23.** **A DECISION RECORDED, not a criterion. It is in this list so the
set is complete and so nobody later reads the blank as an oversight.**
RECORD: D9 row **MR-09**, which is an observation record and not a figure.
WHY IT EXISTS: **no other row exercises the one state the system enters on every fault
and every shutdown**, and leaves by a human pressing a button at a moment software does
not choose.

**D8-28. Run C-06 energised: jug above the inlet, and observe whether the head holds
against back-siphon.**
SOURCE: C-06. **Two numbers, not one, and this is the first.**
BEFORE: jug placed above the inlet.
ACCEPT: it holds, or it does not. **The row's own two-state answer is the criterion.**
RECORD: D9 row **MR-10**.

**D8-29. Run C-06 de-energised: same arrangement, driver de-energised.**
SOURCE: C-06. The second of the two.
BEFORE: as D8-28. **F-015: a de-energised stepper holds differently from an energised
one**, which is the whole reason this is a second step and not the same one.
ACCEPT: it holds, or it does not.
RECORD: D9 row **MR-11**.
COST AND WHAT IT BUYS, G-48, AND IT IS THE ONE STEP IN THIS DOCUMENT THAT CAN GENERATE
A PART: **if either answer is that it does not hold, C-06's stated consequence is that
flooded suction is unsafe and an anti-siphon device is required.** That is a part, a buy
line and a build step, **arriving after D7 has been used once.** G-47: it is unpriced,
which is not the same as cheap.

**GATE 6. Do not start stage 7 until every box in stage 6 is ticked.**

---

## 8. STAGE 7. WATER AND THE LOOP

**MUST BE TRUE BEFORE THIS STAGE STARTS:**
- **GATE 3 passed: C-24 is done and the tanks were dry when it was done.**
- Tank as built, floats chosen and set, transfer chain live. C-11's blocked-on.
  **PRODUCER: tank as built is PRODUCED, BB-20, BB-24 and BB-27. Floats set is PRODUCED,
  BB-25 and BB-26. TRANSFER CHAIN LIVE is PRODUCED BY STAGE 4 plus BB-30 and BB-35** -
  a chain is live only once the supply is energised, **so its producer was never a D1
  section at all, which is what made the cycle look like one.** F-126.
- Loop plumbed as built, valves in service positions. C-10's and C-07's blocked-on.
  **PRODUCER: loop plumbed is PRODUCED, BB-32. VALVES IN SERVICE POSITIONS IS
  UNPRODUCED** - no build section sets a valve position and no list of service
  positions exists. Listed in 12.4.
- **SEE SECTION 12, CHECK RESULT 2: C-11's blocked-on and D1 section 19 form a cycle.
  This stage cannot start until that is broken at the source.**

**TRUE AFTER THIS STAGE ENDS:**
- The day tank working volume is measured.
- Both ends of the fill band are set, each with its reason.
- The circulation flow at FL-03 is measured under service conditions.
- The loop turnover time exists as a FLOOR for C-02.
- **THE LOOP IS LEFT RUNNING, the day tank is at the HIGH end of the band, and the
  chiller is in NORMAL SERVICE.** **ADDED 2026-09-23, D-231, AT SOURCE UNDER G-54.**
  Stages 8, 9 and 10 each require this and **stage 7's postconditions were four measured
  figures, none of which said the machine was left in a state.** One missing line, met
  three times. **A stage that MEASURES something is not thereby a stage that LEAVES
  something, and only the postcondition can say which.**

**D8-30. Run C-11: measure the day tank working volume.**
SOURCE: C-11.
BEFORE, FOLDED IN BECAUSE IT IS THE MISTAKE THE ROW WAS WRITTEN AGAINST: **the figure on
the parts list is nominal vessel capacity, not a working volume, and must not be used as
one.**
ACCEPT: **NO ACCEPTANCE CRITERION IN THE ROW.** It names no target. Owner: **WATER
states what sets each end; the owner measures.**
RECORD: D9 row **MR-12**.

**D8-31. Run C-11: set the fill band's low end, with the reason.**
SOURCE: C-11.
BEFORE: D8-30 ticked. **The low end is a MEASUREMENT-QUALITY limit as well as a pump
limit: a vortex draws air into the loop, and air past a probe makes the spike that looks
like an early arrival.**
ACCEPT: **NO ACCEPTANCE CRITERION IN THE ROW.** Owner: **WATER.**
RECORD: D9 row **MR-13**, value and reason in separate cells.

**D8-32. Run C-11: set the fill band's high end, with the reason.**
SOURCE: C-11.
BEFORE: D8-31 ticked.
ACCEPT: **NO ACCEPTANCE CRITERION IN THE ROW.** Owner: **WATER.**
RECORD: D9 row **MR-14**, value and reason in separate cells.
WHY THE HIGH END IS TICKED BEFORE STAGE 9 STARTS: **C-02 is measured with the day tank
filled at the HIGH end of the band.** Without this figure stage 9 has no fill condition.

**D8-33. Run C-10: measure circulation flow at FL-03 by catch and time at the return
drop, under service conditions.**
SOURCE: C-10. **The method is in `subsystems/water-s18-f003.md` and is not repeated
here.**
BEFORE, FOLDED IN BECAUSE THESE DECIDE WHETHER THE NUMBER IS REAL: **do not lift the
hose, keep the catch short, and repeat at both ends of the fill band.**
ACCEPT: **NO ACCEPTANCE CRITERION IN THE ROW.** It names no expected flow, and says a
pump curve cannot supply one because the operating point is where the curve meets a
system curve whose every term is open. Owner: **WATER.**
RECORD: D9 row **MR-15**.

**D8-34. Run C-07: establish the loop turnover time, day tank through manifold and
back.**
SOURCE: C-07.
BEFORE: D8-33 ticked, because C-07 is derived from tank volume and circulation flow when
it is not measured directly.
ACCEPT: **NO ACCEPTANCE CRITERION IN THE ROW.** It feeds C-02 as a **FLOOR only**: one
turnover is not mixing to homogeneity, and the multiplier between them is a property of
this tank's mixing that no agent will quote. Owner: **WATER, or the owner measuring.**
RECORD: D9 row **MR-16**.

**GATE 7. Do not start stage 8 until every box in stage 7 is ticked.**

---

## 9. STAGE 8. CHANNEL IDENTITY. THIS IS THE GATE THE WHOLE DOCUMENT TURNS ON

**C-09 IS FIRST AMONG THE MEASUREMENTS. D-022.** Nothing below it is worth measuring
until channel N is proven to be what the wall says it is. **A measurement taken against
a mislabelled channel is not a wrong number, it is a right number filed against the
wrong thing, and every later check confirms it.**

**WHERE THIS DOCUMENT DIFFERS FROM "C-09 IS FIRST", AND WHY:** C-09's own blocked-on
cell is **loop running, tokens applied**, which needs the wet build, the rail, the
drivers and the Pi. **So C-09 cannot be the first step in D8.** It is the first row that
measures anything about a channel, and it gates every row that follows. **Stages 1 to 7
contain no row that touches a channel's identity**, which is what makes that reading
safe. Derived from the rows rather than assumed.

**MUST BE TRUE BEFORE THIS STAGE STARTS:**
- Stage 6 closed and stage 7 closed.
- Loop running. Tokens applied at both ends of every per-channel core, per
  `channel-token.md`.
  **PRODUCER: PRODUCED. Tokens applied, BB-35, which labels every conductor at both
  ends. Loop running, STAGE 7's fourth postcondition, added 2026-09-23 at source.**
- **G-06 serialises the heads, which is what makes this check possible at all.**
  **PRODUCER: RULE.** A standing constraint, not a state. Nothing produces it and
  nothing ends it.

**TRUE AFTER THIS STAGE ENDS:**
- Every channel's head, tube, jug and product are bound, and the binding is written into
  D11, `channel-register.md`.
- Every channel carries an acid, base or salt answer.
- Every channel's role setting is confirmed against the product's actual role.
- The pump box question is answered once across the build.

**D8-35. Command one channel alone and confirm by eye which head turns.**
SOURCE: C-09. **Write the channel token beside the tick.** How many channels there are
is D11's fact.
BEFORE: only that channel commanded. G-06 makes that the normal state.
ACCEPT: exactly one head turns, and it is the head that channel's token names.
RECORD: D9 group **MR-G5**, one row per channel.

**D8-36. Confirm by eye which tube moves.**
SOURCE: C-09. **With translucent tubing this needs no disassembly.**
BEFORE: the same channel still commanded.
ACCEPT: the tube that moves is the one carrying that channel's token at both ends.
RECORD: D9 group **MR-G5**.

**D8-37. Confirm by eye which jug's level drops.**
SOURCE: C-09.
BEFORE: the same channel still commanded.
ACCEPT: one jug's level drops, and it is the jug that channel's token names.
RECORD: D9 group **MR-G5**.

**D8-38. Record which product is in that jug.**
SOURCE: C-09.
BEFORE: the three confirmations above ticked for this channel.
ACCEPT: the product written down matches the label on the jug in front of you.
RECORD: **D11, `channel-register.md`, which is where per-channel product, role and jug
live.** D9 records only that the trace was run, by whom and when. **G-45: the binding
has one home and D9 is not it.**

**D8-39. Answer C-09 question (a) for this channel: is this product an acid, a base, or
a salt solution?**
SOURCE: C-09(a), added by D-106. One line.
BEFORE: D8-38 ticked for this channel.
ACCEPT: the answer is one of those three. **IF IT IS NONE OF THEM, STOP.** D-084
specifies the token carrier against exactly those three duty classes, and its residual
says nothing would detect a product outside them at assignment time. **D-077 makes
assignment time BE commissioning, so this step is that moment.** F-077. Owner of what
happens next: **BOSS.**
RECORD: D9 group **MR-G5**.

**D8-40. Answer C-09 question (b) for this channel: is this channel's role setting -
nutrient, pH-up or pH-down - the role this product actually has?**
SOURCE: C-09(b), added by D-106.
BEFORE: D8-39 ticked for this channel.
ACCEPT: the role setting and the product's actual role are the same. **A wrong role is
worse than a wrong product: it makes the signed check expect the wrong direction, so the
check CONFIRMS the error.** G-32 as amended, D-105.
RECORD: D9 group **MR-G5**, and the role itself in D11.

**D8-41. Repeat D8-35 to D8-40 for the next channel, and start none until the one before
it is ticked.**
SOURCE: C-09.
BEFORE: as D8-35.
ACCEPT: as each of those steps.
RECORD: D9 group **MR-G5**.

**D8-42. Confirm every channel in D11 carries a tick.**
SOURCE: C-09, against `channel-register.md`.
BEFORE: D8-41 exhausted.
ACCEPT: the count of ticks equals the count of channels D11 lists.
RECORD: no figure. Tick only.

**D8-43. Answer C-09 question (c) once across the build: are pH-up and pH-down assigned
to two channels in the same pump box?**
SOURCE: C-09(c), added 2026-09-05 by D-178. **Asked once, not per channel.**
BEFORE: D8-42 ticked, so every role is known. **CH1 to CH4 are in box A and CH5 to CH8
in box B**, so an acid and a base assigned within one group share ONE SEALED ENCLOSURE
AND ONE LID.
ACCEPT: **they are not in the same box.**
RECORD: D9 row **MR-17**.
COST AND WHAT IT BUYS, G-48, STATED BECAUSE THE COST IS ALL IN THE TIMING: **free to
avoid at assignment, expensive to avoid by moving a head.** It sits beside the existing
rule against adjacent tokens and neighbouring colours.

**GATE 8. THIS IS THE ONE GATE NOTHING MAY PASS. Not one step in stage 9 or stage 10
runs until D8-42 and D8-43 are ticked.** C-09 is free, needs no hardware, and is the
ONLY check that catches a build-time labelling error or a numbering disagreement between
software, wiring, head and jug. **Those failures pass every other check in the system.**
S-19 and D-022 both say so, and F-075 says what it costs to run C-01 before this gate.

---

## 10. STAGE 9. THE BASELINE AND THE TIMING

**THE ORDER IN THIS STAGE AND THE NEXT IS NOT FREE AND IT IS NOT MINE.**
`commissioning.md`'s ordering note fixes it: **C-08 first, the baseline band with nothing
happening. C-02 next, using a deliberately OVERSIZED single dose chosen for the clearest
signal. C-03 and C-04 last, at real dose sizes, using the timing established in C-02.**
Timing first with a big dose, magnitudes second with real ones. **The blocked-on column
originally made C-03 and C-04 wait on C-02 alone, which is circular, and DOSING caught
it.**

**MUST BE TRUE BEFORE THIS STAGE STARTS:**
- **GATE 8 passed.**
- Probes live, loop circulating, **no dose in flight** for C-08.
  **PRODUCER: PRODUCED. Probes live, stage 5. Loop circulating, stage 7. NO DOSE IN
  FLIGHT is OPERATOR** - a condition the person running the step holds, produced by no
  section and ended by the next dose.
- Day tank filled at the **HIGH end of the band** set at D8-32, circulation running,
  **chiller in NORMAL SERVICE**, per D-027.
  **PRODUCER: PRODUCED, stage 7** - the band's high end at D8-32, and circulation and
  the chiller in normal service in stage 7's fourth postcondition.
- **SEE SECTION 12, CHECK RESULT 3: C-08's own window length is stated against the
  settling interval, which is C-02's output. That is a cycle and it is not broken here.**

**TRUE AFTER THIS STAGE ENDS:**
- The pH and EC noise and drift band on this build exists.
- t_first and t_settle exist.

### D8-44 AND D8-45 ARE A LOOP. RUN BOTH, IN ORDER, AROUND EVERY WINDOW RUN IN STAGES 9 AND 10

**They are C-23's residual after D-143 reduced it, and they are printed as a loop because
the person holding the stopwatch is the only enforcement.**

**D8-44. Before the window opens, confirm by eye that both day tank pumps are running.**
SOURCE: C-23 as reduced by D-143.
BEFORE: nothing. This is the first thing done in any window run.
ACCEPT: both are seen running now, and you can say they will still be running at the end
of the window.
WHY IT SURVIVED THE REDUCTION: **both day tank pumps run CONTINUOUSLY, so every window
sits inside a running period BY CONSTRUCTION - but "the pump is running" is now an
ASSUMPTION rather than an observation. Nothing commands it, nothing reports it, and
nobody checks it.** A pump that has failed looks exactly like a pump that is running, and
F-102 says nothing else will tell you.
RECORD: a condition cell on the window run's D9 row.

**D8-45. After the window closes, confirm by eye that both day tank pumps were running
for the whole of it.**
SOURCE: C-23.
BEFORE: the window closed.
ACCEPT: both were running throughout. **IF EITHER WAS NOT, THE RUN IS DISCARDED, NOT
ADJUSTED.** G-20's shape, one level up: a run that did not hold its conditions is
discarded.
RECORD: a condition cell on the window run's D9 row, and the word DISCARDED where it
applies.

### The window runs

**D8-46. Run C-08: the pH and EC noise and drift band on this build, in situ, with the
manifold pump running, over a window at least as long as the settling interval.**
SOURCE: C-08.
BEFORE: D8-44 ticked for this run. No dose in flight. **The chiller in normal service,
with its commanded state recorded against every sample, per D-027** - the state is
RECORDED rather than eliminated, so that if the chiller does corrupt a reading the data
will show it.
ACCEPT: **the run's CONDITIONS held, and that is all that can be checked here. THE
FIGURE IS **STRUCTURALLY CRITERION-FREE** AND IS NOT A MISSING CRITERION, D-225: C-08 IS the baseline everything
else is compared against.** Marked N/A with its reason per G-46 rather than left blank.
Owner of that marking: **BOSS.**
RECORD: D9 rows **MR-18** and **MR-19**.
WHY IT CANNOT COME FROM A DATASHEET: pump electrical noise, entrained air and the cable
run all contribute, and datasheet noise is not this loop's noise. **This row was found
independently by CONTROL-SOFTWARE and by DOSING, both reading `commissioning.md`, and
not by BOSS.**
THEN RUN D8-45.

**D8-47. Run C-02: t_first and t_settle, using a deliberately OVERSIZED single dose
chosen for the clearest signal.**
SOURCE: C-02. **The full procedure is in `subsystems/dosing-f004-wet-side.md`.**
BEFORE, AND READ THIS BEFORE OPENING THAT FILE: **F-079. That file gates the settling
timer on the manifold pump being COMMANDED ON, and under G-26 and D-052 no such signal
exists. DO NOT LOOK FOR IT AND DO NOT WAIT FOR IT.** C-23 governs this measurement and
the operator is the enforcement. D8-44 is ticked for this run.
ACCEPT: **the run's conditions held. THE TWO FIGURES ARE STRUCTURALLY CRITERION-FREE AND ARE NOT MISSING CRITERIA, D-225. THEY HAVE NO ACCEPTANCE CRITERION AND
CANNOT HAVE ONE: C-02 DEFINES them.** Marked N/A with its reason per G-46. Owner of that
marking: **BOSS.**
RECORD: D9 rows **MR-20** and **MR-21**.
WHY THE DOSE IS OVERSIZED HERE AND REAL LATER: timing is read off a trace that is
unambiguous. **A check read too early reports a healthy dose as a failure**, and the
tank has no mixer with both short-circuiting and dead zones live at once.
THEN RUN D8-45.

**GATE 9. Do not start stage 10 until D8-46 and D8-47 are ticked, recorded and not
discarded.**

---

## 11. STAGE 10. DELIVERED VOLUME AND DOSE MAGNITUDES

**MUST BE TRUE BEFORE THIS STAGE STARTS:**
- **GATE 8 passed and GATE 9 passed.**
- **C-17 recorded**, stage 6. C-01's blocked-on says C-17 is recorded first.
- Heads mounted, tubing fitted, loop circulating.
  **PRODUCER: PRODUCED throughout. Heads mounted, BB-18. Tubing fitted, BB-33, section
  32a. Loop circulating, stage 7.**
- **F-075 SETTLED. D-102 attached that deadline to C-01 and it is the first step of this
  stage.**

**TRUE AFTER THIS STAGE ENDS:**
- Delivered volume per revolution and per step exists for every channel.
- The pH step per single dose exists for pH up and for pH down, each SIGNED.
- The EC step per single dose exists for every EC-moving channel.

**D8-48. Confirm F-075 is settled before C-01 is run on any channel.**
SOURCE: C-01's blocked-on cell, gated 2026-09-03 by D-102.
BEFORE: nothing commanded.
ACCEPT: `findings.md` F-075 is closed, both halves: **`software-spec.md` 3.4 states how a
channel leaves OUT OF SERVICE, and 5.2's admission check includes C-09.**
**BLOCKED TODAY. Missing: F-075 is open.** Owner: **CONTROL-SOFTWARE**, with the deadline
D-102 attached.
WHY THIS IS A GATE AND NOT A NOTE: **before C-01 runs, a channel measured against the
wrong channel is a mistake. After it runs, it is a dated entry in
`channel-register.md` with a procedure behind it, indistinguishable from data, and G-05
decrements a jug against it forever.**
RECORD: no figure. Tick only.

**D8-49. Run C-01 on one channel: delivered volume per revolution and per step, measured
against REAL BACK PRESSURE into the running manifold.**
SOURCE: C-01. **Write the channel token beside the tick.**
BEFORE: D8-48 ticked. The manifold running, so the back pressure is the real one.
**G-04: nothing in this system measures delivered volume, so a wrong figure here is
invisible.**
ACCEPT: **TWO CONDITIONS, BOTH DECIDABLE AT THE BENCH.**

**1. The measured volume per revolution is BELOW the manufacturer's no-back-pressure
figure.** C-01 already names the direction: back pressure can only reduce delivery, **so
a figure at or above the catalogue figure means the measurement is wrong**, not that the
pump is good.

**2. The eight channels agree with each other within 5 PERCENT.** Eight identical heads
on eight identical drivers into one manifold should agree within a few percent. **A
channel 15 percent off its siblings has a tube seated wrong, a head not clamped, or a
driver at a different current.**

**The second condition is the one C-01 does not have and it is worth more than the
first**, because the first only catches a bad measurement and the second catches a bad
build.
**ORIGIN: ELIJAH, 2026-09-23.** **CONDITION 1 IS DERIVED from C-01's own stated direction.
CONDITION 2's 5 PERCENT IS CHOSEN, WITH NO EXTERNAL BASIS, and the owner says so:
tighten it after the first full set if the real spread is tighter.**

**The row's original note stands:** C-01 names a
DIRECTION only: the manufacturer's per-revolution figure is specified at NO back
pressure, so the real figure is lower, in a known direction, by an amount nobody has
measured. **A measured figure at or above the no-back-pressure figure is the one thing
the row lets you call wrong.** Owner of a tolerance, if one is wanted: **BOSS.**
RECORD: D9 group **MR-G6**, one row per channel, two value cells.

**D8-50. Repeat D8-49 for the next channel, and start none until the one before it is
ticked.**
SOURCE: C-01.
BEFORE: as D8-49.
ACCEPT: as D8-49. **Below the catalogue figure, and within 5 percent of its
siblings.** **ORIGIN: ELIJAH, 2026-09-23.**
RECORD: D9 group **MR-G6**.

**D8-51. Confirm every channel in D11 carries a C-01 tick.**
SOURCE: C-01, against `channel-register.md`.
BEFORE: D8-50 exhausted.
ACCEPT: the count of ticks equals the count of channels D11 lists.
RECORD: no figure. Tick only.

**D8-52. Run C-03 for pH up: the pH step per single dose, at a real dose size, and
record its SIGN.**
SOURCE: C-03.
BEFORE: D8-44 ticked for this run. The timing established at C-02 is in hand.
ACCEPT: **the measured step exceeds the noise and drift band recorded at D8-46**, which
is the row's own criterion: the attribution must exceed probe noise and drift to mean
anything. **And the sign is recorded, because the measured step IS the reference sign for
S-16's direction check, per D-083 and G-32. THE SIGN COMES FROM THIS MEASUREMENT AND
NEVER FROM A PRODUCT NAME.**
RECORD: D9 row **MR-22**.
THEN RUN D8-45.

**D8-53. Run C-03 for pH down: the pH step per single dose, at a real dose size, and
record its SIGN.**
SOURCE: C-03. **Separately, which is why it is a second step.**
BEFORE: D8-44 ticked for this run.
ACCEPT: as D8-52.
RECORD: D9 row **MR-23**.
THEN RUN D8-45.

**D8-54. Run C-04 on one EC-moving channel: the EC step per single dose.**
SOURCE: C-04. **Write the channel token beside the tick.**
BEFORE, AND IT IS FOLDED IN BECAUSE IT CHANGES WHICH CHANNELS YOU RUN: **"EC-moving" is
an ASSUMPTION, not a measurement, D-107.** D-013 asserts fulvic moves neither EC nor pH
meaningfully and no measurement is named for it anywhere, **so this scope excludes from
the only measurement that could falsify the assumption whichever channel carries fulvic,
and the premise is UNTESTABLE BY CONSTRUCTION.** Per D-122 **there is no fulvic channel**:
fulvic is a PRODUCT attribute bound at C-09, so which channel this scope excludes is not
knowable until GATE 8 has passed. **The decision stands, fulvic stays unattributed, and
the premise is marked unmeasured rather than quietly treated as tested.** D8-44 ticked
for this run.
ACCEPT: **the measured step exceeds the band recorded at D8-46.** Same criterion as
C-03, and the row says so.
RECORD: D9 group **MR-G7**, one row per EC-moving channel.
THEN RUN D8-45.

**D8-55. Repeat D8-54 for the next EC-moving channel, and start none until the one
before it is ticked.**
SOURCE: C-04.
BEFORE: as D8-54.
ACCEPT: as D8-54.
RECORD: D9 group **MR-G7**.

**D8-56. Confirm every channel D11 records as EC-moving carries a tick.**
SOURCE: C-04, against `channel-register.md`.
BEFORE: D8-55 exhausted.
ACCEPT: the count of ticks equals the count of EC-moving channels D11 lists.
RECORD: no figure. Tick only.

**GATE 10. When every box above is ticked, copy every figure into D9,
`maintenance-record.md`. Nothing that later wants one of these figures reads this page:
it reads D9.**

---

## 12. THE SEQUENCE CHECK, RUN ON THIS DOCUMENT

**G-50: every stage states what must be true before it starts and what is true after it
ends, so a stage requiring X comes after the stage producing X. This is the result of
running that comparison.** Preconditions only, because that is all this check reads, and
**F-116 is the standing warning that a dependency living in prose is invisible to it.**

### 12.1 Every stage's precondition, matched

| Stage | Requires | Produced by |
|---|---|---|
| 1 | D1 section 13, D1 section 15 | D1, before commissioning |
| 2 | F-106 closed, BB-35, D1 31-02, stage 1 | D1, stage 1 |
| 3 | stage 2, tanks dry, pull-downs fitted, V_IL known | stage 2; **pull-downs and V_IL NOT PRODUCED, see 12.3** |
| 4 | stage 2, stage 3, **C-16's own "nothing else on the rail"** | stage 2, stage 3; **the last is UNMATCHED, see 12.2** |
| 5 | stage 4, sense circuits built, Pi reading, watchdog fitted, external reset confirmed | stage 4; **the last two NOT PRODUCED, see 12.3** |
| 6 | stage 4, boxes closed and heatsinked, jugs placed, EN policy | stage 4, D1; **EN policy already frozen by G-21, see section 13 defect 4** |
| 7 | GATE 3, tank as built, floats set, transfer chain live, loop plumbed | stage 3, D1; **CYCLE, see 12.2** |
| 8 | stage 6, stage 7, loop running, tokens applied | stages 6 and 7, `channel-token.md` |
| 9 | GATE 8, probes live, no dose in flight, high end of band, chiller in service | stage 8, stage 7 (D8-32); **the window length is CIRCULAR, see 12.2** |
| 10 | GATE 8, GATE 9, C-17 recorded, F-075 settled | stage 8, stage 9, stage 6 (D8-22); **F-075 NOT PRODUCED, see 12.3** |

**Every stage-to-stage dependency is satisfied by an EARLIER stage. No stage in this
document depends on a later one.**

### 12.2 The three defects the check found in the ORDER itself

**1. C-16's PRECONDITION IS UNMATCHED BY ANY STATE THE BUILD PRODUCES.** C-16 says to
measure the trim **"before anything else is connected to the rail"**. D1 section 31 lands
**every** conductor in D5 and ends at BB-35, and D8's own first-stage prerequisite is
that every wire is landed. **There is no moment in the build order where the supply is
powered and nothing else is on the rail.** `commissioning.md` records C-22 as sitting
awkwardly against this same phrase and calls that tension deliberate; **it does not
record the tension with the build order, and that is a different one.** Not resolved
here. Owner: **BOSS**, at C-16's blocked-on cell.

**2. A CYCLE BETWEEN C-11 AND D1 SECTION 19.** C-11's blocked-on requires **the transfer
chain live for the surge measurement**. The transfer chain is live only after D1 section
31, which requires BB-27 from section 23, which requires BB-24 and BB-26 from sections 20
and 22, **all three of which require BB-23 from section 19 - and section 19 is BLOCKED on
C-11.** D1 section 34.2 records a candidate cycle on C-11 and breaks it on a different
term, the fill band against the float marks. **The surge term is not addressed by that
break and the cycle survives through it.** Not resolved here. Owner: **BOSS**, at C-11's
blocked-on cell, with WATER.

**3. C-08'S WINDOW LENGTH IS CIRCULAR AGAINST C-02.** C-08 is to be measured **"over a
window at least as long as the settling interval"**. The settling interval is C-02's
output, and the ordering note puts C-08 **first**, before C-02. **C-07 exists and gives
C-02 a FLOOR, but no row says C-07 may set C-08's window.** The ordering note broke the
C-02 against C-03 and C-04 circularity and left this one. Not resolved here. Owner:
**BOSS**, at C-08's row.

### 12.3 Preconditions nothing in the build produces today

Each is a blocker rather than an ordering defect, and each is named on its step.

| Precondition | Stage | Owner |
|---|---|---|
| **F-106 closed.** Nobody has read a terminal | 2, and it blocks all 127 of D4's joints | D1 section 4, `terminal-survey.md`. One evening with the parts and a pen |
| **Pull-downs fitted at the driver end** | 3 | PUMP-BOXES, under D-043. D5 records them as an owed fix, not a fitted part |
| **V_IL known from the datasheet** | 3 | The owner's lookup, G-15 |
| **S-12 frozen.** It is an OPEN row and every stage 5 step needs the Pi reading a pin | 5 | DISPLAY-BOX proposes, CONTROL-SOFTWARE builds against it, BOSS freezes |
| **An external reset input exists at all** | 5 | DISPLAY-BOX |
| **P-09's remaining open half** | 6 | It is what C-18 observes, and running C-18 is the decision |
| **F-075 settled** | 10, and it gates C-01 absolutely | CONTROL-SOFTWARE, deadline attached by D-102 |
| **S-01, S-02 open**, so no float is chosen and no float position can be named by a printed identifier | 3 and 7 | WATER |

### 12.4 Postconditions nothing later consumes

**Three, and only one of them is a defect.**

- **C-05's figure.** Consumed by nothing, and that is correct: the row says it is only
  needed if a pressure-based option is ever chosen, and it is **NOT SCHEDULED**.
- **C-18's observation.** It produces a decision rather than a figure, and the decision is
  its own consumer. Correct.
- **C-13's standstill current. THIS ONE IS A DEFECT.** The row names its consumer - the
  standstill figure is what sets the rail's real load - **and no document read for this
  checklist holds a rail load budget for it to land in.** `parts.md` holds the assumption
  it replaces. Owner: **BOSS** to say where the budget lives.

### 12.6 THE PRODUCER PASS, 2026-09-23, D-229. THIS SECTION IS NOW MACHINE-CHECKED.

**Every precondition in this document carries a PRODUCER tag naming what makes it true,
or naming the reason nothing does.** `tools/cross-document-check.py` reads them and
builds one graph across D1, D8 and D4.

| Kind | Count | Meaning |
|---|---|---|
| **PRODUCED** | **17** | A section makes it true. The tag names the id |
| **UNPRODUCED** | **7** | **Nothing in the build makes it true. These are the real gaps** |
| OPEN ROW | 2 | Closed by agents agreeing an interface, not by a build step |
| INVARIANT | 2 | True from the start. **The tag names what ENDS it, not what starts it** |
| LOOKUP | 1 | A fact from outside the build. G-15 |
| RULE | 1 | A standing constraint. Nothing produces it and nothing ends it |
| OPERATOR | 1 | Held by the person running the step |
| DECISION | 1 | Already made and frozen |
| **UNTAGGED** | **0** | |

**WHAT THE CHECK FOUND ONCE IT COULD SEE: ONE CROSS-DOCUMENT CYCLIC CLUSTER, FOURTEEN
SECTIONS WIDE.**

    D1 19, 20, 21, 22, 23, 24, 25, 27, 28, 30, 31 and D8 stages 2, 3 and 7

**21 distinct paths run round it and they are one defect.** Section 12.2's check result
2 named three of those fourteen. **The direction was right and the size was wrong by
eleven sections, which is T-031 exactly.**

**The arc that closes it was invisible until it was written down.** D1 section 19's
dependency on C-11 lived in a BLOCKED note, and G-50 reads only preconditions. It is
now a precondition.

### 12.7 THE SEVEN GAPS. NOTHING IN THE BUILD MAKES THESE TRUE

| # | State required | Stage | Who |
|---|---|---|---|
| 1 | **The watchdog fitted, and an external reset input confirmed to exist** | 5 | **DISPLAY-BOX. `build-book.md` contains no occurrence of "watchdog". NO BUILD SECTION FITS IT, and a stage requires a part the build never installs** |
| 2 | **Valves in service positions** | 7 | **WATER. No section sets a valve position and no list of service positions exists anywhere** |
| 3 | **The loop left running** | 8, 9, 10 | **Three stages need it and stage 7's postconditions are four measured figures, none of which is "the loop is left running." One missing postcondition, met three times** |
| 4 | **Circulation running, chiller in NORMAL SERVICE** | 9 | As 3 |
| 5 | **The supply powered with nothing else on the rail** | 4 | **F-125: the requirement contradicts its own reason and wants inverting, not relaxing. Owner** |
| 6 | **No dose in flight** | 9 | **OPERATOR, not a gap in the build. Listed so it is not mistaken for one** |
| 7 | **Loop circulating** at stage 10 | 10 | As 3 |

**Three of the seven are ONE missing postcondition on stage 7.** Adding it is a
one-line fix and it is INTEGRATOR's, not BOSS's - **G-54: the fact enters at the stage
that produces it.**

**Two are real absences in D1: a part nobody installs, and a valve state nobody sets.**
Both routed.

### 12.8 THREE SAFE DIRECTIONS THAT ARE NOT STATED, AND ONE BUDGET THAT DOES NOT EXIST

**Produced by writing D8-18's acceptance criterion, 2026-09-23, D-231. The owner's
instruction: if any conductor's safe direction is not stated, that is a gap and it comes
to him rather than being guessed at the bench.** Searched the interface table, G-22,
G-27, G-29 and D-049.

| Conductor | Safe direction | State |
|---|---|---|
| **S-03 NC leg**, fill in progress | Severed reads as FILLING, dosing inhibited | **STATED.** D-042 |
| **S-03 NO leg**, dose inhibit | Complement of the above on the same pole | **STATED by construction.** G-27: any state where both agree is a broken sense path |
| **S-08**, the 22.32 readback | Severed leaves the Pi input high, reads contact open, reads a drop | **STATED, and named as a CHOSEN property rather than an inheritance** |
| **S-20 and its complement leg**, K-DRY | **OPEN ON LOSS. A severed readback reads as NOT PULLED IN.** The readback tells the controller whether the contactor answered its coil, **and the alternative is a controller that believes motor power is present when it is not** | **ANSWERED 2026-09-23 by the owner, D-233, and written onto the row.** It was established-but-unstated, G-37's shape |
| **S-04**, the leak console's Form C legs | **C-NC: OPENS on power loss OR on leak.** A dead console and a wet floor do the same thing, so the unsafe case does not exist | **STATED.** F-115, closed by the owner and recorded in D5 section 6 |
| **S-11**, the probe conductors | **AN UNREADABLE PROBE STOPS DOSING.** A probe that fails to respond on the bus raises a fault, **the fault is LATCHING, and no batch may start or continue while it is raised.** Not a fallback, not a last-known value, not a default: **the dose divides by a measurement, and a measurement that does not exist cannot be substituted for** | **ANSWERED 2026-09-23 by the owner, D-233. CONTROL-SOFTWARE's to implement.** G-22's frame does not fit it. A severed I2C conductor is not a two-state loop failing in a direction - **it makes a probe unreadable, and whether unreadable INHIBITS dosing is a software question. Searched `software-spec.md`: no row says what an unreadable probe does** |

**D8-18 disconnects at the GLAND, and S-11's probe cable is the most likely conductor a
person reaches for there.** So gap 2 is not academic: **it is the first conductor the
step will meet.**

**AND A THIRD ENTRY WAS WRITTEN HERE AND WITHDRAWN BEFORE IT WAS SENT.** S-04 was listed
as a gap on the strength of **G-39's own annotation, which still reads "what the contact
does when its own 24 V fails is on file nowhere."** It is not: **F-115 closed it and the
owner answered it - C-NC, opens on power loss or leak.** G-39's annotation is STALE and
is the thing to fix.

**G-38's shape on a rule instead of on a grade: the annotation was true against the tree
it was written on, and it reads today as a live absence.** A rule that carries its
founding example keeps that example after the example is closed, **and the rule is the
last place anybody looks for a stale fact.** G-39's annotation is corrected; **the rule
itself is unchanged and was never wrong.** D-231.

### 12.9 AND THE CONSEQUENCE OF D8-25 HAS NOWHERE TO LAND

**The owner's criterion for D8-25 is a check on an assumption: 2.4 A total at
standstill, and "if the measured figure exceeds it, every branch loading figure keyed to
it moves." His instruction was to cite MAIN-PANEL's loading model.**

**SEARCHED `parts.md`, `subsystems/main-panel*.md` and `decisions.md` for a rail load
budget, a loading model or an assembled 24 V total. THERE IS NONE.**

**What exists is `parts.md` lines 241 to 248:** 1.0 A per driver, **8.0 A worst case
with all eight connected**, and a 10 A supply. **That worst case will never occur,
because G-06 runs one head at a time.** The real figure is one running plus seven at
standstill, **and the standstill term is exactly what D8-25 measures.**

**So the step measures the one term that would turn a worst case nobody will see into a
number somebody could use, and nothing assembles it.** MAIN-PANEL's, and it is the
fourth ordering defect from D-222 arriving with a number attached.

### 12.11 THE WATCHDOG IS SPECIFIED AT ONE END ONLY. ROUTED 2026-09-23, D-231

**The owner asked plainly whether the watchdog is a part, a software mechanism, or
something assumed and never specified. SEARCHED THE WHOLE TREE. The answer is the third,
and it is more specific than that.**

| What the tree says | Where |
|---|---|
| **How it is FED** | **D-033 and `software-spec.md` 2.4.10: from the sequencer and state loop, NEVER from an independent timer thread.** A timer that keeps ticking while the sequencer is wedged passes forever and hides exactly what it names |
| **Why it exists** | **P-07: nothing in the panel can power cycle the Pi.** It reboots by software or by killing the panel, **so a watchdog is the only recovery path from a hang** |
| **That it must not resume anything** | **G-16 has no crash exemption.** A watchdog reset may not resume a batch |
| **Whose it is** | **P-07: "The watchdog is CONTROL-SOFTWARE's and DISPLAY-BOX's"** |
| **WHAT IT DRIVES** | **NOTHING. NO FILE.** Not a part, not a pin, not a Pi facility, not a mechanism |

**SO IT IS NOT "A PART THE BUILD NEVER INSTALLS", WHICH IS HOW I REPORTED IT LAST TURN.
IT IS A MECHANISM SPECIFIED AT ITS INPUT AND NOT AT ITS OUTPUT.** D1 installs nothing
because there may genuinely be nothing to install - **or because nobody chose. Those are
different answers and the tree cannot tell them apart.**

**THE WORD "FITTED" IN THIS STAGE'S PRECONDITION IS WHERE IT SHOWS.** "Fitted" reads as
a part. **Everything on file describes software. Nobody noticed because each end was
written by the agent that owned its own end, and neither wrote the join.**

**ROUTED TO DISPLAY-BOX AND CONTROL-SOFTWARE JOINTLY, with the question stated so it
cannot be answered halfway:**

1. **What does the watchdog ACT ON when the feed stops?** A facility the Pi already has,
   a part on the display box plate, or nothing yet chosen.
2. **If it is a part, it is a D7 line, a D1 step and a D3 position, and none of the three
   exists.**
3. **C-20's other half - "confirmation that an external reset input exists at all" - is
   the same question asked from the other side**, and it has been sitting in a blocked-on
   cell as though somebody were going to look it up.

**IF NOBODY CHOSE, THAT IS A DECISION AND IT GOES TO THE OWNER**, per his instruction.
**It is not a lookup: which recovery path this machine has is a design choice, and the
only reason it looks like a lookup is that the question was never asked out loud.**

### 12.12 VALVE SERVICE POSITIONS. ROUTED TO WATER, 2026-09-23, D-231

**Stage 7 requires "valves in service positions". NO BUILD SECTION SETS A VALVE
POSITION AND NO LIST OF SERVICE POSITIONS EXISTS ANYWHERE IN THIS TREE.**

**Same shape as the watchdog and it is the owner's word for it: a plumbing document
nobody has asked for.** The valves exist - D1 sections 24 to 28 fit them - **and what
each one's position IS during normal service is on file nowhere.**

**WATER's, and what is wanted is one line per valve: its name, its position in normal
service, and what changes it.** The last term is the one that makes it worth having:
**a valve whose service position nobody wrote down is a valve the next person leaves
where they found it.**

**It is not blocked on the wall, on the survey or on anything the owner is measuring.**

### 12.5 What this check cannot see

**F-116's lesson, restated because it applies to this document too: this check reads
PRECONDITIONS.** A dependency stated in a step's prose and not lifted into a stage
precondition is invisible to it. **This document was swept once for that on writing, and
a builder read will still find things this check cannot.** Three dependencies were found
sitting in prose during that sweep and are now stage preconditions: C-24 before water,
C-17 before C-01, and C-11's high end before C-02's fill condition.

---

## 13. WHAT IS WRONG IN `commissioning.md`, REPORTED AND NOT FIXED HERE

**G-54: a fact enters at the source, never at the view. Every item below is a defect in
the register and each is routed rather than patched on this page.** Owner of the file is
BOSS.

**1. C-24 contradicts itself inside one row.** Its measurement cell says **"Prove every
float's FAIL DIRECTION with a meter and a hand"** and its reason cell says **"No
instrument needed and no hardware added"**. A meter is an instrument. **A commissioner
reading the second sentence will not bring one.** The row also does not say whether the
panel is energised for the test, and "conductors and coils" can be read either way.

**2. C-16's precondition cannot be satisfied by the build order.** Section 12.2, item 1.
The row records the tension with C-22 and not the one with BB-35.

**3. C-11's blocked-on closes a cycle with D1 section 19.** Section 12.2, item 2. **The
row bundles two measurements with different preconditions - the working volume and band,
and the surge - under one blocked-on cell, and it is the surge term that closes the
cycle.**

**4. THREE ROWS TREAT THE EN POLICY AS STILL OPEN AND G-21 FROZE IT PERMANENTLY.** C-06's
blocked-on asks for **"an EN policy at least provisionally chosen"**; C-13 asks for
**"the EN state it was measured in"**; C-15 asks for **"the EN state of the three idle
ones"**. **G-21: EN stays unwired and the drivers default enabled, permanently, D-032.**
The cells are not wrong to want the state recorded, but the C-06 cell reads as a blocker
that closed a year of decisions ago. **A blocker that is already closed reads as an open
question and gets asked for twice. G-35's shape.**

**5. C-23 NAMES C-12 AS A ROW IT APPLIES TO, AND C-12 IS VOID.** C-23's applies-to cell
lists "C-02, C-03, C-04, C-08, C-12". C-12 is **VOID 2026-09-04 by D-143**, struck with
its reason and correctly kept visible. **A void row named as a live consumer in another
row's cell is the kind of thing a reader resolves by running the void row.**

**6. NOTHING SCHEDULES RECORDING THE AS-SET VREF.** C-22 requires Vref to be set with VS
present, per driver. **No C- row records the value.** C-16's own argument applies word for
word - a rail nobody recorded is a rail nobody can check later - **and Vref sets the
current in eight motors.** **D9 has no row for it, deliberately**, because adding one
would put the view ahead of its source. Owner: **BOSS**, as a row in `commissioning.md`
or as an explicit decision that it is not recorded.

**7. C-23's HEADLINE AND ITS BODY DISAGREE IN ONE CELL.** The cell opens in bold with the
rule that the window **"MUST NOT SPAN A START OR A STOP"** and then says most of that
dissolved when D-143 made both day tank pumps run continuously. **A reader who reads the
bold opening and stops carries away the withdrawn half.** T-022's shape: a withdrawn
claim filed under a surviving claim's label. **The residual that survives is real and is
what D8-44 and D8-45 run.**

**8. C-08 does not say whether the noise and drift band is ONE figure per probe or TWO.**
It says "noise and drift band" for pH and EC. **D9 gives one row per probe and says so,
and if it should be four rows that is the register's to say.** Owner: **BOSS.**

**Two things that are GAPS rather than defects, logged and not stopped for**, per BOSS's
working rule 1: C-21 does not say whether VDD is present for the measurement, and C-20
states no time bound on "does not loop silently".

---

## 14. WHAT TO DO WHEN A STEP FAILS

**THERE IS NO FAULT-FINDING TABLE IN THIS DOCUMENT AND THAT IS DELIBERATE.** The old set
carried one. **Not one C- row in `commissioning.md` states a diagnosis, so a
fault-finding table written here would be facts entering at the view. G-54.** What
follows is only the disposal rules the rows themselves state.

| When this happens | What the source says to do | Where it says it |
|---|---|---|
| A window run's pumps were not running throughout | **DISCARD the run. Do not adjust it** | C-23, and G-20's shape one level up |
| Any run that turned a head did not complete | **DISCARD it. Do not scale it** | G-20 |
| C-09(a) returns a product that is not an acid, a base or a salt solution | **STOP.** D-084's carrier specification is invalidated and nothing else detects it | C-09(a), F-077 |
| C-09(b) returns a role that does not match the product | **STOP.** The signed check will confirm the error rather than catch it | C-09(b), G-32, D-105 |
| C-09(c) returns pH-up and pH-down in one pump box | Fix it **at assignment**. Moving a head is the expensive route | C-09(c), D-178 |
| A step's ACCEPT line says NO ACCEPTANCE CRITERION | **Record the figure, tick nothing as passed, and route to the owner named on the step** | G-46: a cell that can never be filled must not look like one not filled yet |
| A step is BLOCKED | Leave it in place, do not substitute and do not skip ahead | D4's rule, and rule 9 |
| A check reports no movement during a dose | **The batch STOPS and tells the operator. Software never re-doses, tops up, retries or corrects** | G-16 |
| The operator's instinct is to command the opposing pH channel | **Do not.** That is the forbidden correction a louder alarm invites | G-16a |

---

## 15. WHAT THIS DOCUMENT DOES NOT COVER

- **Any measurement, threshold, target or tolerance.** Every one is a C- row's, and where
  a row has none this page says so instead of supplying one.
- **Any build step.** Nothing here mounts, fits, cuts or lands anything. That is D1, D4
  and D6.
- **Any conductor, terminal or landing fact.** Stage 2 checks against D5 and D2 and
  restates neither.
- **Per-channel product, role, jug or cable core.** That is D11, `channel-register.md`,
  written at C-09 and updated for the life of the build. **D9 records that the trace was
  run; D11 records what it bound.**
- **Any quantity, count or price of a thing the build contains.** D7 is the only document
  in this set where those live. **Where this document needs a count it names whose fact it
  is - D5's, D11's, D2's roster's - and does not restate it.**
- **The add-on commissioning block the old set carried.** There is no add-on package in
  this set, so there is no supplement and G-41 does not arise here.

---

## 16. STATUS

**Stopped part way. INTEGRATOR does not declare this finished**, rule 7. That waits until
somebody works a stage from it and finds nothing.

**Eleven stages, ten gates, 56 numbered steps.** All 25 C- rows in `commissioning.md` are
accounted for: **23 are run by a step, C-05 is NOT SCHEDULED and C-12 is VOID**, and both
appear in D9 marked N/A with their reason rather than omitted, per G-46.

**NINE OF THE 56 STEPS STILL CARRY NO ACCEPTANCE CRITERION, 2026-09-23, D-231.** It was twenty. **Two - D8-46 running C-08 and D8-47 running C-02 - ARE STRUCTURALLY CRITERION-FREE AND ARE MARKED AS THAT RATHER THAN AS MISSING, D-225:** they DEFINE the figures every other step is judged against, so there is nothing to judge them by. **Nine were BOSS's and the owner supplied SIX CRITERIA COVERING ALL NINE on 2026-09-23, each marked ORIGIN: ELIJAH with the derived ones distinguished from the chosen ones, per G-53.** **The nine that remain are PUMP-BOXES', WATER's and the owner's lookups**, each saying so on its own ACCEPT
line with its owner named. **Eighteen of those are rows that owe a criterion. Two are
structurally criterion-free** - C-08 and C-02 define the figures everything else is
compared against, and there is nothing behind them to compare to.

**NOT ONE STAGE CAN BE RUN TODAY.** Stage 2 is blocked on F-106, stage 3 on the
pull-downs and V_IL, stage 5 on S-12, stage 7 on the C-11 cycle, stage 10 on F-075, and
stages 3 and 7 on S-01 and S-02. **Stage 1 is the closest to runnable: it needs only the
parts and the plate.** The document is written with its blocked steps carrying real ids
and saying what blocks them, per rule 9 and D-142's precedent, **because a schedule of
blocked rows with real ids is a document and a schedule waiting for everything to close
is not.**

**What would move the most, in order, and it is a count rather than a characterisation,
per T-031:**

1. **F-106.** One evening with the parts and a pen. It unblocks stage 2 entirely and 61
   of D4's 127 joints.
2. **F-075.** One CONTROL-SOFTWARE pass. It is the only thing between GATE 8 and the four
   figures in stage 10 that G-05 will decrement a jug against forever.
3. **The C-11 cycle**, section 12.2 item 2. It blocks stage 7, and stage 7 blocks stages
   8, 9 and 10, which is six of the eleven stages.
4. **The eight defects in section 13**, none of which needs a purchase or a measurement.
