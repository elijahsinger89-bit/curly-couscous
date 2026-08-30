# Findings

Defects found and deliberately not fixed, with the reason each was left. BOSS
owns this file. A subsystem reports a boundary defect and never fixes it.

Absence note: a short file means little has been reported to BOSS. It does not
mean the design has been checked. Almost nothing has been checked.

| ID | Found by | Where | Defect | Why it was left | Date |
|---|---|---|---|---|---|
| F-001 | Owner, before any subsystem was invoked | Between DOSING, PUMP-BOXES and CONTROL-SOFTWARE | No per-channel dose verification exists, and none at rest | Open design question, routed. Options returned, see subsystems/dosing-verification-options.md. Nothing decided. No sensor added | 2026-08-30 |
| F-002 | DOSING, answering F-001 | The jug end of the wet path, Z3 and Z4 | A jug reconnected to the wrong channel after a change produces the exact F-001 symptom, a batch completing with one nutrient missing. No flow-measuring option catches it: eight healthy flow readings are fully consistent with two jugs swapped | Left open. It is a physical identity problem, not an instrument problem. The options that address it, O-09 identity at all three ends and O-11 keyed couplings, are among the cheapest on the list and neither is decided | 2026-08-30 |
| F-003 | BOSS, from DOSING's answer | F-001 limit 1, nothing verifies at rest | Unrouted. The circulation submersible sitting dead between batches is WATER's device on a MAIN-PANEL relay, not on DOSING's path. DOSING correctly declined it | ASSIGNED 2026-08-30 by D-016. WATER primary, MAIN-PANEL the other end. No longer in the gap | 2026-08-30 |
| F-010 | Owner, in parts.md | The 24 V rail, and everything on it | **The rail is not 24 V. It is whatever the NDR-240-24's front panel trimmer is set to: 23.76 to 28.28 V, with OVP not tripping until 29 V, and nothing fixes the trim position.** Every device on that rail sees whatever it is at, including eight driver VM inputs and two 24 Vdc contactor coils | Not fixed. Nobody has stated the 6121's VM range from its datasheet, and BOSS will not state it from memory. Routed to PUMP-BOXES to return the range, to MAIN-PANEL to set and record the trim, and to commissioning C-16 to record where it was left | 2026-08-30 |
| F-014 | PUMP-BOXES, on P-09 | Frozen decision G-09, and PUMP-BOXES' own frozen slice | **G-09 as written does not distinguish the two supplies.** It says the permissive "removes power from every stepper driver at once". That was written when everyone believed a stepper driver had one supply. parts.md has since established the 6121 has two: VM and a separate VDD logic supply. **Whether VDD is "power" under G-09 decides whether a permanently-live VDD is a legitimate option or a violation of a frozen row** | Not fixed. PUMP-BOXES correctly refused to rule on a frozen row and reported it. It is the owner's ruling and it blocks P-09 | 2026-08-30 |
| F-015 | PUMP-BOXES, reading commissioning.md in full | C-06 against any EN policy | **A de-energised stepper holds differently from an energised one.** C-06 tests whether the head holds against back-siphon with the jug above the inlet. So an EN policy of "disable everything not dosing" is not a free safety improvement: it may remove the holding torque C-06 is about to test for | Not fixed. The coupling is DOSING's and PUMP-BOXES' jointly and it was on no row. Recorded before either sets an EN policy | 2026-08-30 |
| F-013 | BOSS, reading parts.md against S-08 | MAIN-PANEL, the permissive readback contact | parts.md records the 22.32 as **2 NO, 25 A**, and lists no auxiliary block. The permissive readback at S-08 needs a contact. If the second NO pole is being used as the readback, then a 25 A power pole is switching a 3.3 V logic input, which is the textbook dry-circuit oxidation case and makes F-011 much worse than a general caution. BOSS does not know which pole is intended and is not assuming | Open, and a question to the owner: is there an auxiliary contact block on the 22.32 that is not in the parts list, or is the readback the second NO pole? | 2026-08-30 |
| F-011 | Owner, in parts.md | MAIN-PANEL contacts feeding the Pi | Minimum switching load differs by part: the 55.34 needs 300 mW at 5 V and 5 mA, the 22.32 needs 1000 mW at 10 V and 10 mA, and a contact switching below its minimum oxidises. **The two contacts that feed the Pi are exactly the low-current case:** S-03, the day tank fill-in-progress dry contact, and S-08, the permissive auxiliary readback. A 3.3 V logic input draws far less than either minimum | Not fixed. It is MAIN-PANEL's contact and DISPLAY-BOX's input circuit, and the fix is a choice between them. Reported because an oxidised contact fails intermittently and INTERMITTENTLY OPEN ON S-08 MEANS THE READBACK REPORTS A WELDED CONTACTOR THAT IS FINE, OR MISSES ONE THAT IS NOT | 2026-08-30 |
| F-012 | BOSS, against its own tree | The chiller loop submersible's tank | The owner stated in his second message that the second submersible sits IN THE DAY TANK. BOSS never wrote it down. WATER then searched F-08, P-05, water.md and dosing-f004-wet-side.md, correctly reported that no file stated it, and had to leave F-008 conditional on it | Fixed now, in parts.md and water.md. Recorded as a finding rather than quietly corrected, because the failure is BOSS's and it is the exact failure the tree exists to prevent: a fact stated once in conversation and never written down is a fact nobody has. It cost WATER a conditional it did not need to carry | 2026-08-30 |
| F-008 | WATER, on S-18 | Between G-12 and D-023 | G-12 puts the chiller and its loop pump on ONE contactor. So "hold the chiller off across settle windows" also stops the chiller loop submersible. If that pump sits in the day tank, D-023 removes a mixing source during exactly the window in which we are waiting for the tank to mix, and **lengthens the very interval it is applied across.** It buys read cleanliness with settle time | Not fixed. No file states which tank the chiller loop submersible sits in: WATER checked F-08, P-05, its own file and DOSING's. That placement is WATER's open item and is now load-bearing on t_settle in a way it was not before | 2026-08-30 |
| F-009 | WATER, reading commissioning.md in full | Commissioning | Two rows presupposed figures that no row produced: C-07 assumes a circulation flow number, and DOSING's derivation assumes a day tank working volume and fill band. Same shape as the C-08 gap | FIXED by adding C-10 and C-11. Recorded because it is the third instance of one pattern: a row that compares against a figure nothing schedules. Every instance was found by an agent reading the file, never by BOSS, who wrote it | 2026-08-30 |
| F-006 | DOSING, reading the whole interface table | Between CONTROL-SOFTWARE, DISPLAY-BOX, INTERCONNECT, PUMP-BOXES and DOSING | There was no interface row for channel identity or channel numbering. Four subsystems each own a fragment of one token and none owned the token | Opened as interface S-19 rather than left. Not fixed: the scheme, the carriers and the index belong to different agents and BOSS assigns none of them alone. The only check that closes it is C-09 | 2026-08-30 |
| F-007 | DOSING, from what makes the settling time drift | Probes, across DOSING and DISPLAY-BOX | No probe calibration or cleaning interval exists anywhere on file. DOSING read commissioning.md and all subsystem files; none names one. A fouled bulb or coated cell slows the response and widens the noise band, so a check calibrated at commissioning slowly becomes a false-fail generator, and a false-fail generator is what an operator switches off | Left open. Recorded as a re-measure trigger in commissioning.md, but the interval itself is nobody's yet | 2026-08-30 |
| F-005 | CONTROL-SOFTWARE, reading S-15 against F-004 | Interface row S-15, BOSS's own wording | S-15 says the EC check is "valid only during a dose". F-004 says the observable arrives after the dose. Taken literally together they define a window in which the evidence cannot appear | Not fixed. CONTROL-SOFTWARE reported it rather than acting on it, which is correct: S-15 is a FROZEN row and BOSS's. The reading it worked to is that the window is anchored to the dose and extends past it by the settling interval, but that is a reading, not what the row says. Owner to rule | 2026-08-30 |
| F-004 | Owner, from the S-16 constraints | Every implicit verification in the system | All of them read the day tank after recirculation, because the probes are upstream of every injection point. Each is therefore delayed by an interval nobody has measured. Named for pH at S-16, but it applies equally to the EC check at S-15 and was not stated when S-15 was frozen | Open and routed to DOSING and CONTROL-SOFTWARE between them. Not fixable by either alone and not a defect in either | 2026-08-30 |

## F-001 in full

What verification actually exists is implicit, not instrumented.

The Pi reads EC continuously. During a dose, EC rising confirms that the loop is
moving and that something was delivered, because a dead circulation pump or a
blocked manifold would leave it flat. That check is real, it costs nothing and
it already exists. Interface S-15.

Its three limits matter more than the check itself.

1. It only works DURING a dose. Between batches nothing moves and EC sits flat
   whether the circulation pump is healthy or dead. A failed pump at rest is
   indistinguishable from a healthy idle, and the first anyone knows is at the
   start of the next batch.
2. It confirms the MANIFOLD flowed, not WHICH head delivered. Eight heads inject
   into one stream and one EC reading cannot attribute the change. A single
   stalled head, a collapsed tube or a dry jug produces a batch that completes
   with one nutrient missing, and EC still moves because the other seven
   delivered. The probes also sit upstream of every injection point, so they
   read the tank rather than the result.
3. It says nothing about pH down, pH up or fulvic, which do not move EC
   meaningfully.

Compounding it, from decisions.md G-04 and G-05: nothing measures what a
peristaltic head actually delivered, and jug remainder is arithmetic against a
user-entered volume. A stalled head therefore also decrements its jug on paper.
The books and the jug diverge silently and nothing in the system compares them.

Status: not verified and not absent. Written as it is.

Routed as an open design question, not as a change:
- what would it take to confirm a per-channel dose moved
- what it would cost
- where it would land

DOSING answers for its path. Nobody adds a sensor. If the answer is a flow meter
per channel, the owner expects to decline it, and wants that recorded as a
decision he made rather than a gap nobody named.

## F-002 in full

The failure: a jug is changed and reconnected to the wrong channel. Every head
then delivers, every line flows, every instrument reads healthy, and two
nutrients are swapped. The batch completes with one nutrient missing from the
recipe's point of view, which is the F-001 symptom exactly.

Why it matters more than its cost suggests: it is the one failure on the wet
path that instrumentation does not touch. O-19, a flow meter on every dosing
line, the most expensive option on the list, reports eight healthy channels
while this is happening. So does O-16, the weigh platform, if the jugs share one
surface. The options that catch it are O-09, matched identity at head, both tube
ends and jug, and O-11, keyed or coded couplings that will not mate wrongly.
Both are near the bottom of the cost list.

Not decided. Recorded so that a verification decision is not made on flow
measurement alone while this stays open.

## F-003 in full

F-001 limit 1 says nothing verifies anything at rest: between batches the loop
is still and EC sits flat whether the circulation submersible is healthy or
dead, and the first anyone knows is at the start of the next batch.

DOSING was asked for options and correctly answered that this is not on its
path. The circulation pump is WATER's device, switched by a MAIN-PANEL relay,
and DOSING owns neither.

So the limit that started this whole thread is the one still unrouted. Recorded
here now, before either WATER or MAIN-PANEL is invoked, because it sits exactly
between them and each could reasonably assume the other has it.

## F-004 in full

The probes sit first in line, ahead of every injection point, per G-10. That is
correct and it is frozen: it stops injectate corrupting a reading. Its
consequence was not written down until now.

A probe therefore reads the day tank, never the manifold. Any change caused by a
dose appears only after that dose has travelled the manifold, entered the tank,
and mixed. Every implicit verification in this system is delayed by that
interval, and nobody has measured it.

This was named for pH when S-16 was frozen. It applies equally to the EC check
at S-15, which was frozen as the accepted whole-loop check without the delay
being stated. S-15 is now extended to say so.

What it changes: a check read too early reads flat and reports a healthy dose as
a failure. A check with no settling discipline at all cannot distinguish a dose
that failed from a dose that has not arrived yet. Both produce a verification
that is worse than none, which is the same shape as the stuck sight indicator
and the latched pressure switch in the option list.

Routed, not solved. DOSING and CONTROL-SOFTWARE between them return: what
settling time these checks require, what sets it, and whether it can be derived
from day tank volume and loop flow rate or has to be measured at commissioning.
If it is a measurement it goes on commissioning.md.

ANSWERED 2026-08-30, both sides. subsystems/control-software-f004.md and
subsystems/dosing-f004-wet-side.md. It must be measured, not derived. It is two
times, not one: t_first, before which a check is guaranteed flat, and t_settle,
before which a magnitude cannot be judged.

The sharpest thing to come out of it, and it is not about timing:

**The settling number's dominant input is the one thing this design cannot
observe, by choice.** Tank mixing is set by circulation flow. Nothing measures
flow: D-007 closed S-13, G-04 forbids meters. So flow degradation from a fouled
impeller, an intake screen, biofilm or scale lengthens the settling time
silently, and the check that depends on it drifts toward reporting healthy doses
as failures. That is not an argument for adding a meter. It is the reason the
re-measure trigger list in commissioning.md exists and is an event list rather
than a calendar.

## F-002 status, 2026-08-30

Owner ruling: F-002 outranks the option list. The finding is the inversion. A
jug on the wrong channel defeats every instrument in the list including O-19,
and the two things that catch it sit at the bottom of the cost list.

O-19 is off the table, D-014. Matched identity at head, tube and jug, and keyed
couplings, come back as their own proposal, separate from the nineteen, D-015.

## F-005 in full

S-15 as frozen: EC rise during a dose is the whole-loop check, "valid only
during a dose".

F-004: the probe reads the day tank, so the change appears only after the dose
has circulated back and mixed.

Literally, the check is valid only in a window during which its evidence cannot
have arrived. The row as written excludes the moment it is supposed to describe.

CONTROL-SOFTWARE built its answer on the reading that the window is anchored to
the dose and extends past the last step by the settling interval. It flagged that
this is an interpretation rather than what the row says, and did not act on it
further. That is the correct behaviour for a boundary defect.

This is the second consequence of T-005 to surface from the same freeze. The row
needs rewording and the rewording is a decision, not a costless fix, so BOSS has
not made it.

## F-006 in full

The chain is: software channel index, logic board output S-12, cable core,
driver, head in one of two boxes, head barb, tube, keyed coupling, jug station,
jug, product. One token has to ride all of it with no translation at any point,
because the operator's real workflow is "the UI says channel N is low, walk to
the wall, find N", and a translation step is performed by a person, at night,
from memory.

Until DOSING read the whole interface table, no row covered it. PUMP-BOXES owned
how the two boxes divide the channels. INTERCONNECT owned a labelling scheme for
conductors. DISPLAY-BOX owned the pin map. CONTROL-SOFTWARE owned the channel
index. Four fragments, no token.

What it costs if the ends disagree: a head labelled N but driven by software
channel N+1 doses the wrong product every batch, permanently, with no jug ever
touched. And it passes every check in the system. S-16 attributes a pH movement
to the channel that was commanded, so the pH check confirms a movement that came
from the wrong pump and reads healthy. G-05 decrements the wrong jug, so the
remainder warnings are wrong too and the jug that actually empties does so
without warning.

Opened as interface S-19. The only thing that catches it is C-09, the end-to-end
trace, which costs nothing and is possible only because G-06 serialises the
heads.

This is the second time T-002's shape has appeared: a thing that sits between
scopes and shows up in the interface table as nothing at all. Recorded there.

## F-008 in full

D-023 holds the chiller off across settle windows so that temperature does not
ride into the pH and compensated EC readings. WATER confirmed the direction and
then found what the decision did not say.

G-12 is frozen: the chiller and its loop pump are on one contactor, because the
chiller has no internal pump. There is no way to stop one without the other. So
the decision as written also stops a submersible.

If that submersible sits in the day tank, its return is a second mixing jet in a
tank whose only agitation is the circulation pump's bottom suction and the return
drop's plunge. F-004 leg 5 names mixing as the dominant leg of the settling time.
Switching a mixing source off for the duration of a settle window lengthens the
settling time being waited out.

The offsetting effect, also WATER's, is real and pulls the other way: the chiller
stratifies the tank, stratification suppresses convection and makes mixing worse,
and holding it off reduces stratification during the window. Which effect
dominates is not knowable from any file and is a matter for C-02 to measure, with
the chiller in its held-off state.

**RESOLVED 2026-08-30, and it resolves against D-023.** The chiller loop
submersible IS in the day tank. The owner stated it at the start and BOSS failed
to record it, which is F-012. So the conditional is not a conditional: holding the
chiller off DOES remove a mixing source from the day tank during the settle
window.

Combined with the temperature facts now on file, see D-025.

## F-003 status, 2026-08-30: the reframe

WATER's answer changed the question rather than answering it, and the reframe is
worth more than any of the options.

**No sense element can verify a stopped pump.** At rest a flow switch reads
no-flow, a current switch reads no-current and a pressure switch reads
no-pressure, and all three are the correct readings for a healthy idle pump. They
are also the correct readings for a dead one.

So the first half of F-003 is not a sensing question, it is a SCHEDULING
question. The only way to know a stopped pump is alive is to run it. An exercise
run on a rest interval, and unconditionally at batch start before the first dose,
costs nothing and adds nothing. Sensing only ever answers what witnesses the
exercise.

Options and their honest costs are in subsystems/water-s18-f003.md. WATER
recommends W-1, the temperature step at the probes when the standing column is
displaced, plus W-5, the operator's eyes at the return drop, because both are free
and neither forecloses anything, and holding the flow element pending the return
drop geometry. That is D-019's pattern applied again.

## Search terms for F-010 and F-011, requested by the owner 2026-08-30

BOSS states no figure for any of these. These are lookups, and the answers go into
parts.md when they come back.

**F-010, the 6121's VM range against a rail that can sit at 28.28 V:**
- Adafruit 6121 TMC2209 stepper driver breakout datasheet motor supply voltage range
- Adafruit TMC2209 breakout pinout VM VDD specifications
- TMC2209 datasheet absolute maximum ratings motor supply voltage
- TMC2209 recommended operating VM range

What is wanted is two numbers: the recommended maximum VM and the absolute maximum
VM, so the 28.28 V worst case can be checked against both rather than against one.
The absolute maximum is not a design limit, and a rail sitting near it is not the
same as a rail transiently reaching it.

**F-011 and F-013, whether the Finder contacts suit the two Pi-facing circuits:**
- Finder 22.32 datasheet auxiliary contact block accessory
- Finder 22.32 technical data minimum switching load
- Finder 55.34 minimum switching load gold plated contact option
- Finder 55.34 AgNi versus gold contact low level signal dry circuit
- relay contact dry circuit switching gold plated low level signal

What is wanted: whether either part is available with, or already has, a contact
material suited to a dry-circuit load, and whether the 22.32 takes an auxiliary
block at all. If the readback is the second 25 A NO pole, the question becomes
whether that pole can be made reliable at logic-level current or whether the
readback must be taken somewhere else entirely.
