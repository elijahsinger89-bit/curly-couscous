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
| G-16 | **NO AUTOMATIC RE-DOSE. EVER.** Software never tops up, retries, re-doses or corrects on its own on the strength of any reading of any check. If a check reports no movement, the batch STOPS and tells the operator. The operator decides | Frozen 2026-08-30 as a RULE, not a parameter. Not a configurable retry count, not a threshold anyone can turn up. See D-017 |
| G-17 | Jugs are dedicated per channel for life. Not interchangeable vessels. A jug is refilled with the same product forever or it is retired | Frozen 2026-08-30. See D-018 |
| G-18 | The jug change break point is at the jug. The tube stays with the channel and is never moved between channels | Frozen 2026-08-30. See D-020 |

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

**D-017 NO AUTOMATIC RE-DOSE. Frozen as a rule before any code exists.**
G-16. Reason, and it is CONTROL-SOFTWARE's reasoning accepted whole: every other
error in this software is recoverable, and a double dose is not. Nothing measures
the excess, G-04. The books record only what was commanded, G-05. On the two pH
channels the excess leaves through V3 and is gone. The tank and the books diverge
in a direction nobody can ever see.

It is a rule and not a parameter. No configurable retry count. No threshold
anyone can turn up. No reading of any check may cause software to top up. If a
check reports no movement the batch stops and tells the operator, and the
operator decides.

**The direction of error is chosen, not accidental.** With this rule in place a
timing error in the settle window can only produce a FALSE STOP, which is loud
and safe. It cannot produce a silent overdose. That is why the whole class of
settle-window bugs stops being dangerous, and it is the reason to write the rule
before the code rather than after.

**D-018 Jugs are dedicated per channel for life.** G-17. The channel token goes
on the jug body permanently. A jug is refilled with the same product forever or
it is retired. This is the cheap half of F-002 and it costs a label and a
decision. It also resolves the departure DOSING proposed: with dedicated jugs the
station carries the channel token AND the jug body carries it too, belt and
braces, which is only safe because the vessel never moves channel.

**D-019 The keyed coupling is NOT taken yet.** Reason: once jugs are dedicated
the coupling is worth less than it looked, and DOSING's air-ingress warning is
the reason to hold it. On a suction line a bad seal does not drip, it draws air,
the head turns, the books decrement and nothing is delivered. Trading a visible
failure for an invisible one is the wrong trade.

Taken instead, both free, both preconditions DOSING already named: translucent
tubing, O-03, and the jug end in the operator's sightline, O-04. Both make air
ingress visible.

Revisit the coupling after C-09 exists and the jug procedure is in use. Not
declined, held.

**D-020 The jug change procedure is defined.** G-18. The break point is at the
jug. The tube stays with the channel. The tube is never moved between channels.
Written that way the key becomes optional rather than load-bearing, which is the
whole reason D-019 can hold the coupling without leaving F-002 open.

**D-021 The channel token gets an OWNER, not a row.** CONTROL-SOFTWARE is the
definitional end: it declares what channel N is, and every other subsystem
consumes that declaration and matches it. DISPLAY-BOX, INTERCONNECT, PUMP-BOXES
and DOSING carry it, none of them defines it.

Reason: as a shared row with four contributors it was lost twice. One agent
declares, everyone else matches. Interface S-19 is rewritten on that basis.

**D-022 C-09 goes FIRST in the commissioning order.** Before anything that
depends on a channel meaning what it says. It is free, it needs no hardware, and
it is the only check that catches a build-time labelling error. Every measurement
after it is worthless if channel N is not what the wall says it is.

**D-023 The chiller is held off across settle windows.** S-18. Read cleanliness
beats a small temperature excursion on a 40 gal tank over a window measured in
minutes. Routed to WATER to confirm that nothing about the chiller's duty cycle
makes holding it off unsafe. Provisional until WATER answers.

**D-024 S-15 is corrected rather than carrying an interpretation.** F-005. As
written the row said the EC check is valid only during a dose, which is a window
in which its own evidence cannot exist. The row now says the window is anchored
to the dose and extends past the last step by the settling interval. The
correction is recorded here rather than made silently, because S-15 is frozen.

**D-025 The S-18 reassessment, against the temperature facts now on file.**
The owner asked BOSS to check whether the setpoint changes the S-18 reasoning. It
does, and it changes it against D-023 rather than for it.

The facts: setpoint 66 F, pull down at 68, stop at 64, room 62 to 65. The chiller
only cools. So the tank's natural drift is toward a room that sits BELOW the
pull-down point, and the chiller has very little work to do. That is exactly the
case WATER predicted would make most of S-18 moot.

What that does to each side of the trade:

| | Effect |
|---|---|
| WATER's objection 1, starts per hour | WEAKENS. A compressor that rarely runs is rarely truncated mid-run by a hold-off, so the cycle fragmentation WATER objected to mostly does not arise |
| WATER's objection 2, G-12 stops the loop pump too | UNCHANGED, and now unconditional. The loop pump runs whenever the contactor is closed, regardless of what the compressor is doing. And the submersible is IN THE DAY TANK, F-012, so holding the chiller off removes a mixing source from the tank during the settle window |
| The BENEFIT of D-023, avoiding temperature steps in the trace | SHRINKS in proportion to how rarely the compressor runs. There are fewer steps to avoid |

**So D-023 mostly switches off a mixing pump to avoid a temperature step that
mostly is not happening.** The benefit shrank and the cost did not.

One thing that pulls the other way and must be checked rather than assumed: the
circulation submersible puts essentially all of its electrical input into the water
it sits in, and it runs continuously through a settle window. **The moment the
chiller is MOST likely to be called is during extended circulation, which is
exactly when the settle windows are.** So "the chiller rarely runs" may not hold
during the window, which is the only time S-18 is about. Nobody has measured that.
It is a question for C-02's trace and for WATER, not something BOSS will assume in
either direction.

D-023 is therefore put back to the owner rather than confirmed. BOSS's
recommendation, stated as a recommendation: drop the hold-off, let C-02 and C-08
measure whether a compressor cycle actually appears in the trace at this setpoint,
and reinstate the hold-off only if it does. That keeps the mixing source, and it
replaces an assumed disturbance with a measured one.

**D-026 parts.md is authoritative.** Every figure in it came from the owner with
the part in hand or the datasheet open. No agent may contradict a line in it and
no agent may extend it from memory. Anything not in it is not known.

**D-027 D-023 IS REVERSED. The chiller is NOT held off across settle windows.**
Both entries stay on file, per the rule that a reversed decision keeps both and
says why.

D-023 said: hold the chiller off across settle windows, because chiller cycling
moves temperature and temperature moves both readings. Reason it was made: read
cleanliness beats a small temperature excursion.

Why it is reversed, 2026-08-30, after the setpoint facts arrived:

- At a 66 F setpoint in a 62 to 65 F room the compressor rarely runs, so a
  hold-off mostly prevents a temperature step that mostly is not happening.
- G-12 guarantees the hold-off always stops the chiller loop submersible, and
  F-012 established that submersible is in the day tank. So it always removes a
  mixing source.
- **That is paying a certain cost for an occasional benefit.**
- And the thing BOSS refused to assume in either direction is the reason to
  reverse rather than keep it conditionally: if extended circulation is what heats
  the tank enough to call the chiller, then the settle windows are exactly when
  the chiller is most likely to run AND exactly when losing the loop pump hurts
  most. **Both effects concentrate in the same window, which makes the hold-off
  worst precisely where it was supposed to help.** Nobody has measured it.

**What replaces it: record the chiller state with every reading.** The Pi commands
the contactor, so it knows. Every pH, EC and temperature sample is tagged with
whether the chiller was commanded on. It costs nothing, it keeps the mixing pump
running, and it turns a contaminant into a known variable that can be filtered
later if it turns out to matter.

If C-02 and C-08 show the chiller genuinely corrupts a reading, revisit with data.
D-023 stays on file as declined-with-reason so it is not rediscovered from
scratch.

Note the shape, because it is the second time: the chiller state is COMMANDED
state, not measured state. Tagging a sample with it is legitimate because it
records what the Pi asked for. It is not evidence the compressor was running, and
no code may present it as such. parts.md's rule stands: software never reports
commanded state as measured state.

**D-028 The pump tube belongs to DOSING.** Interface F-10 closed. It is wetted, it
is a consumable, and it is in the path DOSING already owns end to end.
PUMP-BOXES stops at the barb by D-006. **The head is a mechanical mount that
happens to have a tube in it.** DOSING therefore also owns the change interval,
the change procedure, and telling CONTROL-SOFTWARE that C-01 is void for that
channel after a change.
