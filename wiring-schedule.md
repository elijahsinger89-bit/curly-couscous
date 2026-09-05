# D5. Wiring schedule

**Every conductor in the build, one row each, keyed CDR-. Issued 2026-09-05.**

**Owner.** BOSS holds the list; each conductor's row is filled by the subsystem that
owns the crossing it realises. **This issue is INTERCONNECT's and covers the
conductors inside the jackets of D6.** Section 7 states what it does not cover and
who owns it.

**Who reads this and when.** The person with strippers in hand, before and during
wiring. **D4 is a generated VIEW of this list, one page per conductor - never a
transcription**, so no rule is written here saying the two must agree. G-45: they are
one source.

**Where each fact comes from.** D2, electrical-schematic.md, says what a conductor is
FOR. D6, cable-and-terminal-schedule.md, says the jacket it travels IN and the
landings at its ends. **This is where a conductor fact lives, and per
document-plan.md section 3.2 it is the only place one lives.**

**Deliberately not columns:** length, gauge, core count, colour, part number. **They
are outputs of a cut rule and a lookup, not facts about a conductor**, and storing
them here is what makes a wire table disagree with a cable schedule. Length comes from
D-090's rule at the cut step, per T-020, and F-099 is open against parts.md's two
allowance tables. **Nothing below states one.**

---

## 1. HOW TO READ A ROW

### 1.1 The schema

Thirteen columns, from wire-table-row-zero.md with the two amendments already made:
**column 8 splits into VOLTAGE CLASS and DUTY per D-150**, and **G-46 applies
throughout**.

| # | Column | Where it appears below |
|---|---|---|
| 1 | Conductor ID | Row |
| 2 | Cable | **Group header**, or the row where it varies |
| 3, 4 | From: device, terminal | Row, as `device . terminal` |
| 5, 6 | To: device, terminal | Row, as `device . terminal` |
| 7 | Function | Row |
| 8a | **Voltage class** | Group header |
| 8b | **Duty** | Group header, or the row where it varies |
| 9 | **Design current, and WHICH EVENT** | Row |
| 10 | Interface row | Row |
| 11 | **Fail behaviour on a severed conductor** | Row |
| 12 | Status | Row |

**A constant is stated once per group rather than repeated down a column.** G-45
again: a value written once cannot disagree with itself, and a group header is the
cheapest generator there is.

### 1.2 A cell has three states, G-46

**Filled**; **n/a** with its reason, meaning the conductor has no such property and it
waits on nobody; **OPEN** with its blocker. **A cell that can never be filled must not
look like one that has not been filled yet.**

### 1.3 What makes a conductor exist

**A conductor exists in this list when the circuit that requires it is stated in a
frozen or closed interface row, or drawn in D2, AND both of its ends are named as
DEVICES.** Terminal markings may be OPEN - that is columns 4 and 6, and
wire-table-row-zero.md's own prototype has both open on a conductor that certainly
exists.

**Every conductor cites its interface row, and a conductor with no interface row does
not exist.** Where one was needed and no row named it, that is F-107's shape and it is
reported in section 6, never invented here.

**The number in a CDR- id carries no meaning.** **CDR-001 keeps the identity
wire-table-row-zero.md gave it - the fill solenoid's coil hot leg - so it appears out
of sequence, in the RUN-011 group.** No rule is keyed to a CDR- number and a gap is
never closed.

### 1.4 Three facts carried in from elsewhere, applied to every row

**1. The grounding conductor rides inside the run**, D-165. Each cross-box jacket
holds one, landing on a local bar at the remote end and on the single-point copper bar
in the main panel. **RUN-017 was retired for this reason and no bonding cable exists.**
**Nothing bonds anywhere else** - written down because a builder who finds a
convenient screw will use it.

**2. Insulation follows the worst company, not the conductor's own circuit.** A
conductor sharing a jacket, a tie bundle or a LANDING with a 120 V circuit is
insulated for the highest voltage present. **It arrived three times from three
directions** - the standpipe bundle at D-156, the leak console jacket at D-163, and
the ground bar at D-165, a bar being always in the 120 V chain even in a box that
holds only 24 V because the ground is common. **So every grounding conductor below,
and every 24 V conductor landing on a bar, takes that rating whatever it carries.**

**3. A supplied assembly has no conductors in this list.** RUN-009's USB-C cable,
RUN-014's and RUN-016's supplied leads and the three cord routes are manufactured
assemblies whose conductors nothing lands. **Section 5 names them so their absence
reads as a property rather than as an omission.**

---

## 2. THE SCHEDULE

**Sixty-four conductors. CDR-001 through CDR-064.**

Column 4 and column 6 are OPEN on every row for one reason and it is F-106: **nobody
in this project has ever been asked to look at a terminal and report what is printed
on it.** It is stated here once instead of sixty-four times.

---

### RUN-001. Cable: RUN-001 | Voltage: **24 V**, and insulated for the bar it lands on | Duty: **ARC**, D2 rung 16

| CDR | From | To | Function | Current, and which event | Row | Severed conductor | Status |
|---|---|---|---|---|---|---|---|
| **CDR-002** | MAIN-PANEL.KM-DRV `{pole 1}` | PUMP-BOX-A.`{driver supply block, + side}` | Motor supply positive to the four drivers in box A | **OPEN** - PUMP-BOXES owes the driver supply range and draw from the datasheet | P-06 | Motor supply absent, heads stop. **What a driver does with STEP asserted and VM absent is uncharacterised, P-09, and C-18 accepts that once under observation** | BLOCKED: P-06, CBL-02 |
| **CDR-003** | MAIN-PANEL.`{24 V rail, -V}` | PUMP-BOX-A.`{driver supply block, - side}` | Motor supply return | **OPEN**, as CDR-002 | P-06 | As CDR-002 | BLOCKED: P-06, CBL-02 |
| **CDR-004** | PUMP-BOX-A.`{local ground bar}` | MAIN-PANEL.`{ground bar}` | Equipment grounding, daisies box A's local bar home | **n/a.** A grounding conductor carries no design current; its sizing is a fault-current question and MAIN-PANEL's | CBL-07 | **Box A's local bar is no longer bonded home and nothing reports it.** That is why the bar is the single point | BLOCKED: CBL-02. The bars are not bought |

### RUN-002. Cable: RUN-002 | Voltage: **24 V**, insulated for the bar | Duty: **ARC**, rung 16

| CDR | From | To | Function | Current, and which event | Row | Severed conductor | Status |
|---|---|---|---|---|---|---|---|
| **CDR-005** | MAIN-PANEL.KM-DRV `{pole 1}` | PUMP-BOX-B.`{driver supply block, + side}` | Motor supply positive, box B | **OPEN**, as CDR-002 | P-06 | As CDR-002 | BLOCKED: P-06, CBL-02 |
| **CDR-006** | MAIN-PANEL.`{24 V rail, -V}` | PUMP-BOX-B.`{driver supply block, - side}` | Motor supply return | **OPEN** | P-06 | As CDR-002 | BLOCKED: P-06, CBL-02 |
| **CDR-007** | PUMP-BOX-B.`{local ground bar}` | MAIN-PANEL.`{ground bar}` | Equipment grounding, box B | **n/a**, as CDR-004 | CBL-07 | As CDR-004 | BLOCKED: CBL-02 |

**Note on CDR-002 and CDR-005: both leave ONE terminal.** parts.md: one pole for
motor-supply distribution, both feeds off one terminal downstream of it. **T-010 is
live at that landing and is D6's check, not this document's.**

### RUN-003. Cable: RUN-003 | Voltage: **SIGNAL** | Duty: **n/a, no pole** on all three

| CDR | From | To | Function | Current, and which event | Row | Severed conductor | Status |
|---|---|---|---|---|---|---|---|
| **CDR-008** | DISPLAY-BOX.`{5 V rail}` | PUMP-BOX-A.`{driver VDD}` | Driver logic supply, box A. **Unswitched: the permissive removes motor supply only**, G-09 as amended by D-031 | **OPEN** - PUMP-BOXES owes the VDD draw | P-09 | **VDD absent while the logic board still drives STEP and DIR into those pins - which is the exact state D-031 says the drivers must never see, an overdrive through the input protection diodes.** Severed here produces it on four drivers | BLOCKED: CBL-02, CBL-03 |
| **CDR-009** | DISPLAY-BOX.`{5 V return}` | PUMP-BOX-A.`{driver GND}` | Logic supply return, and the reference the STEP and DIR levels are measured against | **OPEN** | P-09 | As CDR-008, and **T-007: without this common the drive does nothing while both ends look correct** | BLOCKED: CBL-02, CBL-03 |
| **CDR-010** | PUMP-BOX-A.`{local ground bar}` | DISPLAY-BOX.`{local ground bar}` | Equipment grounding | **n/a**, as CDR-004 | CBL-07 | As CDR-004 | BLOCKED: CBL-02, CBL-03 |

### RUN-004. Cable: RUN-004 | Voltage: **SIGNAL** | Duty: **n/a, no pole**

| CDR | From | To | Function | Current, and which event | Row | Severed conductor | Status |
|---|---|---|---|---|---|---|---|
| **CDR-011** | DISPLAY-BOX.`{5 V rail}` | PUMP-BOX-B.`{driver VDD}` | Driver logic supply, box B | **OPEN** | P-09 | As CDR-008 | BLOCKED: CBL-02, CBL-03 |
| **CDR-012** | DISPLAY-BOX.`{5 V return}` | PUMP-BOX-B.`{driver GND}` | Logic supply return and level reference | **OPEN** | P-09 | As CDR-009 | BLOCKED: CBL-02, CBL-03 |
| **CDR-013** | PUMP-BOX-B.`{local ground bar}` | DISPLAY-BOX.`{local ground bar}` | Equipment grounding | **n/a** | CBL-07 | As CDR-004 | BLOCKED: CBL-02, CBL-03 |

### The per-channel conductors. Cable: **OPEN on all sixteen** | Voltage: **SIGNAL** | Duty: **n/a, no pole**

**These sixteen exist because the eight channels exist, S-19 and D-021, and the pin
list exists.** **Their JACKET does not**, because PUMP-BOXES has not returned which
tokens sit in which box - so column 2 is OPEN on every one and is the only place in
this document where it is.

**The token is the conductor's identity at both ends and there is no per-cable
restart when they split across RUN-003 and RUN-004.** channel-token.md, and its
forbidden list bars a renumbering to match a connector's pin order or a core's
position in a bundle. **The token appears IN ADDITION to the CDR- id and the two are
never merged.**

| CDR | From | To | Function | Current, and which event | Row | Severed conductor | Status |
|---|---|---|---|---|---|---|---|
| **CDR-014** | DISPLAY-BOX.`{logic board, CH1 STEP}` | `{the driver assigned CH1}` . `{STEP}` | Step pulses, **CH1** | **OPEN** - DISPLAY-BOX owes the drive form and PUMP-BOXES the input threshold | S-10 | **Not "no steps": an undriven CMOS input on a driver enabled by default, in a box where four choppers drive eight motor phase conductors. Coupled noise can clock it and the books never record it.** F-018, F-060 | BLOCKED: S-10, and the box division |
| **CDR-015** | DISPLAY-BOX.`{logic board, CH1 DIR}` | `{the driver assigned CH1}` . `{DIR}` | Direction, **CH1** | **OPEN** | S-10 | **THE WORST OUTCOME IN THE FAIL-SAFE SWEEP. Direction undefined on a driver enabled by default: a head runs backwards, drawing from the manifold toward the jug, while the books decrement as though it dosed forward.** D-096: severed goes HIGH by the board. The fix is a pull-down AT THE DRIVER END, PUMP-BOXES', D-043 | BLOCKED: S-10, D-043, and the box division |
| **CDR-016 / CDR-017** | as above, **CH2** STEP / DIR | " | " | **OPEN** | S-10 | As CDR-014 / CDR-015 | BLOCKED |
| **CDR-018 / CDR-019** | **CH3** STEP / DIR | " | " | **OPEN** | S-10 | " | BLOCKED |
| **CDR-020 / CDR-021** | **CH4** STEP / DIR | " | " | **OPEN** | S-10 | " | BLOCKED |
| **CDR-022 / CDR-023** | **CH5** STEP / DIR | " | " | **OPEN** | S-10 | " | BLOCKED |
| **CDR-024 / CDR-025** | **CH6** STEP / DIR | " | " | **OPEN** | S-10 | " | BLOCKED |
| **CDR-026 / CDR-027** | **CH7** STEP / DIR | " | " | **OPEN** | S-10 | " | BLOCKED |
| **CDR-028 / CDR-029** | **CH8** STEP / DIR | " | " | **OPEN** | S-10 | " | BLOCKED |

**SIXTEEN MORE CONDUCTORS ARE REQUIRED AND ARE NOT ENUMERATED HERE, DELIBERATELY.**
F-030 requires every STEP and DIR to be paired with its own return, so that the
nearest neighbour of every signal is a ground return rather than another signal -
because a STEP shorted to another channel's STEP steps two heads together, which
violates G-06 in hardware where software cannot prevent it. **F-030 is a stated
requirement and not a decision, so its conductors are named and not issued ids.**
G-29 is the construction rule they would satisfy. **They are cheaper now than after
the cable is bought, and D-149 says the parent ids retire when they arrive.**

### RUN-005. Cable: RUN-005 | Voltage: **24 V**, insulated for the bar | Duty: **COIL**, rung 15

| CDR | From | To | Function | Current, and which event | Row | Severed conductor | Status |
|---|---|---|---|---|---|---|---|
| **CDR-030** | MAIN-PANEL.KM-DRV `{coil}` | DISPLAY-BOX.`{ULN2003 output, BCM 18}` | **The coil RETURN.** The device SINKS, so the coil positive is taken in the panel and this conductor is the return, T-006 | **OPEN** - MAIN-PANEL owes the coil burden, and F-021 asks whether the logic board can drive it at all | S-07 | **Coil de-energises, KM-DRV drops, motor supply is removed. Fail-safe.** The dangerous case is the other one: **F-019, a SHORTED output device, and whether it defeats G-07 depends on where the coil positive is taken from - raw 24 V or node PB. ?17 is OPEN and the row must state which** | BLOCKED: S-07, ?17, CBL-01, CBL-03 |
| **CDR-031** | MAIN-PANEL.`{24 V rail, -V}` | DISPLAY-BOX.`{logic board common}` | The shared common the sinking driver switches against | **OPEN** | S-07, **or a second F-107** - section 6 | **The drive does nothing and both ends look correctly landed.** T-007, and it is the failure that passes every check in isolation | BLOCKED: S-07, and section 6 |
| **CDR-032** | DISPLAY-BOX.`{local ground bar}` | MAIN-PANEL.`{ground bar}` | Equipment grounding, daisies the display box home | **n/a**, as CDR-004 | CBL-07 | As CDR-004 | BLOCKED: CBL-01, CBL-03 |

### RUN-006. Cable: RUN-006 | Voltage: **24 V**, insulated for the bar | Duty: **SENSE**, rung 24

| CDR | From | To | Function | Current, and which event | Row | Severed conductor | Status |
|---|---|---|---|---|---|---|---|
| **CDR-033** | MAIN-PANEL.KM-DRV `{pole 2}` | DISPLAY-BOX.`{optocoupler LED, S-08}` | Permissive readback, wetted feed. **The burden is a second branch IN THE PANEL, so the contact stays wetted when this cable is unplugged** | **45 to 55 mA total across both branches, at make and break of KM-DRV pole 2**, against the contactor's 1000 mW minimum. parts.md, GIVEN, not re-derived | S-08 | **The Pi input stays HIGH, reads contact open, reads a drop. A CHOSEN property, not an inheritance**, G-22 | BLOCKED: CBL-01, CBL-03, DISPLAY-BOX's input side |
| **CDR-034** | DISPLAY-BOX.`{optocoupler LED return}` | MAIN-PANEL.`{24 V rail, -V}` | Readback loop return | As CDR-033, same loop and same event | S-08 | As CDR-033 | BLOCKED: as CDR-033 |
| **CDR-035** | DISPLAY-BOX.`{local ground bar}` | MAIN-PANEL.`{ground bar}` | Equipment grounding | **n/a** | CBL-07 | As CDR-004 | BLOCKED: CBL-01, CBL-03 |

**G-30 conflict on CDR-033's source, marked and not resolved:** pole 1 of KM-DRV is an
ARC pole and pole 2 is a SENSE pole. **S-08 has nowhere to move - there is no
auxiliary block and none was bought.** D2 rung 24.

### RUN-007. Cable: RUN-007 | Voltage: **24 V**, insulated for the bar | Duty: **SENSE**, rungs 25 and 26

**Both legs of ONE changeover pole. G-27: same potential, same cable, exactly one
conducting, and any state where both agree is a broken sense path.** Neither may be
split into another jacket.

| CDR | From | To | Function | Current, and which event | Row | Severed conductor | Status |
|---|---|---|---|---|---|---|---|
| **CDR-036** | MAIN-PANEL.K-FILL-D-Q `{changeover pole, NC leg}` | DISPLAY-BOX.`{optocoupler LED, S-03}` | Day tank fill in progress. **CLOSED means NO FILL, OPEN means FILLING** | **About 12.5 mA, one series branch, at make and break**, against the 55.34's 300 mW minimum. **Copying S-08's two-branch arrangement here would add a part for nothing.** parts.md | S-03 | **Reads as FILLING, so dosing is inhibited and the failure is a stop rather than a permission.** D-042, closed by INVERSION rather than by logic. T-016 | BLOCKED: CBL-01, CBL-03, DISPLAY-BOX's input side |
| **CDR-037** | MAIN-PANEL.K-FILL-D-Q `{same pole, NO leg}` | DISPLAY-BOX.`{optocoupler LED, dose inhibit}` | The D-042 dose-inhibit leg, to a second isolated Pi input | As CDR-036, same pole | **S-03**, amended to state it is a two-conductor pair rather than split into a new row, under G-45 | As CDR-036, **and G-27 makes the pair fail-DETECTED: if both legs report the same state, the sense path is broken** | BLOCKED: as CDR-036 |
| **CDR-038** | DISPLAY-BOX.`{local ground bar}` | MAIN-PANEL.`{ground bar}` | Equipment grounding | **n/a** | CBL-07 | As CDR-004 | BLOCKED: CBL-01, CBL-03 |

**The RETURN arrangement of this pair is not enumerated and its absence is stated
rather than left:** whether the two LED loops share one return or take one each is
DISPLAY-BOX's input side and is open. **Two more conductors, or one, and nobody can
say which yet.**

### RUN-008. Cable: RUN-008 | Voltage: **24 V**, insulated for the bar | Duty: **SENSE**, rungs 27 and 28

| CDR | From | To | Function | Current, and which event | Row | Severed conductor | Status |
|---|---|---|---|---|---|---|---|
| **CDR-039** | MAIN-PANEL.K-DRY-Q `{changeover pole, NO leg}` | DISPLAY-BOX.`{optocoupler LED, S-20}` | Dry-run relay state to the Pi, so the circulation VERIFICATION judgement is made in software under G-16 | **OPEN.** Sized independently under G-23 by MAIN-PANEL: **a minimum switching load belongs to a contact and no figure is carried from another** | S-20 | **Reads as K-DRY dropped, which reads as the manifold pump not permitted.** With ?25 closed by D-154, K-DRY energised is the permitted state, **so this sense is established from this build's topology and inherited from nothing**, per F-017 | BLOCKED: S-20, CBL-01, CBL-03 |
| **CDR-040** | MAIN-PANEL.K-DRY-Q `{same pole, NC leg}` | DISPLAY-BOX.`{optocoupler LED, complement}` | S-20's G-27 complement | **OPEN**, as CDR-039 | **S-20**, amended to state the pair rather than split it | As CDR-039, and **any state where both legs agree is a broken sense path** | BLOCKED: as CDR-039 |
| **CDR-041** | DISPLAY-BOX.`{local ground bar}` | MAIN-PANEL.`{ground bar}` | Equipment grounding | **n/a** | CBL-07 | As CDR-004 | BLOCKED: CBL-01, CBL-03 |

**Same return question as RUN-007, and same answer: not enumerable yet.**

### RUN-010. Cable: RUN-010 | Voltage: **LINE** | Duty: **n/a, no pole** on all three

| CDR | From | To | Function | Current, and which event | Row | Severed conductor | Status |
|---|---|---|---|---|---|---|---|
| **CDR-042** | `{building branch circuit}` . `{line}` | MAIN-PANEL.`{line input}` | Supply, line | **OPEN.** The branch arrangement, its protection and what shares each circuit are unstated, and no disconnecting means is named anywhere | P-01 | **The whole panel is dead**, which is G-39's question answered by the tree rather than by this row: **the fill valve spring-returns CLOSED, K-DRY de-energises and stops the manifold pump, KM-DRV drops and removes motor supply.** Nothing is left energised | BLOCKED: P-01, CBL-01 |
| **CDR-043** | `{building branch circuit}` . `{neutral}` | MAIN-PANEL.`{neutral}` | Supply, neutral | **OPEN** | P-01 | As CDR-042 | BLOCKED: P-01, CBL-01 |
| **CDR-044** | `{building branch circuit}` . `{equipment ground}` | MAIN-PANEL.`{ground bar}` | **The system's equipment ground, arriving at the single point** | **n/a**, as CDR-004 | P-01, CBL-07 | **Every local bar downstream loses its path home at once, and nothing reports it** | BLOCKED: P-01, CBL-01 |

**RUN-010 may be two jackets.** D-137 puts the chiller and loop pump on a DEDICATED
circuit and P-01 names one branch circuit. **If a second feed arrives, these three
conductors are joined by three more and D6 issues a new RUN- id.**

### RUN-011. Cable: RUN-011 | Voltage: **LINE** | Duty: **ARC**, rung 06

| CDR | From | To | Function | Current, and which event | Row | Severed conductor | Status |
|---|---|---|---|---|---|---|---|
| **CDR-001** | MAIN-PANEL.K-FILL-S `{solenoid pole}` | FV-1 `{coil lead}` | **Switched 120 VAC to the fill solenoid coil** | **0.58 A INRUSH, at make and break. NOT the 0.21 A holding figure**, D-136. **A relay contact makes and breaks the inrush, and sizing against the holding figure is sizing against the wrong event** | **P-02** | **The coil de-energises and the valve SPRING-RETURNS CLOSED.** D-114 and G-39. **The one cell in this document that filled with certainty, because the fail state was chosen before the part was** | BLOCKED: P-02, CBL-01, CBL-04 |
| **CDR-045** | FV-1 `{coil lead}` | MAIN-PANEL.`{neutral}` | Coil return | As CDR-001, same event | P-02 | As CDR-001 | BLOCKED: as CDR-001 |
| **CDR-046** | FV-1 `{ground}` | MAIN-PANEL.`{ground bar}` | Equipment grounding for the valve | **n/a**, as CDR-004 | CBL-07 | As CDR-004 | BLOCKED: CBL-01, CBL-04 |

**CDR-001 is corrected here against wire-table-row-zero.md, and the correction is the
point of having filled one row early.** Its Cable cell read **CBL-04**, which is a
crossing and not a jacket - D-149 fixed that and it is **RUN-011**. Its Interface row
cell read **OPEN**, on the belief that the solenoid had no power row - **P-02 exists,
names both ends, and always did**, F-098. **Two of that row's five open cells were
never open.**

### RUN-012, the day tank floats. Cable: RUN-012 | Voltage: **24 V, insulated for the highest voltage in the standpipe bundle**, D-156 | Duty: **COIL**, D2 section 4

**Every float is a series element in a 24 V coil chain and no float switches a load**,
D-154. **So the fail direction is FORCED by topology and is the same at all eight
positions: severed equals open equals coil de-energised equals the action stops.** It
is not chosen and it is not inherited.

**Both conductors of every float come home. No series link is made in the wet zone**,
and that is INTERCONNECT's decision under G-48: **parts - none, it is a
cable-selection consequence D7 buys; steps - none in the tank, and one landing pair per
float in the panel; what it buys - C-24 can test each float's fail direction at the
panel with a meter, a failed float is identified rather than a chain being open
somewhere, and there is no splice in a tank where D-131 says to adjust the tie and
never the wiring.**

**No grounding conductor: there is no local bar at a float and nothing conductive to
bond.** The standpipe is PVC, confirmed 2026-09-05.

| CDR | From | To | Function | Current, and which event | Row | Severed conductor | Status |
|---|---|---|---|---|---|---|---|
| **CDR-047 / CDR-048** | LS-1 `{day tank fill start}` , both switch terminals | MAIN-PANEL.K-FILL-D `{coil chain}` , rung 20 | Series element, day tank fill start | **OPEN** - MAIN-PANEL owes the coil burden, and **F-112: the break is DC and inductive, not AC**, which is a different contact problem at the same power | S-02 | Coil de-energises, the day tank fill stops | BLOCKED: S-02, CBL-01, CBL-04, D-118 |
| **CDR-049 / CDR-050** | LS-5 `{day tank fill stop}` , both terminals | MAIN-PANEL.K-FILL-D `{coil chain}` , rung 20 | Series element, day tank fill stop | **OPEN** | S-02 | Coil de-energises, the fill stops. **Under D-130 this is the float that is the only thing knowing the tank is full, and the overflow is its second line** | BLOCKED: as above |
| **CDR-051 / CDR-052** | LS-4 `{day tank low-low}` , both terminals | MAIN-PANEL.K-DRY `{coil chain}` , rung 22 | Series element, **the S-05 dry-run element under G-11 and D-119** | **OPEN** | S-02 | K-DRY de-energises and the manifold pump stops. **G-39's question answered for this relay by D2 rung 22** | BLOCKED: as above |
| **CDR-053 / CDR-054** | LS-2 `{day tank high-high}` , both terminals | **OPEN** | Series element, overfill backstop | **OPEN** | S-02 | The chain it sits in de-energises | BLOCKED: **whether the high-high floats sit in the permissive string, and their landing, is open** - D2's ?13 and ?14, MAIN-PANEL and WATER jointly |

### RUN-013, the storage floats. Cable: RUN-013 | Voltage and duty **as RUN-012**

| CDR | From | To | Function | Current, and which event | Row | Severed conductor | Status |
|---|---|---|---|---|---|---|---|
| **CDR-055 / CDR-056** | LS-6 `{storage fill start}` , both terminals | MAIN-PANEL.K-FILL-S `{coil chain}` , rung 19 | Series element, storage fill start | **OPEN** | S-01 | Coil de-energises, the storage fill stops | BLOCKED: S-01, CBL-01, CBL-04, D-118 |
| **CDR-057 / CDR-058** | LS-7 `{storage fill stop}` , both terminals | MAIN-PANEL.K-FILL-S `{coil chain}` , rung 19 | Series element, storage fill stop | **OPEN** | S-01 | As CDR-049 | BLOCKED: as above |
| **CDR-059 / CDR-060** | LS-3 `{storage low, pump-down}` , both terminals | MAIN-PANEL.K-FILL-D `{coil chain}` , rung 20 | **Series element in the DAY TANK fill chain, not the permissive string.** MAIN-PANEL's ruling closing ?15: a dry storage tank then stops the transfer only, rather than dropping the drivers and both fills | **OPEN** | S-01 | The day tank fill stops. **The transfer pump is protected from running dry** | BLOCKED: as above |
| **CDR-061 / CDR-062** | LS-8 `{storage high-high}` , both terminals | **OPEN** | Series element, overfill backstop | **OPEN** | S-01 | The chain it sits in de-energises | BLOCKED: **?13 and ?14, as CDR-053** |

### RUN-015, the leak console. Cable: RUN-015 | Voltage: **LINE-rated on every conductor**, CBL-06 | Duty: **COIL or ARC, contested**

| CDR | From | To | Function | Current, and which event | Row | Severed conductor | Status |
|---|---|---|---|---|---|---|---|
| **CDR-063** | MAIN-PANEL.`{24 V rail, +V}` | WB200 `{supply}` | Console supply, positive. **Insulated for 600 V although it carries 24 V, because its jacket holds contact legs in the 120 V chain** | **OPEN** - the console's draw is not stated in any file I read | CBL-06 | **OPEN, and it is section 6's finding: what this console's Form C contact does when its own supply fails is on file nowhere, and its legs are in the permissive chain** | BLOCKED: CBL-06, CBL-01, the console's position, and its de-energised contact state |
| **CDR-064** | WB200 `{supply return}` | MAIN-PANEL.`{24 V rail, -V}` | Console supply, return | **OPEN** | CBL-06 | **OPEN**, as CDR-063 | BLOCKED: as CDR-063 |

**The console's CONTACT LEGS are not enumerated and their absence is stated:**
**MAIN-PANEL states the legs**, per CBL-06's own owner column, and a Form C has three
terminals of which nobody has said how many are used. **Two more conductors, or three,
and it is not INTERCONNECT's to decide.**

---

## 3. WHAT IS FILLED, HONESTLY

**Sixty-four conductors, thirteen columns, 832 cells: 592 FILLED, 42 with NO VALID
VALUE, 198 still EMPTY.**

**The empty cells are not spread evenly and three columns hold nearly all of them:**

| Column | Empty | Why, in one line |
|---|---|---|
| **4 and 6, the terminals** | **128** - two on every row | **F-106. Nobody has been asked to look at a part.** It is one request, not sixty-four |
| **9, design current and its event** | **48** | Each belongs to the subsystem owning the load. **Six are filled and every one of them came from parts.md having recorded a real figure with its event** |
| **2, the cable** | **16** | Only the per-channel conductors, waiting on PUMP-BOXES' box division |
| Everything else | **6** | LS-2's and LS-8's landings, ?13 and ?14; and RUN-015's two fail cells, section 6 |

**Not one conductor is buildable**, and the reason is D6's and unchanged: CBL-01
through CBL-04 are OPEN, and every jacket lands at a gland or bulkhead they govern.

---

## 4. THE FAIL COLUMN IS PER CONDUCTOR AND IS NEVER ROLLED UP

**Column 11 is filled per conductor, never averaged over a jacket**, because
averaging several directions into one is the F-017 inheritance itself - BOSS once put
S-03's fail direction on file as S-08's without establishing it, and that is why G-22
was amended.

**What the column shows when you read it down rather than across, and it is worth the
pass:**

- **Sixty of sixty-four fail SAFE on a severed conductor**, and almost none of them
  fails safe by luck. The float chains fail safe because D-154 forced it from topology;
  the solenoid because D-114 chose the fail state before the part; the sense loops
  because D-042 inverted a contact and G-22 chose the severed case on frequency.
- **Two fail UNSAFE and both are known: CDR-015's family.** A severed DIR leaves
  direction undefined on a driver enabled by default, and a severed STEP is an
  undriven CMOS input that noise can clock. **Their remedy is a pull-down at the
  DRIVER end, PUMP-BOXES' under D-043, because a pull at the display end does nothing
  once the conductor is cut.**
- **Two are OPEN, CDR-063 and CDR-064**, section 6.
- **And the severed case is only half of G-22.** The SHORT case is answered by
  adjacency - the wiring plan - and that is D6's segregation groups and entry order,
  not this document. **On the standpipe there is no wiring plan left to answer with,
  which is F-113 and is answered in D6 section 4.**

---

## 5. WHAT HAS NO CONDUCTORS HERE, AND WHY THAT IS A PROPERTY

**Six of D6's nineteen jackets contribute no CDR- row, and every one is a manufactured
assembly whose conductors nothing lands.**

| Jacket | Why |
|---|---|
| **RUN-009** | A USB-C cable, supplied and **not cuttable**. Its conductors are inside the assembly and it terminates at a bulkhead connector, not a clamp |
| **RUN-014, RUN-016** | Supplied leads: the leak sensor's and the probes'. Their conductors are the manufacturer's, and S-11 and S-04 are open besides |
| **RUN-018, RUN-019, RUN-020** | Cord caps into panel-mounted receptacles, D-046. Nothing lands a cord's conductors |

**D4 will therefore have no page for these six, and that is correct rather than a
gap.** A page per conductor over a cable nobody terminates would be a page describing
nothing.

---

## 6. WHAT WRITING THIS FOUND

**F-115 shape, and it is the sharper of the two. WHAT THE LEAK CONSOLE'S CONTACT DOES
WHEN ITS OWN SUPPLY FAILS IS ON FILE NOWHERE, AND ITS LEGS ARE IN THE PERMISSIVE
CHAIN.**

CDR-063 and CDR-064 are the console's 24 V supply. **Severing either one leaves a
powered device unpowered while its dry contact still sits in a hardwired safety
string.** G-39 asks what a DEAD PANEL does, and it was frozen for actuators. **Nobody
has asked it of a powered sense device**, and the console is the only one in the
build.

What I read to establish the absence: **CBL-06, D-163, D2's device roster and rung 11,
parts.md's leak console section, and order.md.** All four describe the 24 V supply and
the Form C output. **None states the contact's de-energised state.** If it fails to
the "no leak" state, a dead console is a permission; if it fails to the "leak" state,
a dead console is a stop. **One is fail-safe and one is not, and which it is decides
whether this conductor's fail cell can be filled at all.** Routed to MAIN-PANEL, which
states the legs, and to the owner, whose lookup it is. **I state neither direction and
inherit none**, per F-017.

**F-107's shape, a possible second instance, reported and not invented. CDR-031, the
shared common for the permissive coil drive.** T-007 is explicit: a remote
open-collector driver needs a shared common back to the supply it switches against, or
both ends land correctly and the circuit does nothing. **S-07 names the drive and the
coil. It does not name a common.** Either S-07 covers it, or it is a second instance
of the thing MAIN-PANEL found at ?27 and ?28. **BOSS amended two rows rather than
creating them last time and this is the same choice. I have not invented a row and I
have not left the conductor out.**

**And one correction this document makes to its own prototype**, in RUN-011: **two of
CDR-001's five open cells were never open.** Its Cable named a crossing rather than a
jacket, which D-149 has since forbidden, and its Interface row was recorded as absent
when P-02 exists and names both ends. **The prototype was right that filling one row
early is worth it - it is just that the two defects it found were three.**

---

## 7. WHAT THIS ISSUE DOES NOT COVER

**Every conductor internal to the main panel.** D2 draws thirty-one rungs and most of
their conductors never leave the enclosure: the rails, the permissive string, the
seal-in poles, the coil buses, the lamps and their burdens, the two receptacle
feeds and the burden branches of all four sense circuits.

**They are D5 rows and they are MAIN-PANEL's to fill, not mine.** Rule 1. What I read
to say this rather than assuming it: **document-plan.md's D5 section gives BOSS the
list and each conductor's row to the subsystem owning the crossing; MAIN-PANEL's own
file says terminal numbers are assigned late; and D2 states in terms that it carries no
terminal number anywhere.** **A panel-internal conductor cannot be written down before
its terminals have names, and F-105 was closed only last night.**

**No id in the CDR- range is reserved for them and none is skipped.** D-149's rule
holds: the number carries no meaning, so MAIN-PANEL's conductors take the next free
ids whenever they are written, and nothing is renumbered around them.

---

## 8. STATUS

**Stopped part way. INTERCONNECT does not declare this finished** - rule 7, and that
waits until another agent builds against it and finds nothing. **The agent that will
is whoever generates D4 from it.**

**Deliverable as it stands:** sixty-four conductors with real ids, each citing an
interface row, each carrying its own fail direction, each naming its blocker. **A
person can see what every wire in the crossings is for and what it does when it
breaks.** Nobody may cut or land against it.

**Four things would move the most, in order:**

1. **One request nobody has made: look at the parts and write down what is printed on
   the terminals.** F-106. It is 128 of the 198 empty cells and it is not a decision,
   a purchase or a design - it is somebody with the parts in hand and a pen.
2. **PUMP-BOXES' box division**, which fills the only sixteen empty Cable cells.
3. **The leak console's de-energised contact state**, section 6.
4. **F-030's per-signal returns**, after which sixteen more conductors are issued and
   RUN-003 and RUN-004 retire under D-149.

**Not returned, so no absence is read as an answer:** no length, gauge, core count,
colour or part number, none of which is a column here; **no conductor internal to any
enclosure**, section 7; and **no fail direction stated for CDR-063 or CDR-064**, which
is unanswered rather than safe.
