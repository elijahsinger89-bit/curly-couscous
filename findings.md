# Findings

Defects found and deliberately not fixed, with the reason each was left. BOSS
owns this file. A subsystem reports a boundary defect and never fixes it.

Absence note: a short file means little has been reported to BOSS. It does not
mean the design has been checked. Almost nothing has been checked.

| ID | Found by | Where | Defect | Why it was left | Date |
|---|---|---|---|---|---|
| F-001 | Owner, before any subsystem was invoked | Between DOSING, PUMP-BOXES and CONTROL-SOFTWARE | No per-channel dose verification exists, and none at rest | Open design question, routed. Not a defect in any one subsystem, which is why it would otherwise go unowned. No sensor is to be added | 2026-08-30 |

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
