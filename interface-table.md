# Interface table

Every crossing between subsystems, both ends named. BOSS owns this file. No
subsystem edits it. A subsystem that finds a boundary defect reports it here
through BOSS and does not fix it.

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
| F-01 | Building cold water supply | WATER: fill solenoid inlet | OPEN | WATER |
| F-02 | WATER: fill solenoid outlet | WATER: storage tank inlet | internal to WATER | WATER |
| F-03 | WATER: circulation submersible discharge | DOSING: manifold inlet union | OPEN | WATER and DOSING jointly, BOSS freezes |
| F-04 | DOSING: manifold outlet union | WATER: return drop to day tank | OPEN | WATER and DOSING jointly, BOSS freezes |
| F-05 | DOSING: dose delivery tubing | PUMP-BOXES: head discharge end, 3/16 in barb | **SIZE CLOSED 2026-08-30 by parts.md**: 3/16 in straight connector mating 4.8 mm ID tube. The fixed-tube null head means external tubing joins at the ends of the short BPT piece, so this crossing is external tubing to barb and never involves the pump tube. Still open: DOSING's tubing selection against chemical compatibility and translucency, D-019 | DOSING |
| F-06 | DOSING: jug suction tubing | PUMP-BOXES: head suction end, 3/16 in barb | As F-05. **This unblocks the F-002 proposal, which was blocked on F-06** | DOSING |
| F-10 | PUMP-BOXES: the head, a mechanical mount that happens to have a tube in it | DOSING: the pump tube, PharMed BPT B25, wetted, consumable at about 1000 h | **CLOSED 2026-08-30 by D-028. DOSING owns the pump tube**, including the change interval, the change procedure, and telling CONTROL-SOFTWARE that C-01 is void for that channel after a change. PUMP-BOXES stops at the barb per D-006 | closed |
| F-07 | DOSING: injection ports | DOSING: manifold body | internal to DOSING | DOSING |
| F-08 | WATER: chiller loop submersible and return | WATER: chiller ports | internal to WATER | WATER |
| F-09 | WATER: day tank outlet | V3 inlet | FROZEN as the scope boundary. V3 is manual, nothing in this project actuates it, nothing downstream is designed here | closed |

F-05 and F-06 are the seam that had no owner in the first agent proposal. Both
ends are now named. DOSING owns the whole wet path from manifold to head to
jug, including jug placement and how a jug is changed. PUMP-BOXES owns the head
and stops at the barb.

## Power crossings

| ID | End A | End B | Status | Owner of the open item |
|---|---|---|---|---|
| P-01 | Building branch circuit | MAIN-PANEL: line input | OPEN | MAIN-PANEL |
| P-02 | MAIN-PANEL: fill solenoid relay output | WATER: fill solenoid coil | OPEN. Solenoid coil voltage is undecided and the relay contact rating depends on it | WATER returns the solenoid requirement, MAIN-PANEL sizes the contact |
| P-03 | MAIN-PANEL: relay-switched receptacle | WATER: transfer pump cord | OPEN | MAIN-PANEL |
| P-04 | MAIN-PANEL: relay-switched receptacle | WATER: circulation submersible cord | OPEN | MAIN-PANEL |
| P-05 | MAIN-PANEL: chiller contactor, own circuit | WATER: chiller and chiller loop submersible, switched together | OPEN | MAIN-PANEL |
| P-06 | MAIN-PANEL: permissive contactor load side | PUMP-BOXES: stepper driver VM distribution | OPEN, and sharpened 2026-08-30 by parts.md. This is the conductor the permissive removes. It carries VM, from a rail that is settable 23.76 to 28.28 V with nothing fixing the trim, F-010. Both ends must agree on voltage, conductor and gland before either box is built, and PUMP-BOXES must return the 6121's VM range from the datasheet first | MAIN-PANEL and PUMP-BOXES jointly, BOSS freezes |
| P-09 | Wherever VDD comes from | PUMP-BOXES: the 6121's VDD logic supply pin, 3.3 to 5 V | **OPEN AND NEW 2026-08-30. Nobody has said where VDD comes from or whether the permissive removes it.** parts.md: VDD is a separate logic supply, the motor terminal block does not generate it, and with VDD unconnected the driver does not respond to STEP or DIR at all. So the permissive contactor removing VM does not by itself de-power the logic side. Both cases must be reasoned about explicitly: VM present with VDD absent, and VDD present with VM absent. Also on this row: **EN unwired leaves the driver ENABLED**, so the power-up default is on, not off | DISPLAY-BOX, PUMP-BOXES and MAIN-PANEL jointly. Nothing is built against it |
| P-07 | MAIN-PANEL: fused, NOT relay switched receptacle | DISPLAY-BOX: Pi power | **CLOSED 2026-08-30 by parts.md.** The Pi is powered independently of everything else. It has power whenever the panel does, stays alive through a permissive drop, and can log and alert on it. No software may assume it loses power with the system. **Nothing in the panel can power cycle the Pi: it reboots by software or by killing the panel, so a watchdog is the only recovery path** | closed. The watchdog is CONTROL-SOFTWARE's and DISPLAY-BOX's |
| P-08 | MAIN-PANEL: 24 V supply | MAIN-PANEL: relay and contactor coils | internal to MAIN-PANEL | MAIN-PANEL |

## Signal crossings

| ID | End A | End B | Status | Owner of the open item |
|---|---|---|---|---|
| S-01 | WATER: storage tank floats, pilot duty | MAIN-PANEL: fill relay seal-in chain | OPEN. WATER owns which floats, their type and where they sit. MAIN-PANEL owns the relay chain and the contact rating it needs | split, see the note below |
| S-02 | WATER: day tank floats, pilot duty | MAIN-PANEL: transfer relay seal-in chain | OPEN | split, see the note below |
| S-03 | MAIN-PANEL: day tank fill in progress dry contact | DISPLAY-BOX: logic board input, then CONTROL-SOFTWARE | OPEN. The only level information the Pi has. **Minimum switching load applies here, F-011: a 3.3 V logic input draws far less than either contact's minimum and an under-loaded contact oxidises** | MAIN-PANEL and DISPLAY-BOX jointly |
| S-04 | WATER: leak detection sensor placement | MAIN-PANEL: leak console into the permissive chain | OPEN | split, see the note below |
| S-05 | WATER: dry run sense element | MAIN-PANEL: dry run interlock relay | OPEN, and DELIBERATELY HELD 2026-08-30. WATER established that S-05 and F-003 are TWO questions with one asymmetrically available shared answer: a FLOW-proving element senses the result and can also catch a dry tank, so it can subsume dry-run protection, while a LEVEL element senses the supply and can NEVER subsume circulation verification, because it reads healthy through a fouled impeller, an air-locked volute, a blocked intake and a shut valve. **Choosing a level-based answer here forecloses the shared solution. S-05 must not be answered before F-003 is.** They also want opposite timing: dry-run must act fast, circulation verification must not act on a start-up transient, and that conflict lands in MAIN-PANEL's chain | WATER holds it open on purpose, not as a stall. MAIN-PANEL must rule on whether a verification failure may drop the pump in hardware |
| S-06 | MAIN-PANEL: E-stop and manual reset in the permissive chain | operator, mounted location | OPEN | MAIN-PANEL owns the chain, INTERCONNECT owns where it lands on the wall |
| S-07 | DISPLAY-BOX: logic board permissive coil drive | MAIN-PANEL: permissive contactor coil | OPEN. Termination A of the permissive chain | MAIN-PANEL and DISPLAY-BOX jointly, BOSS freezes |
| S-08 | MAIN-PANEL: permissive contactor auxiliary contact | DISPLAY-BOX: logic board readback input | OPEN. Termination B of the permissive chain. Exists so a welded contact is detected rather than assumed, and **software may never report commanded state as measured state anywhere.** **Minimum switching load applies, F-011, and it matters more here than anywhere: an oxidised aux contact fails intermittently, and an intermittently open readback either reports a welded contactor that is fine or misses one that is not** | MAIN-PANEL and DISPLAY-BOX jointly, BOSS freezes |
| S-09 | DISPLAY-BOX: logic board relay drive outputs | MAIN-PANEL: fill, transfer, circulation and chiller coils | OPEN | MAIN-PANEL and DISPLAY-BOX jointly |
| S-10 | DISPLAY-BOX: logic board step and direction outputs | PUMP-BOXES: the 6121's STEP and DIR screw terminals | OPEN, and sharpened 2026-08-30 by parts.md. **The 6121 is a NON-ISOLATED CMOS breakout with screw terminals. There are no PUL+, DIR+ or differential pairs and there is no opto.** Anything drafted assuming an opto-isolated differential interface is already wrong and must be re-read against the real pin list: STEP DIR EN MS1 MS2 DIAG INDEX VDD GND VM 1A 1B 2A 2B. See traps.md T-015, which is the exact failure this is. Runs are short: 4 ft display to box A, 6 ft to box B, measured | DISPLAY-BOX and PUMP-BOXES jointly, BOSS freezes |
| S-11 | DOSING: pH, EC and PT-1000 probes in the manifold probe section | DISPLAY-BOX: EZO pH and EZO EC each on an ISCCB-2, EZO RTD on NO carrier | OPEN. DOSING owns the wet fitting and probe placement, DISPLAY-BOX owns the carriers and the I2C side, INTERCONNECT owns the cable run | split |
| S-12 | DISPLAY-BOX: Pi GPIO and I2C map | CONTROL-SOFTWARE: pin and address assignments | OPEN. Must be FROZEN in writing before either side builds. This is the seam that would otherwise live in one agent's head | DISPLAY-BOX proposes, CONTROL-SOFTWARE reviews by building against it, BOSS freezes |
| S-13 | DOSING: flow cell in the manifold | CONTROL-SOFTWARE: circulation knowledge | CLOSED as a signal. There is no flow signal into the Pi. The flow cell is a PVC body that holds the probes in the moving stream. It is a fitting, not an instrument: no output, no contact, no wire. Nobody has ever specified a sensor in it | closed by the owner 2026-08-30 |
| S-14 | CONTROL-SOFTWARE: fault registry | the named "no-circulation fault" | OPEN and UNVERIFIED. Searched 2026-08-30 by CONTROL-SOFTWARE with source access: no Pi application source in reach, so the question is not answerable from what can be read. See the search record in subsystems/control-software.md. Not present, not absent. Nothing builds against it | blocked on the owner saying where the code lives |
| S-15 | DOSING: EC probe in the manifold | CONTROL-SOFTWARE: implicit whole-loop check | FROZEN, corrected 2026-08-30 by D-024 after F-005. EC rise attributable to a dose is the only whole-loop check that exists. **The window is anchored to the dose and extends past the last commanded step by the settling interval.** The previous wording, "valid only during a dose", defined a window in which the evidence could not have arrived, because the probe reads the tank after recirculation. It is a DELAYED check, see F-004 and the two times t_first and t_settle. Nothing may treat it as per-channel or as valid at rest | settling interval OPEN, commissioning C-02 |
| S-16 | DOSING: pH probe in the manifold | CONTROL-SOFTWARE: attribution of the pH up and pH down channels | FROZEN 2026-08-30 by owner decision D-011, WITH TWO CONSTRAINTS THAT ARE PART OF THE ROW. (1) pH up and pH down cannot be attributed at the same time. If both fire in one batch the movements cancel and pH shows the net. Only one runs in a given correction, so attribute whichever was commanded, and a batch that fires both is a FAULT CONDITION which must not read as passing. (2) The probe is upstream of every injection point and reads the day tank, not the manifold, so the change appears only after the dose has circulated back and mixed. This is a delayed check with a settling time that nobody has measured. See findings.md F-004 | constraint 1 is CONTROL-SOFTWARE's to enforce. The settling time in constraint 2 is OPEN, DOSING and CONTROL-SOFTWARE between them |
| S-19 | CONTROL-SOFTWARE: the DEFINITION of channel N | every other subsystem, which CONSUMES it: DISPLAY-BOX at the S-12 pin map, INTERCONNECT at the cable core, PUMP-BOXES at the driver, head and box, DOSING at the tube, jug station and jug | OWNED 2026-08-30 by D-021, no longer a shared row. CONTROL-SOFTWARE declares what channel N is. Everyone else matches it and nobody else defines it. One token, eleven hops, no translation at any point. Reason for the change: as a shared row with four contributors it was lost twice. If the ends disagree, a head labelled N driven by software channel N+1 doses the wrong product every batch, permanently, AND PASSES EVERY CHECK, because S-16 attributes to the COMMANDED channel and G-05 decrements the commanded jug. A crossed pair confirms itself | CONTROL-SOFTWARE declares. Verified only by C-09, which is first in the commissioning order |
| S-18 | WATER: chiller loop, commanded by MAIN-PANEL's contactor | CONTROL-SOFTWARE: verification windows | **CLOSED 2026-08-30 by D-027, which REVERSES D-023. The chiller is NOT held off across settle windows.** At a 66 F setpoint in a 62 to 65 F room the compressor rarely runs, so a hold-off prevents a step that mostly is not happening, while G-12 guarantees it always stops the chiller loop submersible, which is in the day tank. A certain cost for an occasional benefit, and both effects concentrate in the same window. **Instead: every pH, EC and temperature sample is tagged with the chiller's COMMANDED state.** That is commanded, not measured, and no code may present it as measured | closed. Revisit only with data from C-02 and C-08 |
| S-17 | Fulvic channel | any attribution mechanism | CLOSED as unattributed, by owner decision D-013. It moves neither EC nor pH meaningfully. One unattributed channel out of eight is accepted. Do not solve it | closed |

Note on the split rows S-01, S-02 and S-04. The permissive and interlock chains
are electrically MAIN-PANEL's. The devices in those chains sit in tanks and on
floors that WATER owns. Neither agent owns both halves and neither may assume
the other. WATER returns the device requirement, the search term and the
physical location. MAIN-PANEL returns the chain, the contact duty it needs and
the terminal it lands on. BOSS holds the row until both halves are in.

## Enclosure and cable crossings

| ID | End A | End B | Status | Owner of the open item |
|---|---|---|---|---|
| C-01 | MAIN-PANEL: glands | INTERCONNECT: cable runs on the wall | OPEN | INTERCONNECT owns the run, MAIN-PANEL owns what is inside its gland |
| C-02 | PUMP-BOXES: glands | INTERCONNECT: cable runs | OPEN | as C-01 |
| C-03 | DISPLAY-BOX: glands | INTERCONNECT: cable runs | OPEN | as C-01 |
| C-04 | WATER: field devices, floats, solenoid, leak sensors, pump cords | INTERCONNECT: field cable runs | OPEN | as C-01 |
| C-06 | MAIN-PANEL: leak console, 24 V in, Form C dry contact out | INTERCONNECT: the leak console cable | OPEN. **The console is POWERED, not a passive float. Its contact legs sit in the 120 V chain, so EVERY conductor in its cable must be insulated for 600 V**, including the 24 V supply pair sharing that jacket | INTERCONNECT selects the cable, MAIN-PANEL states the legs |
| C-07 | All four enclosures | INTERCONNECT: equipment grounding | OPEN. **The display box is polycarbonate and the pump boxes are plastic, so there is no bonding path through any of them. Every equipment ground lands on a ground bar, not on a box** | MAIN-PANEL provides the bar, INTERCONNECT lands the runs |
| C-05 | PUMP-BOXES: lid penetrations for the heads | DOSING: tubing passing the lid | OPEN | PUMP-BOXES owns the penetration, DOSING owns the tubing through it |

## Mechanical and placement crossings

| ID | End A | End B | Status | Owner of the open item |
|---|---|---|---|---|
| M-01 | WATER: day tank penetrations and hangers | WATER internal, but both submersible cords and the manifold return pass through it | internal to WATER | WATER |
| M-02 | DOSING: manifold mounted on the dosing wall | PUMP-BOXES mounted on the same wall | OPEN. Both claim wall space and the tubing between them sets the spacing | DOSING and PUMP-BOXES jointly, INTERCONNECT arbitrates the wall layout |
| M-03 | DISPLAY-BOX: enclosure on the wall | operator reach and sightline | OPEN | DISPLAY-BOX |
