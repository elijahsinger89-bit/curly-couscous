# Decisions

Dated, with the reason. A reversed decision keeps both entries and says why.
BOSS owns this file.

## 2026-08-30

**D-001 Scope is tap water in, through to V3 the day tank outlet valve.**
Everything downstream of V3 exists and operates. Reason: stated by the owner as
a fixed boundary. V3 is manual and nothing in this project actuates it.

**D-002 Nine agents: WATER, DOSING, MAIN-PANEL, PUMP-BOXES, DISPLAY-BOX,
CONTROL-SOFTWARE, INTERCONNECT, INTEGRATOR, AUDIT.**
Reason: smallest set that covers the work on physical boundaries.

**D-003 STORAGE-AND-FILL and DAY-TANK-AND-LOOPS merged into WATER.**
Reason: owner correction. The proposed split created four crossings between two
agents doing the same discipline in the same room. Day tank floats sat in one
agent's tank and belonged to the other's fill chain. The transfer pump
discharged into the other agent's tank. Manifold suction and return were two
more. The owner does the plumbing himself and is proficient at it. The seams
cost something and bought nothing. Recorded in traps.md as T-001.

**D-004 CONTROL-SOFTWARE stays separate from DISPLAY-BOX even though they share
an enclosure.** Reason: the seam between them is a pin and address map. Frozen
in writing it is checkable by a second agent. Left inside one agent it is not.
This is a deliberate exception to dividing on physical boundaries and the only
one. Interface S-12.

**D-005 The permissive chain is owned physically by MAIN-PANEL.**
It crosses four subsystems and reaches the field: MAIN-PANEL builds the
electrical chain, DISPLAY-BOX drives the coil and reads the auxiliary contact,
PUMP-BOXES is the load it removes, WATER places the leak sensors and the float
devices. Its terminations S-07 and S-08 are BOSS-owned interfaces. Reason: a
chain that nobody owns at the ends is how this build fails.

**D-006 DOSING owns the whole wet path: manifold, injection ports, dose tubing,
suction tubing, the nutrient jugs, and how a jug is placed and changed.**
PUMP-BOXES ends at the head barb. Reason: owner correction. In the first
proposal the jugs and suction tubing were between two agents and owned by
neither. Recorded in traps.md as T-002.

## Owner decisions taken as given, not revisitable by any agent

These were stated by the owner as already decided. An agent that wants one
changed reports to BOSS and does not act.

| ID | Decision | Reason |
|---|---|---|
| G-01 | Float switches are hardwired to relays and invisible to the Pi | Level control is hardware, not software |
| G-02 | The Pi gets exactly one level signal: a dry contact saying a day tank fill is in progress | Deliberate. It is the only level information software has |
| G-03 | Storage and day tank fill use a start float and a stop float with relay seal-in between them | Fills to a level rather than chattering at one point |
| G-04 | No flow meters on the dosing lines. Nothing measures what a peristaltic pump actually delivered | Deliberate. The Pi commands a step count and books the volume as dispensed |
| G-05 | No level sensors on the nutrient jugs. Remaining volume is arithmetic against a user-entered full-jug volume, per channel | Deliberate. Do not add jug floats |
| G-06 | Only one dosing pump turns at a time, mandatory in software | Holds until a thermal measurement says otherwise |
| G-07 | The permissive chain is a hardwired series string. A leak, an E-stop or a lost interlock drops everything independent of the Pi | Safety is not in software |
| G-08 | The leak detection console is wired into the permissive chain and drops power in hardware | As G-07 |
| G-09 | The permissive contactor removes power from every stepper driver at once, and the Pi reads back an auxiliary contact | So a welded contact is detected rather than assumed |
| G-10 | Probes sit first in line in a vertical manifold section, ahead of every injection point | So a bubble cannot corrupt a reading and no injectate reaches a probe before mixing |
| G-11 | The circulation submersible takes suction at the day tank bottom | So the tank mixes |
| G-12 | The chiller and its loop pump are switched together by one contactor on their own circuit | The chiller has no internal pump |
| G-13 | E-stop and manual reset are in the permissive chain and are not software | As G-07 |
| G-14 | UL listing is not gating. Hobby build, no electrical inspection | Owner's stated condition. It does not license unsafe work |
| G-15 | The owner does all part lookups. Agents return a requirement and a search term and stop | No agent states a part number or a spec from memory |

## Parts the owner already has

Listed so no agent re-specifies them. Quantities beyond what is stated here are
not decided and no agent may assume one.

| Item | Note |
|---|---|
| 100 gal cone bottom storage tank, open top | WATER |
| 40 gal food-grade day tank, open top | WATER |
| Anbull transfer pump, 120 V corded | WATER |
| Two hi-flow submersibles, 120 V corded | WATER, one circulation and one chiller loop |
| JBJ Arctica DBE-200 chiller, 115 V, 6 A, no internal pump | WATER |
| All the PVC | WATER and DOSING |
| Eight peristaltic pump heads | PUMP-BOXES |
| Eight Adafruit 6121 TMC2209 stepper driver breakouts | PUMP-BOXES |
| Raspberry Pi 5 and a 7 inch touch display | DISPLAY-BOX |
| Three Atlas Scientific EZO circuits: pH, EC, PT-1000 | DISPLAY-BOX, probes wet-fitted by DOSING |
| Two ISCCB-2 carriers | DISPLAY-BOX |
| Four Finder 55.34 relays | MAIN-PANEL |
| Two Finder 22.32 contactors | MAIN-PANEL |
| Mean Well NDR-240-24 supply | MAIN-PANEL |
| Enclosure 20.7 x 16.6 in | MAIN-PANEL |
| Two plastic boxes | PUMP-BOXES |
| Enclosure for the display box | DISPLAY-BOX |

## Site conditions

| Fact | Source |
|---|---|
| Room 62 to 65 F year round on dehumidifying AC | owner |
| Under 60 percent humidity, not wet, but water moves tank to tank | owner |
| Four enclosures, cables run between them on a wall | owner |
| 36 plants served downstream of V3 | owner, out of scope |

**D-007 There is no flow signal into the Pi. The flow cell is a fitting, not an
instrument.** No output, no contact, no wire, no sensor ever specified. Reason:
established by the owner 2026-08-30 after BOSS refused to write interface S-13
in either direction. Interface S-13 is closed as a signal.

**D-008 The named "no-circulation fault" is unverified.** What raises it, or
whether anything does, is not established. Routed to CONTROL-SOFTWARE to answer
from the code rather than from anyone's memory. Recorded as neither present nor
absent. Interface S-14. Nothing builds against it.

**D-009 EC rise during a dose is the accepted whole-loop check, and it is
implicit rather than instrumented.** Reason: it is real, it costs nothing, and
it already exists. Frozen as interface S-15 with its three limits written into
findings.md F-001 so no agent mistakes it for per-channel verification or for a
check that works at rest.

**D-010 No sensor is added for per-channel dose verification.** The gap is
logged as findings.md F-001 and routed as an open design question: what it would
take, what it would cost, where it would land. DOSING answers for its path. If
the answer is a flow meter per channel the owner expects to decline it, and
wants that recorded as a decision he made rather than a gap nobody named.

**D-011 The pH probe attributes the pH up and pH down channels. S-15 is extended
and S-16 is frozen.** Reason: free, the hardware is bought and read
continuously, and it is the only per-channel attribution in the option list that
costs nothing. Two constraints are part of the decision and are not to be
recorded as clean:
- pH up and pH down cannot be attributed at the same time. If both fire in one
  batch the movements cancel and pH shows the net. Only one runs in a given
  correction, so attribute whichever was commanded. A batch that fires both is a
  fault condition and the check must not read as passing.
- The probes are upstream of every injection point and read the day tank, not
  the manifold. The change appears only after the dose has circulated back and
  mixed. This is a delayed check with a settling time, and nobody has measured
  it.

**D-012 Every implicit verification in this system is delayed by an unmeasured
interval.** The second constraint on D-011 applies to the EC check as well and
was not named when S-15 was frozen. All of it reads the tank after
recirculation. Logged as findings.md F-004 and routed to DOSING and
CONTROL-SOFTWARE between them: what settling time the checks require, what sets
it, and whether it can be derived from tank volume and loop flow or must be
measured at commissioning. If it is a measurement it goes on commissioning.md.

**D-013 Fulvic stays unattributed.** It moves neither EC nor pH meaningfully.
One unattributed channel out of eight, recorded, is acceptable. Nobody solves it.
Interface S-17 is closed on that basis.

**D-014 O-19, a flow meter on every dosing line, is off the table.** Not to be
brought back unless something changes. Reason: it is the most expensive option
in every column and it does not catch F-002, which a matched label and a keyed
coupling do. G-04 already forbade it; this is the owner declining it knowingly,
which is what D-010 asked for. The gap is now a decision he made rather than a
gap nobody named.

**D-015 F-002 outranks the option list.** The finding is the inversion, not the
failure: the cheapest options catch the failure the most expensive one cannot.
Matched identity at head, tube and jug, and keyed couplings, are to come back as
their own proposal, separate from the nineteen. Routed to DOSING.

**D-016 F-003 is assigned, not left in the gap.** Nothing verifies anything at
rest. WATER holds it as primary because it owns the circulation submersible, the
day tank and the placement of any sense element. MAIN-PANEL holds the other end
because it owns the relay and the dry run interlock chain. Neither may assume
the other has it. BOSS's note, not a design instruction: this sits next to the
already-open S-05, where WATER owes what the dry run interlock senses. Whether
those are one question or two is for WATER and MAIN-PANEL to answer, not for
BOSS to assume.
