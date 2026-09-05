# Interface table

Every crossing between subsystems, both ends named. BOSS owns this file. No
subsystem edits it. A subsystem that finds a boundary defect reports it here
through BOSS and does not fix it.

## THE ID NAMESPACE. RESERVED, AND NOT REUSABLE. D-145, 2026-09-04.

**Every prefix below is TREE-GLOBAL. No document may use one for a local list.**

| Prefix | Means | Lives in |
|---|---|---|
| **FL-nn** | **FLUID** interface row. **RENAMED FROM F-nn 2026-09-04** | this file |
| P-nn | POWER interface row | this file |
| S-nn | SIGNAL interface row | this file |
| CBL-nn | **A CABLE CROSSING, not a cable** | this file |
| M-nn | MECHANICAL interface row | this file |
| G-nn | Frozen rule | decisions.md |
| D-nnn | Dated decision | decisions.md |
| **F-nnn** | **FINDING**, and now the only meaning of F- | findings.md |
| T-nnn | Trap | traps.md |
| C-nn | Commissioning row | commissioning.md |
| CH1 to CH8 | Channel token | channel-token.md |
| LS-n | Float switch POSITION, not a part | the float requirement |
| **RUN-nnn** | **One physical cable run. NEW** | the cable schedule |
| **TRM-** | **One terminal. NEW, and its shape is INTERCONNECT's to propose** | the terminal schedule |
| **CDR-nnn** | **One conductor. NEW** | the wire table |

**A DOCUMENT THAT NEEDS A LOCAL LIST USES A PREFIX NOBODY ELSE COULD MEAN, keyed to
that document. Not a bare letter.** All three collisions found were made by BOSS or
AUDIT inventing a local list, never by a subsystem.

Status meanings:
- FROZEN: both ends may build against it. Changing it costs a BOSS decision
  and a dated entry in decisions.md.
- OPEN: not settled. The owner column names who must return the answer. Nobody
  builds against an OPEN row.

Scope boundary: tap water in, through to V3 the day tank outlet valve.
Everything downstream of V3 exists, operates, and is out of scope.

No counts, sizes, gauges, terminal numbers or part numbers appear in this file
until a subsystem returns them with a datasheet behind them.

## Fluid crossings

| ID | End A | End B | Status | Owner of the open item |
|---|---|---|---|---|
| FL-01 | Building cold water supply | WATER: fill solenoid inlet | OPEN | WATER. **AND IT CARRIES THE AIR GAP, D-138: this crossing is where municipal supply meets a tank of nutrient solution, and the air gap is the backflow measure. NOT a separate row - it is a property of this crossing** |
| FL-02 | WATER: fill solenoid outlet | WATER: storage tank inlet | internal to WATER | WATER |
| FL-03 | WATER: manifold pump discharge | DOSING: manifold inlet union | OPEN | WATER and DOSING jointly, BOSS freezes |
| FL-04 | DOSING: manifold outlet union | WATER: return drop to day tank | OPEN | WATER and DOSING jointly, BOSS freezes |
| FL-05 | DOSING: dose delivery tubing | PUMP-BOXES: head discharge end, 3/16 in barb | **SIZE CLOSED 2026-08-30 by parts.md**: 3/16 in straight connector mating 4.8 mm ID tube. The fixed-tube null head means external tubing joins at the ends of the short BPT piece, so this crossing is external tubing to barb and never involves the pump tube. Still open: DOSING's tubing selection against chemical compatibility and translucency, D-019 | DOSING |
| FL-06 | DOSING: jug suction tubing | PUMP-BOXES: head suction end, 3/16 in barb | As FL-05. **This unblocks the F-002 proposal, which was blocked on FL-06** | DOSING |
| FL-10 | PUMP-BOXES: the head, a mechanical mount that happens to have a tube in it | DOSING: the pump tube, PharMed BPT B25, wetted, consumable at about 1000 h | **CLOSED 2026-08-30 by D-028. DOSING owns the pump tube**, including the change interval, the change procedure, and telling CONTROL-SOFTWARE that C-01 is void for that channel after a change. PUMP-BOXES stops at the barb per D-006 | closed |
| FL-11 | WATER: day tank overflow bulkhead | WATER: the floor track drain | **NEW 2026-09-04, D-153. A requirement under D-130 that had no row after two irreversible holes were made requirements.** Entry point is FREE, D-147. Lands ABOVE the high-high mark unless WATER returns a reason, D-134 | WATER |
| FL-12 | WATER: storage tank overflow bulkhead | WATER: the floor track drain | **NEW 2026-09-04, D-153.** As FL-11 | WATER |
| FL-07 | DOSING: injection ports | DOSING: manifold body | internal to DOSING | DOSING |
| FL-08 | WATER: chiller loop submersible and return | WATER: chiller ports | internal to WATER | WATER |
| FL-09 | WATER: day tank outlet | V3 inlet | FROZEN as the scope boundary. V3 is manual, nothing in this project actuates it, nothing downstream is designed here | closed |

FL-05 and FL-06 are the seam that had no owner in the first agent proposal. Both
ends are now named. DOSING owns the whole wet path from manifold to head to
jug, including jug placement and how a jug is changed. PUMP-BOXES owns the head
and stops at the barb.

## Power crossings

| ID | End A | End B | Status | Owner of the open item |
|---|---|---|---|---|
| P-01 | Building branch circuit | MAIN-PANEL: line input | OPEN | MAIN-PANEL |
| P-02 | MAIN-PANEL: fill solenoid relay output | WATER: fill solenoid coil | OPEN. Solenoid coil voltage is undecided and the relay contact rating depends on it | WATER returns the solenoid requirement, MAIN-PANEL sizes the contact |
| P-03 | MAIN-PANEL: relay-switched receptacle, PANEL MOUNTED in the enclosure face | WATER: transfer pump cord, plugged in from OUTSIDE | Mounting CLOSED 2026-08-30 by D-046: receptacles are panel mounted and cords are not fed through grips. MAIN-PANEL places them. Circuit and rating still open | MAIN-PANEL |
| P-04 | MAIN-PANEL: relay-switched receptacle, PANEL MOUNTED in the enclosure face | WATER: manifold pump cord, plugged in from OUTSIDE | As P-03, D-046 | MAIN-PANEL |
| P-05 | MAIN-PANEL: chiller contactor, own circuit | WATER: chiller and chiller loop submersible, switched together | OPEN | MAIN-PANEL |
| P-06 | MAIN-PANEL: permissive contactor load side | PUMP-BOXES: stepper driver VM distribution | OPEN, and sharpened 2026-08-30 by parts.md. This is the conductor the permissive removes. It carries VM, from a rail that is settable 23.76 to 28.28 V with nothing fixing the trim, F-010. Both ends must agree on voltage, conductor and gland before either box is built, and PUMP-BOXES must return the 6121's VM range from the datasheet first | MAIN-PANEL and PUMP-BOXES jointly, BOSS freezes |
| P-09 | DISPLAY-BOX: 5 V rail, the Pi's own supply, UNSWITCHED | PUMP-BOXES: the 6121's VDD logic supply pin | **SOURCE CLOSED 2026-08-30 by D-031. VDD is not "power" under G-09: the permissive removes MOTOR supply only and VDD stays live.** Reasons: a second switched supply to both boxes would be new conductors, terminals and a failure mode to switch off a few milliamps; **it would create a state the drivers must never see, buffer outputs at 5 V driving STEP and DIR into pins whose VDD is zero, an overdrive through the input protection diodes on all eight drivers on every permissive drop**; and logic staying alive keeps DIAG and INDEX meaningful while the Pi is awake. **EN stays unwired and defaults ENABLED, D-032, so software has no per-driver disable, ever.** WHAT REMAINS OPEN: what a 6121 does with STEP asserted and VM absent, and what software must do so it is not clocking into a dead rail | PUMP-BOXES, from the chip datasheet AND the board schematic. Both documents, mapping established first |
| P-07 | MAIN-PANEL: fused, NOT relay switched receptacle | DISPLAY-BOX: Pi power | **CLOSED 2026-08-30 by parts.md.** The Pi is powered independently of everything else. It has power whenever the panel does, stays alive through a permissive drop, and can log and alert on it. No software may assume it loses power with the system. **Nothing in the panel can power cycle the Pi: it reboots by software or by killing the panel, so a watchdog is the only recovery path**. **FORM SETTLED 2026-09-04, D-162. THE AC-DC CONVERSION IS OUTSIDE BOTH ENCLOSURES: a 27 W USB-C brick on an UNSWITCHED RECEPTACLE ON THE MAIN PANEL FACE. What crosses to the display box is 5 V DC over a USB-C cable, NOT LINE.** And the crossing is a **BULKHEAD, NOT A GRIP**, for a physical reason: **a USB-C connector will not pass a grip bore, and cutting and re-terminating a USB-C cable is not a thing anyone should do.** Panel-mount USB-C bulkhead at the display box face | closed. The watchdog is CONTROL-SOFTWARE's and DISPLAY-BOX's |
| P-08 | MAIN-PANEL: 24 V supply | MAIN-PANEL: relay and contactor coils | internal to MAIN-PANEL | MAIN-PANEL |

## Signal crossings

| ID | End A | End B | Status | Owner of the open item |
|---|---|---|---|---|
| S-01 | WATER: storage tank floats, pilot duty | MAIN-PANEL: fill relay seal-in chain | OPEN. WATER owns which floats, their type and where they sit. MAIN-PANEL owns the relay chain and the contact rating it needs. **MOUNTING METHOD ADOPTED 2026-09-03, D-121: THE STANDPIPE. One rigid pipe per tank carrying every float and every cord, hung off the rim, nothing hanging off a float body. METHOD ONLY - no dimension, no material, no attachment detail, no count.** **The row stays OPEN on which floats, their type and their positions: D-118 struck the inherited LS roster and the float pass RESTARTS FROM REQUIREMENTS - what a float must DO at each position, then a part.** F-089 goes into that requirement: the contact must switch a 24 V control circuit, and under G-31 that is a fifth of the power of the 120 VAC coil the old set's floats were rated for. **Heights are NOT adopted from any source** | split, see the note below |
| S-02 | WATER: day tank floats, pilot duty | MAIN-PANEL: transfer relay seal-in chain | OPEN. **MOUNTING METHOD ADOPTED 2026-09-03, D-121: THE STANDPIPE. One rigid pipe per tank carrying every float and every cord, hung off the rim, nothing hanging off a float body. METHOD ONLY - no dimension, no material, no attachment detail, no count.** **The row stays OPEN on which floats, their type and their positions: D-118 struck the inherited LS roster and the float pass RESTARTS FROM REQUIREMENTS - what a float must DO at each position, then a part.** F-089 goes into that requirement: the contact must switch a 24 V control circuit, and under G-31 that is a fifth of the power of the 120 VAC coil the old set's floats were rated for. **Heights are NOT adopted from any source** | split, see the note below |
| S-03 | MAIN-PANEL: the NORMALLY CLOSED contact of a 55.34, wetted at 24 V, single series branch through an optocoupler LED, burden in the MAIN PANEL | DISPLAY-BOX: isolated Pi input, sense inverted | **CLOSED 2026-08-30 by D-042, and closed BY INVERSION rather than by logic.** No dose may start during a fill: a fill changes tank volume while a dose is computed against it, and every verification here is a delayed tank reading, so a fill inside a settle window corrupts the measurement. **Wired so CLOSED means NO FILL and OPEN means FILLING, a severed cable reads as filling, dosing is inhibited, and the failure is a stop rather than a permission.** Same relay, same circuit, same roughly 12.5 mA under G-23, different pole. See traps.md T-016. **AMENDED 2026-09-04, D-157: THIS ROW IS A TWO-CONDUCTOR PAIR FROM ONE CHANGEOVER POLE. Its NC leg is the fill-in-progress sense; its NO leg is the D-042 dose-inhibit leg to a second isolated Pi input, carried on RUN-007.** MAIN-PANEL found the conductor had no row and the fix is to amend this one rather than create a new one - **under G-45 two rows would be a written contract where one row is a mechanism.** G-27 applies: both legs at the same potential on the same cable, and any state where both agree is a broken sense path | closed. DISPLAY-BOX's input side remains part of S-12 |
| S-20 | MAIN-PANEL: second pole of K-DRY, a 55.34 contact | DISPLAY-BOX: isolated Pi input | **OPEN AND NEW 2026-08-30, created by D-038.** The dry-run element's contact drives K-DRY, which latches and drops the manifold pump in hardware; a second pole of the same relay reports to the Pi so the VERIFICATION judgement is made in software under G-16. **A third instance of S-03's circuit shape, and it had no row.** Sized independently under G-23: 55.34 minimum, single series branch, burden in the panel, sense inverted, and **its fail direction is established rather than inherited, per F-017's lesson**. **AMENDED 2026-09-04, D-157: THIS ROW IS A TWO-CONDUCTOR PAIR FROM ONE CHANGEOVER POLE.** Its second leg is S-20's complement on the NC leg of the same K-DRY pole, carried on RUN-008. Amended rather than split, per G-45. G-27 applies as above | MAIN-PANEL and DISPLAY-BOX jointly. Blocked on WATER returning the S-05 element, which is now unblocked from MAIN-PANEL's side |
| S-04 | WATER: leak detection sensor placement | MAIN-PANEL: leak console into the permissive chain | OPEN | split, see the note below |
| S-05 | WATER: dry run sense element | MAIN-PANEL: dry run interlock relay | OPEN, and DELIBERATELY HELD 2026-08-30. WATER established that S-05 and F-003 are TWO questions with one asymmetrically available shared answer: a FLOW-proving element senses the result and can also catch a dry tank, so it can subsume dry-run protection, while a LEVEL element senses the supply and can NEVER subsume circulation verification, because it reads healthy through a fouled impeller, an air-locked volute, a blocked intake and a shut valve. **Choosing a level-based answer here forecloses the shared solution. S-05 must not be answered before F-003 is.** They also want opposite timing: dry-run must act fast, circulation verification must not act on a start-up transient, and that conflict lands in MAIN-PANEL's chain | **CLOSED 2026-09-03 BY D-119, LEVEL-BASED, BY THE OWNER. Everything in this system is level switches; there is no flow element anywhere and there is not going to be one.** **The SHARED SOLUTION IS SPENT DELIBERATELY, not by default** - D-116's guard refused the same answer arriving from the 1st Edition set the day before, and a decision is not an inheritance. **CIRCULATION VERIFICATION DOES NOT VANISH and D-060's withdrawn overstatement does not return with the fork being taken: F-003 is separately assigned under D-016, C-12's temperature-step witness is free, and S-20 exists on either fork because circulation is a pole on K-DRY under D-058. What is gone is the FREE version.** D-060's other half is now spent too: level-based means NO TIMING ELEMENT, and that device is not bought. MAIN-PANEL still rules on whether a verification failure may drop the pump in hardware, which G-25 already answers no |
| S-06 | MAIN-PANEL: E-stop and manual reset in the permissive chain | operator, at the panel's top face | **CLOSED 2026-08-30 by D-048. The panel-face E-stop satisfies S-06 and there is no second remote E-stop.** Both devices are on the top face per parts.md, 22 mm, and INTERCONNECT does not place them on the wall | closed |
| S-07 | DISPLAY-BOX: logic board permissive coil drive | MAIN-PANEL: permissive contactor coil | OPEN. Termination A of the permissive chain. **Findings F-019: a severed drive is fail-safe, but a SHORTED output device is not, and whether that can defeat G-07 depends on where the coil positive is taken from. Downstream of the master latch, G-07 holds. From raw 24 V, one shorted transistor defeats the E-stop. THIS ROW MUST STATE WHICH.** Also open: whether the logic board can drive a 22.32 coil directly at all, which decides whether the panel is short one relay or three, F-021 | MAIN-PANEL and DISPLAY-BOX jointly, BOSS freezes |
| S-08 | MAIN-PANEL: pole 2 of the 22.32, terminals 3 and 4, wetted from 24 V | DISPLAY-BOX: optocoupler transistor pulling a Pi input low | **SOURCE CLOSED 2026-08-30 by D-029. There is no auxiliary block: the readback is the second NO pole.** Pole 1 carries the 24 V rail to both pump boxes; pole 2 was free. The wetting circuit is recorded in parts.md AS GIVEN and is not to be re-derived: an optocoupler branch and a bare burden branch in parallel, sized for 45 to 55 mA against the 22.32's 1000 mW minimum, **the burden in the MAIN PANEL so the contact stays wetted if the cable is unplugged or a conductor breaks. The sense is INVERTED: contact closed means the Pi input goes LOW.** Software may never report commanded state as measured state. **The asymmetric discipline of D-030 applies to this signal** **G-22: a severed cable or a dead LED leaves the Pi input high, reads as contact open, reads as a drop. That is the safe state and it is a CHOSEN PROPERTY, not an inheritance.** | closed on the circuit. DISPLAY-BOX's input side still open |
| S-09 | DISPLAY-BOX: ONE logic board output, BCM 18, a ULN2003 SINKING the coil return, SUP-1 across the coil | MAIN-PANEL: the driver permissive contactor coil, and nothing else | **CORRECTED 2026-08-30 by D-052, and the row is now nearly empty: its old End B named four coils and G-26 removes all four. It should close as "no relay drive outputs" or MERGE INTO S-07, which is the same conductor.** DISPLAY-BOX's scope still says "relay coil drives", plural, and must be told. **The Pi does NOT drive: the day tank fill coil, the storage fill coil, the transfer pump (a POLE on the day tank fill relay), the manifold pump (a POLE on the dry-run interlock relay), or the chiller (a CONTACTOR). The Pi commands a permissive that GATES those circuits.** G-26 | BOSS to merge or close. T-006 and T-007 still apply to the one drive that exists |
| S-10 | DISPLAY-BOX: logic board step and direction outputs | PUMP-BOXES: the 6121's STEP and DIR screw terminals | OPEN. **THE WORST OUTCOME IN THE WHOLE FAIL-SAFE SWEEP LIVES ON THIS ROW: a severed DIR leaves the direction undefined on a driver that is enabled by default, so a head can run backwards, drawing from the manifold toward the jug, while the books decrement as though it dosed forward. Nothing measures direction and nothing measures delivery.** The fix is a PULL-DOWN AT EACH DRIVER INPUT, owned by PUMP-BOXES per D-043, because a pull at the display end does nothing once the conductor is cut. Carrying findings F-018: a severed STEP or DIR fails UNSAFE. Pull resistors are required AT THE DRIVER END, inside the pump boxes, because a pull at the display end does nothing once the conductor is cut. Plus a low-impedance drive at the display end: both, not either.** Also sharpened 2026-08-30 by parts.md. **The 6121 is a NON-ISOLATED CMOS breakout with screw terminals. There are no PUL+, DIR+ or differential pairs and there is no opto.** Anything drafted assuming an opto-isolated differential interface is already wrong and must be re-read against the real pin list: STEP DIR EN MS1 MS2 DIAG INDEX VDD GND VM 1A 1B 2A 2B. See traps.md T-015, which is the exact failure this is. Runs are short: 4 ft display to box A, 6 ft to box B, measured | DISPLAY-BOX and PUMP-BOXES jointly, BOSS freezes |
| S-11 | DOSING: pH, EC and PT-1000 probes in the manifold probe section | DISPLAY-BOX: EZO pH and EZO EC each on an ISCCB-2, EZO RTD on NO carrier | OPEN. DOSING owns the wet fitting and probe placement, DISPLAY-BOX owns the carriers and the I2C side, INTERCONNECT owns the cable run | split |
| S-12 | DISPLAY-BOX: Pi GPIO and I2C map | CONTROL-SOFTWARE: pin and address assignments | OPEN. Must be FROZEN in writing before either side builds. This is the seam that would otherwise live in one agent's head | DISPLAY-BOX proposes, CONTROL-SOFTWARE reviews by building against it, BOSS freezes |
| S-13 | DOSING: flow cell in the manifold | CONTROL-SOFTWARE: circulation knowledge | CLOSED as a signal. There is no flow signal into the Pi. The flow cell is a PVC body that holds the probes in the moving stream. It is a fitting, not an instrument: no output, no contact, no wire. Nobody has ever specified a sensor in it | closed by the owner 2026-08-30 |
| S-14 | CONTROL-SOFTWARE: fault registry | the named "no-circulation fault" | OPEN and UNVERIFIED. Searched 2026-08-30 by CONTROL-SOFTWARE with source access: no Pi application source in reach, so the question is not answerable from what can be read. See the search record in subsystems/control-software.md. Not present, not absent. Nothing builds against it | blocked on the owner saying where the code lives |
| S-15 | DOSING: EC probe in the manifold | CONTROL-SOFTWARE: implicit whole-loop check | FROZEN, corrected 2026-08-30 by D-024 after F-005. EC rise attributable to a dose is the only whole-loop check that exists. **The window is anchored to the dose and extends past the last commanded step by the settling interval.** The previous wording, "valid only during a dose", defined a window in which the evidence could not have arrived, because the probe reads the tank after recirculation. It is a DELAYED check, see F-004 and the two times t_first and t_settle. Nothing may treat it as per-channel or as valid at rest | settling interval OPEN, commissioning C-02 |
| S-16 | DOSING: pH probe in the manifold | CONTROL-SOFTWARE: attribution of the pH up and pH down channels | FROZEN 2026-08-30 by owner decision D-011, WITH TWO CONSTRAINTS THAT ARE PART OF THE ROW. (1) pH up and pH down cannot be attributed at the same time. If both fire in one batch the movements cancel and pH shows the net. Only one runs in a given correction, so attribute whichever was commanded, and a batch that fires both is a FAULT CONDITION which must not read as passing. (2) The probe is upstream of every injection point and reads the day tank, not the manifold, so the change appears only after the dose has circulated back and mixed. This is a delayed check with a settling time that nobody has measured. See findings.md F-004 | **CONSTRAINT 3, added 2026-09-01 by D-083: THE CHECK IS DIRECTION-AWARE. It compares a SIGNED movement against a signed prediction. A magnitude-only pH check attributes nothing and is a duplicate of S-15 wearing S-16's name.** And the sign comes from C-03's MEASUREMENT, never from the product name, G-32. Four outcomes, not three: pass, fail-no-movement, indeterminate, and WRONG DIRECTION kept distinct. | constraint 1 is CONTROL-SOFTWARE's to enforce. The settling time in constraint 2 is OPEN, DOSING and CONTROL-SOFTWARE between them |
| S-19 | CONTROL-SOFTWARE: the DEFINITION of channel N | every other subsystem, which CONSUMES it: DISPLAY-BOX at the S-12 pin map, INTERCONNECT at the cable core, PUMP-BOXES at the driver, head and box, DOSING at the tube, jug station and jug | OWNED 2026-08-30 by D-021, no longer a shared row. CONTROL-SOFTWARE declares what channel N is. Everyone else matches it and nobody else defines it. One token, eleven hops, no translation at any point. Reason for the change: as a shared row with four contributors it was lost twice. If the ends disagree, a head labelled N driven by software channel N+1 doses the wrong product every batch, permanently, AND PASSES EVERY CHECK, because S-16 attributes to the COMMANDED channel and G-05 decrements the commanded jug. A crossed pair confirms itself | CONTROL-SOFTWARE declares. Verified only by C-09, which is first in the commissioning order |
| S-18 | WATER: chiller loop, on KM-CHIL | CONTROL-SOFTWARE: verification windows | **REOPENED 2026-08-30 by D-059. It was CLOSED by D-027 on a mechanism that G-26 has removed.** D-027 replaced the chiller hold-off with sample tagging, and its mechanism was "the Pi commands the contactor, so it knows". **Under G-26 the Pi does NOT command the chiller. So it knows the chiller's state neither as commanded nor as measured, and the replacement mechanism has no source.** T-004's shape landing on a frozen row. Three ways out, none BOSS's: the Pi READS a contact on the chiller contactor, which G-26 permits since it restricts what the Pi drives and not what it reads, but which needs a spare pole on KM-CHIL that exists only if one pole can carry both chiller loads; or accept untagged samples; or the Pi drives the chiller after all, which contradicts G-26 | Owner. **And a plain absence with what was read to establish it: NOTHING STATES WHAT ENERGISES THE CHILLER CONTACTOR COIL under G-26. The one state in the panel whose driver is unaccounted for** |
| S-17 | **The channel whose assigned PRODUCT is fulvic** | any attribution mechanism | CLOSED as unattributed, by owner decision D-013. It moves neither EC nor pH meaningfully. One unattributed channel out of eight is accepted. Do not solve it. **REWORDED 2026-09-03 BY D-122, and the wording is the point: THERE IS NO FULVIC CHANNEL. This row previously read "Fulvic channel" as if it were a fixed identity, which is what D-105 removed.** **Fulvic is a NUTRIENT by role. Not moving EC meaningfully is a PRODUCT attribute and lives in the channel register under G-33, so it follows the product to whichever channel is assigned it - and it is bound at C-09, not derivable from the role setting.** D-107 and F-078 stand alongside: the premise is unmeasured, and C-04's "per EC-moving channel" scope excludes it from the only measurement that could falsify it | closed |

Note on the split rows S-01, S-02 and S-04. The permissive and interlock chains
are electrically MAIN-PANEL's. The devices in those chains sit in tanks and on
floors that WATER owns. Neither agent owns both halves and neither may assume
the other. WATER returns the device requirement, the search term and the
physical location. MAIN-PANEL returns the chain, the contact duty it needs and
the terminal it lands on. BOSS holds the row until both halves are in.

## Enclosure and cable crossings

| ID | End A | End B | Status | Owner of the open item |
|---|---|---|---|---|
| CBL-01 | MAIN-PANEL: glands | INTERCONNECT: cable runs on the wall | OPEN | INTERCONNECT owns the run, MAIN-PANEL owns what is inside its gland |
| CBL-02 | PUMP-BOXES: glands | INTERCONNECT: cable runs | OPEN | as CBL-01 |
| CBL-03 | DISPLAY-BOX: glands | INTERCONNECT: cable runs | OPEN | as CBL-01 |
| CBL-04 | WATER: field devices, floats, solenoid, leak sensors, pump cords | INTERCONNECT: field cable runs | OPEN | as CBL-01 |
| CBL-06 | MAIN-PANEL: leak console, 24 V in, Form C dry contact out | INTERCONNECT: the leak console cable | OPEN. **The console is POWERED, not a passive float. Its contact legs sit in the 120 V chain, so EVERY conductor in its cable must be insulated for 600 V**, including the 24 V supply pair sharing that jacket. **CONFIRMED 2026-09-04, D-163: the console is REMOTE, in no enclosure. It sits outside the main panel, fed 24 V through its own cord grip, with the sensor on the floor. Its position on the wall is the OWNER'S and is not fixed.** The 600 V insulation requirement is the same rule applied to the float cords by D-156, arriving from the other direction: **the cable is rated for the highest voltage in the bundle even though the console runs on 24 V** | INTERCONNECT selects the cable, MAIN-PANEL states the legs |
| CBL-07 | All four enclosures | INTERCONNECT: equipment grounding | **CLOSED 2026-09-04 BY D-165, SHAPE GIVEN BY THE OWNER.** The display box is polycarbonate and the pump boxes are plastic, so there is no bonding path through any of them. **A COPPER GROUND BAR IN THE MAIN PANEL IS THE SINGLE POINT. Each remote enclosure has its OWN LOCAL BAR, and a GREEN CONDUCTOR INSIDE THE CROSS-BOX CABLE joins the local bar to the main one - the bars are daisied home rather than every device running back to the main panel.** **So the EGC is a conductor inside each run and NOT a separate bonding cable, which retires RUN-017 under D-149.** **NOTHING BONDS ANYWHERE ELSE, and that is written down because a builder who finds a convenient screw will use it.** **And the bar is a terminal that is always in the 120 V chain even in a box holding only 24 V, because the ground is common - so whatever insulates a conductor landing there is rated for the highest voltage ANYWHERE ON THE BAR** | MAIN-PANEL provides the bar, INTERCONNECT lands the runs |
| CBL-05 | PUMP-BOXES: lid penetrations for the heads | DOSING: tubing passing the lid | OPEN | PUMP-BOXES owns the penetration, DOSING owns the tubing through it |

## Mechanical and placement crossings

| ID | End A | End B | Status | Owner of the open item |
|---|---|---|---|---|
| M-01 | WATER: day tank penetrations and hangers | WATER internal, but both submersible cords and the manifold return pass through it | internal to WATER | WATER |
| M-02 | DOSING: manifold mounted on the dosing wall | PUMP-BOXES mounted on the same wall | OPEN. Both claim wall space and the tubing between them sets the spacing | DOSING and PUMP-BOXES jointly, INTERCONNECT arbitrates the wall layout |
| M-03 | DISPLAY-BOX: enclosure on the wall | operator reach and sightline | OPEN | DISPLAY-BOX |

## The gland boundary. ALLOCATED 2026-09-04 by D-146, to break a four-way deadlock.

**CBL-01 through CBL-04 each say the enclosure owner owns what is inside its gland
and INTERCONNECT owns the run. That left nobody able to move: all four enclosure
owners waited on INTERCONNECT for gland positions and INTERCONNECT waited on all
four.** INTERCONNECT declined to break it under rule 5 and was right to - **an
allocation of decision rights is an interface decision, so it belongs here.**

**THE ALLOCATION. It is a rule about WHO DECIDES, not a dimension:**

| Decision | Owner | Why it can be made without the other |
|---|---|---|
| **WHICH FACE a cable enters, and the ORDER of entries on that face** | **The enclosure owner** | It follows from what is inside the box and from D-047's shed rule. **The main panel's faces are already partly fixed by the owner: five 22 mm holes on top, cord grips on the bottom** |
| **WHERE on that face, and the spacing between glands** | **INTERCONNECT** | It follows from the wall layout and the approach direction of the run |

**So neither waits.** An enclosure owner states faces and order without knowing a
run. INTERCONNECT positions within a stated face.

**IF AN ENCLOSURE OWNER CANNOT STATE A FACE WITHOUT KNOWING THE RUN, THAT IS A
FINDING TO REPORT, NOT A REASON TO WAIT.** BOSS wants to know which box and why -
**it would mean that box's contents are being decided by its cabling rather than the
other way round.**

**BOSS states no gland count, no spacing, no face dimension and no position.**

