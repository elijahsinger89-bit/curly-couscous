# D9. Baseline and maintenance record

**The form. Written 2026-09-23 by INTEGRATOR, with D8.**

---

## THIS DOCUMENT IS EMPTY BY DEFINITION. IT IS NOT UNWRITTEN

**Every value cell below is empty because commissioning has not run. That is the only
reason, and it is a different thing from a cell nobody has got to yet.** G-46: a cell
that can never be filled must not look like one that has not been filled yet, and the
same distinction applies to a whole document. **D9's form is written with D8. D9's
content cannot exist until D8 has run.**

**So: do not read an empty cell here as a gap in the design, do not fill one from a
datasheet, and do not treat this file's emptiness as a sign that work is outstanding
anywhere but at the bench.** The only thing that fills it is a person with a meter
working D8, `commissioning-checklist.md`.

**Three kinds of empty appear below and they are marked differently:**

| Mark | Means |
|---|---|
| **blank** | **EMPTY BY DEFINITION.** Waiting for the D8 step named in its row. This is almost every cell |
| **N/A, with a reason** | **CAN NEVER BE FILLED.** The row is void or not scheduled. It stays visible with its reason rather than being deleted. G-46 |
| **NO CRITERION** in the Measured against column | The C- row states no success criterion, so there is nothing to compare the figure to. **The owner of that absence is named in the row.** It is not an invitation to supply one here |

---

## 1. WHAT THIS DOCUMENT IS FOR

**Everything in this build that consumes a measured figure cites D9 and never a
datasheet.** That is the whole job. `document-plan.md` section 3.2: a measured RESULT
lives in D9, once.

**It is filled once at handover and returned to for the life of the machine.** The
baseline is section 3. Section 5 is the log that runs forever.

**IT HOLDS NO REASONING.** Why a figure is needed is its C- row's, in
`commissioning.md`. Why the machine is the way it is belongs to `decisions.md`,
`findings.md` and `traps.md`. **No delivered document in this set carries reasoning.**

**IT HOLDS NO PER-CHANNEL BINDING.** Product, role, jug and cable core are D11's,
`channel-register.md`, which is written at C-09 and updated at every jug change and every
rewire. **D9 is filled once and D11 is not. Different lifetimes, different reader
moments.** D9 records that the C-09 trace was run, by whom and when; **D11 records what
it bound.** G-45: one home per fact.

**IT ADDS NO ROW OF ITS OWN.** Every row below exists because a C- row in
`commissioning.md` produces the figure, or because the re-measure trigger table names the
event. **Where a figure is set during commissioning and no C- row schedules recording it,
THERE IS NO ROW HERE.** One such figure exists today and it is named in section 6, so
that its absence is not read as an oversight. **G-54: a fact enters at the source, never
at the view, and a view that is ahead of its source is no longer a view.**

---

## 2. HOW TO FILL A ROW

**Fill every column. A figure without its conditions is not a figure.**

| Column | What to write |
|---|---|
| **Value** | The number, or the observation, as measured |
| **Units** | As you read them off the instrument. **Do not convert** |
| **Date** | The day the measurement was taken, not the day it was written up |
| **By** | The person who held the instrument |
| **Measured against** | What the value was compared to, or **NO CRITERION** where the row says so. **Never a datasheet** |
| **Conditions** | What the C- row requires to be recorded alongside. The chiller's commanded state, the EN state, the fill level, the run's completion |
| **D8 step** | Pre-printed. The step that produced it |
| **Voided** | Left blank until a re-measure trigger fires, then dated and pointed at the log entry in section 5 |

**A run that did not hold its conditions is DISCARDED, not adjusted, and the discarded
run is still written down.** G-20, and C-23's own discard rule. **Write DISCARDED in the
Value cell with the reason in Conditions, and take the run again on a new row.** A
discarded run nobody recorded is a run somebody repeats without knowing why.

---

## 3. THE BASELINE. FILLED ONCE, AT COMMISSIONING

**Twenty-five fixed rows and seven per-item groups.** Every figure `commissioning.md`
schedules appears exactly once.

### 3.1 Fixed rows

| Row | Figure | C- row | D8 step | Value | Units | Date | By | Measured against | Conditions | Voided |
|---|---|---|---|---|---|---|---|---|---|---|
| **MR-01** | Continuity across the main panel inter-bar jumper | C-25 | D8-01 | | | | | Continuity, per the row | Nothing else landed on either bar; plate confirmed non-conductive | |
| **MR-02** | EZO pH circuit: which mode pin, which procedure | C-14 | D8-02 | | | | | The Pi sees the circuit | Recorded before the display box was closed | |
| **MR-03** | EZO EC circuit: which mode pin, which procedure | C-14 | D8-03 | | | | | The Pi sees the circuit | As MR-02 | |
| **MR-04** | EZO RTD circuit: which mode pin, which procedure | C-14 | D8-04 | | | | | The Pi sees the circuit | As MR-02. **The mode pin differs by circuit type: three procedures, not one repeated** | |
| **MR-05** | NDR-240-24 trim position as actually left, at the rail | C-16 | D8-16 | | | | | **NO CRITERION.** The row names no target. Owner: PUMP-BOXES for the 6121 VM range per F-010; the owner for every other device rating under G-15 | VS and its return short and paired when read | |
| **MR-06** | The watchdog fired, and did not loop silently | C-20 | D8-21 | | | | | It fires; it does not loop. **No time bound is stated** | External reset input confirmed to exist | |
| **MR-07** | Driver standstill current | C-13 | D8-25 | | | | | **NO CRITERION.** The row names no limit and no document holds the rail load budget it feeds. Owner: BOSS; MAIN-PANEL owns the rail | **The EN state it was measured in.** Rail as left per MR-05. VDD source per P-09 | |
| **MR-08** | Temperature rise inside a sealed pump box | C-15 | D8-26 | | | | | **NO CRITERION.** The row names no limit. Owner: BOSS, with PUMP-BOXES stating the rating | One motor running, three idle at standstill current. **The EN state of the three idle ones.** Heatsinks fitted, lid on | |
| **MR-09** | The permissive-drop state, entered deliberately: what was observed | C-18 | D8-27 | | | | | **NO CRITERION, AND NONE IS POSSIBLE.** Running it IS the decision to accept an uncharacterised state once, under observation. Owner: the owner decides, BOSS records | STEP commanded with VM removed; the manual-reset re-application transient | |
| **MR-10** | Head holds against back-siphon, **ENERGISED** | C-06 | D8-28 | | | | | It holds, or it does not | Jug above the inlet | |
| **MR-11** | Head holds against back-siphon, **DE-ENERGISED** | C-06 | D8-29 | | | | | It holds, or it does not | Jug above the inlet. **F-015: a de-energised stepper holds differently** | |
| **MR-12** | Day tank working volume | C-11 | D8-30 | | | | | **NO CRITERION.** Owner: WATER states what sets each end | **Not the nominal vessel capacity on the parts list** | |
| **MR-13** | Fill band, LOW end, **and the reason for it** | C-11 | D8-31 | | | | | **NO CRITERION.** Owner: WATER | The reason goes in the same row and is not optional | |
| **MR-14** | Fill band, HIGH end, **and the reason for it** | C-11 | D8-32 | | | | | **NO CRITERION.** Owner: WATER | As MR-13. **C-02 is measured at this end of the band** | |
| **MR-15** | Circulation flow at FL-03 | C-10 | D8-33 | | | | | **NO CRITERION.** A pump curve cannot supply one. Owner: WATER | Service conditions, valves in service positions, catch and time at the return drop, repeated at both ends of the fill band | |
| **MR-16** | Loop turnover time, day tank through manifold and back | C-07 | D8-34 | | | | | **NO CRITERION.** Owner: WATER | **It is a FLOOR for C-02 and not a settling time** | |
| **MR-17** | Are pH-up and pH-down in the same pump box? | C-09(c) | D8-43 | | | | | **They must not be** | Asked once across the build, after every role is known | |
| **MR-18** | pH noise and drift band on this build | C-08 | D8-46 | | | | | **N/A. THIS IS THE BASELINE. There is nothing behind it to compare to.** Marked with its reason per G-46. Owner of the marking: BOSS | Probes live, loop circulating, **no dose in flight**, chiller in normal service with its commanded state against every sample. Both pumps confirmed running before and after | |
| **MR-19** | EC noise and drift band on this build | C-08 | D8-46 | | | | | **N/A. As MR-18** | As MR-18 | |
| **MR-20** | t_first | C-02 | D8-47 | | | | | **N/A. C-02 DEFINES this figure.** Marked with its reason per G-46 | Deliberately OVERSIZED single dose. Tank at the HIGH end of the band per MR-14. Chiller state against every sample. Both pumps confirmed before and after | |
| **MR-21** | t_settle | C-02 | D8-47 | | | | | **N/A. As MR-20** | As MR-20 | |
| **MR-22** | pH step per single dose, **pH UP**, with its SIGN | C-03 | D8-52 | | | | | **Must exceed MR-18.** The row states it | Real dose size, using the timing from MR-20 and MR-21. Both pumps confirmed before and after. **The sign recorded here is the reference sign for S-16 and never comes from a product name** | |
| **MR-23** | pH step per single dose, **pH DOWN**, with its SIGN | C-03 | D8-53 | | | | | **Must exceed MR-18** | As MR-22 | |
| **MR-24** | Head discharge pressure against a flowing manifold | C-05 | none | **N/A** | **N/A** | **N/A** | **N/A** | **N/A** | **NOT SCHEDULED. Only needed if a pressure-based option is ever chosen, and none is. The row is kept visible so that the option does not look declined** | **N/A** |
| **MR-25** | The W-1 transient: the PT-1000 step when the pump starts after a rest | C-12 | none | **N/A** | **N/A** | **N/A** | **N/A** | **N/A** | **VOID 2026-09-04 by D-143. UNRUNNABLE: both day tank pumps run CONTINUOUSLY, so there is no rest, no start and no transient. Kept visible rather than deleted, because D-119 named it as the FREE surviving F-003 route and a deleted row would let that route look declined rather than spent.** F-101 | **N/A** |

### 3.2 Per-item groups

**A group is one row per item. HOW MANY ITEMS THERE ARE IS NOT STATED HERE** - it is the
source named in the group's own line, and a count copied into this page would be a second
inventory that goes stale the moment the source changes. **Print one row per item from
that source when the form is printed.**

**MR-G1. Float fail direction, one row per float position.** C-24, step D8-09.
Count and position names: **D2's roster and the float requirement.**

| Position | Chain behaviour when the conductor is lifted | Date | By | Measured against | Voided |
|---|---|---|---|---|---|
| | | | | **NO CRITERION IN C-24.** The eight fail directions are D-154's and are not in the C- row. Owner: BOSS | |

**Condition for every row in this group: the tanks were empty and dry.**

**MR-G2. STEP and DIR level at the driver terminal, one row per conductor.** C-21, step
D8-12. Count and ids: **D5's CDR- rows.**

| CDR- id | Measured level at the driver terminal | Units | Date | By | Measured against | Voided |
|---|---|---|---|---|---|---|
| | | | | | **Below V_IL. V_IL IS NOT IN THE ROW.** Owner: the owner's lookup under G-15, PUMP-BOXES stating the requirement | |

**Condition for every row: the pull-down fitted at the DRIVER end. Whether VDD is present
is not stated by C-21 - record what you did.**

**MR-G3. Sense path fail direction, one row per sense conductor.** C-19, step D8-18.
Count and ids: **D5's CDR- rows.**

| CDR- id | What the Pi reported with the conductor disconnected at the gland | Date | By | Measured against | Voided |
|---|---|---|---|---|---|
| | | | | **NO CRITERION IN C-19.** The expectation per signal is G-22's and is not in the row. Owner: BOSS | |

**MR-G4. Microstep configuration as set, one row per driver.** C-17, step D8-22. Count
and identifiers: **`terminal-survey.md` and D5.**

| Driver identifier | MS1 as set | MS2 as set | Date | By | Measured against | Voided |
|---|---|---|---|---|---|---|
| | | | | | The record matches the pins as physically set. **Set by pins, never over UART, D-075** | |

**MR-G5. Channel trace, one row per channel.** C-09, steps D8-35 to D8-40. Count and
tokens: **D11, `channel-register.md`.**

| Channel token | Trace run: head, tube, jug all confirmed | (a) Acid, base or salt solution | (b) Role setting matches the product's role | Date | By | Voided |
|---|---|---|---|---|---|---|
| | | | | | | |

**The head, tube, jug and product BINDING is written into D11 and not here.** This group
records that the trace was run and what the two questions returned. **If (a) returns
anything but acid, base or salt solution, STOP: D-084's carrier specification is
invalidated and nothing else detects it.** F-077.

**MR-G6. Delivered volume, one row per channel.** C-01, step D8-49. Count and tokens:
**D11.**

| Channel token | Per revolution | Per step | Units | Date | By | Measured against | Voided |
|---|---|---|---|---|---|---|---|
| | | | | | | **NO TOLERANCE IN C-01.** A direction only: lower than the manufacturer's no-back-pressure figure. Owner of a tolerance: BOSS | |

**Condition for every row: measured against REAL BACK PRESSURE into the running manifold,
with MR-G4 recorded first.** G-04: nothing in this system measures delivered volume, so a
wrong figure here is invisible, **and G-05 decrements the jug against it forever.**

**MR-G7. EC step per single dose, one row per EC-moving channel.** C-04, step D8-54.
Count: **D11, and it is not knowable until C-09 has run** - fulvic is a PRODUCT attribute
bound at C-09, D-122.

| Channel token | EC step per single dose | Units | Date | By | Measured against | Voided |
|---|---|---|---|---|---|---|
| | | | | | **Must exceed MR-19** | |

**Standing note on this group, carried from C-04 and not softened:** "EC-moving" is an
ASSUMPTION and not a measurement, D-107. **The scope excludes from the only measurement
that could falsify it whichever channel carries fulvic, so the premise is UNTESTABLE BY
CONSTRUCTION.** The decision stands, fulvic stays unattributed, **and the premise is
recorded here as unmeasured rather than silently treated as tested.**

---

## 4. THE CONDITIONS THAT TRAVEL WITH A WINDOW RUN

**Four rows use a measurement window: MR-18, MR-19, MR-20, MR-21, plus MR-22, MR-23 and
every row in MR-G7.** Each of them carries these three cells, and a run missing any of
them is not a measurement.

| Condition | Why it is recorded and not eliminated | Source |
|---|---|---|
| **The chiller's COMMANDED state, against every sample** | The chiller is NOT held off, so normal service IS the condition to measure under. **Recorded rather than eliminated, so that if the chiller does corrupt a reading the data will show it** | D-027, rewritten 2026-08-30 after D-027 reversed D-023 |
| **Both day tank pumps confirmed running by eye, BEFORE the window** | Nothing commands them, nothing reports them, nobody else checks. **A pump that has failed looks exactly like a pump that is running** | C-23 as reduced by D-143, F-102 |
| **Both day tank pumps confirmed running by eye, at the END of the window** | **If either was not running for the whole window, the run is DISCARDED, not adjusted** | C-23, G-20's shape |

---

## 5. THE RE-MEASURE LOG. THIS SECTION RUNS FOREVER

**NO FIGURE IN SECTION 3 IS PERMANENT.** `commissioning.md` says so in terms, and it
names the reason C-02 in particular cannot be trusted with age: **circulation flow is a
dominant input that this system cannot observe by choice.** D-007 closed S-13 and G-04
forbids meters, **so flow degradation from a fouled impeller, an intake screen, biofilm
or scale is invisible, and it lengthens the settling time silently.**

### 5.1 The triggers. Re-measure on the EVENT, not on a calendar alone

**One row per trigger in `commissioning.md`. Nothing here is added and nothing is
dropped.**

| Trigger | Event | What it voids and what must be re-measured |
|---|---|---|
| **MR-T01** | Any plumbing change: manifold, ports, tubing runs, the return drop's landing point, the submersible's position in the tank | **MR-20, MR-21, MR-16.** The return-versus-suction geometry changes short-circuiting more than anything else, **and it can be changed by someone tidying a cord** |
| **MR-T02** | Pump or impeller service, or any suspicion of reduced flow | **MR-20, MR-21, MR-16** |
| **MR-T03** | Probe replacement, recalibration or cleaning | **MR-18 and MR-19 first, then MR-22, MR-23 and MR-G7** |
| **MR-T04** | A product or recipe change | **MR-22, MR-23, MR-G7.** Different density and response, different detectability |
| **MR-T05** | Anything added to the loop: a filter, more plants served, a second manifold | **MR-20, MR-21, MR-16** |
| **MR-T06** | Any rewiring or renumbering of channels | **MR-G5.** The whole C-09 trace, every channel |
| **MR-T07** | Anyone touching the supply trimmer, for any reason | **MR-05, and re-check every device rating on the rail** |
| **MR-T08** | **A pump tube change on any channel, at about 1000 h** | **MR-G6 for that channel.** A worn tube delivers less per revolution **while every instrument reads healthy. The trigger is the tube change, not a date** |
| **MR-T09** | Any change to MS1 or MS2 on any driver | **MR-G4 for that driver, then MR-G6 for that channel** |
| **MR-T10** | Periodically, to catch fouling before it is a false-fail generator | **MR-20, MR-21, MR-18, MR-19, MR-15** |
| **MR-T11** | A driver replaced, where the driver's step configuration is part of what PUMP-BOXES sets | **MR-G6 for that channel is VOID until re-measured.** CONTROL-SOFTWARE will not carry a steps-per-millilitre figure across a driver change on the assumption that the configuration was reproduced. **Plus MR-G5** |

### 5.2 The log itself. EMPTY BY DEFINITION

**Write one line every time a trigger fires. Write it when the trigger fires, not when
the re-measurement is done** - the gap between the two is exactly when a stale figure is
in use and nothing says so.

| Entry | Date | Trigger | What happened | Rows voided | Re-measured on | By | New values entered |
|---|---|---|---|---|---|---|---|
| | | | | | | | |

**A voided row in section 3 is struck and dated and its replacement is written beneath
it. It is never overwritten.** The struck value is how anybody later tells a figure that
drifted from a figure that was always wrong.

---

## 6. WHAT IS NOT IN THIS FORM, AND WHY

**One figure is set during commissioning and has NO ROW HERE, deliberately.**

**The as-set VREF, per driver.** C-22 requires Vref to be set with VS present, and **no
C- row in `commissioning.md` schedules recording the value.** C-16's own argument applies
to it word for word: a rail nobody recorded is a rail nobody can check later, and Vref
sets the current in the motors. **A row here would be a figure entering at the view
instead of at the source, which is exactly G-54's defect.** Reported to BOSS as
`commissioning-checklist.md` section 13 defect 6. **When a C- row exists for it, a row
appears here and not before.**

**Also not here, each with its home:**

- **Per-channel product, role, jug and cable core.** D11, `channel-register.md`. Written
  at C-09, updated for the life of the build.
- **Any conductor, terminal, cable or landing fact.** D5 and D6.
- **Any quantity, count or price.** D7. **This form's per-item groups name whose fact each
  count is rather than stating one.**
- **Why any figure is needed.** Its C- row in `commissioning.md`.
- **Any datasheet value.** **Nothing in this build reads a datasheet where a D9 row
  exists.** That is the point of the document.

---

## 7. STATUS

**The FORM is complete. The CONTENT is EMPTY BY DEFINITION and will stay empty until D8
has been run.**

**Twenty-five fixed rows, seven per-item groups, eleven re-measure triggers and one open
log.** Twenty-three of the fixed rows are figures; two are marked N/A with their reason
and kept visible - **C-05 is NOT SCHEDULED and C-12 is VOID.**

**Twelve of the twenty-three figure rows carry NO CRITERION in the Measured against
column**, each naming the owner of that absence. That is not a defect in this form: **it
is what `commissioning.md` says today, carried across without invention.** G-54.

**Stopped part way. INTEGRATOR does not declare this finished**, rule 7. It is finished
when somebody has filled a row from a real measurement and found the column they needed
was there.
