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
| G-16a | **A LOUDER ALARM INVITES EXACTLY THE FORBIDDEN CORRECTION. Making a check louder makes that failure MORE likely, not less.** The operator's instinct on "pH went up when you asked for down" is to command the opposing pH channel. **The UI must not offer it and the corrective path must be structurally incapable of it, not merely discouraged** | Moved here 2026-09-02 at the owner's instruction, from the check's own file, because it belongs beside G-16 rather than inside one check |
| G-16 | **NO AUTOMATIC RE-DOSE. EVER.** Software never tops up, retries, re-doses or corrects on its own on the strength of any reading of any check. If a check reports no movement, the batch STOPS and tells the operator. The operator decides. **AND THE LAUNDERED VERSION IS ALSO FORBIDDEN: no "resume dose" button. A remainder computed from an unknown fraction is an automatic re-dose with a human as its trigger.** What the operator may do is command a FRESH dose of a volume they choose, which is an ordinary dose. That distinction is the whole rule. **G-16 has no crash exemption either: a watchdog reset may not resume anything** | Frozen 2026-08-30 as a RULE, not a parameter. Not a configurable retry count, not a threshold anyone can turn up. See D-017, extended by the P-09 pass |
| G-17 | Jugs are dedicated per channel for life. Not interchangeable vessels. A jug is refilled with the same product forever or it is retired | Frozen 2026-08-30. See D-018 |
| G-18 | The jug change break point is at the jug. The tube stays with the channel and is never moved between channels | Frozen 2026-08-30. See D-020 |
| G-19 | **No progress bar on an interrupted dose, and no delivered-fraction percentage anywhere.** A percentage computed from step index renders a commanded count as a delivered fraction | Frozen 2026-08-30. It is the confident-wrong-answer shape and the one thing a tired operator will believe |
| G-20 | **Any run that turns a head records whether it completed. A calibration that did not complete is DISCARDED, not scaled** | Frozen 2026-08-30. See D-034 and findings F-016 |
| G-24 | **THE MINIMUM SWITCHING LOAD QUESTION IS ASKED OF EVERY CONTACT, not only of the two that feed the Pi.** Lamps on relay poles included. An under-loaded contact oxidises, and an oxidised lamp contact gives you an indicator that works until it does not | Frozen 2026-08-30, findings F-022. The same promotion G-22 made for the severed-cable question |
| G-25 | **A no-flow CONDITION may drop the pump in hardware. A circulation VERIFICATION FAILURE may not.** They are not the same event and must not be wired to the same decision. Hardware protects the pump with dry-run timing; software protects the batch and stops it loudly under G-16 | Frozen 2026-08-30, MAIN-PANEL's ruling, D-038 |
| G-33 | **THE SEED, THE CAPACITY AND THE POURED VOLUME ARE THREE DIFFERENT QUANTITIES AND ARE NEVER ONE COLUMN.** A seed is what a file had to contain. A capacity is what a vessel holds. A poured volume is what the arithmetic runs on. **None of the three was the same number and all three were one column** | Frozen 2026-09-02, the standing shape rather than a local fix. See T-018 and D-086 |
| G-34 | **WHERE A RULE CAN BE WRITTEN AGAINST A ROLE RATHER THAN AGAINST A DIMENSION, IT SHOULD BE.** A rule keyed to what a thing IS outlives a rule keyed to how big it is | Frozen 2026-09-02. Established by what survived the seed retraction: everything keyed to volume fell, everything keyed to role stood |
| G-35 | **A QUESTION ANSWERED NO IS CLOSED. WHAT THE NO FORCES IS A SEPARATE OPEN ITEM, WITH ITS OWN ID.** An answered question left open because its consequence is unresolved reads, a month later, as an unanswered question, and the answer gets asked for twice. **And the reverse failure is worse: closing the question and letting its consequence close with it silently** | Frozen 2026-09-03. Established by three instances in one turn: P-09 answered NO by documentation, which forced C-18 as its own item, D-070. F-059's level question answered, which forced F-072's sizing item. DIAG answered NO, which forced F-073. **In each case the answer and the consequence wanted different lifetimes** |
| G-36 | **IMPOSSIBLE HAS TWO GRADES AND THEY ARE NOT INTERCHANGEABLE. STRUCTURALLY impossible follows from a frozen rule or from physics and no addition could change it. CURRENTLY impossible follows from what has been bought, wired or decided so far, and something already on the table would change it. ANY CLAIM OF IMPOSSIBILITY NAMES ITS GRADE, AND A CURRENT ONE NAMES WHAT WOULD CHANGE IT** | Frozen 2026-09-03, D-101. **The reason it is a rule and not a style note: a structural claim removes the reason to keep paying for the door, so it makes itself true retroactively.** A claim of fact gets re-derived by the next agent that needs it. A claim of impossibility gets copied, because there is nothing to re-derive. T-023. **AMENDED 2026-09-03 by D-103, and the amendment is the half that costs money: A CURRENT CLAIM ALSO SAYS WHETHER DECLINING TO PAY MAKES IT TRUE. Some wrong impossibilities are expensive and RECOVERABLE - the thing can still be bought later. Some are SELF-FULFILLING: they remove the reason to pay for the capability, the capability is then not bought, and the claim becomes true with no step anyone would notice.** The tree had no marking that distinguished the two and G-36 as first frozen did not require one. AUDIT found four of the second kind in decisions.md alone |
| G-37 | **A CITATION IS NOT A SOURCE. CITE THE FROZEN ROW, NOT THE DOCUMENT THAT QUOTES IT.** **Two files where one cites the other and neither cites the source is a SECOND-SOURCE ILLUSION: it reads as corroboration and is one claim wearing two hats.** A citation chain that terminates in itself has the same shape as a check anchored to its own inputs | Frozen 2026-09-03, D-102. From F-074: the settle-window claim sat in software-spec.md and in commissioning C-23, C-23 citing the spec, **and neither cited D-060, which contradicts it, or S-20, which would deliver the capability.** Two files agreeing is worth nothing when one of them is the other's only source. G-32's shape - an expectation derived from a label rather than a measurement - arriving on provenance instead of on chemistry |
| G-38 | **A GRADE IS ONLY TRUE AGAINST THE TREE IT WAS GRADED ON. WHEN A DECISION MOVES, THE IMPOSSIBILITY CLAIMS DOWNSTREAM OF IT ARE RE-GRADED, NOT INHERITED** | Frozen 2026-09-03, D-112. **Two instances the same day, in opposite directions: D-064's chiller tagging was graded CURRENT on S-18's Pi-read exit, and D-108 removed the chiller contactor, so it is STRUCTURAL. software-spec.md section 12's "six of the eight channels" was correctly STRUCTURAL when written, and D-105 made the count an assignment, so it is CURRENT.** F-085. A grade is a relation between a claim and a tree, not a property of the claim, **and that is exactly why G-36's naming requirement matters: a claim that names what would change it tells the next reader when to re-grade it** |
| G-39 | **WHEN CHOOSING AN ACTUATOR, ASK WHAT IT DOES WITH NO POWER BEFORE ASKING ANYTHING ELSE. EVERY OTHER PROPERTY IS A PREFERENCE. THAT ONE IS THE FAILURE MODE** | Frozen 2026-09-03, D-114, at the owner's instruction and placed beside G-22 deliberately. **G-22 asks what a severed conductor does and what a short to a neighbour does. NEITHER ASKS WHAT A DEAD PANEL DOES**, and an actuator is the only class of device where that is a different question. **Established by the owner reversing his own part choice within one exchange: he proposed a motorized ball valve, reasoned about it for a paragraph, and withdrew it on the fail state. The deciding property was not the first thing either party looked at.** Voltage, size, speed and control type are all preferences. Hold-last on a valve that fills a tank is a flood |
| G-40 | **THE 1ST EDITION SET IS A CITATION, NOT A SOURCE, AND NOTHING IN IT BECOMES A DEFAULT BY BEING THE ONLY THING ON THE PAGE.** Where it disagrees with this tree, THE TREE WINS. Anything taken from it is recorded as "observed in the 1st Edition set, unverified" and its verification is routed to the owner. **Its figures are T-018 candidates, its parts may have been superseded, returned or never bought, and its impossibility claims are UNGRADED - which under G-36 means they are not claims anyone can check** | Frozen 2026-09-03, D-115, the owner's caveat made a rule so it binds on subsystems that never read the message. **The specific danger it exists to stop: an OPEN question closing because the old set already answered it, with nobody deciding to close it.** AUDIT found a live instance on the first read - see D-116 |
| G-32 | **AN EXPECTED SIGN COMES FROM A MEASUREMENT, NEVER FROM A LABEL.** If a check derives what it expects from a product name on a token, **a mislabelled jug produces a mislabelled expectation and the check CONFIRMS the swap instead of catching it** | Frozen 2026-09-01, D-083. The reference sign is the measured step for that token from C-03, and it is only as good as C-09. **A swap present at commissioning is baked into the reference and confirms itself forever**. **AMENDED 2026-09-03 by D-105: THE SAME RULE NOW BINDS ON ROLE. With role a per-channel SETTING, a wrong role is worse than a wrong product - it makes the signed check expect the wrong direction, so the check CONFIRMS the error instead of catching it. C-09 verifies the ROLE, not only the product** |
| G-30 | **DUTY IS SEPARATED BY RELAY, NOT BY CONTACT MATERIAL.** A power pole and a sense pole never share a relay. **All four poles share one volume in a dust-protected, not-wash-tight plug-in, and a 7 A break throws silver vapour, oxide and carbon onto the quiet pole. Gold plating survives and the contact still degrades, by a path that no contact material and no burden value addresses** | Frozen 2026-09-01, D-067. It supersedes the contact-material remedy as the answer to mixed duty, and it is why the browser build deleted its low-level contact rather than improving it |
| G-31 | **A MINIMUM SWITCHING LOAD IS ONE POWER REQUIREMENT. The published V/mA pair is a REFERENCE COORDINATE, not an operating point, and not three independent floors.** A current figure that clears its reference coordinate is not a margin | Frozen 2026-09-01, D-068. 5 V times 5 mA is 25 mW against a published 300 mW, so the pair cannot be a legal operating point. Sharpens G-23 rather than replacing it |
| G-29 | **A SIGNAL'S NEAREST NEIGHBOUR MUST BE AT THE SAME POTENTIAL AS ITS PULL'S DESTINATION.** Pull down, pair with the return. Pull up, pair with the 5 V. **Then severed and shorted-to-neighbour produce the same level, and only one decision has to be right.** And it must be a PAIR: in a random-lay bundle you cannot guarantee which core ends up against which, **and a twisted pair guarantees adjacency by construction** | Frozen 2026-08-30, D-061. Polarity-agnostic, so it survives whichever way the missing link resolves. It is what dissolves F-033's "necessarily opposite" limit, **by construction rather than by circuit design**. **ANNOTATED 2026-09-03, D-103: THE RULE STANDS AND THE DISSOLUTION CLAIM DOES NOT HOLD FOR DIR.** D-096 reversed the convergence - severed goes HIGH by the board, shorted to a return-paired neighbour goes LOW - so F-033's limit is live again on that signal. BOSS annotated D-069, D-095 and F-053 with that reversal and MISSED this row and D-061. **G-29 is a construction rule and is still correct. What is withdrawn is that DIR satisfies it for free** |
| G-26 | **THE PANEL RUNS WITHOUT THE PI.** Fills, transfer, circulation and chiller all operate on float and interlock logic with no computer involved. **The Pi adds dosing and removes driver power. If it dies, the water system keeps running and only dosing stops** | Frozen 2026-08-30, D-052. Deliberate, and recorded as a property rather than left to be rediscovered |
| G-27 | **A COMPLEMENTARY PAIR IS A FAIL-DETECT, and the construction rule is: BOTH LEGS AT THE SAME POTENTIAL, ON THE SAME CABLE.** Then a severed conductor makes them contradict, and **any state where both agree is a broken sense path** | Frozen 2026-08-30, D-053. Free wherever two legs of one changeover are already bought. It converts a fail-safe into a fail-detected, which is T-012's rule arriving in hardware |
| G-28 | **RELAYS ARE NOT INTERCHANGEABLE ONCE BOUGHT. Which relay goes in which socket is a BUILD FACT, labelled BY NAME and never by position** | Frozen 2026-08-30, D-054. Dry-circuit duty and receptacle duty want different contact materials, and using a dry-circuit contact at high current destroys the property it was bought for. T-013 |
| G-22 | **EVERY FAILURE OF A SENSE PATH MUST READ AS THE SAFE STATE, AS FAR AS THE TOPOLOGY ALLOWS.** For every signal, TWO questions: what does a SEVERED conductor do, and what does a SHORT TO ITS REALISTIC NEIGHBOUR do. **AMENDED by D-049: on a two-state sense loop the two fail in OPPOSITE directions and both cannot be made safe. The SEVERED case is chosen safe, on frequency. The SHORT case is then managed by ADJACENCY - the wiring plan - and not by circuit design** | Frozen 2026-08-30, extended the same day by D-039. **For outputs the short is often the dangerous one**, and **the adjacent conductor in a duct or a jacket is the realistic short, not ground in the abstract** |
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

**D-042 NO DOSE DURING A FILL, and F-017 is closed BY INVERSION rather than by
logic.**

The interlock's reasons: a fill changes tank volume while a dose is being computed
against it, and **every verification in this system is a delayed tank reading, so a
fill inside a settle window corrupts the measurement the same way the chiller would
have.**

**The fix is the normally closed contact.** Wire it so CLOSED means no fill in
progress and OPEN means filling. Then a severed cable reads as filling, dosing is
inhibited, and the failure is a stop rather than a permission. Same 55.34, same
wetting circuit, same current, different pole.

**That is G-22 satisfied by WIRING rather than by software, which is where it
should be satisfied. Software cannot make a severed cable safe. Contact selection
can.** The general form is traps.md T-016.

**D-043 The STEP and DIR pull-downs belong to PUMP-BOXES, not to DISPLAY-BOX.**
F-018. A pull at the display end does nothing once the conductor is cut, so the
part is per-driver, at the driver input, inside the pump boxes. Routed with two
questions PUMP-BOXES owns: what value, and **where it physically lands, given the
driver has screw terminals and no board space of its own.**

**A severed DIR producing a head that runs backwards while the books decrement
forward is the worst outcome in the whole sweep**, and the S-10 row says so.

**ANNOTATED 2026-08-30, findings F-035: this decision says pull-DOWN, and whether
DOWN is the safe direction for DIR is not established by anybody.** It needs three
links and only one is a datasheet: which DIR level gives which rotation, which
rotation gives which flow through the head as mounted, and which flow direction is
safe. **If DIR low is the direction that draws from the manifold toward the jug,
the wording is fail-unsafe and must be revisited.** PUMP-BOXES correctly refused to
substitute a pull-up on its own initiative.

**And findings F-033: no resistor at the driver end can close both of G-22's
questions on DIR.** The severed and shorted cases define opposite levels. D-043
closes the severed case only.

**D-044 Buy the relays. The panel is not designed around a shortage.**

Definite now, one: **the dry-run interlock relay, K-DRY.** Five independently
commanded states are required as a floor and four relays exist.

Contingent, up to four more, each decided by a named question rather than by
guesswork:

| Contingency | How many | What decides it |
|---|---|---|
| Interposers for the two 22.32 contactor coils | 2 | Whether the logic board can drive a 22.32 coil directly: DISPLAY-BOX's sink capability per channel and in total against the 22.32's coil pull-in and hold current at the trim voltage C-16 records. Interfaces S-07 and S-09, both OPEN |
| Splitting K-FILL-D | 1 | Whether one 55.34 in a 94.74SMA socket may carry a 120 V receptacle load and a roughly 12.5 mA SELV sense pole on adjacent poles. If not, it splits |
| A timing relay for the dry-run start-up bypass | 1 | Whether the bypass is implemented as a separate timing relay rather than within K-DRY. It must be shorter than the pump's dry-run tolerance and longer than flow establishment, and neither number exists yet |

**Of what: the same 55.34 already in use, and each added relay needs its 94.74SMA
socket. Coil suppression is a requirement on every coil regardless of who drives
it**, because an open-collector output switching an inductive load without it fails
slowly and looks like something else. MAIN-PANEL returns the coil and suppression
requirement with search terms; BOSS states no part number.

**D-045 PL-Y is a lamp across the outgoing 24 V rail, downstream of the permissive
contactor.** Accepted as MAIN-PANEL proposed it. Measured rather than commanded,
costs no coil, and **the impossible state is diagnostic: PL-R and PL-Y both on
means the contactor is welded.** It also forces PL-Y to be 24 V class specifically,
which decides the top-face routing question.

**D-046 The receptacles are PANEL MOUNTED in the enclosure face and the cords plug
into them from outside.** They are not fed through cord grips. F-023 closed.
MAIN-PANEL places them.

**D-047 The top face is treated as needing GASKETED DEVICES.** F-025 stands open on
the enclosure's own rating, which the owner has not chosen. The room is not wet but
it carries water tank to tank, and five upward-facing penetrations is the right
objection. **Routed to MAIN-PANEL: say what gasketed-device selection constrains
about the E-stop, the reset and the lamps, because it may change the parts.**

**D-048 S-06 is CLOSED. The panel-face E-stop satisfies it and there is no second
remote E-stop.** F-024 closed.

**D-049 G-22 is amended: severed is answered by the circuit, shorted is answered by
the wiring plan.** Findings F-028.

DISPLAY-BOX established, working the second column, that **for an optocoupler sense
loop severed and shorted-to-an-energised-neighbour fail in opposite directions,
always. Severed extinguishes the LED, a short to a live neighbour lights it. You can
choose which is safe. You cannot make both safe.** No two-state sense line can
report three states.

So G-22 as originally worded promised what the topology cannot deliver, and the
honest form is:

- **The SEVERED case is chosen safe, on frequency.** A pulled cable, a broken
  strand, a backed-out terminal and a corroded crimp are ordinary. An insulation
  failure to one specific energised neighbour is not.
- **The SHORT case is managed by ADJACENCY, not by circuit design.** Which conductor
  sits next to which, in which jacket, in which duct.

**That makes MAIN-PANEL's duct plan and INTERCONNECT's cable schedule load-bearing
on a safety rule rather than merely tidy**, which is a different status than either
had before, and both should be told so.

**D-050 The C-nn namespace collision is fixed by renaming.** Findings F-026. The
interface table's cable and enclosure crossings are now CBL-01 to CBL-07 and every
reference in the tree is updated. Costless and certain to fix a real defect, so BOSS
made it under rule 5 rather than asking. **It was T-013's shape: a thing named by an
index in a namespace that was not its own, cited by two returns meaning two
different rows.**

**D-051 BOSS annotates a return in place when a decision is made out of it.**
Findings F-032. A return that stays on disk arguing for something since frozen reads
as an open request when it is an answered one. G-24 and G-25 both came out of
MAIN-PANEL's return and its text still asks for them.

**D-052 S-09 IS CORRECTED. THE PI DRIVES ONE COIL.** F-027 closed. The owner
answered from the browser package, the same hardware built to a different set of
documents.

**What the Pi drives:** the driver permissive contactor coil, and nothing else. One
output, BCM 18, through a ULN2003 sinking the coil return, with SUP-1 across the
coil. It reads that contactor's auxiliary contact back on a separate input so it can
tell commanded state from actual state.

**What it does not drive:** the day tank fill coil, hardwired float seal-in; the
storage fill coil, same construction, separate relay; **the transfer pump, which is
a POLE on the day tank fill relay and not its own coil; the circulation pump, which
is a POLE on the dry-run interlock relay; and the chiller, which is a CONTACTOR on
its own circuit.**

**What it observes:** one dry contact from the day tank fill relay saying a fill is
in progress. The only level information it has, and F-017 is why its polarity
matters.

**Where the error came from, recorded because provenance matters:** the owner's
original project description said the Pi commands relays for the transfer pump, the
circulation pump and the chiller. **That was loose. It commands a permissive that
GATES those circuits; it does not command them.** MAIN-PANEL's table listing only
K-CIRC was closer to the truth than S-09 and still not right.

**G-26 is the property that falls out of it and it is deliberate: the panel runs
without the Pi.**

**A consequence BOSS is routing rather than computing: the pole budget may have
changed.** MAIN-PANEL built its shortfall on five independently commanded states
including K-CIRC as its own relay. **Circulation is now a pole on the dry-run
interlock relay, not a relay of its own.** Whether the shortfall survives that is
MAIN-PANEL's to answer before anything is ordered.

**D-053 The complementary-pair fail-detect is kept, and the construction rule is
frozen as G-27:** both legs at the same potential, on the same cable. That rule is
what makes it work and it is what would be lost if only the outcome were recorded.

**D-054 Relays are labelled by name, never by position, G-28.** A labelling
requirement on the sheet, not a note.

**D-055 The DIR question is a ROUTING question, not an electrical one.** No resistor
at the driver end makes DIR safe against both failures, and exactly one of the two
gives the backwards head whichever way it is chosen. PUMP-BOXES was right to refuse
to substitute a pull-up on its own initiative.

**So the question is not which resistor. It is WHICH FAILURE IS MORE LIKELY IN THIS
CABLE.** Routed to PUMP-BOXES: which conductor is DIR physically adjacent to, and is
a short to it more or less likely than a severed conductor. **Then choose the pull
direction against that answer, and RECORD THE OTHER FAILURE AS ACCEPTED AND NAMED.**

**D-056 AUDIT's A7 is settled and G-21 is untouched.** Both statements were true and
they are not the same thing. **G-21 is about the EN pin and a HARDWARE disable.
Refusing to command a channel is the SEQUENCER skipping it, which needs no hardware
at all.** The change procedure in channel-token.md is corrected to say the sequencer
skips the channel.

**D-057 AUDIT's B11 is settled: ONE FILE holds the token's attributes.**
channel-register.md at the root is the one record. Each subsystem returns its own
attribute to BOSS, who writes it there. **The declaration's rule is narrowed
accordingly: an attribute is recorded ONCE, in the register, and a subsystem file
may reference it but not restate it.** Four files holding four attributes was close
to the thing the declaration's own forbidden list calls a table in any medium.

**D-058 The relay shortfall does not survive G-26. ZERO definite additional
relays.** MAIN-PANEL recounted against the corrected topology.

**Four states, four relays, an exact and MINIMAL fit** - not an arithmetic
coincidence, because none of the four can be merged: K-FILL-S and K-FILL-D are two
tanks with two float sets under G-03; K-DRY cannot fold into K-PERM, which is
T-017, MAIN-PANEL's own deadlock finding; and K-PERM cannot fold into anything
because it is the only thing RESET re-arms. K-CIRC is deleted, circulation being a
pole on K-DRY.

**But the constraint moved rather than vanished, and the order is still gated.**

**It is now CONTACT DUTY, and it binds on TWO relays instead of one.** K-FILL-D
carries the transfer pump and the S-03 and D-042 SELV pair. **K-DRY now carries the
circulation pump AND the interlock contact to the Pi, which is new and was created
by G-26 moving circulation onto it.** Under G-28 those are different duties bought
as different parts. **If either the mixed-voltage socket question or the mixed-duty
contact question binds, it forces TWO slaves, not one.**

**So the order is gated by two LOOKUPS, not by the count:** the 55.34's contact
material options and what current a dry-circuit version may carry, and the socket's
rated insulation between poles plus whether both legs of a changeover may be loaded
simultaneously. **Order range: zero additional relays if both come back permissive,
two if either binds, plus one timing element if S-05 is flow-proving. Zero
interposers, on the browser package's evidence that a ULN2003 with SUP-1 already
drives that coil on this hardware.**

**MAIN-PANEL's recommendation, marked as one: order margin. Four states in four
relays is an exact fit with no spare coil, and at least one unresolved item, the
chiller's command path, could still turn into a state.**

Also noted and not taken: **K-PERM's 120 V bus pole may not be needed**, since the
pumps' coils already sit on the permissive's 24 V bus. Dropping it frees a pole and
removes a contact that would otherwise carry the sum of every 120 V load plus two
motor inrushes. Keeping it puts two contacts in series between the permissive and
each pump, so a single welded pole cannot keep a pump running. **Given that G-09
exists entirely because of welded contacts, that redundancy may be worth the pole.**
Owner's pick.

**D-059 Interface S-18 is REOPENED.** Findings F-043. It was closed by D-027 on a
mechanism G-26 has removed. **A closed row whose premise has been withdrawn is not
closed, and reopening it is cheaper than discovering at commissioning that no sample
carries a chiller state.**

**D-060 The dry-run bypass timing element is promoted from contingent to
DEFINITE-IF-FLOW-PROVING.** With circulation as a pole on K-DRY, **K-DRY cannot
start itself from a flow contact: the pump only runs when K-DRY is energised, K-DRY
only holds when flow is proved, and flow only exists when the pump runs. That is
T-017's deadlock again, now INSIDE A SINGLE RELAY instead of inside the permissive
string.** RESET alone does not solve it, because a momentary close cannot survive
the interval before flow establishes.

So the S-05 fork now costs a device as well as a capability: flow-proving means a
timing element is definite and circulation verification stays possible; level-based
means no timing element and **circulation verification is foreclosed permanently.**

**CORRECTED 2026-09-03 BY D-103, at the owner's instruction, and it is the worst instance in the file. THE CLAUSE AS WRITTEN IS WITHDRAWN. WHAT D-060 SAYS IS: level-based means no timing element, and the SHARED SOLUTION is foreclosed - the element itself cannot subsume circulation verification. IT DOES NOT SAY CIRCULATION VERIFICATION IS FORECLOSED, AND IT NEVER HAD THE GROUND TO.** T-024, and the escalation happened in the summary rather than in the argument. S-05's frozen row says a level element forecloses THE SHARED SOLUTION - that this element cannot subsume circulation verification. **D-060 escalated that to circulation verification being foreclosed PERMANENTLY, which is a claim about every route rather than about one element.** Three things on the table would change it:

- **F-003 is separately assigned** by D-016 to WATER with MAIN-PANEL at the other end, and S-05's own row says S-05 must not be answered before F-003 is.
- **C-12's W-1 transient**, which C-12 itself calls the only F-003 option that costs nothing and adds nothing.
- **S-20 exists on EITHER fork**, because circulation is a pole on K-DRY under D-058, so the Pi can read whether the pump was energised regardless of how S-05 resolves.

**Declining to pay makes it true retroactively, and this is the strongest form of it in the tree: D-060 is the entry that F-074, D-101 and C-23's correction all cite as the authority for saying the door is open.** T-023's mechanism running on T-023's own cited source.

And an operational consequence to make visible rather than discovered: **a latched
dry-run trip now stops circulation until a human presses RESET, and the Pi cannot
restart it.** It can log and alert, since it never loses power, but it cannot
recover. Consistent with G-26's philosophy.

**D-061 The DIR question is answered, and D-055's thesis is proved: it was a routing
question.** G-29 frozen.

**ANNOTATED 2026-09-03 BY D-103, AND IT SHOULD HAVE BEEN ANNOTATED THE SAME MORNING.** D-096 reversed the DIR convergence and F-072 records that G-29's severed-versus-shorted convergence is BROKEN AGAIN on this signal. **So "the DIR question is answered" is no longer true, and "F-033's limit is dissolved" is no longer true for DIR.** BOSS annotated D-069, D-095 and F-053 and missed this entry and G-29's own row. **This one has a clock on it: D-062 is a gate before the S-10 cable is bought and before any resistor is fitted, and D-043's pull-down is now load-bearing for the level per F-072. An unannotated entry saying the question is answered is exactly what gets read by whoever buys the cable.**

**Segment 5 is good news and it is fixed by the board.** At the driver terminal
block DIR's two physical neighbours are STEP and EN, **and neither is an energised
rail.** VDD is six terminals away and VM eight. **So the two worst adjacencies in
this build - F-031's VDD-to-VM closest approach, and DIR's exposure - sit at
opposite ends of one part and do not interact.** Nothing needs doing there and
nothing can be done: the order is the board's.

**With DIR paired to its own return, the two G-22 failures stop being opposite and
converge on one state.** F-033's limit was correct for sixteen conductors in a
common jacket and is dissolved by construction.

**The frequency argument transfers, and PUMP-BOXES said precisely where it
weakens.** It holds cleanly in the cable: the mechanisms that cause insulation
failure to a specific energised neighbour - abrasion, crush, over-temperature,
chemical attack, UV, flexing - **are none of them present** on a 4 ft indoor
wall-mounted run at 62 to 65 F. **And the strongest evidence is not generic
reliability data, it is traps.md: T-008 to T-011 are ALL termination failures, all
recorded because they actually bit this owner on this kind of work.**

**It weakens at the terminations**, where the short mechanism is not insulation but a
stray strand, **and the landing field the fix requires ADDS whisker opportunities.**
That reinforces the soldered-carrier option against the terminal-strip option on
this specific ground, and **makes ferrules on every stranded conductor a requirement
rather than a preference.**

**And one severing mechanism nobody had named: the lid is a heavy serviceable
assembly carrying four motors, lifted with its wiring attached every time the box is
opened. A recurring strain event applied directly to interior terminations, on a
schedule, with no short-circuit counterpart.**

**PUMP-BOXES' honest qualification, kept because it is the part that stops this
being a rule of thumb: frequency is not the only axis. The two outcomes are not
symmetric in consequence. Choosing on frequency is right HERE only because pairing
lets the likelier failure and the safe state coincide. It would not have been
sufficient on frequency alone.**

**D-062 THE GATE, and it has a deadline.** Findings F-049.

**Links (a) DIR level to rotation and (b) rotation to flow through the head as
mounted are settled BEFORE the S-10 cable is bought and before any resistor is
fitted.** Link (c), which flow direction is safe, is established and was correctly
not reopened.

The reason it is a gate and not a preference: **the convergence is an amplifier.**
Pairing makes both failures produce one level, which is a win only if that level is
safe. **If DIR low is the backwards direction, pairing makes it worse rather than
better, because both failures would then give the unsafe rotation instead of one of
them.** And F-030 already says the pairing is cheaper before the cable is bought, so
**the cable decision and the polarity decision collide on the same missing fact.**

If they resolve against low being safe, D-043 and F-030 are revisited by the owner,
not worked around by an agent. PUMP-BOXES refused to substitute a pull-up on its own
initiative for exactly that reason, twice now.

## 2026-09-01

**D-063 The circulation pump is INTERMITTENT, not continuous.** It runs when the
system needs the tank mixed or moving: during a batch, during dosing, and through a
settle window. Between batches it is off. **The dry-run interlock is a PERMISSION
for it to run, not a command that it should.**

Three consequences, all favourable:

1. **F-003's exercise run does not dissolve. It is needed**, and needed precisely
   because a pump that is off between batches is exactly the case where nobody knows
   it still works.
2. **WATER's free witness survives and gets BETTER.** The column standing in the
   vertical probe section drifts to room temperature while the tank is chilled, so on
   start the PT-1000 sees a step. **That works hardest after a long rest, and long
   rests are now the normal state rather than an edge case.**
3. **D-025's premise survives.** Continuous pump heat was the thing that might have
   called the chiller more than the setpoint suggests. An intermittent pump does not
   put continuous heat into the tank.

**And one gain nobody asked for: the settle window now sits INSIDE a running period
rather than spanning a transition**, which matters for the C-02 timing
measurements. A window that spans a start or a stop measures two regimes.

**What remains from F-045: the exercise run still has no command path.** The Pi
cannot command the circulation pump under G-26. That is a real gap and it is
separate from the question of whether the exercise is needed.

**D-064 The chiller contactor coil's driver is an OPEN QUESTION, and it is the
owner's to settle.** Findings F-044.

MAIN-PANEL's plain absence is confirmed: nothing on file says what energises that
coil. The owner does not have an answer and is not inventing one. **Candidates named,
not chosen: a thermostat, a float or interlock chain, or a manual switch.**

**Routed as an open question and NOT as a design task. No subsystem designs around
it.** It is the one state in the panel whose driver is unaccounted for, and a
subsystem that assumes a driver in order to get on with its own work would bury the
hole rather than leave it visible.

**Until it is settled, S-18 stays OPEN and D-027's sample tagging cannot be
implemented as written, because there is no chiller state to tag with.**

**D-065 The order stays stopped, on the owner's instruction.** Not against a stale
count, which is now corrected, and not now that the constraint has moved from count
to contact duty. **Two lookups gate it and G-28 makes the type irreversible once
bought.**

**D-066 The datasheets are with the owner and D-062's gate stands.** The TMC2209
chip datasheet and the Adafruit 6121 board schematic, before the S-10 cable is
bought. The framing is accepted: pairing is an amplifier, both failures give one
level, and that is a win only if the level is safe.

**And PUMP-BOXES' qualification is kept verbatim, because it is what stops the
reasoning being reused where it does not hold:** frequency is not the only axis, the
consequences are not symmetric, and choosing on frequency is right HERE only because
pairing makes the likelier failure and the safe state coincide.

**D-067 The mixed-duty question is settled, and NOT by plating. G-30 frozen.**

The debris path decides it: all four poles share one volume, the plug-in is dust
protected and not wash tight, and a power break throws silver vapour, oxide and
carbon onto the quiet pole. **Gold plating on a quiet pole survives AND the contact
still degrades, by a path that is not the one being argued about. No contact
material and no burden value addresses it.**

**So MAIN-PANEL's two gates are answered from a direction neither of them was
pointing.** It offered the mixed-VOLTAGE socket question and the mixed-DUTY contact
question, both to be settled by lookups. **The lookups came back and the answer is
that the duty question does not depend on either: a relay carrying a power pole and
a sense pole degrades regardless.**

**Both relays that G-26 left carrying both duties are affected: K-FILL-D, which
carries the transfer pump plus the S-03 and D-042 SELV pair, and K-DRY, which
carries the circulation pump plus the interlock contact to the Pi.** BOSS is routing
the conclusion to MAIN-PANEL with the fact in hand rather than drawing it, because
it is a purchase and the split is MAIN-PANEL's to draw. **What it points to is two
slaves.**

Also settled and worth keeping: **gold cannot be mixed pole by pole. Option 5 is the
whole relay**, and gold is consumed by switching above roughly 30 V and 100 mA after
which the AgNi floor returns. So a gold relay used for a power pole stops being a
gold relay.

**D-068 G-31: a minimum switching load is one power requirement.** The V/mA pair is a
reference coordinate. **The roughly 12.5 mA at 24 V already on file for the 55.34 is
the correct figure, so S-03's, S-20's and D-042's sizing all stand unchanged** - but
they are AT the floor, not above it, and nothing on file should read as though they
carried margin.

**D-069 F-018 is NARROWED by the schematic, and only DIR survives it.**

**EN has an explicit 20k board pulldown, R3. STEP has a board pulldown plus an LED
load. So a floating STEP is pulled low by the board and a floating EN leaves ENN low,
which is the enabled state parts.md already recorded.** The "floating CMOS input"
premise of F-018 is therefore **wrong for STEP and for EN**.

**DIR is the one that survives, and it survives differently than anyone assumed:
there is NO board pull on DIR at all. What sits on it is two indicator LEDs, which is
loading and not a defined logic pull. Its defined level comes from the CHIP's
internal pulldown, DI(pd).**

**So a severed DIR converges LOW, and D-062's remaining question is unchanged and is
not a datasheet question: whether DIR low is the safe rotation on these heads. That
is a pump fact.**

What is NOT settled by this: whether the chip's internal pulldown is strong enough
against the coupled noise F-018 describes, which is the second of PUMP-BOXES' four
bounds and the one it said no datasheet can close. **The level is defined. The noise
immunity is not.** D-043's external pull-down is therefore no longer needed to DEFINE
the level and may still be needed to HOLD it. Routed to PUMP-BOXES.

**D-070 P-09 CANNOT BE CLOSED FROM DOCUMENTATION.** The datasheet neither allows,
forbids, sequences nor characterises VS absent while VCC_IO is live. No leakage
figure, no clamp current, no STEP or UART behaviour in that state.

**It closes by MEASUREMENT or by REMOVING THE STATE.** Those are the only two, and
they are the owner's:
- **Measure it**, which is commissioning C-18, deliberately entering the state and
  observing. C-18 was written blocked on the datasheet saying whether entering it is
  safe. **The datasheet will not say. So running C-18 is itself the decision to
  accept an uncharacterised state on purpose, once, under observation.**
- **Remove the state**, which means VDD follows the permissive after all. **D-031
  rejected that for three reasons and its reason 2 was the overdrive at STEP and
  DIR** - which is now a different question, because the board's own pulldowns and
  the chip's internal pull change what those pins do when VCC_IO is absent. Reopening
  D-031 would need that re-argued, not merely re-decided.

**And one thing the datasheet does say that bears on the watchdog: cycling any of VS,
5VOUT or VCC_IO resets the chip to power-on defaults, and it says VCC_IO is easiest
and safest to cycle.** That is a recovery path nobody had, and it is the opposite end
of P-09 from the hazard.

**D-071 The rail's ceiling and the board's ceiling are the same number, and the
margin is in the WIRING rather than in the setting.** The board publishes 5 to 29 V
DC, labelled neither recommended nor absolute, with no VM regulator and no clamp. The
rail is settable to 28.28 V and OVP does not trip until 29 V.

**So at the top of its range the rail sits exactly at the board's published ceiling
with nothing between them.** And the abs-max footnote says the real hazard is not the
DC level: **stray inductance in GND and VS rings the supply when driving an inductive
load, and a meter reading 28 V can ring toward 32.**

**That makes it a wiring requirement, not a voltage setting: keep VS and its return
short and paired, and the local bulk cap is what absorbs the ring.** C-16 records the
trim, but **the trim reading is not the number that matters, and C-16 should say so.**

**D-072 G-30 forces both splits unconditionally, and the dividing line moves from
VOLTAGE to ARCING DUTY.**

Both prior gates are **moot rather than answered**: the plating question because gold
survives and the contact degrades anyway, the insulation question because insulation
is not the failure path. **T-015's shape in miniature: the argument was being had
about the wrong property.** The mixed-voltage socket question stays separately open
and now decides nothing about the split.

**The line asks one question of each pole: does it break a load that arcs. Voltage is
not the variable.**

| Tier | Poles | Debris |
|---|---|---|
| 1, arcing loads | transfer pump, circulation pump, fill solenoid, the 120 V permissive bus | The source. Must be isolated |
| 2, suppressed coil switching | seal-ins, latches, the 24 V coil bus, any slave-coil drive | Mild, and only if suppression is AT THE COIL |
| 3, quiet | S-03, the D-042 inhibit, the K-DRY contact to the Pi, every lamp | What must be protected |

**Two places the line moves, and both matter. The fill solenoid crosses to the power
side even if it is a 24 V coil** - it is an inductive load being broken, and under the
old voltage line it would have sat with the quiet group. **The lamps cross to the
quiet side even though they are 24 V** - under the voltage line PL-R sat happily
beside a 120 V bus pole.

MAIN-PANEL placed tier 2 with tier 3 **and flagged it as a judgement rather than a
rule, refusing to extend a frozen rule past its words.** Two conditions on that:
suppression sits at the coil, not at the driving contact, **and the point is now to
keep arc energy out of the quiet envelope rather than only to protect the driver**;
and the coil current is checked against the gold-consumption threshold.

**Parallel coils, not cascade.** Each split pair's two coils are driven from one point.
It frees a pole in each pair, largely removes F-039, and removes a coil-switching pole
from the quiet envelope. **The right description, and it answers whether the count
reasoning survives: a duty-split pair is ONE STATE IN TWO ENVELOPES. It adds no
state. The four-state topology is untouched; what grew is the envelope count.**

**A dead end named before anyone spends a lookup on it: a sealed or wash-tight relay
does not solve this. The debris is generated inside the shared volume, not admitted
from outside. A tighter seal traps it better.**

**And two independent routes to one conclusion: gold is a whole-relay order option
and cannot be mixed pole by pole, so even with no debris fact, gold-not-mixable would
have forced duty separation by relay.**

**D-073 The order: two to four additional 55.34s, and TWO GATES THE OWNER CLEARS IN A
MINUTE DECIDE IT.**

**Gate 1, and nothing on file states it: which contact option the four relays in hand
are.** Gold is a whole-relay option. **If the four in hand are standard they become
the power envelopes and the order is GOLD. If they are gold they become the quiet
envelopes and the order is STANDARD.** And never use a gold relay as a power
envelope: the gold is consumed above roughly 30 V and 100 mA and the relay reverts to
AgNi with the 300 mW floor back, **so you would pay for a property and destroy it in
service.**

**Gate 2: which fill PL-G means, which now costs a relay.** Day-tank-only leaves
K-FILL-S a single power envelope. Either-fill splits it and adds a quiet envelope,
because a PL-G pole in the storage chain cannot sit beside the fill solenoid.

Six envelopes minimum, three quiet and three power: K-PERM quiet with the latch, the
coil bus and PL-R; K-FILL-S power with the seal-in and solenoid; K-FILL-D-Q quiet with
the seal-in, the S-03 and D-042 changeover pair and PL-G; K-FILL-D-P power with the
transfer pump; K-DRY-Q quiet with the seal-in and the G-27 complementary pair to the
Pi; K-DRY-P power with the circulation pump. **Eight at maximum if both gates bind,
which resolves to a clean statement: four states, each in two envelopes, one quiet and
one power.**

**G-28 applies AT DELIVERY, not at installation: label each relay by name to its
envelope the moment it is unpacked. Once the two types are in the same panel and look
alike, a swapped pair is a defect that passes every check - the quiet relay silently
degrades and the power relay is over-specified and nobody sees either.**

**Zero interposers**, on the browser package's evidence.

**And a conflict that decides a relay: fast-release suppression and arc-quenching
suppression pull in opposite directions, and they pull on exactly the two relays where
both properties matter, K-PERM and K-DRY. Splitting K-PERM resolves it** - the coil
bus goes to an AgNi envelope where arc energy is tolerable and fast release is free,
and PL-R stays in a gold envelope that switches nothing but a lamp. **Two independent
reasons now favour splitting K-PERM, and MAIN-PANEL leans toward buying for it.**

**D-074 The VCC_IO cycle is recorded as a candidate recovery path and is NOT built.**

Why it is worth more than it looks, and the reason is about this build rather than
the chip: **the Pi currently has no recovery action on a driver at all.** EN is
unwired for ever under G-21 so there is no disable, the permissive is hardware-latched
and only a manual button re-closes it, **so the Pi's entire influence on a driver is
STEP and DIR. A VCC_IO cycle would be the only software-reachable recovery action on
a driver anywhere in this system**, and the first candidate answer to "the Pi is
awake, it has detected something, and it can do nothing".

**It composes with D-075: with MS1 and MS2 set by pins, a reset restores the same
configuration, so the recovery is idempotent. Set over UART it would not be.**

Against it, honestly: VCC_IO feeds all eight from one unswitched rail, so a cycle is
all-eight or all-four-per-box unless eight switched elements go inside sealed boxes.
**It puts a switching element in the Pi's OWN 5 V rail, which F-020 already names as a
conductor that can brown out the controller from six feet away.** And cycling VCC_IO
with VS present and a motor mid-step is **its own uncharacterised transient**: the
datasheet calling VCC_IO easiest and safest of the three to cycle is a COMPARATIVE
statement, not a characterisation of the bridge during the reset. **Doing it safely
means doing it with VS absent, which is the state D-070 says nobody has
characterised. Circular, and it resolves the same way everything here does, through
C-18.**

**It is a THIRD option on P-09, neither D-031's always-live nor D-070's
follows-the-permissive: momentary, commanded, software-initiated.** Recorded as such
so it is not mistaken for either. If it ever becomes a design feature, DISPLAY-BOX is
told because it is a new output, a new S-12 row and a switched element in the Pi's own
supply, and **CONTROL-SOFTWARE is told because it is an automatic corrective action,
and D-017's reasoning should be applied to it before any code exists rather than
after. A reset is not a re-dose, but a reset mid-batch that silently resumes is the
same family.**

**D-075 MS1 and MS2 are set in HARDWARE, and the existence of a UART route is a reason
to be more careful rather than a new option.** Findings F-062. Reached with no
datasheet figure, from a statement already on file: cycling any rail resets the chip
to power-on defaults, **so a UART-set microstep factor silently reverts mid-batch on a
rail dip while every instrument reads healthy, and G-04 and G-05 make it invisible.
Set by pins, the same reset restores the same configuration and becomes idempotent.**

**D-076 UART does not rescue P-09 Q3, and the datasheet's own words are why: VCC_IO
does not supply the IC logic part and logic is sourced from VS.** In the P-09 state VS
is absent, so the logic core has no supply and register-based status is questionable
at best. **UART is a richer channel in every state EXCEPT the one P-09 is about.**

**D-077 The five products are DELIBERATELY UNASSIGNED UNTIL COMMISSIONING, and that
is a decision not made rather than a gap in a file.** The owner checked rather than
reconstructing: the controller config names every channel "Channel 1" to "Channel 8"
and says on its own line that nothing there knows what is plugged into which channel.
**No subsystem holds a row open for them and no subsystem assumes a product to get on
with its own work. C-09 is where a token is bound to a product, with the jugs
physically present.**

Recorded in channel-register.md, along with what the software does know: **six
nutrient channels and two pH; the two 1000 mL channels are the pH adjusters; CH5 is
marked pH-down through the blocked-channels path, which is a ROLE and not a product;
and pH channels are excluded from every injection plan by construction.** CH6 is the
other pH channel by elimination, marked as an inference.

**BOSS searched every markdown file for a channel-to-product list. There is none.** The
only product-like names in the tree are channel-token.md's own FORBIDDEN examples.
Nothing to strike, and the search is recorded so nobody repeats it.

**D-078 The jug sizes are not uniform and that is now a constraint, not a detail.**
CH1 to CH4 are 4000 mL, CH5 and CH6 are 1000 mL, CH7 and CH8 are 3785 mL. **If the jug
station, the coupling or the tubing was specified against one container size it is
wrong for two of the eight.** Routed to DOSING to check rather than assume, and it
lands on jug placement, height relative to the head, and how a jug is changed - all of
which DOSING already owns and none of which was drawn against three sizes.

**D-079 The relay order is settled by the owner's two answers. The four 55.34s in hand
are STANDARD contact, not the option 5 gold variant. PL-G means the DAY TANK fill, not
storage.**

So the four in hand become the POWER envelopes and the order is GOLD, per D-073's gate
1. And per gate 2, **K-FILL-S does not split**: it stays a single power envelope with
the seal-in and the fill solenoid, and PL-G sits in K-FILL-D's quiet envelope where it
was already placed.

Routed to MAIN-PANEL to state the final list rather than computed here, because it is
a purchase and the envelope split is MAIN-PANEL's to draw. **What it points to: three
gold envelopes, K-PERM, K-FILL-D-Q and K-DRY-Q, against three power envelopes covered
by relays already in hand with one standard spare, plus a fourth gold if K-PERM
splits.**

**D-080 F-062 is taken. Microstepping is set by PINS, never over UART.** Already frozen
as D-075 and now confirmed by the owner in the same terms: **a UART-set factor
reverting to the pin default on a rail dip, mid-batch, with every instrument reading
healthy, is invisible by construction. Pins reset to the same configuration the same
reset produces.**

**D-081 F-061's safety consequence is recorded as a commissioning hazard in its own
right**, C-22, not as a footnote to a procedure. **Setting Vref requires the permissive
closed and 24 V live in the box while a person has a screwdriver on a pot beside four
motors.** And the good news in the same finding is kept: **VREF is scaled off 5VOUT
rather than off VS, so motor current is to first order independent of the trim, and the
trim does not propagate into the flow calibration.**

**D-082 The order is complete and is written to order.md.** Six envelopes minimum,
seven if K-PERM splits. **Buy four gold 55.34s and three sockets**, on MAIN-PANEL's
recommendation.

**The decisive argument for the fourth gold is not the split. It is that a standard
relay cannot substitute for a gold one under G-30, so at the minimum the panel has one
standard spare and ZERO GOLD SPARES - and the envelopes with no spare are exactly the
ones carrying every Pi-facing signal and both contact-driven lamps. The fourth gold is
used either way: as K-PERM-Q if the split happens, or as the only gold spare if it
does not.**

Two things in the list that are absences with reasons rather than omissions: zero
interposers, and zero suppression for the permissive contactor coil because SUP-1 is
already across it in the corrected package and is taken as given rather than
respecified.

**G-28 is sharpened to apply AT DELIVERY: label each relay by name to its envelope the
moment it is unpacked. The two types look alike, and a swapped pair is a defect that
passes every check** - the gold relay silently degrades in a power envelope and the
standard one carries the Pi-facing signals with the 300 mW floor and no gold.

**And one thing must be settled before the lamp burdens are chosen and it is not in
the order: F-056's sizing at the bottom of the trim range.** S-08 survives it because
it was specified as a window. S-03 does not because it was specified as a point. Five
circuits are affected.

order.md also lists what the order does NOT cover, so nothing reads as complete: the
gasketed devices, the hood, the receptacles, the lamps and their burdens, the ground
bar, and the terminals, duct and rail.

**D-083 S-16 IS DIRECTION-AWARE, and it was required before F-063 was written.**

CONTROL-SOFTWARE answered from what the check MUST do, not from what it does, and said
so: S-14 is still open, no source is in reach, and D-012 means no verification logic
ships until C-02 exists. **Written into the specification today it costs nothing.
Retrofitted onto a magnitude-only implementation it changes the outcome set, every
operator message and the commissioning reference data. The same argument as freezing
G-16 before any code existed.**

**The reason is not the token adjacency. It is what the check is FOR. S-16 exists to
ATTRIBUTE. A check that reports only "pH moved" attributes nothing: it confirms the
loop moved and something arrived, which is exactly what S-15 already provides through
EC. A MAGNITUDE-ONLY pH CHECK IS A DUPLICATE OF S-15 WEARING S-16'S NAME.** The only
thing that makes pH an attribution mechanism is that the two channels move the
observable in OPPOSITE directions. Discard the sign and D-011's entire reason is
discarded.

**What it costs, none of it presented as free.** Settling time: nothing, same window
and same C-02, the comparison is against a signed prediction instead of an absolute
one. Commissioning data: nothing new, because C-03 already reads pH up and pH down
SEPARATELY, and measuring them separately is measuring them signed. Baseline handling:
a real tightening, because a signed check is exposed to drift's DIRECTION where a
magnitude check treated drift as noise that only ever adds, **so the drift half of
C-08, which could have been advisory, becomes load-bearing. No new row; a row that was
optional becomes mandatory.**

**Three outcomes become FOUR, and the fourth must not be folded into failure:** pass;
fail, no movement; indeterminate; and **WRONG DIRECTION.** Two reasons it stays
separate. **It sends the operator somewhere different** - no-movement points at the
pump, the tube and the jug level, wrong-direction points at which product stands on
which station, which is F-063's failure exactly. **And under G-04 they mean different
things about the tank: no-movement means the tank probably received nothing;
wrong-direction means the tank DEFINITELY received something and it was the wrong
chemical, already mixed, already partly downstream of V3, unmeasurable and
irreversible.**

**Two costs that come with the loudness.** A loud wrong-direction alarm **invites
exactly the action the frozen rules forbid**: the operator's instinct is to command the
opposing pH channel to correct it, which is the overshoot pattern already named,
lands inside an open window, and is forbidden by S-16 constraint 1 and G-16. **The UI
must not offer it and the corrective path must be structurally incapable of it, not
merely discouraged. Making the check louder makes this failure more likely, not less.**
And a signed check adds a new false mode: **saying the sign was wrong when it was
right**, from a fill diluting the tank, another channel still settling, or the chiller.
**A false "wrong chemical" alarm is far more alarming than a false "no movement", and
by the credibility argument already on file it is the fastest route to the check being
switched off. So window-validity gating gets MORE load-bearing, not less.**

**What it does to F-063: it removes the INVISIBILITY, not the failure. F-063 shrinks in
SEVERITY, from a permanent invisible mis-dose to a bounded one-dose error followed by a
loud stop, and does NOT shrink in kind.**

Four things it does not remove: **it is a detector, not a preventer, and it acts a dose
too late** - the wrong chemical reaches the tank once, in full, before anything is
known, while DOSING's station measures act at the moment of the swap, **so they are
complements at different times and not alternatives**; small trim doses stay below the
band and a swap discovered only through them stays invisible; a swap present at
commissioning is baked into the reference; and **it generalises nowhere else, because
for the six nutrient channels EC moves the same way for all of them and a crossed pair
still confirms itself completely.**

**CONTROL-SOFTWARE explicitly refused to conclude that this makes DOSING's wall length
unnecessary. What it supports is that the damage of a swap is bounded to one dose plus
a stop, which changes how much wall length is worth spending. That trade is DOSING's
proposal and the owner's decision.**

And the convergence worth recording: **CH5-versus-CH6 is the ONE confusion on this
build where direction is a discriminator at all, because those two products are the
only pair that move a probe in opposite directions.** F-064 narrowed the confusion to
exactly that pair from the physical side, and this answer lands on it from the software
side, independently.

## 2026-09-02

**D-084 The token carrier is specified against THREE DUTY CLASSES, and the residual is
recorded as ACCEPTED rather than closed.** DOSING's proposal, taken.

Specify against acid, base and generic nutrient-concentrate duty. **The union cannot be
computed because five products are unassigned, and waiting for them means waiting for a
decision the owner makes at commissioning. Three duty classes covers the real
chemistry: something strongly acidic, something strongly alkaline, and salt
solutions.**

**The residual, in the owner's words: a product outside those three classes arriving on
any channel invalidates the carrier specification, and NOTHING WILL DETECT THAT AT
ASSIGNMENT TIME.**

**D-085 NO EXTRA WALL LENGTH for the CH5 and CH6 gap. The free axes only.**

**Recorded as a decision with its reason and not as a deferral: the gap was justified
when a swap was permanently invisible. The signed check made it a bounded one-dose
error followed by a loud stop, so the physical remedy is no longer worth wall length.**
Wall length is finite and the manifold and the raceway share that wall.

Taken instead, both free: **non-neighbouring colours on the two tokens, which the
colour axis already allows, and whatever spacing the existing station run gives without
enlarging it.** F-064 established that spacing is free WITHIN the sequence, so use what
is there and do not create more.

**IF THE SIGNED CHECK IS EVER REMOVED, THIS REOPENS.**

**D-086 THE JUG FIGURES ARE DEFAULTS, NOT CONTAINERS, AND THREE CONCLUSIONS RESTED ON
THEM.** The 1000, 3785 and 4000 in config.yaml are seed values, each overwritten per
channel with the volume the owner enters. **CH7 and CH8 carry 3785 because it was the
closest seed to a US gallon and nothing more.**

**So the reasoning that the two pH channels are the two 1000 mL containers is an
inference from a DEFAULT. It is probably right, because pH adjusters are concentrated
and used in small volumes, but the config does not say it and the containers are not
decided.**

Three things are marked as resting on that inference rather than on a stated container:
**the size-axis narrowing of F-063, which BOSS had wrongly filed under F-064's label
and which is now F-071, withdrawn by its author - NOTE that F-064 ITSELF, the
sequence-versus-spacing opening, depends on no volume, is unqualified, and is what
D-085 soundly spends; F-066's argument that the two smallest
containers are handled most often; and DOSING's three depth classes for the suction
pickup.**

What does NOT rest on it: **CH5 is marked pH-down through the blocked-channels path,
which is a ROLE marking and not a default.**

Recorded in channel-register.md beside the capacity column as a THIRD quantity - a seed
that is neither the container's capacity nor the volume poured - and in traps.md as
T-018. **The owner will state the actual containers when he buys them.**

**D-087 D-078 is qualified, not withdrawn.** It said the jug sizes are a constraint and
that anything specified against one container size is wrong for two of eight. **The
INSTRUCTION survives - nothing should be specified against a single container size -
but the three sizes it named are seeds. DOSING's finding that the suction pickup is
UNSPECIFIED rather than mis-specified is unaffected and is the durable half of that
pass.**

**D-088 F-064 and F-071 are separated, at DOSING's request, and it caught a record
defect BOSS created.**

BOSS filed DOSING's size-axis NARROWING of F-063 under F-064's label. **F-064 as
written is the sequence-versus-spacing OPENING, which is a reading of the ordering rule
and depends on no volume at all.** The narrowing was a separate claim made in prose.

**Why it mattered rather than being tidy-up: D-085 spends F-064 in the other direction
- "take whatever spacing the existing station run gives" relies on F-064 being sound.
With the narrowing filed under F-064's label and marked as resting on a retracted
inference, a later reader could have withdrawn the OPENING along with the NARROWING and
lost the free half of the decision that had just been made.**

The narrowing is now F-071 and is withdrawn by its author. F-064 stands unqualified.

**DOSING withdrew three things of its own without being asked to: the size-axis
narrowing, the three depth classes with the per-size riser lever and the levelled-band
argument that O-04 and O-05 would have ridden on, and F-066's direction. On the last it
noted that it had already refused to estimate the consumption rates, and that what it
had not noticed was that the VESSEL half of that argument was no firmer than the rate
half.**

What it kept, with the reason each survives: F-065, because the grep found what it
found regardless of any volume; its own self-audit, because three places drawn against
one container stay drawn against one container whatever the containers are; **anything
keyed to ROLE rather than to volume, which is why its hazard rule stands - no acid or
base container stationed where breaking or lifting it puts it above the operator's
forearms**; and F-064.

**D-089 Four traps recorded from the owner, T-019 to T-022, and T-018 extended.**

T-018 gains three more instances from the parallel build, all caught by the same
question and all later treated as measurements: **a 41.7 mA loop current, a 24 AWG
resistance constant, and an optocoupler forward voltage. All three were figures a file
had to contain.** The question that catches them: **did this come from the world, or
from a file that had to contain something.**

**T-019 PARTIAL SCEPTICISM**, DOSING's self-correction generalised. Refusing to estimate
one term while accepting another that rests on the same quality of evidence, in the same
argument. **The refusal even makes the argument look rigorous, which is what lets the
other half through.**

**T-020 A CORRECTION STATED AFTER THE STEP IT MODIFIES.** From the parallel build, and it
cost stock rather than rework, because a cut cable cannot be un-cut. **The fix that
matters is not swapping the steps: it is folding the allowance INTO the cut step,
because two steps that must be read in order is what produced it.**

**T-021 THE QUESTION DEPENDS ON THE KIND OF FILE.** A state machine produces untested
joins and half-wired mechanisms. A routing layer produces neither, because it holds no
mechanisms; its defects are boundary defects. **Asking the state-machine question of a
routing layer finds nothing, and a clean result there is evidence of nothing.**

**T-022 A WITHDRAWN CLAIM FILED UNDER A SURVIVING CLAIM'S LABEL**, which is BOSS's own
defect from D-088, generalised. **Its consequence is in the future, which is the hardest
kind to see.**

And two rules frozen out of the same turn: **G-33**, the three-quantity separation as the
standing shape, and **G-34**, prefer a role to a dimension, established by what survived
the retraction rather than argued for.

**D-090 The wall is 8 ft by 8 ft, and cut length is the wall run plus 3 ft.** Recorded
in parts.md. **Z5, M-02 and the station run are consequences of how the four
enclosures, the manifold, the raceway and the jug stations are placed inside that
envelope, not independent unknowns.**

**D-091 F-057 is ANSWERED, and the answer is that nothing commands intermittent
circulation.** The pump is a pole on the dry-run interlock relay and the Pi does not
command it: it runs when the interlock is made and the relay is energised, and it is
off between batches.

**So there is no command path, and the F-003 exercise run cannot happen as designed
until one exists or the design changes.** That is a CLOSED QUESTION WITH AN OPEN
CONSEQUENCE, which is a different thing from an open question, and the file says so.

**D-092 The main enclosure is treated as UNRATED AS ASSEMBLED, and the design sheds
rather than seals.** F-025 stays the owner's, but the design does not wait on the
number.

The reasoning, taken as given: **five upward-facing 22 mm holes and four receptacles
whose cord caps do not seal mean the assembly's rating is set by its worst penetration
regardless of what is fitted above.** So the answer will be a shield or a slope on the
top face rather than gasketed devices, **because a surface that sheds needs no seal and
a gasket is the youngest part in the assembly.**

**Design to shed. Do not wait on the number.**

**D-093 P-09 is closed BY MEASUREMENT and the fault model proceeds.** The datasheet is
silent, C-18 is the decision to accept an uncharacterised state once under observation,
and that is the only path. **CONTROL-SOFTWARE proceeds on that basis rather than
holding the fault model open behind it.**

**D-094 The work order, in the owner's order.** Document 12, the software
specification, which is unblocked and is real output. Then three lookups the owner
runs. Then the colour map proposal. **NOTHING IN THE GENERATED SET IS STARTED: the wire
table is downstream of a schematic that is downstream of what is still with the owner,
and starting it now means building on rows that will move.**

**The seven audits are accepted as the right set, and audit 7, the seed audit tracing
every figure to the world or to a file that had to contain something, is named as the
one nobody else has. They get built when there is something to run them against.**

**D-095 Document 12 exists. software-spec.md, 1154 lines, twelve sections, written in
one pass on the third attempt after two container restarts killed the first two.**

**SUPERSEDED IN PART 2026-09-03 BY D-101.** The first of the three things this entry banked as STRUCTURALLY IMPOSSIBLE, positive confirmation that a settle window was valid, **is only CURRENTLY impossible.** D-060 says flow-proving keeps circulation verification possible. The entry is kept whole, per the rule on reversals. Read the rest of it knowing the grade of one of its three was wrong.

**It is the first builder-facing document in the project and it is PARTIAL in a stated
way**, which is the right shape: what is implementable today, what is blocked with the
blocker named, and - the distinction that matters most - **what is STRUCTURALLY
IMPOSSIBLE rather than pending, so nobody reads it later as a gap waiting to close.**
Three things are in that last category: positive confirmation that a settle window was
valid, attribution for six of the eight channels, and any measurement of delivered
volume.

**BOSS checked rather than trusting the report:** swept the file for pins, addresses,
timing figures, resistances and steps-per-millilitre and found none; read section 10 and
confirmed every row names a source and no row states a value; read section 12 and
confirmed the partial status is specific rather than a hedge.

**BOSS has NOT declared it finished, and neither did CONTROL-SOFTWARE.** Under rule 7
that waits until another agent has built against it and found nothing, and the physical
half of that begins at C-09.

**What the document does that is worth recording beyond its contents:**

**It withdraws one of its author's own prior conclusions inside itself.** The
window-validity precondition in control-software-f004.md rested on the Pi commanding
the circulation relay, which G-26 and D-052 removed. F-070 is addressed rather than
left as a finding: section 6.4 states the four things window validity CAN do with the
inputs that exist and the five it cannot, **including that D-063's requirement that a
window sit inside a running period is a procedural condition on the operator and on the
C-02 measurement and is NOT ENFORCEABLE IN SOFTWARE.**

**It applied T-022 to itself**, splitting the S-03-based claim, which stands, from the
S-20-based claim, which may be withdrawn if S-05 goes level-based under D-060, and
stating that the first does not depend on the second.

**It applied T-019 to itself**, in its own words: having refused the settling interval
for want of evidence, it checked the other terms in the same paragraph and refused the
band, the magnitudes, the margin, the qualification length and the write-ahead
granularity on the same grounds.

**And it declined two decisions rather than inventing them:** whether an INDETERMINATE
outcome stops the remainder of a batch, and whether a low-jug warning blocks a plan.
Both are in section 11 as blockers rather than in the body as choices.

## 2026-09-03

**D-096 THE DIR CONVERGENCE IS REVERSED. A FLOATING DIR FLOATS HIGH.** This
CORRECTS D-069's closing claim, F-053's resolution and F-059's inference. Both
entries stay, per the standing rule on reversals.

The owner's lookup returned the three numbers F-059 said would close it:

| Quantity | Value |
|---|---|
| DIR internal pull-down | 132 k min, **166 k typical**, 200 k max |
| STEP internal pull-down | **NONE.** The pin type is DI with no (pd) |
| VINLO max | 0.30 x VCC_IO, so **0.99 V** at 3.3 V |
| VINHI min | 0.70 x VCC_IO, so **2.31 V** at 3.3 V |

**The board's green-LED branch, 20 k plus an LED to VDD, beats a 166 k internal
pull-down by an order of magnitude, and the pin sits above VINHI.** So D-069's
sentence "a severed DIR converges LOW" is WRONG. It converges HIGH.

**What this does NOT change:** D-069's narrowing of F-018 stands. The schematic
reading stands. F-059's refusal to state a level without the numbers stands, and
was right - it named the exact three quantities and declined to guess the
direction, which is why the correction is one line and not a rebuild.

**What it DOES change, and it is not small:**

1. **D-062's remaining question flips.** It was: is DIR LOW the safe rotation. It
   is now: **IS DIR HIGH THE SAFE ROTATION.** Still a pump fact, still not a
   datasheet question, still the gate before the S-10 cable is bought and before
   any resistor is fitted. **But the answer that would have been reassuring is now
   the answer that would be alarming, and vice versa.** Anyone who resolved D-062
   in their head against the old direction has resolved it backwards.
2. **D-043's external pull-down becomes load-bearing for the LEVEL**, not only for
   noise immunity. F-072.
3. **STEP has NO internal pull-down.** F-060 asked the noise question of STEP on
   the assumption that a board pull-down closed the level question there. The
   board pull-down on STEP is real, from the schematic; **what is now known is that
   the chip contributes nothing to it.** F-060's question is unchanged in substance
   and better founded.
4. **G-29's convergence on DIR is broken again.** Severed goes HIGH, shorted to a
   return-paired neighbour goes LOW. Opposite once more. F-072.

**Routed to PUMP-BOXES**, with the four numbers above and nothing else: size the
external pull-down against 166 k typical in parallel and against the 20 k plus LED
branch, to a level below VINLO, and say what that does to G-29's pairing. **BOSS
states no resistance value.**

**D-097 DIAG IS NOT A SPECIFIED DETECTOR FOR VM ABSENT, AND ONLY C-18 CAN SETTLE
IT.** The owner's DIAG lookup is recorded in parts.md. DIAG is pin 11, active
high, push-pull, specified for the fault conditions the datasheet names, **and VM
absent is not among them.** Separately: **uv_cp and VUV_VS are two different
things and must not be conflated** - one is a charge-pump undervoltage flag, the
other a VS supply threshold.

This is D-070 arriving at a second pin. P-09 could not be closed from the
datasheet; neither can this. **No agent may build a permissive-drop detection on
DIAG on the strength of the word "diagnostic".** C-18 is now the only route, and
C-18 already carries the ruling that running it IS the decision.

**CORRECTED 2026-09-03 BY D-103, HOURS AFTER IT WAS WRITTEN, AND IT IS D-101 ITEM 2's SHAPE LANDING ON BOSS'S OWN NEXT ENTRY.** Two different questions were run together in one sentence:

| Question | Grade |
|---|---|
| What a driver DOES with VM absent while VCC_IO is live | **STRUCTURAL** as far as documentation goes, per D-070, and C-18 is the only route |
| Whether the Pi can KNOW the permissive dropped | **CURRENT, and already answered.** S-08 is pole 2 of the 22.32 whose pole 1 carries the 24 V rail to both pump boxes, wetted from 24 V and reported to the Pi, with contact open reading as a drop |

**So C-18 is the only route to the FIRST question and never was the only route to the second.** What stands unchanged: DIAG is not a specified detector for VM absent, uv_cp and VUV_VS are different things, and no agent may build detection on the word "diagnostic".

**D-098 THE PI 5 PAD DEFAULTS ARE RECORDED, WITH THEIR PROVENANCE, AND THE
EXTERNAL PULL IS AUTHORITATIVE.** In parts.md. GPIO0-8 come up pulled UP, GPIO9-27
pulled DOWN, pad pull about 50 k. **GPIO2 and GPIO3 are held strongly high by
1.8 to 2 k and are not a pad default at all.**

Two things attach to this and both matter more than the numbers:

- **The provenance is forum statements by Raspberry Pi engineers, not a
  datasheet.** Recorded as such under G-15's spirit. It is the weakest provenance
  of anything currently load-bearing in the tree.
- **The HAT+ specification says fit an external resistor.** So the design rule is:
  **every Pi pin whose power-on level matters gets an external pull, and the pad
  default is a fallback nobody designs against.** That is the rule; the numbers
  are only there to say which way an unfitted pin would drift while someone is
  diagnosing.

Routed to DISPLAY-BOX for its third-case sweep: **GPIO2 and GPIO3 cannot be used
for anything whose safe power-on state is low**, and that is a hard exclusion, not
a preference.

**D-099 THE COLOUR MAP IS ACCEPTED.** colour-map-proposal.md, as proposed:

| Token | Colour |
|---|---|
| CH1 | white |
| CH2 | brown |
| CH3 | grey |
| CH4 | red |
| CH5 | **blue** |
| CH6 | **yellow** |
| CH7 | black |
| CH8 | violet |

**The colour lives on the MARKER, not on the insulation.** That is the whole
reason it survives: it does not compete with conductor colour, it does not require
buying eight cable colours, and it does not break when a cable is replaced with
whatever is on the shelf. **It is an identity axis added to the token, not a
second token.** channel-token.md's forbidden list is unaffected: a colour is not a
translation table and nothing is permitted to compute from it.

**D-100 DOCUMENT 12, software-spec.md, IS ACCEPTED.** Accepted, not declared
finished. Under agents.md rule 7 finished waits until another agent has built
against it and found nothing, and the physical half of that begins at C-09. The
acceptance covers what it contains and what it declined to contain: two decisions
left in section 11 as blockers rather than invented in the body, and one of its
own author's prior conclusions withdrawn inside it, F-070.

**D-101 AUDIT RUN 3 IS ACCEPTED, AND IT REVERSES PART OF D-095 AND PART OF WHAT
BOSS WROTE HOURS EARLIER.** audit/2026-09-03-doc12-vs-frozen.md. Pairwise against
the frozen rows document 12 claims to restate, plus the structural-versus-current
sweep the owner asked for.

| | Count |
|---|---|
| Pairs compared | 126 |
| Clean RESTATEMENT | 111 |
| DRIFT | 4 |
| WIDENING | 3 |
| OMISSION | 5 |
| CONTRADICTION | 1 |
| STALE | 1 |
| MIS-TRACE | 1 |
| Impossibility claims found | 24: 17 structural, 6 current, 1 mixed |

**THE RULING, and it is the reason the second half of the run was worth asking
for.** Document 12 calls positive confirmation of settle-window validity
STRUCTURALLY impossible. **D-060 says the opposite in frozen text: flow-proving
means a timing element is definite and circulation verification stays possible.**
So the claim is CURRENT, not structural, and the decision that would close the
door is S-05, which WATER holds open on purpose.

Three separate errors stack, and BOSS made the third:

1. The support document 12 cites, F-001 limit 1 and F-003, is about the pump AT
   REST. A settle window is by design inside a RUNNING period, per D-063.
2. **G-26 restricts what the Pi DRIVES and not what it READS**, and S-18's row is
   the frozen statement of that boundary. Document 12 respects it at 4.3 and blurs
   it at 6.4, where "neither commands nor observes" runs the two halves together.
   **The command half is structural. The observe half is not, and G-26 is not the
   rule that makes it so.** S-20 reports a second pole of K-DRY to the Pi and
   circulation is a pole on that same relay under D-058.
3. **BOSS BANKED IT IN D-095 AND THEN PROPAGATED IT INTO C-23 THE SAME DAY.** C-23
   cited software-spec.md as its authority. **The claim was in two files, one
   citing the other, and neither cited D-060 or S-20.** C-23's reason is corrected.
   D-095's line is superseded here rather than deleted, per the rule on reversals.

**The cost, which is what makes it expensive rather than untidy:** D-060 attaches a
price to keeping the door open. Flow-proving costs a timing element. **Nobody pays
for a capability they have been told is impossible**, so the false structural claim
would have foreclosed S-05 by making the flow-proving fork look like waste - and
then the claim becomes true retroactively.

**The other five current-not-structural claims** are in the audit file's Part 2
table with the sentence that decides each: loop movement and the slow failure, 2.10
and 2.18, where "the mitigation is not a sensor" states a design preference as a
property; the chiller tagging at 6.4 item 4 and 11.5, which S-18's row already
names a Pi READ as one of three exits from; and 7.1's "never name a cause", right
today, but grounded in "the Pi has no such input" rather than "the Pi may not have
one", and only the second would be structural.

**And AUDIT recorded two claims document 12 got RIGHT**, 11.16 and 11.12, so the
pattern is visible as a standard rather than only as a defect. 11.12 is T-003
observed exactly by a document that had every incentive to assert an absence.

**ROUTED, and none of it is BOSS's to write:**

| To | What |
|---|---|
| CONTROL-SOFTWARE | Its own document. 2.17, 11.6 and section 12 restate a structural claim the frozen tree does not support; 6.4 items 2, 3, 4 and 5, 4.4, 7.1 and 7.9 need their grade named under G-36. Plus the four DRIFT, three WIDENING and five OMISSION rows, of which 1.15 is the one that bites: **section 3.4 says how a channel enters OUT OF SERVICE and never how it leaves, and 5.2 admission checks a live token plus a non-void C-01 and C-17 but NOT C-09** |
| WATER, and to the owner | **S-05 is carrying a cost it was not told about.** It was held open deliberately. It has since been described, in two files, as a fork one side of which is already impossible. It is not. D-060's price stands and the capability it buys is real |
| CONTROL-SOFTWARE | N-20 and channel-token.md both say the colours are not bound. **D-099 bound them 2026-09-03.** Stale by hours, and the fix is the declaration's owner's, not BOSS's |
| MAIN-PANEL and CONTROL-SOFTWARE | **F-055 is absent from document 12**, and the readback discipline, both permissive faults and N-14 all run on the contact F-055 is about |

**Not routed and left as AUDIT filed it:** 1.11, where document 12 is AHEAD of
channel-register.md on G-33. Reported by AUDIT because it runs the other way, which
is the right instinct and is recorded here so it is not lost as a non-defect.

**D-102 F-075 IS PULLED OUT FROM BEHIND THE GRADING AND GIVEN A DEADLINE. IT MUST
BE SETTLED BEFORE C-01 IS EVER RUN.** Owner's instruction, and the reason is the
deadline rather than the severity.

The defect: **software-spec.md 3.4 states how a channel enters OUT OF SERVICE and
never how it leaves, and 5.2's admission check is a live token plus a non-void
C-01 and C-17 and does NOT include C-09.**

**Why the deadline is C-01 and not later.** A channel readmitted on a C-01 that was
measured against the wrong channel is the exact failure S-19 and D-022 both say
passes every other check in the system. **Before C-01 runs, the wrong number does
not exist. After C-01 runs, the wrong number is in channel-register.md and looks
like data** - it has a token, a date and a measurement procedure behind it, and
nothing downstream can tell it from a right one. G-05 then decrements a jug against
it forever.

**This is T-012's shape with a clock on it: correct until the data moves, with
nothing to say when it stopped. The difference is that here the moment it stops
being correct is a scheduled event we control, so it can be gated instead of
discovered.**

C-01's preconditions now carry the gate. **CONTROL-SOFTWARE owns the fix** - the
exit condition from OUT OF SERVICE, and whether C-09 joins the admission check. It
is a state with an entry and no exit, which is also the shape that gets exited by
hand.

**G-37 is frozen out of the same finding**, and BOSS is answering the owner's
question about whether the shape appears elsewhere by looking rather than by
recall. Routed to AUDIT as its own sweep, separate from the grading run. **Until
that sweep reports, BOSS asserts nothing about whether the tree has other
instances.**

**T-023 is exported to the parallel build at the owner's instruction.** Recorded
here because an export is a fact about the trap, and because the parallel build has
had three traps come the other way.

**D-103 THE GRADING RUN AGAINST decisions.md IS ACCEPTED. THE FROZEN FILE GRADES
WORSE THAN THE DOCUMENT DID, WHICH IS WHAT THE OWNER PREDICTED.**
audit/2026-09-03-decisions-impossibility-grading.md.

| | Count |
|---|---|
| Claims graded | 60 |
| STRUCTURAL | 37 |
| CURRENT | 19 |
| MIXED, two grades in one sentence | 4 |
| Could not be settled from the tree | 6 |
| **FLAGGED: would stop a purchase, a measurement or a capability** | **8** |
| **Of those, SELF-FULFILLING if declined** | **4** |

**Seven entries grade themselves correctly in place** - D-014, G-06's reason
column, D-070, D-074, D-085, D-091 and D-102. Recorded because it shows the
standard was already being practised here before it was a rule, so G-36 is a
promotion rather than an import.

**THE FOUR THAT MAKE THEMSELVES TRUE IF DECLINED.** These are the ones the G-36
amendment exists for.

**1. D-060, and it is the worst thing in the file.** Annotated above.
"Circulation verification is foreclosed permanently" overstates S-05's own row,
which says a level element forecloses the SHARED SOLUTION. **D-060 is the entry
BOSS cited this morning as the authority for reversing document 12's structural
claim. The authority overstates in the same direction as the claim it was used to
correct.** F-076.

**2. D-061, and this one has a clock.** Annotated above. D-096 reversed the DIR
convergence and BOSS annotated D-069, D-095 and F-053 and **missed D-061 and
G-29's own row** - the two entries that say the question is answered. D-062 gates
the S-10 cable purchase and D-043's pull-down is now load-bearing for the level.
**An entry saying "the DIR question is answered" is exactly what gets read by
whoever buys the cable.** T-020's form.

**3. D-084's residual: "NOTHING WILL DETECT THAT AT ASSIGNMENT TIME."** In the
owner's words, so it is not reversed here, it is put back to him. **D-077 makes
assignment time BE commissioning, and C-09 is a commissioning row that already
confirms which product is on which channel by eye, first in the order, free, jugs
in hand.** So there is a detection opportunity: one question added to C-09's
script - is this product an acid, a base, or a salt solution. That is the whole
test, and the three duty classes D-084 specifies against are exactly its three
answers. F-077. **Routed to DOSING, which owns the carrier, and to the owner,
because the sentence is his.**

**4. D-013 and S-17, fulvic.** The DECISION is structural and stays: the owner
froze it, twice, and said not to bring O-19 back unless something changes. **What
is flagged is the PREMISE, "it moves neither EC nor pH meaningfully", for which
AUDIT searched D-013, S-17, C-03, C-04, C-08 and F-001 and found no measurement
named.** And the loop closes on itself: **C-04 is scoped "per EC-moving channel",
so the assumption excludes the channel from the test that would check it.** F-078.
The decision is not reopened. The premise is marked as unmeasured, which is all
G-36 asks.

**THE OTHER FOUR FLAGS, expensive but RECOVERABLE**, in AUDIT's order: D-097,
corrected above; D-095's two surviving structural items, which are structural by
RULE - G-04 and G-05 - and not by physics, and one of which document 12 itself
grades as current at 11.16; D-064's chiller tagging - **REGRADED 2026-09-03 by D-108: the CURRENT grade rested on S-18's Pi-read exit, and there is no chiller contactor to read, so the claim is STRUCTURAL. The requirement survives anyway because the owner records chiller state by LOOKING** - and
D-049 with G-22, true for a single two-state line and softened by G-27 the very
next entry, which D-053 calls free wherever both changeover legs are already
bought. **Soft deadline at the order.**

**G-36 IS AMENDED, above, and the amendment is what this run bought.** A current
claim now also says whether declining to pay makes it true. AUDIT's closing
observation is the reason: the tree had no marking distinguishing an expensive
recoverable claim from a self-fulfilling one, and G-36 as first frozen did not
require one.

**ROUTED:**

| To | What |
|---|---|
| WATER, and to the owner | **D-060.** S-05's fork was described in the frozen file as closing a door that F-003, C-12 and S-20 all leave open. Second time in one day that S-05 has been found carrying a cost it was not told about, and this time the overstatement is in decisions.md rather than in a document |
| PUMP-BOXES | D-061 and G-29's row are now annotated. Nothing changes in what was already routed by D-096; this removes the two entries that contradicted it |
| DOSING, and to the owner | **D-084.** One question at C-09 tests all three duty classes. The sentence is the owner's, so DOSING returns whether the question is sufficient, not whether the residual is accepted |
| CONTROL-SOFTWARE | D-095's surviving structural items are structural by rule and not by physics, and 11.16 is its own model for how to say so |

**Not routed:** the six AUDIT could not settle from the tree. They are listed in
the audit file with what it read to try, and they stay there until something
arrives that would settle them. **BOSS states no grade for any of the six.**

**D-104 THE SECOND-SOURCE SWEEP IS ACCEPTED AND IT ANSWERS THE OWNER'S QUESTION
WITH A NUMBER INSTEAD OF A RECOLLECTION.** audit/2026-09-03-second-source-sweep.md.
33 files read in full, 42 cross-file citation chains followed to a terminus.

| Classification | Count |
|---|---|
| CONFIRMED second-source illusion | 6 |
| SUSPECTED | 2 |
| CLEAN-BUT-FRAGILE | 3 |

**So the answer to "does anything else in the tree have that shape" is YES, six
times, and F-074 was not the exception.**

**THE WORST, AND IT REACHES A COMMISSIONING PROCEDURE. "The Pi commands the
circulation relay."** F-079.

subsystems/control-software-f004.md cites S-09 for it. **S-09 as first written came
from the owner's original project description, which D-052 records verbatim as
"That was loose."** So the chain terminates in a description rather than an origin,
and F-027, D-052 and G-26 killed the claim on 2026-08-30.

**It is still live in five files, and F-070 covers exactly one of them.** The three
unflagged instances are control-software-f004.md, control-software-p09.md step 6
"commanded circulation and chiller states alongside", and control-software.md's own
"Settled" bullet.

**The bite, and it is why this is F-074's class and not a documentation defect:
subsystems/dosing-f004-wet-side.md tells the reader the settling timer must be
gated on the circulation pump being COMMANDED ON. That file is named in
commissioning.md as C-02's full procedure.** The person running C-02 is told to
gate on a signal that does not exist and cannot exist under G-26. **C-23 already
says the operator is the only enforcement; the procedure C-23 governs says
something different.**

**THE OTHER FIVE CONFIRMED:**

| | Claim | Terminus | Verdict |
|---|---|---|---|
| 2 | The VDD-to-VM adjacency, in F-031, D-061 and display-box-short-column.md | Each other | **F-051 already says the terminal is a circled plus and minus and not VM.** Documentation defect around a claim whose true form is recorded |
| 3 | **"CH5 and CH6 are the pH pair"** | **CH5 has a real origin in the controller config, per D-086. CH6's runs through a RETRACTED SEED** | **UNSETTLED, and D-099 is frozen on it.** Six files state it flat; only channel-register.md's header and software-spec.md 3.2 mark it as an inference |
| 4 | "Auxiliary contact", for what D-029 established is a 25 A power pole | Five files plus parts.md | **F-051's shape again: a part named by a name not on it.** Not renamed silently, per F-051's own standing instruction |
| 5 | commissioning.md instructing chiller-state tagging three times, per D-027 | D-027, whose mechanism G-26 removed | **D-064 says it cannot be done as written, and D-103 grades that CURRENT: S-18's row names a Pi READ as the first exit.** The instruction may survive; its mechanism has no source |
| 6 | The Vref "before any power is applied" instruction, in pump-boxes.md | Copied past its own correction | **C-22 already records that the instruction is unexecutable.** The corrected form did not propagate to the copy |

**D-099 IS NOT REOPENED AND ONE GATE IS ADDED, which costs nothing.** The colour
map stands. **But its hardest constraint is CH5 and CH6 maximally separated, and
CH6's claim to be the second pH channel rests on a seed that T-018 and D-086
retracted.** Nothing binds a token to a product before C-09.

**So: THE CHANNEL MARKERS ARE NOT MADE UNTIL C-09 HAS BOUND TOKENS TO PRODUCTS.**
Before C-09 that is free. After the markers exist it is eight relabels. Nothing
required them to be made early, and rule 5 covers a change that costs nothing and
prevents a wrong build. **If C-09 confirms the pair, the map is unchanged and the
gate cost nothing.**

**AND THE RUN NUMBERING IS DROPPED.** Two parallel runs both called themselves
"AUDIT run 4". **The sweep recognised it as F-026's shape - a namespace collision
between two things that never met - and declined to take a number rather than
guessing one.** That is the right instinct and it becomes the rule: **audit runs
are identified by date and topic, which the filenames already carry, and never by
an ordinal.** An ordinal assigned by whoever finished first is not an identifier.

**ROUTED:**

| To | What |
|---|---|
| **DOSING, and it is gated to C-02** | **dosing-f004-wet-side.md is C-02's named procedure and it gates the settling timer on circulation-commanded-on, which does not exist under G-26.** Highest priority of anything in this sweep because it is an instruction to a person, not a claim in a document |
| CONTROL-SOFTWARE | The three unflagged instances in its own files, which F-070 does not cover. And confirmed 5: whether chiller tagging survives on S-18's Pi-read exit, per D-103 |
| PUMP-BOXES | Confirmed 6. The Vref instruction in pump-boxes.md was copied past the correction C-22 records |
| The owner | **Confirmed 4.** "Auxiliary contact" for a 25 A power pole is in parts.md, which is AUTHORITATIVE under D-026. **F-051 says such a thing is not renamed silently, so BOSS has not touched it** |
| Nobody yet | The 2 SUSPECTED and 3 CLEAN-BUT-FRAGILE are in the audit file. **CLEAN-BUT-FRAGILE means correctly sourced today but only one file carries the origin, so if it moved nothing would flag the copies. That is a watch item, not a defect** |

**D-105 ROLE IS A PER-CHANNEL SETTING. ANY CHANNEL MAY CARRY NUTRIENT, pH-UP OR
pH-DOWN.** Owner's requirement, 2026-09-03. **This is the largest change since
G-26 and it dissolves rather than shrinks several open items.**

**The hardware already allows it and always did.** All eight pumps are identical,
the tubing, the drivers and the wiring are the same, and nothing physical assigns a
role. **What prevented it was software keying role to a channel number.**

**THE TWO MECHANISMS THAT NEED THE ROLE, AND BOTH ALREADY EXIST:**

| Mechanism | What it does with role today | What it does instead |
|---|---|---|
| The plan builder | Excludes pH channels from every injection group so pH runs alone and last. **Reads a FIXED LIST** | Reads the per-channel role setting |
| The signed pH attribution, S-16 and D-083 | Needs to know which direction to expect from a commanded channel, because pH-up and pH-down move the probe opposite ways | Reads the per-channel role setting |

**Everything downstream follows from the ASSIGNMENT rather than from the NUMBER.**

**THE COST, NAMED RATHER THAN ABSORBED, in the owner's words: a role that can
change is a role someone can change wrongly, and a wrong role is WORSE than a wrong
product - it makes the signed check expect the wrong direction, so the check
CONFIRMS the error.** That is G-32 arriving through the role instead of through the
label, and **G-32 is amended above to bind on role.**

**So C-09 verifies the ROLE, not only the product.** Added to its script alongside
D-084's duty-class question. C-09 was already the only check that catches a
build-time labelling error, and it is now the only check that catches a
configuration one.

**F-063 DISSOLVES. It does not shrink.** There is no fixed pH pair to separate,
because any two channels could be the pair. **Whatever separation matters becomes a
property of the ASSIGNMENT at commissioning rather than of the token numbering.**
That also disposes of F-080 and of the CH6 question underneath it: **CH6's role no
longer needs an origin, because no channel's role comes from elimination any more.**

**The owner's CH6 answer is recorded anyway, because it stands on its own and
because a later reader will hit F-080 before this entry:** eight channels, two of
them pH, the controller marks CH5 as pH-down by ROLE through the blocked-channels
path, and there is no third pH role, **so CH6 is pH-up by elimination FROM A ROLE
MARKING and not from the retracted seed.** The elimination is sound. **What BOSS
cannot confirm from the tree is whether the config carries a role marking for CH6
the way it does for CH5** - channel-register.md states the CH5 marking and calls
CH6 an inference, and nothing in the tree shows the blocked list itself. **That is
an owner lookup, not an agent question, and it is now optional rather than
load-bearing.**

**THE MARKER GATE EXTENDS.** F-080 gated the channel markers on C-09 binding
tokens to products. **It now gates on C-09 binding both PRODUCT and ROLE.** Still
free before C-09, still eight relabels after.

**WHAT IT TOUCHES. The owner's expectation is the plan builder, the attribution
check, the register schema and C-09, and asked whether it reaches further. BOSS IS
NOT ANSWERING THAT FROM RECALL.** A reach sweep is running across the whole tree.
**Until it reports, BOSS asserts nothing about what else is keyed to a channel
number, and NOTHING IS BUILT against this decision.** The four the owner named are
certain; the question is only whether there is a fifth.

**Also running: the downstream trace**, graded per the owner's instruction on WHICH
of three different facts each decision needs - **the pair being pH, the pair being
ADJACENT, or the specific identity of CH6.** Those are three dependencies and they
fail differently. The trace stays useful after this decision because it says which
rows dissolve with F-063 and which were never about CH6 at all.

**D-106 THE C-09 SCRIPT TAKES BOTH QUESTIONS.** D-084's duty class, at the owner's
instruction, and D-105's role. **One line each on a script that already confirms
which product is on which channel, and both close a residual for free.**

**D-107 D-013'S PREMISE IS UNTESTABLE BY CONSTRUCTION, AND THAT GOES ON THE ROW
RATHER THAN IN A SCOPE NOTE.** Owner's instruction. **The decision stands: fulvic
stays unattributed and O-19 does not come back.** What is now stated where a reader
will find it: **D-013 asserts fulvic moves neither EC nor pH meaningfully, no
measurement is named for that anywhere, and C-04 is scoped "per EC-moving channel"
- so the assumption removes the channel from the only measurement that could
falsify it.** F-078. **A premise nobody measured, protected from measurement by
itself.**

## 2026-09-03, later. The owner's four answers.

**D-108 THE CHILLER IS ENTIRELY SELF-CONTAINED. F-044 CLOSES, AND WHAT IT FORCES
IS A SEPARATE OPEN ITEM UNDER G-35.**

It plugs in, it senses its own water with its own built-in sensor, and it cycles
its own compressor. **Nothing in the panel energises a chiller contactor coil,
because there is no chiller contactor to energise.** The one state in the panel
whose driver was unaccounted for was unaccounted for because it does not exist.

**CONSEQUENCE 1, and it is the big one: the Pi's day tank temperature reading is
for the DOSE, not for control.** It compensates the pH and EC measurements. **It is
not a control input to anything** and no subsystem may treat it as one.

**CONSEQUENCE 2: THE SAMPLE-TAGGING CHAIN IS DEAD AS DESIGNED, AND IT DIES ONE
LEVEL DEEPER THAN D-064 THOUGHT.** D-027 replaced the chiller hold-off with
sample tagging. Its mechanism was "the Pi commands the contactor, so it knows".
G-26 removed that, D-059 reopened S-18, and D-064 said it could not be implemented
as written. **S-18's first way out was for the Pi to READ a contact on the chiller
contactor, needing a spare pole on the 22.32. There is no chiller contactor, so
there is no contact and no pole. That exit is gone, not merely unbuilt.** D-103
graded D-064's claim as CURRENT on the strength of that exit. **THAT GRADE IS NOW
WRONG AND THE CLAIM IS STRUCTURAL: the Pi cannot know the chiller's state because
nothing in the system is wired to the chiller at all.**

What survives, and it is enough: **the owner measures C-02 and C-08 by hand and
can record chiller state by LOOKING.** D-027's requirement was that chiller state
be recorded against every sample, not that software record it. **The requirement
stands and its mechanism is a human eye.** C-02 and C-08 already say "recorded
against every sample"; nothing there needs changing.

**CONSEQUENCE 3, AND IT IS AN OPEN ITEM, NOT AN ANSWER. G-12 IS A FROZEN RULE AND
IT SAYS: "The chiller and its loop pump are switched together by one contactor on
their own circuit", with the reason "The chiller has no internal pump."**

**If there is no contactor, nothing on file switches the LOOP PUMP.** The chiller
controlling itself says nothing about what moves water through it. **This is G-35
exactly: F-044 answered NO, and what the NO forces is a separate open item with
its own ID.** F-086. **BOSS is not deciding whether G-12 is wrong, whether the
loop pump is on its own switch, whether it runs continuously, or whether the
chiller in fact has a pump. That is the owner's and it is one question.**

**D-109 ALL PVC IS 3/4 INCH SCHEDULE 80.** Owner's answer. **The manifold diameter
is 3/4 in and the port arrangement is downstream of it.**

**Schedule 80, not 40**, so wall thickness and inside diameter differ from the
common case **and any threaded port is into a thicker wall.** Recorded here rather
than reasoned about: **no agent derives a port count, a spacing, a thread depth or
a pressure drop from this.** It is one dimension and a schedule, and what follows
from it is WATER's and DOSING's to return with search terms.

**D-110 THE ENCLOSURE IS IP65 FOR ALL INTENTS AND PURPOSES. F-025 CLOSES AT THAT
LEVEL, AND THE DESIGN-TO-SHED PRINCIPLE IS KEPT ANYWAY.**

The owner's reasoning, recorded because it is the part that outlives the rating:
**five upward-facing holes and four cord caps mean the ASSEMBLY's rating is set by
its worst penetration, regardless of what the box is rated.** So the box being
IP65 closes the question of the box and does not close the question of the top
face. **D-047's treatment of the top face as needing gasketed devices stands
unchanged, and the requirement for each 22 mm device's rating IN THAT ORIENTATION
is still live.** F-025 is closed on the enclosure and its top-face half is
re-filed as its own item rather than carried inside a closed finding. G-35.

**D-111 THE FILL VALVE IS A MOTORIZED BALL VALVE, NOT A SOLENOID, AND THE
DIFFERENCE IS A FAIL-STATE DIFFERENCE.** The owner confirms it was missing and
names the distinction: **a solenoid is energise-to-open and springs closed on power
loss. A motorized ball valve drives open and drives closed, holds position without
power, and takes seconds rather than milliseconds.**

**NOTHING IS CHOSEN AND BOSS NAMES NO PART.** The requirement and the search terms
are in findings.md under F-087. **Four things must come back from the datasheet
before any subsystem designs around this valve, and the first is the one that
touches a frozen rule:**

| | What must be known | Why it is not a detail |
|---|---|---|
| 1 | **What it does on power loss** | Most stay where they are. **That is a different fail state from a solenoid and it means A FILL CAN BE LEFT OPEN BY A POWER FAILURE unless the valve is spring-return.** G-22 asks what a severed conductor does; this asks what a dead PANEL does, and no row in the tree asks that of an actuator |
| 2 | How it is driven | Two-wire, three-wire and five-wire types exist and need **different relay arrangements**. Some need a MAINTAINED signal, some a PULSE. The relay count and the contact arrangement both depend on the answer, so **the order cannot be finalised without it** |
| 3 | Whether it reports position | Many have auxiliary limit switches. **If this one does, that is a signal the panel could read and NOBODY HAS CONSIDERED IT.** It would be the only direct confirmation in the water path that a commanded thing actually moved |
| 4 | Travel time | **It is not instant.** Anything assuming a fill starts or stops promptly needs the number, and the float logic is the first thing to check against it |

**Item 1 is raised to the owner as a hazard question and not as a lookup**, because
a fill left open by a power failure is a flood, and the answer decides whether that
is a purchasing constraint rather than a wiring one.

**D-112 THE ROLE REACH SWEEP IS ACCEPTED. EIGHT PLACES BEYOND THE OWNER'S FOUR, AND
NOTHING IS BUILT AGAINST D-105 UNTIL THE FIVE BREAKS ARE ANSWERED.**
audit/2026-09-03-role-reach-sweep.md. 41 items: **5 BREAK, 24 REQUIRE CHANGE, 8
DISSOLVE, 4 SURVIVE unchanged.**

**The owner's four were right and they were not the whole list.** The five breaks
are one family and F-081 is the sharpest: **C-03 and C-04 are role-dependent
recorded data with no re-measure trigger for a role change**, while the voiding
mechanism sits in the same document and is applied to C-01 on a driver or tube
change. **Applied to the figure whose wrongness is loud, not to the one whose
wrongness makes the check confirm the error.**

**THE POST-C-09 GAP IS REAL AND IT IS A SCHEDULING GAP, NOT A CAPABILITY GAP.**
C-09's new question (b) is a sufficient TEST and catches a wrong role whenever it
runs. **Nothing schedules it.** Three separate absences: **no trigger** - no file
names a role change as an event, not channel-token.md's four change cases, not the
eleven re-measure trigger rows, not software-spec.md 3.4's OUT OF SERVICE causes;
**no invalidation** - C-03 is not voided the way C-01 is; **and no detection** -
under G-32 as amended the signed check scores a wrong-role dose as PASS, because
the prediction moved with the error. **BOSS designs no mechanism. The gap is
stated and routed.**

**What did NOT reach, and it is worth as much as what did: nothing physical is
keyed to the pH pair being adjacent.** No cable core, insulation colour, duct,
gland or wall position, across twelve files named in the sweep. **And no frozen
interface row keys behaviour to a channel number** - S-15, S-16, S-17 and S-19 all
check clean. **So D-105 is a software and commissioning change, not a hardware
one**, which is why it can be taken this late without cost.

The other six: F-083, G-34's printed reason now false; F-084, "the fulvic channel"
against a role set fulvic is not in; F-085, six count-as-property claims; where
role definitionally LIVES, the register under D-057 or the controller's
blocked-channels path that no file in this tree shows; the acid-and-base physical
items that follow the assignment while the stations are fixed; and **"opposing" is
now a TIME-VARYING SET while an open window records which CHANNEL, not the role it
was opened under.**

**D-113 THE CH6 DEPENDENCY TRACE IS ACCEPTED. F-063 TRULY DISSOLVES, AND THE ONE
THING THAT SURVIVES IT SHOULD NOT.** audit/2026-09-03-ch6-dependency-trace.md. 63
items graded. **PAIR-IS-pH 25, PAIR-IS-ADJACENT 6, IDENTITY-OF-CH6 14, none of the
three 18. SURVIVES 25, NEVER-ABOUT-CH6 18, MUST-BE-REWRITTEN 13, DISSOLVES 7.**

**F-063 was TESTED claim by claim rather than assumed to dissolve**, and it is four
claims: the non-adjacency rule was never F-063's and traces cleanly to S-16; the
pair being CH5 and CH6 and adjacent dissolves; the 1000 mL compounding was already
withdrawn as F-071; and "not fixable by renumbering" has its premise removed,
because renumbering was only the sole fix while the pair was fixed to numbers.
**No residual smaller version. It dissolves.**

**WHAT SURVIVES THAT SHOULD NOT: D-099's frozen colour binding. F-082, and the
constraint has REVERSED DIRECTION.** Colour is bound to token and frozen. Role is
free at assignment. **So the frozen colour map now constrains WHICH TOKEN PAIRS MAY
BE GIVEN THE pH ROLES, and nobody has written that set out** - which
channel-token.md forbidden item 4 requires, since a set may not be computed. **And
the owner's carrier-availability lookup is still owed; the proposal says a reduced
palette protects the CH5-CH6 binding first, which would spend the strongest
separation on a pair that no longer means anything.**

**Nothing needs CH6 specifically going forward.** All 14 identity items dissolve or
rename to a role. **Nothing has been bought against it** - order.md and parts.md
carry no channel marker, colour or label line, checked. So the only cost of D-099
having been frozen on CH6 is a commitment, not a purchase.

**AND THE TRACE CAUGHT A SECOND-ORDER THING WORTH THE RUN ON ITS OWN: F-064 WAS
NEVER ABOUT CH6.** It is a reading of the Position axis, volume-independent and
role-independent, and it sits next to F-063 in the file. **D-088 and T-022 fought
once to keep it separate from F-071. D-105 is the second occasion that separation
paid.** Applying F-063's dissolution to everything filed near it would have lost
D-085's free half a second time. **Proximity in a file is not a dependency, and
this tree has now twice tried to treat it as one.**

**D-114 THE FILL VALVE IS A SOLENOID. THIS REVERSES D-111, WHICH IS KEPT.** Owner,
2026-09-03, within one exchange of proposing the opposite. **Energise to open,
spring closed on power loss.**

**The deciding property is the fail state and nothing else came close:**

| | Solenoid | Motorized ball valve |
|---|---|---|
| Power loss mid-fill | **Springs CLOSED** | **HOLDS POSITION. Leaves the fill open and the day tank overfills** |
| Shut speed | Instant | Several seconds of travel |

**"On a valve that fills a tank, hold-last is the wrong failure."** And the speed
half is not a separate point but the same one: **the float that stops the fill is
the only thing stopping it**, so a valve that takes seconds to close puts an
unmeasured volume past the float's switching point every time.

**EVERYTHING D-111 SAID ABOUT THE MOTORIZED VALVE'S CONSEQUENCES IS WITHDRAWN.**
The relay-arrangement fork on two, three and five wire types; the travel-time
number; the auxiliary position contact that would have been the only direct
confirmation in the water path. **All gone with the part.** D-111 stays on file
because a reversal keeps both entries and because the reasoning in it is what
produced G-39.

**WHAT SURVIVES FROM D-111 IS THE QUESTION, and the owner made the point rather
than BOSS: what a valve does on power loss is a DESIGN PROPERTY and not an
incidental one. For a solenoid the answer is closed, and that is why it is the
right part.** Frozen as G-39, above.

**ONE PHYSICAL FACT ADDED: the valve is installed with UNIONS EITHER SIDE so it
can be replaced without cutting pipe.** That is a maintenance property of the
installation, not of the part, and it survives any later change of valve.

**STILL OPEN AND WITH THE OWNER: voltage, pipe size, and whether it is normally
closed.** Requirement and search terms in findings.md under F-087, rewritten.
**BOSS names no part.**

**A NOTE ON THE THIRD OF THOSE, offered as a reading and not as a correction:**
"energise to open, spring closed" IS the definition of normally closed, so the
owner has already stated the requirement. **What the lookup is for is confirming
that a CANDIDATE PART meets it, which is a different act from deciding it** - and
it is worth keeping separate, because a solenoid sold as normally OPEN exists and
would satisfy every other line of the requirement.

**D-115 THE 1ST EDITION DOCUMENT SET IS RECEIVED UNDER THE OWNER'S CAVEAT AND
NOTHING IN IT IS ADOPTED.** Read 2026-09-03. Report in
audit/2026-09-03-1st-edition-floats-and-wall.md, headed with the caveat verbatim.
**The set itself is NOT in the working tree and is not committed** - it lives
outside it, so no artifact of it can become accountable by accident.

**The caveat is frozen as G-40** so it binds on subsystems that never read the
message it arrived in.

**24 float proposals and 26 wall proposals, every one written as "the old set
appears to show X, observed in the 1st Edition set, unverified, confirm or
replace."** That is the shape the owner asked for: he is a faster confirmer than
originator, and this turns two blank questions into two questions with a starting
proposal.

**TEN CONTRADICTIONS WITH THE TREE, ALL MARKED TREE-WINS AND NONE OF THEM A
FINDING ABOUT THE TREE:** board size against D-090's 8 by 8 ft; one enclosure
against the frozen four; wall-mounted receptacle boxes against D-046; **a motorized
ball valve against D-114 and G-39**, which is the same reversal arriving from two
directions on the same day; six channels against eight; a chiller pump on a
receptacle against D-108 and open F-086; the storage float pair as an add-on
against G-03; and mixed duty on one relay against G-30.

**AND SIX FIGURES THAT CONTRADICT THEMSELVES INSIDE THE OLD SET**, including one
float with two different trip heights across five documents, and two different
measurement datums used with the same numbers. **That is the strongest possible
argument for the caveat and it came from the set itself.**

**D-116 TWO ITEMS FROM THE OLD SET ARE GUARDED RATHER THAN PROPOSED, BECAUSE BOTH
COULD CLOSE AN OPEN QUESTION BY DEFAULT.**

**GUARD 1, AND IT IS THE MOST DANGEROUS THING IN THE SET. The old set closes
dry-run protection with the day tank low-low float, which is a LEVEL element.**

**That is precisely the choice S-05 is being held open to avoid foreclosing.**
S-05's row says a level element can never subsume circulation verification, and
D-060 prices the flow-proving fork at one timing element. **If the old set's answer
is adopted because it is the only answer on the page, D-060's door closes with
NOBODY HAVING DECIDED TO CLOSE IT** - which is T-023's mechanism arriving through a
document instead of through a claim.

**S-05 STAYS OPEN. No subsystem may cite the 1st Edition set for a dry-run element,
and WATER is told so directly.** The owner may of course decide it; what is
forbidden is it deciding itself.

**GUARD 2. The old set's floats are rated to switch a 120 VAC coil, and this
build's control voltage is 24 V.** F-089. **Under G-31 a minimum switching load is
ONE POWER requirement and not three independent floors, so a fifth of the voltage
at the same current is a fifth of the contact power.** It lands directly on S-01
and S-02, the two rows this whole pass exists to feed. **G-24 already says the
minimum switching load question is asked of EVERY contact; this is the first time
it has been asked of a float.**

**D-117 THE MOST VALUABLE THING THE OLD SET HAS IS A MECHANISM WITH NO NUMBER IN
IT, AND THE TREE HAS NO POSITION ON IT AT ALL: HOW A FLOAT IS PHYSICALLY HELD IN A
TANK.**

S-01 and S-02 both wait on WATER for "the physical location", and **nothing
anywhere in this tree says what a float is attached to.**

**The old set's answer is a STANDPIPE: one rigid pipe per tank carrying every float
and every cord, hung off the rim, with nothing hanging off a float body.**

**Why it is worth more than the 50 proposals around it: it contains no figure, so
it survives every number in the old set being wrong.** That is G-34's shape - a
rule keyed to what a thing IS rather than to how big it is - arriving from a source
where every dimension is suspect. **And it unblocks S-01, S-02 and CBL-04
together**, because a cord route is a consequence of a mounting method.

**And the tree already holds the principle without having applied it here.**
water.md says of the submersibles: **"Position held by fixture, not by cord. A
cord-hung pump is a pump whose position is a suggestion."** Nobody applied that
sentence to the floats.

**Two facts make a drifted float worse than a drifted pump, and both are already
frozen:** nothing in this system measures a level, so **a float that has moved is
invisible**; and D-114 establishes that **the fill-stop float is the only thing
stopping the fill.**

**IT IS STILL A PROPOSAL AND NOT A DECISION.** Observed in the 1st Edition set,
unverified. **BOSS adopts nothing, sizes nothing and names no part.** Put to the
owner as one question, with the tree's own sentence beside it.

## 2026-09-03, later still. S-05 closes, and the float pass restarts from requirements.

**D-118 F-090 IS CONFIRMED: parts.md's LS ROSTER IS 1ST EDITION LINEAGE, AND IT IS
STRUCK.** Owner's answer. **The roster in parts.md came from the same body of work
as the document set, not from an independent arrival.** So the authoritative file
was holding a 1st Edition fact under "established facts about real parts", and
confirming a float proposal against it would have been checking a document against
itself. **G-37's second-source illusion, confirmed inside parts.md.**

**Marked in place under G-40's terms rather than deleted**, so a later reader sees
what was there and why it went.

**THE FLOAT PASS RESTARTS FROM REQUIREMENTS: ask what a float must DO at each
position, then find a part. The old roster is ONE CANDIDATE and carries no priority
for having been there first.** F-089 goes into the requirement rather than into a
part comparison: **the 1st Edition floats switch a 120 VAC coil, this build's
control voltage is 24 V, and under G-31 that is a fifth of the contact power at the
same current.**

**The owner's note on why this is the best finding of the pass, recorded because it
is a standard rather than a compliment: IT STOPPED WORK RATHER THAN PRODUCING
IT.** An audit that prevents a circular confirmation has produced nothing visible
and saved the pass.

**D-119 S-05 CLOSES LEVEL-BASED. THE DRY-RUN INTERLOCK SENSES LEVEL, NOT FLOW.**
Owner's decision, 2026-09-03. **Everything in this system is level switches. There
is no flow element anywhere and there is not going to be one.**

**The decision arrives from the owner and NOT from the 1st Edition set.** D-116's
GUARD 1 refused the adoption and was correct to: the same answer arriving as a
decision is a different thing from the same answer arriving as an inheritance.
**Recorded that way deliberately, because a later reader must not conclude the
guard was pedantic.**

**TWO CONSEQUENCES, BOTH TAKEN KNOWINGLY BY THE OWNER:**

**1. THE SHARED SOLUTION IS CLOSED.** A level element cannot subsume circulation
verification: **it reads healthy through a fouled impeller, an air-locked volute, a
blocked intake or a shut valve.** WATER established that and it is why S-05 was
held open. It is now spent deliberately rather than by default.

**2. CIRCULATION VERIFICATION DOES NOT VANISH, AND D-060'S OVERSTATEMENT MUST NOT
RETURN HERE.** The owner's instruction, in his words: what is gone is **the free
version.** Three routes survive and all three are already on file:

| Route | Status |
|---|---|
| F-003 | **Separately assigned** under D-016, WATER primary, MAIN-PANEL the other end |
| C-12, the W-1 temperature-step witness | **Free.** C-12 calls it the only F-003 option that costs nothing and adds nothing |
| S-20 | **Exists on either fork**, because circulation is a pole on K-DRY under D-058 |

**This is T-024's exact shape being refused at the moment it would have recurred.**
D-060 said level-based means circulation verification is foreclosed permanently.
That clause was withdrawn by D-103. **The fork it described has now actually been
taken, and the withdrawn clause does not come back with it.** A claim about one
route stays a claim about one route even when that route is the one chosen.

**And D-060's OTHER half stands and is now spent: level-based means NO TIMING
ELEMENT.** The device D-060 priced is not bought.

**D-120 THE FLOAT ROSTER FROM THE 1ST EDITION DRAWINGS IS RECORDED AS OBSERVED AND
UNVERIFIED. THE HEIGHTS ARE NOT ADOPTED.** Owner's transcription, and it corrects
what he says he would otherwise have told BOSS from memory.

| Tank | Float | Function | Height as drawn |
|---|---|---|---|
| Day | LS-2 | high-high | **30 in** |
| Day | LS-5 | fill stop | not stated on the pages seen |
| Day | LS-1 | fill start | **11 in** |
| Day | LS-4 | low-low | **8 in** |
| Storage | LS-6 | fill start | not stated |
| Storage | LS-7 | fill stop | not stated |
| Storage | unnumbered | **STORAGE LOW pump-down float, not in the LS series** | not stated |

**LS-3 is captioned as being in storage. LS-8 is unaccounted for on the pages
seen.**

**THE HEIGHTS ARE T-018 CANDIDATES AND ARE NOT ADOPTED. 30, 11 and 8 inches are not
to be used by anything.** The owner names the reason and it is the strongest one
available: **height is exactly the class of figure the old set contradicts itself
on** - AUDIT found one float with two different trip heights across five documents,
and two different measurement datums used with the same numbers. **A number that
disagrees with itself inside its own source is not a seed, it is noise.**

**What the roster IS useful for: it names the POSITIONS a design has to have an
answer for.** Four on the day tank, two plus a pump-down on storage, and two
unaccounted-for numbers that are themselves a question. **Positions are a
requirement. Heights are a measurement nobody has taken on this build.**

**D-121 THE STANDPIPE IS ADOPTED AS THE MOUNTING METHOD. NOT AS A DIMENSION.**
Owner, D-117 accepted.

**One rigid pipe per tank carrying every float and every cord, hung off the rim,
with nothing hanging off a float body.**

**NO DIMENSION, NO MATERIAL, NO ATTACHMENT DETAIL, NO COUNT.** The owner's words
and they are the whole scope of the adoption. **What is adopted is a rule about
what holds what.**

**Why it can be adopted from a non-authoritative source when nothing else can: it
carries no figure, so it survives every number in the old set being wrong.** G-34
exactly - a rule keyed to what a thing IS rather than to how big it is - arriving
from a source where every dimension is suspect.

**The tree already held the principle and had not applied it here.** water.md, on
the submersibles: **"Position held by fixture, not by cord. A cord-hung pump is a
pump whose position is a suggestion."** It applies harder to a float: **nothing in
this system measures a level, so a float that has moved is invisible, and under
D-114 the fill-stop float is the only thing stopping the fill.**

**It unblocks S-01, S-02 and CBL-04 together**, because a cord route is a
consequence of a mounting method.

**D-122 THE ROLE VOCABULARY: EXACTLY TWO IS NOT ENFORCED, AND THE RULE IS
CONDITIONAL RATHER THAN COUNTED.** Owner, answering the question D-105 opened.

**Zero pH channels is legal. One is legal. Three is legal and foolish, and software
does not prevent it.**

**What must hold is CONDITIONAL, not counted: the signed attribution works from the
ROLE, not from the pair, so it works with one pH channel or with two.** That is the
property that makes the count irrelevant, and it is why the count does not have to
be defended.

**THE REWRITE, and it is a form rather than a judgement call.** The 25 items AUDIT
found assuming a pair are rewritten so that **"the opposing pH channel" becomes "a
channel with the opposing pH role, IF ONE IS ASSIGNED."**

**Anything that CANNOT be written that way is a real dependency on the pair, and is
LISTED SEPARATELY rather than forced into the form.** That instruction is the
valuable half: **the rewrite is a test, and the items that fail it are the finding.**
CONTROL-SOFTWARE returns that list.

**FULVIC IS A PRODUCT, NOT A ROLE, AND THERE IS NO FULVIC CHANNEL.** F-084 is
answered. **Fulvic is a NUTRIENT by role. Its property - that it does not move EC
meaningfully - is a PRODUCT ATTRIBUTE and lives in the channel register.**

**"The fulvic channel" is struck from all four files.** There is a channel whose
assigned product happens to be fulvic. **The distinction is not pedantry: a fixed
identity in four files is exactly what D-105 removed, and leaving one product's
identity keyed to a channel would have reintroduced the thing the decision
dissolved.** And it puts D-013's premise where G-33 says it belongs - **an
attribute of the product, recorded once, in the register.**

**D-123 F-081 IS FIXED BY RULE: ANY ROLE CHANGE VOIDS EVERY ROLE-DEPENDENT RECORDED
FIGURE.** Owner's instruction. **C-03 and C-04 are voided by a role change exactly
as C-01 is voided by a driver change or a tube change.**

**The owner's diagnosis is the part worth keeping: the voiding was applied to the
figure whose wrongness is LOUD, and not to the one whose wrongness makes the check
CONFIRM the error.** A wrong steps-per-millilitre shows up as a dose that looks
wrong. **A wrong signed reference makes the signed check expect the wrong direction,
so a wrong-role dose scores PASS.** The quiet failure was the one left unguarded.

**Three things follow and CONTROL-SOFTWARE implements all three, since D-112 found
three separate absences:** a role change becomes **a case in the change procedures**
- channel-token.md's cases, the re-measure trigger table, and software-spec 3.4's
OUT OF SERVICE causes; **an invalidation**, voiding C-03 and C-04 for that channel;
and **a re-measure trigger row** so the void has a route back. **C-09 is the test
and it now has an event that schedules it.**

**D-124 F-082: UNBIND. DO NOT REBIND.** Owner's ruling and it is the right shape.

**Colour was frozen to token and role became free, so the frozen colour map was
constraining which tokens may take the pH roles. Backwards.**

**Nothing physical is keyed to it and nothing was bought** - order.md and parts.md
carry no marker, colour or label line, checked by AUDIT. **So the binding is broken
at zero cost.**

| Before | After |
|---|---|
| Colour separation was a property of the CH5-CH6 pair | **Colour identifies the CHANNEL. Nothing more** |
| The pH separation rule constrained the colour map | **The pH separation is a rule at ASSIGNMENT: whatever two tokens take the pH roles must not have neighbouring colours** |
| Checked nowhere | **Checked at C-09** |
| The carrier lookup had to protect the CH5-CH6 binding first | **The carrier lookup runs against eight distinguishable colours with NO PAIR PRIVILEGED** |

**That last row is what the unbinding buys.** The owner's carrier-availability
lookup was going to spend the strongest separation in a reduced palette on a pair
that no longer means anything. **It now runs against a plain requirement: eight
colours that a person can tell apart.**

**And it dissolves F-082's other half for free.** channel-token.md forbidden item 4
required the permitted token pairs be written out rather than computed. **With the
binding broken there is no permitted-pairs set to enumerate: there is a rule
checked against whatever assignment exists.** A rule is not a set.

**D-125 F-086: THE CHILLER LOOP PUMP MAY BE SUPPLIED WITH THE CHILLER. OBSERVED,
UNVERIFIED, AND NOBODY DESIGNS AROUND IT EITHER WAY.** The 1st Edition drawing
shows it as a submersible that comes with the unit.

**If that holds it is not a separate load at all, and G-12 is wrong about there
being a loop pump to switch** - which would close F-086 by removing its subject
rather than by answering it.

**The owner will check his own hardware.** Under G-40 the drawing is a citation and
not a source. **F-086 stays OPEN and no subsystem designs for either outcome.**

