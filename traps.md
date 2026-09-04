# Traps

Failure modes this project has actually hit, written so the next agent
recognises one. Not hypotheticals. A trap goes in here after it has bitten.

## T-029 A sound finding is not automatically a finding worth having

Called 2026-09-04 by the owner, on F-104, in four words: an unnecessary rabbit
hole.

**F-104 was correct.** A floor with a track drain is built to move water to the
track, so a leak goes to the track rather than to a sensor sitting elsewhere on it.
Nothing in the reasoning was wrong.

**It was still not worth having.** It would have cost a WATER pass, a placement
proposal, a price, and every later document that had to carry the qualification -
**to relocate a sensor that is fine where it is.**

**The mechanism, and it is this project's own success working against it.** Every
finding here has earned its keep, so the habit is to follow one wherever it goes.
**But the tree now generates findings faster than it consumes them, and a finding's
SOUNDNESS says nothing about its VALUE.** F-104 passed every test this project has
for whether a finding is real, and none for whether it is worth pursuing, **because
there was no such test.**

**The test, and it is one question: WHAT WOULD CHANGE IF THIS WERE ACTED ON, AND IS
THAT WORTH THE PASS IT COSTS?** If the answer is a device moved a few feet to catch
a failure mode nothing else in the build treats as urgent, file it and stop.

**It is the owner's earlier diagnosis arriving one level down.** He said the
analysis loop is self-sustaining and runs indefinitely without a document existing.
**T-029 is where that loop actually starts: not with a bad finding, with a good one
that nobody asked whether to follow.**

## T-028 A document written to stand alone re-buys what the base set already has

Found 2026-09-04 by the owner, in the 1st Edition set, and it is the one defect in
that set that would have cost money rather than time.

**The storage add-on sheet lists four float switches and four weights in its parts
table. Its own text, on the same page, says one of those four is already on the
panel and only three arrive with the add-on. Three new, four listed.**

**Buy per the base sheet and then per the add-on sheet and you get nine floats for
eight positions.**

**The cause is structural and it is not carelessness.** An add-on document is
written to be handed to someone who may not have the base set in front of them, so
**it states its whole scope rather than its increment** - and that is the right
instinct for the ASSEMBLY sections, which have to be followable alone. **The parts
table inherits the same instinct and becomes wrong**, because a parts table is the
one section whose meaning is a DELTA against what already exists.

**The tell is that the sheet contradicts itself rather than the base sheet.** The
text says three, the table says four, on one page. **Nobody reconciled the totals
because the document was never read against the base set - which is exactly what
"written to stand alone" means.**

**Why this build has to care.** The generated set is not started yet and will have
the same shape: **a main package and an add-on, or a first edition and a
revision.** So the rule arrives before the documents do.

**The recognition test.** For any document that supplements another, ask of each
section: **is this section's meaning ABSOLUTE or is it a DELTA?** Assembly steps
are absolute and should repeat. **Quantities, counts and totals are deltas and must
never repeat.** If a table can be read as either, it will be read as absolute by
whoever is holding a credit card.

**And it is the T-018 family seen from a new side.** T-018 was a seed read as a
measurement. **This is an increment read as a total.** Both are a number whose
MEANING depends on a context that did not travel with it.

## T-027 Proximity in a file is not a dependency. Twice now.

Hit twice, 2026-09-02 and 2026-09-03, and it is a pattern because it is twice.

**F-064 sits next to F-063 in findings.md. It is a reading of the Position axis:
volume-independent, role-independent, and about neither the jug sizes nor the pH
pair.** It has now twice been at risk of being withdrawn along with a neighbour it
does not depend on.

| When | What nearly took it |
|---|---|
| 2026-09-02 | **BOSS filed DOSING's withdrawn narrowing under F-064's label.** DOSING caught it. The narrowing was withdrawn; the opening stands. T-022, split into F-071 and F-064 |
| 2026-09-03 | **D-105 dissolved F-063.** Applying that dissolution to what was filed near it would have taken F-064 with it - and D-085 spends F-064 in the other direction, so **the free half would have been lost a second time** |

**The mechanism.** A file is a one-dimensional list and a dependency graph is not.
**Two items land next to each other because they were written on the same day or
about the same area, which is a fact about the AUTHOR's attention, not about the
items.** When one is withdrawn, the reader's eye supplies a relationship the file
never asserted.

**It is worse in a findings file than anywhere else**, because a finding is written
at the moment of noticing, so **filing order is chronological, and chronological
order is the strongest possible generator of accidental adjacency.**

**The recognition test.** When you withdraw, dissolve or narrow an item, do not
look at what is NEAR it. **Search for what CITES it.** If nothing cites the
neighbour, the neighbour is not affected, however similar it looks. **And if you
find yourself saying "and the one below it too", stop: that sentence has no
argument in it.**

**What caught it both times was an agent that had the item's own argument in hand.**
DOSING the first time, AUDIT's dependency trace the second. **Neither found it by
reading carefully. Both found it by asking what the item actually rests on.**

## T-026 The deciding property was not the first thing either of us looked at

Hit on 2026-09-03, by the owner, on his own part choice, and caught by him within
one exchange.

He named the fill valve a motorized ball valve, reasoned about it for a paragraph -
wiring types, travel time, position feedback, four consequences to work through -
and then withdrew it. **The deciding property was the fail state, and it was not
what either of us examined first.**

**A motorized ball valve holds position with no power. On a valve that fills a
tank, hold-last is a flood.** Nothing in the paragraph of consequences reached
that; the paragraph was about how to drive it and how to read it.

**Why this is a trap and not just a correction.** The properties that are easy to
reason about are the ones with numbers and options: voltage, wire count, travel
time, feedback contacts. **The fail state has no options. It is one word, it is
often not on the front page of a datasheet, and it does not generate any
interesting design work - which is exactly why the reasoning went elsewhere
first.** An hour of good thinking about relay arrangements is an hour spent on a
part that was already wrong.

**The recognition test.** If you are choosing an actuator and you have started
reasoning about how to WIRE it, stop: you skipped a step. **Ask what it does with
no power. If you cannot answer in one word, you are not ready to think about
anything else.**

Frozen as G-39, beside G-22 deliberately. **G-22 asks what a severed conductor does
and what a short to a neighbour does. Neither asks what a DEAD PANEL does, and an
actuator is the only class of device where that is a different question.**

**And the reversal cost one exchange because he had not built anything on it yet.**
Same shape as F-059 and the DIR level: the cheapness of a correction is set by how
much was built on the guess, not by how wrong the guess was.

## T-025 Knowing a pattern does not stop you producing it. The interval was four entries.

**Put at the top at the owner's instruction, 2026-09-03, and it belongs there.**

D-101 caught document 12 running two questions together in one sentence: the
command half of a claim, which was structural, and the observe half, which was not.
BOSS wrote the finding, froze G-36 out of it, and routed it.

**Four entries later, in D-097, BOSS did the same thing.** "C-18 is now the only
route" ran together what a driver DOES with VM absent, which is structural as far
as documentation goes, and whether the Pi can KNOW the permissive dropped, which is
current and which S-08 already answers. **It was caught by an audit, not by the
agent that had just written the rule against it.**

**Four instances across both builds now, all self-caught, none caught at the moment
of writing.** The parallel build has three.

**What this does NOT mean.** It is not an argument for more care, and "be careful"
is not a mitigation. **The recognition test is the interval: the closer you are to
having just articulated a pattern, the more confident you are that you are not
committing it, and confidence is the thing that removes the check.** A rule you
froze this morning does not inspect your afternoon.

**What actually caught all four was a second reader with the rule in hand and no
memory of having written it.** That is an argument for the audit cadence, not for
introspection.

## T-024 A claim about ONE ROUTE escalated into a claim about ALL ROUTES

Hit on 2026-09-03, found by AUDIT grading decisions.md. **Distinct from T-023 and
the owner named the distinction: the escalation happens in the SUMMARY rather than
in the argument.**

S-05's frozen row says a LEVEL element cannot subsume circulation verification.
That is a claim about one element: this device senses supply, so it reads healthy
through a fouled impeller and cannot witness flow.

**D-060's summary line says circulation verification is foreclosed PERMANENTLY.**
That is a claim about every route. Nothing in the argument above it supports the
jump, and three other routes were on file the whole time: F-003 separately assigned
under D-016, C-12's W-1 transient, and S-20, which exists on either fork.

**Why the summary is where it happens.** The argument names its subject and stays
with it. The summary compresses, and compression drops the qualifier before it
drops the claim. **"This element cannot" becomes "it cannot" becomes "it is
impossible", and each step reads as the same sentence to whoever wrote it.**

**The recognition test.** When a line says something is foreclosed, ask what the
SUBJECT of the sentence above it was. If the argument was about one device, one
signal, one fork or one file, and the summary is about the capability, the
escalation happened in between. **And under G-36 that is now a grading error as
well as a wording one: a claim about one route is CURRENT by construction, because
the other routes are what would change it.**

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

### The second method, from the third instance

The third instance was the pump tube, interface FL-10. PharMed BPT B25: wetted, a
consumable at about 1000 hours, living inside PUMP-BOXES' head and forming part of
DOSING's wet path. D-006 gave DOSING the wet path and stopped PUMP-BOXES at the
barb, and the tube fell between them.

**It did not surface from reading the table. It surfaced when an external fact
arrived** - a manufacturer spec sheet naming a consumable nobody had known was
there. Nothing in the tree implied it, because nothing in the tree knew the head
had a serviceable tube in it.

So there are two methods, not one:

1. **Assign work that cannot proceed without crossing the gap.** Found instances
   one and two.
2. **Re-read the seams every time an external fact arrives.** A new datasheet, a
   measured figure, a part in hand. New facts create seams that did not exist when
   the table was written, and they expose seams the table never had words for.
   Found instance three.

Both are cheap. Neither is inspection.

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

## T-016 A sense path that fails to the wrong state: reach for the other contact, not more logic

Hit on 2026-08-30. S-03, the day tank fill-in-progress contact.

The contact was wired so that closed meant a fill was in progress. So contact open
meant no fill, and a severed cable read as **permission to dose**. With dosing
during a fill forbidden, that is the unsafe direction: the failure grants the
permission instead of withdrawing it.

The reflex fix is software: qualify the input, cross-check it, add a timeout, treat
a suspiciously long "no fill" as suspect. **Every one of those is logic added to
compensate for a contact chosen the wrong way round, and none of them makes a
severed cable safe.**

The actual fix was the other contact. Use the normally closed contact, so closed
means no fill and open means filling. Then a severed cable reads as filling, dosing
is inhibited, and the failure is a stop rather than a permission. Same relay, same
wetting circuit, same current, different pole.

**The general form: when a sense path fails to the wrong state, the first fix to
reach for is THE OTHER CONTACT, not more logic. Software cannot make a severed
cable safe. Contact selection can.**

G-22 is satisfied by wiring, which is where it should be satisfied.

## T-017 The chain that can never start

Found on 2026-08-30 by MAIN-PANEL, tracing rather than inspecting. Not built, and
caught before it was.

The panel is short of coils, so the cheapest fix was to put the dry-run element
straight into the permissive series string, which costs zero relays and looks
obviously correct.

**A flow-proving element reads open at rest and open through every start-up
transient. In the string: the permissive cannot latch until there is flow. There is
no flow until the pump runs. The pump needs the permissive.**

A chain that can never start. Every element in it is individually correct and the
loop is dead.

How to recognise it: a condition is added to an enabling chain, and the condition
is itself produced by something the chain enables. **Ask of every element in a
permissive or interlock string: what makes this element true, and does the string
have to be closed first for that to happen.** A state diagram will not show it. Only
tracing the loop by hand does, which is the same discipline T-007 demands of an
open-collector return.

This is T-007's shape applied to a chain rather than to a coil, and it is worth its
own entry because the string version is the one that gets designed in for free
under budget pressure.


## T-018 A seed value read as a measurement of the world

Hit on 2026-09-02, by BOSS, and it propagated into three conclusions and one decision
before the owner caught it.

config.yaml carries a per-channel volume: 4000, 1000, 3785. **They are DEFAULTS. Every
one is a seed that gets overwritten on the Pumps screen with the volume the owner
actually enters. CH7 and CH8 carry 3785 because that was the closest seed to a US
gallon, and for no other reason.**

BOSS read them as container sizes, recorded them as facts in the channel register, and
built on them: that the two 1000 mL channels are the pH adjusters, so the size axis
separates the pH pair from the six nutrients for free; that the smallest containers are
therefore handled most often; and three depth classes for a suction pickup nobody has
specified. **DOSING then did honest work against all three.**

How to recognise it: **a number that came out of a configuration file, a template or a
fixture, being cited as though someone had measured something.** The tell is that it is
suspiciously round, or suspiciously conventional, or the same across several entries
that have no reason to agree. 3785 is a US gallon in millilitres. **A number that is a
unit conversion is a number somebody typed, not a number somebody measured.**

The general form, and it is one step past T-012: **T-012 says a quantity asserted
rather than derived will be correct until the data moves. This says a quantity may be
neither asserted nor derived but SEEDED, and a seed is not evidence about the world at
all. Ask of any figure: did this come from the world, or from a file that had to
contain something.**

The register now separates three quantities that were being treated as one: the seed,
the container's capacity, and the volume actually poured. **Only the third is what the
jug arithmetic runs on, and none of the three was the same number.** That separation is
frozen as G-33 and is the standing shape, not a local fix.

**Three more from the parallel build, supplied by the owner 2026-09-02, all caught by
the same question and all later treated as measurements: a 41.7 mA loop current, a
24 AWG resistance constant, and an optocoupler forward voltage. All three were figures a
file had to contain.**

## T-019 Partial scepticism

Hit on 2026-09-01 by DOSING, and caught by DOSING itself the next day.

It argued that the two smallest containers are the pH channels, so the pair the system
most wants left alone is the pair handled most often. **In the same argument it
explicitly REFUSED to estimate the consumption rates, because nobody has them.** What it
did not notice is that **the VESSEL half of the argument was no firmer than the rate
half** - both were seeds.

**Careful about one input and credulous about another, in the same sentence.**

How to recognise it: a paragraph that names one term as unavailable and refuses to
estimate it, while treating a second term of the same argument as given. **The
scepticism is real and it is aimed at one term only.** The refusal even makes the
argument LOOK rigorous, which is what lets the other half through.

The test: **when you decline to estimate a term, ask what quality of evidence the OTHER
terms in that same argument rest on. If any of them is weaker than the one you just
refused, the refusal was not scepticism, it was selective.**

## T-020 A correction stated after the step it modifies

From the parallel build, and it cost stock rather than rework.

A build procedure said at step 7 "cut each cable to the length recorded", and at step 8
"add 100 mm at each end before cutting". **A builder running in order cuts at 7 and
reads 8 too late. Five cables, 200 mm short each, and a cut cable cannot be un-cut.**

**Every other ordering defect in that read cost rework. That one cost stock.**

The general form: **any step that states an allowance, an offset, a correction or a
precondition must not come after the step it modifies.**

And the fix that matters more than the ordering: **the answer was not to swap the two
steps. It was to FOLD THE ALLOWANCE INTO THE CUT STEP, because two steps that must be
read in order is what produced the defect.** Swapping them leaves the same mechanism in
place for the next reader.

## T-021 The question to ask of a file depends on what kind of file it is

From the parallel build, learned by reading three software files in sequence.

**A file that holds a STATE MACHINE produces two families:**
- **UNTESTED JOINS.** The parts are correct and individually tested, and the thing
  joining them is never exercised.
- **HALF-WIRED MECHANISMS.** Created, connected at one end, never connected at the
  other. **An event created and read and never set. A function returning None into
  callers that do arithmetic on it. A refcount that nothing holds.**

**A file that is a ROUTING LAYER produces NEITHER, because it holds no mechanisms. Its
defects are the defects of a boundary: wrong assumptions about what is on the other
side, and stale references to things deleted elsewhere.**

**So asking the state-machine question of a routing layer finds nothing**, and a clean
result there is not evidence of anything. **Classify the file first, then choose the
question.** A review that asks one question of every file is a review that is looking in
the wrong place most of the time and reporting silence as health.

## T-022 A withdrawn claim filed under a surviving claim's label

Hit on 2026-09-02, by BOSS, and caught by DOSING.

DOSING made two separate points in one return: an OPENING, that the ordering rule
constrains sequence and not spacing, and a NARROWING, that the size axis already
separates the pH pair for free. **BOSS filed both under F-064's label.** When the
narrowing was retracted, the qualification landed on the label - and the label was
carrying the opening too.

**Why it was not tidy-up: a decision made the same day, D-085, spends the OPENING. Take
whatever spacing the existing run already gives. A later reader finding F-064 marked as
resting on a retracted inference would have withdrawn the opening along with the
narrowing, and lost the free half of a decision, leaving only the expensive half on the
table.**

**The consequence is in the future, which is the hardest kind to see.** Nothing is
wrong today. The defect is a landmine set for whoever reads next.

How to recognise it: **a return makes more than one claim and one label goes on top of
all of them.** Ask of every retraction: **what ELSE is filed under the label I am about
to qualify, and does any of it survive?** If it does, split before qualifying, not after.

## What survived the seed retraction, and why it is a rule

**Anything keyed to ROLE rather than to VOLUME survived intact.** CH5 is pH-down because
the controller marks it so, not because of a number. DOSING's hazard rule - no acid or
base container stationed where breaking or lifting it puts it above the operator's
forearms - survived for the same reason.

**A rule keyed to what a thing IS outlives a rule keyed to how big it is.** Sizes are
provisional until something is bought. Roles are decided earlier and change less.
**Where a rule can be written against a role rather than against a dimension, it should
be.**

## T-023. A claim of impossibility propagates. A claim of fact gets re-derived.

BOSS accepted document 12, banked its structural claims in D-095, and hours later
wrote one of them into commissioning C-23 citing document 12 as the authority. The
claim was then in two files, one citing the other, and **neither cited D-060, which
contradicts it, or S-20, which is the row that would deliver the capability.**

**The mechanism, and it is not carelessness.** When an agent needs a FACT it goes
and gets it, because it has to build on it and a wrong one shows up in the build.
When an agent is told something is IMPOSSIBLE it stops, because there is nothing to
build and therefore nothing to check the claim against. **The claim's own content
removes the occasion to test it.** That is why it travels further and faster than
anything true.

**And it is self-fulfilling where the impossibility is only CURRENT.** D-060 prices
the flow-proving fork of S-05 at one timing element. Nobody pays for a capability
they have been told is impossible. Decline to pay and the fork closes, and the
false claim becomes a true one, with no step in between that anyone would notice.

**The recognition test.** When you write or copy the word "cannot", ask which grade
it is under G-36 and what would change it. If you cannot name what would change it,
you have not established that nothing would. **The absence of a route is not the
absence of a possible route, which is T-003 arriving on capabilities instead of on
files.**

**What caught it was not review. It was the owner's extra instruction** to ask
whether anything stated as structurally impossible is only currently impossible.
Nobody had asked that question of any document before, and it found six.

