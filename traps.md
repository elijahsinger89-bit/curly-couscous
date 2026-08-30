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

### The method, and this is the lesson rather than the token

An interface table cannot show a missing owner. It can only show a disagreeing
one. Reading the table finds neither, and the table was read carefully both
times by BOSS and both times the gap was invisible.

**To find an unowned seam, do not review the interface table. Assign work that
cannot proceed without crossing it.** Both times the gap was found by an agent
told to build something that had to reach across it: DOSING asked to own the wet
path found the jug and suction gap, and DOSING asked to propose channel identity
found that nobody defined a channel. Neither was found by inspection.

This is the same rule already in agents.md for stalled threads, promoted to a
method: reviewing finds nothing, using finds everything. It applies to seams that
are missing, not only to seams that are contested.

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

# Traps carried in from prior work on THIS EXACT HARDWARE

Supplied by the owner 2026-08-30. These are not hypotheticals and not general
wisdom. Each cost several sessions. They are written here so the next agent
recognises one rather than finding it the slow way.

## T-006 An open-collector device sinks and cannot source

A ULN2003 or any open-collector device SINKS. If it drives a coil, the coil
positive comes from the supply and the device takes the RETURN.

Getting it backwards produces a coil that can never operate, **and every check
still passes**, because each end looks correct in isolation.

Live relevance: DISPLAY-BOX's logic board drives relay and contactor coils that
belong to MAIN-PANEL, interfaces S-07 and S-09. Both ends of that crossing must
state which side is the supply and which is the return before either is built.

## T-007 An open-collector driver on a remote board needs a shared common

No shared common conductor back to the supply it switches against means no
current flows. **Both ends of the wire can land correctly and the circuit still
does nothing.** Trace the loop by hand.

Live relevance: the logic board is in the display box and the coils are in the
main panel, 4 ft apart. That is exactly the remote-board case.

## T-008 A cable declared as N conductors is not N landed conductors

Count LANDINGS, never the jacket. Cables declared six and landed two happened
twice.

## T-009 A terminal carrying exactly one conductor is an open circuit, not a spare

## T-010 Count clamps against conductors

Two bus terminals landed twelve conductors on eight clamps for months.

## T-011 Colour is not identity unless it is unique in the jacket

Two conductors in one jacket cannot share a colour. A colour that changes at a
terminal must be documented, or a builder assumes it is an error and "fixes" it.

## T-012 A quantity asserted rather than derived

It will be correct until the data moves, **and nothing will tell you when it
stops being correct.** Seven separate instances occurred.

The fix is always the same: **derive it, or make the check an identity rather than
a bound.** A bound passes while the number drifts. An identity fails the moment
the two sides disagree.

## T-013 A procedure step that names a terminal by list index

It follows the index and not the meaning when the data behind it changes. One such
step instructed a builder to verify a short across a 5 V supply and tick the box.

Names, never positions. This is the same disease as the positional channel list
forbidden in channel-token.md.

## T-014 A check whose condition is a literal True

It passes forever and hides exactly what it names. A green check is evidence of
nothing until you have read what it tests.

## T-015 The most expensive class: a part substitution that looks like a naming problem

The package was designed for an opto-isolated driver. A non-isolated CMOS breakout
was bought. That single substitution produced:

- wrong pin names
- a missing logic supply
- two returns bonded on one pin
- a parallel return path
- a ground loop

**They were reported as six findings and they were one cause.**

How to recognise it: several findings appear at once, in different subsystems,
each individually plausible and individually small, and each fix is a rename or a
rewire. Stop and ask what part the design assumed. Six symptoms with one
substitution behind them is cheaper to fix once than six times.

**LIVE RIGHT NOW.** The Adafruit 6121 IS a non-isolated CMOS breakout with screw
terminals, a separate VDD logic supply, no differential pairs and no opto. See
parts.md. Anything in this project that was drafted assuming an opto-isolated
differential step and direction interface is already wrong and must be re-read
against the real pin list before it is built. Interfaces S-10 and P-06.

## The method that found most of them

**Not review, and not auditing a document against itself.** Every serious defect
surfaced when one subsystem had to BUILD against another and could not proceed
until it knew what a real part actually does.

**A model checked against itself is self-consistent, not verified.**

This is the same method already recorded under T-002, arrived at independently
from real build experience. Two separate lines of evidence for one rule.
