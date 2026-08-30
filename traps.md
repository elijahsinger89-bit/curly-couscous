# Traps

Failure modes this project has actually hit, written so the next agent
recognises one. Not hypotheticals. A trap goes in here after it has bitten.

## T-001 Splitting one discipline across two agents and calling the result a boundary

Hit on 2026-08-30, by BOSS, in the first agent proposal.

Storage-and-fill and day-tank-and-loops were proposed as two agents. The day
tank floats sat in one agent's tank and belonged to the other's fill chain. The
transfer pump discharged into the other agent's tank. The manifold suction and
return were two more crossings. Four seams between two agents doing the same
plumbing in the same room, for one builder.

How to recognise it: the split follows a process step, tap then storage then day
tank, rather than a physical thing. Count the crossings the split creates. If
the same person with the same tools works both sides and the crossings exist
only because of the split, it is not a boundary.

Corrected by merging into WATER. See decisions.md D-003.

## T-002 A seam that both agents end before reaching

Hit on 2026-08-30, by BOSS, in the same proposal.

PUMP-BOXES ended at the head barb. DOSING ended at the tubing back to the
manifold. Between them sat the nutrient jugs, the suction tubing, and how a jug
is placed and changed. Nobody owned it and the interface table would not have
caught it, because a crossing needs two named ends and this had none.

How to recognise it: read the scope-ends of every adjacent pair and ask what
physically sits between them. An unowned gap does not appear as a row in the
interface table. It appears as nothing at all, which is why it survives.

Corrected by giving the whole wet path to DOSING. See decisions.md D-006.

RECURRED 2026-08-30, found by DOSING, not by BOSS. The channel token: one
identity that has to ride from the software channel index through the pin map,
the cable, the driver, the head, the tube and the coupling to the jug station.
Four subsystems owned a fragment each and none owned the token. Same shape, same
reason it survived, and BOSS did not catch it the second time either. Now
interface S-19 and findings F-006.

The lesson from the recurrence: an interface table cannot show a missing owner,
only a disagreeing one. Reading the table finds neither. The thing that found it
both times was an agent asked to BUILD something that had to cross the gap.

## T-003 Asserting from absence

Not yet hit in this project. Seeded because BOSS's own instructions name it as
the single most common error in this pattern.

"There is no interlock for X" requires having looked at the file or the panel.
If you have not looked, the sentence is "I have not checked whether there is an
interlock for X." AUDIT is invoked without source access precisely so its output
is questions rather than assertions. Any agent that writes an absence claim must
name what it read to establish it.

Move this entry's first line when it is hit for real.

## T-004 A capability that exists only in the description

Hit on 2026-08-30, in the project description itself.

A "no-circulation fault" was named as something the Pi has, alongside a flow
cell "so the Pi knows whether the loop is moving". The flow cell turned out to
be a PVC body that holds the probes in the stream. It is a fitting, not an
instrument: no output, no contact, no wire. No sensor was ever specified. What
raises the named fault, or whether anything does, is still not established.

How to recognise it: a capability stated as a fact, sitting next to a physical
thing whose name sounds like an instrument. Flow cell, sight glass, sensor well.
Ask what wire leaves it. If nothing leaves it, no software can read it.

Cost of not catching it: DOSING would have built a section around a sensor that
does not exist, and CONTROL-SOFTWARE would have written a fault handler for a
signal that never arrives. Both would have passed their own checks.

What saved it: refusing to write the row. BOSS did not assert that nothing
existed, and did not assume something did. The row stayed OPEN and the question
went to the owner. See interface-table.md S-13 and S-14.

## T-005 Freezing a check without writing down what makes it late

Hit on 2026-08-30, by BOSS, freezing interface S-15.

EC rise during a dose was frozen as the accepted whole-loop check, with its three
limits attached: only during a dose, not per-channel, and blind to pH up, pH down
and fulvic. All true. What was not written is that the probes sit upstream of
every injection point, per G-10, so a probe reads the day tank and not the
manifold. Every one of these checks is therefore delayed by the time it takes a
dose to circulate back and mix, and nobody has measured that interval.

The owner named it when the same row was extended to pH. It applies identically
to the EC check that had already been frozen.

How to recognise it: a check is frozen with its limits listed, and every limit
answers "what can it not see" while none answers "when does it see". A
verification with no settling discipline cannot tell a dose that failed from a
dose that has not arrived yet, and it will report healthy doses as failures.

The general shape: a constraint that is frozen and correct, G-10, has a
consequence somewhere else that nobody wrote down. Freezing a row is not the
same as understanding what the row costs. See findings.md F-004.
