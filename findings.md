# Findings

Defects found and deliberately not fixed, with the reason each was left. BOSS
owns this file. A subsystem reports a boundary defect and never fixes it.

Absence note: a short file means little has been reported to BOSS. It does not
mean the design has been checked. Almost nothing has been checked.

| ID | Found by | Where | Defect | Why it was left | Date |
|---|---|---|---|---|---|
| F-001 | Owner, before any subsystem was invoked | Between DOSING, PUMP-BOXES and CONTROL-SOFTWARE | No per-channel dose verification exists, and none at rest | Open design question, routed. Options returned, see subsystems/dosing-verification-options.md. Nothing decided. No sensor added | 2026-08-30 |
| F-002 | DOSING, answering F-001 | The jug end of the wet path, Z3 and Z4 | A jug reconnected to the wrong channel after a change produces the exact F-001 symptom, a batch completing with one nutrient missing. No flow-measuring option catches it: eight healthy flow readings are fully consistent with two jugs swapped | Left open. It is a physical identity problem, not an instrument problem. The options that address it, O-09 identity at all three ends and O-11 keyed couplings, are among the cheapest on the list and neither is decided | 2026-08-30 |
| F-003 | BOSS, from DOSING's answer | F-001 limit 1, nothing verifies at rest | Unrouted. The circulation submersible sitting dead between batches is WATER's device on a MAIN-PANEL relay, not on DOSING's path. DOSING correctly declined it | Left open pending routing to WATER and MAIN-PANEL. Recorded now so it does not vanish between the two agents that could each assume the other has it | 2026-08-30 |

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
