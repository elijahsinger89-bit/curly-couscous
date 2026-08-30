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
| F-05 | DOSING: dose delivery tubing | PUMP-BOXES: head discharge barb | OPEN | DOSING and PUMP-BOXES jointly, BOSS freezes |
| F-06 | DOSING: jug suction tubing | PUMP-BOXES: head suction barb | OPEN | DOSING and PUMP-BOXES jointly, BOSS freezes |
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
| P-06 | MAIN-PANEL: permissive contactor load side | PUMP-BOXES: stepper driver power distribution | OPEN. This is the conductor that the permissive removes. Both ends must agree on voltage, conductor and gland before either box is built | MAIN-PANEL and PUMP-BOXES jointly, BOSS freezes |
| P-07 | MAIN-PANEL: 24 V supply | DISPLAY-BOX: Pi and logic board power | OPEN | MAIN-PANEL and DISPLAY-BOX jointly |
| P-08 | MAIN-PANEL: 24 V supply | MAIN-PANEL: relay and contactor coils | internal to MAIN-PANEL | MAIN-PANEL |

## Signal crossings

| ID | End A | End B | Status | Owner of the open item |
|---|---|---|---|---|
| S-01 | WATER: storage tank floats, pilot duty | MAIN-PANEL: fill relay seal-in chain | OPEN. WATER owns which floats, their type and where they sit. MAIN-PANEL owns the relay chain and the contact rating it needs | split, see the note below |
| S-02 | WATER: day tank floats, pilot duty | MAIN-PANEL: transfer relay seal-in chain | OPEN | split, see the note below |
| S-03 | MAIN-PANEL: day tank fill in progress dry contact | DISPLAY-BOX: logic board input, then CONTROL-SOFTWARE | OPEN. This is the only level information the Pi has | MAIN-PANEL and DISPLAY-BOX jointly |
| S-04 | WATER: leak detection sensor placement | MAIN-PANEL: leak console into the permissive chain | OPEN | split, see the note below |
| S-05 | WATER: dry run sense element | MAIN-PANEL: dry run interlock relay | OPEN. What it senses is undecided. Nothing may be built against this row | WATER returns the sensing method, MAIN-PANEL wires it |
| S-06 | MAIN-PANEL: E-stop and manual reset in the permissive chain | operator, mounted location | OPEN | MAIN-PANEL owns the chain, INTERCONNECT owns where it lands on the wall |
| S-07 | DISPLAY-BOX: logic board permissive coil drive | MAIN-PANEL: permissive contactor coil | OPEN. Termination A of the permissive chain | MAIN-PANEL and DISPLAY-BOX jointly, BOSS freezes |
| S-08 | MAIN-PANEL: permissive contactor auxiliary contact | DISPLAY-BOX: logic board readback input | OPEN. Termination B of the permissive chain. Exists so a welded contact is detected rather than assumed | MAIN-PANEL and DISPLAY-BOX jointly, BOSS freezes |
| S-09 | DISPLAY-BOX: logic board relay drive outputs | MAIN-PANEL: fill, transfer, circulation and chiller coils | OPEN | MAIN-PANEL and DISPLAY-BOX jointly |
| S-10 | DISPLAY-BOX: logic board step and direction outputs | PUMP-BOXES: stepper driver step and direction inputs | OPEN | DISPLAY-BOX and PUMP-BOXES jointly, BOSS freezes |
| S-11 | DOSING: pH, EC and PT-1000 probes in the manifold probe section | DISPLAY-BOX: EZO circuits on the ISCCB-2 carriers | OPEN. DOSING owns the wet fitting and probe placement, DISPLAY-BOX owns the carriers and the I2C side, INTERCONNECT owns the cable run | split |
| S-12 | DISPLAY-BOX: Pi GPIO and I2C map | CONTROL-SOFTWARE: pin and address assignments | OPEN. Must be FROZEN in writing before either side builds. This is the seam that would otherwise live in one agent's head | DISPLAY-BOX proposes, CONTROL-SOFTWARE reviews by building against it, BOSS freezes |
| S-13 | Loop circulation detection, method not established | CONTROL-SOFTWARE: no-circulation fault | OPEN. See the open question in subsystems/dosing.md. A flow cell and a no-circulation fault are both stated to exist, but how the Pi learns the loop is moving has not been established and BOSS has not checked it against any device | BOSS to ask the owner, then route |

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
| C-05 | PUMP-BOXES: lid penetrations for the heads | DOSING: tubing passing the lid | OPEN | PUMP-BOXES owns the penetration, DOSING owns the tubing through it |

## Mechanical and placement crossings

| ID | End A | End B | Status | Owner of the open item |
|---|---|---|---|---|
| M-01 | WATER: day tank penetrations and hangers | WATER internal, but both submersible cords and the manifold return pass through it | internal to WATER | WATER |
| M-02 | DOSING: manifold mounted on the dosing wall | PUMP-BOXES mounted on the same wall | OPEN. Both claim wall space and the tubing between them sets the spacing | DOSING and PUMP-BOXES jointly, INTERCONNECT arbitrates the wall layout |
| M-03 | DISPLAY-BOX: enclosure on the wall | operator reach and sightline | OPEN | DISPLAY-BOX |
