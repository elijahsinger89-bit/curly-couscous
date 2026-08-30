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
| G-09 | **AMENDED 2026-08-30 by D-031: the permissive contactor removes MOTOR SUPPLY (VM) from every stepper driver at once.** It does NOT remove VDD, the driver's logic supply, which stays live. The original wording said "power" and was written when everyone believed a stepper driver had one supply. That belief is now known to be false, so the row says which supply. The Pi reads back a contact on the contactor | So a welded contact is detected rather than assumed, and so the two supplies are never confused again |
| G-10 | Probes sit first in line in a vertical manifold section, ahead of every injection point | So a bubble cannot corrupt a reading and no injectate reaches a probe before mixing |
| G-11 | The circulation submersible takes suction at the day tank bottom | So the tank mixes |
| G-12 | The chiller and its loop pump are switched together by one contactor on their own circuit | The chiller has no internal pump |
| G-13 | E-stop and manual reset are in the permissive chain and are not software | As G-07 |
| G-14 | UL listing is not gating. Hobby build, no electrical inspection | Owner's stated condition. It does not license unsafe work |
| G-15 | The owner does all part lookups. Agents return a requirement and a search term and stop | No agent states a part number or a spec from memory |
| G-16 | **NO AUTOMATIC RE-DOSE. EVER.** Software never tops up, retries, re-doses or corrects on its own on the strength of any reading of any check. If a check reports no movement, the batch STOPS and tells the operator. The operator decides. **AND THE LAUNDERED VERSION IS ALSO FORBIDDEN: no "resume dose" button. A remainder computed from an unknown fraction is an automatic re-dose with a human as its trigger.** What the operator may do is command a FRESH dose of a volume they choose, which is an ordinary dose. That distinction is the whole rule. **G-16 has no crash exemption either: a watchdog reset may not resume anything** | Frozen 2026-08-30 as a RULE, not a parameter. Not a configurable retry count, not a threshold anyone can turn up. See D-017, extended by the P-09 pass |
| G-17 | Jugs are dedicated per channel for life. Not interchangeable vessels. A jug is refilled with the same product forever or it is retired | Frozen 2026-08-30. See D-018 |
| G-18 | The jug change break point is at the jug. The tube stays with the channel and is never moved between channels | Frozen 2026-08-30. See D-020 |
| G-19 | **No progress bar on an interrupted dose, and no delivered-fraction percentage anywhere.** A percentage computed from step index renders a commanded count as a delivered fraction | Frozen 2026-08-30. It is the confident-wrong-answer shape and the one thing a tired operator will believe |
| G-20 | **Any run that turns a head records whether it completed. A calibration that did not complete is DISCARDED, not scaled** | Frozen 2026-08-30. See D-034 and findings F-016 |
| G-24 | **THE MINIMUM SWITCHING LOAD QUESTION IS ASKED OF EVERY CONTACT, not only of the two that feed the Pi.** Lamps on relay poles included. An under-loaded contact oxidises, and an oxidised lamp contact gives you an indicator that works until it does not | Frozen 2026-08-30, findings F-022. The same promotion G-22 made for the severed-cable question |
| G-25 | **A no-flow CONDITION may drop the pump in hardware. A circulation VERIFICATION FAILURE may not.** They are not the same event and must not be wired to the same decision. Hardware protects the pump with dry-run timing; software protects the batch and stops it loudly under G-16 | Frozen 2026-08-30, MAIN-PANEL's ruling, D-038 |
| G-22 | **EVERY FAILURE OF A SENSE PATH MUST READ AS THE SAFE STATE.** For every signal, without exception, TWO questions are asked deliberately: **what does a SEVERED conductor do, and what does a SHORT TO THE NEAREST ADJACENT RAIL do.** A signal that fails in the unsafe direction either way is a DEFECT, not a tolerance | Frozen 2026-08-30, extended the same day by D-039. **For outputs the short is often the dangerous one**, and **the adjacent conductor in a duct or a jacket is the realistic short, not ground in the abstract** |
| G-23 | **A minimum switching load belongs to a CONTACT, not to a circuit.** No figure is carried from one contact to another. The 22.32's minimum and the 55.34's minimum are sized independently, always | Frozen 2026-08-30. See D-035 |
| G-21 | **EN stays unwired and the drivers default enabled. Software has no per-driver disable, permanently** | Frozen 2026-08-30. See D-032. The cost is recorded, not argued away |

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

**D-029 F-013 is resolved, and it is confirmed rather than a caution.** There is no
auxiliary block on the 22.32 and none was ever bought. Pole 1 carries the 24 V
rail out to both pump boxes, one pole for VM distribution, and pole 2 was unwired
and free and now carries the readback. **So a 25 A power pole is the readback
contact.** S-08 has a source and everything both agents wrote at P-09 is
implementable.

What saves it is that it is not a bare logic input. The wetting circuit is
recorded in parts.md as given: pole 2 wetted from 24 V, an optocoupler branch and
a bare burden branch in parallel, sized together for 45 to 55 mA against the
22.32's 1000 mW minimum, the burden in the MAIN PANEL rather than at the Pi, and
the sense inverted so contact closed means the Pi input goes low.

Two reasons for the burden's position, both worth carrying as principles:
- A power contact left switching 14 mA oxidises.
- **The failure of the cable must not degrade the contact it senses.**

**F-011 therefore stands as a caution and not as a defect ON THIS CIRCUIT.** Note
carefully what that does and does not cover: the wetting circuit was designed for
S-08. **S-03, the day tank fill-in-progress contact, has not been addressed and
F-011 still stands against it unresolved.**

**D-030 The asymmetric readback discipline is approved, and it is recorded as the
same choice as D-017 rather than as a new idea.**
- An apparent DROP, readback open while commanded on, is qualified over
  consecutive samples before acting. Worst case is a nuisance stop, which is loud
  and safe.
- An apparent WELD, readback closed while commanded off, **latches on a SINGLE
  sample and is never cleared because later samples read open.** A long
  qualification there is a filter that hides exactly the failure G-09 was built to
  catch.
- So an oxidising contact produces false stops and never a missed weld.

**The guard is kept verbatim: software may not solve F-011 by lengthening the
filter until the nuisance stops.** That change also hides a real drop, it looks
like tuning, and it will be proposed by whoever is tired of the false stops. The
fix is at the contact.

**D-031 F-014 is ruled: VDD IS NOT "POWER" UNDER G-09.** The permissive removes
motor supply. VDD stays live. G-09 is amended to say motor supply explicitly.

The reasons, in the owner's order:

1. **VDD comes from the display box 5 V rail, which is the Pi's own supply, and
   the Pi is deliberately not on the permissive.** Making VDD follow the permissive
   would mean routing a second switched supply to both pump boxes: new conductors,
   new terminals and a new failure mode, to switch off a few milliamps.
2. **Worse, it would create a state the drivers must never see: buffer outputs at
   5 V driving STEP and DIR pins whose VDD is at zero, which is an overdrive
   through the input protection diodes on all eight drivers, on every permissive
   drop.** The reason VDD is fed from the same board that drives the logic is that
   they cannot then mismatch.
3. **Logic staying alive is better on its own merits.** The Pi is awake through a
   drop, the drivers keep their logic reference, and DIAG and INDEX stay
   meaningful.

Worth recording: reason 2 is exactly the mirror case PUMP-BOXES named as the
argument against its own option B, arrived at independently by the owner from the
other direction. Two lines of evidence, one conclusion.

**What P-09's remaining question actually is, now that this is settled:** not
whether VDD should be removed, but **what a 6121 does with STEP asserted and VM
absent, and what the software must do so it is not clocking into a dead rail.**
Still open, and PUMP-BOXES is right that it needs the datasheet.

**D-032 EN STAYS UNWIRED.** It is unwired on the built package and it defaults
enabled.

Reason: F-015. A de-energised stepper holds differently from an energised one, and
C-06 tests holding against back-siphon. **Do not trade a tested hold for a
theoretical safety improvement.**

This overrules PUMP-BOXES, which argued EN must be wired and held disabled at
power-up. The residual cost is recorded rather than argued away: **software has no
per-driver disable, permanently, and never will.** The only protection against a
stuck or floating STEP is the permissive chain removing VM from all eight at once,
which is a chain-level backstop and not a per-channel one. CONTROL-SOFTWARE's
standing request, to be told if EN is ever landed on a Pi output, is answered: it
will not be. Its drop handler abstains rather than acts, permanently.

C-06 records two numbers, energised and de-energised, as PUMP-BOXES proposed.

**D-033 The watchdog is fed from the sequencer and state loop, never from an
independent timer thread.** Approved as written. A timer that keeps ticking while
the sequencer is wedged is a check whose condition is effectively a literal True:
it passes forever and hides exactly what it names. T-014 in the most expensive
place on this build.

**D-034 A run that turns a head records whether it COMPLETED, and a calibration
that did not complete is DISCARDED, not scaled.** F-016. This covers doses,
primes, purges, operator tests and C-01 calibration runs alike. A calibration run
cut short by a permissive drop and recorded as complete corrupts the figure every
dose in this system divides by, and G-04 guarantees nothing notices.

**D-035 S-03 gets the same topology as S-08 with different numbers, and it is not
a copy.** Recorded in parts.md as given. Same shape, same two reasons verbatim.
Different current because the minimum belongs to the contact: about 41.7 mA for
the 22.32 at 24 V against about 12.5 mA for the 55.34.

**That difference is the design.** At 42 mA an optocoupler LED is near its
continuous rating, so S-08 splits into a sense branch and a bare burden branch. At
12.5 mA a single series branch carries the whole loop and the LED sits in its
normal band. **Copying S-08's two-branch arrangement onto S-03 would add a part
for nothing.**

MAIN-PANEL gets both minimums explicitly and sizes each independently. G-23.

**D-036 The fail-safe direction of every sense path is a chosen design property.**
G-22. A broken cable or a dead LED leaves the Pi input high, reads as contact
open, reads as a drop. That is the false-stop direction and the same choice as
D-017 and D-030. It is written into the S-08 and S-03 rows as a property rather
than left to be inherited by luck.

**And the third case is checked rather than assumed.** For every Pi input
anywhere, the question is asked: what does a severed cable read as, and is that
the safe reading. **An input that fails in the other direction is a defect.**
Routed to DISPLAY-BOX, which owns every Pi input through the logic board, to
enumerate them and answer for each.

**D-037 PL-Y is not a lamp question.** "Healthy" as a word is a summary, and a lamp
driven from a relay pole can only show a contact. **So the real question is which
single contact means healthy, and the owner does not think one exists.**

Candidates he named: the master permissive latched, which PL-R already shows the
inverse of, and the driver permissive contactor closed, which is a different
thing.

Routed to MAIN-PANEL, and the shape of the answer is specified: **report what
contacts are actually available on the pole budget after the fill chains and the
seal-ins, and what each would MEAN if a lamp were on it.** The owner picks from
real options rather than defining healthy in the abstract.

The pole budget is the useful half of this. Three lamps, both 22.32 poles already
spoken for, and the fill chains and seal-ins all competing. **That constraint may
be the thing that decides what the lamps can say.**

**D-038 MAIN-PANEL's F-003 ruling, accepted and frozen as G-25.** A no-flow
condition at the discharge may drop the pump in hardware. A circulation
verification failure may not.

The reason BOSS would not give up either, of the five MAIN-PANEL gave: **a hardware
drop is SILENT, and every check downstream is a delayed tank reading.** If the pump
is dropped in hardware the Pi still believes the loop is turning, and S-15, S-16 and
F-004 go on comparing tank readings taken from a still tank. That is the
confident-wrong-answer shape this project has already been bitten by twice. A batch
stop is loud. A pump that quietly went away is not.

If one flow element serves both duties: the contact goes to K-DRY with dry-run
timing, **K-DRY latches and does not auto-restart when flow returns**, and a second
pole goes to the Pi for the software judgement. One element, one relay, two poles,
two consequences, two reset paths. **WATER's line is now satisfied: it is a decision
and not a side effect.**

That second pole is interface S-20, a third instance of S-03's circuit shape, which
had no row until now.

**D-039 The sweep takes TWO columns per signal, not one.** G-22 extended the same
day it was frozen.

The severed case is one failure mode. **The other is a SHORT, and for outputs it is
often the dangerous one. A severed step line stops a pump. A step line shorted to
the 5 V rail asserts it permanently, and with EN defaulting ENABLED under G-21 that
is a driver being clocked or held by something other than the Pi.**

Two constraints on how the second column is answered:

- **In a duct or a jacket the adjacent conductor is the realistic short, not ground
  in the abstract. So the answer must say what each signal is actually NEXT TO**,
  against the real cable and duct arrangement. Where a subsystem does not know what
  a signal is next to, it says so and names who owns that answer rather than
  assuming a neighbour.
- **This may CONFIRM the pair assignments, the colour work and the class separation
  rather than find anything, and that is a fine outcome.** A confirmation stated as
  one is worth having. No agent manufactures a finding to justify a pass.

**D-040 AUDIT is invoked, and INTERCONNECT is not.**

AUDIT had never run. Every other subsystem had reported at least once, and there
were frozen rows, rulings and four agents' returns that nothing had cross-read.
Invoked 2026-08-30 with access to exactly five files and no general access to the
tree: the two returns from DISPLAY-BOX and MAIN-PANEL, plus interface-table.md,
decisions.md and traps.md. **Its output is questions, not assertions, and its job is
whether the pictures AGREE, not whether the work is good.**

If it needs a file it was not given, saying so is itself a finding: **a picture that
cannot be checked without a document nobody handed you is a finding about the
picture.**

**D-041 AUDIT runs per return, pairwise, not per batch.** Written into agents.md as
its invocation rule. It finds things by comparing two parties on one fact: two
returns and it compares them, six and it summarises them, which is worth much less
and costs more. Each run gets the return that just landed, the frozen rows it
builds against, and any earlier return touching the same fact. Nothing else.

It had nothing to compare until two subsystems had reported on overlapping ground,
which is why it had not run before 2026-08-30. That was correct. From here it runs
on every return that touches a frozen row or another subsystem's slice.

**INTERCONNECT is deliberately NOT invoked yet.** It needs the pin map and the panel
layout and both are in flight. Invoking it now would have it build against two
moving targets, which is the same mistake as designing a UI against a moving fault
model.
